import os
import tempfile
import pytest
from giglog.app import app

@pytest.fixture
def client():
    # Creata a temporary directory for test data
    temp_dir = tempfile.TemporaryDirectory()
    
    # Create a test version of the "data" folder
    data_path = os.path.join(temp_dir.name, "data")
    os.makedirs(data_path, exist_ok=True)
    
    app.config["TESTING"] = True
    app.config["USERS_FILE"] = os.path.join(data_path, "users.json")
    app.config["GIGS_FILE"] = os.path.join(data_path, "gigs.json")
    app.config["FOLLOWS_FILE"] = os.path.join(data_path, "follows.json")
    
    
    # Initialise empty test data files
    with open(app.config["USERS_FILE"], "w") as f:
        f.write("{}")
    
    with open(app.config["GIGS_FILE"], "w") as f:
        f.write("{}")
    
    with open(app.config["FOLLOWS_FILE"], "w") as f:
        f.write("[]")
    
    # Yield Flask test client
    with app.test_client() as client:
        yield client