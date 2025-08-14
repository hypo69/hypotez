# # \file /src/webdriver/chrome/chrome.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for working with WebDriver Chrome.
===============================================
This module provides an extended class of `chrome` for Selenium Webdriver,
Including automatic settings of options, profiles, user-agent and proxy.

 `` `RST
 .. Module :: src.webdriver.chrome
    : synopsys: module for working with Webdriver Chrome
 `` `"""

import os
import random
from pathlib import Path
from typing import List

from selenium.webdriver import Chrome as WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from fake_useragent import UserAgent

import header
from header import __root__
from src import gs
from src.webdriver.executor import ExecuteLocator
from src.webdriver.js import JavaScript
from src.webdriver.proxy import get_proxies_dict, check_proxy
from src.utils.jjson import j_loads_ns # Assuming j_loads_ns is in src.utils.jjson
from src.logger.logger import logger
# from src.utils.printer import pprint as print # Not used in this file


class Chrome(WebDriver):
    """Expansion for `webdriver.chrome` with additional functionality.

    Args:
        Profile_name (str | None, Optional): Name of the user profile Chrome. By default `none`.
        Chromedriver_version (Str | None, Optional): The Chromedriver version (in the current implementation is not used, the path to Chromedriver is taken from configuration). By default `none`.
        user_agent (str | None, Optional): user agent in line format. If `none`, random is generated. By default `none`.
        Proxy_file_path (str | None, Optional): the path to the file with proxy (in the current implementation is not used, the proxies are taken through `get_Proxies_dict`). By default `none`.
        Options (List [str] | None, Optional): List of additional string options for Chrome. By default `none`.
        Window_Mode (str | None, Optional): Browser window mode (for example, 'Windowless', 'Kiosk', 'Full_window'). By default `none`.
        *Args: Additional positional arguments for `selenium.webdriver.chrome`.
        ** KWARGS: additional named arguments for `selenium.webdriver.chrome`.

    RAISES:
        WebDriverexception: If an error occurs when launching webdriver (for example, incompatibility of versions, lack of Chrome).
        Exception: with other general errors during initialization.

    Example:
        >>> Driver = chrome (Profile_name = 'My_profile', Window_Mode = 'Full_window')
        >>> Driver.get ('https://google.com')
        >>> # driver.quit ()"""
    driver_name: str = 'chrome'

    def __init__(self, profile_name: str | None = None,
                 chromedriver_version: str | None = None, # The parameter is not used
                 user_agent: str | None = None,
                 proxy_file_path: str | None = None, # The parameter is not used
                 options: list[str] | None = None,
                 window_mode: str | None = None,
                 *args, **kwargs) -> None:
        # Ads of variables used in the method
        service: Service | None = None
        options_obj: Options | None = None
        config: 'SimpleNamespace | dict' # Type hint for j_loads_ns result
        chromedriver_path: str
        profile_directory: str | Path

        # Download configuration settings for json file Chrome
        config = j_loads_ns(Path(gs.path.src / 'webdriver' / 'chrome' / 'chrome.json'))

        # Check that the configuration is loaded successfully
        if not config or not hasattr(config, 'executable_path') or not hasattr(config.executable_path, 'chromedriver'):
            logger.critical('Ошибка загрузки конфигурации Chrome или отсутствуют необходимые ключи.', None, exc_info=False)
            return # Completion of initialization in case of configuration error

        # Formation of the full path to the executable file Chromedriver
        chromedriver_path = str(Path(gs.path.root, config.executable_path.chromedriver))

        # Initialization of the Service object for managing Chromedriver
        service = Service(chromedriver_path)

        # Creating Options object to set up Chrome launch parameters
        options_obj = Options()

        # Adding options to the Options object from a loaded configuration
        if hasattr(config, 'options') and config.options:
            for option_val in config.options: # Renamed 'option' to 'option_val' to avoid conflict
                options_obj.add_argument(option_val)

        # Determination of the window mode: the value is used from the arguments of the function or from the configuration
        current_window_mode: str | None = window_mode
        if not current_window_mode and hasattr(config, 'window_mode') and config.window_mode:
            current_window_mode = config.window_mode

        # Application of the selected window mode to launch options
        if current_window_mode:
            if current_window_mode == 'kiosk':
                options_obj.add_argument('--kiosk')
            elif current_window_mode == 'windowless':
                options_obj.add_argument('--headless')
            elif current_window_mode == 'full_window':
                options_obj.add_argument('--start-maximized')

        # Adding additional options transferred as an argument to the Options object
        if options:
            for option_val in options: # Renamed 'option' to 'option_val'
                options_obj.add_argument(option_val)

        # Setting user-agent: the transmitted or random is used
        final_user_agent: str = user_agent or UserAgent().random
        options_obj.add_argument(f'--user-agent={final_user_agent}')

        # Calling the method to configure proxies, if it is indicated in the configuration
        if hasattr(config, 'proxy_enabled') and config.proxy_enabled:
            self.set_proxy(options_obj)

        # Determining and setting up the path to the Chrome user profile directory
        if hasattr(config, 'profile_directory'):
            profile_directory = config.profile_directory.os if hasattr(config.profile_directory, 'default') and config.profile_directory.default == 'os' else str(Path(gs.path.src, config.profile_directory.internal))

            if profile_name:
                profile_directory = str(Path(profile_directory).parent / profile_name)
            
            profile_directory_str: str = str(profile_directory) # Ensure it's a string for string operations
            if '%LOCALAPPDATA%' in profile_directory_str and os.environ.get('LOCALAPPDATA'):
                profile_directory = Path(profile_directory_str.replace('%LOCALAPPDATA%', os.environ.get('LOCALAPPDATA', '')))
            
            options_obj.add_argument(f'--user-data-dir={str(profile_directory)}')
        else:
            logger.warning('Конфигурация директории профиля отсутствует.')


        try:
            logger.info('Запуск Chrome WebDriver')
            super().__init__(service=service, options=options_obj, *args, **kwargs)
            self._payload()
        except WebDriverException as ex:
            logger.critical(
                """------------------------------------
                        Webdriver launch error
                        Possible reasons:
                        - CHROME update
                        - Lack of Chrome on OS
                        - incompatibility Chromedriver
                    --------------------------------------""", ex, exc_info=True)
            return  # Completion of initialization in an error
        except Exception as ex:
            logger.critical('Непредвиденная ошибка при инициализации Chrome WebDriver.', ex, exc_info=True)
            return  # Completion of initialization in an error

    def set_proxy(self, options: Options) -> None:
        """Sets up http/socks4/socks5 proxy for Webdriver from the list of available.

        Selects a random working proxy of those that returns `get_proxies_dict`
        And applies it to the object `Options`.

        Args:
            Options (Options): The Options of the Chrome options, to which the proxy settings are added."""
        # Ads of variables
        proxies_dict: dict
        all_proxies: list
        working_proxy: dict | None = None
        proxy_details: dict | None = None # Renamed 'proxy' to 'proxy_details' to avoid confusion in loops
        protocol: str | None = None

        # Dictionary extraction with available proxy servers
        proxies_dict = get_proxies_dict()
        if not proxies_dict:
            logger.warning('Словарь прокси пуст или не удалось его получить. Прокси не будет установлен.')
            return

        # Formation of a common list of proxy types of SOCKS4 and SOCKS5
        all_proxies = proxies_dict.get('socks4', []) + proxies_dict.get('socks5', []) + proxies_dict.get('http', [])

        if not all_proxies:
            logger.warning('Список доступных прокси пуст. Прокси не будет установлен.')
            return

        # Random busting of the proxy from the list to find active and checking its performance
        shuffled_proxies = random.sample(all_proxies, len(all_proxies))
        for p_details in shuffled_proxies:
            if check_proxy(p_details): # It is assumed that Check_Proxy accepts the p_details dictionary
                working_proxy = p_details
                break
        
        # If a working proxy is found, its data is used to configure
        if working_proxy:
            proxy_details = working_proxy
            protocol = proxy_details.get('protocol')
            host: str | None = proxy_details.get('host')
            port: str | int | None = proxy_details.get('port')

            if not host or not port:
                logger.warning(f'Неполные данные для прокси: {proxy_details}. Прокси не будет установлен.')
                return

            # Adding an argument to indicate a proxy server in the Chrome option, depending on the protocol
            if protocol == 'http':
                options.add_argument(f'--proxy-server=http://{host}:{port}')
                logger.info(f'Установка HTTP Proxy: http://{host}:{port}')
            elif protocol == 'socks4':
                options.add_argument(f'--proxy-server=socks4://{host}:{port}')
                logger.info(f'Установка SOCKS4 Proxy: socks4://{host}:{port}')
            elif protocol == 'socks5':
                options.add_argument(f'--proxy-server=socks5://{host}:{port}')
                logger.info(f'Установка SOCKS5 Proxy: socks5://{host}:{port}')
            else:
                logger.warning(f'Неизвестный или неподдерживаемый тип прокси: {protocol} для {host}:{port}')
        else:
            logger.warning('Рабочий прокси не найден среди доступных. Запуск без прокси.')

    def _payload(self) -> None:
        """Initializes and ties an auxiliary methods to the driver's copy.

        The function loads performers for JavaScript scripts and operations with web elements,
        Making them accessible as the methods of the object `chrome`."""
        j: JavaScript = JavaScript(self)
        self.get_page_lang = j.get_page_lang
        self.ready_state = j.ready_state
        self.get_referrer = j.get_referrer # Fixed with J.Ready_state to J.Get_referr
        self.unhide_DOM_element = j.unhide_DOM_element
        self.window_focus = j.window_focus

        execute_locator: ExecuteLocator = ExecuteLocator(self)
        self.execute_locator = execute_locator.execute_locator
        self.get_webelement_as_screenshot = execute_locator.get_webelement_as_screenshot
        self.get_webelement_by_locator = execute_locator.get_webelement_by_locator
        self.get_attribute_by_locator = execute_locator.get_attribute_by_locator
        self.send_message = self.send_key_to_webelement = execute_locator.send_message

if __name__ == '__main__':
    # Example of use:
    # For the correct work of the example, make sure that gs.path.src and gs.path.root are configured,
    # As well as the configuration file 'SRC/WebDriver/Chrome/Chrome.json' exists and is correct.
    # Chromedriver is also needed, the path to which is indicated in Chrome.json.
    try:
        driver = Chrome(window_mode='full_window')
        if hasattr(driver, 'service') and driver.service.process: # Check that the driver was successfully initialized
            driver.get(r'https://google.com')
            logger.info(f'Заголовок страницы: {driver.title}')
            # It is recommended to always close the driver after use
            # Driver.quit () # Represent to automatically close the browser
        else:
            logger.error('Не удалось инициализировать WebDriver.')
    except Exception as ex:
        logger.error(f'Ошибка в примере использования Chrome: {ex}', exc_info=True)
