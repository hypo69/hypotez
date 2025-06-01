## \file /sandbox/davidka/experiments/7_build_directories_for_new_suppliers.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль создает директории для новых поставщиков и синхронизирует их с Google Spreadsheet.

================================================================
Скрипт загружает информацию о поставщиках из Google Spreadsheet,
сравнивает список поставщиков с существующими директориями,
при необходимости добавляет новых поставщиков в Spreadsheet,
извлекает ID существующих и обрабатывает данные.

 ```rst
 .. module:: sandbox.davidka.experiments.7_build_directories_for_new_suppliers
 ```
"""
import shutil 
import re
import sys
import argparse
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Dict, Any, List, Tuple


import header
from header import __root__
from src import gs
from src.utils.jjson import  j_loads, j_loads_ns, j_dumps
from src.logger import logger

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    # для создания новых поставщиков нужно копиривать hb  (ШАБЛОН) 
    # в папку suppliers_list/<supplier_name>
    template_directory:str = 'hb' # Папка шаблона для создания новых поставщиков. 

    # Список поставщиков, для которых нужно создать директории
    suppliers: list[str] = [
        "ads-tec-iit.com",
        "apple.com",
        "atlascopco.com",
        "bucketmaster.com.cn",
        "cisco.com",
        "de-de.ring.com",
        "de.hexcel.com",
        "de.rs-online.com",
        "denaliweld.com",
        "dewesoft.com",
        "elektrometal.eu",
        "findernet.com",
        "fresubin.com",
        "generex.de",
        "georgin.com",
        "imos3d.com",
        "induprogress.pl",
        "industrierat-west.de",
        "it.alwsci.com",
        "it.defelsko.com",
        "it.jarvis-smart.com",
        "it.superb-heater.com",
        "it.thermo-heater.com",
        "janitza.com",
        "jungbluth.com",
        "ledodm.com",
        "leybold.com",
        "mecalux.it",
        "megatron.de",
        "megger.com",
        "mococonnectors.com",
        "mordorintelligence.it",
        "omnipod.com",
        "opel.de",
        "pfannenberg.com",
        "pl.dmgmori.com",
        "plm.sw.siemens.com",
        "prebiel.pl",
        "prusa3d.com",
        "ridgid.eu",
        "sensysmagnetometer.com",
        "shop.loxone.com",
        "shop.scheppach.com",
        "sigmaaldrich.com",
        "sphinxitalia.it",
        "vidaxl.pl",
        "zebra.com"
    ]




# def build_directories_for_new_suppliers(suppliers: list[str]) -> bool:
#     """
#     Создает директории для новых поставщиков и синхронизирует их с Google Spreadsheet.
#     Args:
#         suppliers(list): Список поставщиков.
#     """
#     suppliers_directory: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'
#     template_path: Path = suppliers_directory / Config.template_directory

#     if not template_path.exists():
#         logger.error(f"Template directory does not exist: {template_path}")
#         return False

#     for supplier in suppliers:
#         sanitized_name = supplier.lower().strip()
#         supplier_path: Path = suppliers_directory / sanitized_name

#         if supplier_path.exists():
#             logger.info(f"Directory already exists: {supplier_path}")
#             continue

#         try:
#             shutil.copytree(template_path, supplier_path)
#             logger.info(f"Created directory for supplier: {supplier_path}")
            
#         except Exception as ex:
#             logger.error(f"Failed to create directory for {supplier}", ex)
#             return False

#     return True


def build_directories_for_new_suppliers(suppliers: list[str]) -> bool:
    """
    Создает директории для новых поставщиков и синхронизирует их с Google Spreadsheet.
    Также создает JSON-файлы в папке `scenarios` с именами вида <поставщик>.json, если они не существуют.

    Args:
        suppliers (list): Список поставщиков.

    Returns:
        bool: True если все успешно, False если возникли ошибки.
    """
    suppliers_directory: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list'
    template_path: Path = suppliers_directory / Config.template_directory
    scenarios_directory: Path = __root__ / 'SANDBOX' / 'davidka' / 'scenarios'

    if not template_path.exists():
        logger.error(f"Template directory does not exist: {template_path}")
        return False

    scenarios_directory.mkdir(parents=True, exist_ok=True)

    for supplier in suppliers:
        sanitized_name = supplier.lower().strip()
        supplier_path: Path = suppliers_directory / sanitized_name
        scenario_file_path: Path = scenarios_directory / f"{sanitized_name}.json"

        if not supplier_path.exists():
            try:
                shutil.copytree(template_path, supplier_path)
                logger.info(f"Created directory for supplier: {supplier_path}")
            except Exception as ex:
                logger.error(f"Failed to create directory for {supplier}", ex)
                return False
        else:
            logger.info(f"Directory already exists: {supplier_path}")

        if not scenario_file_path.exists():
            try:
                scenario_data: Dict[str, Any] = {
                    "supplier": sanitized_name,
                    "status": "new",
                    "created_at": None,
                    "metadata": {}
                }
                j_dumps(scenario_data, scenario_file_path)
                logger.info(f"Created scenario file: {scenario_file_path}")
            except Exception as ex:
                logger.error(f"Failed to create scenario file for {supplier}", ex)
                return False
        else:
            logger.info(f"Scenario file already exists: {scenario_file_path}")

    return True

if __name__ == "__main__":
    try:
        build_directories_for_new_suppliers(Config.suppliers)
    except Exception as e:
        logger.error("Ошибка при выполнении build_directories_for_new_suppliers", e)

