### **Анализ кода модуля `catalog_router`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/user/catalog_router.py

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `Router` из `aiogram` для обработки callback-запросов.
    - Логическая структура разделена на функции для обработки различных типов запросов.
    - Использование асинхронных функций для работы с Telegram Bot API и базой данных.
- **Минусы**:
    - Отсутствует обработка исключений в некоторых местах (например, в функции `page_catalog`, исключение `e` проигнорировано).
    - Не все переменные аннотированы типами.
    - Жестко заданные значения, такие как `10` в `send_stars_invoice`, должны быть вынесены в константы или параметры конфигурации.
    - Не везде используется `logger` для записи ошибок и отладочной информации.
    - Magic strings (например, `'yukassa'`, `'stars'`, `'robocassa'`) разбросаны по коду.
    - Не хватает обобщенной обработки ошибок при отправке счетов.
    - Дублирование логики отправки счетов (почти идентичные блоки кода в `send_yukassa_invoice` и `send_stars_invoice`).

**Рекомендации по улучшению:**

- Добавить обработку исключений с использованием `logger.error` для записи ошибок и `exc_info=True` для получения трассировки стека.
- Добавить аннотации типов для всех переменных и параметров функций.
- Заменить жестко заданные значения константами или параметрами конфигурации.
- Использовать `enums` вместо строковых литералов для `payment_type`.
- Рефакторинг логики отправки счетов для устранения дублирования кода.
- Добавить общую функцию для отправки счетов с параметризацией необходимых данных.
- Добавить docstring к каждой функции.
- Улучшить обработку ошибок, возникающих при удалении сообщения в функции `page_catalog`.
- Изменить обработку ошибок `Exception as e` на более конкретные типы исключений, где это возможно.
- Добавить логирование действий пользователей (например, выбор категории, запрос товара).
- Всегда добавляй пробелы вокруг оператора `=`, чтобы повысить читаемость.

**Оптимизированный код:**

```python
"""
Модуль для обработки каталога товаров в Telegram боте.
========================================================

Модуль содержит функции для отображения каталога категорий, товаров,
обработки покупок и платежей через различные платежные системы.
"""
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger import logger # подключаем logger
from bot.app.utils import generate_payment_link
from bot.config import bot, settings
from bot.dao.dao import UserDAO, CategoryDao, ProductDao, PurchaseDao
from bot.user.kbs import catalog_kb, product_kb, get_product_buy_youkassa, \
    get_product_buy_stars, get_product_buy_robocassa
from bot.user.schemas import TelegramIDModel, ProductCategoryIDModel, PaymentData
from bot.user.utils import successful_payment_logic

catalog_router = Router()

PAYMENT_TYPE_YUKASSA: str = 'yukassa'
PAYMENT_TYPE_STARS: str = 'stars'
PAYMENT_TYPE_ROBOCASSA: str = 'robocassa'
CURRENCY_RUB: str = 'rub'
CURRENCY_XTR: str = 'XTR'
STARS_DEFAULT_AMOUNT: int = 10


@catalog_router.callback_query(F.data == "catalog")
async def page_catalog(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Отображает каталог категорий товаров.

    Args:
        call (CallbackQuery): Объект CallbackQuery, содержащий информацию о вызове.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при удалении предыдущего сообщения.
    """
    await call.answer("Загрузка каталога...")
    try:
        await call.message.delete()
    except Exception as ex: # Обрабатываем исключение и логируем его
        logger.error('Error while deleting message', ex, exc_info=True)

    catalog_data = await CategoryDao.find_all(session=session_without_commit)

    await call.message.answer(
        text="Выберите категорию товаров:",
        reply_markup=catalog_kb(catalog_data)
    )


@catalog_router.callback_query(F.data.startswith("category_"))
async def page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Отображает товары выбранной категории.

    Args:
        call (CallbackQuery): Объект CallbackQuery, содержащий информацию о вызове.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при выполнении запроса к базе данных.
    """
    category_id: int = int(call.data.split("_")[-1])
    products_category = await ProductDao.find_all(session=session_without_commit,
                                                  filters=ProductCategoryIDModel(category_id=category_id))
    count_products: int = len(products_category)
    if count_products:
        await call.answer(f"В данной категории {count_products} товаров.")
        for product in products_category:
            product_text: str = (
                f"📦 <b>Название товара:</b> {product.name}\n\n"
                f"💰 <b>Цена:</b> {product.price} руб.\n\n"
                f"📝 <b>Описание:</b>\n<i>{product.description}</i>\n\n"
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
        call (CallbackQuery): Объект CallbackQuery, содержащий информацию о вызове.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Raises:
        ValueError: Если данные в `call.data` имеют неверный формат.
        Exception: Если происходит ошибка при выполнении запроса к базе данных или отправке счета.
    """
    user_info = await UserDAO.find_one_or_none(
        session=session_without_commit,
        filters=TelegramIDModel(telegram_id=call.from_user.id)
    )

    try:
        _, payment_type, product_id, price = call.data.split('_')
    except ValueError as ex:
        logger.error(f'Invalid data format in callback query: {call.data}', ex, exc_info=True)
        await call.answer('Произошла ошибка. Пожалуйста, попробуйте еще раз.')
        return

    if payment_type == PAYMENT_TYPE_YUKASSA:
        await send_yukassa_invoice(call, user_info, product_id, price)
    elif payment_type == PAYMENT_TYPE_STARS:
        await send_stars_invoice(call, user_info, product_id, STARS_DEFAULT_AMOUNT)
    elif payment_type == PAYMENT_TYPE_ROBOCASSA:
        await send_robocassa_invoice(call, user_info, product_id, price, session_without_commit)
    else:
        logger.warning(f'Unknown payment type: {payment_type}')
        await call.answer('Неизвестный тип оплаты.')

    try:
        await call.message.delete()
    except Exception as ex:
        logger.error('Error while deleting message', ex, exc_info=True)


async def send_yukassa_invoice(call: CallbackQuery, user_info: object, product_id: str, price: str) -> None:
    """
    Отправляет счет для оплаты через ЮKassa.

    Args:
        call (CallbackQuery): Объект CallbackQuery, содержащий информацию о вызове.
        user_info (object): Информация о пользователе.
        product_id (str): Идентификатор товара.
        price (str): Цена товара.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при отправке счета.
    """
    try:
        await bot.send_invoice(
            chat_id=call.from_user.id,
            title=f'Оплата 👉 {price}₽',
            description=f'Пожалуйста, завершите оплату в размере {price}₽, чтобы открыть доступ к выбранному товару.',
            payload=f"{PAYMENT_TYPE_YUKASSA}_{user_info.id}_{product_id}",
            provider_token=settings.PROVIDER_TOKEN,
            currency=CURRENCY_RUB,
            prices=[LabeledPrice(
                label=f'Оплата {price}',
                amount=int(price) * 100
            )],
            reply_markup=get_product_buy_youkassa(price)
        )
    except Exception as ex:
        logger.error('Error while sending Yookassa invoice', ex, exc_info=True)
        await call.answer('Произошла ошибка при формировании счета. Пожалуйста, попробуйте позже.')


async def send_robocassa_invoice(call: CallbackQuery, user_info: object, product_id: str, price: str, session: AsyncSession) -> None:
    """
    Отправляет счет для оплаты через Robokassa.

    Args:
        call (CallbackQuery): Объект CallbackQuery, содержащий информацию о вызове.
        user_info (object): Информация о пользователе.
        product_id (str): Идентификатор товара.
        price (str): Цена товара.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при формировании ссылки на оплату или отправке сообщения.
    """
    pay_id: int = await PurchaseDao.get_next_id(session=session)
    text: str = f'Пожалуйста, завершите оплату в размере {price}₽, чтобы открыть доступ к выбранному товару.'
    description: str = f"Оплата за товар: ID {user_info.id} ({price}₽)"
    payment_link: str = generate_payment_link(cost=float(price), number=pay_id, description=description,
                                         user_id=user_info.id, user_telegram_id=call.from_user.id,
                                         product_id=product_id)
    kb = get_product_buy_robocassa(price, payment_link)
    try:
        await call.message.answer(text, reply_markup=kb)
    except Exception as ex:
        logger.error('Error while sending Robokassa invoice', ex, exc_info=True)
        await call.answer('Произошла ошибка при формировании счета. Пожалуйста, попробуйте позже.')


async def send_stars_invoice(call: CallbackQuery, user_info: object, product_id: str, stars_price: int) -> None:
    """
    Отправляет счет для оплаты звездами (внутренняя валюта).

    Args:
        call (CallbackQuery): Объект CallbackQuery, содержащий информацию о вызове.
        user_info (object): Информация о пользователе.
        product_id (str): Идентификатор товара.
        stars_price (int): Цена товара в звездах.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при отправке счета.
    """
    try:
        await bot.send_invoice(
            chat_id=call.from_user.id,
            title=f'Оплата 👉 {stars_price} ⭐',
            description=f'Пожалуйста, завершите оплату в размере {stars_price} звезд, '
                        f'чтобы открыть доступ к выбранному товару.',
            payload=f"{PAYMENT_TYPE_STARS}_{user_info.id}_{product_id}",
            provider_token="",
            currency=CURRENCY_XTR,
            prices=[LabeledPrice(
                label=f'Оплата {stars_price} ⭐',
                amount=int(stars_price)
            )],
            reply_markup=get_product_buy_stars(stars_price)
        )
    except Exception as ex:
        logger.error('Error while sending Stars invoice', ex, exc_info=True)
        await call.answer('Произошла ошибка при формировании счета. Пожалуйста, попробуйте позже.')


@catalog_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery) -> None:
    """
    Обрабатывает предварительный запрос перед подтверждением оплаты.

    Args:
        pre_checkout_q (PreCheckoutQuery): Объект PreCheckoutQuery, содержащий информацию о запросе.

    Returns:
        None
    """
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@catalog_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, session_with_commit: AsyncSession) -> None:
    """
    Обрабатывает успешную оплату.

    Args:
        message (Message): Объект Message, содержащий информацию о сообщении.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при обработке успешной оплаты.
    """
    payment_info = message.successful_payment
    payment_type, user_id, product_id = payment_info.invoice_payload.split('_')

    if payment_type == PAYMENT_TYPE_STARS:
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

    try:
        await successful_payment_logic(session=session_with_commit,
                                       payment_data=payment_data, currency=currency,
                                       user_tg_id=message.from_user.id, bot=bot)
    except Exception as ex:
        logger.error('Error in successful_payment_logic', ex, exc_info=True)
        await message.answer('Произошла ошибка при обработке платежа.')