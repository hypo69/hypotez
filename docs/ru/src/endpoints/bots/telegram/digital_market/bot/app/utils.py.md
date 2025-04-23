# Модуль `utils.py` для работы с платежами в Telegram-боте

## Обзор

Модуль содержит функции для генерации платежных ссылок Robokassa, проверки статуса платежей и разбора ответов от платежной системы. Он используется в Telegram-боте для организации приема платежей от пользователей.

## Подробней

Модуль предназначен для интеграции с платежной системой Robokassa. Он содержит функции для формирования подписи запросов, создания платежных ссылок и проверки подлинности ответов от Robokassa. Использование этого модуля позволяет безопасно и надежно принимать платежи от пользователей Telegram-бота.

## Функции

### `calculate_signature`

```python
def calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False):
    """
    Вычисляет подпись для запроса к Robokassa.

    Args:
        login (str): Логин мерчанта в Robokassa.
        cost (float): Сумма платежа.
        inv_id (int): Номер заказа.
        password (str): Пароль мерчанта в Robokassa.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_result (bool, optional): Флаг, указывающий, что подпись вычисляется для Result URL. По умолчанию `False`.

    Returns:
        str: MD5-хеш, представляющий подпись запроса.

    Как работает функция:
    - Определяет строку для вычисления подписи в зависимости от флага `is_result`. Если `is_result` равен `True`, используется формат строки для Result URL, иначе - для initial и Success URL.
    - Создает словарь `additional_params`, содержащий дополнительные параметры запроса: `user_id`, `user_telegram_id` и `product_id`.
    - Сортирует элементы словаря `additional_params` по ключам и добавляет их в строку для вычисления подписи.
    - Вычисляет MD5-хеш от полученной строки в кодировке UTF-8 и возвращает его в шестнадцатеричном формате.

    """
```

### `generate_payment_link`

```python
def generate_payment_link(cost: float, number: int, description: str,
                          user_id: int, user_telegram_id: int, product_id: int,
                          is_test=1, robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx') -> str:
    """
    Генерирует ссылку для оплаты через Robokassa с обязательными параметрами.

    Args:
        cost (float): Стоимость товара.
        number (int): Номер заказа.
        description (str): Описание заказа.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_test (int, optional): Флаг тестового режима (1 - тест, 0 - боевой режим). По умолчанию 1.
        robokassa_payment_url (str, optional): URL для оплаты Robokassa. По умолчанию 'https://auth.robokassa.ru/Merchant/Index.aspx'.

    Returns:
        str: Ссылка на страницу оплаты.

    Как работает функция:
    - Вызывает функцию `calculate_signature` для вычисления подписи запроса.
    - Формирует словарь `data`, содержащий параметры запроса для Robokassa, включая логин мерчанта, сумму платежа, номер заказа, описание заказа, подпись, флаг тестового режима и дополнительные параметры.
    - Кодирует словарь `data` в строку запроса с помощью `parse.urlencode`.
    - Формирует URL для оплаты, объединяя `robokassa_payment_url` и строку запроса.
    - Возвращает полученный URL.

    """
```

### `parse_response`

```python
def parse_response(request: str) -> dict:
    """
    Разбирает строку запроса на параметры.

    Args:
        request (str): Строка запроса.

    Returns:
        dict: Словарь с параметрами.

    Как работает функция:
    - Извлекает строку запроса из URL, используя `urlparse(request).query`.
    - Разбирает строку запроса на параметры с помощью `parse.parse_qsl` и преобразует результат в словарь.
    - Возвращает полученный словарь с параметрами.

    """
```

### `check_signature_result`

```python
def check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id) -> bool:
    """
    Проверяет подпись ответа от Robokassa (ResultURL).

    Args:
        out_sum (float): Сумма платежа.
        inv_id (int): Номер заказа.
        received_signature (str): Подпись, полученная от Robokassa.
        password (str): Пароль мерчанта в Robokassa.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.

    Returns:
        bool: `True`, если подпись верна, `False` в противном случае.

    Как работает функция:
    - Вызывает функцию `calculate_signature` для вычисления подписи на основе параметров ответа.
    - Сравнивает вычисленную подпись с подписью, полученной от Robokassa, приводя обе подписи к нижнему регистру.
    - Возвращает `True`, если подписи совпадают, `False` в противном случае.

    """
```

### `result_payment`

```python
def result_payment(request: str) -> str:
    """
    Обрабатывает результат оплаты (ResultURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: `'OK' + номер заказа`, если оплата прошла успешно, иначе `'bad sign'`.

    Как работает функция:
    - Разбирает строку запроса на параметры с помощью функции `parse_response`.
    - Извлекает значения параметров: `out_sum`, `inv_id`, `signature`, `user_id`, `user_telegram_id` и `product_id`.
    - Вызывает функцию `check_signature_result` для проверки подписи ответа.
    - Если подпись верна, возвращает строку `'OK' + inv_id`, иначе возвращает строку `'bad sign'`.

    """
```

### `check_success_payment`

```python
def check_success_payment(request: str) -> str:
    """
    Проверяет успешность оплаты (SuccessURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: Сообщение об успешной оплате или `'bad sign'` при неверной подписи.

    Как работает функция:
    - Разбирает строку запроса на параметры с помощью функции `parse_response`.
    - Извлекает значения параметров: `out_sum`, `inv_id`, `signature`, `user_id`, `user_telegram_id` и `product_id`.
    - Вызывает функцию `check_signature_result` для проверки подписи ответа.
    - Если подпись верна, возвращает сообщение `'Thank you for using our service'`, иначе возвращает строку `'bad sign'`.

    """