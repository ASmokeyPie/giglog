from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/feed")
def feed():
    return render_template("feed.html")

@app.route("/add_gig")
def add_gig():
    return render_template("add_gig.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)