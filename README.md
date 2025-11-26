# Giglog

**Giglog** is a simple web application built with **Flask** that allows users to log, edit, and view music gigs they have attended. Users can register, create profiles, add gig entries, follow other users, and browse a global or followed users' feed. 

The app uses JSON files to store users, gigs, and follow data, making it lightweight and easy to run locally.

---

[![Python 3](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-2.x-purple)](https://palletsprojects.com/p/flask/)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/ASmokeyPie/giglog/python-packages.yml?branch=main)](https://github.com/ASmokeyPie/giglog/actions)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)  

---

## Features

### User Management
- Register and log in with username and email.
- Secure password storage with hashing.
- Profile page with bio and profile picture upload.
- View other users' profiles and follow/unfollow them.

### Gigs
- Add new gigs with details: artist, venue, date, review.
- Edit or delete your own gigs.
- Each gig is linked to the user who created it.
- Global feed showing all gigs.
- Followed feed showing gigs from users you follow.

### Interface
- Bootstrap 5 responsive UI.
- Flash messages for feedback.
- Navbar with dynamic login/logout links.
- Sticky footer that stays at the bottom on short pages.

---

## Installation

1. **Clone the repository**:

```
git clone https://github.com/ASmokeyPie/giglog.git
cd giglog
```
2. Create a virtual environment:
```
python -m venv env
```
3. Activate the virtual environment:

- Windows:
```
env\Scripts\activate
```
- macOS/Linux:
```
source env/bin/activate
```
4. Install dependencies:
```
pip install flask werkzeug
```

---

## Running the App

1. Ensure the data/ folder exists with gigs.json, users.json, and follows.json. Empty lists [] can be used for initial JSON files.

2. Run the Flask app:
```
python app.py
```
3. Open your browser and visit:
```
http://127.0.0.1:5000
```

---

## Usage

- Register a new account or log in.

- Update your profile with bio and picture.

- Add gigs using the Add Gig page.

- View your gigs on your Profile page.

- Edit or delete your own gigs.

- Browse the Feed for all gigs.

- Follow other users to see their gigs in the Following Feed.

---

## Notes
- Data is stored in local JSON files (data/gigs.json, data/users.json, data/follows.json).

- Profile pictures are uploaded to static/uploads/.

- The app is for local development and learning purposes. Not recommended for production use.

---

## Technologies

- Python 3

- Flask

- Werkzeug (password hashing)

- Bootstrap 5 (UI)

- JSON (data storage)