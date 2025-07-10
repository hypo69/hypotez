# Модуль для обработки успешной оплаты в боте Telegram

## Обзор

Модуль предоставляет функцию `successful_payment_logic` для обработки успешной оплаты в боте Telegram. 

## Детали

Функция `successful_payment_logic` вызывается после успешной оплаты пользователем товара в боте. 
Она получает информацию о платеже, данные пользователя и информацию о товаре, 
затем сохраняет информацию о покупке в базе данных и отправляет уведомления 
пользователю и администраторам бота.

## Функции

### `successful_payment_logic`

```python
async def successful_payment_logic(session: AsyncSession, payment_data, currency, user_tg_id, bot: Bot):
    """
    Функция обрабатывает успешную оплату товара пользователем.

    Args:
        session (AsyncSession): Сессия базы данных.
        payment_data (dict): Данные о платеже.
        currency (str): Валюта платежа.
        user_tg_id (int): Telegram ID пользователя.
        bot (Bot): Объект бота Telegram.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка во время обработки оплаты.
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
            logger.error(f"Ошибка при отправке уведомления администраторам: {ex}")

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

**Цель**: 
Функция обрабатывает успешную оплату товара пользователем, сохраняет информацию о покупке в базе данных и отправляет уведомления пользователю и администраторам бота.

**Входные параметры**:
- `session` (AsyncSession): Сессия базы данных.
- `payment_data` (dict): Данные о платеже.
- `currency` (str): Валюта платежа.
- `user_tg_id` (int): Telegram ID пользователя.
- `bot` (Bot): Объект бота Telegram.

**Возвратое значение**:
- `None`

**Возможные исключения**:
- `Exception`: Возникает в случае ошибки во время обработки оплаты.

**Пример**:
```python
# Пример вызова функции с данными о платеже
payment_data = {
    "product_id": 123,
    "price": 10.00,
    "payment_type": "stars",
    "payment_id": "1234567890",
    "user_id": 123456789
}

# Вызов функции с необходимыми параметрами
await successful_payment_logic(session=session, payment_data=payment_data, currency="USD", user_tg_id=123456789, bot=bot)
```
**Описание работы**:

- Функция извлекает информацию о товаре, ID пользователя, цену и тип оплаты из `payment_data`.
- Сохраняет информацию о покупке в базе данных с помощью `PurchaseDao.add`.
- Получает информацию о товаре из базы данных с помощью `ProductDao.find_one_or_none_by_id`.
- Отправляет уведомления администраторам о покупке с использованием `bot.send_message`.
- Отправляет информацию о товаре пользователю с использованием `bot.send_document` или `bot.send_message` в зависимости от наличия файла.
- Возвращает звезды за покупку, если тип оплаты - "stars".

## Внутренние функции
 
**Нет.**

## Параметры
 
- `session` (AsyncSession): Сессия базы данных.
- `payment_data` (dict): Данные о платеже.
- `currency` (str): Валюта платежа.
- `user_tg_id` (int): Telegram ID пользователя.
- `bot` (Bot): Объект бота Telegram.

## Примеры
 
- Пример вызова функции с данными о платеже
```python
# Пример вызова функции с данными о платеже
payment_data = {
    "product_id": 123,
    "price": 10.00,
    "payment_type": "stars",
    "payment_id": "1234567890",
    "user_id": 123456789
}

# Вызов функции с необходимыми параметрами
await successful_payment_logic(session=session, payment_data=payment_data, currency="USD", user_tg_id=123456789, bot=bot)