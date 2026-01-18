import allure
from playwright.sync_api import Page

from page_objects.register_page import RegisterPage
from python_tool_shop.page_objects.base_page import BasePage
from python_tool_shop.helper.utils import log_message, LogLevel, take_screenshot


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.username_field = self.find_element("[data-test='email'], #email, [type='email']")
        self.password_field = self.find_element("[data-test='password'], #password, [type='password']")
        self.login_button = self.find_element("[data-test='login-submit'], [aria-label=Login], [type='submit']")
        self.register_your_account_button = self.find_element("[data-test='register-link'], [routerlink=/auth/register], [aria-label='Register your account']")


    @allure.step("Login to the website")
    def perform_login(self, username: str, password: str) -> None:
        log_message(self.logger, "performing login", level=LogLevel.INFO)
        self.type_text(self.username_field, username)
        self.type_text(self.password_field, password)
        self.click_element(self.login_button)
        self.page.wait_for_load_state("networkidle")
        is_login_button_visible = self.login_button.is_visible()
        assert not is_login_button_visible, "Login button should not be visible after login."



    @allure.step("Click on register your account link")
    def open_register_your_account_page(self) -> RegisterPage:
        log_message(self.logger, "Click on register your account link", level=LogLevel.INFO)
        self.click_element(self.register_your_account_button)
        registration_page = RegisterPage(self.page)
        return registration_page

