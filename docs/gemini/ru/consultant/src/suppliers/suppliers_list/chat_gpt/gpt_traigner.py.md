### **Анализ кода модуля `gpt_traigner.py`**

## \file /src/suppliers/chat_gpt/gpt_traigner.py

Модуль предназначен для обучения GPT-моделей на основе данных, полученных из чата. Он включает в себя сбор данных с веб-страниц, их очистку и сохранение в различных форматах для дальнейшего использования в обучении моделей.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код разбит на функции, что улучшает читаемость и упрощает поддержку.
  - Используется модуль `logger` для логирования ошибок.
  - Применяются `j_loads_ns` и `j_dumps` для работы с JSON, что соответствует стандартам проекта.
  - Используется аннотация типов.
- **Минусы**:
  - Отсутствует docstring для класса `GPT_Traigner` и его методов `__init__`, `determine_sentiment`, что затрудняет понимание назначения класса и методов.
  - Не все переменные аннотированы типами.
  - Не используется `ex` в блоке except.
  - Не все docstring переведены на русский язык.
  - Лишние импорты в коде.
  - Дублирование кода, которое снижает читаемость и усложняет поддержку.
  - Не все переменные аннотированы типами.
  - Не все docstring переведены на русский язык.
  - Отсутствует обработка исключений при работе с файлами.

**Рекомендации по улучшению:**

1.  **Добавить docstring для класса `GPT_Traigner` и его методов `__init__`, `determine_sentiment`**:

    -   Описать назначение класса и каждого метода, их аргументы, возвращаемые значения и возможные исключения.
    -   Пример:

        ```python
        class GPT_Traigner:
            """
            Класс для обучения GPT-моделей на основе данных из чата.

            Args:
                Нет аргументов.

            """

            driver = Driver(Chrome)

            def __init__(self):
                """
                Инициализация экземпляра класса GPT_Traigner.

                Args:
                    Нет аргументов.

                Returns:
                    None
                """
                self.gs = GptGs()
        ```

2.  **Проверить и добавить аннотации типов для всех переменных и параметров функций.**

3.  **В блоках `except` использовать `ex` вместо `e` для обозначения исключения.**

4.  **Перевести все docstring на русский язык.**

5.  **Удалить лишние импорты.**

    -   Удалить неиспользуемые импорты для улучшения читаемости кода.

6.  **Добавить обработку исключений при работе с файлами.**

    -   Использовать блоки `try-except` при открытии, чтении и записи файлов для обработки возможных ошибок.
    -   Пример:

        ```python
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(j_dumps(clean_string(item)) + "\\n")
        except Exception as ex:
            logger.error(f"Ошибка при записи в файл: {ex}", exc_info=True)
        ```

7. **Удалить дублирование кода**
8.  **Изменить возвращаемое значение функции `determine_sentiment`**

**Оптимизированный код:**

```python
## \file /src/suppliers/chat_gpt/gpt_traigner.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для обучения GPT-моделей на основе данных из чата
=============================================================

Модуль содержит класс :class:`GPT_Traigner`, который используется для сбора и обработки данных
из чата для обучения GPT-моделей.
"""

import re
import argparse
import asyncio
from pathlib import Path
from itertools import zip_longest

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
    Класс для обучения GPT-моделей на основе данных из чата.

    Args:
        Нет аргументов.

    """
    driver = Driver(Chrome)

    def __init__(self) -> None:
        """
        Инициализация экземпляра класса GPT_Traigner.

        Args:
            Нет аргументов.

        Returns:
            None
        """
        self.gs = GptGs()

    def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str | None = 'positive') -> str:
        """
        Определяет сентимент (тональность) для пары сообщений в диалоге.

        Args:
            conversation_pair (dict[str, str]): Пара сообщений (пользователь и ассистент).
            sentiment (str | None, optional): Предполагаемый сентимент. По умолчанию 'positive'.

        Returns:
            str: Сентимент ('positive' или 'negative').

        """
        if sentiment:
            return 'positive'
        else:
            return 'negative'

    def save_conversations_to_jsonl(self, data: list[dict], output_file: str) -> None:
        """
        Сохраняет список диалогов в формате JSONL в указанный файл.

        Args:
            data (list[dict]): Список диалогов, где каждый диалог представлен словарем.
            output_file (str): Путь к файлу для сохранения данных.

        Returns:
            None

        Raises:
            Exception: Если возникает ошибка при записи в файл.
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(j_dumps(clean_string(item)) + "\n")
        except Exception as ex:
            logger.error(f'Ошибка при записи в файл: {ex}', ex, exc_info=True)

    def dump_downloaded_conversations(self) -> None:
        """
        Собирает диалоги со страниц chatgpt, загружает их и сохраняет в файлы.

        Args:
            Нет аргументов.

        Returns:
            None
        """
        conversation_directory: Path = Path(gs.path.google_drive / 'chat_gpt' / 'conversation')
        html_files: list[Path] = list(conversation_directory.glob("*.html"))

        all_data: list[pd.DataFrame] = []
        counter: int = 0  # <- counter

        for local_file_path in html_files:
            # Get the HTML content
            file_uri: str = local_file_path.resolve().as_uri()
            self.driver.get_url(file_uri)

            user_elements = self.driver.execute_locator(locator['user'])
            assistant_elements = self.driver.execute_locator(locator['assistant'])

            user_content: list[str] | None = [element.text for element in user_elements] if isinstance(user_elements, list) else [user_elements.text] if user_elements else None
            assistant_content: list[str] | None = [element.text for element in assistant_elements] if isinstance(assistant_elements, list) else [assistant_elements.text] if assistant_elements else None

            if not user_content and not assistant_content:
                logger.error(f"Где данные?")
                continue

            for user_text, assistant_text in zip_longest(user_content, assistant_content):
                if user_text and assistant_text:
                    data: dict[str, list[str]] = {
                        'role': ['user', 'assistant'],
                        'content': [clean_string(user_text), clean_string(assistant_text)],
                        'sentiment': ['neutral', 'neutral']
                    }
                    all_data.append(pd.DataFrame(data))
                    print(f'{counter} - {local_file_path}')
                    counter += 1

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
                logger.error(f'Ошибка при записи в raw_file: {ex}', ex, exc_info=True)


traigner: GPT_Traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()
model: Model = Model()
model.stream_w(data_file_path=Path(gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'))