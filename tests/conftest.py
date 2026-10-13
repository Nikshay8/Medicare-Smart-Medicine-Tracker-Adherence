"""Shared fixtures for all tests.

Prerequisites before running:
  1. The Django app is running (python manage.py runserver)
  2. A user exists with the credentials below (defaults: testuser / testpass123)
     You can override them without editing code:  set TEST_USERNAME / TEST_PASSWORD
"""

import os
import re

import pytest
from playwright.sync_api import expect

from helpers import Medicine, unique_name
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.medicine_form_page import AddMedicinePage

# Credentials come from environment variables, not hardcoded in the tests
TEST_USERNAME = os.getenv("TEST_USERNAME", "testuser")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "testpass123")


@pytest.fixture(scope="session")
def credentials():
    """Single place where tests get the username/password."""
    return {"username": TEST_USERNAME, "password": TEST_PASSWORD}


@pytest.fixture(scope="session")
def auth_state(browser, base_url, credentials, tmp_path_factory):
    """Log in through the UI ONCE per test run and save the cookies to a file.

    Every other test re-uses this file, so it starts already logged in.
    This is much faster than logging in at the start of every test.
    """
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).open().login(credentials["username"], credentials["password"])
    # If this fails, the test user probably doesn't exist or the server isn't running
    expect(page).to_have_url(re.compile(r"/dashboard/$"))

    state_file = tmp_path_factory.mktemp("auth") / "state.json"
    context.storage_state(path=str(state_file))
    context.close()
    return str(state_file)


@pytest.fixture
def auth_page(new_context, auth_state):
    """A browser page that is ALREADY logged in (uses the saved login state).

    'new_context' is a pytest-playwright fixture; contexts made with it still get
    the trace / screenshot / video on failure that we configured in pytest.ini.
    Tests that need a logged-out user (login tests) use the normal 'page' fixture.
    """
    context = new_context(storage_state=auth_state)
    return context.new_page()


@pytest.fixture
def created_medicines(auth_page):
    """A list tests can append medicine names to. After the test finishes, every
    name in the list is deleted from the app, so tests leave no junk behind."""
    names = []
    yield names  # the test runs here

    # ---- teardown: runs even if the test failed ----
    dashboard = DashboardPage(auth_page).open()
    for name in names:
        if dashboard.medicine_card(name).count():  # only delete if it still exists
            dashboard.delete(name)
            expect(dashboard.medicine_card(name)).to_have_count(0)


@pytest.fixture
def medicine(auth_page, created_medicines):
    """A fresh medicine created for ONE test (so the test doesn't depend on old data).
    It is deleted automatically afterwards by 'created_medicines'."""
    med = Medicine(name=unique_name())
    created_medicines.append(med.name)
    AddMedicinePage(auth_page).open().save(med.name, med.hour, med.minute, med.period)
    expect(DashboardPage(auth_page).medicine_card(med.name)).to_be_visible()
    return med