#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

from io import BytesIO
import os
import ssl
import sys
import warnings
import base64
import socket  # Ensure socket is imported for socket.error
import logging  # Added for logging

from six.moves import urllib
from six.moves import http_client

from .TTransport import TTransportBase, TTransportException
import six

_LOGGER = logging.getLogger(__name__)


class THttpClient(TTransportBase):
    """Http implementation of TTransport base."""

    def __init__(self, uri_or_host, port=None, path=None, cafile=None, cert_file=None, key_file=None, ssl_context=None):
        """THttpClient supports two different types of construction:

        THttpClient(host, port, path) - deprecated
        THttpClient(uri, [port=<n>, path=<s>, cafile=<filename>, cert_file=<filename>, key_file=<filename>, ssl_context=<context>])

        Only the second supports https.  To properly authenticate against the server,
        provide the client's identity by specifying cert_file and key_file.  To properly
        authenticate the server, specify either cafile or ssl_context with a CA defined.
        NOTE: if both cafile and ssl_context are defined, ssl_context will override cafile.
        """
        if port is not None:
            warnings.warn(
                "Please use the THttpClient('http{s}://host:port/path') constructor",
                DeprecationWarning,
                stacklevel=2)
            self.host = uri_or_host
            self.port = port
            assert path
            self.path = path
            self.scheme = 'http'
        else:
            parsed = urllib.parse.urlparse(uri_or_host)
            self.scheme = parsed.scheme
            assert self.scheme in ('http', 'https')
            if self.scheme == 'http':
                self.port = parsed.port or http_client.HTTP_PORT
            elif self.scheme == 'https':
                self.port = parsed.port or http_client.HTTPS_PORT
                self.certfile = cert_file
                self.keyfile = key_file
                self.context = ssl.create_default_context(cafile=cafile) if (cafile and not ssl_context) else ssl_context
            self.host = parsed.hostname
            self.path = parsed.path
            if parsed.query:
                self.path += '?%s' % parsed.query
        try:
            proxy = urllib.request.getproxies()[self.scheme]
        except KeyError:
            proxy = None
        else:
            if urllib.request.proxy_bypass(self.host):
                proxy = None
        if proxy:
            parsed = urllib.parse.urlparse(proxy)
            self.realhost = self.host
            self.realport = self.port
            self.host = parsed.hostname
            self.port = parsed.port
            self.proxy_auth = self.basic_proxy_auth_header(parsed)
        else:
            self.realhost = self.realport = self.proxy_auth = None
        self.__wbuf = BytesIO()
        self.__http = None
        self.__http_response = None
        self.__timeout = None
        self.__custom_headers = None
        self.headers = None

    @staticmethod
    def basic_proxy_auth_header(proxy):
        if proxy is None or not proxy.username:
            return None
        ap = "%s:%s" % (urllib.parse.unquote(proxy.username),
                        urllib.parse.unquote(proxy.password))
        cr = base64.b64encode(ap.encode()).strip()
        return "Basic " + cr

    def using_proxy(self):
        return self.realhost is not None

    def open(self):
        """Open the HTTP transport."""
        try:
            if self.scheme == 'https':
                try:
                    # Create SSL context
                    context = ssl.create_default_context()
                    if self.context and self.context.verify_mode is not None:
                        context = self.context
                    if self.certfile:
                        # key_file can be None if the private key is embedded in the cert_file
                        context.load_cert_chain(self.certfile, keyfile=self.keyfile)

                    self.__http = http_client.HTTPSConnection(
                        self.host, self.port,
                        timeout=self.__timeout,
                        context=context
                    )
                except Exception as e:
                    _LOGGER.warning('SSL setup failed: %s', str(e), exc_info=True)
                    self.__http = None  # Ensure __http is None on SSL setup failure
                    raise TTransportException(
                        type=TTransportException.SSL_ERROR,
                        message='SSL setup failed: %s' % e
                    )
            else:  # 'http'
                self.__http = http_client.HTTPConnection(
                    self.host, self.port,
                    timeout=self.__timeout
                )

            self.__http.connect()

        except (http_client.HTTPException, socket.error, socket.gaierror) as e:
            # This block catches errors from self.__http.connect() or HTTPConnection/HTTPSConnection instantiation
            _LOGGER.warning('Connect failed: %s', str(e), exc_info=True)
            self.__http = None  # Ensure __http is None on connect failure
            raise TTransportException(type=TTransportException.NOT_OPEN, message=str(e))

    def close(self):
        self.__http.close()
        self.__http = None
        self.__http_response = None

    def isOpen(self):
        return self.__http is not None

    def setTimeout(self, ms):
        if ms is None:
            self.__timeout = None
        else:
            self.__timeout = ms / 1000.0

    def setCustomHeaders(self, headers):
        self.__custom_headers = headers

    def read(self, sz):
        return self.__http_response.read(sz)

    def write(self, buf):
        self.__wbuf.write(buf)

    def flush(self):
        if self.__http_response is not None:
            self.__http_response.close()
            self.__http_response = None

        if not self.isOpen():
            self.open()

        # Pull data out of buffer
        data = self.__wbuf.getvalue()
        self.__wbuf = BytesIO()

        # HTTP request
        if self.using_proxy() and self.scheme == "http":
            # need full URL of real host for HTTP proxy here (HTTPS uses CONNECT tunnel)
            self.__http.putrequest('POST', "http://%s:%s%s" %
                                   (self.realhost, self.realport, self.path))
        else:
            self.__http.putrequest('POST', self.path)

        # Write headers
        self.__http.putheader('Content-Type', 'application/x-thrift')
        self.__http.putheader('Content-Length', str(len(data)))
        if self.using_proxy() and self.scheme == "http" and self.proxy_auth is not None:
            self.__http.putheader("Proxy-Authorization", self.proxy_auth)

        if not self.__custom_headers or 'User-Agent' not in self.__custom_headers:
            user_agent = 'Python/THttpClient'
            script = os.path.basename(sys.argv[0])
            if script:
                user_agent = '%s (%s)' % (user_agent, urllib.parse.quote(script))
            self.__http.putheader('User-Agent', user_agent)

        if self.__custom_headers:
            for key, val in six.iteritems(self.__custom_headers):
                self.__http.putheader(key, val)

        # Saves the cookie sent by the server in the previous response.
        # HTTPConnection.putheader can only be called after a request has been
        # started, and before it's been sent.
        if self.headers and 'Set-Cookie' in self.headers:
            self.__http.putheader('Cookie', self.headers['Set-Cookie'])

        self.__http.endheaders()

        # Write payload
        self.__http.send(data)

        # Get reply to flush the request
        self.__http_response = self.__http.getresponse()
        self.code = self.__http_response.status
        self.message = self.__http_response.reason
        self.headers = self.__http_response.msg
