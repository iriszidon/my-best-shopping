from playwright.sync_api import Page
from typing import List
import allure

from python_tool_shop.page_objects.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.search_button = self.page.locator("[data-test='search-submit'], button.btn.btn-secondary:has-text('Search')")
        self.search_test_box = self.page.locator("#search-query, [data-test='search-query'], [placeholder=Search]")
        self.top_bar = self.page.get_by_text("Practice Black Box Testing & Bug Hunting")

    def login(self):
        pass

    @allure.step("search items by name under price")
    def search_items_by_name_under_price(
        self, query: str, max_price: int, limit=5
    ) -> List[str]:
        # search by a query
        self.type_text(self.search_test_box, query)
        self.click_element(self.search_button)
        # use min/max filter if exists
        # get  first 5 (limit) items that have a price <= max_price
        # in case of less than 5 items exist:
        # if there is a next button, click next and get items from next page
        # if no paging, get less than 5 items
        # return a url array of 5 items that meet the condition, or less.
        # example urls = search_items_by_name_under_price("hammer", 220, 5)
        return ["a", "b", "c"]

    @allure.step("add items to cart")
    def add_items_to_cart(self, urls: List[str]) -> None:
        # foreach url go to url
        # choose a size and a color if exists
        # take screenshot foreach selected item
        # click add to cart
        # go back to search page
        pass

    @allure.step("assert cart total not exceeds")
    def assert_cart_total_not_exceeds(
        self, budget_per_item: int, items_count: int
    ) -> None:
        # open that cart
        # read to total amount
        # Calculate budget_per_item * items_count
        # verify that budget_per_item * items_count <= limit
        # take a screenshot of the cart
        pass
