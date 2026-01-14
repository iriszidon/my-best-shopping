import allure
from playwright.sync_api import Page
from playwright.async_api import expect

from python_tool_shop.page_objects.base_page import BasePage
# from python_tool_shop.page_objects.main_page import MainPage
from python_tool_shop.helper.utils import log_message, LogLevel, take_screenshot


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.proceed_to_checkout_button = self.page.locator("button.btn.btn-success, [data-test='proceed-1'], //button[text()='Proceed to checkout']")
        self.cart_total = self.page.locator("td.col-md-2.text-end, [data-test='cart-total']")


    @allure.step("get total amount")
    def get_total_price(self) -> float:
        self.wait_for_selector_to_appear(self.cart_total)
        total_amount = self.cart_total.text_content()
        take_screenshot(self.page, "shopping_cart")
        log_message(self, f"Found total amount: {total_amount}$", level=LogLevel.INFO)
        return float(total_amount)

    @allure.step("assert cart total not exceeds")
    def assert_cart_total_not_exceeds(
        self, budget_per_item: int, items_count: int
    ) -> None:
        assert budget_per_item * items_count <= 300
