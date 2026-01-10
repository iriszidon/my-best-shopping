from enum import Enum

import allure

class LogLevel(Enum):
    INFO = "info"
    DEBUG = "debug"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

def log_message(logger, message: str, level: LogLevel = LogLevel.INFO, attach_to_allure: bool = True):

    if level == LogLevel.INFO:
        logger.info(message)
    elif level == LogLevel.DEBUG:
        logger.debug(message)
    elif level == LogLevel.WARNING:
        logger.warning(message)
    elif level == LogLevel.ERROR:
        logger.error(message)
    elif level == LogLevel.CRITICAL:
        logger.critical(message)


    if attach_to_allure:
        allure.attach(
            message,
            name=f"(Log ({level.value.upper()}",
            attachment_type = allure.attachment_type.TEXT
        )

def take_screenshot(page, name: str = "screenshot"):
    try:
        screenshot_data = page.page.screenshot(type="png")
        allure.attach(
            screenshot_data,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        return screenshot_data
    except Exception:
        return None

