import asyncio
from calendar import c
from typing import List, Any
from types import SimpleNamespace
from pydoll.browser.chrome import Chrome
from pydoll.constants import By
from pydoll.browser.page import Page

from header import __root__
from src.logger import logger


async def execute_locator(page: 'Page', locator: SimpleNamespace) -> Any:
    """Locate and return content from the element based on locator info."""
    
    if locator.by.upper() == 'VALUE':
        return locator.attribute
    
    res:list = []
    elements:'WebElement' | list['WebElement' ] = None

    """XPATH не умеет в жадную логику"""
    match getattr(locator,'strategy_for_multiple_selectors','find_first_match').lower():
        case 'find_first_match':
            selectors:list = locator.selector.split(';')
            for selector in selectors:
                try:
                    elements = await page.find_elements(By[locator.by.upper()], selector)
                    if elements:
                        break
                except Exception as ex:
                    logger.warning(f"Error executing locator: {locator}", ex, exc_info=True)
                    return None
                
    
    
    match getattr(locator,'attribute','').lower():
        case '':
            # Локатор {locator} не содержит атрибута для извлечения данных.\n
            # Вероятней всего мне требутеся весь вебэелемент"
            res = elements 

        case 'innertext':
            if len(elements) == 1:
                return await elements[0].get_element_text()
            res = [await el.get_element_text() for el in elements]
            
        
        case 'innerhtml':
            if len(elements) == 1:
                return await elements[0].inner_html
            res =  [await el.inner_html for el in elements]

        case  'src' | 'href':
            
            if len(elements) == 1:
                return elements[0].get_attribute(locator.attribute) 
            res =  [ el.get_attribute(locator.attribute) for el in elements]
            

        case _:
            raise ValueError(f"Unsupported attribute: {locator=}")

    match getattr(locator,'if_list','').lower():

        case '':
            return res

        case 'all':
            return res

        case 'first':
            return res[0]

        case 'last':
            return res[-1]

        case 'even':
            return [res[i] for i in range(0, len(res), 2)]

        case 'odd':
            return [res[i] for i in range(1, len(res), 2)]

        case isinstance(if_list, list):
            return [res[i] for i in if_list]

        case isinstance(if_list, int):
            return res[if_list - 1]

    return None
