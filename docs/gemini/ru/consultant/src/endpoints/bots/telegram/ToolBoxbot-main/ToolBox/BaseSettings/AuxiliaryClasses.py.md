### **Анализ кода модуля `AuxiliaryClasses.py`**

## \file /hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/BaseSettings/AuxiliaryClasses.py

**Качество кода:**
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на классы, что способствует лучшей организации и повторному использованию.
    - Используются аннотации типов, что улучшает читаемость и упрощает отладку.
- **Минусы**:
    - Отсутствует подробная документация для классов и методов.
    - Не используются логирование для отслеживания ошибок и работы программы.
    - Жестко заданный путь к файлу `prompts.json`.
    - Не везде используются одинарные кавычки.
    - Нет обработки исключений.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    *   Добавить подробные docstring для каждого класса и метода, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения.
2.  **Использовать логирование**:
    *   Внедрить логирование для записи информации о работе программы и отслеживания ошибок.
3.  **Обработка исключений**:
    *   Добавить блоки `try...except` для обработки возможных исключений, например, при открытии и чтении файла `prompts.json`.
4.  **Изменить способ хранения `prompts.json`**:
    *   Изменить способ хранения файла `prompts.json`, чтобы путь к нему не был жестко задан. Можно использовать переменные окружения или аргументы командной строки для указания пути.
5.  **Перейти на одинарные кавычки**:
    *   Везде использовать одинарные кавычки.
6. **Документировать возвращаемые типы**
    *   Добавить аннотации типов в методах _reply_keyboard
7. **Соблюдать PEP8**
    *   Проверить на соответствие стандарту оформления кода PEP8

**Оптимизированный код:**

```python
import json
import re
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List
from src.logger import logger  # Добавлен импорт logger


# Keyboard class
class Keyboards:
    """
    Класс для создания клавиатур Telegram бота.
    """

    # Protected
    # Keyboard with 2 fields
    def _keyboard_two_blank(self, data: list[str], name: list[str]) -> InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру с кнопками в два столбца.

        Args:
            data (list[str]): Список callback_data для кнопок.
            name (list[str]): Список текстов для кнопок.

        Returns:
            InlineKeyboardMarkup: Объект inline-клавиатуры.

        Raises:
            Exception: Если возникает ошибка при создании клавиатуры.

        Example:
            >>> data = ['1', '2', '3', '4']
            >>> name = ['Button 1', 'Button 2', 'Button 3', 'Button 4']
            >>> keyboard = Keyboards()._keyboard_two_blank(data, name)
        """
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = [InlineKeyboardButton(str(name[i]), callback_data=str(data[i])) for i in range(len(data))]
        if len(buttons) % 2 == 0:
            [keyboard.add(buttons[i], buttons[i + 1]) for i in range(0, len(buttons), 2)]
        else:
            [keyboard.add(buttons[i], buttons[i + 1]) for i in range(0, len(buttons) - 1, 2)]
            keyboard.add(buttons[-1])
        return keyboard

    def _reply_keyboard(self, name: list[str]) -> ReplyKeyboardMarkup:
        """
        Создает reply-клавиатуру с кнопками в один столбец.

        Args:
            name (list[str]): Список текстов для кнопок.

        Returns:
            ReplyKeyboardMarkup: Объект reply-клавиатуры.

        Raises:
            Exception: Если возникает ошибка при создании клавиатуры.

        Example:
            >>> name = ['Button 1', 'Button 2', 'Button 3']
            >>> keyboard = Keyboards()._reply_keyboard(name)
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [KeyboardButton(el) for el in name]
        [markup.add(btn) for btn in buttons]
        return markup


# Prompts compression class
class PromptsCompressor:
    """
    Класс для сжатия и обработки промптов.
    """

    def __init__(self):
        """
        Инициализирует класс PromptsCompressor.
        """
        self.commands_size = [
            ['TOPIC', 'TA', 'TONE', 'STRUCT', 'LENGTH', 'EXTRA'], ['TOPIC', 'TA', 'STYLE', 'LENGTH'],
            ['TOPIC', 'IDEA_NUM'], ['TYPE', 'TOPIC', 'TA', 'LENGTH', 'STYLE'],
            ['HEADLINE', 'NUM'], ['TOPIC', 'KEYWORDS', 'INFO', 'LENGTH'],
            ['TEXT', 'LENGTH', 'EXTRA'], ['TEXT', 'RED_TYPE', 'EXTRA']
        ]

    def get_prompt(self, info: list[str], ind: int) -> str:
        """
        Извлекает и формирует промпт на основе предоставленной информации.

        Args:
            info (list[str]): Список информации для подстановки в промпт.
            ind (int): Индекс промпта в файле.

        Returns:
            str: Сформированный промпт.

        Raises:
            FileNotFoundError: Если файл prompts.json не найден.
            json.JSONDecodeError: Если файл prompts.json содержит некорректный JSON.
            KeyError: Если в файле prompts.json отсутствует ключ 'commands'.
            Exception: Если возникает другая ошибка при чтении файла.

        Example:
            >>> info = ['topic', 'ta', 'tone', 'struct', 'length', 'extra']
            >>> ind = 0
            >>> prompt = PromptsCompressor().get_prompt(info, ind)
        """
        try:
            with open('ToolBox/BaseSettings/prompts.json', 'r', encoding='utf-8') as file:
                commands = json.load(file)['commands'][ind]
            for i, el in enumerate(self.commands_size[ind]):
                commands = commands.replace(f'[{el}]', info[i])
            return commands
        except FileNotFoundError as ex:
            logger.error('Файл prompts.json не найден', ex, exc_info=True)  # Добавлено логирование
            return ''
        except json.JSONDecodeError as ex:
            logger.error('Файл prompts.json содержит некорректный JSON', ex, exc_info=True)  # Добавлено логирование
            return ''
        except KeyError as ex:
            logger.error('В файле prompts.json отсутствует ключ \'commands\'', ex, exc_info=True)  # Добавлено логирование
            return ''
        except Exception as ex:
            logger.error('Произошла ошибка при чтении файла prompts.json', ex, exc_info=True)  # Добавлено логирование
            return ''

    @staticmethod
    def html_tags_insert(response: str) -> str:
        """
        Вставляет HTML-теги в текст ответа для форматирования.

        Args:
            response (str): Текст ответа для форматирования.

        Returns:
            str: Отформатированный текст ответа.

        Raises:
            Exception: Если возникает ошибка при вставке HTML-тегов.

        Example:
            >>> response = '#### Заголовок 1\\n### Заголовок 2\\n**Жирный текст**\\n*Курсив*'
            >>> formatted_response = PromptsCompressor.html_tags_insert(response)
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