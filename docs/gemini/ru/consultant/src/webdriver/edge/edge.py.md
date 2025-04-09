### **Анализ кода модуля `edge.py`**

## \file /src/webdriver/edge/edge.py

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `fake_useragent` для генерации случайных user-agent.
    - Наличие класса `Edge`, наследующегося от `WebDriver`, что позволяет расширять функциональность Edge WebDriver.
    - Использование `j_loads_ns` для загрузки настроек из JSON.
    - Логирование основных этапов запуска WebDriver.
    - Четкое разделение ответственности между методами, такими как `_payload` и `set_options`.
- **Минусы**:
    - Отсутствие подробной документации для некоторых методов и атрибутов.
    - Использование `hasattr` для проверки наличия атрибутов в объекте `settings`, что может быть заменено на более Pythonic-way.
    - Обработка исключений с общим `except Exception`, рекомендуется более конкретная обработка исключений.
    - Местами отсутствует описание типов, например, в `set_options`.
    - Код содержит как кириллицу так и латиницу в комментариях

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Добавить docstring для класса `Edge` и его методов, описывающие их назначение, параметры и возвращаемые значения.
    *   В docstring указать возможные исключения, которые могут быть выброшены.
    *   Подробно документировать все параметры и возвращаемые значения функций, чтобы было понятнее, для чего они нужны.

2.  **Обработка исключений**:
    *   Использовать более конкретные блоки `except` вместо общего `except Exception`. Например, можно обрабатывать `FileNotFoundError` при загрузке файла настроек.
    *   В блоках `except` использовать `logger.error` для логирования ошибок, передавая исключение как аргумент `ex` и устанавливая `exc_info=True` для получения трассировки стека.

3.  **Использование `hasattr`**:
    *   Рассмотрет варианты отказа от `hasattr` и прямого обращения к атрибутам с обработкой исключений `AttributeError` при необходимости.

4.  **Аннотации типов**:
    *   Добавить аннотации типов для всех параметров и возвращаемых значений функций, где они отсутствуют.

5.  **Улучшение читаемости**:
    *   В блоках `if` с несколькими условиями выносить условия в отдельные переменные для улучшения читаемости.

6. **Согласованность комментариев**:
   *  Привести все комментарии к одному языку (русскому).

**Оптимизированный код:**

```python
## \file /src/webdriver/edge/edge.py
# -*- coding: utf-8 -*-\
\n
#! .pyenv/bin/python3
\n
"""
Модуль для работы с Edge WebDriver
====================================

Модуль содержит класс :class:`Edge`, который используется для управления Edge WebDriver с расширенными функциями,
такими как управление user-agent, опциями запуска и профилями.

Пример использования
----------------------

>>> driver = Edge(window_mode='full_window')
>>> driver.get("https://www.example.com")
"""
\n
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
    Класс для управления Edge WebDriver с расширенными функциями.

    Attributes:
        driver_name (str): Имя драйвера, по умолчанию 'edge'.
    """
    driver_name: str = 'edge'

    def __init__(self, profile_name: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 options: Optional[List[str]] = None,
                 window_mode: Optional[str] = None,
                 *args, **kwargs) -> None:
        """
        Инициализирует Edge WebDriver с указанным user-agent и опциями.

        Args:
            profile_name (Optional[str]): Имя профиля пользователя. По умолчанию None.
            user_agent (Optional[str]): User-agent для использования. Если `None`, генерируется случайный user-agent.
            options (Optional[List[str]]): Список опций Edge для передачи во время инициализации.
            window_mode (Optional[str]): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).

        Raises:
            WebDriverException: Если не удалось запустить Edge WebDriver.
            Exception: При возникновении общей ошибки во время запуска Edge WebDriver.

        Example:
            >>> driver = Edge(window_mode='full_window')
            >>> driver.get("https://www.example.com")
        """
        self.user_agent = user_agent or UserAgent().random
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

        # Добавление пользовательских опций, переданных во время инициализации
        if options:
            for option in options:
                options_obj.add_argument(option)

        # Добавление аргументов из опций конфигурации
        if hasattr(settings, 'options') and settings.options:
            for option in settings.options:
                options_obj.add_argument(option)

        # Добавление аргументов из заголовков конфигурации
        if hasattr(settings, 'headers') and settings.headers:
            for key, value in vars(settings.headers).items():
                options_obj.add_argument(f'--{key}={value}')

        # Настройка директории профиля
        profile_directory = settings.profiles.os if settings.profiles.default == 'os' else str(
            Path(gs.path.src, settings.profiles.internal))

        if profile_name:
            profile_directory = str(Path(profile_directory).parent / profile_name)
        if '%LOCALAPPDATA%' in profile_directory:
            profile_directory = Path(profile_directory.replace('%LOCALAPPDATA%', os.environ.get('LOCALAPPDATA')))
        options_obj.add_argument(f"--user-data-dir={profile_directory}")
        try:
            logger.info('Starting Edge WebDriver')
            edgedriver_path = settings.executable_path.default  # Ensure this is correctly defined in your JSON file
            service = EdgeService(executable_path=str(edgedriver_path))
            super().__init__(options=options_obj, service=service)
            self._payload()
        except WebDriverException as ex:
            logger.critical('Edge WebDriver failed to start:', ex, exc_info=True)
            return
        except Exception as ex:
            logger.critical('Edge WebDriver crashed. General error:', ex, exc_info=True)
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
            opts (Optional[List[str]]): Список опций для добавления в Edge WebDriver. По умолчанию `None`.

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