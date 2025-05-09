## \file /sandbox/davidka/experiments/generate_train_data_by_page_type.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Описание вашего модуля.
=========================
Здесь может быть более подробное описание того, что делает этот скрипт.

 ```rst                     
 .. module:: sandbox.davidka.experiments.generate_train_data_by_page_type
 ```
"""

import asyncio
import random
from types import SimpleNamespace
from typing import Optional, Dict, Any 
# -------------------------------------------------------------------
import header
from header import __root__
from src import gs 
from pathlib import Path
from src.utils.file import read_text_file, recursively_yield_file_path
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print
from src.logger.logger import logger 

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    STORAGE: Path
    if config: # Добавлена проверка, что config загрузился
        STORAGE = Path(config.storage)
    else:
        # Обработка случая, если davidka.json не загрузился или не содержит 'storage'
        # logger.error("Не удалось загрузить конфигурацию или отсутствует ключ 'storage'. Установка STORAGE в None.")
        print("Ошибка: Не удалось загрузить конфигурацию или отсутствует ключ 'storage'.")
        STORAGE = None # Или установите путь по умолчанию, или прервите выполнение

    WINDOW_MODE: str = 'headless' # Этот параметр не используется в текущем фрагменте
    GEMINI_API_KEY: Optional[str] = getattr(gs.credentials.gemini.onela, 'api_key', None) if hasattr(gs, 'credentials') and hasattr(gs.credentials, 'gemini') and hasattr(gs.credentials.gemini, 'onela') else None

    GEMINI_MODEL_NAME = 'gemini-2.0-flash-exp' # Используйте актуальное имя модели
    system_instructuction: Optional[str] = read_text_file(ENDPOINT / 'instructions/analize_html.md')
    updated_links_file_name:str =  'updated_links.json'

    DELAY_AFTER_LINK_PROCESSING: int = 15


# ---------------------------------- Определитеь типа содержимого ---------------------------

def get_page_type(value_ns: SimpleNamespace) -> Optional[str]:
    """
    Извлекает значение 'page_type' из SimpleNamespace,
    независимо от того, находится ли оно на верхнем уровне
    или вложено в атрибут 'ai_analized_content'.

    Args:
        value_ns (SimpleNamespace): Входной SimpleNamespace.

    Returns:
        Optional[str]: Значение 'page_type', если найдено, иначе None.
                       Может вернуть пустую строку, если она была значением атрибута.

    Примеры структур (исходные данные могли быть словарями):
        # Структура 1: page_type на верхнем уровне
        # value_ns будет иметь атрибут value_ns.page_type = 'homepage'
        # { 'page_type': 'homepage', ... }

        # Структура 2: page_type во вложенном ai_analized_content
        # value_ns.ai_analized_content.page_type = 'product_page'
        # { "ai_analized_content": {'page_type':'product_page',}, ... }
    """
    page_type_value: Optional[str] = None

    if not isinstance(value_ns, SimpleNamespace):
        # logger.error(f"Ожидался SimpleNamespace, получен {type(value_ns)}")
        return None

    # 1. Попытка извлечь 'page_type' с верхнего уровня
    page_type_value = getattr(value_ns, 'page_type', None)
    if page_type_value is not None: # Найдено (может быть и пустой строкой)
        return page_type_value

    # 2. Попытка извлечь из вложенного 'ai_analized_content'
    # Предполагаем, что j_loads_ns также преобразует вложенные словари в SimpleNamespace
    ai_content_ns: Optional[SimpleNamespace] = getattr(value_ns, 'ai_analized_content', None)
    if isinstance(ai_content_ns, SimpleNamespace):
        page_type_nested: Optional[str] = getattr(ai_content_ns, 'page_type', None)
        if page_type_nested is not None: # Найдено во вложенной структуре
            return page_type_nested
            
    return None # 'page_type' не найден ни на одном из уровней

# ---------------------------------------------------------------------

def get_product_title(value_ns: SimpleNamespace) -> str:
    """
    Извлекает 'product_title' из SimpleNamespace, проверяя несколько мест.
    Возвращает пустую строку, если 'product_title' не найден или сам является пустой строкой.

    Args:
        value_ns (SimpleNamespace): Входной SimpleNamespace.

    Returns:
        str: Значение 'product_title' или пустая строка.
    """
    product_title_found: str = ''

    if not isinstance(value_ns, SimpleNamespace):
        # logger.error(f"Ожидался SimpleNamespace, получен {type(value_ns)}")
        return '' # Возврат пустой строки по умолчанию

    # 1. Попытка получить с верхнего уровня
    title_top: Optional[str] = getattr(value_ns, 'product_title', None)
    # Проверяем, что атрибут существует, он не None и не пустая строка
    if title_top: # Эквивалентно (title_top is not None and title_top != '')
        product_title_found = title_top
    
    # 2. Если на верхнем уровне не нашли (или нашли пустое), ищем во вложенной структуре
    if not product_title_found: # Если product_title_found все еще пустая строка
        ai_content_ns: Optional[SimpleNamespace] = getattr(value_ns, 'ai_analized_content', None)
        
        if isinstance(ai_content_ns, SimpleNamespace):
            nested_title: Optional[str] = getattr(ai_content_ns, 'product_title', None)
            if nested_title: # Эквивалентно (nested_title is not None and nested_title != '')
                product_title_found = nested_title
    
    return product_title_found

# Основной цикл обработки
if Config.STORAGE: # Продолжаем, только если STORAGE определен
    for path in recursively_yield_file_path(Config.STORAGE, ['*.json']):
        if path.stem in ('updated_links', 'processed_internal_links'):
            continue
            
        # Функция j_loads возвращает dict или list
        data: Dict[str, Any] = j_loads(path) 
        if not data: # Проверка, что данные успешно загружены
            # logger.warning(f"Не удалось загрузить данные из файла: {path}")
            print(f"Предупреждение: Не удалось загрузить данные из файла: {path}")
            continue

        products_dict: Dict[str, Any] = {}
        categories_dict: Dict[str, Any] = {}
        others: Dict[str, Any] = {}

        for key, value_dict_from_json in data.items(): # value_dict_from_json здесь все еще словарь
            # print(f'{path.stem=}\n{key=}\n ')
            
            # Преобразуем value (которое является словарем) в SimpleNamespace
            value_ns: Optional[SimpleNamespace] = j_loads_ns(value_dict_from_json)
            
            if not value_ns: # Проверка, что преобразование в SimpleNamespace прошло успешно
                # logger.warning(f"Не удалось преобразовать в SimpleNamespace значение для ключа {key} в файле {path}")
                print(f"Предупреждение: Не удалось преобразовать в SimpleNamespace значение для ключа {key} в файле {path}")
                continue

            # ... (ваш код до ...)

            page_type: Optional[str] = get_page_type(value_ns)
            
            if page_type in ('product', 'category'):
                # ... (ваш код до ...)
                internal_data: Dict[str, Any] = {
                    'html': getattr(value_ns, 'html', ''),
                    'text': getattr(value_ns, 'text', ''),
                    'product_title': get_product_title(value_ns), # Передаем value_ns
                    'meta_og_title': getattr(value_ns, 'meta_og_title', ''),
                    'meta_name_title': getattr(value_ns, 'meta_name_title', ''),
                    'meta_keywords': getattr(value_ns, 'meta_keywords', ''),
                    'meta_description': getattr(value_ns, 'meta_description', ''),
                    'title_tag_content': getattr(value_ns, 'title_tag_content', ''),
                    specification
                    sku
                    summary
                    specification
                    descritpion
                    'product_type': page_type,
                }

                print(internal_data)
                # ... (ваш код после ...)
            # ... (ваш код после ...)
else:
    # logger.error("Переменная Config.STORAGE не определена. Завершение работы.")
    print("Ошибка: Переменная Config.STORAGE не определена. Проверьте конфигурационный файл.")

