from playwright.sync_api import Page
from typing import List
import allure
import os

from python_tool_shop.page_objects.cart_page import CartPage
from python_tool_shop.helper.utils import take_screenshot
from python_tool_shop.page_objects.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.search_button = self.page.locator("[data-test='search-submit'], button.btn.btn-secondary:has-text('Search')")
        self.add_to_cart_button = self.page.locator("#btn-add-to-cart, [data-test='add-to-cart'], button.btn-success.btn")
        self.home_page_button = self.page.locator("[data-test='nav-home'], a.nav-link.active, [aria-current='page']")
        self.toast_message = self.page.locator(".toast-message")
        self.navigation_bar = self.page.locator("#navbarSupportedContent")
        self.search_text_box = self.page.locator("#search-query, [data-test='search-query'], [placeholder=Search]")
        self.open_cart_button = self.navigation_bar.locator("#lblCartCount")
        self.top_bar = self.page.get_by_text("Practice Black Box Testing & Bug Hunting")

    def login(self):
        pass

    @allure.step("search items by name under price")
    def search_items_by_name_under_price(
        self, query: str, max_price: int, limit=5
    ) -> List[str]:
        # search by a query
        self.type_text(self.search_text_box, query)
        self.click_element(self.search_button)
        # use min/max filter if exists
        # wait for text Searched for: hammer
        self.wait_to_see_in_page('[data-test="search-term"]')
        self.set_slider(max_price)
        # get  first 5 (limit) items that have a price <= max_price
        item_list = self.get_items_url_list(limit)
        # in case of less than 5 items exist:
        # if there is a next button, click next and get items from next page
        # if no paging, get less than 5 items
        # return a url array of 5 items that meet the condition, or less.
        # example urls = search_items_by_name_under_price("hammer", 220, 5)
        return item_list

    @allure.step("add items to cart")
    def add_items_to_cart(self, urls: List[str]) -> None:
        # foreach url go to url
        for url in urls:  # upper bound to avoid runaway
            self.navigate_to(url)
            # take screenshot foreach selected item
            take_screenshot(self.page, name=url[-27:])
            # click add to cart
            self.click_element(self.add_to_cart_button)
            # wait for text product added to shopping cart
            self.wait_for_selector_to_appear(self.toast_message)
            # go back to search page
            self.click_element(self.home_page_button)


    @allure.step("set the slider to narrow the price range")
    def set_slider(self, target) -> None:
        slider = self.page.locator(".ngx-slider-span.ngx-slider-pointer.ngx-slider-pointer-max")
        cur_val = 100
        # Focus and nudge with ArrowRight until we reach/approach the target
        slider.focus()
        # Sometimes sliders change by step=1; guard against infinite loops
        for _ in range(cur_val):  # upper bound to avoid runaway
            cur = int(slider.get_attribute("aria-valuenow"))
            if cur >= target:
                break
            slider.press("ArrowLeft")

    @allure.step("Add items to the wish list")
    def get_items_url_list(self, limit: int) -> List[str]:
        url_list = []
        base_url = os.environ.get("BASE_URL")
        # Find all <a> elements with class "card" and an href attribute
        elements = self.page.locator("a.card[href]")
        # Get all href values
        href_list = elements.evaluate_all("els => els.map(e => e.getAttribute('href'))")[:limit]
        prefixed_href_list = [f"{base_url}{item}" for item in href_list]
        self.logger.info(prefixed_href_list)
        return prefixed_href_list

    @allure.step("Open shopping cart")
    def open_cart_page(self, setup_playwright) -> CartPage:
        self.click_element(self.open_cart_button)
        cart_page = CartPage(setup_playwright)
        return cart_page