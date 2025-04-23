## \file /sandbox/davidka/generate_links_for_trainig.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""

Модуль для генерации ссылок на страницы товаров с различных сайтов

```rst
.. module:: sandbox.davidka.generate_links_for_trainig
```
"""

import header
from src.llm.gemini import GoogleGenerativeAi

class Config:
    ENDPOINT = header.__root__ / 'SANDBOX' / 'davidka'
    mining_data_path = ENDPOINT / 'mining_data'
    task_description = ENDPOINT / 'tasks' / 'grab_product_page.md'

agent = GoogleGenerativeAi()

ca.
