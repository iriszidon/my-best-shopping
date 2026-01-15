import allure
import pytest
import os
from page_objects.main_page import MainPage
from page_objects.base_page import BasePage


@allure.description("Test for tool shop website")
@pytest.mark.good_experimental_test
@pytest.mark.parametrize(
    "tool_name, max_price, limit", [("hammer", 20, 5), ("pliers", 19, 2)]
)
def test_end_to_end_search_filter_add_sum(tool_name, max_price, limit, setup_playwright):
    # search a product, filter by price, add to cart
    base_url = os.environ.get("BASE_URL")
    base_page = BasePage(setup_playwright)
    base_page.navigate_to(base_url)
    main_page = MainPage(setup_playwright)
    items_urls = main_page.search_items_by_name_under_price(tool_name, max_price, limit)
    main_page.add_items_to_cart(items_urls)
    cart_page = main_page.open_cart_page()
    total_price = cart_page.get_total_price()
    cart_page.assert_cart_total_not_exceeds(limit * max_price, len(items_urls), total_price)


def test_print_locator(setup_playwright) -> None:
    base_page = BasePage(setup_playwright)
    base_url = os.environ.get("BASE_URL")
    base_page.navigate_to(base_url)
    main_page = MainPage(setup_playwright)
    main_page.click_element(main_page.contact_button_ness)
    main_page.click_element(main_page.home_page_button_ness)

