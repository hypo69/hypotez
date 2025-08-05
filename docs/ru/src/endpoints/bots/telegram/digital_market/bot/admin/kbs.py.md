# Модуль для создания клавиатур администратора Telegram-бота

## Обзор

Модуль предоставляет набор функций для создания различных инлайн-клавиатур, Используетсяых в Telegram-боте для административных целей. Клавиатуры предназначены для управления каталогом товаров, добавления/удаления товаров, просмотра статистики и навигации по основным разделам бота.

## Подробнее

Модуль содержит функции, которые генерируют объекты `InlineKeyboardMarkup` для различных сценариев взаимодействия администратора с ботом. Каждая функция создает определенную конфигурацию кнопок с соответствующими `callback_data`, которые обрабатываются ботом для выполнения определенных действий.

## Функции

### `catalog_admin_kb`

**Назначение**: Создает инлайн-клавиатуру для управления категориями товаров в административной панели.

**Параметры**:
- `catalog_data` (List[Category]): Список объектов `Category`, для каждой из которых создается кнопка с названием категории.

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопками для каждой категории и кнопкой "Отмена".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Перебирает список категорий `catalog_data`.
- Для каждой категории создает кнопку с текстом, равным названию категории, и `callback_data`, содержащим ID категории.
- Добавляет кнопку "Отмена" с `callback_data="admin_panel"`.
- Настраивает расположение кнопок в два столбца.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup
from bot.dao.models import Category
from typing import List

# Пример данных о категориях
catalog_data: List[Category] = [
    Category(id=1, category_name="Электроника"),
    Category(id=2, category_name="Одежда"),
    Category(id=3, category_name="Обувь")
]

# Создание клавиатуры
keyboard: InlineKeyboardMarkup = catalog_admin_kb(catalog_data)
```

### `admin_send_file_kb`

**Назначение**: Создает инлайн-клавиатуру для выбора отправки файла или отказа от отправки при добавлении товара.

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопками "Без файла" и "Отмена".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "Без файла" с `callback_data="without_file"`.
- Добавляет кнопку "Отмена" с `callback_data="admin_panel"`.
- Настраивает расположение кнопок в два столбца.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup

# Создание клавиатуры
keyboard: InlineKeyboardMarkup = admin_send_file_kb()
```

### `admin_kb`

**Назначение**: Создает основную инлайн-клавиатуру административной панели с кнопками для просмотра статистики, управления товарами и перехода на главную страницу.

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопками "📊 Статистика", "🛍️ Управлять товарами" и "🏠 На главную".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "📊 Статистика" с `callback_data="statistic"`.
- Добавляет кнопку "🛍️ Управлять товарами" с `callback_data="process_products"`.
- Добавляет кнопку "🏠 На главную" с `callback_data="home"`.
- Настраивает расположение кнопок в два столбца.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup

# Создание клавиатуры
keyboard: InlineKeyboardMarkup = admin_kb()
```

### `admin_kb_back`

**Назначение**: Создает инлайн-клавиатуру для возврата в административную панель или на главную страницу.

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопками "⚙️ Админ панель" и "🏠 На главную".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "⚙️ Админ панель" с `callback_data="admin_panel"`.
- Добавляет кнопку "🏠 На главную" с `callback_data="home"`.
- Настраивает расположение кнопок в один столбец.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup

# Создание клавиатуры
keyboard: InlineKeyboardMarkup = admin_kb_back()
```

### `dell_product_kb`

**Назначение**: Создает инлайн-клавиатуру для подтверждения удаления товара с возможностью возврата в админ-панель или на главную страницу.

**Параметры**:
- `product_id` (int): ID удаляемого товара.

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопками "🗑️ Удалить", "⚙️ Админ панель" и "🏠 На главную".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "🗑️ Удалить" с `callback_data`, содержащим ID товара.
- Добавляет кнопку "⚙️ Админ панель" с `callback_data="admin_panel"`.
- Добавляет кнопку "🏠 На главную" с `callback_data="home"`.
- Настраивает расположение кнопок в три ряда: 2, 2 и 1 кнопка.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup

# Создание клавиатуры для товара с ID 123
keyboard: InlineKeyboardMarkup = dell_product_kb(123)
```

### `product_management_kb`

**Назначение**: Создает инлайн-клавиатуру для управления товарами: добавление, удаление, возврат в админ-панель или на главную страницу.

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопками "➕ Добавить товар", "🗑️ Удалить товар", "⚙️ Админ панель" и "🏠 На главную".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "➕ Добавить товар" с `callback_data="add_product"`.
- Добавляет кнопку "🗑️ Удалить товар" с `callback_data="delete_product"`.
- Добавляет кнопку "⚙️ Админ панель" с `callback_data="admin_panel"`.
- Добавляет кнопку "🏠 На главную" с `callback_data="home"`.
- Настраивает расположение кнопок в три ряда: 2, 2 и 1 кнопка.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup

# Создание клавиатуры
keyboard: InlineKeyboardMarkup = product_management_kb()
```

### `cancel_kb_inline`

**Назначение**: Создает инлайн-клавиатуру с кнопкой "Отмена".

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопкой "Отмена".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "Отмена" с `callback_data="cancel"`.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup

# Создание клавиатуры
keyboard: InlineKeyboardMarkup = cancel_kb_inline()
```

### `admin_confirm_kb`

**Назначение**: Создает инлайн-клавиатуру для подтверждения действия администратором с возможностью отмены и возврата в админ-панель.

**Возвращает**:
- `InlineKeyboardMarkup`: Инлайн-клавиатура с кнопками "Все верно" и "Отмена".

**Как работает функция**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "Все верно" с `callback_data="confirm_add"`.
- Добавляет кнопку "Отмена" с `callback_data="admin_panel"`.
- Настраивает расположение кнопок в один столбец.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup`.

**Примеры**:
```python
from aiogram.types import InlineKeyboardMarkup

# Создание клавиатуры
keyboard: InlineKeyboardMarkup = admin_confirm_kb()