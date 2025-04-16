## \file /sandbox/davidka/run_suppliers_scenarios.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: sandbox.davidka.run_suppliers_scenarios
	:platform: Windows, Unix
	:synopsis: Запуск сцеанриев различных поставщиков

"""
import asyncio
from types import SimpleNamespace
import header
from header import __root__
from src import gs
from src.suppliers.suppliers_list import *
from src.utils.jjson import j_loads

#---------------------------- supplier `HB` ---------------------
scenario:dict = j_loads(__root__ /  'src' / 'suppliers' / 'suppliers_list' / 'hb' / 'scenarios' / 'bodyspa.json')
hb:'Graber' = HbGraber()
asyncio.run(hb.process_supplier_scenarios_async('hb', scenario, 1))