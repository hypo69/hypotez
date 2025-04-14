# Модуль для создания клавиатур для Telegram-бота
====================================================

Модуль предоставляет функциональность для создания inline-клавиатур для Telegram-бота, использующего библиотеку aiogram. Клавиатуры используются для навигации и выбора опций в боте.

## Обзор

Модуль содержит определения inline-клавиатур, которые могут быть использованы для предоставления пользователям возможности выбора действий, таких как поиск фильмов или выбор типа контента (фильм или сериал).

## Подробней

Данный модуль предоставляет два типа inline-клавиатур: `find_movie` и `choice`. Клавиатура `find_movie` предлагает пользователю кнопку "Найти", а клавиатура `choice` предлагает выбор между "Сериал" и "Фильм". Эти клавиатуры используются для упрощения взаимодействия пользователя с ботом, позволяя делать выбор одним нажатием кнопки.

## Классы

В данном модуле нет классов.

## Функции

В данном модуле нет функций.

## Переменные

### `find_movie`

```python
find_movie = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]
])
```

**Описание**: Inline-клавиатура с одной кнопкой "Найти".

**Назначение**: Предоставляет пользователю возможность начать поиск новых фильмов.

**Параметры**:

-   `inline_keyboard` (list): Список списков объектов `InlineKeyboardButton`, представляющих клавиатуру.
    -   `InlineKeyboardButton` (aiogram.types.InlineKeyboardButton): Кнопка с текстом "Найти" и callback-данными `new_movies`.

**Принцип работы**:

Клавиатура `find_movie` создается с помощью `InlineKeyboardMarkup` из библиотеки `aiogram`. Она содержит одну кнопку с текстом "Найти", при нажатии на которую боту отправляются callback-данные `new_movies`. Это позволяет боту определить, что пользователь хочет начать поиск новых фильмов.

### `choice`

```python
choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сериал', callback_data='series'),
     InlineKeyboardButton(text='Фильм', callback_data='film')]
])
```

**Описание**: Inline-клавиатура с двумя кнопками: "Сериал" и "Фильм".

**Назначение**: Предоставляет пользователю возможность выбрать тип контента для поиска (сериал или фильм).

**Параметры**:

-   `inline_keyboard` (list): Список списков объектов `InlineKeyboardButton`, представляющих клавиатуру.
    -   `InlineKeyboardButton` (aiogram.types.InlineKeyboardButton): Кнопка с текстом "Сериал" и callback-данными `series`.
    -   `InlineKeyboardButton` (aiogram.types.InlineKeyboardButton): Кнопка с текстом "Фильм" и callback-данными `film`.

**Принцип работы**:

Клавиатура `choice` создается с помощью `InlineKeyboardMarkup` из библиотеки `aiogram`. Она содержит две кнопки: "Сериал" и "Фильм". При нажатии на одну из кнопок боту отправляются соответствующие callback-данные (`series` или `film`), что позволяет боту определить, какой тип контента выбрал пользователь.

## Примеры

### Пример использования `find_movie`:

```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

find_movie = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]
])
```

### Пример использования `choice`:

```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сериал', callback_data='series'),
     InlineKeyboardButton(text='Фильм', callback_data='film')]
])