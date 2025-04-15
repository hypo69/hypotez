### **Анализ кода модуля `kbs.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и читаем.
  - Используются `InlineKeyboardBuilder` для создания клавиатур, что упрощает процесс.
  - Функции имеют понятные имена, отражающие их назначение.
- **Минусы**:
  - Отсутствуют docstring для функций.
  - Не все переменные аннотированы типами.
  - Не используется `logger` для логирования.
  - Не везде используются одинарные кавычки.

**Рекомендации по улучшению:**

1.  **Добавить docstring для каждой функции**. Описать, что делает функция, какие аргументы принимает и что возвращает.
2.  **Аннотировать типы для всех переменных** в функциях, где это необходимо.
3.  **Использовать `logger`** для логирования важных событий, особенно ошибок.
4.  **Использовать одинарные кавычки** вместо двойных.
5.  **Удалить** неиспользуемые импорты.
6.  **Вместо** `Union[]` используй `|`

**Оптимизированный код:**

```python
from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.app.utils import generate_payment_link
from bot.config import settings
from bot.dao.models import Category
from src.logger import logger  # Импорт logger


def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    """
    Создает основную клавиатуру пользователя с кнопками: "Мои покупки", "Каталог", "О магазине", "Поддержать автора" и "Админ панель" (если пользователь является администратором).

    Args:
        user_id (int): ID пользователя.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками.

    Example:
        >>> main_user_kb(12345)
        <InlineKeyboardMarkup object>
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='👤 Мои покупки', callback_data='my_profile')
    kb.button(text='🛍 Каталог', callback_data='catalog')
    kb.button(text='ℹ️ О магазине', callback_data='about')
    kb.button(text='🌟 Поддержать автора 🌟', url='https://t.me/tribute/app?startapp=deLN')
    if user_id in settings.ADMIN_IDS:
        kb.button(text='⚙️ Админ панель', callback_data='admin_panel')
        logger.info(f'User {user_id} is admin, added admin panel button')  # Логирование для администраторов
    kb.adjust(1)
    return kb.as_markup()


def catalog_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру каталога с кнопками для каждой категории и кнопкой "На главную".

    Args:
        catalog_data (List[Category]): Список объектов Category.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками категорий.

    Example:
        >>> catalog_kb([Category(id=1, category_name='Category 1'), Category(id=2, category_name='Category 2')])
        <InlineKeyboardMarkup object>
    """
    kb = InlineKeyboardBuilder()
    for category in catalog_data:
        kb.button(text=category.category_name, callback_data=f'category_{category.id}')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(2)
    return kb.as_markup()


def purchases_kb() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления покупками с кнопками "Смотреть покупки" и "На главную".

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками управления покупками.

    Example:
        >>> purchases_kb()
        <InlineKeyboardMarkup object>
    """
    kb = InlineKeyboardBuilder()
    kb.button(text='🗑 Смотреть покупки', callback_data='purchases')
    kb.button(text='🏠 На главную', callback_data='home')
    kb.adjust(1)
    return kb.as_markup()


def product_kb(product_id: int, price: int, stars_price: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру продукта с кнопками для оплаты через ЮKassa, Robocassa и звездами, а также кнопками "Назад" и "На главную".

    Args:
        product_id (int): ID продукта.
        price (int): Цена продукта в рублях.
        stars_price (int): Цена продукта в звездах.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками оплаты и навигации.

    Example:
        >>> product_kb(123, 100, 50)
        <InlineKeyboardMarkup object>
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
    Создает клавиатуру для оплаты продукта через ЮKassa с кнопкой "Оплатить" и кнопкой "Отменить".

    Args:
        price (int): Цена продукта в рублях.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками оплаты и отмены.

    Example:
        >>> get_product_buy_youkassa(100)
        <InlineKeyboardMarkup object>
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплатить {price}₽', pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])


def get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для оплаты продукта через Robocassa с кнопкой "Оплатить" (через web_app) и кнопкой "Отменить".

    Args:
        price (int): Цена продукта в рублях.
        payment_link (str): Ссылка для оплаты через Robocassa.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками оплаты и отмены.

    Example:
        >>> get_product_buy_robocassa(100, 'https://example.com/robocassa_payment')
        <InlineKeyboardMarkup object>
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
    Создает клавиатуру для оплаты продукта звездами с кнопкой "Оплатить" и кнопкой "Отменить".

    Args:
        price (int): Цена продукта в звездах.

    Returns:
        InlineKeyboardMarkup: Объект InlineKeyboardMarkup с кнопками оплаты и отмены.

    Example:
        >>> get_product_buy_stars(50)
        <InlineKeyboardMarkup object>
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Оплатить {price} ⭐', pay=True)],
        [InlineKeyboardButton(text='Отменить', callback_data='home')]
    ])