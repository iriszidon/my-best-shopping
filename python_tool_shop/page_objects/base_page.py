import logging
from asyncio import timeout

from playwright.sync_api import Page, Locator

from python_tool_shop.helper.utils import LogLevel

from python_tool_shop.helper.utils import take_screenshot, log_message


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def safe_execute(self, action, action_name: str, *args):
        try:
            log_message(
                self.logger,
                f"Execution action: {action_name} with arguments {args}",
                LogLevel.INFO,
            )
            action(*args)
        except Exception as e:
            log_message(
                self.logger,
                f"action failed {action_name} with arguments {args}",
                LogLevel.ERROR,
            )
            take_screenshot(self.page, action_name)
            raise

    def click_element(self, locator: Locator):
        self.safe_execute(locator.click, "click_element")

    def type_text(self, locator: Locator, text: str):
        self.safe_execute(locator.fill, "type_text", text)

    def navigate_to(self, url: str):
        self.safe_execute(self.page.goto, "navigate_to", url)

    def wait_for_selector_to_appear(self, locator: Locator):
        self.safe_execute(locator.wait_for, "wait_for_selector")

    def wait_to_see_in_page(self, selector: str):
        self.safe_execute(self.page.wait_for_selector, "navigate_to", selector)
