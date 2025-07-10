# Модуль для создания клавиатур для Telegram-бота
## Обзор

Модуль `kbs.py` предназначен для формирования различных типов клавиатур (инлайн и обычных) для Telegram-бота, Используетсяого в цифровом магазине. Он содержит функции для создания клавиатур главного меню, каталога товаров, истории покупок и вариантов оплаты товаров.

## Подробнее

Этот модуль предоставляет набор функций для генерации клавиатур, которые используются для навигации пользователей по боту, отображения категорий товаров и предоставления способов оплаты. Каждая функция создает соответствующую клавиатуру и возвращает ее в виде объекта `InlineKeyboardMarkup` или `ReplyKeyboardMarkup`, готового для отправки пользователю.

## Классы
В данном модуле классы отсутствуют

## Функции

### `main_user_kb`

```python
def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    """
    Создает главную клавиатуру пользователя с кнопками "Мои покупки", "Каталог", "О магазине", "Поддержать автора" и "Админ панель" (если пользователь является администратором).

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками главного меню.
    
    Принцип работы:
        Функция создает инлайн-клавиатуру с кнопками, предоставляющими пользователю доступ к основным разделам бота: "Мои покупки", "Каталог", "О магазине" и "Поддержать автора". Если идентификатор пользователя находится в списке администраторов, добавляется кнопка "Админ панель". Клавиатура настраивается на отображение кнопок в один столбец.
    
    Примеры:
        Пример для обычного пользователя:
        >>> main_user_kb(12345)
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
        Пример для администратора:
        >>> main_user_kb(settings.ADMIN_IDS[0])
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
    """
    kb = InlineKeyboardBuilder() # Cоздание экземпляра класса InlineKeyboardBuilder для создания инлайн-клавиатуры
    kb.button(text="👤 Мои покупки", callback_data="my_profile") # Добавление кнопки "Мои покупки" с callback_data "my_profile"
    kb.button(text="🛍 Каталог", callback_data="catalog") # Добавление кнопки "Каталог" с callback_data "catalog"
    kb.button(text="ℹ️ О магазине", callback_data="about") # Добавление кнопки "О магазине" с callback_data "about"
    kb.button(text="🌟 Поддержать автора 🌟", url='https://t.me/tribute/app?startapp=deLN') # Добавление кнопки "Поддержать автора" с URL
    if user_id in settings.ADMIN_IDS: # Проверка, является ли user_id администратором
        kb.button(text="⚙️ Админ панель", callback_data="admin_panel") # Добавление кнопки "Админ панель" с callback_data "admin_panel", если пользователь - администратор
    kb.adjust(1) # Автоматическое изменение размера, чтобы все кнопки помещались в один столбец
    return kb.as_markup() # Преобразование InlineKeyboardBuilder в InlineKeyboardMarkup

### `catalog_kb`

```python
def catalog_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру каталога на основе списка категорий.

    Args:
        catalog_data (List[Category]): Список объектов категорий товаров.

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками категорий и кнопкой "На главную".
    
    Принцип работы:
        Функция создает инлайн-клавиатуру, динамически формируя кнопки для каждой категории товара в списке catalog_data. Для каждой категории создается кнопка с названием категории и callback_data, содержащим идентификатор категории. В конце добавляется кнопка "На главную". Клавиатура настраивается на отображение кнопок в два столбца.
    
    Примеры:
        >>> catalog_kb([Category(id=1, category_name='Category 1'), Category(id=2, category_name='Category 2')])
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
    """
    kb = InlineKeyboardBuilder() # Создание экземпляра класса InlineKeyboardBuilder для создания инлайн-клавиатуры
    for category in catalog_data: # Перебор списка категорий
        kb.button(text=category.category_name, callback_data=f"category_{category.id}") # Добавление кнопки для каждой категории с callback_data, содержащим идентификатор категории
    kb.button(text="🏠 На главную", callback_data="home") # Добавление кнопки "На главную" с callback_data "home"
    kb.adjust(2) # Автоматическое изменение размера, чтобы все кнопки помещались в два столбца
    return kb.as_markup() # Преобразование InlineKeyboardBuilder в InlineKeyboardMarkup

### `purchases_kb`

```python
def purchases_kb() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для просмотра истории покупок.

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками "Смотреть покупки" и "На главную".
    
    Принцип работы:
        Функция создает инлайн-клавиатуру с кнопками "Смотреть покупки" и "На главную", предоставляющими пользователю доступ к просмотру истории своих покупок и возврату в главное меню. Клавиатура настраивается на отображение кнопок в один столбец.
    
    Примеры:
        >>> purchases_kb()
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
    """
    kb = InlineKeyboardBuilder() # Создание экземпляра класса InlineKeyboardBuilder для создания инлайн-клавиатуры
    kb.button(text="🗑 Смотреть покупки", callback_data="purchases") # Добавление кнопки "Смотреть покупки" с callback_data "purchases"
    kb.button(text="🏠 На главную", callback_data="home") # Добавление кнопки "На главную" с callback_data "home"
    kb.adjust(1) # Автоматическое изменение размера, чтобы все кнопки помещались в один столбец
    return kb.as_markup() # Преобразование InlineKeyboardBuilder в InlineKeyboardMarkup

### `product_kb`

```python
def product_kb(product_id, price, stars_price) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора способа оплаты товара.

    Args:
        product_id: Идентификатор товара.
        price: Цена товара в рублях.
        stars_price: Цена товара в звездах.

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками для оплаты через ЮКасса, Robocassa и звездами, а также кнопками "Назад" и "На главную".
    
    Принцип работы:
        Функция создает инлайн-клавиатуру с кнопками для выбора способа оплаты товара: "Оплатить ЮКасса", "Оплатить Robocassa" и "Оплатить звездами". Для каждой кнопки оплаты формируется callback_data, содержащий идентификатор товара и цену. Также добавляются кнопки "Назад" и "На главную" для навигации. Клавиатура настраивается на отображение кнопок в два столбца.
    
    Примеры:
        >>> product_kb(123, 100, 50)
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
    """
    kb = InlineKeyboardBuilder() # Создание экземпляра класса InlineKeyboardBuilder для создания инлайн-клавиатуры
    kb.button(text="💳 Оплатить ЮКасса", callback_data=f"buy_yukassa_{product_id}_{price}") # Добавление кнопки "Оплатить ЮКасса" с callback_data, содержащим product_id и цену
    kb.button(text="💳 Оплатить Robocassa", callback_data=f"buy_robocassa_{product_id}_{price}") # Добавление кнопки "Оплатить Robocassa" с callback_data, содержащим product_id и цену
    kb.button(text="⭐ Оплатить звездами", callback_data=f"buy_stars_{product_id}_{stars_price}") # Добавление кнопки "Оплатить звездами" с callback_data, содержащим product_id и цену в звездах
    kb.button(text="🛍 Назад", callback_data="catalog") # Добавление кнопки "Назад" с callback_data "catalog"
    kb.button(text="🏠 На главную", callback_data="home") # Добавление кнопки "На главную" с callback_data "home"
    kb.adjust(2) # Автоматическое изменение размера, чтобы все кнопки помещались в два столбца
    return kb.as_markup() # Преобразование InlineKeyboardBuilder в InlineKeyboardMarkup

### `get_product_buy_youkassa`

```python
def get_product_buy_youkassa(price) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для подтверждения оплаты через ЮКасса.

    Args:
        price: Цена товара в рублях.

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопкой для оплаты и кнопкой "Отменить".
    
    Принцип работы:
        Функция создает инлайн-клавиатуру с кнопкой, предлагающей оплатить указанную цену через ЮКасса, и кнопкой "Отменить" для возврата в предыдущее меню.
    
    Примеры:
        >>> get_product_buy_youkassa(100)
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
    """
    return InlineKeyboardMarkup(inline_keyboard=[ # Создание InlineKeyboardMarkup с заданным inline_keyboard
        [InlineKeyboardButton(text=f'Оплатить {price}₽', pay=True)], # Добавление кнопки "Оплатить {price}₽" с указанием, что это кнопка для оплаты
        [InlineKeyboardButton(text='Отменить', callback_data='home')] # Добавление кнопки "Отменить" с callback_data "home"
    ])

### `get_product_buy_robocassa`

```python
def get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты через Robocassa с использованием web_app.

    Args:
        price (int): Цена товара в рублях.
        payment_link (str): Ссылка на страницу оплаты Robocassa.

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопкой для оплаты через web_app и кнопкой "Отменить".
    
    Принцип работы:
        Функция создает инлайн-клавиатуру с кнопкой, перенаправляющей пользователя на страницу оплаты Robocassa через web_app, и кнопкой "Отменить" для возврата в предыдущее меню.
    
    Примеры:
        >>> get_product_buy_robocassa(100, 'https://example.com/robocassa')
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
    """
    return InlineKeyboardMarkup(inline_keyboard=[ # Создание InlineKeyboardMarkup с заданным inline_keyboard
        [InlineKeyboardButton( # Добавление кнопки с использованием web_app
            text=f'Оплатить {price}₽', # Задание текста кнопки
            web_app=WebAppInfo(url=payment_link) # Указание ссылки для web_app
        )],
        [InlineKeyboardButton(text='Отменить', callback_data='home')] # Добавление кнопки "Отменить" с callback_data "home"
    ])

### `get_product_buy_stars`

```python
def get_product_buy_stars(price) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты звездами.

    Args:
        price: Цена товара в звездах.

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопкой для оплаты звездами и кнопкой "Отменить".
    
    Принцип работы:
        Функция создает инлайн-клавиатуру с кнопкой, предлагающей оплатить указанную цену в звездах, и кнопкой "Отменить" для возврата в предыдущее меню.
    
    Примеры:
        >>> get_product_buy_stars(50)
        <aiogram.types.inline_keyboard.InlineKeyboardMarkup object at 0x...>
    """
    return InlineKeyboardMarkup(inline_keyboard=[ # Создание InlineKeyboardMarkup с заданным inline_keyboard
        [InlineKeyboardButton(text=f"Оплатить {price} ⭐", pay=True)], # Добавление кнопки "Оплатить {price} ⭐" с указанием, что это кнопка для оплаты
        [InlineKeyboardButton(text='Отменить', callback_data='home')] # Добавление кнопки "Отменить" с callback_data "home"
    ])