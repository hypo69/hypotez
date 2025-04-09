### **Анализ кода модуля `utils.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код выполняет логику успешной оплаты, включая добавление записи о покупке, отправку уведомлений администраторам и предоставление информации пользователю.
    - Использование `AsyncSession` для асинхронной работы с базой данных.
    - Использование `logger` для логирования ошибок.
- **Минусы**:
    - Отсутствуют аннотации типов для переменных, полученных из `payment_data`.
    - Обработка исключений для отправки уведомлений администраторам может быть улучшена.
    - Использованы двойные кавычки.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для переменных, полученных из `payment_data`, чтобы улучшить читаемость и облегчить отладку.
2.  **Улучшить обработку исключений**:
    - В блоке `except` при отправке уведомлений администраторам, вместо простого логирования ошибки, можно добавить дополнительную логику, например, повторную отправку уведомления через некоторое время или отправку уведомления в резервный канал.
3.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные.
4.  **Добавить Docstring**:
    - Добавить описание в Docstring для каждой функции, включая описание параметров, возвращаемого значения и возможных исключений.
5.  **Использовать f-строки**:
    - В f-строках нет необходимости оборачивать переменные в фигурные скобки, если сразу указан метод.

**Оптимизированный код:**

```python
from aiogram import Bot
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import settings
from bot.dao.dao import PurchaseDao, ProductDao
from bot.user.kbs import main_user_kb
from bot.user.schemas import PaymentData
from typing import Dict, Any

async def successful_payment_logic(
    session: AsyncSession,
    payment_data: Dict[str, Any],
    currency: str,
    user_tg_id: int,
    bot: Bot
) -> None:
    """
    Обрабатывает логику успешной оплаты, добавляет запись о покупке,
    отправляет уведомления администраторам и предоставляет информацию пользователю.

    Args:
        session (AsyncSession): Сессия базы данных SQLAlchemy.
        payment_data (Dict[str, Any]): Данные об оплате.
        currency (str): Валюта платежа.
        user_tg_id (int): ID пользователя в Telegram.
        bot (Bot): Экземпляр бота aiogram.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при отправке уведомления администраторам.
    """
    product_id: int = int(payment_data.get('product_id'))
    price: str = payment_data.get('price')
    payment_type: str = payment_data.get('payment_type')
    payment_id: str = payment_data.get('payment_id')
    user_id: str = payment_data.get('user_id')
    await PurchaseDao.add(session=session, values=PaymentData(**payment_data))
    product_data = await ProductDao.find_one_or_none_by_id(session=session,
                                                           data_id=product_id)

    # Отправка уведомлений администраторам
    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f'💲 Пользователь c ID {user_id} купил товар <b>{product_data.name}</b> (ID: {product_id}) '
                    f'за <b>{price} {currency}</b>.'
                )
            )
        except Exception as ex:
            logger.error(f'Ошибка при отправке уведомления администраторам: {ex}', exc_info=True)

    # Отправка информации пользователю
    file_text: str = '📦 <b>Товар включает файл:</b>' if product_data.file_id else '📄 <b>Товар не включает файлы:</b>'
    product_text: str = (
        f'🎉 <b>Спасибо за покупку!</b>\n\n'
        f'🛒 <b>Информация о вашем товаре:</b>\n'
        f'━━━━━━━━━━━━━━━━━━\n'
        f'🔹 <b>Название:</b> <b>{product_data.name}</b>\n'
        f'🔹 <b>Описание:</b>\n<i>{product_data.description}</i>\n'
        f'🔹 <b>Цена:</b> <b>{price} {currency}</b>\n'
        f'🔹 <b>Закрытое описание:</b>\n<i>{product_data.hidden_content}</i>\n'
        f'━━━━━━━━━━━━━━━━━━\n'
        f'{file_text}\n\n'
        f'ℹ️ <b>Информацию о всех ваших покупках вы можете найти в личном профиле.</b>'
    )

    if product_data.file_id:
        await bot.send_document(document=product_data.file_id,
                                chat_id=user_tg_id,
                                caption=product_text, reply_markup=main_user_kb(user_tg_id))

    else:
        await bot.send_message(chat_id=user_tg_id, text=product_text, reply_markup=main_user_kb(user_tg_id))

    # автоматический возврат звезд за покупку
    if payment_type == 'stars':
        await bot.refund_star_payment(user_id=user_tg_id, telegram_payment_charge_id=payment_id)