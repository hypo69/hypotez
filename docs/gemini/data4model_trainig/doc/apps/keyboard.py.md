# Модуль для создания клавиатур для бота Movie

## Обзор

Модуль `src.endpoints.bots.telegram.movie_bot-main/apps/keyboard.py` предназначен для создания клавиатур, используемых в Telegram-боте для поиска фильмов и сериалов.

## Подробней

Модуль предоставляет функции для создания инлайн-клавиатур, используемых для навигации по боту и выбора действий.

## Переменные

*   `find_movie` (InlineKeyboardMarkup): Клавиатура для поиска фильма.
*   `choice` (InlineKeyboardMarkup): Клавиатура для выбора типа контента (фильм или сериал).

## Описание переменных

### `find_movie`

```python
find_movie = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]
])
```

**Назначение**: Клавиатура для запуска поиска фильма или сериала.

**Структура**: Содержит одну кнопку "Найти", которая вызывает обратный вызов `new_movies`.

### `choice`

```python
choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сериал', callback_data='series'),
     InlineKeyboardButton(text='Фильм', callback_data='film')]
])
```

**Назначение**: Клавиатура для выбора типа контента (фильм или сериал).

**Структура**: Содержит две кнопки: "Сериал" (вызывает обратный вызов `series`) и "Фильм" (вызывает обратный вызов `film`).