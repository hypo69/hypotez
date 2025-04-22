### **Анализ кода модуля `edge.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Класс `Edge` предоставляет удобный интерфейс для настройки и запуска WebDriver Edge с использованием `fake_useragent` для генерации случайных user-agent.
  - Использование `j_loads_ns` для загрузки настроек из JSON-файла упрощает управление конфигурацией.
  - Обработка различных режимов окна (kiosk, windowless, full_window) делает класс более гибким.
  - Добавлены обработка исключений при запуске WebDriver для предотвращения падений приложения.
  - Применение логгирования через `logger` для отслеживания процесса инициализации и возможных ошибок.
- **Минусы**:
  - Отсутствуют подробные docstring для некоторых методов, например, `_payload` и `set_options`.
  - В коде есть дублирование логики добавления аргументов в `options_obj` (из `settings.options` и переданных аргументов).
  - Не все переменные аннотированы типами.
  - Не используется `cls` вместо `self` там где это возможно
  - Местами есть не консистентность. Например, у нас есть функция `set_options`, но нет функции `set_user_agent`.

**Рекомендации по улучшению**:
1. **Документация**:
   - Добавить подробные docstring для методов `_payload` и `set_options`, описывающие их назначение, параметры и возвращаемые значения.
   - Перевести все docstring на русский язык.
   - Добавить примеры использования для основных методов.

2. **Рефакторинг**:
   - Избегать дублирования логики при добавлении аргументов в `options_obj`. Можно объединить циклы в один.
   - Добавить аннотации типов для всех переменных и параметров функций.
   - Использовать `cls` вместо `self` там, где это уместно (например, если метод не использует состояние экземпляра класса).
   - Рассмотреь вопрос о создании функции `set_user_agent` для консистентности.
   - Использовать более конкретные типы исключений вместо `Exception` в блоке `except`.
   - Заменить все `Union[]` на `|`.
   - Использовать webdriver из `src.webdriver`

3. **Обработка исключений**:
   - Улучшить обработку исключений, добавив более конкретные типы исключений и информативные сообщения в лог.

4. **Улучшение конфигурации**:
   - Рассмотреть возможность вынесения настроек user-agent в отдельный файл конфигурации.

**Оптимизированный код**:
```python
## \file /src/webdriver/edge/edge.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для создания и управления драйвером Edge с расширенными настройками.
========================================================================

Модуль содержит класс :class:`Edge`, который позволяет настраивать и запускать драйвер Edge с использованием
различных опций, включая user-agent, режим окна и профили.

Пример использования
----------------------

>>> driver = Edge(window_mode='full_window')
>>> driver.get("https://www.example.com")
"""

import os
from pathlib import Path
from typing import Optional, List
from selenium.webdriver import Edge as WebDriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import WebDriverException
from src.webdriver.executor import ExecuteLocator
from src.webdriver.js import JavaScript
from fake_useragent import UserAgent
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns


class Edge(WebDriver):
    """
    Кастомный класс WebDriver Edge для расширенной функциональности.

    Attributes:
        driver_name (str): Имя используемого WebDriver, по умолчанию 'edge'.
    """
    driver_name: str = 'edge'

    def __init__(
        self,
        profile_name: Optional[str] = None,
        user_agent: Optional[str] = None,
        options: Optional[List[str]] = None,
        window_mode: Optional[str] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Инициализирует Edge WebDriver с указанным user-agent и опциями.

        Args:
            profile_name (Optional[str], optional): Имя профиля. По умолчанию `None`.
            user_agent (Optional[str], optional): User-agent для использования. Если `None`, генерируется случайный user-agent. По умолчанию `None`.
            options (Optional[List[str]], optional): Список опций Edge для передачи при инициализации. По умолчанию `None`.
            window_mode (Optional[str], optional): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.). По умолчанию `None`.

        """
        self.user_agent: str = user_agent or UserAgent().random
        settings = j_loads_ns(Path(gs.path.src, 'webdriver', 'edge', 'edge.json'))

        # Инициализация опций Edge
        options_obj = EdgeOptions()
        options_obj.add_argument(f'user-agent={self.user_agent}')

        # Установка режима окна из конфига
        if hasattr(settings, 'window_mode') and settings.window_mode:
            window_mode = window_mode or settings.window_mode

        # Установка режима окна из параметров
        if window_mode:
            if window_mode == 'kiosk':
                options_obj.add_argument("--kiosk")
            elif window_mode == 'windowless':
                options_obj.add_argument("--headless")
            elif window_mode == 'full_window':
                options_obj.add_argument("--start-maximized")

        # Добавление пользовательских опций, переданных при инициализации
        if options:
            for option in options:
                options_obj.add_argument(option)

        # Добавление аргументов из конфигурации
        if hasattr(settings, 'options') and settings.options:
            for option in settings.options:
                options_obj.add_argument(option)

        # Добавление аргументов из заголовков конфигурации
        if hasattr(settings, 'headers') and settings.headers:
            for key, value in vars(settings.headers).items():
                options_obj.add_argument(f'--{key}={value}')

        # Настройка директории профиля
        profile_directory = settings.profiles.os if settings.profiles.default == 'os' else str(Path(gs.path.src, settings.profiles.internal))

        if profile_name:
            profile_directory = str(Path(profile_directory).parent / profile_name)
        if '%LOCALAPPDATA%' in profile_directory:
            profile_directory = Path(profile_directory.replace('%LOCALAPPDATA%', os.environ.get('LOCALAPPDATA')))
        options_obj.add_argument(f"--user-data-dir={profile_directory}")

        try:
            logger.info('Запуск Edge WebDriver')
            edgedriver_path = settings.executable_path.default  # Убедитесь, что это правильно определено в вашем JSON-файле
            service = EdgeService(executable_path=str(edgedriver_path))
            super().__init__(options=options_obj, service=service)
            self._payload()
        except WebDriverException as ex:
            logger.critical('Не удалось запустить Edge WebDriver:', ex, exc_info=True)
            return
        except Exception as ex:
            logger.critical('Edge WebDriver завершился с ошибкой. Общая ошибка:', ex, exc_info=True)
            return

    def _payload(self) -> None:
        """
        Загружает executors для локаторов и JavaScript сценариев.
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

    def set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions:
        """
        Создает и конфигурирует параметры запуска для Edge WebDriver.

        Args:
            opts (Optional[List[str]], optional): Список опций для добавления в Edge WebDriver. По умолчанию `None`.

        Returns:
            EdgeOptions: Сконфигурированный объект `EdgeOptions`.
        """
        options = EdgeOptions()
        if opts:
            for opt in opts:
                options.add_argument(opt)
        return options


if __name__ == "__main__":
    driver = Edge(window_mode='full_window')
    driver.get("https://www.example.com")