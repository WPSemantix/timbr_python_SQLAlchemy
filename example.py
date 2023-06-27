from sqlalchemy.engine import create_engine

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

engine = create_engine(f"timbr+{protocol}://{user_name}@{ontology}:{user_pass}@{hostname}:{port}")
conn = engine.connect()
concepts = conn.execute("SHOW CONCEPTS").fetchall()
for concept in concepts:
  print(concept)