## \file /sandbox/davidka/experiments/8_run_suppliers_scenarios.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска сценариев поставщиков
================================================================
Сценарии позволеют получить товары по поставщикам и по категориям


 ```rst
 .. module:: sandbox.davidka.experiments.8_run_suppliers_scenarios
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
from src.webdriver import Driver, Firefox

from src.utils.jjson import  j_loads, j_loads_ns, j_dumps
from src.logger import logger


class Config:
    suppliers_list_for_process:list = [
        "amazon",
        "aliexpress",
        "ebay",
        "wallmart",
        "gearbest",

        ]

driver = Driver(Firefox, window_mode = 'normal')


