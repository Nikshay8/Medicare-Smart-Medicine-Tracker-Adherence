# Medicare – Smart Medicine Adherence & Caregiver Alert System

A Django-based medicine adherence web app for elderly users with caregiver email alerts and missed dose tracking.

## Tech Stack
- Python, Django
- MySQL
- HTML, CSS, JavaScript

## Features
- User registration, login, and session-based authentication
- Medicine scheduling with add, edit, and delete functionality
- Missed dose streak detection with automatic caregiver email alerts
- 30-day adherence reports and medicine history dashboard
- Duplicate entry prevention and time-aware dose reminders

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/Nikshay8/Medicare---Smart-Medicine-Tracker-Adherence.git

### 2. Install dependencies
pip install -r requirements.txt

### 3. Configure database
Update DATABASES settings in settings.py with your MySQL credentials

### 4. Configure email
Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py

### 5. Run migrations
python manage.py migrate

### 6. Start the server
python manage.py runserver
