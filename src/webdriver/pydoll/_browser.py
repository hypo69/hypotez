## \file /src/webdriver/pydoll/driver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 




#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 


#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 
#                        DEPRECATED 









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
from http.cookies import SimpleCookie
from pathlib import Path
from tracemalloc import start
from typing import List,  Optional, Any, TYPE_CHECKING
from types import SimpleNamespace
from dataclasses import dataclass, field

from pydoll.browser import Chrome 

from header import __root__
if TYPE_CHECKING:
    from pydoll.element import WebElement
    from pydoll.browser.tab import Tab as base_tab
    from pydoll.browser.options import ChromiumOptions

from src.webdriver.pydoll.options import Options
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
    tabs:List[Tab] = []
    def __init__(
        self,
        window_mode: Optional[str] = None,
        options: Optional[Options] = None,
    ):
        
        
        options = options or Options()
        resolved_user_data_dir: str | = user_data_dir or options.user_data_dir
        resolved_binary_location: str | None = binary_location or Config.binary_location
        resolved_options: Options = options or Options()

        

        # 1. Профиль, расположение и идентификация
        if resolved_user_data_dir:
            resolved_options.add_argument(f'--user-data-dir={resolved_user_data_dir}')
        if resolved_binary_location:
            resolved_options.binary_location = resolved_binary_location
        if user_agent:
            resolved_options.add_argument(f'user-agent={user_agent}')

        # 2. Опции для стабильности и производительности в средах автоматизации
        resolved_options.add_argument('--no-sandbox')  # Отключает песочницу, часто необходимо для Docker/CI.
        resolved_options.add_argument('--disable-dev-shm-usage') # Предотвращает сбои из-за ограниченных ресурсов в /dev/shm.
        if disable_gpu:
            resolved_options.add_argument('--disable-gpu') # Отключает GPU, важно для стабильности в headless-режиме.

        # 3. Настройки поведения и интерфейса браузера
        resolved_options.add_argument('--start-maximized')  # Запускает браузер в развернутом окне (важно и для headless).
        resolved_options.add_argument('--disable-infobars')  # Отключает уведомление "Chrome is being controlled...".
        resolved_options.add_argument('--disable-extensions')  # Отключает все расширения.
        
        resolved_options.add_argument('--disable-notifications')  # Отключает веб-уведомления.
        resolved_options.add_argument('--disable-default-apps')  # Отключает установку приложений по умолчанию.
        resolved_options.add_argument('--disable-translate')  # Отключает встроенный переводчик страниц.
        resolved_options.add_argument('--disable-background-networking')  # Отключает фоновую сетевую активность.

        # Может вызывать ошибку, если опция уже установлена в профиле.
        # resolved_options.add_argument('--disable-popup-blocking')  # Отключает блокировку всплывающих окон.
        # resolved_options.add_argument('--no-default-browser-check')  # Не проверять, является ли Chrome браузером по умолчанию.
        # resolved_options.add_argument('--no-first-run')      # Не выполнять первый запуск.

        # 4. Прочие настройки
        resolved_options.add_argument('--mute-audio')  # Отключает звук в браузере.
        resolved_options.add_argument('--ignore-certificate-errors')  # Игнорирует ошибки сертификатов SSL.
        if incognito:
            resolved_options.add_argument('--incognito') # Запускает браузер в режиме инкогнито.

        # 5. Режим запуска (обычный или headless)
        if resolved_window_mode == 'headless':
            resolved_options.add_argument('--headless=new') # Использует новый, более стабильный headless-режим.

        super().__init__(options = resolved_options)

        ...


    # +++ МЕТОДЫ ДЛЯ КОНТЕКСТНОГО МЕНЕДЖЕРА +++
    async def __aenter__(self) -> Optional[Tab]:
        """
        Асинхронный вход в контекстный менеджер.
        Запускает браузер и создает первую вкладку.
        """
        try:
            base_tab: 'BaseTab' = await super().start()
            tab: Tab  = Tab(base_tab)
            self.tabs.append(tab)
            return tab
        except Exception as ex:
            print(f"Error starting browser: ", ex)
            return None
        

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный выход из контекстного менеджера."""
        await self.close()
    # +++++++++++++++++++++++++++++++++++++++++++++++++++

    async def start(self) -> Optional[Tab]:
        """! Start the browser and create the first tab.

        Returns:
            Tab: The first tab if successful, None otherwise.
        """
        try:
            base_tab: 'BaseTab' = await super().start()
            tab = Tab(base_tab)
            self.tabs.append(tab)
            return tab
        except Exception as ex:
            print(f"Error starting browser: ", ex)
            return None


    async def new_tab(self, url: Optional[str] = None) -> Optional[Tab]:
        """! Create a new tab, wrap it in our custom Tab class, and return it.
        
        Args:
            url (str, optional): The URL to navigate to. Defaults to None.
            
        Returns:
            Tab: The newly created custom tab 
        """
        try:
            base_tab: BaseTab = await super().new_tab(url)
            tab:Tab = Tab(base_tab)
            return tab
        except Exception as ex:
            logger.error("Failed to create a new tab. Ensure the browser is running.", ex)
            return None

        tab = Tab(base_tab)
        self.tabs.append(tab)
        return tab

    async def close(self):
        """! Close the driver. """
        try:
            await super().close()
        except Exception:
            ... # Игнор ошибки при закрытии браузера
