from flask import Flask, render_template, request, redirect, flash, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

DATA_FILE = "data/gigs.json"

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d %b %Y'):
    """Format a date string like '2025-11-21' to '21 Nov 2025'"""
    dt = datetime.strptime(value, "%Y-%m-%d")
    return dt.strftime(format)


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

@app.route("/delete_gig/<int:index>", methods=["POST"])
def delete_gig(index):
    gigs = load_gigs()
    if 0 <= index < len(gigs):
        gigs.pop(index)
        save_gigs(gigs)
        flash("Gig deleted successfully.", "success")
    return redirect(url_for("feed"))

@app.route("/edit_gig/<int:index>", methods=["GET", "POST"])
def edit_gig(index):
    gigs = load_gigs()
    
    if index < 0 or index >= len(gigs):
        flash("Invalid gig.index.", "danger")
        return redirect(url_for("feed"))
    
    if request.method == "POST":
        # Update gig details
        gigs[index]["artist"] = request.form["artist"]
        gigs[index]["venue"] = request.form["venue"]
        gigs[index]["date"] = request.form["date"]
        gigs[index]["review"] = request.form["review"]
        save_gigs(gigs)
        flash("Gig updated successfully!", "success")
        return redirect(url_for("feed"))
    
    gig = gigs[index]
    return render_template("edit_gig.html", gig=gig, index=index)

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)