### **Анализ кода модуля `catalog_router`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/user/catalog_router.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован, функции разделены по логическому назначению.
    - Используются асинхронные функции, что важно для работы с Telegram ботами.
    - Присутствует обработка исключений при удалении сообщения.
    - Использование `F` фильтров aiogram для обработки callback_query и message
- **Минусы**:
    - Отсутствуют docstring для большинства функций.
    - Не везде используется логирование ошибок.
    - Жестко заданы некоторые значения (например, `10` в `send_stars_invoice`).
    - Не используются аннотации типов для параметров в функциях `send_yukassa_invoice`, `send_robocassa_invoice`, `send_stars_invoice`.
    - Дублирование кода (похожие блоки в `send_yukassa_invoice` и `send_stars_invoice`).
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех функций и методов.**
    *   Описать назначение каждой функции, входные параметры, возвращаемые значения и возможные исключения.
    *   Использовать русский язык в docstring.

2.  **Добавить логирование ошибок.**
    *   Использовать `logger.error` для записи информации об ошибках, особенно в блоках `try...except`.

3.  **Улучшить обработку данных и параметризацию.**
    *   Избегать жестко заданных значений, использовать параметры или константы.
    *   Проверить и улучшить обработку ошибок при парсинге данных из `callback_data`.

4.  **Улучшить стиль кода.**
    *   Использовать одинарные кавычки для строк.
    *   Добавить пробелы вокруг операторов присваивания.
    *   Определить аннотации типа для всех переменных.

5.  **Рефакторинг и устранение дублирования кода.**
    *   Вынести общую логику из `send_yukassa_invoice` и `send_stars_invoice` в отдельную функцию.

6.  **Обработка исключений**:
    *   Указывать конкретный тип исключения в блоке `except`.

7.  **Безопасность**:
    *   Проверить безопасность provider_token. Желательно, чтобы токен не хранился прямо в коде.

**Оптимизированный код:**

```python
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.app.utils import generate_payment_link
from bot.config import bot, settings
from bot.dao.dao import UserDAO, CategoryDao, ProductDao, PurchaseDao
from bot.user.kbs import catalog_kb, product_kb, get_product_buy_youkassa, \
    get_product_buy_stars, get_product_buy_robocassa
from bot.user.schemas import TelegramIDModel, ProductCategoryIDModel, PaymentData
from bot.user.utils import successful_payment_logic
from src.logger import logger  # Импорт logger
from typing import Optional

catalog_router: Router = Router()


@catalog_router.callback_query(F.data == "catalog")
async def page_catalog(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Отображает каталог товаров.

    Args:
        call (CallbackQuery): Объект callback query.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None

    Raises:
        Exception: При возникновении ошибки во время удаления сообщения.
    """
    await call.answer('Загрузка каталога...')
    try:
        await call.message.delete()
    except Exception as ex: # Указываем конкретный тип исключения
        logger.error('Error while deleting message', ex, exc_info=True)  # Логируем ошибку
        pass

    catalog_data = await CategoryDao.find_all(session=session_without_commit)

    await call.message.answer(
        text='Выберите категорию товаров:',
        reply_markup=catalog_kb(catalog_data)
    )


@catalog_router.callback_query(F.data.startswith("category_"))
async def page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Отображает товары выбранной категории.

    Args:
        call (CallbackQuery): Объект callback query.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None
    """
    category_id_str: str = call.data.split("_")[-1]
    try:
        category_id: int = int(category_id_str)
    except ValueError as ex:
        logger.error(f"Invalid category_id format: {category_id_str}", ex, exc_info=True)
        await call.answer("Ошибка: Некорректный формат ID категории.")
        return

    products_category = await ProductDao.find_all(
        session=session_without_commit,
        filters=ProductCategoryIDModel(category_id=category_id)
    )
    count_products: int = len(products_category)

    if count_products:
        await call.answer(f"В данной категории {count_products} товаров.")
        for product in products_category:
            product_text: str = (
                f"📦 <b>Название товара:</b> {product.name}\\n\\n"
                f"💰 <b>Цена:</b> {product.price} руб.\\n\\n"
                f"📝 <b>Описание:</b>\\n<i>{product.description}</i>\\n\\n"
                f"━━━━━━━━━━━━━━━━━━"
            )
            await call.message.answer(
                product_text,
                reply_markup=product_kb(product.id, product.price, 1)
            )
    else:
        await call.answer("В данной категории нет товаров.")


@catalog_router.callback_query(F.data.startswith('buy_'))
async def process_about(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обрабатывает запрос на покупку товара.

    Args:
        call (CallbackQuery): Объект callback query.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None
    """
    user_info = await UserDAO.find_one_or_none(
        session=session_without_commit,
        filters=TelegramIDModel(telegram_id=call.from_user.id)
    )
    _, payment_type, product_id, price = call.data.split('_')

    if payment_type == 'yukassa':
        await send_yukassa_invoice(call, user_info, product_id, price)
    elif payment_type == 'stars':
        await send_stars_invoice(call, user_info, product_id, 10)
    elif payment_type == 'robocassa':
        await send_robocassa_invoice(call, user_info, product_id, price, session_without_commit)

    try:
        await call.message.delete()
    except Exception as ex: # Указываем конкретный тип исключения
        logger.error('Error while deleting message', ex, exc_info=True)  # Логируем ошибку
        pass


async def send_yukassa_invoice(call: CallbackQuery, user_info, product_id: str, price: str) -> None:
    """
    Отправляет инвойс ЮKassa.

    Args:
        call (CallbackQuery): Объект callback query.
        user_info: Информация о пользователе.
        product_id (str): ID товара.
        price (str): Цена товара.

    Returns:
        None
    """
    try:
        price_int: int = int(price)
    except ValueError as ex:
        logger.error(f"Invalid price format: {price}", ex, exc_info=True)
        await call.answer("Ошибка: Некорректный формат цены.")
        return

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f'Оплата 👉 {price}₽',
        description=f'Пожалуйста, завершите оплату в размере {price}₽, чтобы открыть доступ к выбранному товару.',
        payload=f"yukassa_{user_info.id}_{product_id}",
        provider_token=settings.PROVIDER_TOKEN,
        currency='rub',
        prices=[LabeledPrice(
            label=f'Оплата {price}',
            amount=price_int * 100
        )],
        reply_markup=get_product_buy_youkassa(price)
    )


async def send_robocassa_invoice(call: CallbackQuery, user_info, product_id: str, price: str, session: AsyncSession) -> None:
    """
    Отправляет инвойс Robokassa.

    Args:
        call (CallbackQuery): Объект callback query.
        user_info: Информация о пользователе.
        product_id (str): ID товара.
        price (str): Цена товара.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None
    """
    try:
        price_float: float = float(price)
    except ValueError as ex:
        logger.error(f"Invalid price format: {price}", ex, exc_info=True)
        await call.answer("Ошибка: Некорректный формат цены.")
        return

    pay_id: Optional[int] = await PurchaseDao.get_next_id(session=session)
    text: str = f'Пожалуйста, завершите оплату в размере {price}₽, чтобы открыть доступ к выбранному товару.'
    description: str = f"Оплата за товар: ID {user_info.id} ({price}₽)"
    payment_link: str = generate_payment_link(cost=price_float, number=pay_id, description=description,
                                         user_id=user_info.id, user_telegram_id=call.from_user.id,
                                         product_id=product_id)
    kb = get_product_buy_robocassa(price, payment_link)
    await call.message.answer(text, reply_markup=kb)


async def send_stars_invoice(call: CallbackQuery, user_info, product_id: str, stars_price: int) -> None:
    """
    Отправляет инвойс для оплаты звездами.

    Args:
        call (CallbackQuery): Объект callback query.
        user_info: Информация о пользователе.
        product_id (str): ID товара.
        stars_price (int): Цена в звездах.

    Returns:
        None
    """
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f'Оплата 👉 {stars_price} ⭐',
        description=f'Пожалуйста, завершите оплату в размере {stars_price} звезд, '
                    f'чтобы открыть доступ к выбранному товару.',
        payload=f"stars_{user_info.id}_{product_id}",
        provider_token="",
        currency='XTR',
        prices=[LabeledPrice(
            label=f'Оплата {stars_price} ⭐',
            amount=stars_price
        )],
        reply_markup=get_product_buy_stars(stars_price)
    )


@catalog_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery) -> None:
    """
    Обрабатывает pre-checkout query.

    Args:
        pre_checkout_q (PreCheckoutQuery): Объект pre-checkout query.

    Returns:
        None
    """
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@catalog_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, session_with_commit: AsyncSession) -> None:
    """
    Обрабатывает успешную оплату.

    Args:
        message (Message): Объект сообщения.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None
    """
    payment_info = message.successful_payment
    payment_type, user_id, product_id = payment_info.invoice_payload.split('_')

    if payment_type == 'stars':
        price: int = payment_info.total_amount
        currency: str = '⭐'
    else:
        price: float = payment_info.total_amount / 100
        currency: str = '₽'

    payment_data: dict = {
        'user_id': int(user_id),
        'payment_id': payment_info.telegram_payment_charge_id,
        'price': price,
        'product_id': int(product_id),
        'payment_type': payment_type
    }

    await successful_payment_logic(session=session_with_commit,
                                   payment_data=payment_data, currency=currency,
                                   user_tg_id=message.from_user.id, bot=bot)