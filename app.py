# Import necessary Flask modules and Python libraries
from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import os
from functools import wraps

# Initialise the Flask app
app = Flask(__name__)

# Secret key used by Flask for session management and flash messages
app.secret_key = 'supersecret'

# Paths to the JSON files that store app data
DATA_FILE = "data/gigs.json"
USERS_FILE = "data/users.json"
FRIENDS_FILE = "data/friends.json"

# -----------------------------
# Custom Jinja2 template filter
# -----------------------------
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d %b %Y'):
    """
    Converts a date string like '2025-11-21' into a formatted date string '21 Nov 2025'.
    """
    dt = datetime.strptime(value, "%Y-%m-%d")
    return dt.strftime(format)

# ---------------------------
# Current year injector
# ---------------------------
@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}


# ---------------------------
# Helper functions
# ---------------------------

# -- Gig Data --
def load_gigs():
    """
    Loads the gigs from the JSON file.
    Returns an empty list if the file does not exist.
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_gigs(gigs):
    """
    Saves the given list of gigs to the JSON file with indentation for readability.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(gigs, f, indent=4)

# -- User Data --
def load_users():
    """
    """
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """
    """
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# -- User Friends --
def load_friends():
    """
    """
    if not os.path.exists(FRIENDS_FILE):
        return []
    with open(FRIENDS_FILE, "r") as f:
        return json.load(f)

def save_friends(friends):
    """
    """
    with open(FRIENDS_FILE, "w") as f:
        json.dump(friends, f, indent=4)

def get_friends(username):
    """
    Return a list of usernames that are friends with the given username.
    Assumes friends.json is a list of {"user": "...", "friend": "..."} objects or a similar structure.
    """
    friends_data = load_friends()
    friends_list = []
    for entry in friends_data:
        if entry["user"] == username:
            friends_list.extend(entry.get("friends", []))
        elif entry.get("friends") and username in entry["friends"]:
            friends_list.append(entry["user"])
    return friends_list


#-- Require login --
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def index():
    """
    Home page route.
    Renders the index.html template.
    """
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        confirm = request.form["confirm"]
        
        # Load users
        users = load_users()
        
        # Validation
        if any(u["username"] == username for u in users):
            flash("Username already taken.", "danger")
            return redirect(url_for("register"))
        
        if any(u["email"] == email for u in users):
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
        
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))
        
        # Create new user
        new_user = {
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users.append(new_user)
        save_users(users)
        
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        
        users = load_users()
        
        # Check for username match
        for user in users:
            if user["username"] == username:
                
                # Verify hashed password
                if check_password_hash(user["password"], password):
                    session["user"] = username
                    flash("Logeed in successfully!", "success")
                    return redirect(url_for("feed"))
                else:
                    flash("Incorrect password.", "danger")
                    return redirect(url_for("login"))
        
        flash("Username not found.", "danger")
        return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/feed")
def feed():
    """
    Feed page route.
    Loads all gigs from JSON and passes them to the feed.html template.
    """
    gigs = load_gigs()
    return render_template("feed.html", gigs=gigs, title="Global Feed")

@app.route("/feed/friends")
def friend_feed():
    current_user = session.get("user")
    gigs = load_gigs()
    friends_list = get_friends(current_user) # returns list of usernames
    # Only show gigs by user or friends
    filtered_gigs = [g for g in gigs if g["username"] in friends_list + [current_user]]
    return render_template("feed.html", gigs=filtered_gigs, title="Friend Activity")


@app.route("/add_gig", methods=["GET","POST"])
@login_required
def add_gig():
    """
    Route for adding a new gig.
    - GET: Show the empty form to add a gig.
    - POST: Process form submission, add the new gig to JSON, and redirect to feed.
    """
    if request.method == "POST":
        # Retrieve form data
        artist = request.form["artist"]
        venue = request.form["venue"]
        date = request.form["date"]
        review = request.form["review"]
        
        # Load existing gigs and append the new one
        gigs = load_gigs()
        
        new_gig = {
            "artist": artist,
            "venue": venue,
            "date": date,
            "review": review,
            "username": session["user"], # atttach gig to user
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        gigs.append(new_gig)
        
        # Save updated gig list
        save_gigs(gigs)
        
        # Flash a success message and redirect to the feed
        flash("Gig added successfully!", "success")
        return redirect(url_for("feed"))
    
    # For GET requests, show the form
    return render_template("add_gig.html")


@app.route("/delete_gig/<int:index>", methods=["POST"])
@login_required
def delete_gig(index):
    """
    Route for deleting a gig.
    Accepts a POST request with the gig index.
    Removes the gig from the JSON file if the index is valid.
    """
    gigs = load_gigs()
    if 0 <= index < len(gigs):
        gigs.pop(index)  # Remove the gig at the given index
        save_gigs(gigs)
        flash("Gig deleted successfully.", "success")
    return redirect(url_for("feed"))


@app.route("/edit_gig/<int:index>", methods=["GET", "POST"])
@login_required
def edit_gig(index):
    """
    Route for editing a gig.
    - GET: Shows the form pre-filled with the gig data.
    - POST: Updates the gig in the JSON file and redirects to feed.
    """
    gigs = load_gigs()
    
    # Validate index
    if index < 0 or index >= len(gigs):
        flash("Invalid gig index.", "danger")
        return redirect(url_for("feed"))
    
    if request.method == "POST":
        # Update the gig details from the form
        gigs[index]["artist"] = request.form["artist"]
        gigs[index]["venue"] = request.form["venue"]
        gigs[index]["date"] = request.form["date"]
        gigs[index]["review"] = request.form["review"]
        save_gigs(gigs)
        flash("Gig updated successfully!", "success")
        return redirect(url_for("feed"))
    
    # GET request → show the edit form
    gig = gigs[index]
    return render_template("edit_gig.html", gig=gig, index=index)


@app.route("/profile")
@login_required
def profile():
    """
    Profile page route.
    Renders the profile.html template.
    """
    gigs = load_gigs()
    
    # Filter only the current user's gigs
    user_gigs = [g for g in gigs if g.get("username") == session["user"]]
    
    return render_template("profile.html", user=session["user"], gigs=user_gigs)


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/add_friend/<friend_username>", methods=["POST"])
def add_friend(friend_username):
    current_user = session.get["user"]
    friends = load_friends()
    user_friends = next((f for f in friends if f["user"] == current_user), none)
    if user_friends:
        if friend_username not in user_friends["friends"]:
            user_friends["friends"].append(friend_username)
            save_friends(friends)
            flash(f"You are now friends with {friend_username}!", "success")
    else:
        friends.append({"user": current_user, "friends": [friend_username]})
        save_friends(friends)
        flash(f"You are now friends with {friend_username}!", "success")
    return redirect(url_for("profile"))


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    # Enable debug mode for easier development
    app.run(debug=True)
