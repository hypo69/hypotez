### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код предназначен для экспериментов по обучению моделей OpenAI и Gemini на данных с AliExpress. Он загружает заголовки товаров из файлов, читает системные инструкции и использует модели OpenAI и Gemini для получения ответов на основе этих заголовков.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `header`, `gs`, `OpenAIModel`, `GoogleGenerativeAi`, `recursively_get_filenames`, `read_text_file`, `csv2json_csv2dict`, `pprint`.

2. **Получение списка файлов с заголовками товаров**:
   - Функция `recursively_get_filenames` используется для получения списка файлов с заголовками товаров (`product_titles.txt`) из директории `aliexpress` в Google Drive.

3. **Чтение системной инструкции**:
   - Путь к файлу с системной инструкцией определяется переменной `system_instruction_path`.
   - Системная инструкция считывается из файла с использованием функции `read_text_file`.

4. **Инициализация моделей OpenAI и Gemini**:
   - Создаются экземпляры моделей `OpenAIModel` и `GoogleGenerativeAi` с использованием системной инструкции.

5. **Обработка файлов с заголовками товаров**:
   - Цикл `for file in product_titles_files:` перебирает каждый файл с заголовками товаров.
   - Заголовки товаров считываются из файла с использованием функции `read_text_file`.
   - Модели OpenAI и Gemini запрашиваются с использованием заголовков товаров, и ответы сохраняются в переменных `response_openai` и `response_gemini`.
   - Далее ответы обрабатываются (показано многоточием `...`).

Пример использования
-------------------------

```python
                ## \file /src/ai/openai/model/_experiments/model_train_for_aliexpress.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.ai.openai.model._experiments 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.ai.openai.model._experiments """



""" HERE SHOULD BE A DESCRIPTION OF THE MODULE OPERATION ! """

import header 

from src import gs
from src.llm import OpenAIModel, GoogleGenerativeAi
from src.utils.file import recursively_get_filenames, read_text_file
from src.utils.convertors import csv2json_csv2dict
from src.utils.printer import pprint

product_titles_files:list = recursively_get_filenames(gs.path.google_drive / 'aliexpress' / 'campaigns','product_titles.txt')
system_instruction_path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'
system_instruction: str = read_text_file(system_instruction_path)
openai = OpenAIModel(system_instruction = system_instruction)
gemini = GoogleGenerativeAi(system_instruction = system_instruction)
for file in product_titles_files:
    ...
    product_titles = read_text_file(file)
    response_openai = openai.ask(product_titles)
    response_gemini = gemini.ask(product_titles)
    ...

...