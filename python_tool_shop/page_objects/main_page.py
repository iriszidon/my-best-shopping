from playwright.sync_api import Page

from python_tool_shop.page_objects.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.search_button = self.page.locator("[data-test='search-submit']")
        self.top_bar = self.page.get_by_text("Practice Black Box Testing & Bug Hunting")

