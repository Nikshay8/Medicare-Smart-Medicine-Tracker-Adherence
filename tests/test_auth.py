"""Login and access-control tests. These use the plain 'page' fixture = NOT logged in."""

import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

pytestmark = pytest.mark.auth  # tags every test in this file as "auth"


@pytest.mark.smoke
def test_login_with_valid_credentials(page: Page, credentials):
    LoginPage(page).open().login(credentials["username"], credentials["password"])

    expect(page).to_have_url(re.compile(r"/dashboard/$"))


def test_login_with_invalid_credentials_shows_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("wronguser", "wrongpassword")

    # This error comes from the Django server (valid format, wrong credentials)
    expect(login_page.server_error).to_be_visible()
    expect(login_page.server_error).to_contain_text("Invalid username or password.")


def test_login_with_short_password_shows_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("testuser", "abc")

    # Caught by login.js in the browser before the form is even sent
    expect(login_page.client_error).to_contain_text("Password must be at least 8 characters.")
    expect(page).to_have_url(re.compile(r"/login/$"))  # still on the login page


def test_login_with_empty_fields_shows_error(page: Page):
    login_page = LoginPage(page).open()
    # The inputs have the HTML "required" attribute, so we remove the browser's own
    # check to make sure OUR validation message (from login.js) is what gets tested.
    page.locator("#loginForm").evaluate("form => form.setAttribute('novalidate', '')")
    login_page.submit_button.click()

    expect(login_page.client_error).to_contain_text("All fields are required.")


def test_dashboard_redirects_to_login_when_not_logged_in(page: Page):
    page.goto("/dashboard/")

    # @login_required should bounce anonymous users to the login page
    expect(page).to_have_url(re.compile(r"/login/"))