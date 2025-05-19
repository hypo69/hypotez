## \file /sandbox/davidka/experiments/generate_train_data_by_page_type.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для генерации обучающих данных на основе типа страницы.
================================================================
Скрипт обрабатывает JSON-файлы, извлекает структурированную информацию
о товарах и категориях, включая метаданные, описания и другие атрибуты.
Данные извлекаются из словарей (dict), проверяя несколько возможных
мест их нахождения: на верхнем уровне или во вложенном объекте 'ai_analized_content'.
Поддерживает выбор API-ключа Gemini через аргумент командной строки.

 ```rst
 .. module:: sandbox.davidka.experiments.generate_train_data_by_page_type
 ```
"""
import re
import sys
import argparse # Добавлено для парсинга аргументов командной строки
from pathlib import Path
from types import SimpleNamespace 
from typing import Optional, Dict, Any, List, Union 

# -------------------------------------------------------------------
import header
from header import __root__
from src import gs
from src.llm.gemini import GoogleGenerativeAi
from src.webdriver import driver
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from SANDBOX.davidka.graber import extract_page_data # Предполагается, что этот путь корректен
from src.utils.file import read_text_file, recursively_yield_file_path, get_directory_names
from src.utils.url import extract_pure_domain
from src.utils.jjson import j_loads, j_dumps, j_loads_ns
from src.utils.csv import save_csv_file
from src.utils.printer import pprint as print
from src.logger.logger import logger

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json') # Загрузка конфигурации из JSON
    STORAGE: Path = Path(config.local_storage.storage) if config.actual_storage == 'local_storage' else Path(config.google_drive.storage)
    TRAIN_STORAGE: Path = STORAGE / 'train_data' # Папка для хранения обучающих данных
    SOURCE_DIRS:list[Path] = [
                                STORAGE / 'data_by_supplier_it', 
                                STORAGE / 'data_by_supplier_de', 
                                STORAGE / 'data_by_supplier_pl', 
                                STORAGE/'data_by_supplier_set_1 DONT TOUCH!'
                            ] 

    updated_links_file_name: str = 'updated_links.json'


    # список возможных категорий вебстраниц
    error: List[Dict[str, Any]] = []               # 0
    home: List[Dict[str, Any]] = []                # 1
    category: List[Dict[str, Any]] = []            # 2
    product_category: List[Dict[str, Any]] = []    # 3
    product: List[Dict[str, Any]] = []             # 4
    collection: List[Dict[str, Any]] = []          # 5
    brand: List[Dict[str, Any]] = []               # 6
    supplier: List[Dict[str, Any]] = []            # 7
    about_us: List[Dict[str, Any]] = []            # 8
    profile: List[Dict[str, Any]] = []             # 9
    contact: List[Dict[str, Any]] = []             # 10
    terms: List[Dict[str, Any]] = []               # 11
    privacy_policy: List[Dict[str, Any]] = []      # 12
    faq: List[Dict[str, Any]] = []                 # 13
    manuals: List[Dict[str, Any]] = []             # 14
    information: List[Dict[str, Any]] = []         # 15
    document: List[Dict[str, Any]] = []            # 16
    description: List[Dict[str, Any]] = []         # 17
    distributors: List[Dict[str, Any]] = []        # 18
    service: List[Dict[str, Any]] = []             # 19
    support: List[Dict[str, Any]] = []             # 20
    download: List[Dict[str, Any]] = []            # 21
    article: List[Dict[str, Any]] = []             # 22
    blog: List[Dict[str, Any]] = []                # 23
    newsletter: List[Dict[str, Any]] = []          # 24
    forum: List[Dict[str, Any]] = []               # 25
    community: List[Dict[str, Any]] = []           # 25 (совмещено с forum/webinar)
    events: List[Dict[str, Any]] = []              # 29
    careers: List[Dict[str, Any]] = []             # 30
    glossary: List[Dict[str, Any]] = []            # 31
    links: List[Dict[str, Any]] = []               # 28
    library: List[Dict[str, Any]] = []             # 32
    media: List[Dict[str, Any]] = []               # 33
    sitemap: List[Dict[str, Any]] = []             # 26
    search_results: List[Dict[str, Any]] = []      # 27
    unknown: List[Dict[str, Any]] = []             # 36

    

    page_categories: dict = {
    # Ошибка
    'error': 0,

    # Главная страница
    'home': 1,
    'home_page': 1,
    'home page': 1,

    # Категории и товары
    'category': 2,
    'product_category': 3,
    'product category': 3,
    'product category page': 3,
    'productcategory': 3,
    'productcategorypage': 3,
    'product': 4,
    'collection': 5,

    # Бренды и поставщики
    'brand': 6,
    'brand_name': 6,
    'brand name': 6,
    'supplier': 7,
    'supplier_name': 7,
    'supplier name': 7,

    # О компании
    'about_us': 8,
    'about us': 8,
    'about': 8,
    'profile': 9,

    # Контакты
    'contact': 10,
    'contact_page': 10,
    'contact page': 10,

    # Юридическая информация и политика
    'terms': 11,
    'privacy_policy': 12,
    'privacy policy': 12,
    'policy': 12,

    # Поддержка и техдокументация
    'faq': 13,
    'manuals': 14,
    'information': 15,
    'document': 16,
    'description': 17,
    'distributors': 18,
    'service': 19,
    'services': 19,
    'support': 20,
    'support_page': 20,
    'supportpage': 20,

    # Загрузка
    'download': 21,
    'downloads': 21,
    'download_page': 21,
    'download page': 21,
    'downloadpage': 21,
    'application': 21,

    # Контент и новости
    'article': 22,
    'blog': 23,
    'newsletter': 24,
    'newsroom': 24,
    'newspage': 24,
    'news': 24,

    # Сообщество
    'forum': 25,
    'webinar': 25,
    'community': 25,

    # Навигация и поиск
    'sitemap': 26,
    'search_results': 27,
    'search results': 27,
    'searchresult': 27,
    'search result': 27,
    'searchresultpage': 27,
    'searchresults': 27,
    'searchresultspage': 27,
    'search': 27,
    'searchpage': 27,
    'search page': 27,
    'links': 28,

    # События и вакансии
    'event': 29,
    'events': 29,
    'auction': 29,
    'careers': 30,

    # Разное и справка
    'glossary': 31,
    'library': 32,
    'media': 33,
    'member': 34,
    'other': 35,

    # Неопознанное
    'unknown': 36,
    }

    labels_for_train_data:dict = {} # <- метки для модели 

    rejected_page_types:list = [
    'error', 
    'error_page',
    'error page',
    'errorpage',
    'login',
    'loginpage',
    'sign_in',
    'signin',
    'sign_in_page',
    'signinpage',
    'shopping_card',
    'shoppingcard',
    'shoppingcardpage',
    'shoppingcard_page',
    'shoppingcart',
    'cart',
    'search',
    'socialmedia',
    'dataset',
    ]



# ---------------------------------- Вспомогательные функции извлечения данных ---------------------------

def _get_string_attribute_from_dict_or_ai_content(value_dict: Dict[str, Any], attribute_name: str) -> str:
    """
    Извлекает строковый атрибут из словаря, проверяя верхний уровень,
    а затем вложенный 'ai_analized_content'. Атрибут конвертируется в строку.

    Args:
        value_dict (Dict[str, Any]): Входной словарь.
        attribute_name (str): Имя извлекаемого атрибута.

    Returns:
        str: Значение атрибута в виде строки или пустая строка, если не найдено,
             None, или значение пусто после конвертации и очистки.
    """
    final_value_str: str = ''
    top_level_value: Optional[Any] = None
    current_value_str: str = ''
    ai_content_dict: Optional[Dict[str, Any]] = None
    nested_value: Optional[Any] = None
    current_nested_value_str: str = ''

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция _get_string_attribute_from_dict_or_ai_content: ожидался dict для '{attribute_name}', получен {type(value_dict)}")
        return ''

    top_level_value = value_dict.get(attribute_name)

    if top_level_value is not None:
        if isinstance(top_level_value, str):
            current_value_str = top_level_value.strip()
        else:
            try:
                current_value_str = str(top_level_value).strip()
            except Exception as ex:
                logger.debug(f"Функция _get_string_attribute_from_dict_or_ai_content: ошибка конвертации в строку для '{attribute_name}' (верхний уровень): {top_level_value}", ex)
                current_value_str = ''

    if current_value_str:
        final_value_str = current_value_str

    if not final_value_str:
        ai_content_dict_val = value_dict.get('ai_analized_content') # Используем другую переменную, чтобы не конфликтовать с именем параметра
        if isinstance(ai_content_dict_val, dict):
            nested_value = ai_content_dict_val.get(attribute_name)

            if nested_value is not None:
                if isinstance(nested_value, str):
                    current_nested_value_str = nested_value.strip()
                else:
                    try:
                        current_nested_value_str = str(nested_value).strip()
                    except Exception as ex:
                        logger.debug(f"Функция _get_string_attribute_from_dict_or_ai_content: ошибка конвертации в строку для '{attribute_name}' (ai_analized_content): {nested_value}", ex)
                        current_nested_value_str = ''

            if current_nested_value_str:
                final_value_str = current_nested_value_str

    return final_value_str

def _get_optional_attribute_as_str_dict_or_ai(value_dict: Dict[str, Any], attribute_name: str) -> Optional[str]:
    """
    Извлекает атрибут из словаря (верхний уровень или ai_analized_content),
    конвертирует в строку (если не None и не пустая строка после strip). Возвращает Optional[str].
    """
    val_found: Optional[Any] = None
    # ai_content_dict: Optional[Dict[str, Any]] = None # Не используется в этой версии
    str_val: str = ''

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция _get_optional_attribute_as_str_dict_or_ai: ожидался dict для '{attribute_name}', получен {type(value_dict)}")
        return None

    val_found = value_dict.get(attribute_name)

    if val_found is None:
        ai_content_val = value_dict.get('ai_analized_content')
        if isinstance(ai_content_val, dict):
            val_found = ai_content_val.get(attribute_name)

    if val_found is not None:
        try:
            str_val = str(val_found).strip()
            return str_val if str_val else None
        except Exception as ex:
            logger.debug(f"Функция _get_optional_attribute_as_str_dict_or_ai: ошибка конвертации в строку для '{attribute_name}': {val_found}", ex)
            return None
    return None


def get_meta_keywords_str(value_dict: Dict[str, Any]) -> str:
    """
    Извлекает 'meta_keywords', проверяя value_dict и value_dict.get('ai_analized_content').
    Если значение является списком, объединяет его элементы в строку через ', '.
    Если строка, возвращает ее (очищенную). Иначе пустую строку.
    """
    keywords_result_str: str = ''
    raw_keywords: Optional[Any] = None
    processed_keywords: List[str] = []

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция get_meta_keywords_str: ожидался dict, получен {type(value_dict)}")
        return ''

    raw_keywords = value_dict.get('meta_keywords')
    if raw_keywords is None:
        ai_content_val = value_dict.get('ai_analized_content')
        if isinstance(ai_content_val, dict):
            raw_keywords = ai_content_val.get('meta_keywords')

    if raw_keywords is not None:
        if isinstance(raw_keywords, list):
            processed_keywords = [str(kw).strip() for kw in raw_keywords if kw is not None and str(kw).strip()]
            if processed_keywords:
                keywords_result_str = ', '.join(processed_keywords)
        elif isinstance(raw_keywords, str):
            keywords_result_str = raw_keywords.strip()
        else:
            try:
                keywords_result_str = str(raw_keywords).strip()
            except Exception as ex:
                logger.debug(f"Функция get_meta_keywords_str: ошибка конвертации в строку: {raw_keywords}", ex)
                keywords_result_str = ''
    return keywords_result_str

# ---------------------------------- Функции-геттеры для полей ------------------------------------

def get_page_type(value_dict: Dict[str, Any]) -> Optional[str]:
    """
    Извлекает значение 'page_type' из словаря,
    проверяя верхний уровень, а затем вложенный 'ai_analized_content'.
    """
    page_type_val: Optional[Any] = None
    # ai_content_dict: Optional[Dict[str, Any]] = None # Не используется
    page_type_nested: Optional[Any] = None

    if not isinstance(value_dict, dict):
        logger.warning(f"Функция get_page_type: ожидался dict, получен {type(value_dict)}")
        return None

    page_type_val = value_dict.get('page_type')
    if page_type_val is not None:
        return str(page_type_val)

    ai_content_val = value_dict.get('ai_analized_content')
    if isinstance(ai_content_val, dict):
        page_type_nested = ai_content_val.get('page_type')
        if page_type_nested is not None:
            return str(page_type_nested)
    return None

def get_product_title(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'product_title', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'product_title')

def get_meta_og_title(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'meta_og_title', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'meta_og_title')

def get_meta_name_title(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'meta_name_title', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'meta_name_title')

def get_meta_description(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'meta_description', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'meta_description')

def get_title_tag_content(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'title_tag_content', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'title_tag_content')

def get_specification(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'specification', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'specification')

def get_sku(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'sku', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'sku')

def get_price(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'price', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'price')

def get_summary(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'summary', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'summary')

def get_description(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'description', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'description')

def get_ai_content_object(value_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Функция извлекает объект 'ai_analized_content' из словаря,
    если он существует и является словарем.
    """
    ai_content_obj: Optional[Any] = None
    if not isinstance(value_dict, dict):
        logger.warning(f"Функция get_ai_content_object: ожидался dict, получен {type(value_dict)}")
        return None

    ai_content_obj = value_dict.get('ai_analized_content')
    if isinstance(ai_content_obj, dict):
        return ai_content_obj
    elif ai_content_obj is not None:
        logger.debug(f"Функция get_ai_content_object: ключ 'ai_analized_content' найден, но значение не является dict (тип: {type(ai_content_obj)})")
    return None

def get_category(value_dict: Dict[str, Any]) -> str:
    """
    Функция извлекает категорию, проверяя ключи 'category', а затем 'category_name'.
    """
    category_val: str = ''
    category_val = _get_string_attribute_from_dict_or_ai_content(value_dict, 'category')
    if category_val:
        return category_val
    category_val = _get_string_attribute_from_dict_or_ai_content(value_dict, 'category_name')
    return category_val

def get_parent_category(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'parent_category', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'parent_category')

def get_featured_products(value_dict: Dict[str, Any]) -> str:
    """Функция извлекает 'featured_products', используя общую логику."""
    return _get_string_attribute_from_dict_or_ai_content(value_dict, 'featured_products')

# ---------------------------------- Основная логика ------------------------------------
def _create_page_data_object(value_dict: Dict[str, Any], page_type_str: Optional[str], original_url: str) -> Dict[str, Any]:
    """
    Создает стандартизированный словарь с данными страницы.
    """
    processed_page_type_str: str = page_type_str if page_type_str is not None else ''
    supplier_domain = extract_pure_domain(original_url) or "unknown_supplier"

    return {
        'html': value_dict.get('html', ''),
        'text': value_dict.get('text', ''),
        'title': get_product_title(value_dict),
        'meta_og_title': get_meta_og_title(value_dict),
        'meta_name_title': get_meta_name_title(value_dict),
        'meta_keywords': get_meta_keywords_str(value_dict),
        'meta_description': get_meta_description(value_dict),
        'title_tag_content': get_title_tag_content(value_dict),
        'supplier': supplier_domain,
        'price': get_price(value_dict),
        'specification': get_specification(value_dict),
        'sku': get_sku(value_dict),
        'summary': get_summary(value_dict),
        'description': get_description(value_dict),
        'page_type': processed_page_type_str,
        'ai_analized_content': get_ai_content_object(value_dict), # Может быть dict или None
        'category': get_category(value_dict),
        'parent_category': get_parent_category(value_dict),
        'featured_products': get_featured_products(value_dict),
        'original_internal_url': original_url,
    }

def generate_train_data(source_dirs: Optional[list[str, Path] | str | Path] = None) -> bool:
    """
    Загружает JSON-файлы и сохраняет соответствующие секции в TRAIN_STORAGE.

    Если вложенный ключ (секция) не входит в список известных — сохраняет в 'unknown'.
    Данные сохраняются порционно: как только накопится 200 записей в категории — они сбрасываются в файл.
    """
    list_for_csv_llm_data:list = []
    known_sections = {
        "product", "category", "about_us", "contact", "manuals", "about",
        "article", "information", "home", "description",
        "distributors", "service", "faq", "blog", "error","error page"
    }

    buffer: dict[str, list] = {section: [] for section in known_sections}
    buffer["unknown"] = []

    chunk_counters: dict[str, int] = {section: 0 for section in buffer}
    timestamp: str = gs.now
    
    def flush(section: str):
        """Сохраняет текущий буфер категории и очищает его."""
        return True # <~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG!
        nonlocal buffer, chunk_counters, timestamp
        dict_to_save:dict = {}

        if not buffer[section]:
            logger.warning(f'Empty buffer')
            return

        buffer[section] = buffer[section] if isinstance(buffer[section], list) else [buffer[section]]
        for item in buffer[section]:
            dict_to_save.update(item)
            
        out_path = Config.TRAIN_STORAGE / section / f'{timestamp}_{chunk_counters[section]}.json'
        if not j_dumps(dict_to_save, out_path):
            logger.error(f"Ошибка сохранения чанка {chunk_counters[section]} секции {section}", None, True)
        logger.success(f'Успешно сохранен {out_path}')
        chunk_counters[section] += 1
        buffer[section].clear()

    source_dirs: list = (
        source_dirs if isinstance(source_dirs, list)
        else [source_dirs] if source_dirs
        else Config.SOURCE_DIRS if isinstance(Config.SOURCE_DIRS, list)
        else [Config.SOURCE_DIRS]
    )

    for _d in source_dirs:
        suppliers_dirs: list = get_directory_names(_d)
        for supplier_dir in suppliers_dirs:
            for _file in recursively_yield_file_path(_d / supplier_dir, ['*.json']):

                data_from_input_file: Optional[Dict[str, Any]] = j_loads(_file)

                if not data_from_input_file:
                    logger.warning(f'generate_train_data: Нет данных или не удалось загрузить: {_file}.\nБудет изменен суффикс на `.sanitized`')
                    try:
                        sanitized_path = _file.with_suffix(_file.suffix + '.sanitized')
                        sanitized_path.write_text(_file.read_text(encoding='utf-8'), encoding='utf-8')
                        _file.unlink()
                    except Exception as ex:
                        logger.error(f'\n\nНе удалось сохранить и переименовать файл {_file} → {sanitized_path}\n\n', ex, False)
                    continue

                for url, section_dict in data_from_input_file.items():
                    if not isinstance(section_dict, dict):
                        logger.warning(f'generate_train_data: Данные по ключу {url} не являются dict в {_file}')
                        continue

                    page_type:str = section_dict.get("page_type") or "unknown"
                    page_type = re.sub(r'[^a-zA-Z0-9_]', '', page_type)
                    if _file.stem.lower() == _file.parent.name.lower(): page_type = 'home'
                    folder:str = page_type if page_type in known_sections else "unknown"
                    data_by_page_type:dict = _create_page_data_object(section_dict,page_type,url)
                    res_dict:dict = {url:data_by_page_type}
                    buffer[folder].append(res_dict)
                    if page_type not in Config.rejected_page_types:
                        category_number:int = Config.page_categories.get(page_type, 0)
                        if category_number and category_number in Config.page_categories.values():
                            text_data = data_by_page_type['html'] or  data_by_page_type['text']
                            if text_data:
                                list_for_csv_llm_data.append({
                                                            'text':text_data, 
                                                            'labels':category_number,
                                                            })

                        else:
                            logger.debug(f'\n\n\t\tНераспознанный тип вебстраницы:\n{page_type}\n\n\n')
                            ...

                    if len(buffer[folder]) >= 200:
                        flush(folder)
                        buffer[folder] = []
                        processed_file_path:Path = Config.TRAIN_STORAGE / f'llam_{gs.now}'
                        if list_for_csv_llm_data:
                            # if save_csv_file(list_for_csv_llm_data, f'{processed_file_path}.csv'):
                            #     logger.success(f'/nФайл CSV успешно сохранен.\n')
                            if j_dumps(list_for_csv_llm_data, f'{processed_file_path}.json'):
                                logger.success(f'/nФайл JSON успешно сохранен.\n')

                        list_for_csv_llm_data = []


    # Сохраняем остатки
    for section in buffer:
        flush(section)

        processed_file_path:Path = Config.TRAIN_STORAGE / f'llam_{gs.now}'
        if list_for_csv_llm_data:
            # if save_csv_file(list_for_csv_llm_data, f'{processed_file_path}.csv'):
            #     logger.success(f'/nФайл CSV успешно сохранен.\n')
            if j_dumps(list_for_csv_llm_data, f'{processed_file_path}.json'):
                logger.success(f'/nФайл JSON успешно сохранен.\n')

            list_for_csv_llm_data = []
    
    return True


if __name__ == '__main__':
    generate_train_data()
