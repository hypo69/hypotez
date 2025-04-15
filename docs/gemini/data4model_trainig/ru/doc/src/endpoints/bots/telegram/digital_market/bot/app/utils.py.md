# Модуль утилит для работы с Robokassa в Telegram боте

## Обзор

Модуль содержит функции для генерации платежных ссылок Robokassa, проверки подписи и обработки ответов от Robokassa. Этот модуль используется для интеграции с платежной системой Robokassa в Telegram боте, обеспечивая возможность приема платежей от пользователей.

## Подробнее

Этот модуль предоставляет функции для создания платежных ссылок, проверки корректности подписи в ответах от Robokassa и обработки результатов оплаты. Он включает функции для генерации подписи, создания платежной ссылки, разбора ответа от Robokassa, проверки подписи результата и проверки успешности оплаты.

## Функции

### `calculate_signature`

```python
def calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False):
    """
    Вычисляет подпись для формирования запросов к Robokassa и для проверки ответов от неё.

    Args:
        login (str): Логин магазина в Robokassa.
        cost (float): Сумма платежа.
        inv_id (int): Номер заказа.
        password (str): Пароль магазина в Robokassa.
        user_id (int): ID пользователя в системе.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID продукта.
        is_result (bool): Флаг, указывающий, что подпись вычисляется для Result URL. По умолчанию `False`.

    Returns:
        str: Вычисленная MD5-подпись в шестнадцатеричном формате.

    Как работает функция:
    - Функция принимает параметры, необходимые для вычисления подписи.
    - В зависимости от значения флага `is_result` формируется базовая строка для вычисления подписи.
    - Дополнительные параметры (ID пользователя, Telegram ID пользователя и ID продукта) добавляются к базовой строке.
    - Вычисляется MD5-хеш от полученной строки и возвращается в шестнадцатеричном формате.
    """
    ...
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
        is_test (int): Флаг тестового режима (1 - тест, 0 - боевой режим).
        robokassa_payment_url (str): URL для оплаты Robokassa. По умолчанию 'https://auth.robokassa.ru/Merchant/Index.aspx'.

    Returns:
        str: Ссылка на страницу оплаты.

    Как работает функция:
    - Функция принимает параметры, необходимые для формирования платежной ссылки.
    - Вызывает функцию `calculate_signature` для вычисления подписи.
    - Формирует словарь с данными для запроса к Robokassa.
    - Кодирует параметры в URL-строку и возвращает полную ссылку для оплаты.
    """
    ...
```

**Примеры**:

```python
cost = 100.0
number = 12345
description = 'Test Order'
user_id = 1
user_telegram_id = 123456789
product_id = 10
payment_link = generate_payment_link(cost, number, description, user_id, user_telegram_id, product_id)
print(payment_link)
# Output: https://auth.robokassa.ru/Merchant/Index.aspx?...
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
    - Функция принимает строку запроса.
    - Извлекает параметры из URL-строки.
    - Преобразует параметры в словарь и возвращает его.
    """
    ...
```

**Примеры**:

```python
request = 'https://example.com/result?OutSum=100&InvId=12345&SignatureValue=test_signature'
params = parse_response(request)
print(params)
# Output: {'OutSum': '100', 'InvId': '12345', 'SignatureValue': 'test_signature'}
```

### `check_signature_result`

```python
def check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id) -> bool:
    """
    Проверяет подпись результата оплаты.

    Args:
        out_sum (float): Сумма платежа.
        inv_id (int): Номер заказа.
        received_signature (str): Полученная подпись.
        password (str): Пароль магазина в Robokassa.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.

    Returns:
        bool: `True`, если подпись верна, иначе `False`.

    Как работает функция:
    - Функция принимает параметры, необходимые для проверки подписи.
    - Вызывает функцию `calculate_signature` для вычисления подписи на основе переданных параметров и флага `is_result=True`.
    - Сравнивает вычисленную подпись с полученной подписью.
    - Возвращает `True`, если подписи совпадают, иначе `False`.
    """
    ...
```

**Примеры**:

```python
out_sum = 100.0
inv_id = 12345
received_signature = 'test_signature'
password = 'test_password'
user_id = 1
user_telegram_id = 123456789
product_id = 10
is_valid = check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id)
print(is_valid)
# Output: False
```

### `result_payment`

```python
def result_payment(request: str) -> str:
    """
    Обрабатывает результат оплаты (ResultURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

    Как работает функция:
    - Функция принимает строку запроса с параметрами оплаты.
    - Разбирает строку запроса на параметры с помощью функции `parse_response`.
    - Извлекает необходимые параметры из словаря.
    - Проверяет подпись с помощью функции `check_signature_result` и пароля `settings.MRH_PASS_2`.
    - Возвращает 'OK' + номер заказа, если подпись верна, иначе возвращает "bad sign".
    """
    ...
```

**Примеры**:

```python
request = 'https://example.com/result?OutSum=100&InvId=12345&SignatureValue=test_signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=10'
result = result_payment(request)
print(result)
# Output: 'bad sign'
```

### `check_success_payment`

```python
def check_success_payment(request: str) -> str:
    """
    Проверяет успешность оплаты (SuccessURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

    Как работает функция:
    - Функция принимает строку запроса с параметрами оплаты.
    - Разбирает строку запроса на параметры с помощью функции `parse_response`.
    - Извлекает необходимые параметры из словаря.
    - Проверяет подпись с помощью функции `check_signature_result` и пароля `settings.MRH_PASS_1`.
    - Возвращает сообщение об успешной оплате, если подпись верна, иначе возвращает "bad sign".
    """
    ...
```

**Примеры**:

```python
request = 'https://example.com/success?OutSum=100&InvId=12345&SignatureValue=test_signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=10'
result = check_success_payment(request)
print(result)
# Output: 'bad sign'