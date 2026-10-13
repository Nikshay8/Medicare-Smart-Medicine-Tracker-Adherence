from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for /login/ - all selectors for this page live here and only here."""

    path = "/login/"

    def __init__(self, page):
        super().__init__(page)
        # Locators are lazy: Playwright only looks for the element when we use it
        self.username_input = page.locator("#loginUsername")
        self.password_input = page.locator("#loginPassword")
        self.submit_button = page.locator("button.form-submit")

        # Two different error elements exist on this page, so we keep them separate:
        # - server_error: <div class="error-box"> rendered by Django (wrong password etc.)
        # - client_error: <p id="loginError"> filled by login.js (empty / short password)
        # A plain ".error-box" would match both and break Playwright's strict mode.
        self.server_error = page.locator("div.error-box")
        self.client_error = page.locator("#loginError")

    def login(self, username: str, password: str):
        """Fill the form and submit. Does NOT assert anything - tests decide what to check."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()