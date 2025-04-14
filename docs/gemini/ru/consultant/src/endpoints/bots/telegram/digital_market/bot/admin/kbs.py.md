### **Анализ кода модуля `kbs.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/admin/kbs.py

Модуль содержит функции для создания inline-клавиатур для Telegram-бота.
Клавиатуры используются для административных действий, таких как управление каталогом, товарами, статистикой и т.д.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и легко читается.
  - Функции имеют понятные названия, отражающие их назначение.
  - Использование `InlineKeyboardBuilder` для создания клавиатур упрощает процесс.
  - Использование `adjust()` для управления расположением кнопок в клавиатуре.
- **Минусы**:
  - Отсутствуют docstring для функций, что затрудняет понимание их назначения и параметров.
  - Не все callback_data имеют понятные префиксы или суффиксы.
  - Отсутствует обработка возможных ошибок или исключений.
  - Не используются аннотации типов.

**Рекомендации по улучшению:**

1.  **Добавить docstring для каждой функции**. Описать назначение функции, параметры, возвращаемые значения.
2.  **Добавить аннотации типов для всех переменных и параметров функций**.
3.  **Улучшить callback_data**. Сделать их более информативными и стандартизированными.
4.  **Добавить обработку исключений**. Предусмотреть обработку возможных ошибок, например, при формировании клавиатуры.
5.  **Использовать `logger` для логирования**. Добавить логирование для отслеживания работы функций и выявления возможных проблем.

**Оптимизированный код:**

```python
from typing import List
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.dao.models import Category
from src.logger import logger


def catalog_admin_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для администратора с категориями каталога.

    Args:
        catalog_data (List[Category]): Список объектов категорий для отображения.

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> catalog_data = [Category(id=1, category_name='Электроника'), Category(id=2, category_name='Одежда')]
        >>> catalog_admin_kb(catalog_data)
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        for category in catalog_data:
            kb.button(text=category.category_name, callback_data=f"add_category_{category.id}")
        kb.button(text="Отмена", callback_data="admin_panel")
        kb.adjust(2)
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании клавиатуры категорий", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки


def admin_send_file_kb() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для администратора с кнопками "Без файла" и "Отмена".

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> admin_send_file_kb()
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="Без файла", callback_data="without_file")
        kb.button(text="Отмена", callback_data="admin_panel")
        kb.adjust(2)
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании клавиатуры отправки файла", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки


def admin_kb() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для администратора с основными кнопками управления.

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> admin_kb()
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="📊 Статистика", callback_data="statistic")
        kb.button(text="🛍️ Управлять товарами", callback_data="process_products")
        kb.button(text="🏠 На главную", callback_data="home")
        kb.adjust(2)
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании основной клавиатуры администратора", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки


def admin_kb_back() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для возврата в админ-панель и на главную.

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> admin_kb_back()
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="⚙️ Админ панель", callback_data="admin_panel")
        kb.button(text="🏠 На главную", callback_data="home")
        kb.adjust(1)
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании клавиатуры возврата в админ-панель", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки


def dell_product_kb(product_id: int) -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для подтверждения удаления товара.

    Args:
        product_id (int): ID товара для удаления.

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> dell_product_kb(123)
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="🗑️ Удалить", callback_data=f"dell_{product_id}")
        kb.button(text="⚙️ Админ панель", callback_data="admin_panel")
        kb.button(text="🏠 На главную", callback_data="home")
        kb.adjust(2, 2, 1)  # Размещаем кнопки в три ряда: 2, 2 и 1 кнопка
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании клавиатуры подтверждения удаления товара", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки


def product_management_kb() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для управления товарами.

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> product_management_kb()
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="➕ Добавить товар", callback_data="add_product")
        kb.button(text="🗑️ Удалить товар", callback_data="delete_product")
        kb.button(text="⚙️ Админ панель", callback_data="admin_panel")
        kb.button(text="🏠 На главную", callback_data="home")
        kb.adjust(2, 2, 1)  # Размещаем кнопки в три ряда: 2, 2 и 1 кнопка
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании клавиатуры управления товарами", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки


def cancel_kb_inline() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру с кнопкой "Отмена".

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> cancel_kb_inline()
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="Отмена", callback_data="cancel")
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании клавиатуры отмены", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки


def admin_confirm_kb() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для подтверждения действия администратором.

    Returns:
        InlineKeyboardMarkup: Объект inline-клавиатуры.

    Example:
        >>> admin_confirm_kb()
        <InlineKeyboardMarkup object>
    """
    try:
        kb = InlineKeyboardBuilder()
        kb.button(text="Все верно", callback_data="confirm_add")
        kb.button(text="Отмена", callback_data="admin_panel")
        kb.adjust(1)
        return kb.as_markup()
    except Exception as ex:
        logger.error("Ошибка при формировании клавиатуры подтверждения действия", ex, exc_info=True)
        return InlineKeyboardMarkup(inline_keyboard=[])  # Возвращаем пустую клавиатуру в случае ошибки