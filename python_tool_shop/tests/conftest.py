from datetime import datetime
from typing import Any, List, Optional
import os
from urllib.parse import urlencode

import pytest
from python_tool_shop.helper.utils import log_message, LogLevel

DEFAULT_BROWSER_NAME = os.environ.get("BROWSER_NAME", "auto").strip().lower()

def pytest_addoption(parser):
    parser.addoption(
        "--moon-url",
        action="store",
        default=os.getenv("MOON_URL", ""),  # e.g. http://moon.aerokube.local
        help="Base URL of Aerokube Moon. If empty, tests run locally.",
    )
    parser.addoption(
        "--browser-name",
        action="store",
        default=DEFAULT_BROWSER_NAME,
        help="chromium | firefox | webkit | auto (default: env BROWSER_NAME or 'auto').",
    )

@pytest.fixture()
def setup_playwright(playwright, request):
    """
    Yields a Playwright Page:
      - If --moon-url is set: connect to Moon over WS (engine chosen automatically or forced).
      - Otherwise: launch local browser.
    """
    headed = request.config.getoption("--headed", default=False)
    moon_url: str = request.config.getoption("--moon-url")
    browser_name: str = request.config.getoption("--browser-name")

    browser = get_browser(playwright, headed=headed, moon_url=moon_url, browser_name=browser_name)
    page = browser.new_page()
    try:
        yield page
    finally:
        # keep your logging
        try:
            log_message(None, "closing browser", LogLevel.INFO)
        except Exception:
            pass
        browser.close()

def _normalize(engine: str) -> str:
    e = engine.strip().lower()
    if e in ("chrome", "chromium"):
        return "chromium"
    if e in ("ff", "firefox"):
        return "firefox"
    if e in ("webkit", "safari"):
        return "webkit"
    raise ValueError("Browser name must be one of: chromium (chrome), firefox, webkit, or 'auto'.")

def _engine_order(browser_name: str) -> List[str]:
    # If user forced a browser, use only that engine; otherwise pick an order and try.
    if browser_name and browser_name != "auto":
        return [_normalize(browser_name)]
    # Default attempt order; tweak if you prefer randomization:
    # order = ["firefox", "chromium", "webkit"]
    order = ["firefox", "chromium", "webkit"]
    # Optional: uncomment to randomize the first pick
    # random.shuffle(order)
    return order

def _connect_ws(playwright, engine: str, endpoint: str, slow_mo: int):
    if engine == "chromium":
        return playwright.chromium.connect(ws_endpoint=endpoint, slow_mo=slow_mo)
    elif engine == "firefox":
        return playwright.firefox.connect(ws_endpoint=endpoint, slow_mo=slow_mo)
    elif engine == "webkit":
        return playwright.webkit.connect(ws_endpoint=endpoint, slow_mo=slow_mo)
    else:
        raise ValueError("Unsupported engine: " + engine)

def get_browser(playwright, headed: bool, moon_url: str, browser_name: str) -> Any:
    slow_mo = 750

    # If Moon is configured -> connect() to Playwright WS endpoint:
    #   {moon}/playwright/{engine}?<params>
    # Headed runs ask Moon for a visible session (VNC).
    if moon_url:
        params = {}
        if headed:
            params["headless"] = "false"
            params["enableVNC"] = "true"

        qs = f"?{urlencode(params)}" if params else ""
        engines = _engine_order(browser_name)

        last_exc: Optional[Exception] = None
        for eng in engines:
            endpoint = f"{moon_url.rstrip('/')}/playwright/{eng}{qs}"
            try:
                return _connect_ws(playwright, eng, endpoint, slow_mo=slow_mo)
            except Exception as e:
                last_exc = e
                # Try next engine
        # If all engines failed, bubble up the last error
        raise last_exc if last_exc else RuntimeError("Failed to connect to Moon Playwright endpoint.")

    # Else: run locally
    launch_opts = {"headless": not headed, "slow_mo": slow_mo}
    eng = _engine_order(browser_name)[0]  # either forced engine or default first
    if eng == "chromium":
        return playwright.chromium.launch(**launch_opts)
    elif eng == "firefox":
        return playwright.firefox.launch(**launch_opts)
    elif eng == "webkit":
        return playwright.webkit.launch(**launch_opts)
    else:
        raise ValueError("Browser name must be 'chromium', 'firefox', 'webkit', or 'auto'.")


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