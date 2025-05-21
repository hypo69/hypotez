## \file /sandbox/davidka/4_sort_categories.py
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
 .. module:: sandbox.davidka.4_sort_categories
 ```
"""

# Стандартные библиотеки
import random
from pathlib import Path
from types import SimpleNamespace
from typing import Any # Используется для аннотации типов в данных со смешанной структурой

# Импорты проекта
import header # noqa
from header import __root__ # noqa
from src import gs # noqa
from src.logger.logger import logger
from src.utils.json_utils import j_loads, j_loads_ns
from src.utils.file_utils import recursively_yield_file_path, read_text_file, save_text_file


class Config:
    """
    Класс конфигурации для скрипта.
    Содержит пути, настройки хранилища и исходные данные.
    """
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    
    STORAGE: Path = Path(config.local_storage.storage) if config.actual_storage == 'local_storage' else Path(config.google_drive.storage)

    source_dirs: list[Path] = [
        # STORAGE / 'search_results', 
        STORAGE / 'data_by_supplier_de', 
        STORAGE / 'data_by_supplier_it', 
        STORAGE / 'data_by_supplier_set_1 DONT TOUCH!', 
    ]

    known_categories_path: Path = STORAGE / 'known_categories.txt'
    known_categories: list[str] = read_text_file(known_categories_path, as_list=True) or []
    




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
        # Предполагается, что recursively_yield_file_path корректно обрабатывает Path
        for file_path in recursively_yield_file_path(source_dir_path): 
            try:
                # Функция j_loads извлекает данные из JSON файла
                crawl_data = j_loads(file_path)
                
                # j_loads логирует ошибки и возвращает {} или [] при неудаче
                if not crawl_data:
                    continue

                # Приведение к списку, если crawl_data не список, для единообразной обработки
                current_file_items = crawl_data if isinstance(crawl_data, list) else [crawl_data]
                
                for item_data in current_file_items:
                    if isinstance(item_data, dict):
                        if 'parent_category' in item_data and item_data['parent_category']:
                            all_categories.append(str(item_data['parent_category']))
                        if 'category_name' in item_data and item_data['category_name']:
                            all_categories.append(str(item_data['category_name']))
            except Exception as ex:
                # Дополнительный общий обработчик на случай непредвиденных ошибок при обработке файла
                logger.error(f'Ошибка при обработке файла {file_path} для извлечения категорий', ex, exc_info=True)
                continue
    
    if not all_categories:
        logger.info('Категории не найдены в указанных источниках.')
        return []

    # Удаление дубликатов и пустых строк
    unique_categories = list(filter(None, set(all_categories)))
    # Перемешивание списка категорий
    random.shuffle(unique_categories)
    logger.info(f'Найдено и обработано {len(unique_categories)} уникальных категорий.')
    return unique_categories


if __name__ == '__main__':
    # Основная логика скрипта при его прямом запуске:
    # 1. Обработка директорий (переименование папок без товаров)
    # Этот блок можно закомментировать, если требуется только обновление категорий.
    # logger.info("Запуск этапа переименования директорий...")
    # for storage_root_dir_str in Config.source_dirs: # Предполагаем, что это корневые директории для проектов
    #    main_process_all_directories(str(storage_root_dir_str.parent)) # Обрабатываем родительскую папку, где лежат проекты
    # logger.info("Этап переименования директорий завершен.")
    
    # 2. Сбор, обновление и сохранение списка категорий
    logger.info("Запуск этапа обновления списка категорий...")
    
    # Извлечение категорий из файлов данных поставщиков
    found_categories: list[str] = build_categories_from_suppliers_data(Config.source_dirs)
    
    # Расширение существующего списка категорий новыми найденными
    current_known_categories: list[str] = list(Config.known_categories) # Создание копии для изменения
    current_known_categories.extend(found_categories)
    
    # Дедупликация и удаление пустых строк из объединенного списка
    updated_categories_list: list[str] = list(filter(None, set(current_known_categories)))
    random.shuffle(updated_categories_list) # Перемешивание итогового списка

    logger.info(f"Общее количество уникальных категорий для сохранения: {len(updated_categories_list)}.")

    # Сохранение обновленного списка категорий
    # Предполагается, что save_text_file корректно обрабатывает список строк,
    # записывая каждую строку на новой строке файла.
    if save_text_file(updated_categories_list, Config.known_categories_path):
        logger.info(f"Обновленный список категорий успешно сохранен в: {Config.known_categories_path}")
    else:
        # save_text_file сама логирует ошибку
        logger.error(f"Не удалось сохранить обновленный список категорий в: {Config.known_categories_path}")

    logger.info("Этап обновления списка категорий завершен.")

