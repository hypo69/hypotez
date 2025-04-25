# Модуль `keyboard.py`

## Обзор

Этот модуль содержит определения кнопок для бота Telegram, которые используются для взаимодействия с пользователем. 

## Подробней

Модуль `keyboard.py` предоставляет набор кнопок, которые выводятся на экран пользователя в Telegram, чтобы он мог выбрать нужные действия. 

Например, модуль содержит кнопку "Найти", которая позволяет пользователю начать поиск фильма. 

## Классы

### `InlineKeyboardMarkup`

**Описание**: Класс `InlineKeyboardMarkup` используется для создания клавиатур в Telegram. 

**Атрибуты**:

- `inline_keyboard`: Список списков кнопок.

**Методы**:

- `add()`: Добавляет кнопку на клавиатуру.
- `insert()`: Вставляет кнопку на клавиатуру.
- `row()`: Добавляет новую строку на клавиатуру.
- `row_width()`: Устанавливает количество кнопок в строке.

## Методы класса

### `find_movie`

```python
find_movie = InlineKeyboardMarkup(inline_keyboard=[\n    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]\n])
```

**Описание**: Клавиатура с кнопкой "Найти", которая запускает поиск фильма. 

**Параметры**:

- `inline_keyboard`: Список списков кнопок. В данном случае это список с одной кнопкой "Найти".
- `callback_data`: Данные, которые передаются в бота при нажатии на кнопку. В данном случае это "new_movies".

**Возвращает**:

- `InlineKeyboardMarkup`: Объект класса `InlineKeyboardMarkup` с кнопкой "Найти".

**Примеры**:

```python
from aiogram.types import InlineKeyboardMarkup

find_movie = InlineKeyboardMarkup(inline_keyboard=[\n    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]\n])
```

### `choice`

```python
choice = InlineKeyboardMarkup(inline_keyboard=[\n    [InlineKeyboardButton(text='Сериал', callback_data='series'),\n     InlineKeyboardButton(text='Фильм', callback_data='film')]\n])
```

**Описание**: Клавиатура с кнопками "Сериал" и "Фильм", которые позволяют пользователю выбрать тип контента. 

**Параметры**:

- `inline_keyboard`: Список списков кнопок. В данном случае это список с двумя кнопками "Сериал" и "Фильм".
- `callback_data`: Данные, которые передаются в бота при нажатии на кнопку. В данном случае это "series" или "film".

**Возвращает**:

- `InlineKeyboardMarkup`: Объект класса `InlineKeyboardMarkup` с кнопками "Сериал" и "Фильм".

**Примеры**:

```python
from aiogram.types import InlineKeyboardMarkup

choice = InlineKeyboardMarkup(inline_keyboard=[\n    [InlineKeyboardButton(text='Сериал', callback_data='series'),\n     InlineKeyboardButton(text='Фильм', callback_data='film')]\n])