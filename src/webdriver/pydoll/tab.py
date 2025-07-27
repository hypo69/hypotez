## \file src/webdriver/pydoll/tab.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Класс Tab для расширенной работы с вкладками браузера Pydoll.
===============================================================
Модуль предоставляет класс Tab, который является оберткой над базовым Tab
из pydoll.browser.tab и добавляет методы execute_locator для работы с локаторами.
Поддерживает асинхронные операции, ожидание событий и извлечение данных из элементов.

```rst
.. module:: src.webdriver.pydoll.tab
```
"""

import header
from header import __root__
import asyncio
from typing import Any, List, Optional, Union
from types import SimpleNamespace
from pydoll.browser import Chrome
from pydoll.constants import By
from pydoll.browser.tab import Tab as BaseTab
from src.logger.logger import logger

if TYPE_CHECKING:
    from pydoll.element import WebElement


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
        self._base_tab: 'BaseTab' = base_tab

    def __getattr__(self, name: str) -> Any:
        """
        Магический метод, который перенаправляет все обращения к атрибутам,
        которых нет в этой обертке, к оригинальному объекту _base_tab.
        Это позволяет вызывать методы вроде tab.close() или получать доступ
        к tab.page так, как будто мы работаем с оригинальным объектом.
        
        Args:
            name (str): Имя атрибута для получения.
            
        Returns:
            Any: Значение атрибута из базового объекта.
        """
        return getattr(self._base_tab, name)

    async def _find_elements(self, locator: SimpleNamespace) -> Optional[List['WebElement']]:
        """
        Function finds elements on the page.

        Args:
            locator (SimpleNamespace): Объект локатора с настройками поиска.

        Returns:
            Optional[List[WebElement]]: Список найденных веб-элементов или None.
        """
        elements: List['WebElement'] = []
        
        try:
            match locator.by.upper():
                case 'XPATH' | 'CSS_SELECTOR':
                    elements = await self.find(locator.selector, find_all=True)
                case 'ID':
                    elements = await self.find(id=locator.selector, find_all=True)
                case _:
                    raise ValueError(f"Unsupported locator strategy: {locator.by}")

            return elements
            
        except Exception as ex:
            logger.error(f'Error finding elements with locator {locator.selector}: {ex}', ex, exc_info=True)
            return None

    async def _wait_for_event(self, locator: SimpleNamespace, elements: List['WebElement']) -> bool:
        """
        Function waits for a specific event to occur on elements.
        
        Args:
            locator (SimpleNamespace): Locator configuration object.
            elements (List[WebElement]): List of elements to wait for event.
            
        Returns:
            bool: True if event occurred successfully, False otherwise.
        """
        if not locator.event:
            return True
            
        timeout: int = getattr(locator, 'timeout', 10)
        timeout_for_event: str = getattr(locator, 'timeout_for_event', 'presence_of_element_located')
        
        try:
            match locator.event.lower():
                case 'click':
                    # Ожидание пока элемент станет кликабельным
                    if timeout_for_event == 'element_to_be_clickable':
                        await asyncio.sleep(0.1)  # Небольшая задержка для стабильности
                        # Проверка, что элемент видим и активен
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
                    expected_text: str = getattr(locator, 'expected_text', '')
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
                    expected_attribute: str = getattr(locator, 'expected_attribute', '')
                    expected_value: Optional[str] = getattr(locator, 'expected_value', None)
                    
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
                    keys_to_send: str = getattr(locator, 'keys_to_send', '')
                    if not keys_to_send:
                        logger.warning(f"Keys to send not specified for send_keys event in {locator.locator_description}")
                        return False 
                        
                    if elements:
                        await elements[0].send_keys(keys_to_send)
                        return True
                    return False

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
            logger.error(f"Error executing event {locator.event} for {locator.locator_description}: {ex}", ex, exc_info=True)
            return False

    async def _wait_for_condition(self, locator: SimpleNamespace) -> Optional[List['WebElement']]:
        """
        Function waits for a specific condition to be met before finding elements.
        
        Args:
            locator (SimpleNamespace): Locator configuration object.
            
        Returns:
            Optional[List[WebElement]]: List of found elements or empty list if condition not met.
        """
        timeout: int = getattr(locator, 'timeout', 10)
        timeout_for_event: str = getattr(locator, 'timeout_for_event', 'presence_of_element_located')
        
        start_time = asyncio.get_event_loop().time()
        
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            try:
                elements = await self._find_elements(locator)

                if not elements:
                    await asyncio.sleep(0.5)
                    continue

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
                        expected_text: str = getattr(locator, 'text_to_be_present_in_element', '')
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
                        expected_attribute: str = getattr(locator, 'expected_attribute', '')
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
                
            await asyncio.sleep(0.5)
            
        return []

    async def execute_locator(self, locator: SimpleNamespace) -> Optional[List['WebElement'] | str]:
        """
        Function locates and returns content from the element based on locator info.

        Args:
            locator (SimpleNamespace): Locator configuration object.

        Returns:
            Optional[List[WebElement] | str]: The data extracted or list of elements depending on locator and strategy.

        Raises:
            ValueError: If an unsupported attribute is requested.

        Example:
            locator example:
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
                            "text_to_be_present_in_element":"",
                            "locator_description": "product reference"
                      }
        """
        res: List = []
        elements: List['WebElement'] = []
        selectors: List = []

        if not locator.selector and str(locator.by).upper() != 'VALUE':
            if locator.mandatory: # <- селектор может быть пустым. В таком случае возвращается весь вебэлемент если стратегия 'VALUE' 
                logger.warning(f"""Пустой селектор в обязательном локаторе: {locator.locator_description if hasattr(locator,'locator_description') else locator}""", 
               None, False)
            return False

        if ';' in locator.selector: # <- проверка на множественные селекторы
            selectors = locator.selector.split(';')
        else:
            selectors = [locator.selector]
          
        # Special case for 'value' in strategy `BY` returned value from locator.attribute
        # Example: supplier_id = locator.attribute
        if str(locator.by).upper() == 'VALUE':  
            return locator.attribute

        # Strategy for multiple selectors (`XPATH` не умеет в ленивые операторы)
        # TODO:
        #   ЗДЕСЬ ПЛОХАЯ ЛОГИКА. Имеется в виду разбор селектора на составные части. 
        #   В текущей реализации нужно задать селектор в формате <selector >;<selector>;...
        #   т.е. разбивать формат XPATH селектора на блоки
        #   задача: переписать логику для парсинга собственно селектора.
        #   Тогда можно не ломать формат XPATH
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
                        # Создание временного локатора для текущего селектора
                        temp_locator = SimpleNamespace(**vars(locator))
                        temp_locator.selector = selector
                        
                        # Обработка ожиданий
                        if hasattr(locator, 'timeout_for_event') and locator.timeout_for_event and \
                           hasattr(locator, 'timeout') and locator.timeout:
                            elements = await self._wait_for_condition(temp_locator)
                        else:
                            elements = await self._find_elements(temp_locator)
                            
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
                        3. Общая ошибка локатора""")
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
                    _result = elements[0].inner_html
                else:
                    _result = [el.inner_html for el in elements]

            case 'src' | 'href':
                if len(elements) == 1:
                    _result = elements[0].get_attribute(locator.attribute)
                else:
                    _result = [el.get_attribute(locator.attribute) for el in elements]

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
            case int() if isinstance(if_list, int): # <- поле по номеру. Например 4
                return _result[if_list - 1] if isinstance(_result, list) else _result 
            case _:
                return _result

    async def get_url(self, url: str) -> bool:
        """
        Function navigates to the specified URL.
        
        Args:
            url (str): URL to navigate to.
            
        Returns:
            bool: True if navigation successful, False otherwise.
        """
        try:
            await self.go_to(url)
            return True
        except Exception as ex:
            logger.error(f"Failed to navigate to {url}: ", ex, exc_info=True)
            return False