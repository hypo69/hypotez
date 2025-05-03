## \file /sandbox/davidka/aggregate_suppliers.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль анализирует JSON файлы с данными веб-страниц, извлекает информацию
и агрегирует её по поставщикам (доменам) в отдельные JSON файлы.
=================================================================
Скрипт читает JSON файлы из `Config.filtered_urls_dir`, обрабатывает каждый,
определяет поставщика на основе URL, извлекает текст и внутренние ссылки.
Для каждой успешно обработанной записи из исходного файла, скрипт немедленно
обновляет или создает соответствующий JSON файл поставщика в директории
`Config.data_by_supplier_dir`. Существующие файлы поставщиков дополняются
новыми данными по мере их поступления.

```rst
 .. module:: sandbox.davidka.aggregate_suppliers
```
"""

from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Callable
import threading # Импортируем для блокировки

# Стандартные импорты проекта
import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads, j_dumps, sanitize_json_files
from src.utils.file import recursively_yield_file_path
from src.utils.url import get_domain
from src.logger import logger
# from src.utils.printer import pprint as print


class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    filtered_urls_dir: Path = Path("F:/llm/filtered_urls_set1")
    data_by_supplier_dir: Path = Path("F:/llm/data_by_supplier")
    # Создаем директорию для файлов поставщиков при инициализации, если ее нет
    data_by_supplier_dir.mkdir(parents=True, exist_ok=True)


# Создаем словарь для хранения блокировок по именам файлов поставщиков
# Это нужно, чтобы избежать состояния гонки при чтении-модификации-записи файла,
# даже если основной цикл последовательный (на случай будущих изменений или ошибок).
_locks: Dict[Path, threading.Lock] = {}
_lock_guard = threading.Lock() # Блокировка для доступа к словарю _locks

def _get_lock(file_path: Path) -> threading.Lock:
    """Возвращает или создает объект блокировки для указанного пути файла."""
    with _lock_guard:
        if file_path not in _locks:
            _locks[file_path] = threading.Lock()
        return _locks[file_path]


# ==============================================================================
# Функция обработки одного словаря данных 
# ==============================================================================
def extract_and_structure_data(
    raw_data: Dict[str, Any],
    file_path: Path
) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    """
    Извлекает данные из словаря raw_data, определяет поставщика и
    формирует структуру для сохранения.

    Args:
        raw_data (Dict[str, Any]): Словарь с данными из JSON.
        file_path (Path): Путь к исходному JSON файлу (для логирования).

    Returns:
        Optional[Tuple[str, str, Dict[str, Any]]]:
            Кортеж (supplier, url_key, data_to_store) или None при ошибке.

    Example:
        >>> data = {'url': 'https://example.com/page1', 'text': 'Content'}
        >>> result = extract_and_structure_data(data, Path('file.json'))
        >>> print(result)
        ('example.com', 'https://example.com/page1', {'category': 'Content', 'text': '', 'internal_links': []})
    """
    # --- Логика функции осталась прежней ---
    main_link: Optional[str] = None
    supplier: Optional[str] = None
    url_for_domain: Optional[str] = None
    page_data_text: str = ''
    actual_internal_links: list = []
    data_source: Dict[str, Any] = raw_data

    # 1. Определение основного URL и URL для домена
    potential_main_link: Any = raw_data.get('url')
    if potential_main_link and isinstance(potential_main_link, str):
        url_for_domain = potential_main_link
        main_link = potential_main_link
    else:
        nested_data: Any = raw_data.get('data')
        if isinstance(nested_data, dict):
            data_source = nested_data
        internal_links_list: Any = data_source.get('internal_links')
        if isinstance(internal_links_list, list) and internal_links_list:
            try:
                first_link_data: Any = internal_links_list[0]
                if isinstance(first_link_data, dict):
                    link_dict: Any = first_link_data.get('link')
                    if isinstance(link_dict, dict):
                        first_href: Any = link_dict.get('href')
                        if first_href and isinstance(first_href, str):
                            url_for_domain = first_href
                            main_link = first_href
            except Exception as ex:
                 logger.error(f"Ошибка при извлечении первой ссылки из 'internal_links' в {file_path}: {ex}", ex, exc_info=True)

    if not main_link:
        logger.error(f"Функции не удалось определить URL (ключ) из файла: {file_path}. Пропуск.")
        return None
    if not url_for_domain:
         logger.error(f"Функции не удалось определить URL для домена из файла: {file_path}. Пропуск.")
         return None

    # 2. Извлечение домена
    try:
        supplier = get_domain(url_for_domain)
    except Exception as ex:
        logger.error(f"Ошибка при вызове get_domain для URL '{url_for_domain}' ({file_path}): {ex}", ex, exc_info=True)
        return None
    if not supplier:
        logger.error(f"Функция get_domain не вернула домен для URL '{url_for_domain}' (файл: {file_path}). Пропуск.")
        return None

    # 3. Извлечение остальных данных
    page_data_text_raw: Any = data_source.get('text')
    actual_internal_links_raw: Any = data_source.get('internal_links')

    if page_data_text_raw is not None and isinstance(page_data_text_raw, str):
        page_data_text = page_data_text_raw
    elif page_data_text_raw is not None:
        logger.warning(f"Ключ 'text' не строка ({type(page_data_text_raw)}) в {file_path}. Используется ''.")

    if actual_internal_links_raw is not None and isinstance(actual_internal_links_raw, list):
        actual_internal_links = actual_internal_links_raw
    elif actual_internal_links_raw is not None:
        logger.warning(f"Ключ 'internal_links' не список ({type(actual_internal_links_raw)}) в {file_path}. Используется [].")

    # 4. Формирование словаря
    data_to_store: Dict[str, Any] = {
        'category': page_data_text,
        'text': '',
        'internal_links': actual_internal_links
    }

    logger.info(f"Данные для '{supplier}' извлечены из {file_path} (ключ: {main_link})")
    return supplier, main_link, data_to_store

# ==============================================================================
# Функция для немедленного обновления файла поставщика (с дедупликацией ссылок)
# ==============================================================================
def update_supplier_file(
    supplier: str,
    url_key: str,
    data_to_store: Dict[str, Any],
    target_dir: Path
) -> bool:
    """
    Обновляет (или создает) JSON файл для поставщика, добавляя/перезаписывая
    данные для URL-ключа и удаляя дубликаты в 'internal_links' по 'href'.

    Args:
        supplier (str): Имя поставщика (домен).
        url_key (str): URL, используемый как ключ в JSON файле.
        data_to_store (Dict[str, Any]): Словарь новых данных для сохранения.
        target_dir (Path): Директория для файлов поставщиков.

    Returns:
        bool: True в случае успеха, False в случае ошибки.
    """
    # Объявление переменных в начале функции
    supplier_file_path: Path = target_dir / f"{supplier}.json"
    file_lock: threading.Lock = _get_lock(supplier_file_path)
    existing_data: Dict[str, Any] = {}
    loaded_data: Optional[Dict] = None
    success: bool = False
    old_links: list = []
    old_entry: Any = None
    old_links_raw: Any = None
    new_links_raw: Any = None
    new_links: list = []
    seen_hrefs: set[str] = set()
    unique_links: list = []
    link_item: Any = None
    link_data: Any = None
    href: Any = None
    duplicate_count: int = 0


    if not supplier:
        logger.error("Попытка обновления файла с пустым именем поставщика.")
        return False

    logger.debug(f"Попытка обновления файла {supplier_file_path} для ключа '{url_key}'...")

    with file_lock: # Захват блокировки
        # --- Шаг 1: Чтение существующего файла ---
        if supplier_file_path.exists():
            logger.debug(f"Чтение существующего файла {supplier_file_path}...")
            try:
                loaded_data = j_loads(supplier_file_path)
                if loaded_data is not None and isinstance(loaded_data, dict):
                    existing_data = loaded_data
                    logger.debug(f"Файл {supplier_file_path} успешно прочитан.")
                elif loaded_data is None:
                     logger.warning(f"j_loads вернул None для {supplier_file_path}. Файл будет создан заново.")
                     existing_data = {}
                else:
                    logger.error(f"j_loads вернул не словарь ({type(loaded_data)}) для {supplier_file_path}. Файл будет создан заново.")
                    existing_data = {}
            except Exception as ex:
                logger.error(f"Непредвиденная ошибка при чтении {supplier_file_path}: {ex}", ex, exc_info=True)
                existing_data = {} # Начинаем с чистого листа

        # --- Шаг 2: Подготовка к дедупликации ссылок ---
        # Сохраняем старые ссылки ПЕРЕД обновлением основной записи для url_key
        old_links = [] # Сбрасываем на случай повторного использования переменных
        if url_key in existing_data:
            old_entry = existing_data.get(url_key)
            if isinstance(old_entry, dict):
                old_links_raw = old_entry.get('internal_links')
                if isinstance(old_links_raw, list):
                    old_links = old_links_raw
                    logger.debug(f"Найдены существующие ссылки ({len(old_links)}) для ключа '{url_key}'.")
                elif old_links_raw is not None: # Если есть ключ, но не список
                    logger.warning(f"Существующий ключ '{url_key}' содержит 'internal_links', но это не список ({type(old_links_raw)}). Старые ссылки игнорируются для дедупликации.")
            elif old_entry is not None: # Если есть ключ, но не словарь
                 logger.warning(f"Существующий ключ '{url_key}' не является словарем ({type(old_entry)}). Старые ссылки игнорируются для дедупликации.")

        # Получаем новые ссылки из данных, которые пришли на сохранение
        new_links = [] # Сбрасываем
        new_links_raw = data_to_store.get('internal_links')
        if isinstance(new_links_raw, list):
            new_links = new_links_raw
        elif new_links_raw is not None: # Если есть ключ, но не список
            logger.warning(f"Новые данные для ключа '{url_key}' содержат 'internal_links', но это не список ({type(new_links_raw)}). Новые ссылки игнорируются при дедупликации.")

        # --- Шаг 3: Дедупликация ссылок ---
        seen_hrefs = set()
        unique_links = []
        duplicate_count = 0

        # Функция для безопасного извлечения href и добавления уникальной ссылки
        def add_unique_link(link_item_to_add: Any, source_list_name: str):
            nonlocal duplicate_count # Позволяет изменять внешний счетчик
            item_href: Optional[str] = None
            item_link_data: Any = None

            if isinstance(link_item_to_add, dict):
                item_link_data = link_item_to_add.get('link')
                if isinstance(item_link_data, dict):
                    item_href = item_link_data.get('href')
                    if item_href and isinstance(item_href, str):
                        if item_href not in seen_hrefs:
                            seen_hrefs.add(item_href)
                            unique_links.append(link_item_to_add) # Добавляем весь элемент {'link': {...}}
                        elif source_list_name == 'new': # Считаем дубли только из нового списка
                            duplicate_count += 1
                    elif item_href is None:
                         logger.warning(f"Пропуск элемента в {source_list_name}_links: отсутствует ключ 'href' в подсловаре 'link'. Элемент: {link_item_to_add}")
                    else: # href есть, но не строка
                        logger.warning(f"Пропуск элемента в {source_list_name}_links: 'href' не является строкой ({type(item_href)}). Элемент: {link_item_to_add}")
                elif item_link_data is None:
                     logger.warning(f"Пропуск элемента в {source_list_name}_links: отсутствует ключ 'link'. Элемент: {link_item_to_add}")
                else: # link есть, но не словарь
                    logger.warning(f"Пропуск элемента в {source_list_name}_links: 'link' не является словарем ({type(item_link_data)}). Элемент: {link_item_to_add}")
            else: # Элемент списка сам по себе не словарь
                logger.warning(f"Пропуск элемента в {source_list_name}_links: элемент не является словарем ({type(link_item_to_add)}). Элемент: {link_item_to_add}")

        # Обработка старых ссылок
        logger.debug(f"Дедупликация: обработка {len(old_links)} старых ссылок...")
        for link_item in old_links:
            add_unique_link(link_item, 'old')

        # Обработка новых ссылок
        logger.debug(f"Дедупликация: обработка {len(new_links)} новых ссылок...")
        for link_item in new_links:
            add_unique_link(link_item, 'new')

        if duplicate_count > 0:
            logger.info(f"Удалено {duplicate_count} дублирующихся ссылок (по href) при обновлении ключа '{url_key}' для поставщика '{supplier}'.")
        logger.debug(f"Итоговый размер дедуплицированного списка 'internal_links': {len(unique_links)}")

        # --- Шаг 4: Обновление данных в словаре ---
        # Обновляем основные данные ('category', 'text') из data_to_store
        logger.debug(f"Обновление/добавление ключа '{url_key}' в данных для {supplier}...")
        # Важно: data_to_store должен быть словарем к этому моменту
        if not isinstance(data_to_store, dict):
             logger.error(f"Критической ошибка: data_to_store не является словарем ({type(data_to_store)}) перед присвоением existing_data['{url_key}']. Запись не будет произведена.")
             return False # Предотвращаем запись некорректных данных

        existing_data[url_key] = data_to_store.copy() # Копируем, чтобы не изменить исходный data_to_store

        # Обновляем 'internal_links' в сохраненных данных дедуплицированным списком
        # Убедимся, что existing_data[url_key] все еще словарь
        if isinstance(existing_data.get(url_key), dict):
            existing_data[url_key]['internal_links'] = unique_links
            logger.debug(f"Список 'internal_links' для ключа '{url_key}' заменен дедуплицированным списком.")
        else:
            # Эта ситуация маловероятна после предыдущей проверки data_to_store
            logger.error(f"После присвоения data_to_store значение existing_data['{url_key}'] не является словарем ({type(existing_data.get(url_key))}). Не удалось обновить internal_links.")
            # Решаем, прерывать ли запись или записывать без обновленных ссылок
            # В данном случае, лучше прервать, т.к. состояние данных неконсистентное
            return False


        # --- Шаг 5: Запись обновленного словаря в файл ---
        logger.debug(f"Запись итоговых данных в {supplier_file_path}...")
        try:
            # Используем порядок: <что>, <куда>
            success = j_dumps(existing_data, supplier_file_path)
            if success:
                logger.info(f"Файл {supplier_file_path} успешно обновлен для ключа '{url_key}'.")
                return True
            else:
                 logger.error(f"Функция j_dumps сообщила об ошибке при записи файла {supplier_file_path}")
                 return False
        except Exception as ex:
            logger.error(f"Непредвиденная ошибка при записи {supplier_file_path}: {ex}", ex, exc_info=True)
            return False
    # Блокировка освобождается здесь

# ==============================================================================
# Остальной код (импорты, Config, _locks, _get_lock, extract_and_structure_data, __main__)
# остается без изменений по сравнению с предыдущей версией
# ==============================================================================

# ... (импорты, Config, _locks, _get_lock) ...

# ==============================================================================
# Функция обработки одного словаря данных (БЕЗ ИЗМЕНЕНИЙ)
# ==============================================================================
def extract_and_structure_data(
    raw_data: Dict[str, Any],
    file_path: Path
) -> Optional[Tuple[str, str, Dict[str, Any]]]:
    # ... (код функции без изменений) ...
    # Объявление переменных в начале функции
    main_link: Optional[str] = None
    supplier: Optional[str] = None
    url_for_domain: Optional[str] = None
    page_data_text: str = ''
    actual_internal_links: list = []
    data_source: Dict[str, Any] = raw_data
    potential_main_link: Any = None
    nested_data: Any = None
    internal_links_list: Any = None
    first_link_data: Any = None
    link_dict: Any = None
    first_href: Any = None
    page_data_text_raw: Any = None
    actual_internal_links_raw: Any = None
    data_to_store: Dict[str, Any] = {}

    # 1. Определение основного URL и URL для домена
    potential_main_link = raw_data.get('url')
    if potential_main_link and isinstance(potential_main_link, str):
        url_for_domain = potential_main_link
        main_link = potential_main_link
        # logger.debug(f"Функция использует 'url' из корня: {main_link} ({file_path})") # Уже логируется выше
    else:
        # logger.warning(f"Ключ 'url' отсутствует или не строка в {file_path}. Функция ищет в 'internal_links'...") # Уже логируется выше
        nested_data = raw_data.get('data')
        if isinstance(nested_data, dict):
            data_source = nested_data
            # logger.debug(f"Функция ищет 'internal_links' во вложенном словаре 'data' ({file_path})")
        # else:
             # logger.debug(f"Функция ищет 'internal_links' в корневом словаре ({file_path})")

        internal_links_list = data_source.get('internal_links')
        if isinstance(internal_links_list, list) and internal_links_list:
            try:
                first_link_data = internal_links_list[0]
                if isinstance(first_link_data, dict):
                    link_dict = first_link_data.get('link')
                    if isinstance(link_dict, dict):
                        first_href = link_dict.get('href')
                        if first_href and isinstance(first_href, str):
                            url_for_domain = first_href
                            main_link = first_href
                            # logger.info(f"Функция использует первую внутреннюю ссылку как ключ: {main_link} ({file_path})") # Уже логируется выше
            except Exception as ex:
                 logger.error(f"Ошибка при извлечении первой ссылки из 'internal_links' в {file_path}: {ex}", ex, exc_info=True)

    if not main_link:
        # logger.error(f"Функции не удалось определить URL (ключ) из файла: {file_path}. Пропуск.") # Уже логируется выше
        return None
    if not url_for_domain:
         # logger.error(f"Функции не удалось определить URL для домена из файла: {file_path}. Пропуск.") # Уже логируется выше
         return None

    # 2. Извлечение домена
    try:
        supplier = get_domain(url_for_domain)
    except Exception as ex:
        logger.error(f"Ошибка при вызове get_domain для URL '{url_for_domain}' ({file_path}): {ex}", ex, exc_info=True)
        return None
    if not supplier:
        # logger.error(f"Функция get_domain не вернула домен для URL '{url_for_domain}' (файл: {file_path}). Пропуск.") # Уже логируется выше
        return None

    # 3. Извлечение остальных данных
    # logger.debug(f"Функция извлекает 'text' и 'internal_links' из {'корня' if data_source is raw_data else 'вложенного data'} ({file_path})")
    page_data_text_raw = data_source.get('text')
    actual_internal_links_raw = data_source.get('internal_links')

    if page_data_text_raw is not None and isinstance(page_data_text_raw, str):
        page_data_text = page_data_text_raw
    elif page_data_text_raw is not None:
        pass # logger.warning(f"Ключ 'text' не строка ({type(page_data_text_raw)}) в {file_path}. Используется ''.") # Уже логируется выше

    if actual_internal_links_raw is not None and isinstance(actual_internal_links_raw, list):
        actual_internal_links = actual_internal_links_raw
    elif actual_internal_links_raw is not None:
        pass # logger.warning(f"Ключ 'internal_links' не список ({type(actual_internal_links_raw)}) в {file_path}. Используется [].") # Уже логируется выше

    # 4. Формирование словаря
    data_to_store = {
        'category': page_data_text,
        'text': '',
        'internal_links': actual_internal_links # Важно: сохраняем исходный список здесь
    }

    # logger.info(f"Данные для '{supplier}' извлечены из {file_path} (ключ: {main_link})") # Уже логируется выше
    return supplier, main_link, data_to_store


# ==============================================================================
# Основной блок выполнения скрипта (БЕЗ ИЗМЕНЕНИЙ)
# ==============================================================================
if __name__ == '__main__':
    # ... (код блока __main__ без изменений) ...
    # Объявление переменных в начале блока
    need_sanitize_json_files: bool = False
    processed_files_count: int = 0
    error_loading_files_count: int = 0
    error_extracting_data_count: int = 0
    error_writing_files_count: int = 0
    total_files_scanned: int = 0
    file_path: Path
    raw_data: Optional[Dict[str, Any]] = None
    extracted_info: Optional[Tuple[str, str, Dict[str, Any]]] = None
    supplier: str
    url_key: str
    data_to_store: Dict[str, Any]
    write_success: bool

    logger.info(f"--- Начало работы скрипта ---")
    logger.info(f"Чтение исходных JSON файлов из: {Config.filtered_urls_dir}")
    logger.info(f"Запись/обновление файлов поставщиков в: {Config.data_by_supplier_dir}")

    if need_sanitize_json_files:
        logger.info("Запуск санации JSON файлов...")
        try:
            sanitize_json_files(Config.filtered_urls_dir)
            logger.info("Санация JSON файлов успешно завершена.")
        except Exception as ex:
             logger.error(f"Ошибка во время выполнения sanitize_json_files: {ex}", ex, exc_info=True)

    logger.info("Начало обработки JSON файлов...")
    try:
        for file_path in recursively_yield_file_path(Config.filtered_urls_dir, '*.json'):
            total_files_scanned += 1
            logger.debug(f"Обработка файла ({total_files_scanned}): {file_path}")

            # Шаг 1: Загрузка данных
            raw_data = None # Сброс перед попыткой
            try:
                raw_data = j_loads(file_path)
            except Exception as ex:
                logger.error(f"Непредвиденная ошибка при загрузке файла {file_path}: {ex}", ex, exc_info=True)
                error_loading_files_count += 1
                continue

            if not raw_data:
                # logger.warning(f"Пропуск файла из-за ошибки загрузки/формата: {file_path}") # Уже логируется в j_loads
                error_loading_files_count += 1
                continue

            # Шаг 2: Извлечение данных
            extracted_info = None # Сброс перед попыткой
            try:
                 extracted_info = extract_and_structure_data(
                    raw_data=raw_data,
                    file_path=file_path
                )
            except Exception as ex:
                logger.error(f"Непредвиденная ошибка при извлечении данных из {file_path}: {ex}", ex, exc_info=True)
                error_extracting_data_count += 1
                continue

            # Шаг 3: Обновление файла поставщика
            if extracted_info:
                supplier, url_key, data_to_store = extracted_info
                write_success = update_supplier_file(
                    supplier=supplier,
                    url_key=url_key,
                    data_to_store=data_to_store,
                    target_dir=Config.data_by_supplier_dir
                )
                if write_success:
                    processed_files_count += 1
                else:
                    error_writing_files_count += 1
            else:
                error_extracting_data_count += 1
                continue

    except Exception as ex:
        logger.critical(f"Критическая ошибка во время итерации по файлам: {ex}", ex, exc_info=True)

    logger.info(f"--- Обработка файлов завершена ---")
    logger.info(f"Статистика:")
    logger.info(f" - Всего просканировано файлов: {total_files_scanned}")
    logger.info(f" - Успешно обработано записей (записано/обновлено): {processed_files_count}")
    logger.info(f" - Ошибок загрузки/формата исходных файлов: {error_loading_files_count}")
    logger.info(f" - Ошибок извлечения данных из файлов: {error_extracting_data_count}")
    logger.info(f" - Ошибок записи в файлы поставщиков: {error_writing_files_count}")
    logger.info(f"--- Работа скрипта завершена ---")

