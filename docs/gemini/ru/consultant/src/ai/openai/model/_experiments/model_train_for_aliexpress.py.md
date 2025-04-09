### **Анализ кода модуля `_experiments`**

#### **Качество кода**:
- **Соответствие стандартам**: 4/10
- **Плюсы**:
    - Использование функций для чтения файлов и рекурсивного поиска.
    - Наличие импортов, указывающих на использование OpenAI и Gemini моделей.
- **Минусы**:
    - Отсутствие docstring для модуля, что затрудняет понимание его назначения.
    - Неинформативные и повторяющиеся docstring.
    - Не используются аннотации типов.
    - Не используется логирование.
    - В коде используются старые конструкции, такие как `list`. Необходимо заменить на `list[]`.
    - Нет обработки исключений.

#### **Рекомендации по улучшению**:

1.  **Документирование модуля**:
    - Добавить docstring в начале файла с описанием назначения модуля, его основных функций и примеров использования.
2.  **Документирование переменных**:
    - Добавить аннотацию типа для всех переменных.
3.  **Улучшение комментариев**:
    - Заменить существующие комментарии на более информативные и конкретные, описывающие функциональность каждой части кода.
3.  **Обработка исключений**:
    - Добавить блоки try-except для обработки возможных ошибок при чтении файлов или обращении к AI-моделям, логируя ошибки с использованием `logger.error`.
4.  **Использование `j_loads` или `j_loads_ns`**:
    - Если `system_instruction_path` указывает на JSON или конфигурационный файл, использовать `j_loads` или `j_loads_ns` для его чтения.
5.  **Улучшение читаемости**:
    - Улучшить читаемость кода, добавив пробелы вокруг операторов присваивания и другие элементы форматирования в соответствии с PEP8.

#### **Оптимизированный код**:

```python
## \file /src/ai/openai/model/_experiments/model_train_for_aliexpress.py
# -*- coding: utf-8 -*-

"""
Модуль для экспериментов с моделями OpenAI и Gemini для генерации заголовков товаров Aliexpress.
==========================================================================================

Модуль предназначен для загрузки заголовков товаров из файлов, расположенных в Google Drive,
и использования моделей OpenAI и Gemini для создания улучшенных версий этих заголовков.

Пример использования:
----------------------

>>> from src.ai import OpenAIModel, GoogleGenerativeAI
>>> from src.utils.file import recursively_get_filenames, read_text_file
>>> from src import gs
>>> system_instruction_path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'
>>> system_instruction = read_text_file(system_instruction_path)
>>> openai = OpenAIModel(system_instruction=system_instruction)
>>> gemini = GoogleGenerativeAI(system_instruction=system_instruction)
>>> product_titles_files = recursively_get_filenames(gs.path.google_drive / 'aliexpress' / 'campaigns', 'product_titles.txt')
>>> for file in product_titles_files:
>>>     product_titles = read_text_file(file)
>>>     response_openai = openai.ask(product_titles)
>>>     response_gemini = gemini.ask(product_titles)
>>>     print(f"OpenAI Response: {response_openai}")
>>>     print(f"Gemini Response: {response_gemini}")
"""

from src.logger import logger # Импорт модуля логгирования
from pathlib import Path
from typing import List

from src import gs
from src.ai import OpenAIModel, GoogleGenerativeAI
from src.utils.file import recursively_get_filenames, read_text_file
from src.utils.convertors import csv2json_csv2dict
from src.utils.printer import pprint


product_titles_files: List[Path] = recursively_get_filenames(gs.path.google_drive / 'aliexpress' / 'campaigns', 'product_titles.txt') # Получаем список файлов с заголовками товаров
system_instruction_path: Path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt' # Путь к файлу с системными инструкциями
system_instruction: str = read_text_file(system_instruction_path) # Считываем системные инструкции из файла

openai = OpenAIModel(system_instruction = system_instruction) # Инициализация модели OpenAI
gemini = GoogleGenerativeAI(system_instruction = system_instruction) # Инициализация модели Gemini

for file in product_titles_files: # Итерируемся по списку файлов
    try:
        product_titles: str | None = read_text_file(file) # Читаем заголовки товаров из файла
        if product_titles:
            response_openai: str | None = openai.ask(product_titles) # Получаем ответ от OpenAI
            response_gemini: str | None = gemini.ask(product_titles) # Получаем ответ от Gemini
            logger.info(f'OpenAI Response: {response_openai}') # Логируем ответ OpenAI
            logger.info(f'Gemini Response: {response_gemini}') # Логируем ответ Gemini
        else:
            logger.warning(f'No product titles found in {file}') # Логируем предупреждение, если заголовки не найдены
    except Exception as ex:
        logger.error(f'Error processing file {file}', ex, exc_info=True) # Логируем ошибку при обработке файла