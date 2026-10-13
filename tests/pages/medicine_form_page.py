from .base_page import BasePage


class MedicineFormPage(BasePage):
    """Shared logic for the Add and Edit medicine forms (they look the same,
    only the element ids differ - see the two child classes below)."""

    # Child classes fill these in with their own ids
    name_id = ""
    hour_id = ""
    minute_id = ""
    period_id = ""

    def __init__(self, page):
        super().__init__(page)
        self.name_input = page.locator(self.name_id)
        self.hour_select = page.locator(self.hour_id)
        self.minute_select = page.locator(self.minute_id)
        self.period_select = page.locator(self.period_id)
        self.submit_button = page.locator("button.form-submit")

        # Server-side error (Django): <div class="error-box">, e.g. duplicate medicine
        self.server_error = page.locator("div.error-box")

    def fill_form(self, name: str, hour: str, minute: str, period: str):
        """Fill every field. Pass "" for hour/minute/period to leave it unselected."""
        self.name_input.fill(name)
        # Skip empty values so a dropdown can stay on its default "Hour/Min/AM-PM" option
        if hour:
            self.hour_select.select_option(hour)
        if minute:
            self.minute_select.select_option(minute)
        if period:
            self.period_select.select_option(period)

    def submit(self):
        self.submit_button.click()

    def save(self, name: str, hour: str = "08", minute: str = "00", period: str = "AM"):
        """Fill + submit in one call (the common 'happy path')."""
        self.fill_form(name, hour, minute, period)
        self.submit()


class AddMedicinePage(MedicineFormPage):
    """/add-medicine/"""

    path = "/add-medicine/"
    name_id = "#medicineName"
    hour_id = "#medicineHour"
    minute_id = "#medicineMinute"
    period_id = "#medicinePeriod"

    def __init__(self, page):
        super().__init__(page)
        # Client-side error: <p id="medicineError"> filled by add_medicine.js
        self.client_error = page.locator("#medicineError")


class EditMedicinePage(MedicineFormPage):
    """/edit-medicine/<id>/ - we reach it by clicking 'Edit' on the dashboard,
    so there is no fixed path. Note the ids differ from the Add page (edit... prefix)."""

    name_id = "#editMedicineName"
    hour_id = "#editMedicineHour"
    minute_id = "#editMedicineMinute"
    period_id = "#editMedicinePeriod"