def register_and_login(client, username="matt", email="matt@test.com", password="pass123"):
    client.post("/register", data={
    "username": username,
        "email": email,
        "password": password,
        "confirm": password
    }, follow_redirects=True)
    
    client.post("/login", data={
        "username": username,
        "password": password
    }, follow_redirects=True)

def test_add_gig(client):
    register_and_login(client)
    
    response = client.post("/add_gig", data={
        "artist": "Metallica",
        "venue": "Hydro",
        "date": "2024-10-01",
        "review": "Metal up your ass!"
        }, follow_redirects=True)
        
    assert b"Gig added successfully" in response.data