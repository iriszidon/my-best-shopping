import logging
from asyncio import timeout
from concurrent.interpreters import create

from playwright.sync_api import Page, Locator, expect
from typing import List
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

    def get_winner_locator(self, locator_list :List[str]) -> str:
        index = 0
        for locator in locator_list:
            index +=1
            try:
                is_element_visible = self.page.locator(locator).is_visible()
                if is_element_visible:
                    log_message(self.logger, f"Attempt #{index} with Locator: {locator} succeeded ;)")
                    return locator
                else:
                    log_message(self.logger, f"Attempt #{index} with Locator: {locator} failed ;(")
            except Exception as e:
                take_screenshot(self.page, locator)
                log_message(self.logger, f"The element was not found")

    def split_selectors(self, selector_string: str) -> List[str]:
        # Split by comma and strip whitespace around each part
        return [part.strip() for part in selector_string.split(",")]

    def find_element(self, loc_str:str) -> Locator:
        loc_list = self.split_selectors(loc_str)
        winner_loc_str = self.get_winner_locator(loc_list)
        return self.page.locator(winner_loc_str)


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
