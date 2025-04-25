# Модуль для создания клавиатур в Telegram боте

## Обзор

Модуль `kbs.py`  предоставляет функции для создания различных клавиатур для Telegram-бота. Клавиатуры используются для управления взаимодействием пользователей с ботом, особенно в контексте административных действий.

## Функции

### `catalog_admin_kb`

**Назначение**: Создание клавиатуры для выбора категории товара.

**Параметры**:
- `catalog_data` (List[Category]): Список категорий товаров.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с кнопками для каждой категории товара.

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Для каждой категории в списке `catalog_data` добавляется кнопка с названием категории и callback_data, содержащим идентификатор категории.
- Добавляется кнопка "Отмена" с callback_data "admin_panel", чтобы вернуться на главную админ-панель.
- Настройки клавиатуры задаются с помощью метода `adjust`.
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
from bot.dao.models import Category

categories = [Category(id=1, category_name="Одежда"), Category(id=2, category_name="Обувь")]
kb = catalog_admin_kb(categories)
print(kb.to_json())
```
### `admin_send_file_kb`

**Назначение**: Создание клавиатуры для выбора варианта отправки файла.

**Параметры**: 
- Отсутствуют.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с кнопками "Без файла" и "Отмена".

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляются две кнопки: "Без файла" с callback_data "without_file" и "Отмена" с callback_data "admin_panel".
- Настройки клавиатуры задаются с помощью метода `adjust`.
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
kb = admin_send_file_kb()
print(kb.to_json())
```

### `admin_kb`

**Назначение**: Создание основной клавиатуры для админ-панели.

**Параметры**: 
- Отсутствуют.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с кнопками "Статистика", "Управлять товарами", "На главную".

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляются три кнопки: "Статистика" с callback_data "statistic", "Управлять товарами" с callback_data "process_products" и "На главную" с callback_data "home".
- Настройки клавиатуры задаются с помощью метода `adjust`.
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
kb = admin_kb()
print(kb.to_json())
```

### `admin_kb_back`

**Назначение**: Создание клавиатуры для возврата на админ-панель.

**Параметры**: 
- Отсутствуют.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с кнопками "Админ панель" и "На главную".

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляются две кнопки: "Админ панель" с callback_data "admin_panel" и "На главную" с callback_data "home".
- Настройки клавиатуры задаются с помощью метода `adjust`.
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
kb = admin_kb_back()
print(kb.to_json())
```

### `dell_product_kb`

**Назначение**: Создание клавиатуры для подтверждения удаления товара.

**Параметры**:
- `product_id` (int): Идентификатор товара.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с кнопками "Удалить", "Админ панель", "На главную".

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляются три кнопки: "Удалить" с callback_data, содержащим `dell_` и `product_id`, "Админ панель" с callback_data "admin_panel" и "На главную" с callback_data "home".
- Настройки клавиатуры задаются с помощью метода `adjust`.
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
kb = dell_product_kb(product_id=123)
print(kb.to_json())
```

### `product_management_kb`

**Назначение**: Создание клавиатуры для управления товарами.

**Параметры**: 
- Отсутствуют.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с кнопками "Добавить товар", "Удалить товар", "Админ панель", "На главную".

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляются четыре кнопки: "Добавить товар" с callback_data "add_product", "Удалить товар" с callback_data "delete_product", "Админ панель" с callback_data "admin_panel" и "На главную" с callback_data "home".
- Настройки клавиатуры задаются с помощью метода `adjust`.
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
kb = product_management_kb()
print(kb.to_json())
```

### `cancel_kb_inline`

**Назначение**: Создание клавиатуры с кнопкой "Отмена".

**Параметры**: 
- Отсутствуют.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с одной кнопкой "Отмена".

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляется кнопка "Отмена" с callback_data "cancel".
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
kb = cancel_kb_inline()
print(kb.to_json())
```

### `admin_confirm_kb`

**Назначение**: Создание клавиатуры для подтверждения действия.

**Параметры**: 
- Отсутствуют.

**Возвращает**:
- `InlineKeyboardMarkup`: Клавиатура с кнопками "Все верно" и "Отмена".

**Принцип работы**:
- Функция создает объект `InlineKeyboardBuilder`.
- Добавляются две кнопки: "Все верно" с callback_data "confirm_add" и "Отмена" с callback_data "admin_panel".
- Настройки клавиатуры задаются с помощью метода `adjust`.
- Возвращается готовая клавиатура в виде `InlineKeyboardMarkup`.

**Пример**:
```python
kb = admin_confirm_kb()
print(kb.to_json())
```