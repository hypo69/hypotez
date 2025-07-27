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
from pathlib import Path
from tracemalloc import start
from typing import List,  Optional, Any, TYPE_CHECKING
from types import SimpleNamespace
from dataclasses import dataclass, field

from pydoll.browser import Chrome 
from pydoll.browser.options import ChromiumOptions as Options
from pydoll.constants import By
from pydoll.browser.tab import Tab as BaseTab
if TYPE_CHECKING:
    from pydoll.element import WebElement
    


from header import __root__
from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint as print
from src.logger import logger

class Config:
    """! Configuration class for Pydoll Chrome browser. """
    config_path:Path = __root__ / 'src' / 'webdriver' / 'pydoll' / 'pydoll.json'
    config: SimpleNamespace = j_loads_ns(config_path)
    if not config:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    user_data_dir: str = getattr( config, 'user_data_dir', None)
    binary_location: str = getattr( config, 'binary_location', None)
    WINDOW_MODE: str = getattr( config, 'WINDOW_MODE', None)


class Tab:
    """
    Расширенная версия вкладки (Tab), которая добавляет метод execute_locator
    и работает как прокси для оригинального объекта pydoll.browser.tab.Tab.
    """
    def __init__(self, base_tab: 'BaseTab'):
        """
        Инициализирует обертку, сохраняя оригинальный объект вкладки.
        
        Args:
            base_tab (BaseTab): Оригинальный экземпляр вкладки из pydoll.
        """
        self._base_tab = base_tab

    def __getattr__(self, name: str) -> Any:
        """
        Магический метод, который перенаправляет все обращения к атрибутам,
        которых нет в этой обертке, к оригинальному объекту _base_tab.
        Это позволяет вызывать методы вроде tab.close() или получать доступ
        к tab.page так, как будто мы работаем с оригинальным объектом.
        """
        return getattr(self._base_tab, name)

    async def _find_elements(self, locator:SimpleNamespace) -> Optional[ List['WebElement'] ]:
        """! Find elements on the page.

        Args:
            by (By): The method to locate elements (e.g., By.XPATH).
            selector (str): The selector string to use for locating elements.

        Returns:
            list[WebElement]: A list of found web elements.
        """
        elements: List['WebElement'] = []
        match locator.by.upper():
            case 'XPATH' | 'CSS_SELECTOR':
                elements = await self.find(locator.selector, find_all=True)
                ...
            case 'ID':
                elements = await self.find(id=locator.selector, find_all=True)
            case _:
                raise ValueError(f"Unsupported locator strategy: {locator.by}")

        return elements 

    async def _wait_for_event(self, locator: SimpleNamespace, elements: List['WebElement']) -> bool:
        """! Wait for a specific event to occur on elements.
        
        Args:
            locator (SimpleNamespace): Locator configuration object.
            elements (list[WebElement]): List of elements to wait for event.
            
        Returns:
            bool: True if event occurred successfully, False otherwise.
        """
        if not locator.event:
            return True
            
        timeout = getattr(locator, 'timeout', 10)
        timeout_for_event = getattr(locator, 'timeout_for_event', 'presence_of_element_located')
        
        try:
            match locator.event.lower():
                case 'click':
                    # Ожидание пока элемент станет кликабельным
                    if timeout_for_event == 'element_to_be_clickable':
                        await asyncio.sleep(0.1)  # Небольшая задержка для стабильности
                        # Проверяем, что элемент видим и активен
                        for element in elements:
                            if await element.is_displayed() and await element.is_enabled():
                                await element.click()
                                return True
                        return False 
                    else:
                        # Клик по первому доступному элементу
                        if elements:
                            await elements[0].click()
                            return True
                        return False

                case 'hover' | 'mouse_over':
                    # Наведение мыши на элемент
                    if elements:
                        await elements[0].hover()
                        return True
                    return False 
                    
                case 'scroll_into_view':
                    # Скролл к элементу
                    if elements:
                        await elements[0].scroll_into_view()
                        return True
                    return False

                case 'wait_for_visible':
                    # Ожидание пока элемент станет видимым
                    start_time = asyncio.get_event_loop().time()
                    while (asyncio.get_event_loop().time() - start_time) < timeout:
                        for element in elements:
                            if await element.is_displayed():
                                return True
                        await asyncio.sleep(0.5)
                    return False

                case 'wait_for_invisible':
                    # Ожидание пока элемент станет невидимым
                    start_time = asyncio.get_event_loop().time()
                    while (asyncio.get_event_loop().time() - start_time) < timeout:
                        all_invisible = True
                        for element in elements:
                            if await element.is_displayed():
                                all_invisible = False
                                break
                        if all_invisible:
                            return True
                        await asyncio.sleep(0.5)
                    return False 
                    
                case 'wait_for_enabled':
                    # Ожидание пока элемент станет активным
                    start_time = asyncio.get_event_loop().time()
                    while (asyncio.get_event_loop().time() - start_time) < timeout:
                        for element in elements:
                            if await element.is_enabled():
                                return True
                        await asyncio.sleep(0.5)
                    return False
                    
                case 'wait_for_text':
                    # Ожидание пока элемент содержит определенный текст
                    expected_text = getattr(locator, 'expected_text', '')
                    if not expected_text:
                        logger.warning(f"Expected text not specified for wait_for_text event in {locator.locator_description}")
                        return False
                        
                    start_time = asyncio.get_event_loop().time()
                    while (asyncio.get_event_loop().time() - start_time) < timeout:
                        for element in elements:
                            text = await element.get_element_text()
                            if expected_text in text:
                                return True
                        await asyncio.sleep(0.5)
                    return False 
                    
                case 'wait_for_attribute':
                    # Ожидание пока у элемента появится определенный атрибут
                    expected_attribute = getattr(locator, 'expected_attribute', '')
                    expected_value = getattr(locator, 'expected_value', None)
                    
                    if not expected_attribute:
                        logger.warning(f"Expected attribute not specified for wait_for_attribute event in {locator.locator_description}")
                        return False 
                        
                    start_time = asyncio.get_event_loop().time()
                    while (asyncio.get_event_loop().time() - start_time) < timeout:
                        for element in elements:
                            attr_value = await element.get_attribute(expected_attribute)
                            if expected_value is None:
                                # Проверка наличия атрибута
                                if attr_value is not None:
                                    return True
                            else:
                                # Проверка значения атрибута
                                if attr_value == expected_value:
                                    return True
                        await asyncio.sleep(0.5)
                    return False

                case 'send_keys':
                    # Отправка ключей в элемент
                    keys_to_send = getattr(locator, 'keys_to_send', '')
                    if not keys_to_send:
                        logger.warning(f"Keys to send not specified for send_keys event in {locator.locator_description}")
                        return  [] 
                        
                    if elements:
                        await elements[0].send_keys(keys_to_send)
                        return True
                    return  []

                case 'clear':
                    # Очистка поля ввода
                    if elements:
                        await elements[0].clear()
                        return True
                    return False
                    
                case 'submit':
                    # Отправка формы
                    if elements:
                        await elements[0].submit()
                        return True
                    return False 
                    
                case _:
                    logger.warning(f"Unsupported event type: {locator.event} in {locator.locator_description}")
                    return False 
                    
        except Exception as ex:
            logger.error(f"Error executing event {locator.event} for {locator.locator_description}: {ex}")
            return False

    async def _wait_for_condition(self, locator: SimpleNamespace) -> Optional[ List['WebElement'] ]:
        """ Wait for a specific condition to be met before finding elements.
        
        Args:
            locator (SimpleNamespace): Locator configuration object.
            selector (str): CSS/XPath selector string.
            
        Returns:
            list[WebElement]: List of found elements or empty list if condition not met.
        """
        timeout = getattr(locator, 'timeout', 10)
        timeout_for_event = getattr(locator, 'timeout_for_event', 'presence_of_element_located')
        
        start_time = asyncio.get_event_loop().time()
        
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            try:
                elements = await self._find_elements(locator)

                match timeout_for_event.lower():
                    case 'presence_of_element_located':
                        # Элемент просто должен присутствовать в DOM
                        if elements:
                            return elements
                            
                    case 'visibility_of_element_located':
                        # Элемент должен быть видимым
                        visible_elements = []
                        for element in elements:
                            if await element.is_displayed():
                                visible_elements.append(element)
                        if visible_elements:
                            return visible_elements
                            
                    case 'element_to_be_clickable':
                        # Элемент должен быть кликабельным
                        clickable_elements = []
                        for element in elements:
                            if await element.is_displayed() and await element.is_enabled():
                                clickable_elements.append(element)
                        if clickable_elements:
                            return clickable_elements
                            
                    case 'invisibility_of_element_located':
                        # Элемент должен быть невидимым или отсутствовать
                        if not elements:
                            return []
                        invisible_elements = []
                        for element in elements:
                            if not await element.is_displayed():
                                invisible_elements.append(element)
                        if len(invisible_elements) == len(elements):
                            return invisible_elements
                            
                    case 'text_to_be_present_in_element':
                        # В элементе должен быть определенный текст
                        expected_text = getattr(locator, 'text_to_be_present_in_element', '')
                        if not expected_text:
                            logger.warning(f"Expected text not specified for text_to_be_present_in_element in {locator.locator_description}")
                            return []
                            
                        matching_elements = []
                        for element in elements:
                            text = await element.get_element_text()
                            if expected_text in text:
                                matching_elements.append(element)
                        if matching_elements:
                            return matching_elements
                            
                    case 'attribute_to_be_present':
                        # У элемента должен быть определенный атрибут
                        expected_attribute = getattr(locator, 'expected_attribute', '')
                        if not expected_attribute:
                            logger.warning(f"Expected attribute not specified for attribute_to_be_present in {locator.locator_description}")
                            return []
                            
                        matching_elements = []
                        for element in elements:
                            attr_value = await element.get_attribute(expected_attribute)
                            if attr_value is not None:
                                matching_elements.append(element)
                        if matching_elements:
                            return matching_elements
                            
                    case _:
                        logger.warning(f"Unsupported timeout_for_event: {timeout_for_event} in {locator.locator_description}")
                        if elements:
                            return elements
                            
            except Exception as ex:
                logger.debug(f"Waiting for condition {timeout_for_event} for {locator.locator_description}: {ex}")
                return []
                
            await asyncio.sleep(0.5)
            
        return []

    async def execute_locator(self, locator: SimpleNamespace) -> Optional[List['WebElement'] | str]:
        """ Locate and return content from the element based on locator info.

        Args:
            locator (SimpleNamespace): Locator configuration object.

        Returns:
            Any: The data extracted or list of elements depending on locator and strategy.

        Raises:
            ValueError: If an unsupported attribute is requested.

        locator exmaple:
          "reference": {
                        "attribute": "innerText",
                        "by": "XPATH",
                        "strategy_for_multiple_selectors": "find_first_match",
                        "selector": "//span[ contains( @class, 'sku-copy')]",
                        "if_list": "first",
                        "mandatory": true,
                        "timeout": 0,
                        "timeout_for_event": "presence_of_element_located",
                        "event": null,
                        "text_to_be_present_in_element":"","locator_description": "product reference"
                  }
        """

        res: list = []
        elements: list['WebElement'] = []
        selectors: list = []

        if not locator.selector and str(locator.by).upper() != 'VALUE':
            if locator.mandatory: # <- селектор может быть пустым. В таком случае возвращается весь вебэлемент если стратегия 'VALUE' 
                logger.warning(f"""Пустой селектор в обязательном локаторе: {locator.locator_description if hasattr(locator,'locator_description') else print(locator)}""", 
               None, False)
            return False

        if ';' in locator.selector: # <- проверка на множественные селекторы
            selectors = locator.selector.split(';')
        else:
            selectors = [locator.selector]
          
        # Special case for 'value' in starteg `BY` returned value from locator.attribute
        # f.e. supplier_id = locator.attribute
        if str(locator.by).upper() == 'VALUE':  
            return locator.attribute

        # Strategy for multiple selectors (`XPATH` не умеет в ленивые операторы)
        # todo:
        #   ЗДЕСЬ ПЛОХАЯ ЛОГИКА> Имеется в ввиду разбор селектора на составные части. 
        #   В текущей реализации я должен задать селектор в формате <selector >;<selector>;...
        #   т.е. разбивать формат XPATH селектора на блоки
        #   задача: переписать логику для парсинга собственно селектора.
        #   Тогда я смогу не ломать формат XPATH
        #   Пример XPATH с несколькими селекторами:
        #   {"selector":"//div[@class='header'];//div[@id='main-title']"}
        #   Пример XPATH с условными операторами: 
        #   {"selector":"//div[@class='header'] | //div[@id='main-title']"}
        #   {"selector":"//input[@type='text' or @type='password']"}
        #   {"selector":"//*[contains(@class, 'btn') or contains(@class, 'button')]"}
        #   {"selector":"//h1[@id='title'] | //h2[@id='subtitle'] | //h3[@id='section']"}
        #   {"selector":"//a[contains(@href, 'example.com') or @target='_blank']"}
        #   (//div[contains(@class, 'description')])[2]//div | (//div[contains(@class, 'description')])[2]//p  

        match getattr(locator, 'strategy_for_multiple_selectors', 'find_first_match').lower():
            case 'find_first_match':
                for selector in selectors:
                    try:
                        # Обработка ожиданий
                        if hasattr(locator, 'timeout_for_event') and locator.timeout_for_event and \
                           hasattr(locator, 'timeout') and  locator.timeout:
                            elements = await self._wait_for_condition(locator)
                            ...
                        else:
                            elements = await self._find_elements(locator)
                            ...
                        if elements:
                            break
                        else:
                            continue
                    except Exception as ex:
                        logger.warning(f"Error executing locator: {locator.locator_description=}", ex, exc_info=False)
                        return False

        if not elements:
            logger.warning(f"""Пустое значение для локатора  `{locator.locator_description=}`.
                    Возможные причины:
                        1. Нет данных на целевой странице
                        2. Изменился селектор на целевой странице
                        3. общая ошибка локатора""")
            return False

        # ПЕРВЫЙ ЭТАП: Выполнение событий (если они есть)
        if hasattr(locator, 'event') and locator.event:
            event_success = await self._wait_for_event(locator, elements)
            if not event_success:
                logger.warning(f"Event {locator.event} failed for {locator.locator_description}")
                if getattr(locator, 'mandatory', False):
                    return False

        # ВТОРОЙ ЭТАП: Возврат атрибута или элемента
        # Если атрибут не указан - возвращаем весь веб-элемент
        if not hasattr(locator, 'attribute') or not locator.attribute:
            _result = elements
            if isinstance(_result, list) and len(_result) == 1:
                return _result[0]
            else:
                return _result

        
        # Если атрибут указан - извлекаем его значение
        match getattr(locator, 'attribute', '').lower():
            case 'innertext':
                if len(elements) == 1:
                    _result = await elements[0].get_element_text()
                else:
                    _result = [await el.get_element_text() for el in elements]

            case 'innerhtml':
                if len(elements) == 1:
                    # _result = await elements[0].inner_html
                    _result = [elements[0].inner_html]
                else:
                    # _result = [await el.inner_html for el in elements]
                     _result = [ el.inner_html for el in elements]

            case 'src' | 'href':
                if len(elements) == 1:
                    # _result = await elements[0].get_attribute(locator.attribute)
                    _result =  elements[0].get_attribute(locator.attribute)
                else:
                    # _result = [await el.get_attribute(locator.attribute) for el in elements]
                    _result = [ el.get_attribute(locator.attribute) for el in elements]

            case _:
                raise ValueError(f"Unsupported attribute: {locator.attribute} in {locator.locator_description}")

        # Проверка на пустой результат
        if len(_result) == 0:
            return []

        # ТРЕТИЙ ЭТАП: Применение стратегии фильтрации списка
        if_list = getattr(locator, 'if_list', '')
        match if_list:
            case '':
                return _result
            case 'all':
                return _result
            case 'first':
                return _result[0] if isinstance(_result, list) else _result 
            case 'last':
                return _result[-1] if isinstance(_result, list) else _result 
            case 'even':
                return [_result[i] for i in range(0, len(_result), 2)] if isinstance(_result, list) else _result 
            case 'odd':
                return [_result[i] for i in range(1, len(_result), 2)] if isinstance(_result, list) else _result 
            case list() if isinstance(if_list, list): # <- список полей по номерам. Например [1,6,8]
                return [_result[i] for i in if_list if isinstance(i, int)] if isinstance(_result, list) else _result 
            case int() if isinstance(if_list, int): # <-  полей по номеру. Например 4
                return _result[if_list - 1] if isinstance(_result, list) else _result 
            case _:
                return _result

    async def get_url(self, url:str) -> bool:
        """"""
        try:
            await self.go_to(url)
            return True
        except Exception as ex:
            logger.error(f"Failed to navigate to {url}: ", ex)
            return False




class Driver(Chrome):
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
        user_data_dir: Optional[str] = None,
        binary_location: Optional[str] = None,
        user_agent: Optional[str] = None,
        incognito: bool = False,
        disable_gpu: bool = True
    ):
        
        resolved_window_mode: str = window_mode or Config.WINDOW_MODE
        resolved_user_data_dir: str | None = user_data_dir or Config.user_data_dir
        resolved_binary_location: str | None = binary_location or Config.binary_location
        resolved_options: Options = options or Options()

        # --- Настройка опций браузера ---

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

