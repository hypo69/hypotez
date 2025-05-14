## \file /sandbox/davidka/3_process_internal_links.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для обработки директорий проектов и сбора данных о категориях.
======================================================================
Функциональность включает:
1. Переименование директорий проектов:
   Скрипт анализирует файлы `processed_links.json` в поддиректориях.
   Если в файле не найдено записей с `page_type` равным 'product',
   соответствующая директория переименовывается добавлением префикса '_'.
2. Сбор и обновление списка категорий:
   Скрипт извлекает названия категорий (`parent_category`, `category_name`)
   из JSON-файлов в указанных директориях-источниках.
   Собранные категории объединяются с существующим списком известных категорий,
   дедуплицируются, перемешиваются и сохраняются обратно в файл.

Конфигурация для путей и источников данных управляется через класс `Config`.

 ```rst
 .. module:: sandbox.davidka.3_process_internal_links
 ```
"""


import argparse
from pathlib import Path
import random
from typing import Dict, Any, List, Optional, Tuple # Added Tuple for _count_product_page_types
from types import SimpleNamespace
import sys
import time
from datetime import datetime

# Стандартные импорты проекта
import header
from header import __root__
from src import gs

# --- Импорты WebDriver ---
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
# -------------------------
from src.llm.gemini import GoogleGenerativeAi
# -------------------------
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import get_filenames_from_directory, get_directory_names, read_text_file, recursively_yield_file_path # Added recursively_yield_file_path
from src.logger import logger
from src.utils.printer import pprint as print # Используется как print
from SANDBOX.davidka.graber import extract_page_data # Предполагается, что этот модуль существует

class Config:
    """Класс конфигурации скрипта."""

    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    LANG_CODE: str = 'it'  # Язык для обработки данных
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    # 'local_storage' or 'google_drive'  <- ГДЕ НАХОДИТСЯ ХРАНИЛИЩЕ
    actual_storage: str = 'local_storage' 
    STORAGE: Path = Path(config.local_storage.storage) if actual_storage == 'local_storage' else Path(config.google_drive.storage)
    WORK_DIR: Path = Path(STORAGE / f'data_by_supplier_{LANG_CODE}')
    WINDOW_MODE: str = 'headless'
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL_NAME: str = config.gemini_model_name
    system_instructuction: Optional[str] = read_text_file(ENDPOINT / 'instructions' / 'analize_html.md')
    processed_internal_links_file_name: str = 'processed_links.json'
    DELAY_AFTER_LINK_PROCESSING: int = 15

def initialize_llm(username: str) -> Optional[GoogleGenerativeAi]:
    """
    Инициализирует инстанс GoogleGenerativeAi.

    Args:
        username (str): Имя пользователя для получения API ключа.

    Returns:
        Optional[GoogleGenerativeAi]: Инстанс LLM или None в случае ошибки.
    """
    llm_instance: Optional[GoogleGenerativeAi] = None
    user_gemini_config: Optional[SimpleNamespace] = None

    try:
        user_gemini_config = getattr(gs.credentials.gemini, username)
        Config.GEMINI_API_KEY = getattr(user_gemini_config, 'api_key')
        if not Config.GEMINI_API_KEY: 
             logger.critical(f"Ошибка: API ключ для пользователя '{username}' пустой.")
             return None
        logger.info(f"Успешно получен и установлен Gemini API ключ для пользователя: '{username}'")
    except AttributeError:
        logger.critical(f"Ошибка: не удалось найти конфигурацию или API ключ для пользователя '{username}'.")
        return None
    
    if not Config.system_instructuction:
        logger.warning("Системная инструкция для LLM не загружена. LLM может работать некорректно или не будет использован для анализа.")

    try:
        llm_instance = GoogleGenerativeAi(
            api_key=Config.GEMINI_API_KEY, 
            model_name=Config.GEMINI_MODEL_NAME,
            generation_config={'response_mime_type': 'application/json'},
            system_instruction=Config.system_instructuction 
        )
        logger.info("Инстанс GoogleGenerativeAi успешно инициализирован.")
        return llm_instance
    except Exception as ex:
        logger.critical(f"Не удалось инициализировать GoogleGenerativeAi: {ex}", ex, exc_info=True)
        return None


def initialize_driver(window_mode: str) -> Optional[Driver]:
    """
    Инициализирует веб-драйвер.

    Args:
        window_mode (str): Режим окна для драйвера (например, 'headless').

    Returns:
        Optional[Driver]: Инстанс драйвера или None в случае ошибки.
    """
    driver_instance: Optional[Driver] = None
    try:
        driver_instance = Driver(Firefox, window_mode=window_mode)
        logger.info('Драйвер успешно инициализирован.')
        return driver_instance
    except Exception as ex:
        logger.critical(f"Не удалось инициализировать WebDriver: {ex}", ex, exc_info=True)
        return None

# -------------------------------- БЛОК СОРТИРОВКИ ДОМЕНОВ КАНДИДТОВ НА ПАРСИНГ ----------------------------------


def _count_product_page_types(data: dict | list | None) -> Tuple[int, int]:
    """
    Подсчитывает общее количество записей и количество записей с 'page_type': 'product' 
    в предоставленных данных.

    Args:
        data (dict | list | None): Данные, извлеченные из JSON-файла.
                                   Ожидается словарь, где значения являются записями, 
                                   или список таких словарей.

    Returns:
        Tuple[int, int]: Кортеж, содержащий (общее количество записей, количество записей 'product').
    
    Example:
        >>> example_data_dict = {
        ...     "url1": {"page_type": "product"},
        ...     "url2": {"page_type": "home"},
        ...     "url3": {"page_type": "product"}
        ... }
        >>> _count_product_page_types(example_data_dict)
        (3, 2)
        >>> example_data_list = [{"page_type": "product"}, {"page_type": "home"}]
        >>> _count_product_page_types(example_data_list)
        (2, 1)
        >>> _count_product_page_types({"url1": {"page_type": "home"}})
        (1, 0)
        >>> _count_product_page_types(None)
        (0, 0)
        >>> _count_product_page_types({})
        (0, 0)
        >>> _count_product_page_types([])
        (0, 0)
    """
    product_count: int = 0
    all_entries_count: int = 0 # Инициализация счетчика всех записей
    
    # Тип записи, обычно словарь, но может отличаться при некорректных данных.
    entry: Any 
    
    # Функция обрабатывает как словарь, так и список словарей
    entries_to_check: list = []
    if isinstance(data, dict):
        entries_to_check = list(data.values())
    elif isinstance(data, list):
        entries_to_check = data

    # Итерация по записям
    for entry in entries_to_check:
        all_entries_count += 1 # Увеличение счетчика всех записей
        # Проверка, является ли запись словарем и имеет ли атрибут 'page_type' значение 'product'.
        if isinstance(entry, dict) and entry.get('page_type') == 'product':
            product_count += 1
            
    # Функция возвращает кортеж: (общее количество, количество продуктов)
    return all_entries_count, product_count


def rename_directory_if_no_products(directory_path: Path) -> None:
    """
    Считывает 'processed_links.json' в указанной директории, подсчитывает общее количество записей 
    и 'product' page_types, и переименовывает директорию, если продукты не найдены.

    Args:
        directory_path (Path): Путь к директории для обработки.

    Raises:
        OSError: Может возникнуть при ошибке переименования директории (логируется функцией).

    Example:
        >>> # Этот пример концептуальный, так как функция изменяет файловую систему.
        >>> from pathlib import Path
        >>> # import tempfile
        >>> # temp_dir = Path(tempfile.mkdtemp())
        >>> # project_dir = temp_dir / 'my_project_dir'
        >>> # project_dir.mkdir()
        >>> # processed_links = project_dir / 'processed_links.json'
        >>> # import json
        >>> # with open(processed_links, 'w') as f: json.dump({"link1": {"page_type": "home"}}, f)
        >>> # rename_directory_if_no_products(project_dir) # doctest: +SKIP
        >>> # new_dir = temp_dir / '_my_project_dir'
        >>> # assert new_dir.exists()
        >>> # import shutil
        >>> # shutil.rmtree(temp_dir)
        >>> pass 
    """
    # Объявление переменных
    processed_links_file: Path
    data: dict | list | None # Тип возвращаемого значения j_loads
    all_entries_count: int # Переменная для общего количества записей
    product_count: int
    new_dir_name: str
    new_dir_path: Path
    
    processed_links_file = directory_path / 'processed_links.json'

    if not processed_links_file.exists():
        logger.info(f"Файл 'processed_links.json' не найден в {directory_path}. Пропуск.")
        return

    # Функция j_loads извлекает данные из JSON файла
    data = j_loads(processed_links_file)

    # j_loads логирует собственные ошибки и возвращает пустую структуру ({} или []) при неудаче
    if not data: 
        logger.warning(f"Данные не загружены из {processed_links_file} или файл пуст/поврежден. Пропуск проверки для {directory_path}.")
        return

    # Вызов функции и извлечение обоих возвращаемых значений
    all_entries_count, product_count = _count_product_page_types(data) 
    
    logger.info(f"В {processed_links_file} найдено {all_entries_count} записей, из них {product_count} с 'page_type': 'product'.")

    if product_count == 0:
        new_dir_name = f"_{directory_path.name}"
        new_dir_path = directory_path.parent / new_dir_name
        
        # Проверка, не существует ли уже директория с новым именем
        if new_dir_path.exists():
            logger.warning(f"Целевая директория '{new_dir_path}' уже существует. Пропуск переименования для '{directory_path}'.")
            return

        try:
            # Выполнение переименования директории
            directory_path.rename(new_dir_path)
            logger.info(f"Директория '{directory_path}' переименована в '{new_dir_path}'.")
        except OSError as ex:
            logger.error(f"Ошибка при переименовании директории '{directory_path}' в '{new_dir_path}'", ex, exc_info=True)
    else:
        logger.info(f"Директория '{directory_path}' содержит 'product' page_types. Переименование не требуется.")


def main_process_all_directories(base_path_str: str) -> None:
    """
    Итерируется по всем поддиректориям в указанном базовом пути и обрабатывает каждую,
    вызывая `rename_directory_if_no_products`.

    Args:
        base_path_str (str): Строковый путь к базовой директории, содержащей поддиректории для обработки.

    Example:
        >>> # Этот пример концептуальный, так как функция изменяет файловую систему.
        >>> # main_process_all_directories('/path/to/your/base_directory_with_projects') # doctest: +SKIP
        >>> pass
    """
    # Объявление переменных
    base_path: Path
    item: Path

    base_path = Path(base_path_str)

    if not base_path.exists() or not base_path.is_dir():
        logger.error(f"Базовый путь '{base_path_str}' не существует или не является директорией.")
        return

    logger.info(f"Запуск обработки директорий в: {base_path}")
    
    # Итерация по всем элементам в базовой директории
    for item in base_path.iterdir():
        # Проверка, является ли элемент директорией
        # и не начинается ли ее имя с '_', чтобы избежать повторной обработки.
        if item.is_dir():
            if item.name.startswith('_'):
                logger.info(f"Пропуск уже обработанной/помеченной директории: {item.name}")
            else:
                logger.info(f"Обработка директории: {item}")
                rename_directory_if_no_products(item)
        else:
            logger.debug(f"Элемент {item} не является директорией, пропуск.")
            
    logger.info(f"Завершение обработки директорий в: {base_path}")


def build_categories_from_suppliers_data(source_dirs_list: list[Path] | None = None) -> list[str]:
    """
    Извлекает названия категорий из JSON-файлов в указанных директориях-источниках.

    Args:
        source_dirs_list (list[Path] | None, optional): Список путей к директориям с данными поставщиков.
                                                       По умолчанию используется `Config.source_dirs`.

    Returns:
        list[str]: Список уникальных, непустых категорий, отсортированных случайным образом.
                   Возвращает пустой список, если категории не найдены или произошли ошибки.
    
    Example:
        >>> # Концептуальный пример, требует наличия файлов и структуры
        >>> # categories = build_categories_from_suppliers_data([Path('./supplier_data_A')]) # doctest: +SKIP
        >>> # print(categories) # doctest: +SKIP
        >>> # Ожидается список строк, например: ['Electronics', 'Books']
        >>> build_categories_from_suppliers_data([]) # Проверка с пустым списком директорий
        []
    """
    # Объявление переменных
    actual_source_dirs: list[Path]
    all_categories: list[str]
    source_dir_path: Path
    file_path: Path
    crawl_data: dict | list | None
    item_data: Any # Может быть словарем или другой структурой в зависимости от данных
    current_file_items: list
    unique_categories: list[str]

    all_categories = []

    if source_dirs_list is None:
        # Примечание: Config.source_dirs может быть неактуальным, если LANG_CODE изменился
        # и Config.source_dirs не был обновлен. Передавайте source_dirs_list явно.
        actual_source_dirs = Config.source_dirs 
    else:
        actual_source_dirs = source_dirs_list
    
    if not actual_source_dirs:
        logger.info('Список директорий-источников для категорий пуст.')
        return []

    for source_dir_path in actual_source_dirs:
        if not source_dir_path.is_dir():
            logger.warning(f"Директория-источник не найдена или не является директорией: {source_dir_path}. Пропуск.")
            continue
        
        logger.info(f"Обработка директории-источника для категорий: {source_dir_path}")
        for file_path in recursively_yield_file_path(source_dir_path): 
            try:
                crawl_data = j_loads(file_path)
                
                if not crawl_data:
                    continue

                current_file_items = crawl_data if isinstance(crawl_data, list) else [crawl_data]
                
                for item_data in current_file_items:
                    if isinstance(item_data, dict):
                        if 'parent_category' in item_data and item_data['parent_category']:
                            all_categories.append(str(item_data['parent_category']))
                        if 'category_name' in item_data and item_data['category_name']:
                            all_categories.append(str(item_data['category_name']))
            except Exception as ex:
                logger.error(f'Ошибка при обработке файла {file_path} для извлечения категорий', ex, exc_info=True)
                continue
    
    if not all_categories:
        logger.info('Категории не найдены в указанных источниках.')
        return []

    unique_categories = list(filter(None, set(all_categories)))
    random.shuffle(unique_categories)
    logger.info(f'Найдено и обработано {len(unique_categories)} уникальных категорий.')
    return unique_categories

def supplier_candidate(supplier_dir_path: Path) -> bool:
    """Проверка, а релевантна ли категория для парсинга. Другими словами, является ли домен - продавцом"""
    # Объявление переменных
    processed_links_file: Path
    data: dict | list | None 
    all_entries_count: int 
    product_count: int = 0 
    
    processed_links_file = supplier_dir_path / 'processed_links.json'
    if not processed_links_file.exists():
        logger.info(f"Файл 'processed_links.json' не найден в {supplier_dir_path}. Новая директория, считается кандидатом.")
        return True
    data = j_loads(processed_links_file)
    if not data: 
        logger.warning(f"Данные не загружены из {processed_links_file} или файл пуст/поврежден. Считается не кандидатом.")
        return False
    all_entries_count, product_count = _count_product_page_types(data) 
    
    logger.info(f"В {processed_links_file} найдено {all_entries_count} записей, из них {product_count} с 'page_type': 'product'.")
    if product_count > 0:
        return True
    else:
        # Если нет продуктов, но мало других записей, все еще может быть кандидатом (новая, малоизученная)
        return True if all_entries_count < 10 else False 

# --------------------------------- БЛОК ОБРАБОТКИ ВНУТРЕННИХ ССЫЛОК ----------------------------------

def process_single_internal_link(
    driver: Driver,
    internal_link_url: str,
    llm: GoogleGenerativeAi
) -> Optional[Dict[str, Any]]:
    """
    Обрабатывает одну внутреннюю ссылку, извлекает данные, анализирует с помощью LLM.

    Args:
        driver (Driver): Инстанс веб-драйвера.
        internal_link_url (str): URL внутренней ссылки для обработки.
        llm (GoogleGenerativeAi): Инстанс LLM для анализа контента.

    Returns:
        Optional[Dict[str, Any]]: Словарь с обработанными данными страницы или None в случае критической ошибки.
                                   В случае ошибки получения HTML или извлечения, возвращает словарь с информацией об ошибке.
    """
    raw_data_from_url: Optional[str]
    extracted_page_content: Dict[str, Any]
    request_dict: Dict[str, Any]
    q: str
    llm_response_data: Dict[str, Any] = {}
    a: Optional[str] = None 
    parsed_llm_response: Any
    determined_page_type: str
    new_product_links: Any
    current_product_links: List[str]
    field: str

    logger.info(f"\n--- Обработка внутренней ссылки: {internal_link_url} ---\n")

    if not internal_link_url or not internal_link_url.startswith(('http://', 'https://')):
        logger.error(f"Некорректный URL внутренней ссылки: {internal_link_url}")
        return None

    raw_data_from_url = driver.fetch_html(internal_link_url)
    
    if not raw_data_from_url:
        logger.error(f"Не удалось получить HTML для внутреннего URL: {internal_link_url}")
        return {'page_type': 'unknown', 'error': 'page_not_found', 'original_url': internal_link_url, 'processed_at': datetime.now().isoformat()}

    extracted_page_content = extract_page_data(raw_data_from_url, internal_link_url)
    if not extracted_page_content or not extracted_page_content.get('text'):
        logger.warning(f"Не удалось извлечь данные или текст пуст для внутреннего URL: {internal_link_url}")
        return {'page_type': 'unknown', 'error': 'error_while_extract', 'original_url': internal_link_url, 'processed_at': datetime.now().isoformat()}

    request_dict = extracted_page_content.copy()
    request_dict.pop('text', None)
    request_dict.pop('internal_links', None)

    q = f"`{str(request_dict)}`"
    
    try:
        if llm and Config.system_instructuction: 
            a = llm.ask(q)
            if a: 
                parsed_llm_response = j_loads(a) 
                if isinstance(parsed_llm_response, dict):
                    llm_response_data = parsed_llm_response
                elif parsed_llm_response: 
                    logger.error(f"Ответ LLM для {internal_link_url} не является JSON объектом (ожидался dict): {a}")
                    llm_response_data = {'ai_response_data_non_dict': parsed_llm_response, 'ai_raw_response': a}
                else: 
                    logger.error(f"Не удалось распарсить ответ LLM или он пуст для {internal_link_url}. Ответ LLM: {a}")
                    llm_response_data = {'ai_analized_content_error': 'parsing_failed_or_empty_after_parse', 'ai_raw_response': a}
            else:
                logger.error(f"LLM вернул пустой ответ (None или '') для {internal_link_url}")
                llm_response_data = {'ai_analized_content_error': 'empty_response_from_llm'}
        elif not llm:
             logger.warning(f"LLM не инициализирован. Пропуск анализа LLM для {internal_link_url}")
             llm_response_data = {'ai_analized_content_error': 'llm_not_initialized'}
        else: 
             logger.warning(f"Системная инструкция для LLM не задана. Пропуск анализа LLM для {internal_link_url}")
             llm_response_data = {'ai_analized_content_error': 'llm_system_instruction_missing'}

    except Exception as ex: 
        logger.error(f"Ошибка при взаимодействии с LLM или парсинге ответа для {internal_link_url}. Ответ LLM (если был): {a}", ex, exc_info=True)
        llm_response_data = {'ai_analized_content_error': f'exception: {str(ex)}', 'ai_raw_response': a if a else "N/A"}

    determined_page_type = llm_response_data.pop('page_type', extracted_page_content.get('page_type', ''))
    if not determined_page_type: 
        determined_page_type = 'unknown'
    extracted_page_content['page_type'] = determined_page_type
    
    if 'product_links' in llm_response_data:
        new_product_links = llm_response_data.pop('product_links', [])
        if isinstance(new_product_links, list):
            current_product_links = extracted_page_content.get('product_links', [])
            if not isinstance(current_product_links, list): 
                current_product_links = []
            current_product_links.extend(new_product_links)
            extracted_page_content['product_links'] = list(set(filter(None, current_product_links)))

    fields_from_llm: List[str] = ['category_name', 'parent_category', 'title', 'summary', 
                                  'description', 'specification', 'notes', 'price']
    for field in fields_from_llm:
        if field in llm_response_data and llm_response_data[field] is not None:
            extracted_page_content[field] = llm_response_data.pop(field)
        elif field in llm_response_data and llm_response_data[field] is None: 
            extracted_page_content[field] = None 
            llm_response_data.pop(field)

    extracted_page_content['ai_analized_content'] = llm_response_data 
    extracted_page_content['original_internal_url'] = internal_link_url
    extracted_page_content['processed_at'] = datetime.now().isoformat()

    return extracted_page_content


def save_processed_data_and_update_journal(
    processed_data: Dict[str, Any],
    internal_url: str,
    supplier_dir_path: Path,
    supplier_file_name: str, 
    journal: Dict[str, Any]
) -> bool:
    """
    Сохраняет обработанные данные в новый JSON и обновляет файл журнала.

    Args:
        processed_data (Dict[str, Any]): Данные, полученные от process_single_internal_link.
        internal_url (str): Обработанный внутренний URL.
        supplier_dir_path (Path): Путь к директории поставщика.
        supplier_file_name (str): Имя исходного файла поставщика, из которого взята ссылка.
        journal (Dict[str, Any]): Словарь журнала для директории поставщика (будет изменен).

    Returns:
        bool: True, если сохранение и обновление прошли успешно, иначе False.
    """
    
    output_path: Path
    output_data_for_json_file: Dict[str, Dict[str, Any]]
    
    journal_path: Path

    output_path = supplier_dir_path / gs.now
    new_data_filename: str = output_path.relative_to(Config.STORAGE)

    output_data_for_json_file = {
        internal_url: processed_data
    }

    if j_dumps(output_data_for_json_file, output_path): 
        logger.info(f"Успешно сохранена информация для {internal_url} в файл: {output_path.relative_to(Config.STORAGE)} (структура: {{url: data}})")
        
        journal[internal_url] = {
            "processed_at": datetime.now().isoformat(),
            "source_file_name": supplier_file_name, 
            "output_file_name": f'{new_data_filename.stem}.json',
            "page_type": processed_data.get('page_type', 'unknown'),
            "page_url": internal_url,
        }
        journal_path:Path = supplier_dir_path / Config.processed_internal_links_file_name
        if not j_dumps(journal, journal_path):
            return False 
        return True
    else:
        return False


def process_one_link_from_file_content(
    supplier_data_content: Dict[str, Any],
    supplier_file_path: Path, 
    driver: Driver,
    llm: GoogleGenerativeAi,
    journal: Dict[str, Any],
    stats: Dict[str, int]
) -> bool:
    """
    Ищет и обрабатывает одну необработанную внутреннюю ссылку из содержимого файла поставщика.

    Args:
        supplier_data_content (Dict[str, Any]): Содержимое JSON-файла поставщика.
        supplier_file_path (Path): Путь к файлу поставщика.
        driver (Driver): Инстанс веб-драйвера.
        llm (GoogleGenerativeAi): Инстанс LLM.
        journal (Dict[str, Any]): Журнал обработанных ссылок для текущей директории поставщика.
        stats (Dict[str, int]): Словарь для обновления глобальной статистики.

    Returns:
        bool: True, если одна ссылка была найдена и успешно обработана, иначе False.
    """
    data_for_source_url: Any
    internal_links_list: Optional[List[Dict[str, Any]]]
    internal_link_item: Dict[str, Any]
    link_obj: Optional[Dict[str, Any]]
    internal_url_to_process: Optional[str]
    processed_page_data: Optional[Dict[str, Any]]

    for _, data_for_source_url in supplier_data_content.items(): 
        if not isinstance(data_for_source_url, dict):
            continue

        internal_links_list = data_for_source_url.get('internal_links')
        if not internal_links_list or not isinstance(internal_links_list, list):
            continue

        random.shuffle(internal_links_list) 

        for internal_link_item in internal_links_list:
            if not isinstance(internal_link_item, dict) or 'link' not in internal_link_item:
                continue
            
            link_obj = internal_link_item.get('link')
            if not isinstance(link_obj, dict) or 'href' not in link_obj:
                continue

            internal_url_to_process = link_obj.get('href')
            if not internal_url_to_process or not isinstance(internal_url_to_process, str):
                continue
            
            if internal_url_to_process in journal:
                continue

            logger.info(f"Найдена необработанная внутренняя ссылка: {internal_url_to_process} из файла {supplier_file_path.name}")
            
            processed_page_data = process_single_internal_link(
                driver,
                internal_url_to_process,
                llm
            )

            if processed_page_data: 
                if 'error' in processed_page_data:
                     logger.warning(f"Обработка {internal_url_to_process} завершилась с ошибкой: {processed_page_data.get('error')}. Данные не будут сохранены как успешные.")
                elif save_processed_data_and_update_journal(
                    processed_data=processed_page_data,
                    internal_url=internal_url_to_process,
                    supplier_dir_path=supplier_file_path.parent,
                    supplier_file_name=supplier_file_path.name, 
                    journal=journal
                ):
                    stats['internal_links_processed_this_run'] += 1
                    logger.info(f"Задержка на {Config.DELAY_AFTER_LINK_PROCESSING} секунд...")
                    time.sleep(Config.DELAY_AFTER_LINK_PROCESSING)
                    return True 
    return False


def process_supplier_file(
    supplier_file_path: Path,
    driver: Driver,
    llm: GoogleGenerativeAi,
    journal: Dict[str, Any],
    stats: Dict[str, int]
) -> bool:
    """
    Обрабатывает один JSON-файл поставщика, пытаясь найти и обработать одну внутреннюю ссылку.

    Args:
        supplier_file_path (Path): Путь к JSON-файлу поставщика.
        driver (Driver): Инстанс веб-драйвера.
        llm (GoogleGenerativeAi): Инстанс LLM.
        journal (Dict[str, Any]): Журнал обработанных ссылок для директории поставщика.
        stats (Dict[str, int]): Словарь для обновления глобальной статистики.

    Returns:
        bool: True, если одна ссылка из файла была успешно найдена и обработана, иначе False.
    """
    supplier_data_content: Optional[Dict[str, Any]]
    link_processed_from_this_file: bool

    logger.info(f"Сканирование файла: {supplier_file_path.relative_to(Config.STORAGE)}")
    stats['total_source_files_scanned'] += 1

    supplier_data_content = j_loads(supplier_file_path)
    if not supplier_data_content: 
        stats['error_loading_source_files_count'] += 1
        return False 
    
    if not isinstance(supplier_data_content, dict):
        logger.warning(f"Содержимое файла {supplier_file_path.relative_to(Config.STORAGE)} не является словарем. Пропуск.")
        stats['error_loading_source_files_count'] += 1
        return False

    link_processed_from_this_file = process_one_link_from_file_content(
        supplier_data_content,
        supplier_file_path,
        driver,
        llm,
        journal,
        stats
    )

    if link_processed_from_this_file:
        logger.info(f"Обработана одна внутренняя ссылка из файла {supplier_file_path.name}.")
    else:
        logger.debug(f"В файле {supplier_file_path.name} не найдено новых необработанных внутренних ссылок.")
    
    return link_processed_from_this_file


def process_supplier_directory(
    supplier_dir_path: Path,
    driver: Driver,
    llm: GoogleGenerativeAi,
    stats: Dict[str, int]
):
    """
    Обрабатывает все JSON-файлы в указанной директории поставщика.
    Для каждого файла пытается обработать одну внутреннюю ссылку.

    Args:
        supplier_dir_path (Path): Путь к директории поставщика.
        driver (Driver): Инстанс веб-драйвера.
        llm (GoogleGenerativeAi): Инстанс LLM.
        stats (Dict[str, int]): Словарь для обновления глобальной статистики.
    """
    if not supplier_candidate(supplier_dir_path):
        # Функция supplier_candidate уже логирует причину, если не кандидат
        # rename_directory_if_no_products будет вызвана, если это результат проверки product_count
        # Если supplier_candidate вернула False по другим причинам (например, processed_links.json не читается),
        # то переименование может быть нежелательным здесь.
        # Для ясности, rename_directory_if_no_products вызывается только если директория *становится* не кандидатом
        # из-за отсутствия продуктов после анализа.
        # Если она изначально "плохая" (не читается журнал), то supplier_candidate это обработает.
        logger.info(f"Директория {supplier_dir_path.name} не прошла проверку 'supplier_candidate'. Пропуск обработки ссылок.")
        # Опционально: если supplier_candidate означает "не продавец", можно переименовать
        # rename_directory_if_no_products(supplier_dir_path)
        return

    journal_path: Path
    journal: Dict[str, Any]
    supplier_file_names: List[str]
    supplier_file_paths: List[Path]
    supplier_file_path: Path

    logger.info(f"--- Обработка директории поставщика: {supplier_dir_path.name} ---")
    
    journal_path = supplier_dir_path / Config.processed_internal_links_file_name
    journal = j_loads(journal_path) or {} 

    supplier_file_names = get_filenames_from_directory(supplier_dir_path, 'json')
    if not supplier_file_names:
        logger.info(f"В директории {supplier_dir_path.name} нет JSON-файлов для обработки.")
        return

    supplier_file_paths = [
        supplier_dir_path / fname
        for fname in supplier_file_names
        if fname != Config.processed_internal_links_file_name
    ]

    if not supplier_file_paths:
        logger.info(f"В директории {supplier_dir_path.name} нет JSON-файлов для обработки (кроме, возможно, файла журнала).")
        return
    
    random.shuffle(supplier_file_paths)

    for supplier_file_path in supplier_file_paths:
        _ = process_supplier_file( 
            supplier_file_path,
            driver,
            llm,
            journal, 
            stats
        )

    logger.info(f"Завершена обработка файлов в директории '{supplier_dir_path.name}'.")


def main_loop(driver: Driver, llm: GoogleGenerativeAi, stats: Dict[str, int]):
    """
    Основной цикл обработки директорий поставщиков.

    Args:
        driver (Driver): Инстанс веб-драйзера.
        llm (GoogleGenerativeAi): Инстанс LLM.
        stats (Dict[str, int]): Словарь для обновления глобальной статистики.
    """
    suppliers_dir_names: List[str]
    supplier_dir_name: str
    supplier_dir_path: Path
    delay_before_next_global_scan: int

    logger.info(f"Поиск директорий поставщиков в: {Config.WORK_DIR}")
    
    while True:
        # main_process_all_directories(str(Config.WORK_DIR)) # Для сортировки каталогов. Можно вызывать реже.

        suppliers_dir_names = get_directory_names(Config.WORK_DIR) 
        # Фильтруем директории, которые уже помечены как "_" (не кандидаты)
        suppliers_dir_names = [name for name in suppliers_dir_names if not name.startswith('_')]


        if not suppliers_dir_names:
            logger.warning(f'Не найдено активных директорий поставщиков в {Config.WORK_DIR}. Ожидание 60 секунд...')
            time.sleep(60)
            continue
        
        logger.info(f'Найдено {len(suppliers_dir_names)} активных директорий поставщиков. Перемешивание...')
        random.shuffle(suppliers_dir_names)

        for supplier_dir_name in suppliers_dir_names:
            supplier_dir_path = Config.WORK_DIR / supplier_dir_name
            # Дополнительная проверка, что директория все еще существует и не была переименована
            if not supplier_dir_path.is_dir() or supplier_dir_path.name.startswith('_'):
                 logger.info(f"Пропуск директории {supplier_dir_name}, т.к. она была переименована или удалена.")
                 continue
            process_supplier_directory(supplier_dir_path, driver, llm, stats)
        
        delay_before_next_global_scan = Config.DELAY_AFTER_LINK_PROCESSING * 2 # Уменьшил для более частого сканирования
        logger.info(f"--- Все активные директории обработаны. Ожидание {delay_before_next_global_scan} секунд перед новым сканированием. ---")
        time.sleep(delay_before_next_global_scan)


def log_final_stats(stats: Dict[str, int], script_name: str):
    """
    Логирует итоговую статистику работы скрипта.

    Args:
        stats (Dict[str, int]): Словарь с собранной статистикой.
        script_name (str): Имя текущего скрипта для лога.
    """
    logger.info('Итоговая статистика за этот прогон:')
    logger.info(f" - Всего исходных файлов поставщиков просканировано: {stats['total_source_files_scanned']}")
    logger.info(f" - Ошибок при загрузке/чтении исходных файлов: {stats['error_loading_source_files_count']}")
    logger.info(f" - Внутренних ссылок успешно обработано и сохранено: {stats['internal_links_processed_this_run']}")
    logger.info(f"--- Работа скрипта {script_name} завершена ---")


# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================

def parse_arguments() -> argparse.Namespace:
    """
    Парсит аргументы командной строки для имени пользователя и кода языка.

    Returns:
        argparse.Namespace: Спарсенные аргументы.
    """
    script_name: str = Path(__file__).name
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        # Description updated to be more general for 3_process_internal_links.py
        description="Обработка данных поставщиков: анализ внутренних ссылок, управление директориями и категориями.",
        # Usage string now includes the new optional lang_code argument
        usage=f"python {script_name} [username [lang_code]]",
        # Epilog updated with examples for both user and lang_code
        epilog=(
            f"Примеры:\n"
            f"  python {script_name} onela             # Пользователь 'onela', язык по умолчанию ({Config.LANG_CODE})\n"
            f"  python {script_name} kazarinov de    # Пользователь 'kazarinov', язык 'de'\n"
            f"  python {script_name}                   # Пользователь по умолчанию ('onela'), язык по умолчанию ({Config.LANG_CODE})"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Definition for the 'user' argument (matches your snippet's intent)
    parser.add_argument(
        'user', 
        type=str, 
        nargs='?', 
        default='onela', # Default value for user
        help="Имя пользователя для выбора Gemini API ключа. По умолчанию 'onela'." # Help text for user
    )
    
    # Added definition for the 'lang_code' argument
    parser.add_argument(
        'lang_code', 
        type=str, 
        nargs='?', 
        default=Config.LANG_CODE, # Default value from Config.LANG_CODE
        help=f"Код языка для обработки данных (например, 'en', 'de'). По умолчанию '{Config.LANG_CODE}'."
    )
    
    # The function returns the parsed arguments, which __main__ then uses:
    # arguments = parse_arguments()
    # username = arguments.user
    # lang_code_val = arguments.lang_code
    return parser.parse_args()

if __name__ == '__main__':
    # Объявление переменных для __main__
    current_script_name: str
    arguments: argparse.Namespace
    provided_lang_code: str # Объявление переменной в начале блока
    llm_service: Optional[GoogleGenerativeAi]
    web_driver: Optional[Driver]
    run_stats: Dict[str, int]
    # Переменные для исключений будут определены в соответствующих блоках except

    current_script_name = Path(__file__).name
    arguments = parse_arguments()
    
    # Обновление Config.LANG_CODE на основе аргумента командной строки
    # arguments.lang_code будет иметь значение по умолчанию Config.LANG_CODE ('it'), если не указан другой язык
    provided_lang_code = arguments.lang_code.lower() # Присвоение значения переменной
    if Config.LANG_CODE != provided_lang_code:
        Config.LANG_CODE = provided_lang_code
        logger.info(f"Код языка установлен из аргументов: {Config.LANG_CODE}")
    else:
        logger.info(f"Используется код языка (по умолчанию или указанный): {Config.LANG_CODE}")

    # Переопределение Config.WORK_DIR на основе финального Config.LANG_CODE
    Config.WORK_DIR = Config.STORAGE / f'data_by_supplier_{Config.LANG_CODE}'
    logger.info(f"Рабочая директория установлена в: {Config.WORK_DIR}")


    logger.info(f"--- Начало работы скрипта {current_script_name} для пользователя '{arguments.user}' и языка '{Config.LANG_CODE}' ---")

    llm_service = initialize_llm(arguments.user)
    if not llm_service:
        logger.critical("Не удалось инициализировать LLM сервис. Завершение работы.")
        sys.exit()

    web_driver = initialize_driver(Config.WINDOW_MODE)
    if not web_driver:
        logger.critical("Не удалось инициализировать WebDriver. Завершение работы.")
        sys.exit(1)

    run_stats = {
        'total_source_files_scanned': 0,
        'internal_links_processed_this_run': 0,
        'error_loading_source_files_count': 0
    }

    try:
        main_loop(web_driver, llm_service, run_stats)
    except KeyboardInterrupt:
        logger.warning("Обработка прервана пользователем (KeyboardInterrupt).")
    except Exception as ex: 
        logger.critical('Критическая ошибка в главном цикле выполнения:', ex, exc_info=True)
    finally:
        if web_driver:
            logger.info('Завершение работы драйвера...')
            try:
                web_driver.quit()
            except Exception as ex_quit: # Переименована переменная ошибки
                logger.error('Ошибка при закрытии драйвера:', ex_quit, exc_info=True)
        
        log_final_stats(run_stats, current_script_name)
