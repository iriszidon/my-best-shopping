from venv import logger

import pytest

from python_tool_shop.helper.config import URL
from python_tool_shop.helper.utils import log_message, LogLevel
from python_tool_shop.helper.validation import AppValidation
from python_tool_shop.page_objects.login_page import LoginPage
from python_tool_shop.page_objects.main_page import MainPage


@pytest.fixture()
def setup_playwright(playwright, request):
    headed = request.config.getoption(
        "--headed", default=False
    )  # determine when will the UI be displayed
    browser = playwright.chromium.launch(headless=not headed, slow_mo=500)
    page = browser.new_page()  # This will open the page
    try:
        yield page  # use yield and not return because we want to close the browser if the test fails.
    finally:
        log_message(logger, "closing browser", LogLevel.INFO)
        browser.close()


@pytest.fixture()
def setup_load_page(setup_playwright):
    login_page = LoginPage(setup_playwright)
    login_page.navigate_to(URL)
    log_message(logger, f"navigate to {URL}", LogLevel.INFO)
    yield login_page


@pytest.fixture()
def setup_main_page(setup_playwright):
    main_page = MainPage(setup_playwright)
    main_page.navigate_to(URL)
    log_message(logger, f"navigate to {URL}", LogLevel.INFO)
    return main_page


# Creates instances of all the pages. Add every new created page into this fixture
@pytest.fixture()
def setup_all_pages(setup_playwright):
    login_page = LoginPage(setup_playwright)
    main_page = MainPage(setup_playwright)
    yield login_page, main_page


@pytest.fixture()
def validation(setup_all_pages):
    yield AppValidation(setup_all_pages)
