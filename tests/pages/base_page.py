from playwright.sync_api import Page


class BasePage:
    """Parent of all page objects. Holds the Playwright page and common helpers."""

    # Each child page sets its own URL path, e.g. "/login/"
    path = ""

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        """Go to this page. Relative path works because base_url is set in pytest.ini."""
        self.page.goto(self.path)
        return self  # returning self lets us chain: LoginPage(page).open().login(...)