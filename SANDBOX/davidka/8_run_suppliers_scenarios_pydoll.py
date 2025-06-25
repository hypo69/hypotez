## \file /sandbox/davidka/experiments/8_run_suppliers_scenarios_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска сценариев поставщиков
================================================================
Сценарии позволеют получить товары по поставщикам и по категориям


 ```rst
 .. module:: sandbox.davidka.experiments.8_run_suppliers_scenarios_pydoll
 ```
"""
import importlib
import asyncio
import argparse
from operator import ge
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Dict, Any, List

from pydoll.browser.chrome import Chrome
from pydoll.constants import By
from pydoll.browser.page import Page

from header import __root__
from src import gs
from src.webdriver.driver_pydoll import grab_product_page, get_product_urls_from_category_page
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.llm.gemini import GoogleGenerativeAi # Unused, but kept
#from src.endpoints.prestashop.product_async import PrestaProductAsync
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.product_fields import ProductFields
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory, recursively_get_file_path
from src.utils.jjson import j_loads, j_loads_ns, j_dumps # j_dumps unused
from src.utils.image import get_image_bytes, get_raw_image_data 
from src.logger.logger import logger


class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    SUPPLIERS_ENDPOINT: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'
    SCENARIOS_DIR: Path = __root__ / 'SANDBOX' / 'davidka' / 'scenarios'
    # config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json') #  general config.
    scenarios_files: List[str] = get_filenames_from_directory(SCENARIOS_DIR) # SANDBOX/davidka/scenarios/*.json
    PRESTA_API_KEY: str = gs.credentials.prestashop.store_davidka_net.api_key
    PRESTA_API_DOMAIN: str = gs.credentials.prestashop.store_davidka_net.api_domain
    #presta_product_async: PrestaProductAsync = PrestaProductAsync(api_key=PRESTA_API_KEY, api_domain=PRESTA_API_DOMAIN)
    presta_product: PrestaProduct = PrestaProduct(api_key=PRESTA_API_KEY, api_domain=PRESTA_API_DOMAIN)
    browser: Chrome = None
    page: Page = None


# ПРАВИЛЬНО:
async def save_to_prestashop_async(f:ProductFields):
    """"""
    p = Config.presta_product
    result = await p.presta_product.add_new_product_async(f)


async def process_supplier(supplier_prefix:str, page: 'Page', product_url:Optional[str] = None ) -> bool:
    """Название файла JSON соответствуют `supplier_prefix`, а  названия папок в системе - `supplier_alias` """
    ...
    
    try:
        supplier_alias:str = supplier_prefix.replace('.','_').replace('-','_')
        supplier_path:Path = Config.SUPPLIERS_ENDPOINT / supplier_alias 
        product_locators:SimpleNamespace = j_loads_ns(supplier_path / 'locators' / 'product.json')
        category_locators:SimpleNamespace = j_loads_ns(supplier_path / 'locators' / 'category.json')
        actual_fields:list = ['id_supplier',                                                              
                     'name',
                     'price',
                     'reference',
                     'description',
                     'description_short',
                     'default_image_url']

        # --- dev ---
        scenarios_list: list = j_loads(Config.SCENARIOS_DIR  / f'{supplier_prefix}.json') # <- ЧИТАЮ ИЗ ПАПКИ САНДБОХ
        
        graber_module_path:str  = f"src.suppliers.suppliers_list.{supplier_prefix}.graber_via_pydoll"
    except Exception as ex:
        
        logger.error(f'Непредвиденная ошибка', ex)
        return False


    try:
        graber = importlib.import_module(graber_module_path)
    except Exception as ex:
        logger.error(f"Failed to import module `graber` '{supplier_prefix}'", ex)
        return False


    if product_url: # <- обработка одной ссылки
        f:ProductFields = await graber.grab_product_page(page, product_url)
        return save_to_prestashop(f)
        
    for scenario in scenarios_list:
        products_urls_in_category:list = await graber.get_product_urls_from_category_page(scenario['url'], category_locators.product_links, page)

        if not products_urls_in_category:
            logger.debug(f'Вероятно, пустая категория ')
            print(scenario)
            continue # <- мб пустаая категория
            ...

        for product_url in products_urls_in_category:
            f:ProductFields = await graber.grab_product_page(page, product_url)
            save_to_prestashop(f)
            
        return True


async def main(scenario_filename: Optional[str] = None) -> None:
    """
    Основная функция для запуска обработки сценариев.

    Args:
        scenario_filename (Optional[str], optional):
            Путь к конкретному файлу сценария для обработки.
            Может быть абсолютным путем, относительным путем или именем файла,
            который будет искаться в `Config.SCENARIOS_DIR`.
            Если `None`, обрабатываются все файлы из `Config.scenarios_files`.
            По умолчанию `None`.

    Returns:
        None
    """
    ... 
    scenrio_files_to_process: List[Path] = []
    scenario_data: Dict[str, Any] | List[Dict[str, Any]] | None
    supplier_prefix_from_file: str
    # single_scenario: Dict[str,Any] # Объявляется внутри цикла, если необходимо

    if scenario_filename:
        # Если передан конкретный файл, обрабатываем только его.
        path_candidate: Path = Path(scenario_filename)
        # Проверка, является ли указанный путь существующим файлом
        if path_candidate.is_file():
            paths_to_process.append(path_candidate.resolve())
            logger.info(f"Обработка указанного файла сценария: {paths_to_process[0]}")
        # Проверка, существует ли файл с таким именем в директории сценариев по умолчанию
        elif (Config.SCENARIOS_DIR / path_candidate.name).is_file(): # Используем path_candidate.name для корректного поиска в SCENARIOS_DIR
            paths_to_process.append((Config.SCENARIOS_DIR / path_candidate.name).resolve())
            logger.info(f"Обработка указанного файла сценария из директории по умолчанию: {paths_to_process[0]}")
        else:
            logger.error(f"Файл сценария '{scenario_filename}' не найден ни как абсолютный/относительный путь, ни в директории {Config.SCENARIOS_DIR}.")
            return # Выход, если указанный файл не найден
    else:
        # Если имя файла не передано, обрабатываем все файлы из конфигурации.
        logger.info(f"Обработка всех файлов сценариев из директории: {Config.SCENARIOS_DIR}")
        for fname in Config.scenarios_files:
            scenrio_files_to_process.append((Config.SCENARIOS_DIR / fname).resolve())

    if not scenrio_files_to_process:
        logger.info("Нет файлов сценариев для обработки.")
        return

    for current_scenario_path in scenrio_files_to_process:
        ... 
        logger.info(f"Начало обработки файла сценария: {current_scenario_path}")
        # Извлечение сценариев из файла
        scenario_data = j_loads(current_scenario_path)

        if not scenario_data:
            # j_loads уже логирует ошибку, дополнительное сообщение для контекста
            logger.warning(f"Не удалось загрузить или пустой файл сценария: {current_scenario_path}")
            continue

        # Извлечение префикса поставщика из имени файла (без расширения)
        supplier_prefix_from_file = current_scenario_path.stem


        # --- Начало обработки единичного файла сценария ---
        if isinstance(scenario_data, dict):
            # Обработка одного сценария из файла (если файл содержит объект JSON)
            logger.info(f"Обработка одиночного сценария для поставщика '{supplier_prefix_from_file}' из файла {current_scenario_path.name}.")
            await execute_scenario(supplier_prefix=supplier_prefix_from_file,
                                   scenario=scenario_data)

        elif isinstance(scenario_data, list):
            # Обработка списка сценариев из файла (если файл содержит массив JSON)
            logger.info(f"Обработка списка сценариев для поставщика '{supplier_prefix_from_file}' из файла {current_scenario_path.name}.")
            for index, single_scenario in enumerate(scenario_data):
                if isinstance(single_scenario, dict):
                    logger.info(f"Обработка сценария #{index + 1} для поставщика '{supplier_prefix_from_file}'.")
                    await execute_scenario(supplier_prefix=supplier_prefix_from_file,
                                           scenario=single_scenario)
                else:
                    logger.warning(f"Элемент #{index + 1} в списке сценариев файла {current_scenario_path.name} не является словарем: {type(single_scenario)}")
        else:
            logger.warning(f"Неизвестный формат данных в файле сценария {current_scenario_path.name}: {type(scenario_data)}")
        ... 
        logger.info(f"Завершение обработки файла сценария: {current_scenario_path}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Запускает обработку сценариев поставщиков.')
    parser.add_argument(
        '--scenario',
        dest='scenario_filename', # Имя атрибута в args
        type=str,
        default=None,
        help='Опциональный путь к файлу сценария или имя файла в директории сценариев. Если не указан, обрабатываются все сценарии.'
    )
    args = parser.parse_args()

    asyncio.run(main(scenario_filename=args.scenario_filename))

if __name__ == '__main__':
    asyncio.run(main('amazon.json'))
