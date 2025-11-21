from flask import Flask, render_template, request, redirect, flash, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

DATA_FILE = "data/gigs.json"

def load_gigs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_gigs(gigs):
    with open(DATA_FILE, "w") as f:
        json.dump(gigs, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/feed")
def feed():
    gigs = load_gigs()
    return render_template("feed.html", gigs=gigs)

@app.route("/add_gig", methods=["GET","POST"])
def add_gig():
    if request.method == "POST":
        # Get form data
        artist = request.form["artist"]
        venue = request.form["venue"]
        date = request.form["date"]
        review = request.form["review"]
        
        # Load gigs & append new one
        gigs = load_gigs()
        gigs.append({
            "artist": artist,
            "venue": venue,
            "date": date,
            "review": review
        })
        
        # Save updated list
        save_gigs(gigs)
        
        flash("Gig added successfully!", "success")
        return redirect(url_for("feed"))
    
    # GET request shows the form
    return render_template("add_gig.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)