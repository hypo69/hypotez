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

import asyncio
from types import SimpleNamespace
from typing import Any, List, Optional, TYPE_CHECKING, Union

from pydoll.browser.tab import Tab as BaseTab
if TYPE_CHECKING:
    from pydoll.elements.web_element import WebElement

from header import __root__ 
from src.logger.logger import logger
from src.webdriver.pydoll.executor import ExecuteLocator



class Tab:
    """
    Расширенная версия вкладки (Tab), которая добавляет метод execute_locator
    и работает как прокси для оригинального объекта pydoll.browser.tab.Tab.
    """

    

    
    def __init__(self, base_tab: BaseTab):
        """
        Инициализирует обертку, сохраняя оригинальный объект вкладки.
        
        Args:
            base_tab (BaseTab): Оригинальный экземпляр вкладки из pydoll.
        """
        self._base_tab: 'BaseTab' = base_tab

        _executor: ExecuteLocator = ExecuteLocator(self)
        self.execute_locator = _executor.execute_locator
        self.get_webelement_as_screenshot = _executor.get_webelement_as_screenshot
        self.get_webelement_by_locator = _executor.get_webelement_by_locator
        self.get_attribute_by_locator = _executor.get_attribute_by_locator
        self.send_message = _executor.send_message
        self.send_key_to_webelement = _executor.send_message


    def __getattr__(self, name: str) -> Any:
        """
        Магический метод, который перенаправляет все обращения к атрибутам,
        которых нет в этой обертке, к оригинальному объекту _base_tab.
        """
        return getattr(self._base_tab, name)

    async def __aenter__(self) -> 'Tab':
        """
        Метод для входа в асинхронный контекстный менеджер.
        """
        logger.debug(f"Entering context for tab: {self._base_tab._target_id}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Метод для выхода из асинхронного контекстного менеджера.
        """
        logger.debug(f"Exiting context for tab: {self._base_tab._target_id}. Closing tab.")
        try:
            await self.close() 
        except Exception as ex:
            logger.error(f"Failed to close tab {self._base_tab._target_id} on exit: {ex}", exc_info=True)  



    # async def _find_elements_with_wait(self, locator: SimpleNamespace) -> Optional[List['WebElement']]:
    #     """
    #     Находит элементы, ожидая выполнения определенного условия (видимость, кликабельность).
        
    #     Args:
    #         locator (SimpleNamespace): Объект локатора с настройками поиска и ожидания.

    #     Returns:
    #         List[WebElement]: Список найденных веб-элементов. Пустой список, если ничего не найдено.
    #     """
    #     timeout: int = getattr(locator, 'timeout', 10)
    #     wait_condition: str = getattr(locator, 'timeout_for_event', 'presence_of_element_located')
    #     start_time = asyncio.get_event_loop().time()
        
    #     while (asyncio.get_event_loop().time() - start_time) < timeout:
    #         elements: List['WebElement'] = []
    #         try:
    #             # --- ИСПОЛЬЗОВАНА ВАША ПРАВИЛЬНАЯ ЛОГИКА ---
    #             match getattr(locator, 'by', 'CSS_SELECTOR').upper():
    #                 case 'XPATH' | 'CSS_SELECTOR':
    #                     # Вызов `self.find` делегируется в `_base_tab.find` через `__getattr__`
    #                     elements = await self.find(locator.selector, find_all=True)
    #                 case 'ID':
    #                     elements = await self.find(id=locator.selector, find_all=True)
    #                 case _:
    #                     logger.error(f"Unsupported locator strategy: {locator.by}")
    #                     return [] # Критическая ошибка конфигурации, выходим
    #             # ---------------------------------------------
                
    #             # Проверка условия ожидания
    #             match wait_condition.lower():
    #                 case 'presence_of_element_located':
    #                     if elements: return elements
    #                 case 'visibility_of_element_located':
    #                     visible_elements = [el for el in elements if await el.is_displayed()]
    #                     if visible_elements: return visible_elements
    #                 case 'element_to_be_clickable':
    #                     clickable_elements = [el for el in elements if await el.is_displayed() and await el.is_enabled()]
    #                     if clickable_elements: return clickable_elements
    #                 case 'invisibility_of_element_located':
    #                     if not elements: return []
    #         except Exception as ex:
    #             logger.debug(f"Attempt failed while waiting for '{locator.selector}': {ex}")

    #         await asyncio.sleep(0.5)
            
    #     logger.warning(f"Timeout ({timeout}s) while waiting for condition '{wait_condition}' on selector '{locator.selector}'")
    #     return []

    # async def _perform_action(self, locator: SimpleNamespace, elements: List['WebElement'], message: Optional[str] = None) -> bool:
    #     """
    #     Выполняет действие (клик, ввод текста и т.д.) над уже найденными элементами.
        
    #     Args:
    #         locator (SimpleNamespace): Объект локатора с описанием действия (`event`).
    #         elements (List[WebElement]): Список элементов для выполнения действия.
    #         message (Optional[str]): Сообщение для ввода (для `send_keys`).

    #     Returns:
    #         bool: True в случае успеха, False в случае ошибки.
    #     """
    #     event_name = getattr(locator, 'event', None)
    #     if not event_name or not elements:
    #         return False
            
    #     try:
    #         element_to_act_on = elements[0]
    #         match event_name.lower().replace('()', ''):
    #             case 'click':
    #                 await element_to_act_on.click()
    #             case 'hover' | 'mouse_over':
    #                 await element_to_act_on.hover()
    #             case 'scroll_into_view':
    #                 await element_to_act_on.scroll_into_view()
    #             case 'send_keys':
    #                 if message is None:
    #                     logger.warning(f"Event 'send_keys' called without a message for locator: {locator.locator_description}")
    #                     return False
    #                 await element_to_act_on.send_keys(message)
    #             case 'clear':
    #                 await element_to_act_on.clear()
    #             case 'submit':
    #                 await element_to_act_on.submit()
    #             case _:
    #                 logger.warning(f"Unsupported event type: {event_name}")
    #                 return False
    #         return True
    #     except Exception as ex:
    #         logger.error(f"Error executing event '{event_name}' for '{locator.locator_description}': {ex}", exc_info=True)
    #         return False

    # async def execute_locator(self, locator: SimpleNamespace, message: Optional[str] = None) -> Optional[Union[List['WebElement'], List[str], str, bool]]:
    #     """
    #     Находит элементы, выполняет действия и извлекает данные согласно локатору.
    #     """
    #     # --- Этап 0: Предварительная обработка ---
    #     if not getattr(locator, 'selector', None) and str(getattr(locator, 'by', '')).upper() != 'VALUE':
    #         if getattr(locator, 'mandatory', False):
    #             logger.error(f"Empty selector in a mandatory locator: {getattr(locator, 'locator_description', 'N/A')}")
    #         return False
        
    #     if str(getattr(locator, 'by', '')).upper() == 'VALUE':
    #         return getattr(locator, 'attribute', None)
        
    #     # --- Этап 1: ПОИСК И ОЖИДАНИЕ ---
    #     elements = await self._find_elements_with_wait(locator)

    #     if not elements:
    #         log_func = logger.error if getattr(locator, 'mandatory', False) else logger.warning
    #         log_func(f"Locator failed: No elements found for '{locator.locator_description}' with selector '{locator.selector}'")
    #         return False

    #     # --- Этап 2: ВЫПОЛНЕНИЕ ДЕЙСТВИЯ (если указано) ---
    #     if getattr(locator, 'event', None):
    #         action_successful = await self._perform_action(locator, elements, message)
    #         if not action_successful and getattr(locator, 'mandatory', False):
    #             logger.error(f"Mandatory event '{locator.event}' failed for locator: {locator.locator_description}")
    #             return False

    #     # --- Этап 3: ИЗВЛЕЧЕНИЕ ДАННЫХ (если указан атрибут) ---
    #     attribute_to_get = getattr(locator, 'attribute', None)
    #     if not attribute_to_get:
    #         return elements

    #     try:
    #         extracted_data: list = []
    #         for el in elements:
    #             if attribute_to_get.lower() == 'innertext':
    #                 extracted_data.append(await el.get_element_text())
    #             elif attribute_to_get.lower() == 'innerhtml':
    #                 extracted_data.append(await el.get_attribute('innerHTML'))
    #             else:
    #                 extracted_data.append(await el.get_attribute(attribute_to_get))
    #     except Exception as ex:
    #         logger.error(f"Failed to get attribute '{attribute_to_get}' for locator '{locator.locator_description}': {ex}", exc_info=True)
    #         return False

    #     # --- Этап 4: ФИЛЬТРАЦИЯ РЕЗУЛЬТАТА ---
    #     if not isinstance(extracted_data, list) or not extracted_data:
    #         return extracted_data

    #     match getattr(locator, 'if_list', 'all'):
    #         case 'first': return extracted_data[0]
    #         case 'last': return extracted_data[-1]
    #         case 'even': return extracted_data[::2]
    #         case 'odd': return extracted_data[1::2]
    #         case _: return extracted_data

    # async def get_url(self, url: str) -> bool:
    #     """
    #     Переходит по указанному URL.
    #     """
    #     try:
    #         await self.goto(url)
    #         return True
    #     except Exception as ex:
    #         logger.error(f"Failed to navigate to {url}: ", ex, exc_info=True)
    #         return False
