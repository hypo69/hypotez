## \file /src/gs.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""

Загрузка параметров программы, если не использовать хранилище keepass
=======================================================================
В этом случае константа `USE_ENV` устанаvливается в `True` и данные о ключах, апи, паролях и прочем будет загружаться их файлов .env`. 
Крайне неудобный способ. 
Не надо так делать!

"""
import header
from header import __root__
from src.utils.jjson import j_loads_ns
from pathlib import Path

gs = j_loads_ns(__root__ / 'src' / 'config.json')