# Модуль для создания клавиатур для Telegram-бота цифрового магазина
==================================================================

Модуль содержит функции для создания различных типов клавиатур (InlineKeyboardMarkup и ReplyKeyboardMarkup) для Telegram-бота, используемого в цифровом магазине. Включает в себя создание основных меню, каталогов, клавиатур для покупок и оплаты товаров.

## Обзор

Этот модуль предоставляет набор функций для создания интерактивных клавиатур, которые используются в Telegram-боте для цифрового магазина. Каждая функция создает определенный тип клавиатуры с соответствующими кнопками и callback-данными, позволяющими пользователям взаимодействовать с ботом.

## Подробней

Модуль использует библиотеки `aiogram` для создания клавиатур и `bot.config` для получения настроек. Функции в модуле генерируют клавиатуры для различных сценариев использования бота, таких как основное меню, каталог товаров, просмотр покупок и оплата товаров.

## Функции

### `main_user_kb`

```python
def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    """Создает основную клавиатуру пользователя с кнопками "Мои покупки", "Каталог", "О магазине" и "Поддержать автора".

    Args:
        user_id (int): ID пользователя.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками основного меню.

    Пример:
        >>> user_id = 12345
        >>> main_user_kb(user_id)
        <InlineKeyboardMarkup object>
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="👤 Мои покупки", callback_data="my_profile")
    kb.button(text="🛍 Каталог", callback_data="catalog")
    kb.button(text="ℹ️ О магазине", callback_data="about")
    kb.button(text="🌟 Поддержать автора 🌟", url='https://t.me/tribute/app?startapp=deLN')
    if user_id in settings.ADMIN_IDS:
        kb.button(text="⚙️ Админ панель", callback_data="admin_panel")
    kb.adjust(1)
    return kb.as_markup()
    

**Как работает функция**:
- Создает объект `InlineKeyboardBuilder`.
- Добавляет кнопки "👤 Мои покупки", "🛍 Каталог", "ℹ️ О магазине" и "🌟 Поддержать автора 🌟" с соответствующими callback_data и URL.
- Если `user_id` есть в списке `settings.ADMIN_IDS`, добавляет кнопку "⚙️ Админ панель" с callback_data "admin_panel".
- Устанавливает количество кнопок в ряду равным 1.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup` и возвращает его.

**Примеры**:

```python
user_id = 12345
main_user_kb(user_id=user_id)
```

### `catalog_kb`

```python
def catalog_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup:
    """Создает клавиатуру каталога с кнопками для каждой категории и кнопкой "На главную".

    Args:
        catalog_data (List[Category]): Список объектов Category, представляющих категории товаров.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками категорий и кнопкой "На главную".

    Пример:
        >>> catalog_data = [Category(id=1, category_name="Электроника"), Category(id=2, category_name="Одежда")]
        >>> catalog_kb(catalog_data)
        <InlineKeyboardMarkup object>
    """
    kb = InlineKeyboardBuilder()
    for category in catalog_data:
        kb.button(text=category.category_name, callback_data=f"category_{category.id}")
    kb.button(text="🏠 На главную", callback_data="home")
    kb.adjust(2)
    return kb.as_markup()
```
**Как работает функция**:
- Создает объект `InlineKeyboardBuilder`.
- Итерируется по списку `catalog_data`.
- Для каждой категории добавляет кнопку с названием категории и callback_data в формате "category_{category.id}".
- Добавляет кнопку "🏠 На главную" с callback_data "home".
- Устанавливает количество кнопок в ряду равным 2.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup` и возвращает его.

**Примеры**:

```python
from typing import List
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Category: #  class Category in bot.dao.models
    def __init__(self, id: int, category_name: str):
        self.id = id
        self.category_name = category_name

catalog_data: List[Category] = [Category(id=1, category_name="Электроника"), Category(id=2, category_name="Одежда")]

catalog_kb(catalog_data=catalog_data)
```

### `purchases_kb`

```python
def purchases_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру для просмотра покупок с кнопками "Смотреть покупки" и "На главную".

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками просмотра покупок и кнопкой "На главную".

    Пример:
        >>> purchases_kb()
        <InlineKeyboardMarkup object>
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="🗑 Смотреть покупки", callback_data="purchases")
    kb.button(text="🏠 На главную", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()
```

**Как работает функция**:
- Создает объект `InlineKeyboardBuilder`.
- Добавляет кнопку "🗑 Смотреть покупки" с callback_data "purchases".
- Добавляет кнопку "🏠 На главную" с callback_data "home".
- Устанавливает количество кнопок в ряду равным 1.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup` и возвращает его.

**Примеры**:

```python
purchases_kb()
```

### `product_kb`

```python
def product_kb(product_id, price, stars_price) -> InlineKeyboardMarkup:
    """Создает клавиатуру для товара с кнопками оплаты различными способами и кнопками "Назад" и "На главную".

    Args:
        product_id (int): ID товара.
        price (int): Цена товара в рублях.
        stars_price (int): Цена товара в звездах.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками оплаты и навигации.

    Пример:
        >>> product_id = 123
        >>> price = 100
        >>> stars_price = 50
        >>> product_kb(product_id, price, stars_price)
        <InlineKeyboardMarkup object>
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="💳 Оплатить ЮКасса", callback_data=f"buy_yukassa_{product_id}_{price}")
    kb.button(text="💳 Оплатить Robocassa", callback_data=f"buy_robocassa_{product_id}_{price}")
    kb.button(text="⭐ Оплатить звездами", callback_data=f"buy_stars_{product_id}_{stars_price}")
    kb.button(text="🛍 Назад", callback_data="catalog")
    kb.button(text="🏠 На главную", callback_data="home")
    kb.adjust(2)
    return kb.as_markup()
```

**Как работает функция**:
- Создает объект `InlineKeyboardBuilder`.
- Добавляет кнопки "💳 Оплатить ЮКасса", "💳 Оплатить Robocassa" и "⭐ Оплатить звездами" с соответствующими callback_data, включающими `product_id` и `price`.
- Добавляет кнопки "🛍 Назад" с callback_data "catalog" и "🏠 На главную" с callback_data "home".
- Устанавливает количество кнопок в ряду равным 2.
- Преобразует `InlineKeyboardBuilder` в `InlineKeyboardMarkup` и возвращает его.

**Примеры**:

```python
product_id = 123
price = 100
stars_price = 50

product_kb(product_id=product_id, price=price, stars_price=stars_price)
```

### `get_product_buy_youkassa`

```python
def get_product_buy_youkassa(price) -> InlineKeyboardMarkup:
    """Создает клавиатуру для оплаты товара через ЮКасса.

    Args:
        price (int): Цена товара в рублях.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопкой оплаты через ЮКасса и кнопкой "Отменить".

    Пример:
        >>> price = 100
        >>> get_product_buy_youkassa(price)
        <InlineKeyboardMarkup object>
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплатить {price}₽', pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])
```
**Как работает функция**:
- Создает объект `InlineKeyboardMarkup`.
- Добавляет кнопку "Оплатить {price}₽" с параметром `pay=True` для интеграции с ЮКасса.
- Добавляет кнопку "Отменить" с callback_data "home".
- Возвращает созданный объект `InlineKeyboardMarkup`.

**Примеры**:

```python
price = 100
get_product_buy_youkassa(price=price)
```

### `get_product_buy_robocassa`

```python
def get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для оплаты товара через Robocassa.

    Args:
        price (int): Цена товара в рублях.
        payment_link (str): Ссылка для оплаты через Robocassa.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопкой оплаты через Robocassa и кнопкой "Отменить".

    Пример:
        >>> price = 100
        >>> payment_link = "https://example.com/robocassa_payment"
        >>> get_product_buy_robocassa(price, payment_link)
        <InlineKeyboardMarkup object>
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f'Оплатить {price}₽',
            web_app=WebAppInfo(url=payment_link)
        )],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])
```

**Как работает функция**:
- Создает объект `InlineKeyboardMarkup`.
- Добавляет кнопку "Оплатить {price}₽" с использованием `WebAppInfo` для передачи ссылки на оплату через Robocassa.
- Добавляет кнопку "Отменить" с callback_data "home".
- Возвращает созданный объект `InlineKeyboardMarkup`.

**Примеры**:

```python
price = 100
payment_link = "https://example.com/robocassa_payment"

get_product_buy_robocassa(price=price, payment_link=payment_link)
```

### `get_product_buy_stars`

```python
def get_product_buy_stars(price) -> InlineKeyboardMarkup:
    """Создает клавиатуру для оплаты товара звездами.

    Args:
        price (int): Цена товара в звездах.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопкой оплаты звездами и кнопкой "Отменить".

    Пример:
        >>> price = 50
        >>> get_product_buy_stars(price)
        <InlineKeyboardMarkup object>
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Оплатить {price} ⭐", pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])
```

**Как работает функция**:
- Создает объект `InlineKeyboardMarkup`.
- Добавляет кнопку "Оплатить {price} ⭐" с параметром `pay=True` для оплаты звездами.
- Добавляет кнопку "Отменить" с callback_data "home".
- Возвращает созданный объект `InlineKeyboardMarkup`.

**Примеры**:

```python
price = 50
get_product_buy_stars(price=price)
```