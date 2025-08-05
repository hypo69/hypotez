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
import re
from types import SimpleNamespace
from typing import Any, List, Optional, TYPE_CHECKING, Union, TypeVar

from src.webdriver.pydoll.llib.browser.tab import Tab as BaseTab
from src.webdriver.pydoll.llib.constants import By, Key
from src.webdriver.pydoll.llib.protocol.base import Command
from src.webdriver.pydoll.llib.browser import Chrome
from src.webdriver.pydoll.llib.elements.mixins import FindElementsMixin

from header import __root__
from src.webdriver.pydoll.options import Options # <- НЕ ПЕРЕПУТАЙ с src.webdriver.pydoll.llib.options.Options
from src.logger.logger import logger

if TYPE_CHECKING:
    from src.webdriver.pydoll.llib.elements.web_element import WebElement

T = TypeVar('T')

class Tab:
    """
    Расширенная версия вкладки (Tab), которая добавляет метод execute_locator
    и работает как прокси для оригинального объекта pydoll.browser.tab.Tab.
    """
    _base_tab: 'BaseTab' = None 

    def __init__(self, base_tab: BaseTab, *args, **kwargs):
        """
        Инициализирует базовый класс и любые дополнительные атрибуты.
        """
        # Вызов конструктора родительского класса BaseTab
        self._base_tab: 'BaseTab' = base_tab

    async def __aenter__(self) -> 'Tab':
        """Метод для входа в асинхронный контекстный менеджер."""
        logger.debug(f"Entering context for tab: {self._base_tab._target_id}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Метод для выхода из асинхронного контекстного менеджера."""
        logger.debug(f"Exiting context for tab: {self._base_tab._target_id}. Closing tab.")
        try:
            await self.close() 
        except Exception as ex:
            logger.error(f"Failed to close tab {self._base_tab._target_id} on exit: {ex}", exc_info=True)  

    def __getattr__(self, name: str) -> Any:
        """
        Магический метод, который перенаправляет все обращения к атрибутам
        к оригинальному объекту _base_tab.
        """
        return getattr(self._base_tab, name)


    @staticmethod
    def _parse_keys(key_string: str) -> List[Union[Key, str]]:
        """
        Парсит строку с клавишами в список объектов Key и обычных строк.
        """
        if not key_string:
            return []
    
        if (key_string.startswith("'") and key_string.endswith("'")) or \
           (key_string.startswith('"') and key_string.endswith('"')):
            key_string = key_string[1:-1]
    
        parsed_keys: List[Union[Key, str]] = []
        key_parts = key_string.split('+')
    
        for part in key_parts:
            part_stripped = part.strip()
            if not part_stripped: continue
            try:
                key_enum = Key[part_stripped.upper()]
                parsed_keys.append(key_enum)
            except KeyError:
                parsed_keys.append(part_stripped)
        return parsed_keys


    async def _execute_command(self, command: Command[T], timeout: Optional[int] = 60) -> T:
        """Execute CDP command via connection handler (60s timeout)."""
        return await self.base_tab._connection_handler.execute_command(command, timeout=timeout)  # type: ignore

    async def _perform_action(self, event_string: str, elements: List['WebElement'], locator: SimpleNamespace, message: Optional[str] = None) -> bool:
        """
        Выполняет ОДНУ команду-действие (клик, ввод текста и т.д.) над элементами.
    
        Args:
            event_string (str): Одна команда для выполнения, например "send_key(ENTER)".
            elements (List[WebElement]): Список элементов для выполнения действия.
            locator (SimpleNamespace): Исходный локатор для контекста (например, для логов).
            message (Optional[str]): Сообщение для `send_text`.

        Returns:
            bool: True в случае успеха, False в случае ошибки.
        """
        if not event_string or not elements:
            return False
        
        element_to_act_on = elements[0]
        try:
            if event_string.lower().startswith('send_keys'):
                match = re.search(r'\((.*)\)', event_string)
                if not match:
                    logger.warning(f"Invalid format for send_keys. Expected send_keys(...), but got: {event_string}")
                    return False

                content_to_parse = match.group(1).strip()
                keys_to_send = self._parse_keys(content_to_parse)
            
                if keys_to_send:
                    await element_to_act_on.send_keys(*keys_to_send)
                else:
                    logger.warning(f"Could not parse any valid keys from '{content_to_parse}' in event: {event_string}")
                    return False
                return True

            match event_string.lower().replace('()', ''):
                case 'click':
                    await element_to_act_on.click()
                case 'hover' | 'mouse_over':
                    await element_to_act_on.hover()
                case 'scroll_into_view':
                    await element_to_act_on.scroll_into_view()
                case 'send_text' | 'send_message' | 'type_text':
                    if message is None:
                        logger.warning(f"Event 'send_text' requires a 'message' parameter for locator: {locator.locator_description}")
                        return False
                    await element_to_act_on.type_text(message)
                    ...
                case 'clear':
                    await element_to_act_on.clear()
                case 'submit':
                    await element_to_act_on.submit()
                case _:
                    logger.warning(f"Unsupported event command: {event_string}")
                    return False
            return True
        except Exception as ex:
            logger.error(f"Error executing event command '{event_string}' for '{locator.locator_description}': {ex}", exc_info=True)
            return False
        
    async def find(
        self, 
        locator: SimpleNamespace,
        raise_exc: bool = True
    ) -> Optional[Union['WebElement', List['WebElement']]]:
        """
        Находит элемент(ы) с использованием ожидания.
        """
        by: By = None  
        
        match locator.by.lower():
            case 'xpath':
                by = By.XPATH
            case 'id':
                by = By.ID
            case 'name':
                by = By.NAME
            case 'tag_name':
                by = By.TAG_NAME
            case 'class_name':
                by = By.CLASS_NAME
            case 'css_selector':
                by = By.CSS_SELECTOR


        return await self.find_or_wait_element(
            by=by, 
            selector=locator.selector, 
            timeout=getattr(locator, 'timeout', 0), 
            find_all=True, 
            raise_exc=raise_exc
        )


    async def execute_locator(self, locator: SimpleNamespace, message: Optional[str] = None) -> Optional[Union[List['WebElement'], List[str], str, bool]]:
        """
        Находит элементы, выполняет последовательность действий и извлекает данные.
        """
        # --- Этап 0: Предварительная обработка ---
        if not getattr(locator, 'selector', None) and str(getattr(locator, 'by', '')).upper() != 'VALUE':
            if getattr(locator, 'mandatory', False):
                logger.error(f"Empty selector in a mandatory locator: {getattr(locator, 'locator_description', 'N/A')}")
            return False
        if str(getattr(locator, 'by', '')).upper() == 'VALUE':
            return getattr(locator, 'attribute', None)
    
        # --- Этап 1: ПОИСК ---
        elements = await self.find(locator, raise_exc=True)
        if not elements:
            log_func = logger.error if getattr(locator, 'mandatory', False) else logger.warning
            log_func(f"Locator failed: No elements found for '{locator.locator_description}' with selector '{locator.selector}'")
            return False

        # --- Этап 2: ВЫПОЛНЕНИЕ ПОСЛЕДОВАТЕЛЬНОСТИ ДЕЙСТВИЙ ---
        event_sequence = getattr(locator, 'event', None)
        if event_sequence:
            # Разбиваем строку на список команд
            commands = [cmd.strip() for cmd in event_sequence.split(';') if cmd.strip()]
            for command in commands:
                action_successful = await self._perform_action(command, elements, locator, message)
                if not action_successful and getattr(locator, 'mandatory', False):
                    logger.error(f"Mandatory event sequence failed at step '{command}' for locator: {locator.locator_description}")
                    return False # Прерываем всю цепочку

        # --- Этап 3: ИЗВЛЕЧЕНИЕ ДАННЫХ ---
        _attr = getattr(locator, 'attribute', None).lower()
        if not _attr:
            return elements

        try:
            extracted_data: list = []
            for el in elements:
                match _attr:
                    case 'innertext':
                        extracted_data.append(await el.text)
                    case 'innerhtml':
                        extracted_data.append(await el.inner_html)
                    case 'href':
                        extracted_data.append(await el._attributes['href'])
                        ...
                    case _:
                        extracted_data.append(await el.get_attribute(_attr))
        except Exception as ex:
            logger.error(f"Failed to get attribute '{_attr}' for locator '{locator.locator_description}': {ex}", exc_info=True)
            return False

        # --- Этап 4: ФИЛЬТРАЦИЯ РЕЗУЛЬТАТА ---
        if not extracted_data:
            logger.warning(f"No data extracted for locator: {locator.locator_description}")
            return []

        if_list = getattr(locator, 'if_list', None)
        match if_list:
            case 'all': return extracted_data
            case 'first': return extracted_data[0]
            case 'last': return extracted_data[-1]
            case 'even': return extracted_data[::2]
            case 'odd': return extracted_data[1::2]
            case list(): return [extracted_data[i] for i in if_list]
            case int(): return extracted_data[if_list - 1]
            case _: logger.warning(f"Invalid 'if_list' value: {if_list}. Expected 'all', 'first', 'last', 'even', 'odd', or a list of indices."); return extracted_data

    async def get_url(self, url:str) -> bool:
        try:
            await self.go_to(url)
            return True
        except Exception as ex:
            logger.error(f'Failed to open {url}')
            return False


async def experiment( locator: SimpleNamespace, headless: bool = False,):
    """
    Демонстрирует запуск pydoll.Chrome с полностью сконфигурированным
    объектом Options, который позволяет переопределять настройки из pydoll.json.
    """
    logger.info(f"Starting experiment with headless={headless}")
    
    # 1. Создаем объект Options. Он автоматически загрузит файл настрое браузера
    #    и применит переопределение `headless=True` (или False).
    options: Options = Options(headless=False)
    logger.debug(f"Generated arguments for Chrome: {print(options.arguments)}")

    # 2. асинхронный контекстный менеджер.
    try:
        async with Chrome(options = options) as browser:
           
            # 3. Базовая вкладка завернутая в кастомный Tab
            base_tab: 'BaseTab' = await browser.start() 
            async with Tab(base_tab) as tab:
                ...            
                await tab.go_to("https://www.google.com")
                message:str = "Hello, world!"
                await tab.execute_locator(locator = locator, message = message)
                await asyncio.sleep(5) # Пауза, чтобы увидеть результат
    
    except Exception as ex:
        logger.error(f"An error occurred during the experiment: ", ex, exc_info=True)
        ...

if __name__ == "__main__":
    # Запускаем эксперимент

    # --- google.com ---
    supplier_prefix:str = 'google.com'
    supplier_alias:str = supplier_prefix.replace('-','_').replace('.','_')
    locator:SimpleNamespace = SimpleNamespace(**{

                                                "attribute": None,
                                                "by": "XPATH",
                                                "strategy_for_multiple_selectors": "find_first_match",
                                                "selector": "//textarea[@name = 'q']",
                                                "if_list": "first",
                                                "timeout": 0,
                                                "timeout_for_event": "presence_of_element_located",
                                                "event": "send_text();send_keys(ENTER)",
                                                "mandatory": True,
                                                "text_to_be_present_in_element": "",
                                                "locator_description": "окно ввода"

        })
    

    asyncio.run(experiment( locator = locator.q_input, headless = False, ))