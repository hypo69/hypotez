# Модуль для обработки успешной оплаты в Telegram боте цифрового рынка

## Обзор

Этот модуль содержит утилиты для обработки логики успешной оплаты в Telegram боте цифрового рынка. Он включает в себя функцию `successful_payment_logic`, которая выполняет ряд действий, связанных с завершением покупки товара пользователем, таких как добавление информации о покупке в базу данных, отправка уведомлений администраторам и предоставление информации о товаре пользователю.

## Подробней

Модуль обрабатывает информацию об успешной оплате, добавляет данные о покупке в базу данных, отправляет уведомления администраторам и предоставляет пользователю информацию о приобретенном товаре. Он тесно связан с модулями `aiogram`, `loguru`, `sqlalchemy`, `bot.config`, `bot.dao`, `bot.user.kbs` и `bot.user.schemas`, обеспечивая интеграцию с Telegram API, логированием, базой данных, конфигурацией, DAO (Data Access Objects), пользовательскими клавиатурами и схемами данных пользователя.

## Функции

### `successful_payment_logic`

```python
async def successful_payment_logic(session: AsyncSession, payment_data, currency, user_tg_id, bot: Bot):
    """
    Обрабатывает логику успешной оплаты товара пользователем.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        payment_data (dict): Словарь с данными об оплате, содержащий `product_id`, `price`, `payment_type`, `payment_id` и `user_id`.
        currency (str): Валюта, в которой была произведена оплата.
        user_tg_id (int): Telegram ID пользователя, совершившего покупку.
        bot (Bot): Объект бота aiogram для взаимодействия с Telegram API.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при отправке уведомления администраторам.

    
    - Извлекает `product_id`, `price`, `payment_type`, `payment_id` и `user_id` из `payment_data`.
    - Добавляет информацию о покупке в базу данных через `PurchaseDao.add`.
    - Получает данные о товаре из базы данных через `ProductDao.find_one_or_none_by_id`.
    - Отправляет уведомления администраторам о покупке товара пользователем.
    - Формирует текст сообщения с информацией о товаре для пользователя.
    - Отправляет пользователю сообщение с информацией о товаре и, если товар включает файл, отправляет файл.
    - Если тип оплаты - "stars", инициирует возврат звезд пользователю через `bot.refund_star_payment`.

    """
    product_id = int(payment_data.get("product_id"))
    price = payment_data.get("price")
    payment_type = payment_data.get("payment_type")
    payment_id = payment_data.get("payment_id")
    user_id = payment_data.get("user_id")
    await PurchaseDao.add(session=session, values=PaymentData(**payment_data))
    product_data = await ProductDao.find_one_or_none_by_id(session=session,
                                                           data_id=product_id)

    # Отправка уведомлений администраторам
    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f"💲 Пользователь c ID {user_id} купил товар <b>{product_data.name}</b> (ID: {product_id}) "
                    f"за <b>{price} {currency}</b>."
                )
            )
        except Exception as ex:
            logger.error(f"Ошибка при отправке уведомления администраторам: {ex}", ex, exc_info=True)

    # Отправка информации пользователю
    file_text = "📦 <b>Товар включает файл:</b>" if product_data.file_id else "📄 <b>Товар не включает файлы:</b>"
    product_text = (
        f"🎉 <b>Спасибо за покупку!</b>\\n\\n"
        f"🛒 <b>Информация о вашем товаре:</b>\\n"
        f"━━━━━━━━━━━━━━━━━━\\n"
        f"🔹 <b>Название:</b> <b>{product_data.name}</b>\\n"
        f"🔹 <b>Описание:</b>\\n<i>{product_data.description}</i>\\n"
        f"🔹 <b>Цена:</b> <b>{price} {currency}</b>\\n"
        f"🔹 <b>Закрытое описание:</b>\\n<i>{product_data.hidden_content}</i>\\n"
        f"━━━━━━━━━━━━━━━━━━\\n"
        f"{file_text}\\n\\n"
        f"ℹ️ <b>Информацию о всех ваших покупках вы можете найти в личном профиле.</b>"
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

```

**Параметры**:

- `session` (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
- `payment_data` (dict): Словарь с данными об оплате, содержащий `product_id`, `price`, `payment_type`, `payment_id` и `user_id`.
- `currency` (str): Валюта, в которой была произведена оплата.
- `user_tg_id` (int): Telegram ID пользователя, совершившего покупку.
- `bot` (Bot): Объект бота aiogram для взаимодействия с Telegram API.

**Примеры**:

```python
# Пример вызова функции successful_payment_logic
payment_data = {
    "product_id": "123",
    "price": "10.00",
    "payment_type": "card",
    "payment_id": "payment_123",
    "user_id": "user_123"
}
currency = "USD"
user_tg_id = 123456789
# await successful_payment_logic(session, payment_data, currency, user_tg_id, bot)
```

```python
# Пример вызова функции successful_payment_logic с оплатой звездами
payment_data = {
    "product_id": "456",
    "price": "5.00",
    "payment_type": "stars",
    "payment_id": "payment_456",
    "user_id": "user_456"
}
currency = "STARS"
user_tg_id = 987654321
# await successful_payment_logic(session, payment_data, currency, user_tg_id, bot)
```

**Внутренние функции**:
Внутри данной функции отсутствуют внутренние функции.