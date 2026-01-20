from main import User, db

def test_home_page(client):
    """
    Scenario: A user visits the homepage.
    Expected: Status Code 200 (OK).
    """
    response = client.get('/')
    assert response.status_code == 200
    # Check if we see the correct title in the HTML
    assert b"The Grandmaster's Log"  in response.data

def itest_admin_route_security(client):
    """
    Scenario: A stranger (not logged in) tries to create a post.
    Expected: 403 Forbidden OR 401 Unauthorized (depends on your code).
    In your code, @admin_only returns 403 via abort(403).
    """
    # Try to access a protected route
    response = client.get('/new-post')
    
    # Assert they are blocked (403 Forbidden)
    assert response.status_code == 403

def test_register_user(client, app):
    """
    Scenario: A user registers via the form.
    Expected: User is added to the database and redirected (302).
    """
    # Send POST request with registration data
    response = client.post('/register', data={
        "email": "test@example.com",
        "password": "password123",
        "name": "TestUser"
    })

    # 1. Check if redirected to Home (Status 302 means Redirect)
    assert response.status_code == 302
    
    # 2. Check Database: Did the user actually get saved?
    with app.app_context():
        user = db.session.execute(db.select(User).where(User.email == "test@example.com")).scalar()
        assert user is not None
        assert user.name == "TestUser"