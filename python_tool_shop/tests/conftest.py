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
