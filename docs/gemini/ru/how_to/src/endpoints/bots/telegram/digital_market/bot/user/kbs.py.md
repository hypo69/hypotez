### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет набор функций для создания различных встроенных клавиатур (InlineKeyboardMarkup) для Telegram-бота. Каждая клавиатура предназначена для выполнения определенных действий, таких как навигация по каталогу, совершение покупок, переход в профиль пользователя или админ-панель. Клавиатуры создаются с использованием библиотеки `aiogram`.

Шаги выполнения
-------------------------
1. **`main_user_kb(user_id: int)`**:
   - Функция создает главную клавиатуру пользователя с кнопками: "Мои покупки", "Каталог", "О магазине", "Поддержать автора".
   - Если `user_id` присутствует в списке `settings.ADMIN_IDS`, добавляется кнопка "Админ панель".
   - Кнопки располагаются в один столбец.

2. **`catalog_kb(catalog_data: List[Category])`**:
   - Функция создает клавиатуру каталога на основе списка категорий `catalog_data`.
   - Для каждой категории добавляется кнопка с названием категории.
   - Добавляется кнопка "На главную" для возврата к главной клавиатуре.
   - Кнопки располагаются в два столбца.

3. **`purchases_kb()`**:
   - Функция создает клавиатуру для просмотра покупок с кнопками: "Смотреть покупки" и "На главную".
   - Кнопки располагаются в один столбец.

4. **`product_kb(product_id, price, stars_price)`**:
   - Функция создает клавиатуру для отображения вариантов покупки товара с заданным `product_id` и `price`.
   - Добавляются кнопки для оплаты через ЮКасса, Robocassa и звездами.
   - Добавляются кнопки "Назад" (к каталогу) и "На главную".
   - Кнопки располагаются в два столбца.

5. **`get_product_buy_youkassa(price)`**:
   - Функция создает клавиатуру для оплаты через ЮKassa.
   - Добавляется кнопка "Оплатить {price}₽" с включенной опцией `pay=True` (для запроса оплаты).
   - Добавляется кнопка "Отменить" для возврата на главную.

6. **`get_product_buy_robocassa(price: int, payment_link: str)`**:
   - Функция создает клавиатуру для оплаты через Robocassa.
   - Добавляется кнопка "Оплатить {price}₽" с использованием `WebAppInfo` для перенаправления на страницу оплаты.
   - Добавляется кнопка "Отменить" для возврата на главную.

7. **`get_product_buy_stars(price)`**:
   - Функция создает клавиатуру для оплаты звездами.
   - Добавляется кнопка "Оплатить {price} ⭐" с включенной опцией `pay=True`.
   - Добавляется кнопка "Отменить" для возврата на главную.

Пример использования
-------------------------

```python
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.config import settings
from bot.user.kbs import main_user_kb, catalog_kb, product_kb
from bot.dao.models import Category

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    """
    Обработчик команды /start.

    Args:
        message (Message): Объект сообщения от Telegram.

    """
    user_id = message.from_user.id
    keyboard = main_user_kb(user_id)
    await message.answer("Добро пожаловать в магазин!", reply_markup=keyboard)

# Пример использования catalog_kb
@dp.message(Command("catalog"))
async def show_catalog(message: Message):
    """
    Обработчик команды /catalog.

    Args:
        message (Message): Объект сообщения от Telegram.

    """
    # Подготавливаем данные о категориях (в реальном коде они будут загружаться из БД)
    categories = [
        Category(id=1, category_name="Электроника"),
        Category(id=2, category_name="Одежда"),
    ]
    keyboard = catalog_kb(categories)
    await message.answer("Выберите категорию:", reply_markup=keyboard)

# Пример использования product_kb
@dp.message(Command("buy"))
async def show_product(message: Message):
    """
    Обработчик команды /buy.

    Args:
        message (Message): Объект сообщения от Telegram.

    """
    product_id = 123
    price = 100
    stars_price = 50
    keyboard = product_kb(product_id, price, stars_price)
    await message.answer("Выберите способ оплаты:", reply_markup=keyboard)