# Модуль AuxiliaryClasses.py

## Обзор

Модуль содержит вспомогательные классы `keyboards` и `PromptsCompressor`, используемые для создания клавиатур для Telegram-бота и сжатия/обработки текстовых запросов.

## Подробней

Этот модуль предоставляет функциональность для упрощения взаимодействия с пользователем через Telegram-бота, предлагая инструменты для создания интерактивных клавиатур и обработки текстовых запросов с использованием предопределенных шаблонов.

## Классы

### `keyboards`

**Описание**: Класс `keyboards` предназначен для создания различных типов клавиатур для Telegram-бота.

**Аттрибуты**:
- Отсутствуют

**Методы**:
- `_keyboard_two_blank(data: list[str], name: list[str]) -> types.InlineKeyboardMarkup`
- `_reply_keyboard(self, name: list[str])`

### `PromptsCompressor`

**Описание**: Класс `PromptsCompressor` предназначен для сжатия и обработки текстовых запросов на основе предопределенных шаблонов, хранящихся в JSON-файле.

**Аттрибуты**:
- `commands_size (list[list[str]])`: Список, содержащий структуру команд для различных типов запросов.

**Методы**:
- `get_prompt(self, info: list[str], ind: int) -> str`
- `html_tags_insert(response: str) -> str`

## Методы класса `keyboards`

### `_keyboard_two_blank`

```python
    def _keyboard_two_blank(self, data: list[str], name: list[str]) -> types.InlineKeyboardMarkup:
        """
        Создает встроенную клавиатуру с двумя полями в каждом ряду.

        Args:
            data (list[str]): Список данных для callback_data каждой кнопки.
            name (list[str]): Список отображаемых имен кнопок.

        Returns:
            types.InlineKeyboardMarkup: Объект встроенной клавиатуры.
        """
```

**Как работает функция**:
- Функция принимает два списка: `data` (данные для callback_data) и `name` (отображаемые имена кнопок).
- Создается встроенная клавиатура `types.InlineKeyboardMarkup`.
- Создаются кнопки на основе переданных данных и имен.
- Кнопки добавляются на клавиатуру попарно, если количество кнопок четное, иначе последняя кнопка добавляется отдельно.

**Примеры**:

```python
from telebot import types

# Пример данных
data = ["1", "2", "3", "4", "5"]
name = ["Button 1", "Button 2", "Button 3", "Button 4", "Button 5"]

# Создание экземпляра класса keyboards (предполагается, что он уже определен)
kb = keyboards()

# Вызов метода _keyboard_two_blank
keyboard = kb._keyboard_two_blank(data, name)

# Теперь 'keyboard' содержит объект InlineKeyboardMarkup с кнопками, созданными на основе переданных данных.
# Его можно отправить пользователю с помощью telebot.send_message
```

### `_reply_keyboard`

```python
    def _reply_keyboard(self, name: list[str]):
        """
        Создает обычную клавиатуру с кнопками в один ряд.

        Args:
            name (list[str]): Список отображаемых имен кнопок.

        Returns:
            markup (types.ReplyKeyboardMarkup): Объект обычной клавиатуры.
        """
```

**Как работает функция**:

- Функция принимает список `name` (отображаемые имена кнопок).
- Создается обычная клавиатура `types.ReplyKeyboardMarkup`.
- Создаются кнопки на основе переданных имен.
- Кнопки добавляются на клавиатуру.

**Примеры**:

```python
from telebot import types

# Пример данных
name = ["Button 1", "Button 2", "Button 3"]

# Создание экземпляра класса keyboards (предполагается, что он уже определен)
kb = keyboards()

# Вызов метода _reply_keyboard
keyboard = kb._reply_keyboard(name)

# Теперь 'keyboard' содержит объект ReplyKeyboardMarkup с кнопками, созданными на основе переданных имен.
# Его можно отправить пользователю с помощью telebot.send_message
```

## Методы класса `PromptsCompressor`

### `get_prompt`

```python
    def get_prompt(self, info: list[str], ind: int) -> str:
        """
        Извлекает и форматирует строку запроса на основе предоставленной информации и индекса.

        Args:
            info (list[str]): Список строк, содержащих информацию для подстановки в запрос.
            ind (int): Индекс запроса для извлечения из JSON-файла.

        Returns:
            str: Сформированная строка запроса.
        """
```

**Как работает функция**:

- Функция принимает список строк `info` и индекс `ind`.
- Открывает JSON-файл `'ToolBox/BaseSettings/prompts.json'` и загружает данные.
- Извлекает строку запроса из JSON по индексу `ind`.
- Заменяет плейсхолдеры в строке запроса на значения из списка `info` на основе соответствия с `self.commands_size[ind]`.

**Примеры**:

```python
# Пример данных (предположим, что prompts.json содержит необходимые данные)
info = ["Topic Example", "TA Example", "Tone Example", "Struct Example", "Length Example", "Extra Example"]
ind = 0

# Создание экземпляра класса PromptsCompressor
compressor = PromptsCompressor()

# Вызов метода get_prompt
prompt = compressor.get_prompt(info, ind)

# Теперь 'prompt' содержит сформированную строку запроса на основе данных из 'info' и шаблона из prompts.json
print(prompt)
```

### `html_tags_insert`

```python
    @staticmethod
    def html_tags_insert(response: str) -> str:
        """
        Вставляет HTML-теги в строку ответа на основе предопределенных шаблонов.

        Args:
            response (str): Строка ответа для обработки.

        Returns:
            str: Строка ответа с вставленными HTML-тегами.
        """
```

**Как работает функция**:

- Функция принимает строку `response`.
- Определяет список шаблонов `patterns` для замены текста на HTML-теги.
- Использует `re.sub` для замены текста в строке `response` на HTML-теги на основе заданных шаблонов.

**Примеры**:

```python
# Пример данных
response = "#### Заголовок 4\n### Заголовок 3\n**Жирный текст**\n*Курсив*"

# Вызов метода html_tags_insert
formatted_response = PromptsCompressor.html_tags_insert(response)

# Теперь 'formatted_response' содержит строку с HTML-тегами
print(formatted_response)
```