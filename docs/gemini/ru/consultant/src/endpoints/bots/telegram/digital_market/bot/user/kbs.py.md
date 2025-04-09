### **Анализ кода модуля `kbs.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/user/kbs.py

Модуль содержит функции для создания различных инлайн-клавиатур для Telegram-бота цифрового магазина.
Функции генерируют клавиатуры для главного меню, каталога, покупок, страницы продукта и способов оплаты.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Четкая структура функций, каждая из которых отвечает за создание определенной клавиатуры.
    - Использование `InlineKeyboardBuilder` для удобного создания клавиатур.
    - Применение `callback_data` для обработки нажатий на кнопки.
- **Минусы**:
    - Отсутствуют docstring для функций, что затрудняет понимание их назначения и параметров.
    - Не все переменные аннотированы типами.
    - Использованы двойные кавычки в строках, необходимо заменить на одинарные.
    - Не используется модуль `logger` для логгирования возможных ошибок.
    - В некоторых местах отсутствует единообразие в форматировании (например, пробелы вокруг операторов).

**Рекомендации по улучшению:**

1.  Добавить docstring к каждой функции, описывающий её назначение, параметры и возвращаемое значение.
2.  Добавить аннотации типов для переменных и параметров функций.
3.  Заменить двойные кавычки на одинарные.
4.  Добавить обработку исключений с логированием ошибок с использованием модуля `logger`.
5.  Улучшить форматирование кода в соответствии со стандартами PEP8 (пробелы вокруг операторов, отступы и т.д.).
6.  Удалить неиспользуемые импорты.

**Оптимизированный код:**

```python
from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.app.utils import generate_payment_link
from bot.config import settings
from bot.dao.models import Category
from src.logger import logger  # Добавлен импорт logger


def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    """
    Создает главную клавиатуру пользователя.

    Args:
        user_id (int): ID пользователя.

    Returns:
        InlineKeyboardMarkup: Главная клавиатура пользователя.
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
    Создает клавиатуру каталога на основе списка категорий.

    Args:
        catalog_data (List[Category]): Список категорий для отображения.

    Returns:
        InlineKeyboardMarkup: Клавиатура каталога.
    """
    kb = InlineKeyboardBuilder()
    for category in catalog_data:
        kb.button(text=category.category_name, callback_data=f'category_{category.id}')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(2)
    return kb.as_markup()


def purchases_kb() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления покупками.

    Returns:
        InlineKeyboardMarkup: Клавиатура для управления покупками.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='🗑 Смотреть покупки', callback_data='purchases')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(1)
    return kb.as_markup()


def product_kb(product_id: int, price: float, stars_price: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для страницы продукта с опциями покупки.

    Args:
        product_id (int): ID продукта.
        price (float): Цена продукта в рублях.
        stars_price (int): Цена продукта в звездах.

    Returns:
        InlineKeyboardMarkup: Клавиатура для страницы продукта.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='💳 Оплатить ЮКасса', callback_data=f'buy_yukassa_{product_id}_{price}')
    kb.button(text='💳 Оплатить Robocassa', callback_data=f'buy_robocassa_{product_id}_{price}')
    kb.button(text='⭐ Оплатить звездами', callback_data=f'buy_stars_{product_id}_{stars_price}')
    kb.button(text='🛍 Назад', callback_data='catalog')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(2)
    return kb.as_markup()


def get_product_buy_youkassa(price: float) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты продукта через ЮКасса.

    Args:
        price (float): Цена продукта.

    Returns:
        InlineKeyboardMarkup: Клавиатура для оплаты через ЮКасса.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплатить {price}₽', pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])


def get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты продукта через Robocassa.

    Args:
        price (int): Цена продукта.
        payment_link (str): Ссылка на оплату в Robocassa.

    Returns:
        InlineKeyboardMarkup: Клавиатура для оплаты через Robocassa.
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
        InlineKeyboardMarkup: Клавиатура для оплаты звездами.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплатить {price} ⭐', pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])