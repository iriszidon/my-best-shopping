from playwright.sync_api import Page
from typing import List
import allure
import os

from python_tool_shop.page_objects.tool_page import ToolPage
from python_tool_shop.page_objects.cart_page import CartPage
from python_tool_shop.page_objects.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # All locators are defined when an instance of the page is created.
        self.search_button = self.find_element("[data-test='search-submit'], button.btn.btn-secondary:has-text('Search')")
        self.home_page_button = self.find_element("[data-test='nav-home'], a.nav-link.active, [aria-current='page']")
        self.navigation_bar = self.find_element("#navbarSupportedContent")
        self.search_text_box = self.find_element("#search-query, [data-test='search-query'], [placeholder=Search]")
        self.top_bar = self.page.get_by_text("Practice Black Box Testing & Bug Hunting")
        self.home_page_button_ness = self.find_element("[data-test='nav-home'], a.nav-link.active, [aria-current='page']")
        self.contact_button_ness = self.find_element("[data-test='xxx'], [data-test='nav-contact'],[routerlink='/contact']")

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
        return item_list

    @allure.step("add items to cart")
    def add_items_to_cart(self, urls: List[str]) -> None:
        for url in urls:
            tool_page = self.open_tool_page(url)
            tool_page.add_item_to_cart(url)


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
    def open_cart_page(self) -> CartPage:
        # This element does not appear when the page is initialized.
        self.open_cart_button = self.find_element('[data-icon=\'cart-shopping\'], [data-test=\'cart-quantity\'] ]')
        self.click_element(self.open_cart_button)
        cart_page = CartPage(self.page)
        return cart_page

    @allure.step("Open tool page")
    def open_tool_page(self, url) -> ToolPage:
        self.navigate_to(url)
        tool_page = ToolPage(self.page)
        return tool_page