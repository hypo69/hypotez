# Документация модуля AuxiliaryClasses

## Обзор

Модуль `AuxiliaryClasses.py` содержит вспомогательные классы, используемые в проекте `hypotez` для работы с Telegram ботом. В частности, он включает класс `keyboards` для создания различных типов клавиатур и класс `PromptsCompressor` для обработки и сжатия текстовых запросов (prompts).

## Подробнее

Модуль предоставляет инструменты для динамического создания клавиатур в Telegram боте и для манипулирования текстовыми запросами, используемыми для генерации контента. Классы в этом модуле облегчают взаимодействие с пользователем и оптимизируют процесс обработки запросов.

## Классы

### `keyboards`

**Описание**: Класс предназначен для создания различных типов клавиатур, используемых в Telegram боте.
Он включает методы для создания как встроенных клавиатур (`InlineKeyboardMarkup`), так и клавиатур, отображаемых в нижней части экрана (`ReplyKeyboardMarkup`).

**Методы**:

- `_keyboard_two_blank(self, data: list[str], name: list[str]) -> types.InlineKeyboardMarkup`

    **Назначение**: Создает встроенную клавиатуру с кнопками, расположенными в два столбца.

    **Параметры**:
    - `data` (list[str]): Список данных, которые будут переданы в callback_data кнопок.
    - `name` (list[str]): Список отображаемых названий кнопок.

    **Возвращает**:
    - `types.InlineKeyboardMarkup`: Объект встроенной клавиатуры для Telegram бота.

    **Как работает функция**:
    - Функция принимает два списка: `data` и `name`, которые соответствуют callback_data и отображаемым именам кнопок соответственно.
    - Создает объект `types.InlineKeyboardMarkup` для представления встроенной клавиатуры.
    - Создает список кнопок `types.InlineKeyboardButton`, используя данные из списков `data` и `name`.
    - Располагает кнопки в два столбца, добавляя их в клавиатуру парами.
    - Если количество кнопок нечетное, последняя кнопка добавляется в отдельную строку.

- `_reply_keyboard(self, name: list[str])`

    **Назначение**: Создает клавиатуру, отображаемую в нижней части экрана (ReplyKeyboardMarkup).

    **Параметры**:
    - `name` (list[str]): Список отображаемых названий кнопок.

    **Возвращает**:
    - `types.ReplyKeyboardMarkup`: Объект клавиатуры для Telegram бота.

    **Как работает функция**:
    - Функция принимает список `name`, который содержит отображаемые имена кнопок.
    - Создает объект `types.ReplyKeyboardMarkup` для представления клавиатуры.
    - Создает список кнопок `types.KeyboardButton`, используя данные из списка `name`.
    - Добавляет кнопки в клавиатуру.

### `PromptsCompressor`

**Описание**: Класс предназначен для сжатия и обработки текстовых запросов (prompts), используемых для генерации контента.

**Атрибуты**:
- `commands_size` (list[list[str]]): Двумерный список, определяющий структуру запросов для разных типов команд.

**Методы**:

- `__init__(self)`

    **Назначение**: Инициализирует класс `PromptsCompressor` и определяет структуру запросов для разных типов команд.

    **Как работает функция**:
    - Функция инициализирует атрибут `self.commands_size`, который представляет собой двумерный список, определяющий структуру запросов для разных типов команд.

- `get_prompt(self, info: list[str], ind: int) -> str`

    **Назначение**: Извлекает и формирует запрос на основе предоставленной информации и индекса команды.

    **Параметры**:
    - `info` (list[str]): Список информации, необходимой для формирования запроса.
    - `ind` (int): Индекс команды, определяющий структуру запроса.

    **Возвращает**:
    - `str`: Сформированный запрос.

    **Как работает функция**:
    - Открывает файл `ToolBox/BaseSettings/prompts.json` и загружает JSON-данные.
    - Извлекает команду с индексом `ind` из JSON-данных.
    - Заменяет заполнители в команде информацией из списка `info`, используя структуру, определенную в `self.commands_size`.

- `html_tags_insert(response: str) -> str`

    **Назначение**: Вставляет HTML-теги в текст ответа для форматирования.

    **Параметры**:
    - `response` (str): Текст ответа, в который необходимо вставить HTML-теги.

    **Возвращает**:
    - `str`: Текст ответа с вставленными HTML-тегами.

    **Как работает функция**:
    - Функция принимает строку `response`, которая содержит текст ответа.
    - Определяет список шаблонов `patterns`, где каждый шаблон представляет собой кортеж из двух элементов: регулярное выражение для поиска и строка замены с HTML-тегами.
    - Итерируется по списку шаблонов и заменяет соответствующие участки текста в строке `response` на HTML-теги.

## Примеры
### Пример работы с классом `keyboards`
```python
from telebot import TeleBot
from telebot import types
from src.endpoints.bots.telegram.ToolBoxbot_main.ToolBox.BaseSettings.AuxiliaryClasses import keyboards

bot = TeleBot("YOUR_TELEGRAM_BOT_TOKEN")

@bot.message_handler(commands=['start'])
def start(message):
    # Пример создания встроенной клавиатуры
    keyboard_creator = keyboards()
    data = ['data1', 'data2', 'data3']
    name = ['Name 1', 'Name 2', 'Name 3']
    inline_keyboard = keyboard_creator._keyboard_two_blank(data, name)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=inline_keyboard)

    # Пример создания клавиатуры в нижней части экрана
    reply_keyboard_names = ['Option A', 'Option B', 'Option C']
    reply_keyboard = keyboard_creator._reply_keyboard(reply_keyboard_names)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=reply_keyboard)
```
### Пример работы с классом `PromptsCompressor`
```python
from src.endpoints.bots.telegram.ToolBoxbot_main.ToolBox.BaseSettings.AuxiliaryClasses import PromptsCompressor

# Создание инстанса класса PromptsCompressor
compressor = PromptsCompressor()

# Пример использования get_prompt
info = ["Topic Example", "TA Example", "Tone Example", "Struct Example", "Length Example", "Extra Example"]
ind = 0
prompt = compressor.get_prompt(info, ind)
print(f"Generated prompt: {prompt}")

# Пример использования html_tags_insert
response = "#### Important Headline\nThis is a **bold** and *italic* text.\n```python\nprint('Hello')\n```"
formatted_response = compressor.html_tags_insert(response)
print(f"Formatted response: {formatted_response}")
```