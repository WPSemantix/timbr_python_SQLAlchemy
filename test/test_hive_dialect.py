import pytest
from utils import get_connection_uri_using_hive_dialect, run_query_using_hive_dialect

def create_engine_and_run_query(config, is_async=False):
  """
  Creates a SQLAlchemy engine and runs a query using the Hive dialect.
  """
  uri = get_connection_uri_using_hive_dialect(
    hostname=config['hostname'],
    port=config['port'],
    protocol=config['protocol'],
    ontology=config['ontology'],
    username=config['username'],
    password=config['password']
  )
  return run_query_using_hive_dialect(
    uri,
    "SHOW CONCEPTS",
    config['connect_args'],
    is_async,
  )

def test_run_sync_query(test_config):
  results_obj = create_engine_and_run_query(test_config, is_async=False)
  results_data = results_obj["results"]
  results_headers = results_obj["headers"]

  assert results_obj is not None, "Query did not return any results"
  assert len(results_data) > 0, "Query returned no rows"
  assert len(results_headers) > 0, "Query returned no columns"
  assert all(len(row) == len(results_headers) for row in results_data), "Row length does not match header length"

def test_run_async_query(test_config):
  results_obj = create_engine_and_run_query(test_config, is_async=True)
  results_data = results_obj["results"]
  results_headers = results_obj["headers"]

  assert results_obj is not None, "Query did not return any results"
  assert len(results_data) > 0, "Query returned no rows"
  assert len(results_headers) > 0, "Query returned no columns"
  assert all(len(row) == len(results_headers) for row in results_data), "Row length does not match header length"