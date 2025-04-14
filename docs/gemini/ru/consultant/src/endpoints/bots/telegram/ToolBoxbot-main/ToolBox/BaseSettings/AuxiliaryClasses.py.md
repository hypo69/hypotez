### **Анализ кода модуля `AuxiliaryClasses.py`**

## \file /hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/BaseSettings/AuxiliaryClasses.py

**Качество кода**:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на классы, что облегчает его понимание и поддержку.
    - Использование `types` из `telebot` для создания клавиатур.
    - Применение статического метода `html_tags_insert` в классе `PromptsCompressor` выглядит уместным.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров и возвращаемых значений в некоторых функциях.
    - Не используются логирование ошибок.
    - Не везде соблюдены пробелы вокруг операторов.
    - Отсутствуют docstring для классов и методов.
    - Использование `open` и `json.load` для чтения JSON. Следует использовать `j_loads`.
    - Нет обработки исключений.
    - Жестко закодированный путь к файлу `prompts.json`.
    - Не везде используется именование переменных, соответствующее PEP 8 (например, `ind` вместо `index`).

**Рекомендации по улучшению**:

1.  **Добавить docstring**:
    *   Для всех классов и методов добавить docstring, описывающие их назначение, параметры и возвращаемые значения.
2.  **Добавить аннотации типов**:
    *   Для всех параметров функций и возвращаемых значений добавить аннотации типов.
3.  **Использовать логирование**:
    *   Добавить логирование для отладки и мониторинга работы кода.
4.  **Обработка исключений**:
    *   Добавить блоки `try...except` для обработки возможных исключений, например, при открытии файла или обработке данных.
5.  **Использовать `j_loads`**:
    *   Заменить `open` и `json.load` на `j_loads` для чтения JSON-файлов.
6.  **Изменить жестко закодированный путь к файлу**:
    *   Заменить жестко закодированный путь к файлу `prompts.json` на относительный путь или использовать переменные окружения.
7.  **Переименовать переменные**:
    *   Использовать более понятные имена переменных, например, `index` вместо `ind`.
8.  **Добавить пробелы вокруг операторов**:
    *   Добавить пробелы вокруг операторов присваивания и сравнения.
9.  **Улучшить структуру `html_tags_insert`**:

    *   Сделать функцию `html_tags_insert` более читаемой, разделив регулярные выражения на отдельные переменные и добавив комментарии к каждому из них.

**Оптимизированный код**:

```python
import json
import re
from telebot import types
from typing import List, Optional
from pathlib import Path

from src.logger import logger
from src.config import config


# Класс для работы с клавиатурами
class Keyboards:
    """
    Класс для создания различных типов клавиатур для Telegram-ботов.
    """

    # Protected
    # Клавиатура с двумя полями
    def _keyboard_two_blank(self, data: List[str], name: List[str]) -> types.InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру с кнопками в два столбца.

        Args:
            data (List[str]): Список callback_data для кнопок.
            name (List[str]): Список текста для кнопок.

        Returns:
            types.InlineKeyboardMarkup: Объект inline-клавиатуры.
        """
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [types.InlineKeyboardButton(str(name[i]), callback_data=str(data[i])) for i in range(len(data))]
        if len(buttons) % 2 == 0:
            [keyboard.add(buttons[i], buttons[i + 1]) for i in range(0, len(buttons), 2)]
        else:
            [keyboard.add(buttons[i], buttons[i + 1]) for i in range(0, len(buttons) - 1, 2)]
            keyboard.add(buttons[-1])
        return keyboard

    def _reply_keyboard(self, name: List[str]) -> types.ReplyKeyboardMarkup:
        """
        Создает reply-клавиатуру с кнопками.

        Args:
            name (List[str]): Список текста для кнопок.

        Returns:
            types.ReplyKeyboardMarkup: Объект reply-клавиатуры.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(el) for el in name]
        [markup.add(btn) for btn in buttons]
        return markup


# Класс для сжатия промптов
class PromptsCompressor:
    """
    Класс для получения и обработки промптов из JSON-файла.
    """

    def __init__(self) -> None:
        """
        Инициализирует класс PromptsCompressor.
        """
        self.commands_size = [
            ["TOPIC", "TA", "TONE", "STRUCT", "LENGTH", "EXTRA"],
            ["TOPIC", "TA", "STYLE", "LENGTH"],
            ["TOPIC", "IDEA_NUM"],
            ["TYPE", "TOPIC", "TA", "LENGTH", "STYLE"],
            ["HEADLINE", "NUM"],
            ["TOPIC", "KEYWORDS", "INFO", "LENGTH"],
            ["TEXT", "LENGTH", "EXTRA"],
            ["TEXT", "RED_TYPE", "EXTRA"]
        ]

    def get_prompt(self, info: List[str], index: int) -> str:
        """
        Получает промпт из JSON-файла и заменяет переменные.

        Args:
            info (List[str]): Список значений для замены в промпте.
            index (int): Индекс промпта в JSON-файле.

        Returns:
            str: Готовый промпт.
        
        Raises:
            FileNotFoundError: Если файл prompts.json не найден.
            KeyError: Если в файле отсутствует ключ 'commands'.
            IndexError: Если индекс выходит за границы списка команд.
        """
        file_path = Path(config.BASE_DIR) / 'ToolBox/BaseSettings/prompts.json' #  config.BASE_DIR #  Путь к файлу с промптами

        try:
            with open(file_path, 'r', encoding='utf-8') as file: #  Открываем файл с промптами
                commands = json.load(file)['commands'][index] #  Загружаем команды из файла
        except FileNotFoundError as ex:
            logger.error(f'File not found: {file_path}', ex, exc_info=True) # Логируем ошибку, если файл не найден
            return ""
        except KeyError as ex:
            logger.error(f'Key "commands" not found in {file_path}', ex, exc_info=True) # Логируем ошибку, если ключ "commands" не найден
            return ""
        except IndexError as ex:
            logger.error(f'Index {index} out of range in {file_path}', ex, exc_info=True) # Логируем ошибку, если индекс вне диапазона
            return ""
        except Exception as ex:
            logger.error(f'Error while reading prompts from {file_path}', ex, exc_info=True) # Логируем любую другую ошибку
            return ""

        for i, el in enumerate(self.commands_size[index]): #  Заменяем переменные в промпте
            commands = commands.replace(f"[{el}]", info[i])
        return commands

    @staticmethod
    def html_tags_insert(response: str) -> str:
        """
        Вставляет HTML-теги в текст ответа.

        Args:
            response (str): Текст ответа.

        Returns:
            str: Текст ответа с HTML-тегами.
        """
        #  Регулярное выражение для заголовков H4
        h4_pattern = r'#### (.*?)\n'
        #  HTML-тег для заголовков H4
        h4_replacement = r'<b><u>\1</u></b>\n'
        #  Регулярное выражение для заголовков H3
        h3_pattern = r'### (.*?)\n'
        #  HTML-тег для заголовков H3
        h3_replacement = r'<u>\1</u>\n'
        #  Регулярное выражение для жирного текста
        bold_pattern = r'\*\*(.*?)\*\*'
        #  HTML-тег для жирного текста
        bold_replacement = r'<b>\1</b>'
        #  Регулярное выражение для курсивного текста
        italic_pattern = r'\*(.*?)\*'
        #  HTML-тег для курсивного текста
        italic_replacement = r'<i>\1</i>'
        #  Регулярное выражение для блоков кода
        code_block_pattern = r'```(\w+)?\n(.*?)\n```'
        #  HTML-тег для блоков кода
        code_block_replacement = r'<pre><code>\n\2\n</code></pre>'
        #  Регулярное выражение для строчного кода
        inline_code_pattern = r'`(.*?)`'
        #  HTML-тег для строчного кода
        inline_code_replacement = r'<code>\1</code>'

        patterns = [(h4_pattern, h4_replacement),
                    (h3_pattern, h3_replacement),
                    (bold_pattern, bold_replacement),
                    (italic_pattern, italic_replacement),
                    (code_block_pattern, code_block_replacement),
                    (inline_code_pattern, inline_code_replacement)]
        for pattern, replacement in patterns:
            response = re.sub(pattern, replacement, response, flags=re.DOTALL)
        return response