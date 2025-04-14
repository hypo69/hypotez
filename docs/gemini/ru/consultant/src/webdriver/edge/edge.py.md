### **Анализ кода модуля `edge.py`**

## \file /src/webdriver/edge/edge.py

Модуль содержит класс `Edge`, который наследуется от `selenium.webdriver.Edge` и предоставляет упрощенную конфигурацию Edge WebDriver, используя `fake_useragent`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование `fake_useragent` для генерации случайного user-agent.
  - Конфигурирование EdgeOptions через `EdgeOptions` и добавление различных аргументов.
  - Наличие базовой обработки исключений при запуске WebDriver.
  - Использование `j_loads_ns` для чтения конфигурационных файлов.
- **Минусы**:
  - Отсутствие подробной документации для некоторых методов и атрибутов.
  - Смешанный стиль комментариев (использованы как английский, так и русский языки).
  - Некоторые участки кода недостаточно детализированы в комментариях.
  - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Документация**:
    - Дополнить docstring для класса `Edge` и его методов, особенно для `__init__` и `set_options`, указав подробное описание параметров и возвращаемых значений.
    - Добавить описание для атрибута `driver_name`.
    - Все комментарии и docstring должны быть на русском языке в формате UTF-8.

2.  **Обработка исключений**:
    - Улучшить обработку исключений, добавив более конкретные логи сообщения об ошибках.
    - Использовать `logger.error` для логирования ошибок с передачей исключения (`ex`) в качестве второго аргумента и `exc_info=True`.
    - Добавить обработку исключений в методе `set_options`.

3.  **Конфигурация**:
    - Убедиться, что все необходимые параметры из `settings` проверяются на наличие перед использованием (например, `hasattr(settings, 'profiles') and hasattr(settings.profiles, 'default')`).

4.  **Типизация**:
    - Добавить аннотации типов для всех переменных, где это возможно.

5.  **Комментарии**:
    - Уточнить комментарии, избегая расплывчатых формулировок. Например, вместо "Загружает executors" написать "Инициализирует и загружает объекты классов для выполнения локаторов и JavaScript сценариев".
    - Добавить более подробные комментарии к блокам кода, объясняя их назначение.
    - Все комментарии должны быть на русском языке.

6.  **Использование `j_loads_ns`**:
    - Убедиться, что `j_loads_ns` используется для чтения всех конфигурационных файлов.

7.  **Структура кода**:
    - Рассмотреть возможность вынесения логики установки опций в отдельные методы для улучшения читаемости.

**Оптимизированный код:**

```python
## \file /src/webdriver/edge/edge.py
# -*- coding: utf-8 -*-\

#! .pyenv/bin/python3

"""
Модуль для работы с Edge WebDriver
=====================================

Модуль содержит класс :class:`Edge`, который наследуется от `selenium.webdriver.Edge` и предоставляет упрощенную конфигурацию,
используя `fake_useragent` для управления user-agent и параметрами запуска браузера Edge.
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
    Кастомный класс Edge WebDriver для расширенной функциональности.

    Атрибуты:
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
        **kwargs,
    ) -> None:
        """
        Инициализирует Edge WebDriver с указанным user-agent и опциями.

        Args:
            profile_name (Optional[str], optional): Имя профиля пользователя. По умолчанию `None`.
            user_agent (Optional[str], optional): User-agent, который будет использоваться.
                Если `None`, генерируется случайный user-agent. По умолчанию `None`.
            options (Optional[List[str]], optional): Список опций Edge, передаваемых при инициализации. По умолчанию `None`.
            window_mode (Optional[str], optional): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.). По умолчанию `None`.

        Raises:
            WebDriverException: Если не удается запустить Edge WebDriver.
            Exception: При возникновении общих ошибок во время запуска WebDriver.

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
                options_obj.add_argument('--kiosk')
            elif window_mode == 'windowless':
                options_obj.add_argument('--headless')
            elif window_mode == 'full_window':
                options_obj.add_argument('--start-maximized')

        # Добавление пользовательских опций, переданных при инициализации
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
        if hasattr(settings, 'profiles'):
            profile_directory = (
                settings.profiles.os
                if settings.profiles.default == 'os'
                else str(Path(gs.path.src, settings.profiles.internal))
            )

            if profile_name:
                profile_directory = str(Path(profile_directory).parent / profile_name)
            if '%LOCALAPPDATA%' in profile_directory:
                profile_directory = Path(
                    profile_directory.replace('%LOCALAPPDATA%', os.environ.get('LOCALAPPDATA'))
                )
            options_obj.add_argument(f'--user-data-dir={profile_directory}')

        try:
            logger.info('Starting Edge WebDriver')
            edgedriver_path = (
                settings.executable_path.default
            )  # Ensure this is correctly defined in your JSON file
            service = EdgeService(executable_path=str(edgedriver_path))
            super().__init__(options=options_obj, service=service)
            self._payload()
        except WebDriverException as ex:
            logger.error('Edge WebDriver failed to start:', ex, exc_info=True)
            return
        except Exception as ex:
            logger.error('Edge WebDriver crashed. General error:', ex, exc_info=True)
            return

    def _payload(self) -> None:
        """
        Инициализирует и загружает объекты классов для выполнения локаторов и JavaScript сценариев.
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
        Создает и конфигурирует опции запуска для Edge WebDriver.

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


if __name__ == '__main__':
    driver = Edge(window_mode='full_window')
    driver.get('https://www.example.com')