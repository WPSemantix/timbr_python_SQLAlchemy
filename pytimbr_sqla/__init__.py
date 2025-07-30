"""Timbr Python SQLAlchemy connector."""

__version__ = "2.0.1"

try:
  from thrift.transport import THttpClient
  def timbr_flush(self):
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

  THttpClient.flush = timbr_flush
except:
    pass