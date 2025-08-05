## \file /src/webdriver/pydoll/driver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3


"""
Модуль предоставляет высокоуровневый асинхронный драйвер для управления браузером на базе `pydoll`.
======================================================================================================
Модуль реализует асинхронный класс `Driver`, который служит высокоуровневой оберткой над библиотекой `pydoll`
для автоматизации браузера Chrome. Основная цель — упростить взаимодействие с веб-страницами за счет
использования декларативного подхода на основе 'локаторов'.

Ключевая функциональность:
- **Асинхронность:** Все операции с браузером выполняются асинхронно с использованием `asyncio`.
- **Контекстный менеджер:** Поддерживает `async with` для автоматического открытия и закрытия браузера.
- **Управление через локаторы:** Вместо последовательных вызовов методов Selenium-подобного API используется
  единый метод `execute_locator`, который принимает объект-локатор. Этот объект описывает все шаги:
  поиск элемента, ожидание определенного состояния, выполнение действия (клик, ввод текста) и извлечение
  данных (текст, атрибуты).
- **Конфигурация:** Настройки браузера (путь к профилю, режим запуска) загружаются из файла `pydoll.json`.

Пример локатора:
```json
{
  "reference": {
    "attribute": "innerText",
    "by": "XPATH",
    "strategy_for_multiple_selectors": "find_first_match",
    "selector": "//span[contains(@class, 'sku-copy')]",
    "if_list": "first",
    "mandatory": true,
    "timeout": 10,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "text_to_be_present_in_element":"","locator_description": "product reference"
  }
}

Пример использования:
```python
from src.webdriver.pydoll.driver import Driver

driver = Driver(window_mode='headless')

async with driver as browser:
    await browser.get_url('https://example.com')
    reference = await browser.execute_locator(browser.page.locators.reference)
    print(reference)
    
```
"""

import asyncio
import os
import subprocess
from http.cookies import SimpleCookie
from pathlib import Path
from tracemalloc import start
from typing import List,  Optional, Any, TYPE_CHECKING
from types import SimpleNamespace
from dataclasses import dataclass, field

from src.webdriver.pydoll.llib.browser import Chrome 

from header import __root__
if TYPE_CHECKING:
    from src.webdriver.pydoll.llib.elements.web_element import WebElement
    from src.webdriver.pydoll.llib.browser.tab import Tab as base_tab

from src.webdriver.pydoll.options import Options # <- НЕ ПЕРЕПУТАЙ с src.webdriver.pydoll.llib.options.Options
from src.webdriver.pydoll.tab import Tab
from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint as print
from src.logger import logger


class Browser(Chrome):
    """
    Высокоуровневый асинхронный драйвер для браузера Pydoll Chrome.

    Args:
        window_mode (Optional[str]): Режим окна ('headless', 'normal'). По умолчанию используется значение из Config.
        options (Optional[Options]): Пользовательские опции для запуска Chrome.
        user_data_dir (Optional[str]): Путь к профилю пользователя Chrome.
        binary_location (Optional[str]): Путь к исполняемому файлу браузера.
        user_agent (Optional[str]): Пользовательский User-Agent.
        incognito (bool): Запуск в режиме инкогнито. По умолчанию False.
        disable_gpu (bool): Отключение аппаратного ускорения GPU. По умолчанию True.
    """
    pid_file: Path = __root__ / 'src' / 'webdriver' / 'pydoll' / 'process.pid'
    def __init__(self, options: Optional[Options] = None, connection_port: Optional[int] = 0, **kwargs):
        """"""

        super().__init__(options = options or Options(), connection_port = connection_port)
        ...

    def kill_previous_pid(self):
        """"! Удаляет файл с PID предыдущего процесса браузера, если он существует. """
        try:
            probably_pid = self.pid_file.read_text().strip()
        except FileNotFoundError as ex:
            return # Файл не найден, ничего не делаем

        if probably_pid:
            try:
                os.kill(int(probably_pid), 9)
                ...
            except Exception as ex:
                logger.error(f'process {probably_pid} not successfully killed', ex)
                ...
            finally:
                self.pid_file.unlink(missing_ok=True)

    async def save_current_pid(self):
        """! Сохраняет PID текущего процесса браузера в файл. """
        if self.process and self.process.pid:
            self.pid_file.write_text(str(self.process.pid),encoding='UTF-8')
        else:
            logger.warning("Process PID is not available, cannot save.")

    async def start(self) -> Optional[Tab]:
        """! Start the browser and create the first tab.

        Returns:
            Tab: The first tab if successful, None otherwise.
        """
        # Если программа падает - удаляем предыдущий PID (браузера)
        self.kill_previous_pid()
        try:            
            base_tab: 'BaseTab' = await super().start()
            await self.save_current_pid()
            tab = Tab(base_tab)
            return tab
        except Exception as ex:
            logger.error(f"Error starting browser: ",ex)
            return None

    async def close(self):
        """! Close the driver. """
        try:
            await super().close()
        except Exception:
            ... # Игнор ошибки при закрытии браузера
