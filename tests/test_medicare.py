"""
Playwright test suite for MediCare — covers login, medicine CRUD,
and dose-status flows. Run with: pytest tests/test_medicare.py -v --headed
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "testuser"
PASSWORD = "testpass123"


# Logs in with a known-good test user. Called at the start of every test
# that needs an authenticated session, so login logic isn't repeated everywhere.
def login(page: Page):
    page.goto(f"{BASE_URL}/login/")
    page.fill("#loginUsername", USERNAME)
    page.fill("#loginPassword", PASSWORD)
    page.click("button.form-submit")


# Checks that correct credentials actually log the user in and land them
# on the dashboard.
def test_login_valid_credentials(page: Page):
    login(page)
    expect(page).to_have_url(f"{BASE_URL}/dashboard/")


# Checks that wrong credentials are rejected and the server's error message
# is shown. Uses "div.error-box" specifically because the page has a second,
# empty element with the same class (used for client-side JS validation) —
# a plain ".error-box" selector would match both and fail.
def test_login_invalid_credentials(page: Page):
    page.goto(f"{BASE_URL}/login/")
    page.fill("#loginUsername", "wronguser")
    page.fill("#loginPassword", "wrongpassword")
    page.click("button.form-submit")

    error = page.locator("div.error-box")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Invalid username or password.")

# Checks server-side validation catches a too-short password before
# even trying to authenticate — should show the length error message.
def test_login_short_password(page: Page):
    page.goto(f"{BASE_URL}/login/")
    page.fill("#loginUsername", "testuser")
    page.fill("#loginPassword", "abc")
    page.click("button.form-submit")
    error = page.locator("#loginError")
    expect(error).to_contain_text("Password must be at least 8 characters.")


# Adds a new medicine through the form and confirms it shows up on the
# dashboard afterward. URL check includes the trailing slash since Django
# redirects to "/dashboard/", not "/dashboard".
def test_add_medicine(page: Page):
    login(page)
    page.goto(f"{BASE_URL}/add-medicine/")

    page.fill("#medicineName", "Paracetamol")
    page.select_option("#medicineHour", "08")
    page.select_option("#medicineMinute", "00")
    page.select_option("#medicinePeriod", "AM")
    page.click("button.form-submit")

    expect(page).to_have_url(f"{BASE_URL}/dashboard/")
    expect(page.locator(".med-name-lg", has_text="Paracetamol")).to_be_visible()


# Opens the edit page for the first medicine in the list and updates its
# name. Note the field id here is "editMedicineName", not "medicineName" —
# the edit template uses a different naming convention than the add template.
def test_edit_medicine(page: Page):
    login(page)
    page.goto(f"{BASE_URL}/dashboard/")

    page.locator(".bpe-edit").first.click()
    page.fill("#editMedicineName", "Paracetamol 650")
    page.click("button.form-submit")

    expect(page.locator(".med-name-lg", has_text="Paracetamol 650")).to_be_visible()


# Clicks "Taken" on the first medicine and checks the status tag updates
# to reflect that.
def test_mark_medicine_taken(page: Page):
    login(page)
    page.goto(f"{BASE_URL}/dashboard/")

    page.locator(".bpe-taken").first.click()
    expect(page.locator(".tag-status").first).to_contain_text("taken")


# Deletes the first medicine in the list and confirms it's gone from the
# dashboard. The delete link triggers a native browser confirm() dialog,
# which Playwright won't handle automatically — page.once("dialog", ...)
# registers a one-time handler that accepts it before the click resolves.
def test_delete_medicine(page: Page):
    login(page)
    page.goto(f"{BASE_URL}/dashboard/")

    med_name = page.locator(".med-name-lg").first.text_content()

    page.once("dialog", lambda dialog: dialog.accept())
    page.locator(".bpe-delete").first.click()

    expect(page.locator(".med-name-lg", has_text=med_name)).not_to_be_visible()