from playwright.sync_api import expect

from python_tool_shop.helper.utils import log_message, LogLevel, take_screenshot
from python_tool_shop.page_objects.base_page import BasePage


class AppValidation(BasePage):
    def __init__(self, setup_all_pages):
        self.login_page, self.main_page = setup_all_pages
        super().__init__(self.login_page)
        super().__init__(self.main_page)

    def validate_user_logged_in(self):
        login_button = self.login_page.login_button
        try:
            expect(login_button).not_to_be_visible(), "Failed to login"
        except Exception as e:
            log_message(self.logger, "login failed", LogLevel.ERROR)
            take_screenshot(self.page, "login failed")
            raise Exception("Login failed, the login button still appears") from e

    def validate_home_page_is_loaded(self):
        search_button = self.main_page.search_button
        try:
            expect(search_button).to_be_visible(), "Failed to load the page"
        except Exception as e:
            log_message(self.logger, "load failed", LogLevel.ERROR)
            take_screenshot(self.page, "load failed")
            raise Exception("Load failed, the search button does not appear") from e