import allure
import pytest
import os

from helper.utils import take_screenshot
from page_objects.main_page import MainPage
from page_objects.base_page import BasePage


@allure.description("Test for tool shop website")
@pytest.mark.ness_task
@pytest.mark.parametrize(
    "tool_name, max_price, limit", [("hammer", 20, 5), ("pliers", 19, 2)]
)
def test_end_to_end_search_filter_add_sum(
    tool_name, max_price, limit, setup_playwright
):
    base_page = navigate_to_page(setup_playwright)
    main_page = MainPage(base_page.page)
    items_urls = main_page.search_items_by_name_under_price(tool_name, max_price, limit)
    main_page.add_items_to_cart(items_urls)
    cart_page = main_page.open_cart_page()
    total_price = cart_page.get_total_price()
    cart_page.assert_cart_total_not_exceeds(
        limit * max_price, len(items_urls), total_price
    )


@allure.description("Click on 2 elements in the main page")
@pytest.mark.good_test
def test_print_locator(setup_playwright) -> None:
    base_page = navigate_to_page(setup_playwright)
    main_page = MainPage(base_page.page)
    main_page.click_element(main_page.contact_button)
    take_screenshot(main_page, "some_screen_shot")
    main_page.click_element(main_page.home_page_button)


@allure.description("Click again on 2 elements in the main page")
@pytest.mark.good_test
def test_dummy_test_for_parallel_run(setup_playwright) -> None:
    base_page = navigate_to_page(setup_playwright)
    main_page = MainPage(base_page.page)
    main_page.click_element(main_page.contact_button)
    take_screenshot(main_page, "some_screen_shot")
    main_page.click_element(main_page.home_page_button)


def navigate_to_page(setup_playwright) -> BasePage:
    base_page = BasePage(setup_playwright)
    base_url = os.environ.get("BASE_URL")
    base_page.navigate_to(base_url)
    return base_page
