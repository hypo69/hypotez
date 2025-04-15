### **Анализ кода модуля `firefox.py`**

## \file /hypotez/src/webdriver/firefox/firefox.py

Модуль предоставляет класс `Firefox`, расширяющий стандартный `selenium.webdriver.Firefox` с дополнительными функциональностями, такими как управление профилем, киоск-мод и настройки прокси.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура класса `Firefox` с разделением на методы инициализации, настройки прокси и загрузки скриптов.
    - Использование `logger` для логирования различных этапов работы драйвера.
    - Наличие класса `Config` для управления конфигурацией драйвера из JSON файла.
- **Минусы**:
    - Отсутствуют аннотации типов для некоторых переменных.
    - Смешанный стиль кавычек (использование как одинарных, так и двойных кавычек).
    - Не все docstring переведены на русский язык.
    - Не везде используется явное указание типов при объявлении переменных.

**Рекомендации по улучшению:**

1.  **Документация модуля**:
    - Добавить заголовок модуля в формате Markdown с описанием назначения модуля и примером использования.
2.  **Класс `Config`**:
    - Добавить docstring для класса `Config` с описанием его назначения.
    - Добавить аннотации типов для полей класса `Config`.
3.  **Класс `Firefox`**:
    - Перевести docstring для класса `Firefox` и его методов на русский язык.
    - Улучшить обработку исключений, добавив больше конкретики и информативные сообщения в лог.
    - Добавить docstring для метода `set_proxy`.
    - Использовать одинарные кавычки для всех строк.
    - Добавить аннотации типов для локальных переменных.
    - Устранить дублирование кода при установке настроек прокси для разных протоколов.
4.  **Общие рекомендации**:
    - Следовать стандарту PEP8 для форматирования кода.
    - Убедиться, что все переменные и функции имеют аннотации типов.
    - Добавить больше комментариев для сложных участков кода.
    - Улучшить читаемость кода, используя более понятные имена переменных и функций.
    - Избавиться от избыточного кода и дублирования.
    - Использовать `ex` вместо `e` в блоках обработки исключений.
    - Добавить обработку возможных ошибок при чтении конфигурационного файла.
    - Использовать `j_loads` вместо `j_loads_ns` для загрузки JSON файлов.

**Оптимизированный код:**

```python
"""
Модуль для работы с WebDriver Firefox
======================================

Модуль предоставляет класс :class:`Firefox`, который расширяет стандартный
`selenium.webdriver.Firefox` с дополнительными функциональностями, такими как:
- Управление профилем Firefox.
- Режим киоска.
- Настройки прокси.

Пример использования
----------------------

>>> from src.webdriver.firefox.firefox import Firefox
>>> if __name__ == "__main__":
>>>     browser = Firefox(
>>>         profile_name="custom_profile",
>>>         window_mode="kiosk"
>>>     )
>>>     browser.get("https://www.example.com")
>>>     browser.quit()
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
from src.utils.jjson import j_loads
from src.logger.logger import logger


class Config:
    """
    Конфигурационный класс для Firefox WebDriver.

    Args:
        config_path (Path): Путь к JSON-файлу конфигурации.
    """

    def __init__(self, config_path: Path) -> None:
        """
        Инициализирует объект Config, загружая настройки из JSON-файла.
        """
        self._config = j_loads(config_path)
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

    Возможности:
        - Поддержка пользовательских профилей Firefox.
        - Режимы окна, такие как "kiosk" и другие.
        - Настройка User-Agent.
        - Настройки прокси.

    Args:
        profile_name (Optional[str], optional): Имя профиля Firefox для использования. По умолчанию None.
        geckodriver_version (Optional[str], optional): Версия GeckoDriver. По умолчанию None.
        firefox_version (Optional[str], optional): Версия Firefox. По умолчанию None.
        user_agent (Optional[str], optional): Строка User-Agent. Если None, используется случайный User-Agent. По умолчанию None.
        proxy_file_path (Optional[str], optional): Путь к файлу прокси. По умолчанию None.
        options (Optional[List[str]], optional): Список опций Firefox. По умолчанию None.
        window_mode (Optional[str], optional): Режим окна браузера (например, "windowless", "kiosk"). По умолчанию None.

    Raises:
        WebDriverException: Если не удается запустить WebDriver.
        Exception: Для других непредвиденных ошибок во время инициализации.
    """

    driver_name: str = 'firefox'

    def __init__(
        self,
        profile_name: Optional[str] = None,
        geckodriver_version: Optional[str] = None,
        firefox_version: Optional[str] = None,
        user_agent: Optional[str] = None,
        proxy_file_path: Optional[str] = None,
        options: Optional[List[str]] = None,
        window_mode: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Инициализирует Firefox WebDriver с пользовательскими настройками."""
        logger.info('Starting Firefox WebDriver')

        config: Config = Config(Path(gs.path.src, 'webdriver', 'firefox', 'firefox.json'))

        service: Service = Service(executable_path=config.geckodriver_path)
        options_obj: Options = Options()

        # Load options from config file
        if config.options:
            for option in config.options:
                options_obj.add_argument(option)

        # Set window mode
        if window_mode:
            options_obj.add_argument(f'--{window_mode}')

        # Add options from constructor
        if options:
            for option in options:
                options_obj.add_argument(option)

        # Add headers from config
        if config.headers:
            for key, value in config.headers.items():
                options_obj.add_argument(f'--{key}={value}')

        # Set user agent
        user_agent: str = user_agent or UserAgent().random
        options_obj.set_preference('general.useragent.override', user_agent)

        # Set proxy if enabled
        if config.proxy_enabled:
            self.set_proxy(options_obj)

        # Configure profile directory
        profile_directory: str = (
            config.profile_directory_os
            if config.profile_directory_default == 'os'
            else str(Path(gs.path.src, config.profile_directory_internal))
        )

        if profile_name:
            profile_directory = str(Path(profile_directory).parent / profile_name)
        if '%LOCALAPPDATA%' in profile_directory:
            profile_directory = Path(
                profile_directory.replace('%LOCALAPPDATA%', os.environ.get('LOCALAPPDATA'))
            )

        # profile = FirefoxProfile(profile_directory=profile_directory) #  <- @debug не грузится профиль

        try:
            super().__init__(service=service, options=options_obj)
            self._payload()
            logger.success(f'Browser started successfully, {window_mode=}')
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
            logger.critical('Firefox WebDriver error:', ex, False)
            return

    def set_proxy(self, options: Options) -> None:
        """Настраивает параметры прокси из словаря.

        Args:
            options (Options): Firefox options для добавления параметров прокси.
        """
        proxies_dict: dict = get_proxies_dict()
        all_proxies: list = proxies_dict.get('socks4', []) + proxies_dict.get('socks5', [])

        working_proxy: Optional[dict] = None
        for proxy in random.sample(all_proxies, len(all_proxies)):
            if check_proxy(proxy):
                working_proxy = proxy
                break

        if working_proxy:
            proxy: dict = working_proxy
            protocol: str = proxy['protocol']
            host: str = proxy['host']
            port: int = int(proxy['port'])

            options.set_preference('network.proxy.type', 1)
            options.set_preference(f'network.proxy.{protocol}', host)
            options.set_preference(f'network.proxy.{protocol}_port', port)
            logger.info(f'Setting {protocol.upper()} Proxy: {host}:{port}')
        else:
            logger.warning('No available proxies in the provided file.')

    def _payload(self) -> None:
        """Загружает executors для локаторов и JavaScript скриптов."""
        j: JavaScript = JavaScript(self)
        self.get_page_lang = j.get_page_lang
        self.ready_state = j.ready_state
        self.get_referrer = j.ready_state
        self.unhide_DOM_element = j.unhide_DOM_element
        self.window_focus = j.window_focus

        execute_locator: ExecuteLocator = ExecuteLocator(self)
        self.execute_locator = execute_locator.execute_locator
        self.get_webelement_as_screenshot = execute_locator.get_webelement_as_screenshot
        self.get_webelement_by_locator = execute_locator.get_webelement_by_locator
        self.get_attribute_by_locator = execute_locator.get_attribute_by_locator
        self.send_message = self.send_key_to_webelement = execute_locator.send_message


if __name__ == '__main__':
    driver: Firefox = Firefox()
    driver.get('https://google.com')