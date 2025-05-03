## \file /sandbox/davidka/crawler_google_search_api.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль получения ссылок на товары 
=====================================================
В папке `random_urls` находятся словари сгенерированные gemini, в который есть наименования категорий. 
По этим категориям я запускаю driver_use и собираю ссылки, которые мне вернула поисковая система

```rst
.. module:: sandbox.davidka.crawler_google_search_api
```
"""
import asyncio
import random
from pathlib import Path

import header
from header import __root__
from src import gs
from src.webdriver.llm_driver.simple_driver import SimpleDriver
from src.utils.jjson import j_loads, j_dumps
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory
from src.utils.url import get_domain
from src.utils.string.ai_string_utils import normalize_answer
from src.utils.printer import pprint as print
from src.logger import logger