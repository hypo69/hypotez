### **Анализ кода модуля `catalog_router.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/user/catalog_router.py

Модуль содержит роутер для обработки запросов, связанных с каталогом товаров в Telegram-боте.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и логически разделен на функции.
  - Используются аннотации типов.
  - Присутствуют обработчики callback-запросов и сообщений об успешной оплате.
- **Минусы**:
  - Отсутствует подробная документация для всех функций и классов.
  - Обработка исключений в `page_catalog` выполнена слишком просто (просто `pass`).
  - Не все переменные имеют аннотации типов.
  - Используются разные стили кавычек (как двойные, так и одинарные).

**Рекомендации по улучшению:**

1.  **Документирование функций**:
    - Добавить docstring к каждой функции, описывающий её назначение, аргументы, возвращаемые значения и возможные исключения.

2.  **Обработка исключений**:
    - В блоке `except` в функции `page_catalog` следует добавить логирование ошибки с использованием `logger.error` для более информативной отладки.

3.  **Унификация кавычек**:
    - Заменить все двойные кавычки на одинарные для соответствия стандартам.

4.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.

5.  **Использовать `j_loads` или `j_loads_ns`**:
    - Проверь и замени стандартные `open` и `json.load` на `j_loads` или `j_loads_ns`.

6.  **Логирование**:
    - Добавить логирование важных событий и ошибок для облегчения отладки и мониторинга.

**Оптимизированный код:**

```python
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger import logger  # Импорт логгера
from bot.app.utils import generate_payment_link
from bot.config import bot, settings
from bot.dao.dao import UserDAO, CategoryDao, ProductDao, PurchaseDao
from bot.user.kbs import catalog_kb, product_kb, get_product_buy_youkassa, \
    get_product_buy_stars, get_product_buy_robocassa
from bot.user.schemas import TelegramIDModel, ProductCategoryIDModel, PaymentData
from bot.user.utils import successful_payment_logic

catalog_router = Router()


@catalog_router.callback_query(F.data == 'catalog')
async def page_catalog(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик callback-запроса для отображения каталога товаров.

    Args:
        call (CallbackQuery): Объект callback-запроса.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None

    Raises:
        Exception: Если не удается удалить предыдущее сообщение.
    """
    await call.answer('Загрузка каталога...')
    try:
        await call.message.delete()
    except Exception as ex:
        logger.error('Не удалось удалить предыдущее сообщение', ex, exc_info=True)  # Логирование ошибки
    catalog_data: list = await CategoryDao.find_all(session=session_without_commit)

    await call.message.answer(
        text='Выберите категорию товаров:',
        reply_markup=catalog_kb(catalog_data)
    )


@catalog_router.callback_query(F.data.startswith('category_'))
async def page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик callback-запроса для отображения товаров выбранной категории.

    Args:
        call (CallbackQuery): Объект callback-запроса.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None
    """
    category_id: int = int(call.data.split('_')[-1])
    products_category: list = await ProductDao.find_all(
        session=session_without_commit,
        filters=ProductCategoryIDModel(category_id=category_id)
    )
    count_products: int = len(products_category)
    if count_products:
        await call.answer(f'В данной категории {count_products} товаров.')
        for product in products_category:
            product_text: str = (
                f'📦 <b>Название товара:</b> {product.name}\\n\\n'
                f'💰 <b>Цена:</b> {product.price} руб.\\n\\n'
                f'📝 <b>Описание:</b>\\n<i>{product.description}</i>\\n\\n'
                f'━━━━━━━━━━━━━━━━━━'
            )
            await call.message.answer(
                product_text,
                reply_markup=product_kb(product.id, product.price, 1)
            )
    else:
        await call.answer('В данной категории нет товаров.')


@catalog_router.callback_query(F.data.startswith('buy_'))
async def process_about(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик callback-запроса для обработки покупки товара.

    Args:
        call (CallbackQuery): Объект callback-запроса.
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

    await call.message.delete()


async def send_yukassa_invoice(call: CallbackQuery, user_info, product_id: str, price: str) -> None:
    """
    Отправляет инвойс для оплаты через ЮKassa.

    Args:
        call (CallbackQuery): Объект callback-запроса.
        user_info: Информация о пользователе.
        product_id (str): Идентификатор товара.
        price (str): Цена товара.

    Returns:
        None
    """
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f'Оплата 👉 {price}₽',
        description=f'Пожалуйста, завершите оплату в размере {price}₽, чтобы открыть доступ к выбранному товару.',
        payload=f'yukassa_{user_info.id}_{product_id}',
        provider_token=settings.PROVIDER_TOKEN,
        currency='rub',
        prices=[LabeledPrice(
            label=f'Оплата {price}',
            amount=int(price) * 100
        )],
        reply_markup=get_product_buy_youkassa(price)
    )


async def send_robocassa_invoice(call: CallbackQuery, user_info, product_id: str, price: str,
                                 session: AsyncSession) -> None:
    """
    Отправляет инвойс для оплаты через Robocassa.

    Args:
        call (CallbackQuery): Объект callback-запроса.
        user_info: Информация о пользователе.
        product_id (str): Идентификатор товара.
        price (str): Цена товара.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        None
    """
    pay_id: int = await PurchaseDao.get_next_id(session=session)
    text: str = f'Пожалуйста, завершите оплату в размере {price}₽, чтобы открыть доступ к выбранному товару.'
    description: str = f'Оплата за товар: ID {user_info.id} ({price}₽)'
    payment_link: str = generate_payment_link(cost=float(price), number=pay_id, description=description,
                                         user_id=user_info.id, user_telegram_id=call.from_user.id,
                                         product_id=product_id)
    kb = get_product_buy_robocassa(price, payment_link)
    await call.message.answer(text, reply_markup=kb)


async def send_stars_invoice(call: CallbackQuery, user_info, product_id: str, stars_price: int) -> None:
    """
    Отправляет инвойс для оплаты звездами.

    Args:
        call (CallbackQuery): Объект callback-запроса.
        user_info: Информация о пользователе.
        product_id (str): Идентификатор товара.
        stars_price (int): Цена в звездах.

    Returns:
        None
    """
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f'Оплата 👉 {stars_price} ⭐',
        description=f'Пожалуйста, завершите оплату в размере {stars_price} звезд, '
                    f'чтобы открыть доступ к выбранному товару.',
        payload=f'stars_{user_info.id}_{product_id}',
        provider_token='',
        currency='XTR',
        prices=[LabeledPrice(
            label=f'Оплата {stars_price} ⭐',
            amount=int(stars_price)
        )],
        reply_markup=get_product_buy_stars(stars_price)
    )


@catalog_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery) -> None:
    """
    Обработчик pre-checkout query.

    Args:
        pre_checkout_q (PreCheckoutQuery): Объект pre-checkout query.

    Returns:
        None
    """
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@catalog_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, session_with_commit: AsyncSession) -> None:
    """
    Обработчик сообщения об успешной оплате.

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