from sqlalchemy.engine import create_engine

protocol = 'http' # Connection protocol can be 'http' or 'https'
user_name = 'token' # Use 'token' as the username when connecting using a Timbr token, otherwise use the user name
user_pass = '<token_value_or_user_password>' # If using a token as a username then the pass is the token value, otherwise its the user's password.
hostname = '<timbr_server_host>' # The IP / Hostname of the Timbr server (not necessarily the hostname of the Timbr platform).
port = '<timbr_server_port>' # The port to connect to in the Timbr server. Timbr's default port is 11000
ontology = '<ontology_name>' # The name of the ontology (knowledge graph) to connect

engine = create_engine(f"hive+{protocol}://{user_name}@{ontology}:{user_pass}@{hostname}:{port}")
conn = engine.connect()
concepts = conn.execute("SHOW CONCEPTS").fetchall()
for concept in concepts:
    print(concept)
