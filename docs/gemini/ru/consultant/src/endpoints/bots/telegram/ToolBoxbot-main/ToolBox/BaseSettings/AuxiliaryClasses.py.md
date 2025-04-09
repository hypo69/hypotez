### **Анализ кода модуля `AuxiliaryClasses.py`**

## \file /hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/BaseSettings/AuxiliaryClasses.py

**Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на классы, что способствует структурированности.
    - Используются аннотации типов.
- **Минусы**:
    - Не хватает документации в формате docstring для классов и методов.
    - Отсутствует обработка исключений.
    - Не используется модуль `logger` для логирования.
    - Нарушение PEP8 в форматировании (пробелы вокруг операторов).
    - Использованы двойные кавычки вместо одинарных.

**Рекомендации по улучшению**:

1.  **Добавить документацию**:
    *   Добавить docstring для классов `keyboards` и `PromptsCompressor`, а также для всех их методов. Описать назначение каждого класса и метода, входные параметры, возвращаемые значения и возможные исключения.
2.  **Обработка исключений**:
    *   Добавить блоки `try...except` для обработки возможных исключений, например, при открытии и чтении файлов в методе `get_prompt`.
3.  **Логирование**:
    *   Использовать модуль `logger` для логирования ошибок и важных событий.
4.  **Форматирование кода**:
    *   Исправить форматирование в соответствии со стандартами PEP8 (добавить пробелы вокруг операторов присваивания).
    *   Заменить двойные кавычки на одинарные.
5.  **Использовать `j_loads`**:
    *   В методе `get_prompt` заменить стандартное открытие файла и `json.load` на `j_loads`.

**Оптимизированный код**:

```python
import json
import re
from telebot import types
from typing import List
from src.logger import logger  # Добавлен импорт logger
from pathlib import Path
from src.config import j_loads


# Класс для работы с клавиатурами
class keyboards:
    """
    Класс для создания различных типов клавиатур для Telegram бота.
    """

    # Protected
    # Клавиатура с двумя полями
    def _keyboard_two_blank(self, data: List[str], name: List[str]) -> types.InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру с кнопками, расположенными в два столбца.

        Args:
            data (List[str]): Список данных, которые будут передаваться в callback_data кнопок.
            name (List[str]): Список названий кнопок.

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
            name (List[str]): Список названий кнопок.

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
    Класс для работы с промптами, их сжатия и обработки.
    """

    def __init__(self):
        """
        Инициализирует класс PromptsCompressor, определяя размеры команд.
        """
        self.commands_size = [
            ["TOPIC", "TA", "TONE", "STRUCT", "LENGTH", "EXTRA"], ["TOPIC", "TA", "STYLE", "LENGTH"],
            ["TOPIC", "IDEA_NUM"], ["TYPE", "TOPIC", "TA", "LENGTH", "STYLE"],
            ["HEADLINE", "NUM"], ["TOPIC", "KEYWORDS", "INFO", "LENGTH"],
            ["TEXT", "LENGTH", "EXTRA"], ["TEXT", "RED_TYPE", "EXTRA"]
        ]

    # Promts get function
    def get_prompt(self, info: List[str], ind: int) -> str:
        """
        Извлекает промпт из файла и заменяет переменные значения.

        Args:
            info (List[str]): Список значений для подстановки в промпт.
            ind (int): Индекс промпта в файле.

        Returns:
            str: Сформированный промпт.
        
        Raises:
            FileNotFoundError: Если файл prompts.json не найден.
            json.JSONDecodeError: Если файл prompts.json содержит некорректный JSON.
            Exception: При возникновении других ошибок.
        """
        try:
            commands = j_loads('ToolBox/BaseSettings/prompts.json')['commands'][ind]
            # with open('ToolBox/BaseSettings/prompts.json', 'r') as file:
            #     commands = json.load(file)['commands'][ind]
            for i, el in enumerate(self.commands_size[ind]):
                commands = commands.replace(f'[{el}]', info[i])
            return commands
        except FileNotFoundError as ex:
            logger.error('File prompts.json not found', ex, exc_info=True)  # Логирование ошибки
            return ''
        except json.JSONDecodeError as ex:
            logger.error('Incorrect JSON format in prompts.json', ex, exc_info=True)  # Логирование ошибки
            return ''
        except Exception as ex:
            logger.error('Error while getting prompt', ex, exc_info=True)  # Логирование ошибки
            return ''

    # HTML tags insert function
    @staticmethod
    def html_tags_insert(response: str) -> str:
        """
        Вставляет HTML-теги в текст ответа для форматирования.

        Args:
            response (str): Текст ответа.

        Returns:
            str: Текст ответа с HTML-тегами.
        """
        patterns = [(r'#### (.*?)\n', r'<b><u>\1</u></b>\n'),
                    (r'### (.*?)\n', r'<u>\1</u>\n'),
                    (r'\*\*(.*?)\*\*', r'<b>\1</b>'),
                    (r'\*(.*?)\*', r'<i>\1</i>'),
                    (r'```(\w+)?\n(.*?)\n```', r'<pre><code>\n\2\n</code></pre>'),
                    (r'`(.*?)`', r'<code>\1</code>')]
        for pattern in patterns:
            response = re.sub(pattern[0], pattern[1], response, flags=re.DOTALL)
        return response