## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода реализует набор функций для создания кнопок в боте Telegram. Функции генерируют различные виды клавиатур (inline и reply) с различными кнопками, которые отображаются пользователю в зависимости от контекста.

Шаги выполнения
-------------------------
1. **Создание InlineKeyboardBuilder**: Используется объект `InlineKeyboardBuilder` для создания inline-клавиатур.
2. **Добавление кнопок**: К каждой клавиатуре добавляются кнопки с текстом и callback-данными для обработки нажатий.
3. **Дополнительные функции**:  Для некоторых кнопок используются специальные функции: 
    - `generate_payment_link` для создания ссылки на платёжную систему
    - `settings.ADMIN_IDS` для проверки принадлежности пользователя к администраторам
    - `WebAppInfo` для добавления веб-приложения
4. **Форматирование**:  Функции `adjust(N)` и `as_markup()` форматируют клавиатуру и возвращают ее в виде `InlineKeyboardMarkup`.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.user.kbs import main_user_kb, catalog_kb, product_kb

# Отображение главной клавиатуры
kb = main_user_kb(user_id=12345)
await bot.send_message(chat_id=user_id, text="Добро пожаловать!", reply_markup=kb)

# Отображение клавиатуры с категориями
catalog_data = [
    Category(id=1, category_name="Одежда"),
    Category(id=2, category_name="Обувь"),
]
kb = catalog_kb(catalog_data=catalog_data)
await bot.send_message(chat_id=user_id, text="Выберите категорию", reply_markup=kb)

# Отображение клавиатуры для товара
kb = product_kb(product_id=123, price=1000, stars_price=500)
await bot.send_message(chat_id=user_id, text="Купить товар", reply_markup=kb)

# Отображение клавиатуры для оплаты ЮКасса
kb = get_product_buy_youkassa(price=1000)
await bot.send_message(chat_id=user_id, text="Оплатить ЮКасса", reply_markup=kb)

# Отображение клавиатуры для оплаты Robocassa
payment_link = generate_payment_link(product_id=123, price=1000)
kb = get_product_buy_robocassa(price=1000, payment_link=payment_link)
await bot.send_message(chat_id=user_id, text="Оплатить Robocassa", reply_markup=kb)

# Отображение клавиатуры для оплаты звездами
kb = get_product_buy_stars(price=500)
await bot.send_message(chat_id=user_id, text="Оплатить звездами", reply_markup=kb)
```

**Примечание:** 
- `user_id` - идентификатор пользователя в Telegram
- `bot` - объект бота Telegram
- `Category` - модель данных для категории товара
- `generate_payment_link` - функция для создания ссылки на платёжную систему Robocassa (настройка не показана в примере)
- Остальные функции используются для создания различных типов клавиатур, как описано в коде.