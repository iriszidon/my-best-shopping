import allure
from playwright.sync_api import Page
from python_tool_shop.page_objects.base_page import BasePage
from python_tool_shop.helper.utils import log_message, LogLevel, take_screenshot


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.first_name_field = self.find_element("[data-test='first-name'], #first-name, [formcontrolname='first_name']")
        self.last_name_field = self.find_element("[data-test='last-name'], #last-name, [formcontrolname='last-name']")
        self.date_of_birth_field = self.find_element("[data-test='dob'], #dob, [formcontrolname='dob']")
        self.street_field = self.find_element("[data-test='street'], #street, [placeholder='Your street *']")
        self.postal_code_field = self.find_element("[data-test='postal_code'], #postal_code, [placeholder='Your Postcode *']")
        self.city_field = self.find_element("[data-test='city'], #city, [placeholder='Your City *']")
        self.state_field = self.find_element("[data-test='state'], #state, [placeholder='Your State *']")
        self.country_field = self.find_element("[data-test='country'], #country, [formcontrolname='country']")
        self.phone_field = self.find_element("[data-test='phone'], #phone, [placeholder='Your phone *']")
        self.email_address_field = self.find_element("[data-test='email'], #email, [placeholder='Your email *']")
        self.password_field = self.find_element("[data-test='password'], #password, [placeholder='Your password']")
        self.register_button = self.find_element("[data-test='register-submit'], [type=submit], //button[text()='Register ']")


    @allure.step("register")
    def perform_registration(self, username: str, last_name: str) -> None:
        log_message(self.logger, "performing login", level=LogLevel.INFO)
        self.type_text(self.first_name_field, username)
        self.type_text(self.last_name_field, last_name)
        self.type_text(self.date_of_birth_field, "1975-04-01")
        self.type_text(self.street_field, "Hadar")
        self.type_text(self.postal_code_field, "12345")
        self.type_text(self.city_field, "London")
        self.type_text(self.state_field, "Victoria")
        self.page.locator('[data-test="country"]').select_option("Albania")
        self.page.wait_for_timeout(500)
        self.type_text(self.phone_field, "05088447743")
        self.type_text(self.email_address_field, "iriso@finonex.com")
        self.type_text(self.password_field, "Viva#100")
        self.click_element(self.register_button)
        self.page.wait_for_load_state("networkidle")
        # main_page = None(self.page)
        # return main_page

