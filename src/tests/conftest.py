# tests/conftest.py
import pytest
from src import create_app, db
from config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    # Create a Flask app configured for testing
    app = create_app(config_class=TestConfig)

    # Establish an application context
    with app.app_context():
        # Create the database and the database table(s)
        db.create_all()

        # Create a test client using the Flask application configured for testing
        with app.test_client() as testing_client:
            # Yield the client to the tests
            yield testing_client

        # Teardown: drop all tables after the tests are done
        db.drop_all()

        