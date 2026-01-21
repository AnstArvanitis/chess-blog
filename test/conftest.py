import pytest
from main import app as flask_app, db

@pytest.fixture
def app():
    """
    Creates and configures a fresh instance of the Flask application for testing.
    Initializes an in-memory SQLite database.
    """
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # In-memory database
        "WTF_CSRF_ENABLED": False  # Disable CSRF protection for testing
    })

    # Create all database tables
    with flask_app.app_context():
        db.create_all()
        yield flask_app  # Yield the app instance for the test
        
        # Clean up / Teardown after the test runs
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Creates a test client (simulated browser).
    Requires the 'app' fixture to function.
    """
    return app.test_client()