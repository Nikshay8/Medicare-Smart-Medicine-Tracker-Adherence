import re

from .base_page import BasePage


class DashboardPage(BasePage):
    """Page object for /dashboard/ - the list of medicines and their actions."""

    path = "/dashboard/"

    def medicine_card(self, name: str):
        """Return the card of ONE medicine, found by its exact name.

        Why not use .first? Tests would then touch whatever medicine happens to be on top.
        Finding by name makes every test work only on its own data.
        """
        return self.page.locator(".med-card-e").filter(
            has=self.page.get_by_text(name, exact=True)
        )

    def status_of(self, name: str):
        """The status tag of a medicine (e.g. 'taken', 'missed', 'No status yet')."""
        return self.medicine_card(name).locator(".tag-status")

    def time_of(self, name: str):
        """The 'Daily at 08:00 AM' text of a medicine."""
        return self.medicine_card(name).locator(".med-time-lg")

    def mark_taken(self, name: str):
        self.medicine_card(name).locator(".bpe-taken").click()

    def mark_missed(self, name: str):
        self.medicine_card(name).locator(".bpe-missed").click()

    def click_edit(self, name: str):
        self.medicine_card(name).locator(".bpe-edit").click()

    def delete(self, name: str):
        """Delete a medicine. The link opens a native confirm() popup, so we accept it.

        The handler must be registered BEFORE the click, otherwise Playwright
        auto-dismisses the dialog and the delete never happens.
        """
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.medicine_card(name).locator(".bpe-delete").click()