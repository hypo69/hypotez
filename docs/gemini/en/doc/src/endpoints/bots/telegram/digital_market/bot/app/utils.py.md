# Модуль утилит для работы с платежами в Telegram-боте

## Описание

Модуль содержит функции для генерации платежных ссылок через Robokassa, проверки подписи и обработки ответов от платежной системы.

## Содержание

1.  [Функция `calculate_signature`](#calculate_signature)
2.  [Функция `generate_payment_link`](#generate_payment_link)
3.  [Функция `parse_response`](#parse_response)
4.  [Функция `check_signature_result`](#check_signature_result)
5.  [Функция `result_payment`](#result_payment)
6.  [Функция `check_success_payment`](#check_success_payment)

## Функции

### `calculate_signature`

```python
def calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False):
    """Вычисляет подпись для запросов к Robokassa.

    Args:
        login (str): Логин мерчанта в Robokassa.
        cost (float): Сумма платежа.
        inv_id (int): Номер заказа.
        password (str): Пароль мерчанта.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_result (bool, optional): Флаг, указывающий, что подпись вычисляется для Result URL. По умолчанию `False`.

    Returns:
        str: MD5-хеш, представляющий подпись.
    """
```

### `generate_payment_link`

```python
def generate_payment_link(cost: float, number: int, description: str,
                          user_id: int, user_telegram_id: int, product_id: int,
                          is_test=1, robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx') -> str:
    """Генерирует ссылку для оплаты через Robokassa с обязательными параметрами.

    Args:
        cost (float): Стоимость товара.
        number (int): Номер заказа.
        description (str): Описание заказа.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_test (int, optional): Флаг тестового режима (1 - тест, 0 - боевой режим). По умолчанию 1.
        robokassa_payment_url (str, optional): URL для оплаты Robokassa.
            По умолчанию 'https://auth.robokassa.ru/Merchant/Index.aspx'.

    Returns:
        str: Ссылка на страницу оплаты.

    Пример:
        >>> generate_payment_link(100.0, 123, "Test order", 1, 123456789, 1)
        'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=<значение>&OutSum=100.0&InvId=123&Description=Test+order&SignatureValue=<значение>&IsTest=1&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1'
    """
```

### `parse_response`

```python
def parse_response(request: str) -> dict:
    """Разбирает строку запроса на параметры.

    Args:
        request (str): Строка запроса.

    Returns:
        dict: Словарь с параметрами.

    Пример:
        >>> parse_response('https://example.com/path?param1=value1&param2=value2')
        {'param1': 'value1', 'param2': 'value2'}
    """
```

### `check_signature_result`

```python
def check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id) -> bool:
    """Проверяет подпись результата оплаты.

    Args:
        out_sum (float): Сумма платежа.
        inv_id (int): Номер заказа.
        received_signature (str): Полученная подпись.
        password (str): Пароль мерчанта.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.

    Returns:
        bool: `True`, если подпись верна, иначе `False`.
    """
```

### `result_payment`

```python
def result_payment(request: str) -> str:
    """Обрабатывает результат оплаты (ResultURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

    Пример:
        Пример успешной оплаты:
        >>> result_payment('https://example.com/result?OutSum=100.0&InvId=123&SignatureValue=<значение>&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
        'OK123'

        Пример неуспешной оплаты (неверная подпись):
        >>> result_payment('https://example.com/result?OutSum=100.0&InvId=123&SignatureValue=wrong_signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
        'bad sign'
    """
```

### `check_success_payment`

```python
def check_success_payment(request: str) -> str:
    """Проверяет успешность оплаты (SuccessURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

    Пример:
        Пример успешной оплаты:
        >>> check_success_payment('https://example.com/success?OutSum=100.0&InvId=123&SignatureValue=<значение>&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
        'Thank you for using our service'

        Пример неуспешной оплаты (неверная подпись):
        >>> check_success_payment('https://example.com/success?OutSum=100.0&InvId=123&SignatureValue=wrong_signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
        'bad sign'
    """