## \file /src/webdriver/chrome/chrome.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с WebDriver Chrome.
======================================
Этот модуль предоставляет расширенный класс `Chrome` для Selenium WebDriver,
включая автоматическую настройку опций, профилей, User-Agent и прокси.

 ```rst
 .. module:: src.webdriver.chrome
    :synopsys: Модуль для работы с WebDriver Chrome
 ```
"""

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
    """
    Расширение для `webdriver.Chrome` с дополнительной функциональностью.

    Args:
        profile_name (str | None, optional): Имя пользовательского профиля Chrome. По умолчанию `None`.
        chromedriver_version (str | None, optional): Версия chromedriver (в текущей реализации не используется, путь к chromedriver берется из конфигурации). По умолчанию `None`.
        user_agent (str | None, optional): Пользовательский агент в формате строки. Если `None`, генерируется случайный. По умолчанию `None`.
        proxy_file_path (str | None, optional): Путь к файлу с прокси (в текущей реализации не используется, прокси берутся через `get_proxies_dict`). По умолчанию `None`.
        options (list[str] | None, optional): Список дополнительных строковых опций для Chrome. По умолчанию `None`.
        window_mode (str | None, optional): Режим окна браузера (например, 'windowless', 'kiosk', 'full_window'). По умолчанию `None`.
        *args: Дополнительные позиционные аргументы для `selenium.webdriver.Chrome`.
        **kwargs: Дополнительные именованные аргументы для `selenium.webdriver.Chrome`.

    Raises:
        WebDriverException: Если происходит ошибка при запуске WebDriver (например, несовместимость версий, отсутствие Chrome).
        Exception: При других общих ошибках во время инициализации.

    Example:
        >>> driver = Chrome(profile_name='my_profile', window_mode='full_window')
        >>> driver.get('https://google.com')
        >>> # driver.quit()
    """
    driver_name: str = 'chrome'

    def __init__(self, profile_name: str | None = None,
                 chromedriver_version: str | None = None, # Параметр не используется
                 user_agent: str | None = None,
                 proxy_file_path: str | None = None, # Параметр не используется
                 options: list[str] | None = None,
                 window_mode: str | None = None,
                 *args, **kwargs) -> None:
        # Объявление переменных, используемых в методе
        service: Service | None = None
        options_obj: Options | None = None
        config: 'SimpleNamespace | dict' # Type hint for j_loads_ns result
        chromedriver_path: str
        profile_directory: str | Path

        # Загрузка конфигурационных настроек для Chrome из JSON-файла
        config = j_loads_ns(Path(gs.path.src / 'webdriver' / 'chrome' / 'chrome.json'))

        # Проверка, что конфигурация загружена успешно
        if not config or not hasattr(config, 'executable_path') or not hasattr(config.executable_path, 'chromedriver'):
            logger.critical('Ошибка загрузки конфигурации Chrome или отсутствуют необходимые ключи.', None, exc_info=False)
            return # Завершение инициализации при ошибке конфигурации

        # Формирование полного пути к исполняемому файлу chromedriver
        chromedriver_path = str(Path(gs.path.root, config.executable_path.chromedriver))

        # Инициализация объекта Service для управления chromedriver
        service = Service(chromedriver_path)

        # Создание объекта Options для настройки параметров запуска Chrome
        options_obj = Options()

        # Добавление опций в объект Options из загруженной конфигурации
        if hasattr(config, 'options') and config.options:
            for option_val in config.options: # Renamed 'option' to 'option_val' to avoid conflict
                options_obj.add_argument(option_val)

        # Определение режима окна: используется значение из аргументов функции или из конфигурации
        current_window_mode: str | None = window_mode
        if not current_window_mode and hasattr(config, 'window_mode') and config.window_mode:
            current_window_mode = config.window_mode

        # Применение выбранного режима окна к опциям запуска
        if current_window_mode:
            if current_window_mode == 'kiosk':
                options_obj.add_argument('--kiosk')
            elif current_window_mode == 'windowless':
                options_obj.add_argument('--headless')
            elif current_window_mode == 'full_window':
                options_obj.add_argument('--start-maximized')

        # Добавление дополнительных опций, переданных как аргумент, в объект Options
        if options:
            for option_val in options: # Renamed 'option' to 'option_val'
                options_obj.add_argument(option_val)

        # Установка User-Agent: используется переданный или генерируется случайный
        final_user_agent: str = user_agent or UserAgent().random
        options_obj.add_argument(f'--user-agent={final_user_agent}')

        # Вызов метода для настройки прокси, если это указано в конфигурации
        if hasattr(config, 'proxy_enabled') and config.proxy_enabled:
            self.set_proxy(options_obj)

        # Определение и настройка пути к директории профиля пользователя Chrome
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
                """
                    ---------------------------------
                        Ошибка запуска WebDriver
                        Возможные причины:
                        - Обновление Chrome
                        - Отсутствие Chrome на ОС
                        - Несовместимость chromedriver
                    ----------------------------------""", ex, exc_info=True)
            return  # Завершение инициализации при ошибке
        except Exception as ex:
            logger.critical('Непредвиденная ошибка при инициализации Chrome WebDriver.', ex, exc_info=True)
            return  # Завершение инициализации при ошибке

    def set_proxy(self, options: Options) -> None:
        """
        Настраивает HTTP/SOCKS4/SOCKS5 прокси для WebDriver из списка доступных.

        Выбирает случайный рабочий прокси из тех, что возвращает `get_proxies_dict`
        и применяет его к объекту `Options`.

        Args:
            options (Options): Объект опций Chrome, в который добавляются настройки прокси.
        """
        # Объявление переменных
        proxies_dict: dict
        all_proxies: list
        working_proxy: dict | None = None
        proxy_details: dict | None = None # Renamed 'proxy' to 'proxy_details' to avoid confusion in loops
        protocol: str | None = None

        # Извлечение словаря с доступными прокси-серверами
        proxies_dict = get_proxies_dict()
        if not proxies_dict:
            logger.warning('Словарь прокси пуст или не удалось его получить. Прокси не будет установлен.')
            return

        # Формирование общего списка прокси типов SOCKS4 и SOCKS5
        all_proxies = proxies_dict.get('socks4', []) + proxies_dict.get('socks5', []) + proxies_dict.get('http', [])

        if not all_proxies:
            logger.warning('Список доступных прокси пуст. Прокси не будет установлен.')
            return

        # Случайный перебор прокси из списка для нахождения активного и проверки его работоспособности
        shuffled_proxies = random.sample(all_proxies, len(all_proxies))
        for p_details in shuffled_proxies:
            if check_proxy(p_details): # Предполагается, что check_proxy принимает словарь p_details
                working_proxy = p_details
                break
        
        # Если найден рабочий прокси, его данные используются для настройки
        if working_proxy:
            proxy_details = working_proxy
            protocol = proxy_details.get('protocol')
            host: str | None = proxy_details.get('host')
            port: str | int | None = proxy_details.get('port')

            if not host or not port:
                logger.warning(f'Неполные данные для прокси: {proxy_details}. Прокси не будет установлен.')
                return

            # Добавление аргумента для указания прокси-сервера в опции Chrome в зависимости от протокола
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
        """
        Инициализирует и привязывает к экземпляру драйвера вспомогательные методы.

        Функция загружает исполнителей для JavaScript сценариев и операций с веб-элементами,
        делая их доступными как методы самого объекта `Chrome`.
        """
        j: JavaScript = JavaScript(self)
        self.get_page_lang = j.get_page_lang
        self.ready_state = j.ready_state
        self.get_referrer = j.get_referrer # Исправлено с j.ready_state на j.get_referrer
        self.unhide_DOM_element = j.unhide_DOM_element
        self.window_focus = j.window_focus

        execute_locator: ExecuteLocator = ExecuteLocator(self)
        self.execute_locator = execute_locator.execute_locator
        self.get_webelement_as_screenshot = execute_locator.get_webelement_as_screenshot
        self.get_webelement_by_locator = execute_locator.get_webelement_by_locator
        self.get_attribute_by_locator = execute_locator.get_attribute_by_locator
        self.send_message = self.send_key_to_webelement = execute_locator.send_message

if __name__ == '__main__':
    # Пример использования:
    # Для корректной работы примера убедитесь, что gs.path.src и gs.path.root настроены,
    # а также файл конфигурации 'src/webdriver/chrome/chrome.json' существует и корректен.
    # Также необходим chromedriver, путь к которому указан в chrome.json.
    try:
        driver = Chrome(window_mode='full_window')
        if hasattr(driver, 'service') and driver.service.process: # Проверка, что драйвер успешно инициализировался
            driver.get(r'https://google.com')
            logger.info(f'Заголовок страницы: {driver.title}')
            # Рекомендуется всегда закрывать драйвер после использования
            # driver.quit() # Раскомментируйте для автоматического закрытия браузера
        else:
            logger.error('Не удалось инициализировать WebDriver.')
    except Exception as ex:
        logger.error(f'Ошибка в примере использования Chrome: {ex}', exc_info=True)
