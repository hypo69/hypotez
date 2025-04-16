# Модуль вспомогательных классов

## Обзор

Модуль `src.endpoints.bots.telegram.ToolBoxbot-main/ToolBox/BaseSettings/AuxiliaryClasses.py` содержит вспомогательные классы для работы с клавиатурами, промптами и HTML-тегами.

## Подробней

Модуль предоставляет классы `keyboards` и `PromptsCompressor` для упрощения создания клавиатур Telegram-бота, управления промптами и вставки HTML-тегов в текст.

## Классы

### `keyboards`

**Описание**: Класс для создания клавиатур Telegram-бота.

**Методы**:

*   `_keyboard_two_blank(self, data: list[str], name: list[str]) -> types.InlineKeyboardMarkup`: Создает инлайн-клавиатуру с двумя кнопками в ряд.
*   `_reply_keyboard(self, name: list[str])`: Создает клавиатуру ответа (ReplyKeyboardMarkup).

### `PromptsCompressor`

**Описание**: Класс для сжатия и управления промптами.

**Атрибуты**:

*   `commands_size` (list): Список размеров команд.

**Методы**:

*   `get_prompt(self, info: list[str], ind: int) -> str`: Получает промпт на основе предоставленной информации и индекса.
*   `html_tags_insert(response: str) -> str`: Вставляет HTML-теги в текст ответа.

## Методы класса `keyboards`

### `_keyboard_two_blank`

```python
def _keyboard_two_blank(self, data: list[str], name: list[str]) -> types.InlineKeyboardMarkup:
```

**Назначение**: Создает инлайн-клавиатуру с двумя кнопками в ряд.

**Параметры**:

*   `data` (list[str]): Список данных для обратных вызовов кнопок.
*   `name` (list[str]): Список названий кнопок.

**Возвращает**:

*   `types.InlineKeyboardMarkup`: Объект инлайн-клавиатуры.

**Как работает функция**:

1.  Создает объект `types.InlineKeyboardMarkup`.
2.  Создает кнопки с использованием данных из списков `name` и `data`.
3.  Размещает кнопки по две в ряд.
4.  Возвращает сформированную клавиатуру.

### `_reply_keyboard`

```python
def _reply_keyboard(self, name: list[str]):
```

**Назначение**: Создает клавиатуру ответа (ReplyKeyboardMarkup).

**Параметры**:

*   `name` (list[str]): Список названий кнопок.

**Возвращает**:

*   `types.ReplyKeyboardMarkup`: Объект клавиатуры ответа.

**Как работает функция**:

1.  Создает объект `types.ReplyKeyboardMarkup`.
2.  Создает кнопки на основе списка `name`.
3.  Добавляет кнопки на клавиатуру.
4.  Возвращает сформированную клавиатуру.

## Методы класса `PromptsCompressor`

### `get_prompt`

```python
def get_prompt(self, info: list[str], ind: int) -> str:
```

**Назначение**: Получает промпт на основе предоставленной информации и индекса.

**Параметры**:

*   `info` (list[str]): Список информации для заполнения промпта.
*   `ind` (int): Индекс промпта.

**Возвращает**:

*   `str`: Сформированный промпт.

**Как работает функция**:

1.  Загружает промпты из JSON-файла `ToolBox/BaseSettings/prompts.json`.
2.  Заменяет заполнители в промпте на значения из списка `info`.
3.  Возвращает сформированный промпт.

### `html_tags_insert`

```python
@staticmethod
def html_tags_insert(response: str) -> str:
```

**Назначение**: Вставляет HTML-теги в текст ответа.

**Параметры**:

*   `response` (str): Текст для вставки тегов.

**Возвращает**:

*   `str`: Текст с вставленными HTML-тегами.

**Как работает функция**:

1.  Использует регулярные выражения для поиска и замены определенных шаблонов в тексте на соответствующие HTML-теги.
2.  Возвращает текст с вставленными тегами.