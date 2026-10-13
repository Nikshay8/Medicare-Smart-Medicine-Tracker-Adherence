![Playwright Tests](https://github.com/Nikshay8/Medicare-Smart-Medicine-Tracker-Adherence/actions/workflows/playwright.yml/badge.svg)

# Medicare – Smart Medicine Adherence & Caregiver Alert System

A Django-based medicine adherence web app for elderly users with caregiver email alerts, missed dose tracking, and an AI-powered chatbot assistant.

## Version
**v3.0.0** — Refactored Playwright tests to Page Object Model with fixtures, plus GitHub Actions CI.

## Tech Stack
- Python, Django
- MySQL
- HTML, CSS, JavaScript
- Google Gemini API (chatbot)
- Playwright (automated testing)

## Features
- User registration, login, and session-based authentication
- Medicine scheduling with add, edit, and delete functionality
- Missed dose streak detection with automatic caregiver email alerts
- 30-day adherence reports and medicine history dashboard
- Duplicate entry prevention and time-aware dose reminders
- AI chatbot (powered by Gemini) for medicine-related queries and support
- End-to-end test coverage using Playwright

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/Nikshay8/Medicare-Smart-Medicine-Tracker-Adherence.git

### 2. Install dependencies
pip install -r requirements.txt

### 3. Configure database
Update DATABASES settings in settings.py with your MySQL credentials

### 4. Configure email
Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py

### 5. Configure Gemini API
Add your Gemini API key to the `.env` file (see `.env.example` if available)

### 6. Run migrations
python manage.py migrate

### 7. Start the server
python manage.py runserver

## Running Tests

This project uses Playwright for end-to-end testing.

pip install -r requirements-test.txt
playwright install chromium
pytest
