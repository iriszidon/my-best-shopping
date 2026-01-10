import allure
from playwright.sync_api import Page
from playwright.async_api import expect

from python_tool_shop.page_objects.base_page import BasePage
from python_tool_shop.page_objects.main_page import MainPage
from python_tool_shop.helper.utils import log_message, LogLevel, take_screenshot


class LoginPage(BasePage):
    def __init__(self, page:Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.accept_cookies_button = self.page.locator("[data-testid='uc-accept-all-button']")
        self.nav_sign_in_button = self.page.locator("a[title='Login or register']")
        self.username_field = self.page.locator("input[type='email']")
        self.password_field = self.page.locator("input[type='password']")
        self.login_button = self.page.locator("button[value='Login']")
        self.error_message = self.page.locator("//div[@id='email_container']")


    def get_error_message(self, expected_error_message):
        return self.error_message.locator(f"//div[contains(text(), '{expected_error_message}')]") # chain the locator

    @allure.step("login")
    def perform_login(self, username: str, password: str) ->MainPage:
        log_message(self.logger,"performing login",level=LogLevel.INFO)
        self.click_element(self.accept_cookies_button)
        self.click_element(self.nav_sign_in_button) # Click nav sign in button
        self.type_text(self.username_field, username)
        self.type_text(self.password_field, password)
        self.click_element(self.login_button)
        self.page.wait_for_load_state("networkidle")
        if self.login_button.is_visible():
            log_message(self.logger, "Login failed", level=LogLevel.ERROR)
            take_screenshot(self.page, "login_failed")
            return None  # return None when the login fails
        return MainPage(self.page)  # Return MainPage only if the login succeeded

