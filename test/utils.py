from sqlalchemy import create_engine
from TCLIService.ttypes import TOperationState

def set_dialect_for_new_connection_uri(dialect: str, uri: str) -> str:
  """
  Sets the dialect for a new connection URI.
  
  :param dialect: The database dialect to use (e.g., 'timbr', 'hive').
  :param connection_uri: The original connection URI.
  
  :return: A new connection URI with the specified dialect.
  """
  if not uri.startswith(f"{dialect}+"):
    return f"{dialect}+{uri}"
  return uri

def get_connection_uri_using_timbr_dialect(hostname: str, port: int, protocol: str, ontology: str, username: str, password: str) -> str:
  """
  Constructs a connection URI for the database using the provided parameters.
  
  :param hostname: The hostname of the database server.
  :param port: The port number on which the database server is listening.
  :param protocol: The protocol to use (e.g., 'http', 'https').
  :param ontology: The ontology or database name.
  :param username: The username for authentication.
  :param password: The password for authentication.
  
  :return: A formatted connection URI string.
  """
  return f"timbr+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}"

def get_connection_uri_using_hive_dialect(hostname: str, port: int, protocol: str, ontology: str, username: str, password: str) -> str:
  """
  Constructs a connection URI for the Hive database using the provided parameters.
  
  :param hostname: The hostname of the Hive server.
  :param port: The port number on which the Hive server is listening.
  :param protocol: The protocol to use (e.g., 'http', 'https').
  :param ontology: The ontology or database name.
  :param username: The username for authentication.
  :param password: The password for authentication.
  
  :return: A formatted connection URI string for Hive.
  """
  return f"hive+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}"

def run_query_using_timbr_dialect(uri: str, query: str, connect_args={}) -> object:
  """
  Connects to a database using the given URI,
  executes the provided SQL query,
  and returns the result object.
  """
  # Create new sqlalchemy connection
  engine = create_engine(uri, connect_args=connect_args)

  # Connect to the created engine
  conn = engine.connect()

  # Execute a query
  res_obj = conn.execute(query)

  results_headers = res_obj.keys()
  results = res_obj.fetchall()
  connect_args = connect_args or {}

  # Display the results of the execution formatted as a table
  # Print the columns name
  print(f"index | {' | '.join(results_headers)}")
  # Print a separator line
  print("-" * ((len(results_headers)+1) * 10))
  # Print the results
  for res_index, result in enumerate(results, start=1):
    print(f"{res_index} | {' | '.join(map(str, result))}")
  
  return dict(results=results, headers=results_headers)

def run_query_using_hive_dialect(uri: str, query: str, connect_args={}, is_async=False) -> object:
  """
  Connects to a Hive database using the given URI,
  executes the provided SQL query,
  and returns the result object.
  """
  # Create new sqlalchemy connection
  engine = create_engine(uri, connect_args=connect_args)

  # Connect to the created engine
  conn = engine.connect()

  if is_async:
    dbapi_conn = engine.raw_connection()
    cursor = dbapi_conn.cursor()
    
    # Use the connection to execute a query
    cursor.execute(query)
    
    # Check the status of this execution
    status = cursor.poll().operationState
    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
      status = cursor.poll().operationState
    # Get the results of the execution
    results_headers = [(desc[0], desc[1]) for desc in cursor.description]
    results = cursor.fetchall()

  else:
    # Use the connection to execute a query
    res_obj = conn.execute(query)
    results_headers = [(desc[0], desc[1]) for desc in res_obj.cursor.description]
    results = res_obj.fetchall()

  # Print the columns name
  for name, col_type in results_headers:
    print(f"{name} - {col_type}")

  # Print the results
  for result in results:
    print(result)
  
  return dict(results=results, headers=results_headers)