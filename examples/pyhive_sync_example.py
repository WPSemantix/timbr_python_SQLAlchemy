from sqlalchemy.engine import create_engine
from TCLIService.ttypes import TOperationState

if __name__ == '__main__':
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

  # HTTP example
  hostname = 'mytimbrenv.com'
  port = '11000'
  ontology = 'my_ontology'
  protocol = 'http'
  username = 'timbr'
  password = 'StrongPassword'
  connect_args = {
    'configuration': {
      'set:hiveconf:async': 'false',
      'set:hiveconf:hiveMetadata': 'true',
    },
  }

  # HTTPS example
  hostname = 'mytimbrenv.com'
  port = '443'
  ontology = 'my_ontology'
  protocol = 'https'
  username = 'timbr'
  password = 'StrongPassword'
  connect_args = {
    'configuration': {
      'set:hiveconf:async': 'false',
      'set:hiveconf:hiveMetadata': 'true',
    },
  }

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