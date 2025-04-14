### **Анализ кода модуля `gpt_traigner.py`**

## \file /src/suppliers/chat_gpt/gpt_traigner.py

Модуль предназначен для обучения GPT-моделей на основе данных, собранных из чатов. Он включает в себя сбор данных, их очистку и подготовку для обучения модели.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код структурирован в класс `GPT_Traigner`, что облегчает его организацию и повторное использование.
    - Используется модуль `logger` для логирования ошибок.
    - Применение `j_dumps` и `j_loads_ns` для работы с JSON-файлами.
    - Использование `pathlib` для работы с путями к файлам.
    - Использован webdriver для сбора данных
- **Минусы**:
    - Отсутствует docstring для класса `GPT_Traigner`.
    - Не все методы класса `GPT_Traigner` имеют docstring.
    - Не везде указаны типы для переменных.
    - Местами не соблюдается PEP8 (пробелы вокруг операторов).
    - Не используется обработка исключений для потенциально проблемных мест (например, чтение файлов).
    - Дублирование кода (например, чтение `user_content` и `assistant_content`).
    - Переменная `sentiment` в `determine_sentiment` не используется, что делает функцию избыточной.
    - При конкатенации путей следует использовать `/`, а не `\\`.
    - Использование конкатенации строк вместо f-строк.
    - Не все переменные аннотированы.
    - Отсутсвуют комментарии, объясняющие логику работы кода.

**Рекомендации по улучшению:**

1.  **Добавить docstring для класса `GPT_Traigner`**.
2.  **Добавить docstring для метода `__init__`**.
3.  **Добавить аннотации типов для всех переменных и параметров функций**.
4.  **Удалить неиспользуемую переменную `sentiment` из функции `determine_sentiment`**.
5.  **Добавить обработку исключений при чтении файлов и выполнении операций с веб-драйвером**.
6.  **Использовать f-строки для форматирования строк**.
7.  **Заменить конкатенацию путей с помощью `/` на использование `pathlib` для обеспечения кроссплатформенности**.
8.  **Изменить способ получения данных из веб-драйвера, чтобы избежать дублирования кода**.
9.  **Добавить комментарии, объясняющие логику работы кода**.
10. **Удалить неиспользуемые импорты (если таковые имеются)**.
11. **Удалить неинформативные комментарии (`""""""`)**.

**Оптимизированный код:**

```python
                ## \file /src/suppliers/chat_gpt/gpt_traigner.py
# -*- coding: utf-8 -*-\n
#! .pyenv/bin/python3

"""
Модуль для обучения GPT-моделей на основе данных, собранных из чатов.
=======================================================================

Модуль содержит класс :class:`GPT_Traigner`, который используется для сбора,
обработки и сохранения данных для обучения моделей GPT.

Пример использования:
--------------------

>>> trainer = GPT_Traigner()
>>> trainer.dump_downloaded_conversations()
"""

import re
import argparse
import asyncio
from pathlib import Path
from itertools import zip_longest
from typing import List, Dict

import pandas as pd
from aioconsole import ainput

import header
from src import gs
from src.logger.logger import logger
from src.suppliers.chat_gpt import GptGs
from src.webdriver.driver import Driver, Chrome, Firefox, Edge
from src.ai.openai.model import Model
from src.utils.jjson import j_dumps, j_loads, j_loads_ns, clean_string
from src.utils.convertors import dict2csv, json2csv
from src.utils.printer import pprint

locator = j_loads_ns(gs.path.src / 'suppliers' / 'chat_gpt' / 'locators' / 'chat.json')


class GPT_Traigner:
    """
    Класс для сбора, обработки и сохранения данных для обучения моделей GPT.
    """
    driver = Driver(Chrome)

    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса GPT_Traigner.
        """
        self.gs = GptGs()

    def determine_sentiment(self, conversation_pair: Dict[str, str], sentiment: str = 'positive') -> str:
        """
        Определяет сентимент для пары реплик (положительный или отрицательный).

        Args:
            conversation_pair (Dict[str, str]): Пара реплик (пользователь - ассистент).
            sentiment (str, optional): Сентимент. По умолчанию 'positive'.

        Returns:
            str: 'positive', если сентимент задан, иначе 'negative'.
        """
        if sentiment:
            return "positive"
        else:
            return "negative"

    def save_conversations_to_jsonl(self, data: List[Dict], output_file: str) -> None:
        """
        Сохраняет список пар реплик в формате JSONL в файл.

        Args:
            data (List[Dict]): Список словарей с данными для сохранения.
            output_file (str): Путь к файлу для сохранения данных.
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(j_dumps(clean_string(item)) + "\n")
        except Exception as ex:
            logger.error(f'Ошибка при сохранении данных в файл {output_file}', ex, exc_info=True)

    def dump_downloaded_conversations(self) -> None:
        """
        Собирает реплики из HTML-файлов, скачанных со страницы ChatGPT,
        и сохраняет их в CSV и JSONL файлы.
        """
        conversation_directory: Path = Path(gs.path.google_drive / 'chat_gpt' / 'conversation')
        html_files: List[Path] = list(conversation_directory.glob("*.html")) # Получаем список HTML файлов
        all_data: List[pd.DataFrame] = []
        counter: int = 0

        for local_file_path in html_files:
            try:
                file_uri: str = local_file_path.resolve().as_uri()
                self.driver.get_url(file_uri)

                user_elements = self.driver.execute_locator(locator.user)
                assistant_elements = self.driver.execute_locator(locator.assistant)

                # Extract text content from user and assistant elements
                user_content: List[str] = [element.text for element in user_elements] if isinstance(user_elements, list) else [user_elements.text] if user_elements else []
                assistant_content: List[str] = [element.text for element in assistant_elements] if isinstance(assistant_elements, list) else [assistant_elements.text] if assistant_elements else []

                if not user_content and not assistant_content:
                    logger.error(f"Нет данных в файле: {local_file_path}")
                    continue

                for user_text, assistant_text in zip_longest(user_content, assistant_content):
                    if user_text and assistant_text:
                        data: Dict = {
                            'role': ['user', 'assistant'],
                            'content': [clean_string(user_text), clean_string(assistant_text)],
                            'sentiment': ['neutral', 'neutral']
                        }
                        all_data.append(pd.DataFrame(data))
                        print(f'{counter} - {local_file_path}')
                        counter += 1
            except Exception as ex:
                logger.error(f'Ошибка при обработке файла {local_file_path}', ex, exc_info=True)

        if all_data:
            all_data_df: pd.DataFrame = pd.concat(all_data, ignore_index=True)

            # Save all accumulated results to a single CSV file
            csv_file_path: Path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'
            all_data_df.to_csv(csv_file_path, index=False, encoding='utf-8')

            # Save all accumulated results to a single JSONL file
            jsonl_file_path: Path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.jsonl'
            all_data_df.to_json(jsonl_file_path, orient='records', lines=True, force_ascii=False)

            # Save raw conversations to a single line without formatting
            raw_conversations: str = ' '.join(all_data_df['content'].dropna().tolist())
            raw_file_path: Path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'raw_conversations.txt'
            try:
                with open(raw_file_path, 'w', encoding='utf-8') as raw_file:
                    raw_file.write(raw_conversations)
            except Exception as ex:
                logger.error(f'Ошибка при записи raw conversations в файл {raw_file_path}', ex, exc_info=True)

# Запуск сбора и обработки данных
try:
    traigner: GPT_Traigner = GPT_Traigner()
    traigner.dump_downloaded_conversations()
    model: Model = Model()
    model.stream_w(data_file_path=Path(gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'))
except Exception as ex:
    logger.error('Ошибка при выполнении основного кода', ex, exc_info=True)