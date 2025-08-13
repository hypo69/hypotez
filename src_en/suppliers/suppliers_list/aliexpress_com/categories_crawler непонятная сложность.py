# # \file /src/suppliers/suppliers_list/aliexpress/sceanrio.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Category management module for AliExpress supplier.
====================================================================
This module contains functions for interacting with the categories of AliExpress products,
including the collection of URL addresses of goods from categories and updating the list of categories
Based on data from the site.

`` `RST
 .. Module :: src.suppliers.suppliers_list.aliexpress_com.sceanrio
    : Platform: Windows, Unix
    : synopsis: Category Management AliExpress
`` `"""

import header # Default import
from header import __root__ # Default import
from src import gs # Default import

from typing import List, Dict, Any, Tuple 
from pathlib import Path
import requests # Added import for requests

from src.utils.jjson import j_dumps, j_loads
from src.logger.logger import logger
# from src.utils.printer import pprint as print # Add if print is used

# Placeholder for actual Supplier class and other external dependencies
# from src.suppliers.models import Supplier # Example, replace with actual
# from src.db_manager import manager, AliexpressCategory # Example
# from src.utils.notifications import send # Example

# Using TypeAlias for placeholder types for better readability
from typing import TypeAlias
Supplier: TypeAlias = Any # Placeholder for the actual Supplier class/type
WebDriverInstance: TypeAlias = Any # Placeholder for s.driver type
LocatorType: TypeAlias = Dict[str, Any] # Placeholder for locator structure
AliexpressCategoryModel: TypeAlias = Any # Placeholder for DB model
DBManager: TypeAlias = Any # Placeholder for DB manager

# Placeholder for the 'send' function if it's not imported from a specific module
def send(subject: str, message: str) -> None:
    """PLACEHOLDER For A Function that Sends Notifications (E.G., Email).

    Args:
        Subject (str): The topic of the message.
        Message (str): Text of the message."""
    logger.info(f'Функция send вызвана с темой: {subject} и сообщением: {message}')
    # The real logic of sending should be here


def get_list_products_in_category(s: Supplier) -> List[str]:
    """The function reads the URL of goods from the category page.

    If there are several pages with goods in the same category, the function flows everything.
    It is important to understand that by this moment the webdraiter had to open a page of categories.

    Args:
        S (SUPPLIER): A copy of the supplier containing a driver and locators.

    Returns:
        List [str]: a list of collected URLs of goods. Can be empty if
                   There are no goods in the studied category.
    
    Example:
        >>> Supplier_instance = ... # initialization of the copy of Supplier
        >>> Product_urls = get_list_products_in_category (supraplier_instance)
        >>> If Product_URLS:
        ... print (f'niden {len (product_urls)} URL of goods. ')"""
    
    return get_prod_urls_from_pagination (s)
        

def get_prod_urls_from_pagination(s: Supplier) -> List[str]:
    """The function collects links to goods from the page of the category with pages flipping.
    
    Args:
        S (SUPPLIER): A copy of the supplier containing `driver` and` locators'.
    
    Returns:
        List [str]: a list of links collected from the category page.
                   Returns an empty list if the goods are not found.
    
    Example:
        >>> Supplier_instance = ... # initialization of the copy of Supplier
        >>> urls = get_prod_urls_from_pagination (superplier_instance)
        >>> Print (urls)"""
    
    _d: WebDriverInstance = s.driver
    _l_product_links: LocatorType = s.locators['category']['product_links']
    _l_pagination_next: LocatorType = s.locators['category']['pagination']['->']
    
    list_products_in_category: List[str] | str | None
    
    # Removing links from the first page
    list_products_in_category = _d.execute_locator(_l_product_links)
    
    if not list_products_in_category:
        # There are no goods in the category. This is fine.
        return []

    # We guarantee that List_Products_in_category is a list for .EXTEND ()
    if isinstance(list_products_in_category, str):
        collected_urls: List[str] = [list_products_in_category]
    elif isinstance(list_products_in_category, list):
        collected_urls: List[str] = list_products_in_category
    else:
        # Unexpected type of data, logic and return an empty list
        logger.warning(f'Функция execute_locator вернула неожиданный тип для ссылок на товары: {type(list_products_in_category)}')
        return []

    while True:
        # @todo dangerous situation here. You can go into an endless cycle if the logic of pagination is not impeccable.
        # An attempt to transition to the next page
        pagination_result: Any = _d.execute_locator(_l_pagination_next)
        if not pagination_result:
            # If there is nowhere else to press (the pagination element was not found or the action was not found) - the exit from the cycle.
            break
        
        # Removing links from a new page
        new_links_on_page: List[str] | str | None = _d.execute_locator(_l_product_links)
        if isinstance(new_links_on_page, str):
            collected_urls.append(new_links_on_page)
        elif isinstance(new_links_on_page, list):
            collected_urls.extend(new_links_on_page)
        # If new_Links_on_page is none or an empty list, nothing is added, but the cycle continues (if the pagination was successful)
   
    return collected_urls


def update_categories_in_scenario_file(s: Supplier, scenario_filename: str) -> bool:
    """The function checks the changes in categories on the site and updates the script file.

    Compares the list of categories from the JSON script file with the current list of categories,
    obtained from the website of the supplier. Updates the file, marking remote categories
    And adding new ones.

    Args:
        S (SUPPLIER): Supplier copy (used for `get_list_categories_from_site`, if necessary).
        Scenario_filename (str): the name of the script file (without a path).

    Returns:
        Bool: `true`, if the update was successful or not required changes.
              `False`, if an error has occurred (for example, when reading JSON from the site).
    
    RAISES:
        Filenotfounderror: if the script file is not found (through `j_loads`).
        Requests.exceptions.requestexception: If a network error occurs when the JSON categories are requested.
    
    Example:
        >>> Supplier_instance = ... # initialization of the copy of Supplier
        >>> Filename = 'aliexpress_scenario.json'
        >>> Success = update_categories_in_Scenario_file (Supplier_instance, Filename)
        >>> Print (F'Combination of the script file {"Successfully" If Success Else "did not succeed"}. '"""
    scenario_json: Dict[str, Any]
    scenarios_in_file: Dict[str, Any]
    # Categoris_on_Site: List [dict [str, a man]] # the variable was declared, but was not used in the original code.
    all_ids_in_file: List[str | int]
    categories_from_aliexpress_shop_json: Dict[str, Any]
    groups: List[Dict[str, Any]]
    all_ids_on_site: List[str]
    all_categories_on_site: List[Dict[str, Any]]
    removed_categories: List[str | int]
    added_categories: List[str | int]
    category_id: str | int
    category: List[Dict[str, Any]]
    category_name: str
    category_url: str
    post_subject: str
    post_message: str
    
    scenario_file_path: Path = Path(gs.dir_scenarios, f'{scenario_filename}')
    scenario_json = j_loads(scenario_file_path)

    if not scenario_json: # J_loads will return {} or [] with an error
        logger.error(f'Не удалось загрузить файл сценария: {scenario_file_path}')
        return False

    scenarios_in_file = scenario_json.get('scenarios', {})
    # Categoris_on_Site = get_list_categories_from_site (s, scenario_filename) # This line was in the original, but get_list_categories_from_site does not return what is needed here.

    all_ids_in_file = []
    def _update_all_ids_in_file() -> None:
        """Auxiliary function for extracting ID categories from the script file."""
        _cat_id_on_site: Any
        _url: str
        _cat_extracted_id: str

        for _category_name, _category_data in scenarios_in_file.items():
            _cat_id_on_site = _category_data.get('category ID on site')
            if isinstance(_cat_id_on_site, int) and _cat_id_on_site > 0:
                all_ids_in_file.append(_cat_id_on_site)
            elif isinstance(_cat_id_on_site, str) and _cat_id_on_site.isdigit() and int(_cat_id_on_site) > 0: # Strict processing ID
                 all_ids_in_file.append(int(_cat_id_on_site))
            else:
                _url = _category_data.get('url', '')
                if _url and '.html' in _url and '/' in _url and '_' in _url:
                    try:
                        _cat_extracted_id = _url[_url.rfind('/') + 1 : _url.rfind('.html')].split('_')[1]
                        if _cat_extracted_id.isdigit():
                            _category_data['category ID on site'] = int(_cat_extracted_id)
                            all_ids_in_file.append(int(_cat_extracted_id))
                        else:
                            logger.warning(f'Не удалось извлечь числовой ID из URL: {_url} для категории {_category_name}')
                    except IndexError:
                        logger.warning(f'Структура URL не соответствует ожидаемой для извлечения ID: {_url} для категории {_category_name}')
                else:
                    logger.warning(f'Отсутствует или некорректный URL/ID для категории: {_category_name}')
        # J_dumps (Scenario_json, Scenario_file_path) # Maintaining ID changes from URL to a file if you need to do it at this stage.

    _update_all_ids_in_file()

    shop_categories_json_url: str = scenario_json.get('store', {}).get('shop categories json file', '')
    if not shop_categories_json_url:
        logger.error(f'URL для JSON файла категорий магазина не найден в файле сценария: {scenario_filename}')
        return False

    try:
        response: requests.Response = requests.get(shop_categories_json_url, timeout=10)
        response.raise_for_status() # Checking for http errors (4xx, 5xx)
        categories_from_aliexpress_shop_json = response.json()
    except requests.exceptions.RequestException as ex:
        logger.error(f'Ошибка при запросе JSON категорий с {shop_categories_json_url}', ex, exc_info=True)
        return False
    except requests.exceptions.JSONDecodeError as ex:
        logger.error(f'Ошибка декодирования JSON ответа с {shop_categories_json_url}', ex, exc_info=True)
        return False
    
    # The next code compares the list of categories identifiers All_ids_in_file
    # with Current_categories_json_on_site (renamed Categories_from_ALIEXPRESS_SHOP_JSON)
    # Categories received from the current version of the site in JSON format.
    # From Categories_from_Aliexpress_Shop_JSON, a list of groups of categories is removed.
    # Lists are created by all_ids_on_site and all_categories_on_site for ID and these categories from the site.
    # For each group (and subgroup), ID and data are added to these lists.
    # Then the removd_categories (ID from the file that are absent on the site) are calculated
    # and aded_categories (ID from the site absent in the file).
    
    groups = categories_from_aliexpress_shop_json.get('groups', [])
    all_ids_on_site = []
    all_categories_on_site = [] # List of categories from the site
    
    for group in groups:
        if not group.get('subGroupList'): # Check for void or absence of subgrouplist
            group_id_str: str = str(group.get('groupId'))
            if group_id_str.isdigit():
                all_ids_on_site.append(group_id_str)
                all_categories_on_site.append(group)
        else:
            for subgroup in group.get('subGroupList', []):
                subgroup_id_str: str = str(subgroup.get('groupId'))
                if subgroup_id_str.isdigit():
                    all_ids_on_site.append(subgroup_id_str)
                    all_categories_on_site.append(subgroup)

    # We convert all_ids_in_file to the lines for the correct comparison, because all_ids_on_site lines
    all_ids_in_file_str: List[str] = [str(id_val) for id_val in all_ids_in_file]

    set_all_ids_on_site: set[str] = set(all_ids_on_site)
    set_all_ids_in_file_str: set[str] = set(all_ids_in_file_str)

    removed_categories_str: List[str] = [x for x in all_ids_in_file_str if x not in set_all_ids_on_site]
    added_categories_str: List[str] = [x for x in all_ids_on_site if x not in set_all_ids_in_file_str]

    changes_made: bool = False

    if added_categories_str:
        changes_made = True
        for category_id_str in added_categories_str:
            # Search for ID category among all categories received from the site
            category_data_list: List[Dict[str, Any]] = [c for c in all_categories_on_site if str(c.get('groupId')) == category_id_str]
            if category_data_list:
                category_data: Dict[str, Any] = category_data_list[0]
                category_name = category_data.get('name', f'Категория_{category_id_str}')
                category_url = category_data.get('url', '')
                
                # Adding a new category to Scenarios_in_file
                # Check that we do not overwhelm the existing category with such a name, if the name is not unique
                if category_name not in scenarios_in_file:
                     scenarios_in_file[category_name] = {
                        'category ID on site': int(category_id_str), # Save as int
                        'brand': '', # Default value
                        'active': True,
                        'url': category_url,
                        'condition': '', # Default value
                        'PrestaShop_categories': '' # Default value
                    }
                else:
                    logger.warning(f'Категория с именем "{category_name}" уже существует в файле сценария. Пропуск добавления ID {category_id_str}.')
            else:
                logger.warning(f'Данные для добавленной категории с ID {category_id_str} не найдены на сайте.')

        post_subject = f'Добавлены новые категории в файл {scenario_filename}'
        post_message = f'В файл {scenario_filename} были добавлены новые категории (ID): {", ".join(added_categories_str)}'
        send(post_subject, post_message)

    if removed_categories_str:
        changes_made = True
        for category_id_str in removed_categories_str:
            # Search for category in Scenarios_in_file for deactivation
            # We are looking for the value of 'Category Id on Site'
            for cat_name, cat_data in scenarios_in_file.items():
                if str(cat_data.get('category ID on site')) == category_id_str:
                    cat_data['active'] = False
                    logger.info(f'Категория "{cat_name}" (ID: {category_id_str}) помечена как неактивная в {scenario_filename}.')
                    break # Found and updated, we proceed to the next ID
        
        post_subject = f'Отключены категории в файле {scenario_filename}'
        post_message = f'В файле {scenario_filename} были отключены категории (ID): {", ".join(removed_categories_str)}'
        send(post_subject, post_message)

    if changes_made:
        scenario_json['scenarios'] = scenarios_in_file
        if not j_dumps(scenario_json, scenario_file_path):
             logger.error(f'Не удалось сохранить обновленный файл сценария: {scenario_file_path}')
             return False # An error while maintaining

    return True


def get_list_categories_from_site(s: Supplier, scenario_file: str, brand: str = '') -> List[Dict[str, Any]]:
    """The function extracts a list of categories from the supplier website.
    (Current implementation is a plug and requires improvement).

    Args:
        S (SUPPLIER): A copy of the supplier containing a web drive.
        Scenario_file (str): the name of the script file, may contain the URL pages of categories.
        Brand (str, Optional): The name of the brand for filtering categories (if applicable).
                               By default `''`.

    Returns:
        List [dict [str, a ain]]: a list of dictionaries where each dictionary represents a category.
                              Returns an empty list in case of error or if the category is not found.
    
    Example:
        >>> Supplier_instance = ... # initialization of the copy of Supplier
        >>> Categories = get_list_categories_from_site (Supplier_instance, 'Scenario.json', 'Somebrand')
        >>> for Cat in Categories:
        ... print (Cat.get ('NAME'))"""
    _d: WebDriverInstance = s.driver
    scenario_json: Dict[str, Any]
    shop_categories_page_url: str

    scenario_file_path: Path = Path(gs.dir_scenarios, f'{scenario_file}')
    scenario_json = j_loads(scenario_file_path)

    if not scenario_json:
        logger.error(f'Не удалось загрузить файл сценария {scenario_file} для получения URL страницы категорий.')
        return []

    shop_categories_page_url = scenario_json.get('store', {}).get('shop categories page', '')
    if not shop_categories_page_url:
        logger.error(f'URL страницы категорий магазина не найден в {scenario_file}.')
        return []

    _d.get_url(shop_categories_page_url)
    ...  или дальнейшая логика извлечения категорий с помощью WebDriver
    
    logger.warning('Функция get_list_categories_from_site не реализована полностью и вернула пустой список.')
    return [] # The plug, the real logic of the extraction of categories should be here.

    
