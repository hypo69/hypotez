### **Анализ кода модуля `kbs.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/admin/kbs.py

Модуль содержит функции для создания inline-клавиатур для Telegram-бота. Клавиатуры используются в административной панели бота для управления каталогом, товарами, статистикой и другими функциями.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и легко читается.
    - Функции имеют понятные имена, отражающие их назначение.
    - Использование `InlineKeyboardBuilder` делает создание клавиатур удобным.
    - Код соответствует принципу DRY (Don't Repeat Yourself) в том плане, что функции инкапсулируют логику создания клавиатур.
- **Минусы**:
    - Отсутствуют docstring для функций.
    - Не все переменные аннотированы типами.
    - Не хватает комментариев, объясняющих логику работы отдельных частей кода.
    - Используются строки для callback_data, что может привести к ошибкам. Лучше использовать dataclass или enum.
    - `adjust` вызывается с разными аргументами, что не очень удобно для чтения. Лучше вынести логику в отдельную функцию.

**Рекомендации по улучшению:**

1.  **Добавить docstring для каждой функции**, чтобы объяснить ее назначение, аргументы и возвращаемое значение.
2.  **Аннотировать типы** для всех переменных и аргументов функций.
3.  **Добавить комментарии** для объяснения логики работы отдельных частей кода.
4.  **Использовать dataclass или enum** для callback\_data, чтобы избежать ошибок.
5.  **Упростить использование `adjust`**, вынеся логику в отдельную функцию или используя константы для количества кнопок в ряду.
6.  **Добавить логирование** для отслеживания ошибок и предупреждений.
7.  **Использовать f-строки** для форматирования строк.
8.  **Изменить название модуля `kbs.py`** на `keyboards.py`, чтобы соответствовать принятому соглашению об именовании.

**Оптимизированный код:**

```python
from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.dao.models import Category
from src.logger import logger  # Import logger

class CallbackData:
    """
    Класс для хранения callback_data
    """
    ADMIN_PANEL = "admin_panel"
    HOME = "home"
    CANCEL = "cancel"
    CONFIRM_ADD = "confirm_add"
    STATISTIC = "statistic"
    PROCESS_PRODUCTS = "process_products"
    ADD_PRODUCT = "add_product"
    DELETE_PRODUCT = "delete_product"
    WITHOUT_FILE = "without_file"
    DELL_PRODUCT = "dell_"
    ADD_CATEGORY = "add_category_"

def create_inline_keyboard(buttons: List[InlineKeyboardButton], adjust: tuple[int, ...]) -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру на основе списка кнопок и схемы расположения.

    Args:
        buttons (List[InlineKeyboardButton]): Список кнопок для добавления в клавиатуру.
        adjust (tuple[int, ...]): Схема расположения кнопок по рядам.

    Returns:
        InlineKeyboardMarkup: Сгенерированная inline-клавиатура.
    """
    kb = InlineKeyboardBuilder()
    for button in buttons:
        kb.add(button)
    kb.adjust(*adjust)
    return kb.as_markup()

def catalog_admin_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для администратора с категориями каталога.

    Args:
        catalog_data (List[Category]): Список категорий для отображения.

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с категориями и кнопкой "Отмена".
    """
    buttons = [
        InlineKeyboardButton(text=category.category_name, callback_data=f"{CallbackData.ADD_CATEGORY}{category.id}")
        for category in catalog_data
    ]
    buttons.append(InlineKeyboardButton(text="Отмена", callback_data=CallbackData.ADMIN_PANEL))
    return create_inline_keyboard(buttons, adjust=(2,))

def admin_send_file_kb() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для администратора с кнопками "Без файла" и "Отмена".

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с кнопками "Без файла" и "Отмена".
    """
    buttons = [
        InlineKeyboardButton(text="Без файла", callback_data=CallbackData.WITHOUT_FILE),
        InlineKeyboardButton(text="Отмена", callback_data=CallbackData.ADMIN_PANEL)
    ]
    return create_inline_keyboard(buttons, adjust=(2,))

def admin_kb() -> InlineKeyboardMarkup:
    """
    Создает главную inline-клавиатуру для администратора.

    Returns:
        InlineKeyboardMarkup: Главная inline-клавиатура администратора.
    """
    buttons = [
        InlineKeyboardButton(text="📊 Статистика", callback_data=CallbackData.STATISTIC),
        InlineKeyboardButton(text="🛍️ Управлять товарами", callback_data=CallbackData.PROCESS_PRODUCTS),
        InlineKeyboardButton(text="🏠 На главную", callback_data=CallbackData.HOME)
    ]
    return create_inline_keyboard(buttons, adjust=(2,))

def admin_kb_back() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру с кнопками "⚙️ Админ панель" и "🏠 На главную".

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с кнопками возврата в админ-панель и на главную.
    """
    buttons = [
        InlineKeyboardButton(text="⚙️ Админ панель", callback_data=CallbackData.ADMIN_PANEL),
        InlineKeyboardButton(text="🏠 На главную", callback_data=CallbackData.HOME)
    ]
    return create_inline_keyboard(buttons, adjust=(1,))

def dell_product_kb(product_id: int) -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для подтверждения удаления товара.

    Args:
        product_id (int): ID товара для удаления.

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с кнопками "🗑️ Удалить", "⚙️ Админ панель" и "🏠 На главную".
    """
    buttons = [
        InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"{CallbackData.DELL_PRODUCT}{product_id}"),
        InlineKeyboardButton(text="⚙️ Админ панель", callback_data=CallbackData.ADMIN_PANEL),
        InlineKeyboardButton(text="🏠 На главную", callback_data=CallbackData.HOME)
    ]
    return create_inline_keyboard(buttons, adjust=(2, 1))

def product_management_kb() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для управления товарами.

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с кнопками "➕ Добавить товар", "🗑️ Удалить товар", "⚙️ Админ панель" и "🏠 На главную".
    """
    buttons = [
        InlineKeyboardButton(text="➕ Добавить товар", callback_data=CallbackData.ADD_PRODUCT),
        InlineKeyboardButton(text="🗑️ Удалить товар", callback_data=CallbackData.DELETE_PRODUCT),
        InlineKeyboardButton(text="⚙️ Админ панель", callback_data=CallbackData.ADMIN_PANEL),
        InlineKeyboardButton(text="🏠 На главную", callback_data=CallbackData.HOME)
    ]
    return create_inline_keyboard(buttons, adjust=(2, 2))

def cancel_kb_inline() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру с кнопкой "Отмена".

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с кнопкой "Отмена".
    """
    buttons = [
        InlineKeyboardButton(text="Отмена", callback_data=CallbackData.CANCEL)
    ]
    return create_inline_keyboard(buttons, adjust=(1,))

def admin_confirm_kb() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для подтверждения добавления товара.

    Returns:
        InlineKeyboardMarkup: Inline-клавиатура с кнопками "Все верно" и "Отмена".
    """
    buttons = [
        InlineKeyboardButton(text="Все верно", callback_data=CallbackData.CONFIRM_ADD),
        InlineKeyboardButton(text="Отмена", callback_data=CallbackData.ADMIN_PANEL)
    ]
    return create_inline_keyboard(buttons, adjust=(1,))