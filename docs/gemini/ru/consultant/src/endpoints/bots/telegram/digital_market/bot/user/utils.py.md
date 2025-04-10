### **Анализ кода модуля `utils.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и логически понятен.
    - Используются асинхронные функции, что хорошо для производительности.
    - Присутствует обработка исключений при отправке уведомлений администраторам.
    - Использование `PurchaseDao` и `ProductDao` для работы с базой данных.
- **Минусы**:
    - Отсутствуют аннотации типов для переменных `payment_data`, `currency`, `user_tg_id`, `bot`.
    - Исключение перехватывается как `e`, следует использовать `ex`.
    - Не используется модуль `logger` из `src.logger`.
    - В строке `file_text = "📦 <b>Товар включает файл:</b>" if product_data.file_id else "📄 <b>Товар не включает файлы:</b>"` нет пробелов вокруг оператора `=`
    - Отсутствуют docstring для функции `successful_payment_logic`.
    - Использованы двойные кавычки.

**Рекомендации по улучшению:**

1.  **Добавить docstring для функции `successful_payment_logic`**:

    ```python
    async def successful_payment_logic(session: AsyncSession, payment_data: dict, currency: str, user_tg_id: int, bot: Bot):
        """
        Обрабатывает успешную оплату товара: добавляет запись о покупке в БД,
        отправляет уведомления администраторам и пользователю.

        Args:
            session (AsyncSession): Сессия базы данных SQLAlchemy.
            payment_data (dict): Данные об оплате.
            currency (str): Валюта платежа.
            user_tg_id (int): ID пользователя в Telegram.
            bot (Bot): Экземпляр бота aiogram.

        Returns:
            None

        Raises:
            Exception: При возникновении ошибки при отправке уведомления администраторам.

        Example:
            # Пример использования функции
            >>> await successful_payment_logic(session, payment_data, currency, user_tg_id, bot)
        """
    ```

2.  **Использовать одинарные кавычки**: Заменить все двойные кавычки на одинарные.
3.  **Добавить аннотации типов**: Указать типы для всех переменных и параметров функций.
4.  **Использовать `logger` из `src.logger`**: Заменить `from loguru import logger` на `from src.logger import logger` и использовать его для логирования ошибок.
5.  **Переименовать переменную исключения**: Заменить `except Exception as e` на `except Exception as ex`.
6.  **Добавить пробелы вокруг операторов присваивания**: Добавить пробелы вокруг оператора `=` для повышения читаемости.

**Оптимизированный код:**

```python
from aiogram import Bot
from src.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import settings
from bot.dao.dao import PurchaseDao, ProductDao
from bot.user.kbs import main_user_kb
from bot.user.schemas import PaymentData


async def successful_payment_logic(session: AsyncSession, payment_data: dict, currency: str, user_tg_id: int, bot: Bot) -> None:
    """
    Обрабатывает успешную оплату товара: добавляет запись о покупке в БД,
    отправляет уведомления администраторам и пользователю.

    Args:
        session (AsyncSession): Сессия базы данных SQLAlchemy.
        payment_data (dict): Данные об оплате.
        currency (str): Валюта платежа.
        user_tg_id (int): ID пользователя в Telegram.
        bot (Bot): Экземпляр бота aiogram.

    Returns:
        None

    Raises:
        Exception: При возникновении ошибки при отправке уведомления администраторам.

    Example:
        # Пример использования функции
        >>> await successful_payment_logic(session, payment_data, currency, user_tg_id, bot)
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
        f'🎉 <b>Спасибо за покупку!</b>\\n\\n'
        f'🛒 <b>Информация о вашем товаре:</b>\\n'
        f'━━━━━━━━━━━━━━━━━━\\n'
        f'🔹 <b>Название:</b> <b>{product_data.name}</b>\\n'
        f'🔹 <b>Описание:</b>\\n<i>{product_data.description}</i>\\n'
        f'🔹 <b>Цена:</b> <b>{price} {currency}</b>\\n'
        f'🔹 <b>Закрытое описание:</b>\\n<i>{product_data.hidden_content}</i>\\n'
        f'━━━━━━━━━━━━━━━━━━\\n'
        f'{file_text}\\n\\n'
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