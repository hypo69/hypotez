### **Анализ кода модуля `firefox.py`**

## \file /hypotez/src/webdriver/firefox/firefox.py

Модуль предоставляет класс `Firefox`, расширяющий стандартный `selenium.webdriver.Firefox` с дополнительными функциями, такими как управление профилями, киоск-режим и настройки прокси.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура классов и функций.
  - Использование `logger` для логирования.
  - Реализация настроек прокси.
  - Обработка исключений.
- **Минусы**:
  - Отсутствуют docstring для некоторых методов, таких как `_payload`.
  - Не все переменные аннотированы типами.
  - Некоторые комментарии можно улучшить, сделав их более конкретными.

**Рекомендации по улучшению:**

1.  **Документация**:
    - Добавь docstring для метода `_payload`, чтобы объяснить его назначение.
    - Укажи типы для всех входных и выходных параметров функций и методов.
    - Опиши все используемые исключения в `raises`.

2.  **Комментарии**:
    - Улучши существующие комментарии, чтобы они были более конкретными и понятными.
    - Избегай общих фраз, таких как "Loads executors". Вместо этого используй более точные выражения, например, "Initializes and assigns executor instances for handling locators and JavaScript scripts".

3.  **Обработка исключений**:
    - Добавь логирование ошибки в блоке `except Exception as e:` в методе `__init__`.

4.  **Использование `j_loads`**:
    - Убедись, что для чтения JSON используется `j_loads` или `j_loads_ns` вместо стандартного `json.load`.

5.  **Аннотации типов**:
    - Укажи аннотации типов для всех переменных, где это необходимо.
    - Убедись, что все параметры функций и методов аннотированы типами.

**Оптимизированный код:**

```python
"""
Модуль WebDriver Firefox.

Этот модуль предоставляет класс `Firefox`, расширяющий стандартный
`selenium.webdriver.Firefox` с дополнительными функциями, такими как пользовательское
управление профилями, киоск-режим и настройки прокси.

Пример:
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


class Config:
    """
    Класс конфигурации для Firefox WebDriver.
    """

    def __init__(self, config_path: Path) -> None:
        """
        Инициализирует объект Config, загружая настройки из JSON-файла.

        Args:
            config_path (Path): Путь к JSON-файлу конфигурации.
        """
        self._config = j_loads_ns(config_path)
        self.geckodriver_path: str = str(Path(gs.path.root, self._config.executable_path.geckodriver))
        self.firefox_binary_path: str = str(Path(gs.path.root, self._config.executable_path.firefox_binary))
        self.profile_directory_default: str = self._config.profile_directory.default
        self.profile_directory_os: str = self._config.profile_directory.os
        self.profile_directory_internal: str = self._config.profile_directory.internal
        self.options: List[str] = getattr(self._config, 'options', [])
        self.headers: Dict[str, Any] = vars(getattr(self._config, 'headers', {})) if hasattr(self._config, 'headers') else {}
        self.proxy_enabled: bool = getattr(self._config, 'proxy_enabled', False)


class Firefox(WebDriver):
    """
    Расширяет `webdriver.Firefox` с улучшенными возможностями.

    Функции:
        - Поддержка пользовательских профилей Firefox.
        - Киоск и другие режимы окна.
        - Настройка User-Agent.
        - Настройки прокси.

    Args:
        profile_name (Optional[str], optional): Имя используемого профиля Firefox. По умолчанию None.
        geckodriver_version (Optional[str], optional): Версия GeckoDriver. По умолчанию None.
        firefox_version (Optional[str], optional): Версия Firefox. По умолчанию None.
        user_agent (Optional[str], optional): Строка User-Agent. Если None, используется случайный User-Agent. По умолчанию None.
        proxy_file_path (Optional[str], optional): Путь к файлу прокси. По умолчанию None.
        options (Optional[List[str]], optional): Список опций Firefox. По умолчанию None.
        window_mode (Optional[str], optional): Режим окна браузера (например, "windowless", "kiosk"). По умолчанию None.

    Raises:
        WebDriverException: Если не удалось запустить WebDriver.
        Exception: Для других неожиданных ошибок во время инициализации.
    """

    driver_name: str = "firefox"

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
        """Инициализирует Firefox WebDriver с пользовательскими настройками."""
        logger.info('Starting Firefox WebDriver')  # Логируем запуск Firefox WebDriver

        config: Config = Config(Path(gs.path.src, "webdriver", "firefox", "firefox.json")) # загружаем конфиг

        service: Service = Service(executable_path=config.geckodriver_path) # Указываем путь к geckodriver
        options_obj: Options = Options() # Создаем объект Options

        # Загрузка опций из файла конфигурации
        if config.options:
            for option in config.options:
                options_obj.add_argument(option)

        # Установка режима окна
        if window_mode:
            options_obj.add_argument(f'--{window_mode}')  # Добавляем аргумент для режима окна

        # Добавление опций из конструктора
        if options:
            for option in options:
                options_obj.add_argument(option)

        # Добавление заголовков из конфигурации
        if config.headers:
            for key, value in config.headers.items():
                options_obj.add_argument(f'--{key}={value}')  # Добавляем аргументы для заголовков

        # Установка user agent
        user_agent = user_agent or UserAgent().random # Получаем случайный user agent, если не указан
        options_obj.set_preference('general.useragent.override', user_agent)  # Устанавливаем user agent

        # Установка прокси, если включен
        if config.proxy_enabled:
            self.set_proxy(options_obj)

        # Настройка директории профиля
        profile_directory: str = (
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
            super().__init__(service=service, options=options_obj) # Инициализируем WebDriver с настроенными опциями
            self._payload()
            logger.success(f'Browser started successfully, {window_mode=}')  # Логируем успешный запуск браузера
        except WebDriverException as ex:
            logger.critical( # Логируем критическую ошибку при запуске WebDriver
                """
                ---------------------------------
                    Error starting WebDriver
                    Possible reasons:
                    - Firefox update
                    - Firefox not installed
                ----------------------------------
                """,
                ex,
            )
            sys.exit(1)
        except Exception as ex:
            logger.error('Firefox WebDriver error:', ex, exc_info=True)  # Логируем ошибку Firefox WebDriver
            return

    def set_proxy(self, options: Options) -> None:
        """
        Настраивает параметры прокси из словаря.

        Args:
            options (Options): Опции Firefox для добавления настроек прокси.
        """
        proxies_dict: dict = get_proxies_dict() #  Получаем словарь прокси
        all_proxies: list = proxies_dict.get("socks4", []) + proxies_dict.get("socks5", [])  #  Получаем все прокси

        working_proxy: Optional[dict] = None
        for proxy in random.sample(all_proxies, len(all_proxies)):
            if check_proxy(proxy):
                working_proxy = proxy
                break

        if working_proxy:
            proxy: dict = working_proxy
            protocol: str = proxy["protocol"]

            if protocol == "http":
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.http", proxy["host"])
                options.set_preference("network.proxy.http_port", int(proxy["port"]))
                options.set_preference("network.proxy.ssl", proxy["host"])
                options.set_preference("network.proxy.ssl_port", int(proxy["port"]))
                logger.info(f'Setting HTTP Proxy: http://{proxy["host"]}:{proxy["port"]}')  # Логируем установку HTTP прокси

            elif protocol == "socks4":
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.socks", proxy["host"])
                options.set_preference("network.proxy.socks_port", int(proxy["port"]))
                logger.info(f'Setting SOCKS4 Proxy: {proxy["host"]}:{proxy["port"]}')  # Логируем установку SOCKS4 прокси

            elif protocol == "socks5":
                options.set_preference("network.proxy.type", 1)
                options.set_preference("network.proxy.socks", proxy["host"])
                options.set_preference("network.proxy.socks_port", int(proxy["port"]))
                logger.info(f'Setting SOCKS5 Proxy: {proxy["host"]}:{proxy["port"]}')  # Логируем установку SOCKS5 прокси

            else:
                logger.warning(f'Unknown proxy type: {protocol}')  # Логируем предупреждение о неизвестном типе прокси
        else:
            logger.warning('No available proxies in the provided file.')  # Логируем предупреждение об отсутствии доступных прокси

    def _payload(self) -> None:
        """
        Загружает executors для локаторов и JavaScript-скриптов.
        """
        j: JavaScript = JavaScript(self) # Создаем экземпляр JavaScript
        self.get_page_lang = j.get_page_lang
        self.ready_state = j.ready_state
        self.get_referrer = j.ready_state
        self.unhide_DOM_element = j.unhide_DOM_element
        self.window_focus = j.window_focus

        execute_locator: ExecuteLocator = ExecuteLocator(self) # Создаем экземпляр ExecuteLocator
        self.execute_locator = execute_locator.execute_locator
        self.get_webelement_as_screenshot = execute_locator.get_webelement_as_screenshot
        self.get_webelement_by_locator = execute_locator.get_webelement_by_locator
        self.get_attribute_by_locator = execute_locator.get_attribute_by_locator
        self.send_message = self.send_key_to_webelement = execute_locator.send_message


if __name__ == "__main__":
    driver = Firefox()
    driver.get("https://google.com")