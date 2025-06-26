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

# --- end config.py ---


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

        # --- dev ---
        scenarios_ns: SimpleNamespace = j_loads_ns(Config.SCENARIOS_DIR  / f'{supplier_prefix}.json') # <- ЧИТАЮ ИЗ ПАПКИ СЭНДБОХ
        graber_module_path:str  = f"src.suppliers.list_of_suppliers.{supplier_alias}.graber_via_pydoll"

    except Exception as ex:
        
        logger.error(f'Непредвиденная ошибка', ex)
        return False


    try:
        graber_module = importlib.import_module(graber_module_path)
        graber: 'Graber' = graber_module.Graber()
    except Exception as ex:
        logger.error(f"Failed to import module `graber` '{supplier_prefix}'", ex)
        return None    

    if product_url: # <- обработка одной ссылки
        f:ProductFields = await graber.grab_product_page(page, product_url)
        return await save_to_prestashop_async(f)
        

    async for product in graber.yield_all_scenarios(page):
        # Сохранение товара в PrestaShop
        result = await save_to_prestashop_async(product)
        if not result:
            logger.error(f"Ошибка при сохранении товара: {product.name}")
            continue
            
        logger.info(f"Товар успешно сохранен: {product.name}")

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

    browser = Chrome()  
    await browser.start()
    page = await browser.get_page()


    # --- Начало обработки сценариев ---
    if scenario_filename:
        scenario_files_to_process.append((Config.SCENARIOS_DIR / scenario_filename).resolve()) # Если передано имя файла, ищем его в директории сценариев
    
    else:
        # Если имя файла не передано, обрабатываем все файлы из конфигурации.
        logger.info(f"Обработка всех файлов сценариев из директории: {Config.SCENARIOS_DIR}")
        scenarios_files = get_filenames_from_directory(Config.SCENARIOS_DIR)
        for fname in scenarios_files:
            scenario_files_to_process.append((Config.SCENARIOS_DIR / fname).resolve())

    if not scenario_files_to_process:
        logger.info("Нет файлов сценариев для обработки.")
        ... 
        return

    for current_scenario_path in scenario_files_to_process:
        ... 
        logger.info(f"Начало обработки файла сценария: {current_scenario_path}")
        supplier_prefix: str = current_scenario_path.stem
        res = await process_supplier(supplier_prefix, page)


# if __name__ == '__main__':
#     asyncio.run(main('amazon.json'))

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

