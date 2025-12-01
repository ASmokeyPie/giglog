def setup_two_users(client):
    # Register Andrew
	client.post("/register", data={
        "username": "Andrew",
        "email": "andrew@test.com",
        "password": "pass123",
        "confirm": "pass123"
    }, follow_redirects=True)
    
    #Register Oceane
	client.post("/register", data={
        "username": "Oceane",
        "email": "oceane@test.com",
        "password": "123",
        "confirm": "pass123"
    }, follow_redirects=True)

def login(client, username, password):
    response = client.post("/login", data={
        "username": username,
        "password": password
    }, follow_redirects=True)
    
    return response


def test_follow_user(client):
    setup_two_users(client)
    
    # Login as Andrew
    login(client, "Andrew", "pass123")
    
    # Make sure session has 'user'
    with client.session_transaction() as sess:
        assert sess.get("user") == "Andrew"
    
    # Andrew follows Oceane
    response = client.post("/follow/Oceane", follow_redirects=True)
    
    assert b"You are now following Oceane" in response.data or b"You already follow Oceane" in response.data