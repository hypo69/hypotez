# # \file src/webdriver/firefox/firefox.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""WebDriver Firefox Module.

This module provides the `Firefox` class, extending the standard
`selenium.webdriver.Firefox` with functionalities like custom profile
management, kiosk mode, proxy settings, and enhanced cookie handling.

 ```rst
 .. module:: src.webdriver.firefox.firefox
 ```

Example:
    ```python
    # This example assumes the necessary configuration files (e.g., firefox.json)
    # and geckodriver are correctly set up in the project.
    # Ensure 'src' is in PYTHONPATH or the script is run from the project root.

    # import sys # For sys.path modifications if needed
    # from pathlib import Path # For path operations
    # # Assuming header.py and gs are set up if running standalone for __root__
    # # from src.utils.path import set_project_root # Example if header.py needs manual setup
    # # __root__ = set_project_root()
    # # sys.path.insert(0, str(__root__))
    # # from src import gs # Initialize GlobalSettings

    # from src.webdriver.firefox.firefox import Firefox # Actual import if used as a library
    # from src.logger.logger import logger # For logging


    # if __name__ == '__main__':
    # ff_driver = None
    # try:
    # logger.info('Attempting to start Firefox WebDriver for example.')
    # ff_driver = Firefox(
    # # profile_name='custom_profile', # Optional: specify a profile
    # window_mode='headless'          # Example: run in headless mode
    # None
    # logger.info('Firefox WebDriver started. Navigating to a site.')
    # ff_driver.get('https://www.whatismybrowser.com/detect/what-is-my-user-agent')
    # logger.info(f'Successfully navigated to: {ff_driver.current_url}')
    # # Example: Get page source or an element
    # # page_source_sample = ff_driver.page_source[:200]
    # # logger.info(f'Page source sample: {page_source_sample}...')
    # # input('Press Enter to close the browser...') # For non-headless observation
    # except Exception as e:
    # logger.error(f'An error occurred during the Firefox example: {e}', exc_info=True)
    # finally:
    # if ff_driver:
    # logger.info('Quitting Firefox WebDriver.')
    # ff_driver.quit()
    # logger.info('Firefox example finished.')
    ```"""

import os
import sys
import random
from pathlib import Path
from typing import Any
from types import SimpleNamespace

from selenium.webdriver import Firefox as WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import WebDriverException

from fake_useragent import UserAgent # type: ignore
from tenacity import retry, stop_after_attempt, stop_after_delay

import header
from header import __root__
from src import gs
from src.webdriver.executor import ExecuteLocator
from src.webdriver.js import JavaScript
from src.webdriver.proxy import get_proxies_dict, check_proxy
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger # I import a logger


class Config:
    """Configuration class for Firefox WebDriver.

    This class loads WebDriver configuration settings from a JSON file
    and provides them as attributes."""
    _config: SimpleNamespace | dict  # Object of configuration loaded from json
    geckodriver_path: str           # The path to the executable Geckodriver file
    firefox_binary_path: str        # The path to the executable Firefox file
    profile_directory_default: str  # Type of the default profile directory ('os' or 'Internet')
    profile_directory_os: str       # Way to the Directory of the OS profile
    profile_directory_internal: str # The path to the internal directory of the profile (relative to SRC)
    options: list[str]              # List of command line options for Firefox
    headers: dict[str, Any]         # Preferences dictionary for Firefox
    proxy_enabled: bool             # Flag indicating whether the use of proxies is included
    enable_geckodriver_log: bool

    
    def __init__(self, config_path: Path):
        """Initializes The Config Object by Loading Settings from a Json File.

        Args:
            Config_path (Path): The Way to the Json File of the Configuration."""
        # The function extracts a json file configuration.
        self._config = j_loads_ns(config_path)

        # Check, if the configuration is successfully loaded
        if not self._config or not isinstance(self._config, (SimpleNamespace, dict)):
            logger.error(f'Не удалось загрузить или некорректный формат конфигурации Firefox из: {config_path}')
            # Installation of safe default values to prevent Attributeerror
            self.geckodriver_path = ''
            self.firefox_binary_path = ''
            self.profile_directory_default = 'os'
            self.profile_directory_os = ''
            self.profile_directory_internal = ''
            self.options = []
            self.headers = {}
            self.proxy_enabled = False
            self.enable_geckodriver_log = False
            return

        # Safe extraction of invested attributes
        _executable_path_config: SimpleNamespace | dict = getattr(self._config, 'executable_path', SimpleNamespace())
        _profile_directory_config: SimpleNamespace | dict = getattr(self._config, 'profile_directory', SimpleNamespace())

        self.geckodriver_path = str(Path(gs.path.root, getattr(_executable_path_config, 'geckodriver', '')))
        self.firefox_binary_path = str(Path(gs.path.root, getattr(_executable_path_config, 'firefox_binary', '')))
        self.profile_directory_default = getattr(_profile_directory_config, 'default', 'os')
        self.profile_directory_os = getattr(_profile_directory_config, 'os', '')
        self.profile_directory_internal = getattr(_profile_directory_config, 'internal', '')
        self.options = getattr(self._config, 'options', [])
        _headers_config: SimpleNamespace | dict = getattr(self._config, 'headers', SimpleNamespace())
        self.headers = vars(_headers_config) if isinstance(_headers_config, SimpleNamespace) else (_headers_config if isinstance(_headers_config, dict) else {})
        self.proxy_enabled = bool(getattr(self._config, 'proxy_enabled', False))
        self.enable_geckodriver_log = bool(getattr(self._config, 'enable_geckodriver_log', False))


class Firefox(WebDriver):
    """Extends `selenium.webdriver.Firefox` with enhanced capabilities."""

    driver_name: str = 'firefox'

    @retry(stop=(stop_after_delay(10) | stop_after_attempt(2)))
    def __init__(
        self,
        profile_name: str | None = None,
        geckodriver_version: str | None = None,
        firefox_version: str | None = None,
        user_agent: str | None = None,
        proxy_file_path: str | None = None,
        options: list[str] | None = None,
        window_mode: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Announcement of variables at the beginning of the function
        config_obj: Config
        service: Service
        options_obj: Options
        effective_user_agent: str
        profile_dir_path_base: Path
        profile_dir_path: Path
        gecko_log_path: str | None

        logger.info('Инициализация Firefox WebDriver')
        logger.debug(f"Текущий __root__: {str(__root__)}") # Diagnostics __root__

        config_obj = Config(Path(gs.path.src, 'webdriver', 'firefox', 'firefox.json'))
        logger.debug(f"Конфигурация загружена. enable_geckodriver_log: {config_obj.enable_geckodriver_log}") # Diagnosis of the flag

        if not config_obj.geckodriver_path or not Path(config_obj.geckodriver_path).is_file():
            logger.critical(
                f'Критическая ошибка: geckodriver_path ({config_obj.geckodriver_path}) не установлен, некорректен или не является файлом.',
                None, False
            )
            sys.exit(1)

        gecko_log_path = None
        if config_obj.enable_geckodriver_log:
            logger.info("Попытка настроить логирование geckodriver...")
            log_file_path_obj = Path(__root__, 'geckodriver.log')
            logger.debug(f"Предполагаемый путь к лог-файлу geckodriver: {str(log_file_path_obj)}")
            try:
                log_file_path_obj.parent.mkdir(parents=True, exist_ok=True)
                # Trying to create/open a file for checking your entry rights
                with open(log_file_path_obj, 'a', encoding='utf-8') as f_log_test:
                    f_log_test.write(f"--- Log test write at {Path.cwd()} ---\n") # Record something for verification
                
                gecko_log_path = str(log_file_path_obj)
                logger.info(f'Логирование geckodriver настроено. Путь к лог-файлу: {gecko_log_path}')
            except OSError as ex_os:
                logger.warning(f'Не удалось создать/записать лог-файл geckodriver по пути {log_file_path_obj}. Ошибка OSError: {ex_os}')
                gecko_log_path = None
            except Exception as ex_general: # We catch other possible errors
                logger.warning(f'Общая ошибка при тестовой записи в лог-файл geckodriver по пути {log_file_path_obj}. Ошибка: {ex_general}')
                gecko_log_path = None

        service = Service(executable_path=config_obj.geckodriver_path, log_path=gecko_log_path)
        options_obj = Options()

        # if config_obj.firefox_binary_path:
        # if Path(config_obj.firefox_binary_path).is_file():
        # options_obj.binary_location = config_obj.firefox_binary_path
        # else:
        # logger.warning(
        # The f'amant path to the Firefox binary file (Firefox_binary_path) does not exist or is not a file: {config_obj.firefox_binary_path}. '
        # 'System Firefox will be used.'
        # None
        # else:
        # Logger.info ('Way to the Firefox binary file (Firefox_binary_path) is not specified. System Firefox will be used.')

        options_obj.set_preference('network.cookie.cookieBehavior', 0)
        options_obj.set_preference('dom.storage.enabled', True)
        options_obj.set_preference('privacy.trackingprotection.enabled', False)
        options_obj.set_preference('privacy.trackingprotection.socialtracking.enabled', False)

        # if config_obj.options:
        # for option_val in config_obj.options:
        # options_obj.add_argument(option_val)

        if window_mode:
            options_obj.add_argument(f'--{window_mode}')

        if options:
            for option_val in options:
                options_obj.add_argument(option_val)

        if config_obj.headers:
            for key, value in config_obj.headers.items():
                try:
                    if isinstance(value, (bool, int, str)):
                        options_obj.set_preference(key, value)
                    else:
                        logger.warning(f'Значение для preference "{key}" имеет неподдерживаемый тип: {type(value)}. Пропускается.')
                except Exception as ex_pref: 
                    logger.warning(f'Не удалось установить preference "{key}" со значением "{value}": {ex_pref}')

        options_obj.set_preference('general.useragent.override', user_agent if user_agent else UserAgent().random)


        if config_obj.proxy_enabled:
            self.set_proxy(options_obj)

        # if config_obj.profile_directory_default == 'os' and config_obj.profile_directory_os:
        # profile_dir_path_base = Path(config_obj.profile_directory_os)
        # elif config_obj.profile_directory_internal:
        # profile_dir_path_base = Path(gs.path.src, config_obj.profile_directory_internal)
        # else:
        # Logger.info ('The Basic Directory of the Profile is not indicated, the temporary profile selenium will be used.')
        # profile_dir_path_base = Path('')

        # profile_dir_path = profile_dir_path_base
        # if profile_name:
        # if profile_dir_path_base and str(profile_dir_path_base) != '.':
        # profile_dir_path = profile_dir_path_base / profile_name
        # else:
        # logger.warning(
        # The profile "{Profile_name}" is indicated, but the base directory of the profile is not determined or is the current directory. '
        # 'Selenium, most likely, will create a temporary profile, ignoring the name.'
        # None
        # profile_dir_path = Path('')

        # if profile_dir_path and '%LOCALAPPDATA%' in str(profile_dir_path):
        # local_app_data: str | None = os.environ.get('LOCALAPPDATA')
        # if local_app_data:
        # profile_dir_path = Path(str(profile_dir_path).replace('%LOCALAPPDATA%', local_app_data))
        # else:
        # Logger.warning ('% Localappdata% is not found in the environment variables, the path to the profile may be incorrect.')

        # if profile_dir_path and str(profile_dir_path) != '.':
        # resolved_profile_path = profile_dir_path.resolve()
        # # Check if there is a profile directory if it is not temporary and must exist
        # if not resolved_profile_path.exists () and protoname: # If we indicate a specific profile, it must exist or be created Firefox
        # Logger.info (f'directory of profile {resolved_profile_path} does not exist. Firefox will try to create or use temporary. ')
        # elif resolved_profile_path.exists() and not resolved_profile_path.is_dir():
        # Logger.warning (F'ITH WIGHT TO THE Profile {Resolved_Profile_PATH} exists, but not a directory. A temporary profile will be used. ')
        # Profile_dir_path = Path ('') # Reset so as not to transmit an incorrect path

        # if profile_dir_path and str (Profile_dir_path)! = '.'. ': # Repeated check after possible discharge
        # options_obj.add_argument('-profile')
        # options_obj.add_argument(str(resolved_profile_path))
        # Logger.info (F'SOSPOLEDENT TO PROFILE: {str (resolved_profile_path)} ')
        # Elif Profile_name and Not (Profile_dir_path and Str (Profile_dir_path)! = '.'): # If the profile name was, but the path did not form
        # Logger.info (F'mi of the profile "{Profile_name}" was indicated, but the final path to the profile is not defined or incorrect. A temporary profile will be used. ')

        try:
            # super().__init__(service=service, options=options_obj, *args, **kwargs)
            super().__init__(service=service, options=options_obj,  *args, **kwargs)
            self._payload()
            logger.success(f'Браузер Firefox успешно запущен. Режим окна: {window_mode if window_mode else "по умолчанию"}.')
        except WebDriverException as ex_wd:
            error_message = (
                '\n'
                '---------------------------------\n'
                '    Ошибка запуска WebDriver (Firefox)\n'
                '    Возможные причины:\n'
                '    - Firefox не установлен или путь к нему некорректен.\n'
                '    - Версия geckodriver несовместима с версией Firefox.\n'
                '    - geckodriver не найден или путь к нему некорректен.\n'
                '    - Проблемы с указанным профилем Firefox (если используется).\n'
                '    - Антивирус или firewall блокирует geckodriver или Firefox.\n'
                '    - Недостаточно системных ресурсов.\n'
                '\n'
                '    Рекомендации:\n'
                '    - Убедитесь, что Firefox установлен и доступен.\n'
                '    - Проверьте совместимость версий Firefox и geckodriver (см. https://github.com/mozilla/geckodriver/releases).\n'
                '    - Проверьте путь к geckodriver в конфигурации (firefox.json).\n'
                '    - Попробуйте запустить без указания профиля (с временным профилем).\n'
                '    - Проверьте логи geckodriver (geckodriver.log в корне проекта, если включено).\n'
                '----------------------------------'
            )
            logger.critical(error_message, ex_wd, True)
            raise
        except Exception as ex_init:
            logger.critical('Непредвиденная ошибка при инициализации Firefox WebDriver:', ex_init, True)
            raise


    def set_proxy(self, options: Options) -> None:
        proxies_config: dict[str, list[dict[str, Any]]]
        all_proxies_list: list[dict[str, Any]]
        selected_proxy_details: dict[str, Any] | None = None

        proxies_config = get_proxies_dict()

        all_proxies_list = []
        if proxies_config:
            all_proxies_list.extend(proxies_config.get('http', []))
            all_proxies_list.extend(proxies_config.get('socks4', []))
            all_proxies_list.extend(proxies_config.get('socks5', []))

        if not all_proxies_list:
            logger.warning('Список доступных прокси пуст. Прокси не будет использован.')
            return

        random.shuffle(all_proxies_list)

        for proxy_info in all_proxies_list:
            if check_proxy(proxy_info):
                selected_proxy_details = proxy_info
                break

        if selected_proxy_details:
            host: str = str(selected_proxy_details.get('host', ''))
            port_str: str = str(selected_proxy_details.get('port', ''))
            protocol: str = str(selected_proxy_details.get('protocol', 'http')).lower()

            if not host or not port_str:
                logger.warning(f'Некорректные данные для прокси: {selected_proxy_details}. Прокси не будет установлен.')
                return

            try:
                port: int = int(port_str)
            except ValueError:
                logger.warning(f'Некорректный порт для прокси: {port_str}. Прокси не будет установлен.')
                return

            options.set_preference('network.proxy.type', 1)

            if protocol == 'http':
                options.set_preference('network.proxy.http', host)
                options.set_preference('network.proxy.http_port', port)
                options.set_preference('network.proxy.ssl', host)
                options.set_preference('network.proxy.ssl_port', port)
                logger.info(f'Установка HTTP прокси: http://{host}:{port}')
            elif protocol == 'socks4':
                options.set_preference('network.proxy.socks', host)
                options.set_preference('network.proxy.socks_port', port)
                options.set_preference('network.proxy.socks_version', 4)
                logger.info(f'Установка SOCKS4 прокси: {host}:{port}')
            elif protocol == 'socks5':
                options.set_preference('network.proxy.socks', host)
                options.set_preference('network.proxy.socks_port', port)
                options.set_preference('network.proxy.socks_version', 5)
                logger.info(f'Установка SOCKS5 прокси: {host}:{port}')
            else:
                logger.warning(f'Неизвестный тип прокси: {protocol}. Прокси не будет установлен.')
                options.set_preference('network.proxy.type', 0)
        else:
            logger.warning('Рабочий прокси не найден из предоставленного списка. Прокси не будет использован.')


    def _payload(self) -> None:
        js_executor: JavaScript = JavaScript(self)
        self.get_page_lang = js_executor.get_page_lang
        self.ready_state = js_executor.ready_state
        self.get_referrer = js_executor.get_referrer
        self.unhide_DOM_element = js_executor.unhide_DOM_element
        self.window_focus = js_executor.window_focus

        locator_executor: ExecuteLocator = ExecuteLocator(self)
        self.execute_locator = locator_executor.execute_locator
        self.get_webelement_as_screenshot = locator_executor.get_webelement_as_screenshot
        self.get_webelement_by_locator = locator_executor.get_webelement_by_locator
        self.get_attribute_by_locator = locator_executor.get_attribute_by_locator
        self.send_message = locator_executor.send_message
        self.send_key_to_webelement = locator_executor.send_message


if __name__ == '__main__':
    driver_instance: Firefox | None = None
    try:
        logger.info('Запуск примера Firefox WebDriver из __main__...')
        driver_instance = Firefox()
        driver_instance.get('https://www.google.com')
        logger.info(f'Текущий URL: {driver_instance.current_url}')
        # Input ('Browser is launched. Click Enter to complete ...')
    except Exception as ex_main:
        logger.error('Ошибка в процессе выполнения примера __main__', ex_main, exc_info=True)
    finally:
        if driver_instance:
            logger.info('Закрытие Firefox WebDriver из __main__.')
            driver_instance.quit()
        logger.info('Выполнение примера __main__ завершено.')
