## \file /sandbox/davidka/build_hypotez_train_data_from_files.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора датасета для обучения модели 
=====================================================


```rst
.. module:: sandbox.davidka.build_hypotez_train_data_from_files
```
"""

import header
from src import gs
from src.endpoints.hypo69.code_assistant import CodeAssistant

ca = CodeAssistant()
ca.