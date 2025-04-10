### **Анализ кода модуля `kbs.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/user/kbs.py

Модуль содержит функции для создания различных inline-клавиатур для Telegram-бота цифрового магазина.
Обеспечивает навигацию по каталогу, профилю пользователя, информации о магазине, а также предлагает различные способы оплаты товаров.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и выполняет поставленные задачи.
    - Используются `InlineKeyboardBuilder` для удобного создания клавиатур.
    - Присутствуют функции для создания различных типов клавиатур.
- **Минусы**:
    - Отсутствуют docstring для функций и аннотации типов.
    - Смешанный стиль кавычек (использованы как одинарные, так и двойные).
    - Не используется модуль `logger` для логирования.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех функций**:
    *   Добавить подробное описание каждой функции, ее аргументов, возвращаемых значений и возможных исключений.
2.  **Аннотировать типы**:
    *   Указать типы всех переменных и параметров функций.
3.  **Использовать одинарные кавычки**:
    *   Привести все строки к использованию одинарных кавычек.
4.  **Использовать модуль `logger`**:
    *   Добавить логирование важных событий, таких как ошибки при создании клавиатур.
5.  **Изменить способ импорта модулей из `aiogram`**:
    *   Импортировать конкретные классы и функции, а не использовать wildcard импорт (`from aiogram.types import ...`).
6.  **Удалить неиспользуемые импорты**:
    *   Удалить `ReplyKeyboardMarkup` и `ReplyKeyboardBuilder`, если они не используются.

**Оптимизированный код:**

```python
from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.logger.logger import logger  # Добавлен импорт logger
from bot.app.utils import generate_payment_link
from bot.config import settings
from bot.dao.models import Category


def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    """
    Создает главную клавиатуру пользователя с кнопками: "Мои покупки", "Каталог", "О магазине", "Поддержать автора" и "Админ панель" (если пользователь является админом).

    Args:
        user_id (int): ID пользователя.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с главной клавиатурой пользователя.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='👤 Мои покупки', callback_data='my_profile')
    kb.button(text='🛍 Каталог', callback_data='catalog')
    kb.button(text='ℹ️ О магазине', callback_data='about')
    kb.button(text='🌟 Поддержать автора 🌟', url='https://t.me/tribute/app?startapp=deLN')
    if user_id in settings.ADMIN_IDS:
        kb.button(text='⚙️ Админ панель', callback_data='admin_panel')
    kb.adjust(1)
    return kb.as_markup()


def catalog_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру каталога с кнопками категорий и кнопкой "На главную".

    Args:
        catalog_data (List[Category]): Список объектов Category.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с клавиатурой каталога.
    """
    kb = InlineKeyboardBuilder()
    for category in catalog_data:
        kb.button(text=category.category_name, callback_data=f'category_{category.id}')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(2)
    return kb.as_markup()


def purchases_kb() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления покупками с кнопками: "Смотреть покупки" и "На главную".

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с клавиатурой управления покупками.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='🗑 Смотреть покупки', callback_data='purchases')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(1)
    return kb.as_markup()


def product_kb(product_id: int, price: int, stars_price: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру продукта с кнопками для оплаты различными способами и кнопками навигации.

    Args:
        product_id (int): ID продукта.
        price (int): Цена продукта в рублях.
        stars_price (int): Цена продукта в звездах.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с клавиатурой продукта.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='💳 Оплатить ЮКасса', callback_data=f'buy_yukassa_{product_id}_{price}')
    kb.button(text='💳 Оплатить Robocassa', callback_data=f'buy_robocassa_{product_id}_{price}')
    kb.button(text='⭐ Оплатить звездами', callback_data=f'buy_stars_{product_id}_{stars_price}')
    kb.button(text='🛍 Назад', callback_data='catalog')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(2)
    return kb.as_markup()


def get_product_buy_youkassa(price: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты продукта через ЮКасса.

    Args:
        price (int): Цена продукта в рублях.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с клавиатурой для оплаты через ЮКасса.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплатить {price}₽', pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])


def get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты продукта через Robocassa.

    Args:
        price (int): Цена продукта в рублях.
        payment_link (str): Ссылка на оплату через Robocassa.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с клавиатурой для оплаты через Robocassa.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f'Оплатить {price}₽',
            web_app=WebAppInfo(url=payment_link)
        )],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])


def get_product_buy_stars(price: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты продукта звездами.

    Args:
        price (int): Цена продукта в звездах.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с клавиатурой для оплаты звездами.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплатить {price} ⭐', pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])