## \file /sandbox/davidka/experiments/6_sync_suppliers_with_spreadsheet.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для извлечения и обработки страниц товаров поставщиков.
================================================================
Скрипт загружает информацию о поставщиках из Google Spreadsheet,
сравнивает список поставщиков с существующими директориями,
при необходимости добавляет новых поставщиков в Spreadsheet,
извлекает ID существующих и обрабатывает данные.

 ```rst
 .. module:: sandbox.davidka.experiments.sync_suppliers_with_spreadsheet
 ```
"""

import re
import sys
import argparse
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Dict, Any, List, Tuple

import pandas as pd

# -------------------------------------------------------------------
import header
from header import __root__
from src import gs
# from src.llm.gemini import GoogleGenerativeAi
# from src.webdriver import driver
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
# Убедитесь, что путь к graber.py корректен
from SANDBOX.davidka.graber import extract_page_data
# Убедитесь, что здесь импортируется ВАША версия SpreadSheet с методами:
# find_row_index_by_value, get_cell_value_by_row_col, append_row_to_sheet, get_data
from src.goog.spreadsheet.spreadsheet import SpreadSheet
from src.utils.file import read_text_file, recursively_yield_file_path, get_directory_names
from src.utils.url import extract_pure_domain
from src.utils.jjson import j_loads, j_dumps, j_loads_ns
from src.utils.csv import save_csv_file
from src.utils.printer import pprint as print
from src.logger.logger import logger

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    
    STORAGE_PATH_STR: str = ''
    if config and hasattr(config, 'actual_storage') and hasattr(config, 'local_storage') and hasattr(config, 'google_drive'):
        STORAGE_PATH_STR = config.local_storage.storage if config.actual_storage == 'local_storage' else config.google_drive.storage
    else:
        logger.warning("Конфигурационный файл 'davidka.json' не содержит необходимых полей для определения STORAGE. Устанавливается путь по умолчанию.")
        STORAGE_PATH_STR = str(ENDPOINT / 'default_storage')

    STORAGE: Path = Path(STORAGE_PATH_STR)
    TRAIN_STORAGE: Path = STORAGE / 'train_data'
    JSON_FOR_CSV_PATH: Path = STORAGE / 'json_for_csv'
    START_ID: int = 0 # Не используется в текущей логике, но оставлено
    SUPPLIERS_SPREADSHEET_ID: str = '1bLU5aymxwbb8l8H1fuBE9soiajAGWoZ7LSOF9UM8lVQ'
    SUPPLIERS_SHEET_NAME: str = 'SUPPLIERS'
    SUPPLIER_NAME_COLUMN_HEADER: str = 'SupplierName' # Имя заголовка колонки с именами поставщиков
    SUPPLIER_ID_COLUMN_INDEX: int = 1 # 1-based индекс колонки, где находится ID (колонка 'A')
    SUPPLIER_URL_COLUMN_HEADER: str = 'Supplier URL' # Имя заголовка колонки с URL поставщиков

    TRAIN_STORAGE.mkdir(parents=True, exist_ok=True)
    JSON_FOR_CSV_PATH.mkdir(parents=True, exist_ok=True)


def get_suppliers_directories() -> List[str]:
    """
    Функция извлекает и нормализует имена директорий поставщиков из Config.TRAIN_STORAGE.
    Возвращает отсортированный список уникальных, непустых, нормализованных имен.
    """
    suppliers_dirs: List[str] = get_directory_names(Config.TRAIN_STORAGE)
    return suppliers_dirs


def get_all_data_as_dataframe(spreadsheet_id_to_query: str, sheet_name_to_query: str) -> pd.DataFrame | None:
    """
    Функция получает все данные из указанного листа Google Sheets в виде Pandas DataFrame.
    (Эта функция может быть частью вашего класса SpreadSheet или отдельной утилитой,
     если она уже существует, вы можете использовать ее).
    """
    gs_handler: SpreadSheet | None = None
    try:
        gs_handler = SpreadSheet(spreadsheet_id=spreadsheet_id_to_query)
        if not (gs_handler and gs_handler.spreadsheet):
            logger.error(f"Не удалось подключиться к таблице ID: {spreadsheet_id_to_query}")
            return None
        
        all_data_df = gs_handler.get_data(
            worksheet_name=sheet_name_to_query,
            return_as_dataframe=True,
            header_row_num=1 # Первая строка листа используется как заголовки
        )
        if all_data_df is None: # Ошибка внутри get_data
            logger.error(f"Метод get_data вернул None для листа '{sheet_name_to_query}'.")
        elif all_data_df.empty:
            logger.info(f"Лист '{sheet_name_to_query}' пуст или содержит только заголовки.")
        return all_data_df
    except Exception as ex:
        logger.error(f"Ошибка при получении DataFrame из таблицы '{spreadsheet_id_to_query}', лист '{sheet_name_to_query}'", ex, exc_info=True)
        return None





def sync_suppliers_with_spreadsheet(
    gs_handler: SpreadSheet,
    directory_supplier_names: List[str]
) -> List[Dict[str, Any]]:
    """
    Синхронизирует список поставщиков из директорий с Google Spreadsheet 'SUPPLIERS'.
    Сначала считывает все данные из таблицы, затем выполняет сравнение и
    перезаписывает весь лист обновленными данными.

    Args:
        gs_handler (SpreadSheet): Экземпляр класса для работы с Google Sheets.
        directory_supplier_names (List[str]): Список имен поставщиков из директорий (уже нормализованных).

    Returns:
        List[Dict[str, Any]]: Список словарей, где каждый словарь содержит информацию
                              о поставщике из директории и его статусе синхронизации.
    """
    processed_suppliers_info_for_return: List[Dict[str, Any]] = [] # Для возврата статуса по каждому имени из директорий
    
    # Имена колонок, которые мы ожидаем на листе.
    # 'NEXT id =XXXX' и 'Вкл' - это также заголовки, как на вашем скриншоте.
    # Порядок важен, если мы будем создавать DataFrame с нуля.
    # ID колонка, Колонка "Вкл", Колонка Имени Поставщика
    expected_sheet_columns: List[str] = [
        'ID', # Предположим, что первая колонка для ID имеет простой заголовок "ID"
        'Вкл', # Колонка для статуса включения
        Config.SUPPLIER_NAME_COLUMN_HEADER # 'SupplierName'
        # ... добавьте другие ожидаемые колонки, если они есть и должны сохраняться
    ]
    # Имя колонки, по которой ищем совпадения (имена поставщиков)
    name_col_header: str = Config.SUPPLIER_NAME_COLUMN_HEADER
    # Имя колонки (или индекс, если бы мы знали его наверняка) для ID
    id_col_header: str = 'ID' # Предполагаем такой заголовок для ID колонки
    # Если у вас в Config.SUPPLIER_ID_COLUMN_INDEX (1-based) хранится индекс,
    # то мы можем получить имя заголовка по этому индексу при чтении.
    # Пока будем считать, что заголовок колонки ID - это 'ID'.

    print(f"\n--- Синхронизация поставщиков с листом '{Config.SUPPLIERS_SHEET_NAME}' (пакетный режим) ---")

    # 1. Считываем все текущие данные с листа SUPPLIERS в DataFrame
    print(f"Считывание текущих данных с листа '{Config.SUPPLIERS_SHEET_NAME}'...")
    current_sheet_df: pd.DataFrame | None = gs_handler.get_data(
        worksheet_name=Config.SUPPLIERS_SHEET_NAME,
        return_as_dataframe=True,
        header_row_num=1 # Первая строка - заголовки
    )

    if current_sheet_df is None:
        logger.error(f"Не удалось считать данные с листа '{Config.SUPPLIERS_SHEET_NAME}'. Синхронизация прервана.")
        # Заполняем статус для всех поставщиков из директорий как ошибка
        for dir_name in directory_supplier_names:
            processed_suppliers_info_for_return.append({'name': dir_name, 'id': None, 'status': 'error_reading_sheet'})
        return processed_suppliers_info_for_return

    # Убедимся, что все ожидаемые колонки присутствуют в DataFrame, если он не пустой.
    # Если DataFrame пуст (например, лист был пуст или содержал только заголовки), создадим его с нужными колонками.
    if current_sheet_df.empty:
        logger.info(f"Лист '{Config.SUPPLIERS_SHEET_NAME}' пуст или содержит только заголовки. Создается новый DataFrame.")
        current_sheet_df = pd.DataFrame(columns=expected_sheet_columns)
    else:
        # Проверяем наличие ключевых колонок
        missing_cols: List[str] = []
        if id_col_header not in current_sheet_df.columns:
            missing_cols.append(id_col_header)
            # Если ID колонки нет, добавим ее, заполнив None
            current_sheet_df[id_col_header] = None 
            logger.warning(f"Добавлена отсутствующая колонка '{id_col_header}' в DataFrame с листа.")
        if name_col_header not in current_sheet_df.columns:
            missing_cols.append(name_col_header)
            # Если колонки с именами нет, это критично. Но для примера добавим.
            current_sheet_df[name_col_header] = None
            logger.warning(f"Добавлена отсутствующая колонка '{name_col_header}' в DataFrame с листа.")
        
        # Важно: Приведение типов, чтобы избежать проблем с NaN и сравнением
        if name_col_header in current_sheet_df.columns:
            current_sheet_df[name_col_header] = current_sheet_df[name_col_header].astype(str).str.strip()
        if id_col_header in current_sheet_df.columns:
            current_sheet_df[id_col_header] = current_sheet_df[id_col_header].astype(str).str.strip().replace(['nan', 'None', ''], pd.NA)


    # Создаем словарь для быстрого поиска существующих поставщиков и их ID (имя -> ID)
    # Ключ - нормализованное имя поставщика, значение - ID (или pd.NA если нет)
    existing_suppliers_map: Dict[str, Any] = {}
    if name_col_header in current_sheet_df.columns and id_col_header in current_sheet_df.columns:
        for _, row in current_sheet_df.iterrows():
            name_val = row[name_col_header]
            if pd.notna(name_val) and str(name_val).strip(): # Проверяем, что имя не пустое
                # Нормализуем имя из таблицы для ключа (без учета регистра)
                norm_name = str(name_val).strip().lower()
                # Если поставщик с таким нормализованным именем уже есть, не перезаписываем,
                # чтобы избежать потери ID от первой записи с таким именем.
                # Однако, это может скрыть дубликаты в таблице.
                if norm_name not in existing_suppliers_map:
                     existing_suppliers_map[norm_name] = row.get(id_col_header, pd.NA)

    # Список для сбора всех строк, которые будут записаны обратно в таблицу
    updated_sheet_data_rows: List[Dict[str, Any]] = []
    # Сначала добавляем все существующие строки из таблицы, чтобы сохранить порядок и другие данные
    # Мы будем обновлять их или помечать для удаления (если такая логика нужна)
    # В данном случае, мы просто переносим их, а новые добавим в конец.
    if not current_sheet_df.empty:
        updated_sheet_data_rows.extend(current_sheet_df.to_dict('records'))


    # 2. Обработка поставщиков из директорий
    new_suppliers_to_add: List[Dict[str, Any]] = [] # Для новых поставщиков

    for dir_supplier_name_original in directory_supplier_names: # Имена из директорий уже нормализованы (strip)
        # Для поиска в карте используем lower()
        dir_supplier_name_norm_for_search: str = dir_supplier_name_original.lower()
        
        supplier_return_info: Dict[str, Any] = {'name': dir_supplier_name_original, 'id': None, 'status': 'pending'}

        if dir_supplier_name_norm_for_search in existing_suppliers_map:
            # Поставщик найден в таблице
            supplier_id = existing_suppliers_map[dir_supplier_name_norm_for_search]
            supplier_return_info['id'] = None if pd.isna(supplier_id) else str(supplier_id)
            supplier_return_info['status'] = 'found_in_sheet'
            print(f"Поставщик '{dir_supplier_name_original}': найден в таблице, ID: {supplier_return_info['id'] or 'N/A'}.")
        else:
            # Поставщик не найден в таблице, готовим его к добавлению
            print(f"Поставщик '{dir_supplier_name_original}': не найден, будет добавлен в таблицу.")
            new_row_dict: Dict[str, Any] = {col: None for col in expected_sheet_columns} # Инициализируем всеми колонками
            new_row_dict[name_col_header] = dir_supplier_name_original # Устанавливаем имя
            # ID остается None, 'Вкл' и другие кастомные колонки тоже None или значение по умолчанию
            new_row_dict['Вкл'] = None # или 'Да'/'Нет' по умолчанию, если нужно

            new_suppliers_to_add.append(new_row_dict)
            supplier_return_info['status'] = 'added_to_sheet' # ID будет None, т.к. новый
        
        processed_suppliers_info_for_return.append(supplier_return_info)

    # Добавляем новые строки к общему списку данных
    if new_suppliers_to_add:
        updated_sheet_data_rows.extend(new_suppliers_to_add)

    # 3. Подготовка и запись обновленных данных обратно в Google Sheet
    if not updated_sheet_data_rows and not new_suppliers_to_add and current_sheet_df.empty:
        logger.info("Нет данных для записи в Google Sheet (исходный лист был пуст, новых поставщиков нет).")
        return processed_suppliers_info_for_return # Возвращаем статус обработки директорий

    # Создаем DataFrame из объединенных данных
    final_df_to_write: pd.DataFrame
    if updated_sheet_data_rows:
        final_df_to_write = pd.DataFrame(updated_sheet_data_rows)
        # Убедимся, что колонки идут в ожидаемом порядке
        # Сначала колонки, которые точно есть
        cols_order: List[str] = [col for col in expected_sheet_columns if col in final_df_to_write.columns]
        # Затем остальные колонки из DataFrame, которых нет в expected_sheet_columns (если они были)
        other_cols: List[str] = [col for col in final_df_to_write.columns if col not in cols_order]
        final_df_to_write = final_df_to_write[cols_order + other_cols]
    else: # Если исходный лист был пуст и нет новых поставщиков
        final_df_to_write = pd.DataFrame(columns=expected_sheet_columns)


    # Очищаем лист (сохраняя заголовки) и записываем DataFrame
    # ВАЖНО: Это удалит все существующие данные и заменит их!
    # Убедитесь, что это желаемое поведение.
    print(f"Перезапись листа '{Config.SUPPLIERS_SHEET_NAME}' обновленными данными...")
    try:
        # Этапы: 1. Очистить (необязательно, если update_cells справится) 2. Записать.
        # gspread worksheet.update() может принимать список списков или DataFrame.
        # Если используем update с DataFrame, он должен быть корректно обработан gspread.
        # Или конвертируем DataFrame в List[List[Any]] включая заголовки.

        # Очистка листа (сохраняя первую строку с заголовками)
        worksheet_to_update: Any = gs_handler.spreadsheet.worksheet(Config.SUPPLIERS_SHEET_NAME) # type: ignore
        # worksheet_to_update.clear() # Полная очистка
        # Очистка данных, оставляя заголовки:
        # worksheet_to_update.resize(rows=1) # Оставляем только строку заголовков
        # worksheet_to_update.resize(rows=max(2, final_df_to_write.shape[0] + 1)) # Восстанавливаем размер + запас

        # Подготовка данных для gspread.worksheet.update (List[List[Any]])
        # Первая строка - заголовки, затем данные
        header_list_for_write: List[str] = list(final_df_to_write.columns)
        # Заменяем pd.NA и NaN на пустые строки для корректной записи в Google Sheets
        data_values_for_write: List[List[Any]] = final_df_to_write.fillna('').values.tolist()
        
        list_to_write: List[List[Any]] = [header_list_for_write] + data_values_for_write

        # Обновляем весь лист, начиная с ячейки A1
        worksheet_to_update.update('A1', list_to_write, value_input_option='USER_ENTERED')
        
        logger.info(f"Лист '{Config.SUPPLIERS_SHEET_NAME}' успешно обновлен {len(data_values_for_write)} строками данных.")

    except Exception as ex:
        logger.error(f"Ошибка при перезаписи листа '{Config.SUPPLIERS_SHEET_NAME}': {ex}", exc_info=True)
        # Если произошла ошибка записи, статусы 'added_to_sheet' могут быть неверными.
        # Обновим статусы добавленных на ошибку записи.
        for info in processed_suppliers_info_for_return:
            if info['status'] == 'added_to_sheet':
                info['status'] = 'error_writing_to_sheet'
    
    return processed_suppliers_info_for_return



def main(args: argparse.Namespace) -> None:
    """
    Главная функция выполнения скрипта.
    """
    print(f"Конфигурация хранилища: {Config.STORAGE}")
    print(f"Хранилище обучающих данных: {Config.TRAIN_STORAGE}")
    
    directory_supplier_names: List[str] = get_suppliers_directories()
    if not directory_supplier_names:
        logger.info("Директории поставщиков не найдены. Завершение.")
        return
    print(f"Найдено {len(directory_supplier_names)} уникальных имен директорий: {directory_supplier_names[:5]}...")

    gs_handler: SpreadSheet | None = None
    try:
        gs_handler = SpreadSheet(Config.SUPPLIERS_SPREADSHEET_ID)
        if not (gs_handler and gs_handler.spreadsheet):
            logger.error("Не удалось инициализировать или подключиться к Google Spreadsheet. Завершение.")
            return
        print(f"Успешное подключение к таблице '{gs_handler.spreadsheet.title}'.")
    except Exception as ex:
        logger.error(f"Критическая ошибка при инициализации SpreadSheet: {ex}", exc_info=True)
        return

    suppliers_sync_results: List[Dict[str, Any]] = sync_suppliers_with_spreadsheet(gs_handler, directory_supplier_names)

    print("\n--- Результаты синхронизации поставщиков ---")
    for item in suppliers_sync_results:
        print(f"  Поставщик: {item['name']:<30} Статус: {item['status']:<25} ID: {item.get('id', 'N/A')}")

    print(f"\nЗагрузка актуального DataFrame из листа '{Config.SUPPLIERS_SHEET_NAME}'...")
    all_suppliers_df: pd.DataFrame | None = get_all_data_as_dataframe(
        Config.SUPPLIERS_SPREADSHEET_ID, Config.SUPPLIERS_SHEET_NAME
    )

    if all_suppliers_df is None:
        logger.error("Не удалось загрузить DataFrame после синхронизации. Обработка данных поставщиков невозможна.")
        return
    if all_suppliers_df.empty:
        logger.info("DataFrame поставщиков пуст после синхронизации. Нет данных для обработки.")
        return
        
    print(f"Загружен DataFrame с {all_suppliers_df.shape[0]} строками для дальнейшей обработки.")

    # Создаем карту URL для быстрого доступа
    supplier_url_map: Dict[str, str] = {}
    if Config.SUPPLIER_URL_COLUMN_HEADER in all_suppliers_df.columns and \
       Config.SUPPLIER_NAME_COLUMN_HEADER in all_suppliers_df.columns:
        for _, row in all_suppliers_df.iterrows():
            name_val = row.get(Config.SUPPLIER_NAME_COLUMN_HEADER)
            url_val = row.get(Config.SUPPLIER_URL_COLUMN_HEADER)
            if name_val and isinstance(name_val, str) and url_val and isinstance(url_val, str):
                supplier_url_map[name_val.strip()] = url_val.strip() # Ключ - нормализованное имя
    else:
        logger.warning(f"Колонка '{Config.SUPPLIER_URL_COLUMN_HEADER}' или '{Config.SUPPLIER_NAME_COLUMN_HEADER}' не найдена. URL не будут извлечены.")

    for supplier_info in suppliers_sync_results:
        if 'error' in supplier_info['status']:
            logger.warning(f"Пропуск детальной обработки для '{supplier_info['name']}' из-за ошибки: {supplier_info['status']}")
            continue
        
        # Имя поставщика из результатов синхронизации (оно нормализовано)
        current_supplier_name_norm: str = supplier_info['name']
        supplier_id: str | None = supplier_info['id']
        supplier_url: str | None = supplier_url_map.get(current_supplier_name_norm)
        
        process_supplier_data(
            supplier_name=current_supplier_name_norm, # Передаем нормализованное имя
            supplier_id=supplier_id,
            supplier_url=supplier_url
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Обработка страниц товаров поставщиков и синхронизация с Google Sheets.")
    # parser.add_argument('--max_pages', type=int, default=10, help='Максимальное количество страниц для обработки на одного поставщика.')
    
    parsed_args: argparse.Namespace = parser.parse_args()
    
    try:
        main(parsed_args)
    except Exception as e:
        logger.critical("Критическая ошибка в главном потоке выполнения.", e, exc_info=True)
        sys.exit(1)
    print("\nРабота скрипта успешно завершена.")
    sys.exit(0)
