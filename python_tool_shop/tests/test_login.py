import allure
import pytest
from playwright.sync_api import expect
from pytest_playwright.pytest_playwright import playwright
import os
from conftest import setup_main_page
from page_objects.main_page import MainPage
from python_tool_shop.helper.config import VALID_CREDENTIALS


@allure.description("Test for tool shop website")
@pytest.mark.good_experimental_test
@pytest.mark.parametrize(
    "tool_name, max_price, limit", [("hammer", 20, 5)]
)
def test_end_to_end_search_filter_add_sum(tool_name, max_price, limit, setup_playwright):
    # search a product, filter by price, add to cart
    main_page = MainPage(setup_playwright)
    base_url = os.environ.get("BASE_URL")
    main_page.navigate_to(base_url)
    items_urls = main_page.search_items_by_name_under_price(tool_name, max_price, limit)
    main_page.add_items_to_cart(items_urls)
    cart_page = main_page.open_cart_page(setup_playwright)
    total_price = cart_page.get_total_price()
    cart_page.assert_cart_total_not_exceeds(limit * max_price, len(items_urls), total_price)

# -----------------Experiments -------------------------------------------

@pytest.mark.skip(reason="The shopping test website disposes all users")
def test_successfully_login(setup_load_page, validation):
    login_page = setup_load_page  # open browser and load login page
    login_page.perform_login(VALID_CREDENTIALS["email"], VALID_CREDENTIALS["password"])
    validation.validate_user_logged_in()


def test_home_page_is_loaded_should_succeed(setup_load_page, validation):
    login_page = setup_load_page  # open browser and load login page
    validation.validate_home_page_is_loaded()
    assert 1 == 1


def test_home_page_is_loaded_should_succeed_v2(setup_all_pages, setup_load_page):
    login_page_new = setup_load_page  # open browser and load login page
    login_page, main_page = setup_all_pages  # open browser and load login page
    assert main_page.search_button.is_visible(), "Search button should be visible"


@pytest.mark.good_test
def test_home_page_is_loaded_should_have_top_bar(setup_main_page):
    main_page = setup_main_page
    assert main_page.top_bar.is_visible(), "top bar should be visible"


@pytest.mark.good_experimental_test
def test_home_page_is_loaded_should_have_top_bar(setup_playwright):
    main_page = MainPage(setup_playwright)
    # main_page.navigate_to("https://www.morfix.co.il/")
    main_page.navigate_to("https://practicesoftwaretesting.com/")
    assert main_page.top_bar.is_visible(), "top bar should be visible"

@allure.description("Sample for parametrized test")
@pytest.mark.parametrize(
    "username , password", [("abc", "p1"), ("bbb", "p1"), ("ccc", "p1"), ("ddd", "p1")]
)
def test_par(username, password, setup_load_page):
    login_page_new = setup_load_page  # open browser and load login page
    assert username != "ttt"
    assert password != "ttt"
