import allure
from playwright.sync_api import Page
from python_tool_shop.page_objects.base_page import BasePage
from python_tool_shop.helper.utils import take_screenshot


class ToolPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.add_to_cart_button = self.find_element("[data-test='add-to-cart'], #btn-add-to-cart, button.btn-success.btn")
        self.toast_message = self.find_element(".toast-message")
        self.home_page_button = self.find_element("[data-test='nav-home'], a.nav-link.active, [aria-current='page']")


    @allure.step("Add a tool into the cart")
    def add_item_to_cart(self, url:str) -> None:
        self.wait_for_selector_to_appear(self.add_to_cart_button)
        # take screenshot foreach selected item
        take_screenshot(self.page, name=url[-27:])
        self.click_element(self.add_to_cart_button)
        self.wait_for_selector_to_appear(self.toast_message)
        # go back to search page
        self.click_element(self.home_page_button)

