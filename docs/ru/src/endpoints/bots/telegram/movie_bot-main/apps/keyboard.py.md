# Модуль для создания клавиатур Telegram-ботов
## \file hypotez/src/endpoints/bots/telegram/movie_bot-main/apps/keyboard.py

## Обзор

Модуль `keyboard.py` содержит определения встроенных клавиатур для Telegram-бота. В частности, он создает объекты `InlineKeyboardMarkup`, представляющие кнопки "Найти", выбор между "Сериалом" и "Фильмом", которые используются для взаимодействия с пользователем через Telegram-бота.

## Подробней

Этот модуль предоставляет пользователю возможность интерактивно взаимодействовать с ботом. Клавиатуры определены с использованием библиотеки `aiogram`, позволяющей создавать кнопки, привязанные к определенным действиям (callback data). Callback data используется для определения того, какое действие должен выполнить бот при нажатии кнопки.

## Клавиатуры

### `find_movie`

**Описание**: Inline-клавиатура с кнопкой "Найти" для запуска поиска фильмов.

**Атрибуты**:
- `inline_keyboard` (list): Список списков объектов `InlineKeyboardButton`, представляющих структуру клавиатуры.

**Принцип работы**:
Клавиатура состоит из одной кнопки "Найти". Когда пользователь нажимает на эту кнопку, боту отправляется callback data `new_movies`, по которой бот понимает, что нужно запустить поиск новых фильмов.

### `choice`

**Описание**: Inline-клавиатура для выбора между "Сериалом" и "Фильмом".

**Атрибуты**:
- `inline_keyboard` (list): Список списков объектов `InlineKeyboardButton`, представляющих структуру клавиатуры.

**Принцип работы**:
Клавиатура предоставляет пользователю две кнопки: "Сериал" и "Фильм". При нажатии на кнопку "Сериал" боту отправляется callback data `series`, а при нажатии на кнопку "Фильм" - callback data `film`. Это позволяет боту определить, какой тип контента интересует пользователя.

## InlineKeyboardButtons

### InlineKeyboardButton(text='Найти', callback_data='new_movies')

**Назначение**: Создание кнопки "Найти" с callback data `new_movies`.
**Параметры**:

- `text` (str): Текст, отображаемый на кнопке ("Найти").
- `callback_data` (str): Данные, отправляемые боту при нажатии на кнопку (`new_movies`).

### InlineKeyboardButton(text='Сериал', callback_data='series')

**Назначение**: Создание кнопки "Сериал" с callback data `series`.

**Параметры**:

- `text` (str): Текст, отображаемый на кнопке ("Сериал").
- `callback_data` (str): Данные, отправляемые боту при нажатии на кнопку (`series`).

### InlineKeyboardButton(text='Фильм', callback_data='film')

**Назначение**: Создание кнопки "Фильм" с callback data `film`.

**Параметры**:

- `text` (str): Текст, отображаемый на кнопке ("Фильм").
- `callback_data` (str): Данные, отправляемые боту при нажатии на кнопку (`film`).

## Примеры

### Создание клавиатуры "Найти"

```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

find_movie = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]
])
```

### Создание клавиатуры выбора

```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сериал', callback_data='series'),
     InlineKeyboardButton(text='Фильм', callback_data='film')]
])
```