# **GigLog**

A simple Flask-based web app for logging gigs, viewing activity feeds, and following other users.

GigLog is a lightweight social-style application built with Flask.
Users can register, log in, add gigs they’ve attended, and browse a live feed of activity. A follow system lets users keep up with the gig history of their friends or favourite people.

This project is designed as a learning and assessment piece for a university module and aims to demonstrate full-stack fundamentals using Python, Flask, HTML, Bootstrap, and JSON data storage.

---

<p align="left">
<!-- Python version --> <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt="Python 3.13">
<!-- Flask --> <img src="https://img.shields.io/badge/Flask-3.0-black?logo=flask" alt="Flask">
<!-- GitHub Actions CI badge --> <img src="https://github.com/ASmokeyPie/giglog/actions/workflows/python-package.yml/badge.svg" alt="CI Status">
<!-- Last commit --> <img src="https://img.shields.io/github/last-commit/ASmokeyPie/giglog?color=yellow" alt="Last Commit">

---

## Features
### User Accounts

- User registration with validation

- Secure login using hashed passwords

- Session-based authentication

- Profile page showing all gigs created by the user

### Gig Logging

Add gigs with:

- Artist

- Venue

- Date

- Review

Edit and delete existing gig entries

All gig data stored in gigs.json

### Activity Feeds

Global Feed: Shows all gigs from all users

Following Activity: Shows gigs only from people the user follows

Feed items display the artist, venue, date, review, and creator

### Follow System

Users can view other users’ profiles

Follow/unfollow functionality

Following data stored in follows.json

Followed activity appears in a dedicated feed tab

### JSON-Based Data Storage

No database required — the app uses JSON for persistence:

users.json — user accounts

gigs.json — gig entries

follows.json — follow relationships

---

## Project Structure

giglog/
│
├── app.py                # Main Flask application
├── data/
│   ├── users.json        # Registered users
│   ├── gigs.json         # Logged gigs
│   └── follows.json      # Follow relationships
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── feed.html
│   ├── add_gig.html
│   ├── edit_gig.html
│   ├── profile.html
│   └── user_profile.html
│
└── static/
    ├── css/
    └── js/

---

## Technologies Used

- Python 3.13

- Flask

- Werkzeug for secure password hashing

- Bootstrap 5 for UI

- JSON files for persistence

- Jinja2 templating

---

## Running the App Locally

1. Clone the repository
'
git clone https://github.com/https://github.com/ASmokeyPie/giglog.git
cd giglog
'

2. Create a virtual environment
'python -m venv env'

3. Activate the environment

Windows:
'env\Scripts\activate'

Mac/Linux:
'source env/bin/activate'

4. Install dependencies

'pip install -r requirements.txt'

5. Run the development server

'python app.py'


App will run at:
http://127.0.0.1:5000

---

## Security Notes

This app uses session cookies but does not implement CSRF protection.

JSON storage is not encrypted.

For production, a real database and improved auth would be required.

---

##Future Improvements

- User avatars

- Real-time notifications

- Search for gigs or users

- Pagination for feeds

- Swap JSON files for a SQL database

- Unfollow button

---

## License

This project is for educational use.
You may modify or adapt it freely.