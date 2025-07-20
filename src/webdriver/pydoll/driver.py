import asyncio
from tkinter import BitmapImage
from typing import List, Any, Optional
from types import SimpleNamespace
from dataclasses import dataclass, field # <--- Импортируем dataclass и field

from numpy import isin
# from pydoll.browser import Chrome 
# from pydoll.browser.options import ChromeOptions as Options
# from pydoll.browser.page import Page
# from pydoll.constants import By
# from pydoll.element import WebElement

from header import __root__

from src.webdriver.pydoll.llib.pydoll.browser import Chrome
from src.webdriver.pydoll.llib.pydoll.browser.options import ChromiumOptions as Options
from src.webdriver.pydoll.llib.pydoll.browser.tab import Tab
from src.webdriver.pydoll.llib.pydoll.constants import By
from src.webdriver.pydoll.llib.pydoll.elements import web_element as WebElement

from src.utils.jjson import j_loads_ns
from src.utils.printer import pprint as print
from src.logger import logger


class Config:
    """! Configuration class for Pydoll Chrome browser. """
    config_path:Path = __root__ / 'src' / 'webdriver' / 'pydoll' / 'pydoll.json'
    config: SimpleNamespace = j_loads_ns(config_path)
    if not config:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    user_profile_path: str = getattr( config, 'user_profile_path', None)
    binary_location: str = getattr( config, 'binary_location', None)
    WINDOW_MODE: str = getattr( config, 'WINDOW_MODE', None)


#@dataclass(slots=True, kw_only=True)
class Driver(Chrome):
    """Driver class for Pydoll Chrome browser."""
    

    page: Optional['Page'] = field(init=False, default=None)
    
    def __init__(self, window_mode:str, 
                 options: Optional[Options] = None, 
                 user_profile_path:Optional[str] = None, 
                 binary_location:Optional[str] = None,):
       
        window_mode = window_mode or Config.WINDOW_MODE
        user_profile_path = user_profile_path or Config.user_profile_path
        binary_location = binary_location or Config.binary_location

        options = options or Options()

        if user_profile_path:
            options.add_argument(f'--user-data-dir={user_profile_path}')

        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-default-apps')    
        options.add_argument('--start-maximized') # Важно даже в headless

        if binary_location: 
            options.binary_location = binary_location

        if window_mode == 'headless':
            options.add_argument('--headless=new')
        
        super().__init__(options=options)

    # +++ МЕТОДЫ ДЛЯ КОНТЕКСТНОГО МЕНЕДЖЕРА +++
    async def __aenter__(self):
        """Асинхронный вход в контекстный менеджер."""
        await self.async_init_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный выход из контекстного менеджера."""
        await self.close()
    # +++++++++++++++++++++++++++++++++++++++++++++++++++

    async def async_init_page(self) -> 'Page':
        """! Asynchronous initialization to set up the page. """
        if self.page is None:
            self.page = await self.get_page()
        return self.page

    async def close(self):
        """! Close the driver. """
        if self.page:
            try:
                await self.page.close()
            except Exception:
                pass # Игнорируем ошибки при закрытии страницы
        try:
            await super().close()
        except Exception:
            pass # Игнорируем ошибки при закрытии браузера

    # ... (остальные методы вашего класса без изменений)

    # --- Остальные методы остаются без изменений ---

    async def async_init_page(self) -> Page:
        """! Asynchronous initialization to set up the page.
        
        This method should be called after creating the Driver instance.
        
        Returns:
        Driver: Self reference for method chaining.
        """
        if self.page is None:
            self.page = await self.get_page()
        return self.page

    async def close(self):
        """! Close the driver. """
        if self.page:
            await self.page.close()
        await super().close()

    async def _wait_for_event(self, locator: SimpleNamespace, elements: list[WebElement]) -> bool:
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
                    # Ждем пока элемент станет кликабельным
                    if timeout_for_event == 'element_to_be_clickable':
                        await asyncio.sleep(0.1)  # Небольшая задержка для стабильности
                        # Проверяем, что элемент видим и активен
                        for element in elements:
                            if await element.is_displayed() and await element.is_enabled():
                                await element.click()
                                return True
                        return False
                    else:
                        # Просто кликаем по первому доступному элементу
                        if elements:
                            await elements[0].click()
                            return True
                        return False
                        
                case 'hover' | 'mouse_over':
                    # Наводим мышь на элемент
                    if elements:
                        await elements[0].hover()
                        return True
                    return False
                    
                case 'scroll_into_view':
                    # Скроллим к элементу
                    if elements:
                        await elements[0].scroll_into_view()
                        return True
                    return False
                    
                case 'wait_for_visible':
                    # Ждем пока элемент станет видимым
                    start_time = asyncio.get_event_loop().time()
                    while (asyncio.get_event_loop().time() - start_time) < timeout:
                        for element in elements:
                            if await element.is_displayed():
                                return True
                        await asyncio.sleep(0.5)
                    return False
                    
                case 'wait_for_invisible':
                    # Ждем пока элемент станет невидимым
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
                    # Ждем пока элемент станет активным
                    start_time = asyncio.get_event_loop().time()
                    while (asyncio.get_event_loop().time() - start_time) < timeout:
                        for element in elements:
                            if await element.is_enabled():
                                return True
                        await asyncio.sleep(0.5)
                    return False
                    
                case 'wait_for_text':
                    # Ждем пока элемент содержит определенный текст
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
                    # Ждем пока у элемента появится определенный атрибут
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
                                # Просто проверяем наличие атрибута
                                if attr_value is not None:
                                    return True
                            else:
                                # Проверяем значение атрибута
                                if attr_value == expected_value:
                                    return True
                        await asyncio.sleep(0.5)
                    return False
                    
                case 'send_keys':
                    # Отправляем ключи в элемент
                    keys_to_send = getattr(locator, 'keys_to_send', '')
                    if not keys_to_send:
                        logger.warning(f"Keys to send not specified for send_keys event in {locator.locator_description}")
                        return False
                        
                    if elements:
                        await elements[0].send_keys(keys_to_send)
                        return True
                    return False
                    
                case 'clear':
                    # Очищаем поле ввода
                    if elements:
                        await elements[0].clear()
                        return True
                    return False
                    
                case 'submit':
                    # Отправляем форму
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

    async def _wait_for_condition(self, locator: SimpleNamespace) -> list[WebElement]:
        """! Wait for a specific condition to be met before finding elements.
        
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
                elements = await self.page.find_elements(By[locator.by.upper()], locator.selector)
                
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
                        expected_text = getattr(locator, 'expected_text', '')
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
                
            await asyncio.sleep(0.5)
            
        return []

    async def execute_locator(self, locator: SimpleNamespace) -> str |  list | WebElement | bool :
        """! Locate and return content from the element based on locator info.

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
                        "locator_description": "product reference"
                  }
        """
        # Ensure page is initialized
        if not self.page:
            await self.async_init_page()

        res: list = []
        elements: WebElement | list[WebElement] = None
        selectors: list = []

        if not locator.selector or locator.selector == '':
            if locator.mandatory: # <- селектор может быть пустым. В таком случае возвращается весь вебэлемент 
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
                            elements = await self._wait_for_condition(locator, selector)
                        else:
                            elements = await self.page.find_elements(By[locator.by.upper()], selector)
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
                        2. Изменился селектор на целцвой станице 
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
            return False

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

    async def get_url(self, url: str) -> bool:
        """! Navigate to the given URL.

        Args:
        url (str): The target URL.

        Returns:
        bool: `True` if navigation was successful, else `False`.
        """
        # Ensure page is initialized
        if self.page is None:
            await self.async_init_page()
            
        try:
            await self.page.go_to(url)
            return True
        except Exception as ex:
            logger.error(f"Failed to navigate to URL: {url}", ex)
            return False