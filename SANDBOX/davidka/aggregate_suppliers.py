## \file /sandbox/davidka/aggregate_suppliers.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль анализирует JSON файлы с данными веб-страниц, извлекает информацию
и агрегирует её по поставщикам (доменам) в отдельные JSON файлы.
Каждый JSON файл поставщика сохраняется в поддиректории с именем поставщика.
===========================================================================
Скрипт читает JSON файлы из `Config.input_dirs`, обрабатывает каждый,
определяет поставщика на основе URL, извлекает текст и внутренние ссылки.
Для каждой успешно обработанной записи из исходного файла, скрипт немедленно
обновляет или создает соответствующий JSON файл поставщика. Файл поставщика
`supplier_name.json` сохраняется в директории `Config.output_dir / supplier_name /`.
Существующие файлы поставщиков дополняются новыми данными по мере их поступления.

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
from src.utils.url import get_domain, normalize_url
from src.logger import logger
# from src.utils.printer import pprint as print


class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    input_dirs: list[Path] = [Path("F:/llm/filtered_urls"),Path("F:/llm/filtered_urls_set1"),Path(__root__/ 'SANDBOX'/'davidka'/'output_product_data_set1')]
    output_dir: Path = Path("F:/llm/data_by_supplier")


# Создаем словарь для хранения блокировок по именам файлов поставщиков
# Это нужно, чтобы избежать состояния гонки при чтении-модификации-записи файла,
# даже если основной цикл последовательный (на случай будущих изменений или ошибок).
_locks: Dict[Path, threading.Lock] = {}
_lock_guard = threading.Lock() # Блокировка для доступа к словарю _locks

def _get_lock(file_path: Path) -> threading.Lock:
    """
    Возвращает или создает объект блокировки для указанного пути файла.

    Args:
        file_path (Path): Путь к файлу.

    Returns:
        threading.Lock: Объект блокировки для данного файла.
    """
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
    формирует структуру для сохранения. При записи исправляет битые URL.

    Args:
        raw_data (Dict[str, Any]): Словарь с данными из JSON.
        file_path (Path): Путь к исходному JSON файлу (для логирования).

    Returns:
        Optional[Tuple[str, str, Dict[str, Any]]]:
            Кортеж (supplier, url_key, data_to_store) или None при ошибке.
    """
    # Объявление переменных в начале функции
    main_link: Optional[str] = None
    supplier: Optional[str] = None
    url_for_domain: Optional[str] = None
    page_data_text: str = ''
    actual_internal_links: list = []
    data_source: Dict[str, Any] = raw_data
    potential_main_link: Optional[str] = None
    nested_data: Any = None
    internal_links_list: Any = None
    first_link_data: Any = None
    link_dict: Any = None
    first_href: Optional[str] = None
    page_data_text_raw: Any = None
    actual_internal_links_raw: Any = None
    data_to_store: Dict[str, Any]

    # 1. Определение основного URL и URL для домена
    # Попытка извлечь 'url' из корня
    potential_main_link = raw_data.get('url')
    if potential_main_link and isinstance(potential_main_link, str):
        main_link = normalize_url(potential_main_link)
        if main_link:
            url_for_domain = main_link
            logger.debug(f"Функция использует 'url' из корня: {main_link} ({file_path})")

    # Если не нашли в корне, ищем во вложенной структуре или первой внутренней ссылке
    if not main_link:
        logger.debug(f"Ключ 'url' отсутствует или невалиден в {file_path}. Поиск во вложенных данных или internal_links.")
        nested_data = raw_data.get('data', {}) # Используем .get с default, чтобы избежать ошибки, если 'data' нет
        if isinstance(nested_data, dict):
            data_source = nested_data # Переключаем источник данных на вложенный словарь
            # Попытка извлечь 'url' из вложенного 'data'
            potential_main_link = data_source.get('url')
            if potential_main_link and isinstance(potential_main_link, str):
                main_link = normalize_url(potential_main_link)
                if main_link:
                    url_for_domain = main_link
                    logger.debug(f"Функция использует 'url' из вложенного 'data': {main_link} ({file_path})")

        # Если все еще нет main_link, ищем в internal_links
        if not main_link:
            internal_links_list = data_source.get('internal_links') # data_source может быть raw_data или nested_data
            if isinstance(internal_links_list, list) and internal_links_list:
                try:
                    first_link_data = internal_links_list[0]
                    if isinstance(first_link_data, dict):
                        link_dict = first_link_data.get('link')
                        if isinstance(link_dict, dict):
                            first_href_raw = link_dict.get('href')
                            if first_href_raw and isinstance(first_href_raw, str):
                                first_href = normalize_url(first_href_raw)
                                if first_href:
                                    url_for_domain = first_href
                                    main_link = first_href
                                    logger.debug(f"Функция использует первую внутреннюю ссылку как ключ: {main_link} ({file_path})")
                except Exception as ex:
                     logger.error(f"Ошибка при извлечении первой ссылки из 'internal_links' в {file_path}: {ex}", ex, exc_info=True)

    # Проверка наличия main_link и url_for_domain после всех попыток
    if not main_link:
        logger.error(f"Функции не удалось определить URL (ключ) из файла: {file_path}. Пропуск.")
        return None
    if not url_for_domain: # url_for_domain должен был установиться, если main_link есть
         logger.error(f"Функции не удалось определить URL для извлечения домена из файла: {file_path}. Пропуск.")
         return None

    # 2. Извлечение домена для определения имени поставщика
    try:
        supplier = get_domain(url_for_domain)
    except Exception as ex:
        logger.error(f"Ошибка при вызове get_domain для URL '{url_for_domain}' ({file_path}): {ex}", ex, exc_info=True)
        return None
    if not supplier:
        logger.error(f"Функция get_domain не вернула домен для URL '{url_for_domain}' (файл: {file_path}). Пропуск.")
        return None

    # 3. Извлечение остальных данных (text, internal_links) из data_source
    logger.debug(f"Извлечение 'text' и 'internal_links' из источника данных для {file_path}")
    page_data_text_raw = data_source.get('text')
    actual_internal_links_raw = data_source.get('internal_links')

    if page_data_text_raw is not None and isinstance(page_data_text_raw, str):
        page_data_text = page_data_text_raw
    elif page_data_text_raw is not None: # Если есть, но не строка
        logger.warning(f"Ключ 'text' в источнике данных не является строкой ({type(page_data_text_raw)}) в {file_path}. Используется пустая строка ''.")
        page_data_text = '' # Приводим к пустой строке для консистентности

    if actual_internal_links_raw is not None and isinstance(actual_internal_links_raw, list):
        actual_internal_links = actual_internal_links_raw
    elif actual_internal_links_raw is not None: # Если есть, но не список
        logger.warning(f"Ключ 'internal_links' в источнике данных не является списком ({type(actual_internal_links_raw)}) в {file_path}. Используется пустой список [].")
        actual_internal_links = [] # Приводим к пустому списку
    else: # Если ключа нет или он None
        actual_internal_links = []


    # 4. Формирование словаря для сохранения
    # Поля 'text' и 'internal_links' в data_to_store будут перезаписаны
    # при дедупликации в update_supplier_file, если необходимо.
    # 'category' здесь используется как первичный текст, если другого нет.
    data_to_store = {
        'category': page_data_text, # Сохраняем основной текст страницы как 'category'
        'text': '', # Будет заполнено позже, если 'text' отдельное поле в данных
        'internal_links': actual_internal_links # Сохраняем извлеченные ссылки
    }

    logger.info(f"Данные для поставщика '{supplier}' извлечены из {file_path} (ключ: {main_link})")
    return supplier, main_link, data_to_store


# ==============================================================================
# Функция для немедленного обновления файла поставщика (с дедупликацией ссылок)
# ==============================================================================
def update_supplier_file(
    supplier: str,
    url_key: str,
    data_to_store: Dict[str, Any],
    base_output_dir: Path # Базовая директория для всех поставщиков
) -> bool:
    """
    Обновляет (или создает) JSON файл для поставщика в его собственной поддиректории.
    Добавляет/перезаписывает данные для URL-ключа и удаляет дубликаты в 'internal_links'.

    Args:
        supplier (str): Имя поставщика (домен).
        url_key (str): URL, используемый как ключ в JSON файле.
        data_to_store (Dict[str, Any]): Словарь новых данных для сохранения.
        base_output_dir (Path): Базовая директория, где будут создаваться поддиректории поставщиков.

    Returns:
        bool: True в случае успеха, False в случае ошибки.
    """
    # Объявление переменных в начале функции
    supplier_specific_dir: Path
    supplier_file_path: Path
    file_lock: threading.Lock
    existing_data: Dict[str, Any] = {}
    loaded_data: Optional[Dict[str, Any]] = None # Явная аннотация
    success: bool
    old_links: list
    old_entry: Any
    old_links_raw: Any
    new_links_raw: Any
    new_links: list
    seen_hrefs: set[str]
    unique_links: list
    link_item: Any
    # link_data: Any # Не используется напрямую в этой области видимости
    # href: Any # Не используется напрямую в этой области видимости
    duplicate_count: int

    if not supplier:
        logger.error("Попытка обновления файла с пустым именем поставщика.")
        return False

    # Формирование пути к директории и файлу поставщика
    supplier_specific_dir = base_output_dir / supplier
    try:
        supplier_specific_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Не удалось создать директорию для поставщика '{supplier}' в {supplier_specific_dir}: {e}", exc_info=True)
        return False

    supplier_file_path = supplier_specific_dir / f"{supplier}.json" # Имя файла совпадает с именем папки
    file_lock = _get_lock(supplier_file_path)

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
                     existing_data = {} # Начинаем с пустого словаря
                else: # Не None и не dict
                    logger.error(f"j_loads вернул не словарь ({type(loaded_data)}) для {supplier_file_path}. Файл будет создан заново.")
                    existing_data = {} # Начинаем с пустого словаря
            except Exception as ex:
                logger.error(f"Непредвиденная ошибка при чтении {supplier_file_path}: {ex}", ex, exc_info=True)
                existing_data = {} # Начинаем с чистого листа в случае ошибки чтения

        # --- Шаг 2: Подготовка к дедупликации ссылок ---
        old_links = []
        if url_key in existing_data:
            old_entry = existing_data.get(url_key)
            if isinstance(old_entry, dict):
                old_links_raw = old_entry.get('internal_links')
                if isinstance(old_links_raw, list):
                    old_links = old_links_raw
                    logger.debug(f"Найдены существующие ссылки ({len(old_links)}) для ключа '{url_key}'.")
                elif old_links_raw is not None:
                    logger.warning(f"Существующий ключ '{url_key}' содержит 'internal_links', но это не список ({type(old_links_raw)}). Старые ссылки игнорируются.")
            elif old_entry is not None:
                 logger.warning(f"Существующий ключ '{url_key}' не является словарем ({type(old_entry)}). Старые ссылки игнорируются.")

        new_links = []
        new_links_raw = data_to_store.get('internal_links')
        if isinstance(new_links_raw, list):
            new_links = new_links_raw
        elif new_links_raw is not None:
            logger.warning(f"Новые данные для ключа '{url_key}' содержат 'internal_links', но это не список ({type(new_links_raw)}). Новые ссылки игнорируются при дедупликации.")

        # --- Шаг 3: Дедупликация ссылок ---
        seen_hrefs = set()
        unique_links = []
        duplicate_count = 0

        # Внутренняя функция для добавления уникальной ссылки
        def add_unique_link(link_item_to_add: Any, source_list_name: str) -> None:
            nonlocal duplicate_count, seen_hrefs, unique_links # Захват внешних переменных
            item_href: Optional[str] = None
            item_link_data: Any = None

            if isinstance(link_item_to_add, dict):
                item_link_data = link_item_to_add.get('link')
                if isinstance(item_link_data, dict):
                    item_href_raw = item_link_data.get('href')
                    if item_href_raw and isinstance(item_href_raw, str):
                        item_href = normalize_url(item_href_raw) # Нормализуем href перед проверкой
                        if item_href and item_href not in seen_hrefs:
                            seen_hrefs.add(item_href)
                            # Сохраняем исходный link_item_to_add, но href внутри него теперь должен быть нормализован
                            # Лучше создать копию и обновить в ней href, чтобы не менять исходные данные случайно
                            updated_link_item = link_item_to_add.copy()
                            updated_link_item['link'] = item_link_data.copy()
                            updated_link_item['link']['href'] = item_href
                            unique_links.append(updated_link_item)
                        elif item_href: # href есть, но уже видели (дубликат)
                             if source_list_name == 'new': # Считаем дубли только из нового списка
                                duplicate_count += 1
                        else: # Нормализация item_href_raw дала None
                            logger.warning(f"Пропуск элемента в {source_list_name}_links: 'href' ('{item_href_raw}') стал невалидным после нормализации. Элемент: {link_item_to_add}")
                    elif item_href_raw is None:
                         logger.warning(f"Пропуск элемента в {source_list_name}_links: отсутствует ключ 'href' в подсловаре 'link'. Элемент: {link_item_to_add}")
                    else: # href есть, но не строка
                        logger.warning(f"Пропуск элемента в {source_list_name}_links: 'href' не является строкой ({type(item_href_raw)}). Элемент: {link_item_to_add}")
                elif item_link_data is None:
                     logger.warning(f"Пропуск элемента в {source_list_name}_links: отсутствует ключ 'link'. Элемент: {link_item_to_add}")
                else: # link есть, но не словарь
                    logger.warning(f"Пропуск элемента в {source_list_name}_links: 'link' не является словарем ({type(item_link_data)}). Элемент: {link_item_to_add}")
            else: # Элемент списка сам по себе не словарь
                logger.warning(f"Пропуск элемента в {source_list_name}_links: элемент не является словарем ({type(link_item_to_add)}). Элемент: {link_item_to_add}")

        logger.debug(f"Дедупликация: обработка {len(old_links)} старых ссылок...")
        for link_item in old_links:
            add_unique_link(link_item, 'old')

        logger.debug(f"Дедупликация: обработка {len(new_links)} новых ссылок...")
        for link_item in new_links:
            add_unique_link(link_item, 'new')

        if duplicate_count > 0:
            logger.info(f"Удалено {duplicate_count} дублирующихся ссылок (по нормализованному href) при обновлении ключа '{url_key}' для поставщика '{supplier}'.")
        logger.debug(f"Итоговый размер дедуплицированного списка 'internal_links': {len(unique_links)}")

        # --- Шаг 4: Обновление данных в словаре ---
        logger.debug(f"Обновление/добавление ключа '{url_key}' в данных для {supplier}...")
        if not isinstance(data_to_store, dict):
             logger.error(f"Критическая ошибка: data_to_store не является словарем ({type(data_to_store)}) перед присвоением. Запись не будет произведена.")
             return False

        # Обновляем или создаем запись для url_key
        current_entry_data = existing_data.get(url_key, {}) # Получаем существующую запись или пустой словарь
        if not isinstance(current_entry_data, dict): # Если под ключом не словарь, затираем
            logger.warning(f"Данные под ключом '{url_key}' не являются словарем ({type(current_entry_data)}). Будут перезаписаны.")
            current_entry_data = {}

        current_entry_data.update(data_to_store) # Обновляем данными из data_to_store
        current_entry_data['internal_links'] = unique_links # Заменяем ссылки на дедуплицированные
        existing_data[url_key] = current_entry_data # Обновляем основную структуру

        # --- Шаг 5: Запись обновленного словаря в файл ---
        logger.debug(f"Запись итоговых данных в {supplier_file_path}...")
        try:
            success = j_dumps(existing_data, supplier_file_path)
            if success:
                logger.info(f"Файл {supplier_file_path} успешно обновлен для ключа '{url_key}'.")
                return True
            else:
                 # j_dumps сам логирует ошибку
                 logger.error(f"Функция j_dumps сообщила об ошибке при записи файла {supplier_file_path}")
                 return False
        except Exception as ex:
            logger.error(f"Непредвиденная ошибка при записи {supplier_file_path}: {ex}", ex, exc_info=True)
            return False
    # Блокировка освобождается здесь
    # На случай, если поток завершится без явного return внутри with
    logger.error(f"Выход из функции update_supplier_file для {supplier_file_path} без явного return из блока with.")
    return False


# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================
if __name__ == '__main__':
    # Объявление переменных в начале блока
    need_sanitize_json_files: bool = False # Установите True, если санация необходима
    processed_files_count: int = 0
    error_loading_files_count: int = 0
    error_extracting_data_count: int = 0
    error_writing_files_count: int = 0
    total_files_scanned: int = 0
    input_dir: Path
    file_path: Path
    raw_data: Optional[Dict[str, Any]] = None
    extracted_info: Optional[Tuple[str, str, Dict[str, Any]]] = None
    supplier: str
    url_key: str
    data_to_store: Dict[str, Any]
    write_success: bool
    base_output_dir: Path = Config.output_dir # Используем переменную для ясности

    for input_dir in Config.input_dirs:
        logger.info(f"Обработка файлов из директории: {input_dir}")
        logger.info(f"Файлы поставщиков будут сохранены в поддиректории {base_output_dir}/<имя_поставщика>/")

        #1. Санация (опционально)
        if need_sanitize_json_files:
            logger.info(f"--- Запуск санации JSON файлов в {input_dir} ---")
            try:
                sanitize_json_files(input_dir) # Предполагается, что эта функция существует и работает
                logger.info(f"Санация JSON файлов в {input_dir} успешно завершена.")
            except Exception as ex_sanitize:
                 logger.error(f"Ошибка во время выполнения sanitize_json_files для {input_dir}: {ex_sanitize}", exc_info=True)
            logger.info(f"--- Санация завершена для {input_dir} ---")

        logger.info(f"--- Начало обработки JSON файлов из {input_dir} ---")

        # 2. Обработка файлов из текущей input_dir
        try:
            for file_path in recursively_yield_file_path(input_dir, '*.json'):
                total_files_scanned += 1
                logger.debug(f"Обработка файла ({total_files_scanned}): {file_path}")

                # Шаг 1: Загрузка данных
                raw_data = None # Сброс
                try:
                    raw_data = j_loads(file_path)
                except Exception as ex_load: # Более специфичный except
                    logger.error(f"Непредвиденная ошибка при загрузке файла {file_path}: {ex_load}", exc_info=True)
                    error_loading_files_count += 1
                    continue # Переход к следующему файлу

                if not raw_data: # j_loads вернул None или пустой dict
                    # logger.warning(f"Пропуск файла из-за ошибки загрузки/формата или пустых данных: {file_path}") # j_loads уже логирует
                    error_loading_files_count += 1
                    continue

                # Шаг 2: Извлечение данных
                extracted_info = None # Сброс
                try:
                     extracted_info = extract_and_structure_data(
                        raw_data=raw_data,
                        file_path=file_path
                    )
                except Exception as ex_extract: # Более специфичный except
                    logger.error(f"Непредвиденная ошибка при извлечении данных из {file_path}: {ex_extract}", exc_info=True)
                    error_extracting_data_count += 1
                    continue

                # Шаг 3: Обновление файла поставщика
                if extracted_info:
                    supplier, url_key, data_to_store = extracted_info
                    write_success = update_supplier_file(
                        supplier=supplier,
                        url_key=url_key,
                        data_to_store=data_to_store,
                        base_output_dir=base_output_dir # Передаем базовую директорию
                    )
                    if write_success:
                        processed_files_count += 1
                    else:
                        error_writing_files_count += 1
                else: # extract_and_structure_data вернула None
                    error_extracting_data_count += 1
                    # logger.warning(f"Не удалось извлечь структурированные данные из {file_path}. Пропуск записи.") # extract_and_structure_data уже логирует
                    continue

        except Exception as ex_main_loop: # Ошибка в самом цикле for file_path...
            logger.critical(f"Критическая ошибка во время итерации по файлам в {input_dir}: {ex_main_loop}", exc_info=True)
        logger.info(f"--- Обработка файлов из {input_dir} завершена ---")

    logger.info(f"========== Итоговая статистика по всем директориям ==========")
    logger.info(f" - Всего просканировано файлов: {total_files_scanned}")
    logger.info(f" - Успешно обработано записей (записано/обновлено в файлы поставщиков): {processed_files_count}")
    logger.info(f" - Ошибок загрузки/формата исходных файлов: {error_loading_files_count}")
    logger.info(f" - Ошибок извлечения структурированных данных: {error_extracting_data_count}")
    logger.info(f" - Ошибок записи в файлы поставщиков: {error_writing_files_count}")
    logger.info(f"--- Работа скрипта {Path(__file__).name} завершена ---")
