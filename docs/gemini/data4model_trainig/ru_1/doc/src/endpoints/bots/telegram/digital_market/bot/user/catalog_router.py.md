# Модуль маршрутизации каталога для Telegram-бота цифрового магазина
==================================================================

Модуль содержит маршрутизаторы и обработчики callback-запросов, связанных с каталогом товаров в Telegram-боте цифрового магазина.
Он обрабатывает запросы на отображение каталога, списка товаров в категории и инициирует процесс покупки товара через различные платежные системы.

## Обзор

Этот модуль является частью Telegram-бота цифрового магазина и отвечает за обработку запросов, связанных с каталогом товаров.
Он использует библиотеку `aiogram` для создания обработчиков callback-запросов, которые позволяют пользователям взаимодействовать с каталогом товаров через интерфейс бота.
Модуль взаимодействует с базой данных через DAO (Data Access Object) для получения информации о категориях и товарах.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `page_catalog`

```python
async def page_catalog(call: CallbackQuery, session_without_commit: AsyncSession):
    """
    Обработчик callback-запроса на отображение каталога.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при удалении предыдущего сообщения.

    Как работает функция:
    - Отвечает на callback-запрос сообщением "Загрузка каталога...".
    - Пытается удалить предыдущее сообщение с каталогом, если оно есть.
    - Получает из базы данных список всех категорий товаров.
    - Отправляет пользователю сообщение с категориями товаров, используя клавиатуру `catalog_kb` для навигации.

    Примеры:
    >>> from aiogram.types import CallbackQuery
    >>> from sqlalchemy.ext.asyncio import AsyncSession
    >>> # Создаем мок-объект CallbackQuery и AsyncSession
    >>> class MockCallbackQuery:
    ...     async def answer(self, text):
    ...         print(f"Answer: {text}")
    ...     async def message(self):
    ...         return MockMessage()
    >>> class MockMessage:
    ...     async def delete(self):
    ...         print("Message deleted")
    ...     async def answer(self, text, reply_markup):
    ...         print(f"Answer: {text}")

    >>> async def mock_find_all(session):
    ...    return []

    >>> class MockAsyncSession:
    ...     async def __aenter__(self):
    ...         return self
    ...     async def __aexit__(self, exc_type, exc_val, exc_tb):
    ...         pass
    >>> call = MockCallbackQuery()
    >>> session = MockAsyncSession()
    >>> await page_catalog(call, session)
    Answer: Загрузка каталога...
    Message deleted
    Answer: Выберите категорию товаров:
    """
    ...
```

### `page_catalog_products`

```python
async def page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession):
    """
    Обработчик callback-запроса на отображение товаров в выбранной категории.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Как работает функция:
    - Извлекает идентификатор категории из данных callback-запроса.
    - Получает из базы данных список товаров, относящихся к выбранной категории.
    - Если товары в категории есть:
        - Отвечает на callback-запрос сообщением о количестве товаров в категории.
        - Для каждого товара формирует текстовое описание, включающее название, цену и описание товара.
        - Отправляет пользователю сообщение с описанием товара и клавиатурой `product_kb` для покупки товара.
    - Если товаров в категории нет:
        - Отвечает на callback-запрос сообщением об отсутствии товаров в категории.
    """
    ...
```

### `process_about`

```python
async def process_about(call: CallbackQuery, session_without_commit: AsyncSession):
    """
    Обработчик callback-запроса на покупку товара.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Как работает функция:
    - Получает информацию о пользователе из базы данных.
    - Извлекает тип платежа, идентификатор товара и цену из данных callback-запроса.
    - В зависимости от типа платежа вызывает соответствующую функцию для отправки счета:
        - `yukassa` - `send_yukassa_invoice`
        - `stars` - `send_stars_invoice`
        - `robocassa` - `send_robocassa_invoice`
    - Удаляет предыдущее сообщение с товаром.

    """
    ...
```

### `send_yukassa_invoice`

```python
async def send_yukassa_invoice(call, user_info, product_id, price):
    """
    Отправляет пользователю счет на оплату через ЮKassa.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        user_info (User): Объект пользователя из базы данных.
        product_id (int): Идентификатор товара.
        price (float): Цена товара.

    Returns:
        None

    Как работает функция:
    - Отправляет пользователю счет на оплату через ЮKassa, используя метод `send_invoice` объекта `bot`.
    - Формирует заголовок и описание счета.
    - Устанавливает `payload` для счета, содержащий информацию о типе платежа, идентификаторе пользователя и идентификаторе товара.
    - Устанавливает `provider_token` для ЮKassa.
    - Устанавливает валюту счета в рубли.
    - Устанавливает цену товара в счете.
    - Устанавливает клавиатуру `get_product_buy_youkassa` для оплаты товара.
    """
    ...
```

### `send_robocassa_invoice`

```python
async def send_robocassa_invoice(call, user_info, product_id, price, session: AsyncSession):
    """
    Отправляет пользователю ссылку на оплату через Robokassa.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        user_info (User): Объект пользователя из базы данных.
        product_id (int): Идентификатор товара.
        price (float): Цена товара.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Returns:
        None

    Как работает функция:
    - Получает следующий идентификатор платежа из базы данных.
    - Формирует описание платежа.
    - Генерирует ссылку на оплату через Robokassa, используя функцию `generate_payment_link`.
    - Устанавливает параметры платежа, такие как цена, идентификатор платежа, описание, идентификатор пользователя и идентификатор товара.
    - Отправляет пользователю сообщение со ссылкой на оплату и клавиатурой `get_product_buy_robocassa`.
    """
    ...
```

### `send_stars_invoice`

```python
async def send_stars_invoice(call, user_info, product_id, stars_price):
    """
    Отправляет пользователю счет на оплату звездами.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        user_info (User): Объект пользователя из базы данных.
        product_id (int): Идентификатор товара.
        stars_price (int): Цена товара в звездах.

    Returns:
        None

    Как работает функция:
    - Отправляет пользователю счет на оплату звездами, используя метод `send_invoice` объекта `bot`.
    - Формирует заголовок и описание счета.
    - Устанавливает `payload` для счета, содержащий информацию о типе платежа, идентификаторе пользователя и идентификаторе товара.
    - Устанавливает валюту счета в звездах (XTR).
    - Устанавливает цену товара в счете.
    - Устанавливает клавиатуру `get_product_buy_stars` для оплаты товара.
    """
    ...
```

### `pre_checkout_query`

```python
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    """
    Обработчик pre-checkout запроса.

    Args:
        pre_checkout_q (PreCheckoutQuery): Объект pre-checkout запроса.

    Returns:
        None

    Как работает функция:
    - Подтверждает pre-checkout запрос, используя метод `answer_pre_checkout_query` объекта `bot`.
    """
    ...
```

### `successful_payment`

```python
async def successful_payment(message: Message, session_with_commit: AsyncSession):
    """
    Обработчик успешной оплаты.

    Args:
        message (Message): Объект сообщения от пользователя.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных с возможностью коммита.

    Returns:
        None

    Как работает функция:
    - Получает информацию об оплате из сообщения.
    - Извлекает тип платежа, идентификатор пользователя и идентификатор товара из `payload` счета.
    - Определяет цену и валюту в зависимости от типа платежа.
    - Формирует словарь с данными об оплате.
    - Вызывает функцию `successful_payment_logic` для обработки успешной оплаты.
    """
    ...