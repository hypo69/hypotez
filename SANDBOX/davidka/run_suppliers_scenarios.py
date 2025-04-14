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
from src.utils.jjson import j_loads, j_loads_ns, j_dumps


#---------------------------- supplier `HB` ---------------------

scenario:SimpleNamespace = j_loads_ns(__root__ /  'src' / 'suppliers' / 'suppliers_list' / 'hb' / 'bodyspa.json')
hb:'Graber' = HbGraber()
hb.run_scenario(scenario)