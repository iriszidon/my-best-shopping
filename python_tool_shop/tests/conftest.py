from venv import logger

import pytest

# from python_tool_shop.helper.config import URL
from python_tool_shop.helper.utils import log_message, LogLevel
from typing import Any
import os


BROWSER_MAME = os.environ.get("BROWSER_MAME")


@pytest.fixture()
def setup_playwright(playwright, request, browser_name=BROWSER_MAME):
    browser = get_browser(playwright, request, browser_name)
    page = browser.new_page()  # This will open the page
    try:
        yield page  # use yield and not return because we want to close the browser if the test fails.
    finally:
        log_message(logger, "closing browser", LogLevel.INFO)
        browser.close()


def get_browser(playwright, request, browser_name="chrome") -> Any:
    headed = request.config.getoption(
        "--headed", default=False
    )  # determine when will the UI be displayed
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=not headed, slow_mo=750)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=not headed, slow_mo=750)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=not headed, slow_mo=750)
    else:
        raise ValueError(
            "Browser name must be either 'chrome' 'webkit', or 'firefox'. Please check your BROWSER_NAME var in your .env file."
        )
    return browser


# @pytest.fixture()
# def setup_playwright(playwright, request):
#     headed = request.config.getoption(
#         "--headed", default=False
#     )  # determine when will the UI be displayed
#     browser = playwright.chromium.launch(headless=not headed, slow_mo=750)
#     page = browser.new_page()  # This will open the page
#     try:
#         yield page  # use yield and not return because we want to close the browser if the test fails.
#     finally:
#         log_message(logger, "closing browser", LogLevel.INFO)
#         browser.close()
