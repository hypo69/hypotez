"""WebDriver Firefox Module.

This module provides the `Firefox` class, extending the standard
`selenium.webdriver.Firefox` with functionalities like custom profile
management, kiosk mode, and proxy settings.

Example:
    ```python
    if __name__ == "__main__":
        browser = Firefox(
            profile_name="custom_profile",
            window_mode="kiosk"
        )
        browser.get("https://www.example.com")
        browser.quit()
    ```
"""

import os
import sys
import random
from pathlib import Path
from typing import Optional, List, Dict, Any

from selenium.webdriver import Firefox as WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import WebDriverException

from fake_useragent import UserAgent

from src import gs
from src.webdriver.executor import ExecuteLocator
from src.webdriver.js import JavaScript
from src.webdriver.proxy import get_proxies_dict, check_proxy
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger

from dataclasses import dataclass, field

@dataclass
class Config:
    """Configuration class for Firefox WebDriver."""

    def __init__(self, config_path: Path):
        """
        Initializes the Config object by loading settings from a JSON file.

        Args:
            config_path: Path to the JSON configuration file.
        """
        self._config = j_loads_ns(config_path)
        self.geckodriver_path = str(Path(gs.path.root, self._config.executable_path.geckodriver))
        self.firefox_binary_path = str(Path(gs.path.root, self._config.executable_path.firefox_binary))
        self.profile_directory_default = self._config.profile_directory.default
        self.profile_directory_os = self._config.profile_directory.os
        self.profile_directory_internal = self._config.profile_directory.internal
        self.options: List[str] = getattr(self._config, 'options', [])
        self.headers: Dict[str, Any] = vars(getattr(self._config, 'headers', {})) if hasattr(self._config, 'headers') else {}
        self.proxy_enabled: bool = getattr(self._config, 'proxy_enabled', False)

class Firefox(WebDriver):
    """
    Extends `webdriver.Firefox` with enhanced capabilities.

    Features:
        - Custom Firefox profile support.
        - Kiosk and other window modes.
        - User-agent customization.
        - Proxy settings.

    Args:
        profile_name: Name of the Firefox profile to use. Defaults to None.
        geckodriver_version: GeckoDriver version. Defaults to None.
        firefox_version: Firefox version. Defaults to None.
        user_agent: User agent string. If None, a random user agent is used. Defaults to None.
        proxy_file_path: Path to the proxy file. Defaults to None.
        options: List of Firefox options. Defaults to None.
        window_mode: Browser window mode (e.g., "windowless", "kiosk"). Defaults to None.

    Raises:
        WebDriverException: If the WebDriver fails to start.
        Exception: For other unexpected errors during initialization.
    """

    driver_name = "firefox"

    def __init__(
        self,
        profile_name: Optional[str] = None,
        geckodriver_version: Optional[str] = None,
        firefox_version: Optional[str] = None,
        user_agent: Optional[str] = None,
        proxy_file_path: Optional[str] = None,
        options: Optional[List[str]] = None,
        window_mode: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        """Initializes the Firefox WebDriver with custom settings."""
        logger.info("Starting Firefox WebDriver")

        config = Config(Path(gs.path.src, "webdriver", "firefox", "firefox.json"))

        service = Service(executable_path=config.geckodriver_path)
        options_obj = Options()

        # Load options from config file
        if config.options:
            for option in config.options:
                options_obj.add_argument(option)

        # Set window mode
        if window_mode:
            options_obj.add_argument(f"--{window_mode}")

        # Add options from constructor
        if options:
            for option in options:
                options_obj.add_argument(option)

        # Add headers from config
        if config.headers:
            for key, value in config.headers.items():
                options_obj.add_argument(f"--{key}={value}")

        # Set user agent
        user_agent = user_agent or UserAgent().random
        options_obj.set_preference("general.useragent.override", user_agent)

        # Set proxy if enabled
        if config.proxy_enabled:
            self.set_proxy(options_obj)

        # Configure profile directory
        profile_directory = (
            config.profile_directory_os
            if config.profile_directory_default == "os"
            else str(Path(gs.path.src, config.profile_directory_internal))
        )

        if profile_name:
            profile_directory = str(Path(profile_directory).parent / profile_name)
        if "%LOCALAPPDATA%" in profile_directory:
            profile_directory = Path(
                profile_directory.replace("%LOCALAPPDATA%", os.environ.get("LOCALAPPDATA"))
            )

        # profile = FirefoxProfile(profile_directory=profile_directory) #  <- @debug не грузится профиль

        try:
            super().__init__(service=service, options=options_obj)
            self._payload()
            logger.success(f"Browser started successfully, {window_mode=}")
        except WebDriverException as ex:
            logger.critical(
                """
                ---------------------------------
                    Error starting WebDriver
                    Possible reasons:
                    - Firefox update
                    - Firefox not installed

                    Перезапусти код.
                ----------------------------------
                """,
                ex,
                False
            )
            sys.exit(1)
        except Exception as ex:
            logger.critical("Firefox WebDriver error:", ex, False)

            return

    def set_proxy(self, options: Options) -> None:
        """Configures proxy settings from a dictionary.

        Args:
            options: Firefox options to add proxy settings to.
        """
        proxies_dict = get_proxies_dict()
        all_proxies = proxies_dict.get("socks4", []) + proxies_dict.get("socks5", [])

        working_proxy = None
        for proxy in random.sample(all_proxies, len(all_proxies)):
            if check_proxy(proxy):
                working_proxy = proxy
                break

        if working_proxy:
            proxy = working_proxy
            protocol = proxy["protocol"]

            if protocol == "http":
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.http", proxy["host"])
                options.set_preference("network.proxy.http_port", int(proxy["port"]))
                options.set_preference("network.proxy.ssl", proxy["host"])
                options.set_preference("network.proxy.ssl_port", int(proxy["port"]))
                logger.info(f"Setting HTTP Proxy: http://{proxy['host']}:{proxy['port']}")

            elif protocol == "socks4":
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.socks", proxy["host"])
                options.set_preference("network.proxy.socks_port", int(proxy["port"]))
                logger.info(f"Setting SOCKS4 Proxy: {proxy['host']}:{proxy['port']}")

            elif protocol == "socks5":
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.socks", proxy["host"])
                options.set_preference("network.proxy.socks_port", int(proxy["port"]))
                logger.info(f"Setting SOCKS5 Proxy: {proxy['host']}:{proxy['port']}")

            else:
                logger.warning(f"Unknown proxy type: {protocol}")
        else:
            logger.warning("No available proxies in the provided file.")

    def _payload(self) -> None:
        """Loads executors for locators and JavaScript scripts."""
        j = JavaScript(self)
        self.get_page_lang = j.get_page_lang
        self.ready_state = j.ready_state
        self.get_referrer = j.ready_state
        self.unhide_DOM_element = j.unhide_DOM_element
        self.window_focus = j.window_focus

        execute_locator = ExecuteLocator(self)
        self.execute_locator = execute_locator.execute_locator
        self.get_webelement_as_screenshot = execute_locator.get_webelement_as_screenshot
        self.get_webelement_by_locator = execute_locator.get_webelement_by_locator
        self.get_attribute_by_locator = execute_locator.get_attribute_by_locator
        self.send_message = self.send_key_to_webelement = execute_locator.send_message


if __name__ == "__main__":
    driver = Firefox()
    driver.get("https://google.com")