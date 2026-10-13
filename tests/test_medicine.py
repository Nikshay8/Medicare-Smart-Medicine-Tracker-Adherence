"""Medicine CRUD + dose-status tests. These use 'auth_page' = already logged in.

Each test gets its OWN medicine (via the 'medicine' fixture), so tests are independent:
they can run in any order and don't rely on data that was already in the database.
"""

import re

import pytest
from playwright.sync_api import expect

from helpers import unique_name
from pages.dashboard_page import DashboardPage
from pages.medicine_form_page import AddMedicinePage, EditMedicinePage

pytestmark = pytest.mark.medicine  # tags every test in this file as "medicine"


@pytest.mark.smoke
def test_add_medicine(auth_page, created_medicines):
    name = unique_name()
    created_medicines.append(name)  # so it gets cleaned up afterwards

    AddMedicinePage(auth_page).open().save(name, hour="08", minute="00", period="AM")

    dashboard = DashboardPage(auth_page)
    expect(auth_page).to_have_url(re.compile(r"/dashboard/$"))
    expect(dashboard.medicine_card(name)).to_be_visible()
    expect(dashboard.time_of(name)).to_contain_text("08:00 AM")


def test_add_medicine_with_empty_fields_shows_error(auth_page):
    add_page = AddMedicinePage(auth_page).open()
    add_page.fill_form(name="", hour="", minute="", period="")
    # Remove the browser's "required" check so add_medicine.js validation is what we test
    auth_page.locator("#medicineForm").evaluate("form => form.setAttribute('novalidate', '')")
    add_page.submit()

    expect(add_page.client_error).to_contain_text("All fields are required.")


def test_add_duplicate_medicine_is_rejected(auth_page, medicine):
    # 'medicine' already exists at 08:00 AM - adding the same name + time must fail
    add_page = AddMedicinePage(auth_page).open()
    add_page.save(medicine.name, medicine.hour, medicine.minute, medicine.period)

    # This rule is checked by the Django server, so we look at the server error box
    expect(add_page.server_error).to_contain_text("This medicine at the same time already exists.")


def test_edit_medicine_name(auth_page, medicine, created_medicines):
    new_name = f"{medicine.name} Edited"
    created_medicines.append(new_name)  # cleanup must also remove the renamed one

    dashboard = DashboardPage(auth_page).open()
    dashboard.click_edit(medicine.name)
    edit_page = EditMedicinePage(auth_page)
    edit_page.name_input.fill(new_name)
    edit_page.submit()

    expect(dashboard.medicine_card(new_name)).to_be_visible()
    expect(dashboard.medicine_card(medicine.name)).to_have_count(0)  # old name is gone


def test_edit_medicine_time(auth_page, medicine):
    dashboard = DashboardPage(auth_page).open()
    dashboard.click_edit(medicine.name)
    edit_page = EditMedicinePage(auth_page)
    edit_page.hour_select.select_option("09")
    edit_page.minute_select.select_option("30")
    edit_page.period_select.select_option("PM")
    edit_page.submit()

    expect(dashboard.time_of(medicine.name)).to_contain_text("09:30 PM")


def test_mark_medicine_taken(auth_page, medicine):
    dashboard = DashboardPage(auth_page).open()
    expect(dashboard.status_of(medicine.name)).to_contain_text("No status yet")  # starting point

    dashboard.mark_taken(medicine.name)

    expect(dashboard.status_of(medicine.name)).to_contain_text("taken")


def test_mark_medicine_missed(auth_page, medicine):
    dashboard = DashboardPage(auth_page).open()

    dashboard.mark_missed(medicine.name)

    expect(dashboard.status_of(medicine.name)).to_contain_text("missed")


def test_delete_medicine(auth_page, medicine):
    dashboard = DashboardPage(auth_page).open()
    expect(dashboard.medicine_card(medicine.name)).to_be_visible()

    dashboard.delete(medicine.name)

    expect(dashboard.medicine_card(medicine.name)).to_have_count(0)