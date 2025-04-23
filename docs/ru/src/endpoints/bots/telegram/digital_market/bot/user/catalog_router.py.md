# Модуль `catalog_router` для обработки каталога товаров в Telegram боте

## Обзор

Модуль `catalog_router` предназначен для обработки запросов, связанных с каталогом товаров в Telegram-боте. Он предоставляет функциональность для отображения каталога, информации о товарах и организации процесса покупки с использованием различных платежных систем.

## Подробней

Модуль содержит обработчики callback-запросов для навигации по каталогу товаров, отображения информации о товарах и организации процесса покупки через различные платежные системы, такие как ЮKassa, Robocassa и Stars.
Он использует библиотеки aiogram для работы с Telegram API, sqlalchemy для взаимодействия с базой данных, а также собственные модули для формирования клавиатур, выполнения запросов к базе данных и обработки успешных платежей.

## Классы

В данном модуле нет классов.

## Функции

### `page_catalog`

```python
async def page_catalog(call: CallbackQuery, session_without_commit: AsyncSession):
    """Функция отображает каталог товаров.

    Args:
        call (CallbackQuery): Объект CallbackQuery, представляющий входящий callback-запрос от пользователя.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy для работы с базой данных без автоматической фиксации изменений.

    Returns:
        None

    Raises:
        Exception: Обрабатывается любое исключение, которое может возникнуть при удалении сообщения.

    Как работает функция:
    - Отвечает на callback-запрос, уведомляя пользователя о загрузке каталога.
    - Пытается удалить предыдущее сообщение с каталогом.
    - Извлекает данные о категориях товаров из базы данных с помощью `CategoryDao.find_all`.
    - Отправляет новое сообщение с категориями товаров, используя клавиатуру `catalog_kb`.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> call = AsyncMock(spec=CallbackQuery)
    >>> call.message.delete = AsyncMock()
    >>> session = AsyncMock(spec=AsyncSession)
    >>> await page_catalog(call, session)
    """
```

### `page_catalog_products`

```python
async def page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession):
    """Функция отображает товары выбранной категории.

    Args:
        call (CallbackQuery): Объект CallbackQuery, представляющий входящий callback-запрос от пользователя.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy для работы с базой данных без автоматической фиксации изменений.

    Returns:
        None

    Как работает функция:
    - Извлекает идентификатор категории из данных callback-запроса.
    - Получает список товаров, принадлежащих к данной категории, из базы данных с помощью `ProductDao.find_all`.
    - Если товары в категории найдены, отправляет информацию о каждом товаре, включая название, цену и описание, с использованием клавиатуры `product_kb`.
    - Если товары в категории не найдены, отправляет уведомление об отсутствии товаров.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> call = AsyncMock(spec=CallbackQuery)
    >>> call.data = "category_123"
    >>> call.answer = AsyncMock()
    >>> call.message.answer = AsyncMock()
    >>> session = AsyncMock(spec=AsyncSession)
    >>> await page_catalog_products(call, session)
    """
```

### `process_about`

```python
async def process_about(call: CallbackQuery, session_without_commit: AsyncSession):
    """Функция обрабатывает запрос на покупку товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery, представляющий входящий callback-запрос от пользователя.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy для работы с базой данных без автоматической фиксации изменений.

    Returns:
        None

    Как работает функция:
    - Извлекает информацию о пользователе из базы данных с помощью `UserDAO.find_one_or_none`.
    - Извлекает тип платежа, идентификатор товара и цену из данных callback-запроса.
    - В зависимости от типа платежа вызывает соответствующую функцию для отправки счета (ЮKassa, Stars или Robocassa).
    - Удаляет сообщение с кнопками выбора оплаты.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> call = AsyncMock(spec=CallbackQuery)
    >>> call.data = "buy_yukassa_456_789"
    >>> call.from_user.id = 123
    >>> call.message.delete = AsyncMock()
    >>> session = AsyncMock(spec=AsyncSession)
    >>> UserDAO.find_one_or_none = AsyncMock()
    >>> await process_about(call, session)
    """
```

### `send_yukassa_invoice`

```python
async def send_yukassa_invoice(call, user_info, product_id, price):
    """Функция отправляет счет на оплату через ЮKassa.

    Args:
        call (CallbackQuery): Объект CallbackQuery, представляющий входящий callback-запрос от пользователя.
        user_info: Информация о пользователе.
        product_id: Идентификатор товара.
        price: Цена товара.

    Returns:
        None

    Как работает функция:
    - Отправляет счет на оплату через Telegram API с использованием данных о товаре и пользователе.
    - Устанавливает payload для счета, содержащий информацию о типе платежа, идентификаторе пользователя и товара.
    - Использует `settings.PROVIDER_TOKEN` для указания провайдера платежа (ЮKassa).
    - Формирует список цен с указанием стоимости товара.
    - Использует клавиатуру `get_product_buy_youkassa` для отображения кнопок оплаты.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> call = AsyncMock(spec=CallbackQuery)
    >>> call.from_user.id = 123
    >>> bot.send_invoice = AsyncMock()
    >>> await send_yukassa_invoice(call, {"id": 1}, 456, 789)
    """
```

### `send_robocassa_invoice`

```python
async def send_robocassa_invoice(call, user_info, product_id, price, session: AsyncSession):
    """Функция отправляет счет на оплату через Robocassa.

    Args:
        call (CallbackQuery): Объект CallbackQuery, представляющий входящий callback-запрос от пользователя.
        user_info: Информация о пользователе.
        product_id: Идентификатор товара.
        price: Цена товара.
        session (AsyncSession): Асинхровая сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Как работает функция:
    - Получает следующий доступный идентификатор платежа из базы данных с помощью `PurchaseDao.get_next_id`.
    - Формирует описание платежа, содержащее информацию о пользователе и товаре.
    - Генерирует ссылку на оплату с использованием `generate_payment_link`.
    - Использует клавиатуру `get_product_buy_robocassa` для отображения кнопки оплаты со ссылкой на Robocassa.
    - Отправляет сообщение со ссылкой на оплату.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> call = AsyncMock(spec=CallbackQuery)
    >>> call.from_user.id = 123
    >>> call.message.answer = AsyncMock()
    >>> session = AsyncMock(spec=AsyncSession)
    >>> PurchaseDao.get_next_id = AsyncMock(return_value=1)
    >>> await send_robocassa_invoice(call, {"id": 1}, 456, 789, session)
    """
```

### `send_stars_invoice`

```python
async def send_stars_invoice(call, user_info, product_id, stars_price):
    """Функция отправляет счет на оплату через Stars.

    Args:
        call (CallbackQuery): Объект CallbackQuery, представляющий входящий callback-запрос от пользователя.
        user_info: Информация о пользователе.
        product_id: Идентификатор товара.
        stars_price: Цена товара в звездах.

    Returns:
        None

    Как работает функция:
    - Отправляет счет на оплату через Telegram API с использованием данных о товаре и пользователе.
    - Устанавливает payload для счета, содержащий информацию о типе платежа, идентификаторе пользователя и товара.
    - Устанавливает валюту `XTR` (звезды).
    - Формирует список цен с указанием стоимости товара в звездах.
    - Использует клавиатуру `get_product_buy_stars` для отображения кнопок оплаты.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> call = AsyncMock(spec=CallbackQuery)
    >>> call.from_user.id = 123
    >>> bot.send_invoice = AsyncMock()
    >>> await send_stars_invoice(call, {"id": 1}, 456, 789)
    """
```

### `pre_checkout_query`

```python
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    """Функция обрабатывает предварительный запрос перед подтверждением оплаты.

    Args:
        pre_checkout_q (PreCheckoutQuery): Объект PreCheckoutQuery, представляющий входящий запрос перед подтверждением оплаты.

    Returns:
        None

    Как работает функция:
    - Отвечает на предварительный запрос, подтверждая готовность к обработке оплаты.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> pre_checkout_q = AsyncMock(spec=PreCheckoutQuery)
    >>> pre_checkout_q.id = "123"
    >>> bot.answer_pre_checkout_query = AsyncMock()
    >>> await pre_checkout_query(pre_checkout_q)
    """
```

### `successful_payment`

```python
async def successful_payment(message: Message, session_with_commit: AsyncSession):
    """Функция обрабатывает успешную оплату.

    Args:
        message (Message): Объект Message, представляющий входящее сообщение об успешной оплате.
        session_with_commit (AsyncSession): Асинхровая сессия SQLAlchemy для работы с базой данных с автоматической фиксацией изменений.

    Returns:
        None

    Как работает функция:
    - Извлекает информацию о платеже из объекта `message.successful_payment`.
    - Извлекает тип платежа, идентификатор пользователя и товара из payload счета.
    - Определяет цену и валюту платежа.
    - Формирует словарь с данными о платеже.
    - Вызывает функцию `successful_payment_logic` для обработки логики успешной оплаты, такой как предоставление доступа к товару.

    Примеры:
    Пример вызова функции:
    >>> from unittest.mock import AsyncMock
    >>> message = AsyncMock(spec=Message)
    >>> message.successful_payment.invoice_payload = "stars_123_456"
    >>> message.successful_payment.total_amount = 789
    >>> message.from_user.id = 987
    >>> session = AsyncMock(spec=AsyncSession)
    >>> await successful_payment(message, session)
    """
```

## Параметры модуля

- `catalog_router`: Объект `Router` из библиотеки `aiogram`, используемый для регистрации обработчиков callback-запросов и сообщений, связанных с каталогом товаров.