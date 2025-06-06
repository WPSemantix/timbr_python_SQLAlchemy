import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='pytimbr_sqla',
  version='2.0.0',
  author='timbr',
  author_email='contact@timbr.ai',
  description='Timbr Python SQLAlchemy connector',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/WPSemantix/timbr_python_SQLAlchemy',
  download_url = 'https://github.com/WPSemantix/timbr_python_SQLAlchemy/archive/refs/tags/v2.0.0.tar.gz',
  project_urls={
    "Bug Tracker": "https://github.com/WPSemantix/timbr_python_SQLAlchemy/issues"
  },
  license='MIT',
  packages=['pytimbr_sqla', 'TCLIService', 'thrift', 'thrift.transport'],
  install_requires=[
    'future==1.0.0',
    'python-dateutil==2.9.0',
    'ldap3',
    'thrift_sasl==0.4.3',
    'pure-sasl>=0.6.2',
    'sqlalchemy>=1.4.36,<2.0.0',
    'requests_kerberos==0.15.0',
    'pyhive==0.7.0',
  ],
  extras_require={},
  package_data={},
  keywords = [
    'timbr',
    'timbr-python',
    'timbr-connector',
    'python-connector',
    'PyTimbr',
    'pytimbr',
    'py-timbr',
    'Py-Timbr',
    'pytimbr_sqla',
    'pytimbr_Sqla',
    'PyTimbr_Sqla',
    'pytimbr_SQla',
    'PyTimbr_SQla',
    'pytimbr_SQLa',
    'PyTimbr_SQLa',
    'pytimbr_SQlA',
    'PyTimbr_SQLA',
    'pytimbrsqlalchemy',
    'PyTimbrSqlalchemy',
    'PyTimbrSQlalchemy',
    'PyTimbrSQLalchemy',
    'PyTimbrSQLAlchemy',
    'Py-TimbrSQLAlchemy',
    'py-timbrsqlalchemy',
    'Py-Timbr-SQLAlchemy',
    'py-timbr-sqlalchemy',
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
  entry_points={
    'sqlalchemy.dialects': [
      'timbr = pytimbr_sqla.sqlalchemy_timbr:TimbrDialect',
      "timbr.http = pytimbr_sqla.sqlalchemy_timbr:TimbrHTTPDialect",
      "timbr.https = pytimbr_sqla.sqlalchemy_timbr:TimbrHTTPSDialect",
    ],
  }
)
