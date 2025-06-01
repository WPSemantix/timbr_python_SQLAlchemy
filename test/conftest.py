import os
import json
import pytest
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv(override=True)

# Global fixture to load config values
@pytest.fixture(scope="session")
def test_config():
  return {
    "hostname": os.getenv("HOSTNAME"),
    "port": os.getenv("PORT"),
    "protocol": os.getenv("PROTOCOL"),
    "ontology": os.getenv("ONTOLOGY"),
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "connect_args": json.loads(os.getenv("CONNECT_ARGS", "{}"))
  }
