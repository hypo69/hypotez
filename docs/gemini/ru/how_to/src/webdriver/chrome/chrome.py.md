### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой класс `Chrome`, который расширяет возможности стандартного `webdriver.Chrome` из библиотеки Selenium. Он предназначен для упрощения и расширения управления браузером Chrome, добавляя функциональность для работы с профилями пользователей, прокси-серверами и различными режимами отображения окна браузера.

Шаги выполнения
-------------------------
1. **Инициализация класса `Chrome`**:
   - При создании экземпляра класса `Chrome` происходит загрузка конфигурации из файла `chrome.json`, расположенного в директории `src/webdriver/chrome`.
   - Определяется путь к исполняемому файлу `chromedriver` на основе конфигурации.
   - Создается объект `Service` с указанным путем к `chromedriver`.
   - Создается объект `Options` для настройки параметров Chrome.

2. **Настройка опций Chrome**:
   - Добавляются опции из файла конфигурации, такие как отключение графического интерфейса (`--headless`), запуск в режиме киоска (`--kiosk`) или максимизация окна (`--start-maximized`).
   - Устанавливается пользовательский агент (user-agent) либо из переданного параметра, либо генерируется случайным образом с использованием библиотеки `fake_useragent`.
   - Если в конфигурации включена поддержка прокси, вызывается метод `set_proxy` для настройки прокси-сервера.

3. **Настройка профиля пользователя**:
   - Определяется директория профиля пользователя Chrome. Если указано имя профиля, создается поддиректория в указанной директории профиля.
   - Добавляется аргумент `--user-data-dir` для указания директории профиля пользователя Chrome.

4. **Запуск WebDriver**:
   - Инициализируется экземпляр `webdriver.Chrome` с настроенными опциями и сервисом.
   - Вызывается метод `_payload` для загрузки дополнительных исполнителей для локаторов и JavaScript.

5. **Обработка ошибок**:
   - Обрабатываются исключения `WebDriverException` и `Exception`, возникающие при запуске и работе `webdriver.Chrome`. В случае ошибки в лог записывается критическое сообщение, и функция возвращает управление.

6. **Метод `set_proxy`**:
   - Получает словарь прокси из функции `get_proxies_dict`.
   - Перебирает прокси для поиска рабочего.
   - Настраивает прокси в зависимости от протокола (`http`, `socks4`, `socks5`), добавляя соответствующие аргументы в опции Chrome.

7. **Метод `_payload`**:
   - Создает экземпляры классов `JavaScript` и `ExecuteLocator` для выполнения JavaScript-кода и поиска элементов на странице.
   - Присваивает методы из этих классов текущему экземпляру `Chrome`, чтобы их можно было вызывать напрямую.

Пример использования
-------------------------

```python
from src.webdriver.chrome.chrome import Chrome

# Инициализация Chrome WebDriver с пользовательским профилем и оконным режимом
driver = Chrome(profile_name='my_profile', window_mode='full_window')

# Открытие веб-страницы
driver.get("https://www.google.com")

# Выполнение действий на странице
# ...

# Закрытие браузера
# driver.quit()
```
```python
## \file /src/webdriver/chrome/chrome.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
rst
.. module:: src.webdriver.chrome
    :synopsys: Модуль для работы с WebDriver Chrome
"""

import os
from pathlib import Path
from typing import Optional, List

from selenium.webdriver import Chrome as WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

from src import gs
from src.webdriver.executor import ExecuteLocator
from src.webdriver.js import JavaScript
from src.webdriver.proxy import get_proxies_dict, check_proxy
from src.utils.jjson import j_loads_ns
from src.logger.logger import logger
from fake_useragent import UserAgent
import random


class Chrome(WebDriver):
    """
    Расширение для `webdriver.Chrome` с дополнительной функциональностью.

    Args:
        profile_name (Optional[str], optional): Имя пользовательского профиля Chrome. Defaults to `None`.
        chromedriver_version (Optional[str], optional): Версия chromedriver. Defaults to `None`.
        user_agent (Optional[str], optional): Пользовательский агент в формате строки. Defaults to `None`.
        proxy_file_path (Optional[str], optional): Путь к файлу с прокси. Defaults to `None`.
        options (Optional[List[str]], optional): Список опций для Chrome. Defaults to `None`.
        window_mode (Optional[str], optional): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.). Defaults to `None`.

    """
    driver_name: str = 'chrome'
    def __init__(self, profile_name: Optional[str] = None,
                 chromedriver_version: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 proxy_file_path: Optional[str] = None,
                 options: Optional[List[str]] = None,
                 window_mode: Optional[str] = None,
                 *args, **kwargs) -> None:
        #  объявление переменных
        service: Service | None = None
        options_obj: Options | None = None

        # Загрузка настроек Chrome
        config = j_loads_ns(Path(gs.path.src / 'webdriver' / 'chrome' / 'chrome.json'))

        # Путь к chromedriver
        chromedriver_path: str = str(Path(gs.path.root, config.executable_path.chromedriver))

         # Инициализация сервиса
        service = Service(chromedriver_path)

        # Настройка опций Chrome
        options_obj = Options()

        #  Добавление опций из файла настроек
        if hasattr(config, 'options') and config.options:
            for option in config.options:
                options_obj.add_argument(option)

        #  Установка режима окна из конфига
        if hasattr(config, 'window_mode') and config.window_mode:
            window_mode = window_mode or config.window_mode
        #  Установка режима окна из параметров
        if window_mode:
            if window_mode == 'kiosk':
                options_obj.add_argument("--kiosk")
            elif window_mode == 'windowless':
               options_obj.add_argument("--headless")
            elif window_mode == 'full_window':
                 options_obj.add_argument("--start-maximized")


        #  Добавление опций, переданных при инициализации
        if options:
            for option in options:
                options_obj.add_argument(option)


        # Установка пользовательского агента
        user_agent = user_agent or UserAgent().random
        options_obj.add_argument(f'--user-agent={user_agent}')

        # Установка прокси, если включены
        if hasattr(config, 'proxy_enabled') and config.proxy_enabled:
             self.set_proxy(options_obj)


        # Настройка директории профиля
        profile_directory: str = config.profile_directory.os if config.profile_directory.default == 'os' else str(Path(gs.path.src, config.profile_directory.internal))

        if profile_name:
             profile_directory = str(Path(profile_directory).parent / profile_name)
        if '%LOCALAPPDATA%' in profile_directory:
              profile_directory = Path(profile_directory.replace('%LOCALAPPDATA%', os.environ.get('LOCALAPPDATA')))
        options_obj.add_argument(f"--user-data-dir={profile_directory}")
        try:
            logger.info('Запуск Chrome WebDriver')
            super().__init__(service=service, options=options_obj)
            self._payload()
        except WebDriverException as ex:
                logger.critical("""
                    ---------------------------------
                        Ошибка запуска WebDriver
                        Возможные причины:
                        - Обновление Chrome
                        - Отсутствие Chrome на ОС
                    ----------------------------------""", ex)
                return  # Явный возврат при ошибке
        except Exception as ex:
            logger.critical('Ошибка работы Chrome WebDriver:', ex)
            return  # Явный возврат при ошибке

    def set_proxy(self, options: Options) -> None:
        """
        Настройка прокси из словаря, возвращаемого get_proxies_dict.

        Args:
            options (Options): Опции Chrome, в которые добавляются настройки прокси.
        """
        # Получение словаря прокси
        proxies_dict = get_proxies_dict()
        # Создание списка всех прокси
        all_proxies = proxies_dict.get('socks4', []) + proxies_dict.get('socks5', [])
        # Перебор прокси для поиска рабочего
        working_proxy: dict | None = None
        for proxy in random.sample(all_proxies, len(all_proxies)):
            if check_proxy(proxy):
                working_proxy = proxy
                break
         # Настройка прокси, если он найден
        if working_proxy:
            proxy = working_proxy
            protocol = proxy.get('protocol')
            # Настройка прокси в зависимости от протокола
            if protocol == 'http':
                options.add_argument(f'--proxy-server=http://{proxy["host"]}:{proxy["port"]}')
                logger.info(f"Настройка HTTP Proxy: http://{proxy['host']}:{proxy['port']}")

            elif protocol == 'socks4':
                 options.add_argument(f'--proxy-server=socks4://{proxy["host"]}:{proxy["port"]}')
                 logger.info(f"Настройка SOCKS4 Proxy: {proxy['host']}:{proxy['port']}")

            elif protocol == 'socks5':
                options.add_argument(f'--proxy-server=socks5://{proxy["host"]}:{proxy["port"]}')
                logger.info(f"Настройка SOCKS5 Proxy: {proxy['host']}:{proxy['port']}")
            else:
                 logger.warning(f"Неизвестный тип прокси: {protocol}")
        else:
            logger.warning('Нет доступных прокси в предоставленном файле.')

    def _payload(self) -> None:
         """
        Загружает исполнителей для локаторов и JavaScript сценариев.
         """
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
    driver = Chrome(window_mode='full_window')
    driver.get(r"https://google.com")