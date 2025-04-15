## \file /sandbox/davidka/run_suppliers_scenarios.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: sandbox.davidka.run_suppliers_scenarios
	:platform: Windows, Unix
	:synopsis: Запуск сцеанриев различных поставщиков

"""
from types import SimpleNamespace
import header
from header import __root__
from src import gs
#from src.suppliers.graber import Graber
from src.suppliers.suppliers_list import *
from src.suppliers.suppliers_list.hb.scenario import get_list_products_in_category
from src.utils.jjson import j_loads

#---------------------------- supplier `HB` ---------------------
scenario:SimpleNamespace = j_loads(__root__ /  'src' / 'suppliers' / 'suppliers_list' / 'hb' / 'scenarios' / 'bodyspa.json')
hb:'Graber' = HbGraber()
hb.run_scenarios('hb', scenario, get_list_products_in_category)