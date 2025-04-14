# Модуль для создания клавиатур для Telegram-бота
## Обзор

Модуль `keyboard.py` предназначен для создания и управления клавиатурами, используемыми в Telegram-боте. Он содержит определения для различных типов клавиатур, таких как клавиатура для поиска фильмов и клавиатура для выбора типа контента (фильм или сериал).

## Подробнее

Этот модуль предоставляет удобные инструменты для создания интерактивных элементов интерфейса Telegram-бота, позволяя пользователям взаимодействовать с ботом посредством нажатия кнопок. 

## Классы

В данном модуле отсутствуют классы.

## Переменные

### `find_movie`

**Описание**: InlineKeyboardMarkup для поиска фильмов.

**Тип**: InlineKeyboardMarkup

**Принцип работы**:
Эта переменная инициализируется объектом `InlineKeyboardMarkup`, который содержит одну кнопку с текстом "Найти". При нажатии на эту кнопку, бот получает callback_data `new_movies`, что позволяет запустить процесс поиска новых фильмов.

**Примеры**:
```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

find_movie = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]
])
```

### `choice`

**Описание**: InlineKeyboardMarkup для выбора типа контента (сериал или фильм).

**Тип**: InlineKeyboardMarkup

**Принцип работы**:
Эта переменная инициализируется объектом `InlineKeyboardMarkup`, который содержит две кнопки: "Сериал" и "Фильм". При нажатии на кнопку "Сериал", бот получает callback_data `series`, а при нажатии на кнопку "Фильм" - `film`. Это позволяет боту определить, какой тип контента интересует пользователя.

**Примеры**:
```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сериал', callback_data='series'),
     InlineKeyboardButton(text='Фильм', callback_data='film')]
])