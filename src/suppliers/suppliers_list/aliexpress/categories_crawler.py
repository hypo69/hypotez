```python
## \file /src/suppliers/suppliers_list/aliexpress/sceanrio.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль управления категориями для поставщика Aliexpress.
======================================================
Этот модуль содержит функции для взаимодействия с категориями товаров Aliexpress,
включая сбор URL-адресов товаров из категорий и обновление списка категорий
на основе данных с сайта.

```rst
 .. module:: src.suppliers.suppliers_list.aliexpress.sceanrio
    :platform: Windows, Unix
    :synopsis: управление категориями aliexpress
```
"""

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
    """
    Placeholder for a function that sends notifications (e.g., email).

    Args:
        subject (str): Тема сообщения.
        message (str): Текст сообщения.
    """
    logger.info(f'Функция send вызвана с темой: {subject} и сообщением: {message}')
    # Реальная логика отправки должна быть здесь


def get_list_products_in_category(s: Supplier) -> List[str]:
    """  
    Функция считывает URL товаров со страницы категории.

    Если есть несколько страниц с товарами в одной категории - функция пролистывает все.
    Важно понимать, что к этому моменту вебдрайвер уже должен был открыть страницу категорий.

    Args:
        s (Supplier): Экземпляр поставщика, содержащий драйвер и локаторы.

    Returns:
        List[str]: Список собранных URL-адресов товаров. Может быть пустым, если
                   в исследуемой категории нет товаров.
    
    Example:
        >>> supplier_instance = ... # Инициализация экземпляра Supplier
        >>> product_urls = get_list_products_in_category(supplier_instance)
        >>> if product_urls:
        ...     print(f'Найдено {len(product_urls)} URL товаров.')
    """
    
    return get_prod_urls_from_pagination (s)
        

def get_prod_urls_from_pagination(s: Supplier) -> List[str]:
    """
    Функция собирает ссылки на товары со страницы категории с перелистыванием страниц.
    
    Args:
        s (Supplier): Экземпляр поставщика, содержащий `driver` и `locators`.
    
    Returns:
        List[str]: Список ссылок, собранных со страницы категории.
                   Возвращает пустой список, если товары не найдены.
    
    Example:
        >>> supplier_instance = ... # Инициализация экземпляра Supplier
        >>> urls = get_prod_urls_from_pagination(supplier_instance)
        >>> print(urls)
    """
    
    _d: WebDriverInstance = s.driver
    _l_product_links: LocatorType = s.locators['category']['product_links']
    _l_pagination_next: LocatorType = s.locators['category']['pagination']['->']
    
    list_products_in_category: List[str] | str | None
    
    # Извлечение ссылок с первой страницы
    list_products_in_category = _d.execute_locator(_l_product_links)
    
    if not list_products_in_category:
        # В категории нет товаров. Это нормально.
        return []

    # Гарантируем, что list_products_in_category является списком для .extend()
    if isinstance(list_products_in_category, str):
        collected_urls: List[str] = [list_products_in_category]
    elif isinstance(list_products_in_category, list):
        collected_urls: List[str] = list_products_in_category
    else:
        # Неожиданный тип данных, логируем и возвращаем пустой список
        logger.warning(f'Функция execute_locator вернула неожиданный тип для ссылок на товары: {type(list_products_in_category)}')
        return []

    while True:
        # @todo Опасная ситуация здесь. Можно уйти в бесконечный цикл, если логика пагинации не безупречна.
        # Попытка перехода на следующую страницу
        pagination_result: Any = _d.execute_locator(_l_pagination_next)
        if not pagination_result:
            # Если больше некуда нажимать (элемент пагинации не найден или действие не удалось) - выход из цикла.
            break
        
        # Извлечение ссылок с новой страницы
        new_links_on_page: List[str] | str | None = _d.execute_locator(_l_product_links)
        if isinstance(new_links_on_page, str):
            collected_urls.append(new_links_on_page)
        elif isinstance(new_links_on_page, list):
            collected_urls.extend(new_links_on_page)
        # Если new_links_on_page is None или пустой список, ничего не добавляется, но цикл продолжается (если пагинация была успешной)
   
    return collected_urls


def update_categories_in_scenario_file(s: Supplier, scenario_filename: str) -> bool:
    """
    Функция проверяет изменения категорий на сайте и обновляет файл сценария.

    Сравнивает список категорий из файла сценария JSON с актуальным списком категорий,
    полученным с сайта поставщика. Обновляет файл, отмечая удаленные категории
    и добавляя новые.

    Args:
        s (Supplier): Экземпляр поставщика (используется для `get_list_categories_from_site`, если необходимо).
        scenario_filename (str): Имя файла сценария (без пути).

    Returns:
        bool: `True`, если обновление прошло успешно или не требовалось изменений.
              `False`, если произошла ошибка (например, при чтении JSON с сайта).
    
    Raises:
        FileNotFoundError: Если файл сценария не найден (через `j_loads`).
        requests.exceptions.RequestException: Если происходит ошибка сети при запросе JSON категорий.
    
    Example:
        >>> supplier_instance = ... # Инициализация экземпляра Supplier
        >>> filename = 'aliexpress_scenario.json'
        >>> success = update_categories_in_scenario_file(supplier_instance, filename)
        >>> print(f'Обновление файла сценария {"успешно" if success else "не удалось"}.')
    """
    scenario_json: Dict[str, Any]
    scenarios_in_file: Dict[str, Any]
    # categoris_on_site: List[Dict[str, Any]] # Переменная была объявлена, но не использовалась в оригинальном коде.
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

    if not scenario_json: # j_loads вернет {} или [] при ошибке
        logger.error(f'Не удалось загрузить файл сценария: {scenario_file_path}')
        return False

    scenarios_in_file = scenario_json.get('scenarios', {})
    # categoris_on_site = get_list_categories_from_site(s, scenario_filename) # Эта строка была в оригинале, но get_list_categories_from_site не возвращает то, что здесь нужно.

    all_ids_in_file = []
    def _update_all_ids_in_file() -> None:
        """Вспомогательная функция для извлечения ID категорий из файла сценария."""
        _cat_id_on_site: Any
        _url: str
        _cat_extracted_id: str

        for _category_name, _category_data in scenarios_in_file.items():
            _cat_id_on_site = _category_data.get('category ID on site')
            if isinstance(_cat_id_on_site, int) and _cat_id_on_site > 0:
                all_ids_in_file.append(_cat_id_on_site)
            elif isinstance(_cat_id_on_site, str) and _cat_id_on_site.isdigit() and int(_cat_id_on_site) > 0: # Обработка строковых ID
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
        # j_dumps(scenario_json, scenario_file_path) # Сохранение изменений ID из URL в файл, если это необходимо сделать на этом этапе.

    _update_all_ids_in_file()

    shop_categories_json_url: str = scenario_json.get('store', {}).get('shop categories json file', '')
    if not shop_categories_json_url:
        logger.error(f'URL для JSON файла категорий магазина не найден в файле сценария: {scenario_filename}')
        return False

    try:
        response: requests.Response = requests.get(shop_categories_json_url, timeout=10)
        response.raise_for_status() # Проверка на HTTP ошибки (4xx, 5xx)
        categories_from_aliexpress_shop_json = response.json()
    except requests.exceptions.RequestException as ex:
        logger.error(f'Ошибка при запросе JSON категорий с {shop_categories_json_url}', ex, exc_info=True)
        return False
    except requests.exceptions.JSONDecodeError as ex:
        logger.error(f'Ошибка декодирования JSON ответа с {shop_categories_json_url}', ex, exc_info=True)
        return False
    
    # Следующий код производит сравнение списка идентификаторов категорий all_ids_in_file
    # с current_categories_json_on_site (переименовано в categories_from_aliexpress_shop_json),
    # идентификаторами категорий, полученными с текущей версии сайта в формате JSON.
    # Из categories_from_aliexpress_shop_json извлекается список групп категорий.
    # Создаются списки all_ids_on_site и all_categories_on_site для ID и данных категорий с сайта.
    # Для каждой группы (и подгруппы) ID и данные добавляются в эти списки.
    # Затем вычисляются removed_categories (ID из файла, отсутствующие на сайте)
    # и added_categories (ID с сайта, отсутствующие в файле).
    
    groups = categories_from_aliexpress_shop_json.get('groups', [])
    all_ids_on_site = []
    all_categories_on_site = [] # Список словарей категорий с сайта
    
    for group in groups:
        if not group.get('subGroupList'): # Проверка на пустоту или отсутствие subGroupList
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

    # Преобразуем all_ids_in_file к строкам для корректного сравнения, т.к. all_ids_on_site строки
    all_ids_in_file_str: List[str] = [str(id_val) for id_val in all_ids_in_file]

    set_all_ids_on_site: set[str] = set(all_ids_on_site)
    set_all_ids_in_file_str: set[str] = set(all_ids_in_file_str)

    removed_categories_str: List[str] = [x for x in all_ids_in_file_str if x not in set_all_ids_on_site]
    added_categories_str: List[str] = [x for x in all_ids_on_site if x not in set_all_ids_in_file_str]

    changes_made: bool = False

    if added_categories_str:
        changes_made = True
        for category_id_str in added_categories_str:
            # Поиск категории по ID среди всех категорий, полученных с сайта
            category_data_list: List[Dict[str, Any]] = [c for c in all_categories_on_site if str(c.get('groupId')) == category_id_str]
            if category_data_list:
                category_data: Dict[str, Any] = category_data_list[0]
                category_name = category_data.get('name', f'Категория_{category_id_str}')
                category_url = category_data.get('url', '')
                
                # Добавление новой категории в scenarios_in_file
                # Убедимся, что не перезаписываем существующую категорию с таким именем, если имя не уникально
                if category_name not in scenarios_in_file:
                     scenarios_in_file[category_name] = {
                        'category ID on site': int(category_id_str), # Сохраняем как int
                        'brand': '', # Значение по умолчанию
                        'active': True,
                        'url': category_url,
                        'condition': '', # Значение по умолчанию
                        'PrestaShop_categories': '' # Значение по умолчанию
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
            # Поиск категории в scenarios_in_file для деактивации
            # Ищем по значению 'category ID on site'
            for cat_name, cat_data in scenarios_in_file.items():
                if str(cat_data.get('category ID on site')) == category_id_str:
                    cat_data['active'] = False
                    logger.info(f'Категория "{cat_name}" (ID: {category_id_str}) помечена как неактивная в {scenario_filename}.')
                    break # Нашли и обновили, переходим к следующему ID
        
        post_subject = f'Отключены категории в файле {scenario_filename}'
        post_message = f'В файле {scenario_filename} были отключены категории (ID): {", ".join(removed_categories_str)}'
        send(post_subject, post_message)

    if changes_made:
        scenario_json['scenarios'] = scenarios_in_file
        if not j_dumps(scenario_json, scenario_file_path):
             logger.error(f'Не удалось сохранить обновленный файл сценария: {scenario_file_path}')
             return False # Ошибка при сохранении

    return True


def get_list_categories_from_site(s: Supplier, scenario_file: str, brand: str = '') -> List[Dict[str, Any]]:
    """
    Функция извлекает список категорий с сайта поставщика.
    (Текущая реализация является заглушкой и требует доработки).

    Args:
        s (Supplier): Экземпляр поставщика, содержащий веб-драйвер.
        scenario_file (str): Имя файла сценария, может содержать URL страницы категорий.
        brand (str, optional): Название бренда для фильтрации категорий (если применимо).
                               По умолчанию `''`.

    Returns:
        List[Dict[str, Any]]: Список словарей, где каждый словарь представляет категорию.
                              Возвращает пустой список в случае ошибки или если категории не найдены.
    
    Example:
        >>> supplier_instance = ... # Инициализация экземпляра Supplier
        >>> categories = get_list_categories_from_site(supplier_instance, 'scenario.json', 'SomeBrand')
        >>> for cat in categories:
        ...     print(cat.get('name'))
    """
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
    ... # Точка останова или дальнейшая логика извлечения категорий с помощью WebDriver
    
    logger.warning('Функция get_list_categories_from_site не реализована полностью и вернула пустой список.')
    return [] # Заглушка, реальная логика извлечения категорий должна быть здесь.

    
