# Модуль маршрутизации каталога для Telegram-бота

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.user.catalog_router` содержит маршрутизаторы для обработки запросов, связанных с каталогом товаров в Telegram-боте.

## Подробней

Модуль предоставляет функции для отображения каталога товаров, обработки выбора категорий и организации процесса оплаты товаров через различные платежные системы.

## Функции

### `page_catalog`

```python
@catalog_router.callback_query(F.data == "catalog")
async def page_catalog(call: CallbackQuery, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает нажатие кнопки "catalog" для отображения каталога товаров.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Отправляет уведомление о загрузке каталога.
2.  Удаляет предыдущее сообщение (если возможно).
3.  Извлекает данные каталога из базы данных, используя `CategoryDao.find_all`.
4.  Отправляет пользователю сообщение с клавиатурой, содержащей категории товаров.

### `page_catalog_products`

```python
@catalog_router.callback_query(F.data.startswith("category_"))
async def page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает нажатие кнопки категории для отображения списка товаров в выбранной категории.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Извлекает ID категории из данных обратного вызова.
2.  Извлекает список товаров для выбранной категории из базы данных, используя `ProductDao.find_all`.
3.  Отправляет пользователю сообщение со списком товаров и информацией о каждом товаре.

### `process_about`

```python
@catalog_router.callback_query(F.data.startswith('buy_'))
async def process_about(call: CallbackQuery, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает нажатие кнопки "buy" для организации процесса оплаты товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Извлекает тип платежа и ID товара из данных обратного вызова.
2.  В зависимости от типа платежа вызывает соответствующую функцию для организации оплаты (`send_yukassa_invoice`, `send_stars_invoice` или `send_robocassa_invoice`).
3.  Удаляет предыдущее сообщение.

### `send_yukassa_invoice`

```python
async def send_yukassa_invoice(call: CallbackQuery, user_info, product_id, price):
```

**Назначение**: Отправляет счет для оплаты через ЮKassa.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `user_info`: Информация о пользователе.
*   `product_id` (int): ID товара.
*   `price` (int): Цена товара.

**Как работает функция**:

1.  Формирует счет для оплаты с использованием `bot.send_invoice`.
2.  Добавляет кнопку для оплаты через ЮKassa.

### `send_robocassa_invoice`

```python
async def send_robocassa_invoice(call: CallbackQuery, user_info, product_id, price, session: AsyncSession):
```

**Назначение**: Отправляет ссылку для оплаты через Robokassa.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `user_info`: Информация о пользователе.
*   `product_id` (int): ID товара.
*   `price` (int): Цена товара.
*   `session` (AsyncSession): Асинхронная сессия базы данных.

**Как работает функция**:

1.  Получает следующий свободный ID для записи в базе данных, используя `PurchaseDao.get_next_id`.
2.  Формирует ссылку для оплаты, используя функцию `generate_payment_link`.
3.  Добавляет кнопку для оплаты через Robokassa.
4.  Отправляет ссылку пользователю.

### `send_stars_invoice`

```python
async def send_stars_invoice(call: CallbackQuery, user_info, product_id, stars_price):
```

**Назначение**: Отправляет счет для оплаты через Telegram Stars.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `user_info`: Информация о пользователе.
*   `product_id` (int): ID товара.
*   `stars_price` (int): Цена товара в звездах.

**Как работает функция**:

1.  Формирует счет для оплаты с использованием `bot.send_invoice`.
2.  Добавляет кнопку для оплаты через Telegram Stars.

### `pre_checkout_query`

```python
@catalog_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
```

**Назначение**: Обрабатывает запрос перед подтверждением оплаты.

**Параметры**:

*   `pre_checkout_q` (PreCheckoutQuery): Объект запроса перед подтверждением оплаты.

**Как работает функция**:

1.  Подтверждает запрос, используя `bot.answer_pre_checkout_query`.

### `successful_payment`

```python
@catalog_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, session_with_commit: AsyncSession):
```

**Назначение**: Обрабатывает успешное завершение оплаты.

**Параметры**:

*   `message` (Message): Объект сообщения.
*   `session_with_commit` (AsyncSession): Асинхронная сессия базы данных с коммитом.

**Как работает функция**:

1.  Извлекает информацию о платеже из объекта сообщения.
2.  Извлекает ID пользователя и товара из полезной нагрузки (payload).
3.  В зависимости от типа платежа (ЮKassa или Telegram Stars) формирует словарь с данными о платеже.
4.  Вызывает функцию `successful_payment_logic` для обработки данных платежа и обновления информации в базе данных.