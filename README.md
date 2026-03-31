# Job Application Tracker

A full-stack web application to track job applications, built with Python/Flask, MySQL, and HTML/CSS.

## Features
- Track companies, jobs, applications, and contacts
- Dashboard with application statistics
- Job Match feature to rank jobs by skill match percentage

## Tech Stack
- **Backend:** Python 3 / Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, Chart.js

## Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/isaiahL21/job-tracker.git
cd job-tracker
```

### 2. Install dependencies
```
pip install flask mysql-connector-python
```

### 3. Set up the database
- Open MySQL Workbench and connect to your local server
- Open and run `schema.sql` to create the database and tables

### 4. Configure database connection
- Open `database.py`
- Replace `YOUR_PASSWORD` with your MySQL root password

### 5. Run the app
```
py app.py
```

### 6. Open in browser
```
http://127.0.0.1:5000
```

## Project Structure
```
job_tracker/
├── app.py              # Main Flask application
├── database.py         # Database connection
├── schema.sql          # Database creation script
├── templates/          # HTML templates
├── static/             # CSS
├── AI_USAGE.md         # AI tools documentation
└── README.md           # This file
```