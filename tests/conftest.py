import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from rp_flask_api.app import app
from rp_flask_api.build_database import build_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Build the database before running tests
    build_db()

@pytest.fixture
def client():
    # Enable Flask's testing mode
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client



