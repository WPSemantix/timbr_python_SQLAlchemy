import requests
import pandas

def executeQuery(url, ontology, token, query):
    if not url.endswith("/"):
       url += "/"   
    post_data = {'ontology_name': ontology, 'query': query}
    headers = {'Content-Type': 'application/json', 'x-api-key': token}
    response = requests.post(url + "timbr/api/query", headers = headers, json = post_data, verify = False)
    response_data = response.json()
    if response_data['status'] == 'success':
        df = pandas.DataFrame(response_data['data'])
        return df
    else:
        raise Exception("Error in request: " + response_data['data'])

url = "http://" # http://<hostname> or https://<hostname>
ontology = "" # ontology name
token = "" # user token
query = "SHOW CONCEPTS"

response = executeQuery(url, ontology, token, query)
print(response)