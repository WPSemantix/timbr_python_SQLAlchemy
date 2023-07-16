![Timbr logo description](Timbr_logo.png)

# timbr Python connector sample file
This is a sample repository for how to connect to timbr using SQLAlchemy and Python.

## Dependencies
- Access to a timbr-server
- Python from 3.7.13 or newer
- Support SQLAlchemy 1.4.36 or newer but not version 2.x yet.

## Installation
- Install as clone repository:
  - Install Python: https://www.python.org/downloads/release/python-3713/
  - Run the following command to install the Python dependencies: `pip install -r requirements.txt`

- Install using pip and git:
  - `pip install git+https://github.com/WPSemantix/timbr_python_SQLAlchemy`

- Install using pip:
  - `pip install pytimbr_sqla`

## Known issues
If you encounter a problem installing `PyHive` with sasl dependencies on windows, install the following wheel (for 64bit Windows) by running:

`pip install https://download.lfd.uci.edu/pythonlibs/archived/cp37/sasl-0.3.1-cp37-cp37m-win_amd64.whl`

## Sample usage
- For an example of how to use the Python connector for timbr, follow this [example file](example.py)

## Connect options

### Connect using 'pytimbr_sqla' and 'SQLAlchemy' packages
```python
  from sqlalchemy import create_engine

  # Connection protocol can be 'http' or 'https'
  protocol = 'http'
  # Use 'token' as the username when connecting using a Timbr token, otherwise use the user name
  user_name = 'token'
  # If using a token as a username then the pass is the token value, otherwise its the user's password.
  user_pass = '<token_value_or_user_password>'
  # The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
  hostname = '<timbr_server_host>'
  # The port to connect to in the Timbr server. Timbr's default port is 11000
  port = '<timbr_server_port>'
  # The name of the ontology (knowledge graph) to connect
  ontology = '<ontology_name>'
  
  # Create new sqlalchemy connection
  engine = create_engine(f"timbr+{protocol}://{user_name}@{ontology}:{user_pass}@{hostname}:{port}")
  conn = engine.connect()

  # Use the connection to execute a query
  query = "SHOW CONCEPTS"
  concepts = conn.execute(query).fetchall()
  for concept in concepts:
    print(concept)
```
### Attention:
### timbr works only as async when running a query, if you want to use standard PyHive you have two options

### Connect using 'PyHive' and 'SQLAlchemy' packages

#### Connect using PyHive Async Query
```python
  from sqlalchemy import create_engine
  from TCLIService.ttypes import TOperationState

  # Connection protocol can be 'http' or 'https'
  protocol = 'http'
  # Use 'token' as the username when connecting using a Timbr token, otherwise use the user name
  user_name = 'token'
  # If using a token as a username then the pass is the token value, otherwise its the user's password.
  user_pass = '<token_value_or_user_password>'
  # The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
  hostname = '<timbr_server_host>'
  # The port to connect to in the Timbr server. Timbr's default port is 11000
  port = '<timbr_server_port>'
  # The name of the ontology (knowledge graph) to connect
  ontology = '<ontology_name>'
  
  # Create new sqlalchemy connection
  engine = create_engine(f"hive+{protocol}://{user_name}@{ontology}:{user_pass}@{hostname}:{port}", connect_args={'configuration': {'set:hiveconf:hiveMetadata': 'true'}})
  conn = engine.connect()
  dbapi_conn = engine.raw_connection()
  cursor = dbapi_conn.cursor()

  # Use the connection to execute a query
  query = "SHOW CONCEPTS"
  cursor.execute(query)

  # Check the status of this execution
  status = cursor.poll().operationState
  while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
      status = cursor.poll().operationState

  results = cursor.fetchall()
  print(results)
```

#### Connect using PyHive Sync Query
```python
  from sqlalchemy import create_engine
  from TCLIService.ttypes import TOperationState

  # Connection protocol can be 'http' or 'https'
  protocol = 'http'
  # Use 'token' as the username when connecting using a Timbr token, otherwise use the user name
  user_name = 'token'
  # If using a token as a username then the pass is the token value, otherwise its the user's password.
  user_pass = '<token_value_or_user_password>'
  # The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
  hostname = '<timbr_server_host>'
  # The port to connect to in the Timbr server. Timbr's default port is 11000
  port = '<timbr_server_port>'
  # The name of the ontology (knowledge graph) to connect
  ontology = '<ontology_name>'
  
  # Create new sqlalchemy connection
  engine = create_engine(f"hive+{protocol}://{user_name}@{ontology}:{user_pass}@{hostname}:{port}", connect_args={'configuration': {'set:hiveconf:async': 'false', 'set:hiveconf:hiveMetadata': 'true'}})
  conn = engine.connect()

  # Use the connection to execute a query
  query = "SHOW CONCEPTS"
  results = conn.execute(query).fetchall()
  print(results)
```
