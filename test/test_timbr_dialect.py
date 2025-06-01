import pytest
from utils import run_query_using_timbr_dialect, get_connection_uri_using_timbr_dialect

def test_run_query(test_config):
  uri = get_connection_uri_using_timbr_dialect(
    hostname=test_config['hostname'],
    port=test_config['port'],
    protocol=test_config['protocol'],
    ontology=test_config['ontology'],
    username=test_config['username'],
    password=test_config['password']
  )
  results_obj = run_query_using_timbr_dialect(uri, "SHOW CONCEPTS", connect_args=test_config['connect_args'])
  results_data = results_obj["results"]
  results_headers = results_obj["headers"]

  assert results_obj is not None, "Query did not return any results"
  assert len(results_data) > 0, "Query returned no rows"
  assert len(results_headers) > 0, "Query returned no columns"
  assert all(len(row) == len(results_headers) for row in results_data), "Row length does not match header length"