# Import necessary Flask modules and Python libraries
from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import os
from functools import wraps
import uuid

# Initialise the Flask app
app = Flask(__name__)

# Secret key used by Flask for session management and flash messages
app.secret_key = 'supersecret'

# Uploads folder configuration
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB upload limit

# Paths to the JSON files that store app data
DATA_FILE = "data/gigs.json"
USERS_FILE = "data/users.json"
FOLLOWS_FILE = "data/follows.json"

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
    """
    Inject the current year into all templates as 'current_year'
    """
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
    Loads the users from the JSON file.
    Returns an empty list if the file does not exist.
    """
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """
    Saves the given list of users to the JSON file with indentation for readability.
    """
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# -- User Follows --
def load_follows():
    """
    Loads who follows who from the JSON file.
    Returns an empty list if the file does not exist.
    """
    if not os.path.exists(FOLLOWS_FILE):
        return []
    with open(FOLLOWS_FILE, "r") as f:
        return json.load(f)

def save_follows(follows):
    """
    Saves the updated follow data to the JSON file with indentation for readability.
    """
    with open(FOLLOWS_FILE, "w") as f:
        json.dump(follows, f, indent=4)

def get_following(username):
    """
    Return a list of users that the given username is following.
    """
    follows = load_follows()
    entry = next((u for u in follows if u["user"] == username), None)
    if entry:
        return entry.get("following", [])
    return []


#-- Require login decorator --
def login_required(f):
    """
    Provides login required functionality to any route wrapped with this function.
    Redirects users to login page if they are not logged in.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if 'user' exists in session, i.e., user is logged in
        if "user" not in session:
            flash("Please log in first.", "warning")
            # Redirect to login page if not logged in
            return redirect(url_for("login"))
        # User is logged in, proceed to the wrapped route
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


# ---------------------- REGISTER ----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration page route.
    GET: Display registration form.
    POST: Process registration form, validate, create new user, save to JSON, redirect to login.
    """
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        confirm = request.form["confirm"]
        
        # Load users
        users = load_users()
        
        # Validation checks
        if any(u["username"] == username for u in users):
            flash("Username already taken.", "danger")
            return redirect(url_for("register"))
        
        if any(u["email"] == email for u in users):
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
        
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))
        
        # Create new user dictionary
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
    
    # GET request -> show registration form
    return render_template("register.html")


# ---------------------- LOGIN ----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    User login page route.
    GET: Show login form.
    POST: Validate login credentials, set session, redirect to feed.
    """
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        
        users = load_users()
        
        # Loop through users to find matching username
        for user in users:
            if user["username"] == username:
                # Verify hashed password using werkzeug
                if check_password_hash(user["password"], password):
                    # Save username in session to mark user as logged in
                    session["user"] = username
                    flash("Logged in successfully!", "success")
                    return redirect(url_for("feed"))
                else:
                    # Password does not match
                    flash("Incorrect password.", "danger")
                    return redirect(url_for("login"))
        
        # Username not found in users JSON
        flash("Username not found.", "danger")
        return redirect(url_for("login"))
    
    # GET request -> render login form
    return render_template("login.html")


# ---------------------- FEED ----------------------
@app.route("/feed")
def feed():
    """
    Feed page route.
    Loads all gigs from JSON, sorts by created_at descending, renders feed.html.
    """
    gigs = load_gigs()
    gigs = sorted(gigs, key=lambda g: g["created_at"], reverse=True)
    return render_template("feed.html", gigs=gigs, title="Global Feed")

@app.route("/feed/following")
@login_required
def following_feed():
    """
    Following feed page route.
    Shows gigs from users that the current user is following + their own.
    """
    current_user = session.get("user")
    gigs = load_gigs()
    following = get_following(current_user)  # List of usernames
    
    filtered_gigs = [g for g in gigs if g["username"] in following + [current_user]]
    filtered_gigs = sorted(filtered_gigs, key=lambda g: g["created_at"], reverse=True)
    return render_template("feed.html", gigs=filtered_gigs, title="Followed Activity")


# ---------------------- ADD GIG ----------------------
@app.route("/add_gig", methods=["GET","POST"])
@login_required
def add_gig():
    """
    Route for adding a new gig.
    GET: Display empty form.
    POST: Save new gig to JSON and redirect to feed.
    """
    if request.method == "POST":
        artist = request.form["artist"]
        venue = request.form["venue"]
        date = request.form["date"]
        review = request.form["review"]
        
        gigs = load_gigs()
        
        new_gig = {
            "id": str(uuid.uuid4()),           # Unique ID for gig
            "artist": artist,
            "venue": venue,
            "date": date,
            "review": review,
            "username": session["user"],       # Attach gig to current user
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        gigs.append(new_gig)
        save_gigs(gigs)
        
        flash("Gig added successfully!", "success")
        return redirect(url_for("feed"))
    
    return render_template("add_gig.html")


# ---------------------- DELETE + EDIT GIG ----------------------
@app.route("/delete_gig/<gig_id>", methods=["POST"])
@login_required
def delete_gig(gig_id):
    """
    Delete gig by ID if the current user is the owner.
    """
    gigs = load_gigs()
    for i, gig in enumerate(gigs):
        if gig.get("id") == gig_id:
            # Ensure only the owner can delete the gig
            if gig.get("username") != session["user"]:
                flash("You are not allowed to delete this gig.", "danger")
                return redirect(url_for("profile"))
            
            # Remove gig from list and save
            gigs.pop(i)
            save_gigs(gigs)
            flash("Gig deleted successfully.", "success")
            return redirect(url_for("profile"))
    
    # Gig ID not found
    flash("Gig not found.", "danger")
    return redirect(url_for("profile"))


@app.route("/edit_gig/<gig_id>", methods=["GET", "POST"])
@login_required
def edit_gig(gig_id):
    """
    Edit gig by ID.
    GET: Pre-fill form with gig data.
    POST: Update gig details and save to JSON.
    """
    gigs = load_gigs()
    # Find the gig with the matching ID
    gig = next((g for g in gigs if g.get("id") == gig_id), None)
    
    if gig is None:
        flash("Gig not found.", "danger")
        return redirect(url_for("profile"))
    
    # Check if current user is the owner
    if gig.get("username") != session["user"]:
        flash("You are not allowed to edit this gig.", "danger")
        return redirect(url_for("profile"))
    
    if request.method == "POST":
        # Update gig fields with form data
        gig["artist"] = request.form["artist"]
        gig["venue"] = request.form["venue"]
        gig["date"] = request.form["date"]
        gig["review"] = request.form["review"]
        save_gigs(gigs)
        flash("Gig updated successfully!", "success")
        return redirect(url_for("profile"))
    
    # GET request -> show edit form pre-filled with gig data
    return render_template("edit_gig.html", gig=gig, gig_id=gig_id)


# ---------------------- PROFILE ----------------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    User profile page.
    GET: Show profile info and user's gigs.
    POST: Update bio and profile picture.
    """
    current_user = session["user"]  # Get the logged-in username from session

    # Load all users from JSON file
    users = load_users()
    
    # Find the current user's data
    user = next((u for u in users if u["username"] == current_user), None)
    
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("feed"))
    
    if request.method == "POST":
        # ----------------------------
        # Update bio
        # ----------------------------
        bio = request.form.get("bio", "").strip()  # Get bio from form, default empty string
        user["bio"] = bio  # Save to user dictionary
        
        # ----------------------------
        # Update profile picture
        # ----------------------------
        file = request.files.get("profile_pic")  # Get uploaded file from form
        if file and file.filename:  # Check if a file was actually uploaded
            # Extract file extension
            file_ext = file.filename.rsplit(".", 1)[-1]
            # Create a unique filename using username + current timestamp
            filename = f"{current_user}_{int(datetime.now().timestamp())}.{file_ext}"
            # Full path to save the file
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)  # Save the file to the uploads folder
            # Update user dictionary with the filename
            user["profile_pic"] = filename
        
        # Save the updated users list back to the JSON file
        save_users(users)
        
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))
    
    # ----------------------------
    # GET request - display profile
    # ----------------------------
    # Load all gigs
    gigs = load_gigs()
    # Filter only the current user's gigs
    user_gigs = [g for g in gigs if g.get("username") == current_user]
    
    # Render profile page with user info and their gigs
    return render_template("profile.html", user=user, gigs=user_gigs)


# ---------------------- LOGOUT ----------------------
@app.route("/logout")
def logout():
    """
    Logout route.
    Clears the session for the current user.
    """
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


# ---------------------- FOLLOW/UNFOLLOW USER ----------------------
@app.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    """
    Follow a user.
    Adds the username to the current user's following list.
    """
    current_user = session["user"]

    if current_user == username:
        # Prevent users from following themselves
        flash("You cannot follow yourself!", "warning")
        return redirect(url_for("profile"))

    data = load_follows()
    
    # Find the current user's follow record
    entry = next((u for u in data if u["user"] == current_user), None)

    # If record does not exist, create one
    if not entry:
        entry = {"user": current_user, "following": []}
        data.append(entry)

    # Add the target username to the following list if not already following
    if username not in entry["following"]:
        entry["following"].append(username)
        flash(f"You are now following {username}!", "success")
    else:
        flash(f"You already follow {username}.", "info")

    save_follows(data)
    return redirect(url_for("view_user", username=username))


@app.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    """
    Unfollow a user.
    Removes the username from the current user's following list.
    """
    current_user = session["user"]
    data = load_follows()
    
    # Find current user's follow record
    entry = next((u for u in data if u["user"] == current_user), None)
    
    if entry and username in entry.get("following", []):
        # Remove user from following list
        entry["following"].remove(username)
        save_follows(data)
        flash(f"You have unfollowed {username}.", "info")
    else:
        flash(f"You are not following {username}.", "warning")
    
    return redirect(url_for("view_user", username=username))


@app.route("/user/<username>")
@login_required
def view_user(username):
    """
    View another user's profile.
    Shows profile info, gigs, and follow/unfollow status.
    """
    users = load_users()
    user = next((u for u in users if u["username"] == username), None)
    
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("feed"))
    
    gigs = load_gigs()
    user_gigs = [g for g in gigs if g["username"] == username]
    
    current_user = session["user"]
    following = get_following(current_user)
    is_following = username in following
    
    return render_template("user_profile.html", username=username, user=user, gigs=user_gigs, is_following=is_following)


# ---------------------- FOOTER PAGES ----------------------
@app.route("/about")
def about():
    """About page."""
    return render_template("about.html")

@app.route("/contact", methods=["POST", "GET"])
def contact():
    """Contact page."""
    return render_template("contact.html")

@app.route("/help")
def help():
    """Help page."""
    return render_template("help.html")


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    # Enable debug mode for easier development
    app.run(debug=True)
