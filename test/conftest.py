import pytest
from main import app as flask_app, db

@pytest.fixture
def app():
    """
    Δημιουργεί και ρυθμίζει την εφαρμογή (app) για τα tests.
    Φτιάχνει τη βάση στη μνήμη (RAM).
    """
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # Βάση στη μνήμη
        "WTF_CSRF_ENABLED": False  # Κλείνουμε την ασφάλεια φόρμας για τα test
    })

    # Φτιάχνουμε τους πίνακες στη βάση
    with flask_app.app_context():
        db.create_all()
        yield flask_app  # Εδώ δίνουμε το 'app' στο test
        
        # Καθαρισμός μετά το test
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Δημιουργεί τον "ψεύτικο browser" (client).
    Ζητάει το 'app' από πάνω για να λειτουργήσει.
    """
    return app.test_client()