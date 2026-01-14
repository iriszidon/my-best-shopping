import allure
from playwright.sync_api import Page
from python_tool_shop.page_objects.base_page import BasePage
from python_tool_shop.helper.utils import take_screenshot


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.proceed_to_checkout_button = self.page.locator("button.btn.btn-success, [data-test='proceed-1'], //button[text()='Proceed to checkout']")
        self.cart_total = self.page.locator("[data-test='cart-total']")

    @allure.step("Get total amount")
    def get_total_price(self) -> float:
        self.wait_for_selector_to_appear(self.cart_total)
        total_amount = self.cart_total.text_content()
        float_total_amount = float(total_amount[1:])
        take_screenshot(self.page, "shopping_cart")
        self.logger.info(f"Found total amount: {total_amount}")
        return float_total_amount

    @allure.step("Verify that cart total does not exceed a maximum")
    def assert_cart_total_not_exceeds(self, budget_per_item: int, items_count: int, total_budget: float) -> None:
        assert total_budget <= items_count * budget_per_item, \
            f"The total amount {total_budget} should be less than {items_count * budget_per_item}"
