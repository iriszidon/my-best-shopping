from venv import logger
import pytest
from python_tool_shop.helper.utils import log_message, LogLevel
from typing import Any
import os
from datetime import datetime

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


def _make_results_dir() -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"allure-results-{ts}"

def pytest_configure(config):
    """
    Runs in BOTH controller and workers.
    - On controller: decide the dir (if not provided) and create it.
    - On workers: read the dir from controller and apply it.
    """
    is_worker = hasattr(config, "workerinput")  # present only in xdist workers

    if not is_worker:
        # Controller (master)
        if not config.option.allure_report_dir:
            config.option.allure_report_dir = _make_results_dir()
            os.makedirs(config.option.allure_report_dir, exist_ok=True)
    else:
        # Worker: get dir from controller via workerinput
        shared = config.workerinput.get("allure_report_dir")
        if shared:
            config.option.allure_report_dir = shared

def pytest_configure_node(node):
    """
    Runs ONLY on the controller, once per worker node.
    Push the chosen allure_report_dir to every worker.
    """
    node.workerinput["allure_report_dir"] = node.config.option.allure_report_dir



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
