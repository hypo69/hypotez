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

# from pydoll.browser.chrome import Chrome
# from pydoll.constants import By
# from pydoll.browser.page import Page

from header import __root__
from src import gs
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.llm.gemini import GoogleGenerativeAi # Unused, but kept
#from src.endpoints.prestashop.product_async import PrestaProductAsync
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.product_fields import ProductFields
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory, recursively_get_file_path
from src.utils.jjson import j_loads, j_loads_ns, j_dumps # j_dumps unused
from src.utils.image import get_image_bytes, get_raw_image_data 
from src.logger.logger import logger

# --- config.py ---
class Config:
    """Script-wide configuration (not supplier-specific).

    ----------------------------------------------------------
    По умолчанию используется SANDBOX/davidka/scenarios/*.json
    и престашоп store.davidka.net
    
    """

    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    SCENARIOS_DIR: Path = ENDPOINT / 'scenarios'
    
    SUPPLIERS_ENDPOINT: Path = __root__ / 'src' / 'suppliers' / 'list_of_suppliers'

    PRESTA_API_KEY: str = gs.credentials.prestashop.store_davidka_net.api_key
    PRESTA_API_DOMAIN: str = gs.credentials.prestashop.store_davidka_net.api_domain
    Product: PrestaProduct = PrestaProduct(PRESTA_API_KEY, PRESTA_API_DOMAIN)

    @property
    def scenarios_files(self) -> List[str]:
        return get_filenames_from_directory(self.SCENARIOS_DIR)
        
# --- end config.py ---


# Плохо
async def save_to_prestashop_async(f:ProductFields):
    """"""
    async with Config.Product as p:
        return await p.add_new_product_async(f)


async def process_supplier(supplier_prefix:str, page: 'Page', product_url:Optional[str] = None ) -> bool:
    """Название файла JSON соответствуют `supplier_prefix`, а  названия папок в системе - `supplier_alias` 
    Args:
        supplier_prefix (str): Префикс поставщика, соответствующий имени файла сценария (например, 'aliexpress', 'amazon', 'ebay').
        page (Page): Экземпляр страницы Pydoll для работы с веб-страницами.
        product_url (Optional[str], optional):  если указан, то обрабатывается только одна ссылка на товар.
    """
    ...
    
    try:
        supplier_alias:str = supplier_prefix.replace('.','_').replace('-','_')
        supplier_path:Path = Config.SUPPLIERS_ENDPOINT / supplier_alias 
        product_locators:SimpleNamespace = j_loads_ns(supplier_path / 'locators' / 'product.json')
        category_locators:SimpleNamespace = j_loads_ns(supplier_path / 'locators' / 'category.json')

        # --- dev ---
        scenarios_list: list = j_loads_ns(Config.SCENARIOS_DIR  / f'{supplier_prefix}.json') # <- ЧИТАЮ ИЗ ПАПКИ САНДБОХ
        
        graber_module_path:str  = f"src.suppliers.list_of_suppliers.{supplier_alias}.graber_via_pydoll"
    except Exception as ex:
        
        logger.error(f'Непредвиденная ошибка', ex)
        return False


    try:
       
        graber_module = importlib.import_module(graber_module_path)
        graber: 'Graber' = graber_module.Graber(supplier_prefix=supplier_prefix)
    except Exception as ex:
        logger.error(f"Failed to import module `graber` '{supplier_prefix}'", ex)
        return None    

    if product_url: # <- обработка одной ссылки
        f:ProductFields = await graber.grab_product_page(page, product_url)
        return await save_to_prestashop_async(f)
        
    for scenario in scenarios_list:
        products_urls_in_category:list = await graber.get_product_urls_from_category_page(scenario['url'], category_locators.product_links, page)

        if not products_urls_in_category:
            logger.debug(f'Вероятно, пустая категория ')
            print(scenario)
            continue # <- мб пустаая категория
            ...

        for product_url in products_urls_in_category:
            f:ProductFields = await graber.grab_product_page(page, product_url)
            await save_to_prestashop_async(f)
            
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
    scenario_files_to_process: List[Path] = []
    scenario_data: Dict[str, Any] | List[Dict[str, Any]] | None
    supplier_prefix_from_file: str

    # single_scenario: Dict[str,Any] # Объявляется внутри цикла, если необходимо

    if scenario_filename:

                            


    else:
        # Если имя файла не передано, обрабатываем все файлы из конфигурации.
        logger.info(f"Обработка всех файлов сценариев из директории: {Config.SCENARIOS_DIR}")
        for fname in Config.scenarios_files:
            scenario_files_to_process.append((Config.SCENARIOS_DIR / fname).resolve())

    if not scenario_files_to_process:
        logger.info("Нет файлов сценариев для обработки.")
        return

    for current_scenario_path in scenario_files_to_process:
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
