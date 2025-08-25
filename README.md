![Timbr logo](https://timbr.ai/wp-content/uploads/2025/01/logotimbrai230125.png)

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FWPSemantix%2Ftimbr_python_SQLAlchemy.svg?type=shield&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FWPSemantix%2Ftimbr_python_SQLAlchemy?ref=badge_shield&issueType=license)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FWPSemantix%2Ftimbr_python_SQLAlchemy.svg?type=shield&issueType=security)](https://app.fossa.com/projects/git%2Bgithub.com%2FWPSemantix%2Ftimbr_python_SQLAlchemy?ref=badge_shield&issueType=security)

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-3921/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31017/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-31112/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3129/)

[![PypiVersion](https://img.shields.io/pypi/v/pytimbr-sqla.svg)](https://badge.fury.io/py/pytimbr-sqla)

# timbr Python connector using SQLAlchemy
This project is a python connector to timbr using SQLAlchemy.

## Dependencies
- Access to a timbr-server
- Python from 3.9.13 or newer
- Support SQLAlchemy 1.4.36 or newer but not version 2.x yet.
- For <b>Linux</b> based machines only install those dependencies first:
  - gcc
  - heimdal-dev
  - krb5
  - python-devel
  - python-dev
  - python-all-dev
  - libsasl2-dev
- Ubuntu example:
  - apt install gcc, heimdal-dev, krb5, python-devel, python-dev, python-all-dev, libsasl2-dev

## Installation
- Install as clone repository:
  - Install Python: https://www.python.org/downloads/release/python-3913/
  - Run the following command to install the Python dependencies: `pip install -r requirements.txt`

- Install using pip and git:
  - `pip install git+https://github.com/WPSemantix/timbr_python_SQLAlchemy`

- Install using pip:
  - `pip install pytimbr-sqla`

## Sample usage
- For an example of how to use the Python SQLAlchemy connector for timbr, follow this [example file](examples/example.py)
- For an example of how to use the Python SQLAlchemy connector with 'PyHive' as async query for timbr, follow this [example file](examples/pyhive_async_example.py)
- For an example of how to use the Python SQLAlchemy connector with 'PyHive' as sync query for timbr, follow this [example file](examples/pyhive_sync_example.py)

## Connection parameters

### General example
```python
  hostname = '<TIMBR_IP/HOST>'
  port = '<TIMBR_PORT>'
  ontology = '<ONTOLOGY_NAME>'
  protocol = '<http/https>'
  username = '<TIMBR_USER/token>'
  password = '<TIMBR_PASSWORD/TOKEN_VALUE>'

  # hostname - The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
  # port - The port to connect to in the Timbr server. Timbr's default port with enabled_ssl is 443 without SSL is 11000.
  # ontology = The name of the ontology (knowledge graph) to connect.
  # protocol - Connection protocol can be 'http' or 'https'.
  # username - Use 'token' as the username when connecting using a Timbr token, otherwise use the user name.
  # password - If using a token as a username then the pass is the token value, otherwise its the user's password.
```

### HTTP example with dummy data

#### Username and password
```python
  hostname = 'mytimbrenv.com'
  port = '11000'
  ontology = 'my_ontology'
  protocol = 'http'
  username = 'timbr'
  password = 'StrongPassword'
```

#### Timbr token
```python
  hostname = 'mytimbrenv.com'
  port = '11000'
  ontology = 'my_ontology'
  protocol = 'http'
  username = 'token'
  password = '<TOKEN_VALUE>'
```

### HTTPS example with dummy data

#### Username and password
```python
  hostname = 'mytimbrenv.com'
  port = '443'
  ontology = 'my_ontology'
  protocol = 'https'
  username = 'timbr'
  password = 'StrongPassword'
```

#### Timbr token
```python
  hostname = 'mytimbrenv.com'
  port = '443'
  ontology = 'my_ontology'
  protocol = 'https'
  username = 'token'
  password = '<TOKEN_VALUE>'
```
## Connect options

### Connect using 'pytimbr_sqla' and 'SQLAlchemy' packages
```python
  from sqlalchemy import create_engine

  # Declare the connection variables
  # General example
  hostname = '<TIMBR_IP/HOST>'
  port = '<TIMBR_PORT>'
  ontology = '<ONTOLOGY_NAME>'
  protocol = '<http/https>'
  username = '<TIMBR_USER/token>'
  password = '<TIMBR_PASSWORD/TOKEN_VALUE>'

  # hostname - The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
  # port - The port to connect to in the Timbr server. Timbr's default port with enabled_ssl is 443 without SSL is 11000.
  # ontology = The name of the ontology (knowledge graph) to connect.
  # protocol - Connection protocol can be 'http' or 'https'.
  # username - Use 'token' as the username when connecting using a Timbr token, otherwise use the user name.
  # password - If using a token as a username then the pass is the token value, otherwise its the user's password.

  # Create new sqlalchemy connection
  engine = create_engine(f"timbr+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}")

  # Connect to the created engine
  conn = engine.connect()

  # Execute a query
  query = "SHOW CONCEPTS"
  res_obj = conn.execute(query)
  results_headers = [(desc[0], desc[1]) for desc in res_obj.cursor.description]

  # Optional Performance Tuning:
  # By default, Timbr fetches results in batches of 10,000 rows at a time.
  # You can increase this batch size for better performance with large datasets.
  # Note: The maximum batch size is controlled by your Timbr server's 
  # "TIMBR_RESULTSET_MAX_FETCH_SIZE" configuration setting.
  res_obj.cursor._arraysize = 20000

  results = res_obj.fetchall()

  # Print the columns name
  for name, col_type in results_headers:
    print(f"{name} - {col_type}")
  # Print the results
  for result in results:
    print(result)
```
### Attention:
### timbr works only as async when running a query, if you want to use standard PyHive you have two options

### Connect using 'PyHive' and 'SQLAlchemy' packages

#### Connect using PyHive Async Query
```python
  from sqlalchemy import create_engine
  from TCLIService.ttypes import TOperationState

  # Declare the connection variables
  # General example
  hostname = '<TIMBR_IP/HOST>'
  port = '<TIMBR_PORT>'
  ontology = '<ONTOLOGY_NAME>'
  protocol = '<http/https>'
  username = '<TIMBR_USER/token>'
  password = '<TIMBR_PASSWORD/TOKEN_VALUE>'
  connect_args = {
    'configuration': {
      'set:hiveconf:hiveMetadata': 'true',
      'set:hiveconf:active_datasource': '<datasource_name>',
      'set:hiveconf:queryTimeout': '<TIMEOUT_IN_SECONDS>',
    },
  }

  # hostname - The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
  # port - The port to connect to in the Timbr server. Timbr's default port with enabled_ssl is 443 without SSL is 11000.
  # ontology = The name of the ontology (knowledge graph) to connect.
  # protocol - Connection protocol can be 'http' or 'https'.
  # username - Use 'token' as the username when connecting using a Timbr token, otherwise use the user name.
  # password - If using a token as a username then the pass is the token value, otherwise its the user's password.
  # connect_args - The connection special arguments for extra customization. The only argument you must have is the first one (set:hiveconf:hiveMetadata) the others are optional.

  # Create new sqlalchemy connection
  engine = create_engine(f"hive+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}", connect_args = connect_args)

  # Connect to the created engine
  conn = engine.connect()
  dbapi_conn = engine.raw_connection()
  cursor = dbapi_conn.cursor()

  # Execute a query
  query = "SHOW CONCEPTS"
  cursor.execute(query)

  # Check the status of this execution
  status = cursor.poll().operationState
  while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
    status = cursor.poll().operationState

  # Get the results of the execution
  results_headers = [(desc[0], desc[1]) for desc in cursor.description]
  results = cursor.fetchall()

  # Display the results of the execution
  # Print the columns name
  for name, col_type in results_headers:
    print(f"{name} - {col_type}")
  # Print the results
  for result in results:
    print(result)
```

#### Connect using PyHive Sync Query
```python
  from sqlalchemy import create_engine
  from TCLIService.ttypes import TOperationState

  # Declare the connection variables
  # General example
  hostname = '<TIMBR_IP/HOST>'
  port = '<TIMBR_PORT>'
  ontology = '<ONTOLOGY_NAME>'
  protocol = '<http/https>'
  username = '<TIMBR_USER/token>'
  password = '<TIMBR_PASSWORD/TOKEN_VALUE>'
  connect_args = {
    'configuration': {
      'set:hiveconf:async': 'false',
      'set:hiveconf:hiveMetadata': 'true',
      'set:hiveconf:active_datasource': '<datasource_name>',
      'set:hiveconf:queryTimeout': '<TIMEOUT_IN_SECONDS>',
    },
  }

  # hostname - The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
  # port - The port to connect to in the Timbr server. Timbr's default port with enabled_ssl is 443 without SSL is 11000.
  # ontology = The name of the ontology (knowledge graph) to connect.
  # protocol - Connection protocol can be 'http' or 'https'.
  # username - Use 'token' as the username when connecting using a Timbr token, otherwise use the user name.
  # password - If using a token as a username then the pass is the token value, otherwise its the user's password.
  # connect_args - The connection special arguments for extra customization. The only 2 arguments you must have are the first and the second one (set:hiveconf:async, set:hiveconf:hiveMetadata) the others are optional.

  # Create new sqlalchemy connection
  engine = create_engine(f"hive+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}", connect_args = connect_args)

  # Connect to the created engine
  conn = engine.connect()

  # Execute a query
  query = "SHOW CONCEPTS"
  res_obj = conn.execute(query)
  results_headers = [(desc[0], desc[1]) for desc in res_obj.cursor.description]
  results = res_obj.fetchall()

  # Print the columns name
  for name, col_type in results_headers:
    print(f"{name} - {col_type}")
  # Print the results
  for result in results:
    print(result)
```
