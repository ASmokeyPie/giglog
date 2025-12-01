def test_register_and_login(client):
	# Register a user
    response = client.post("/register", data={
        "username": "matt",
        "email": "matt@test.com",
        "password": "pass123",
        "confirm": "pass123"
    }, follow_redirects=True)
    
    assert b"Registration successful" in response.data or b"already taken" in response.data
    
    # Login with that user
    response = client.post("/login", data={
        "username": "matt",
        "password": "pass123"
    }, follow_redirects=True)
    
    assert b"Logged in successfully" in response.data