# Модуль `utils.py` для работы с платежами через Robokassa в Telegram-боте

## Обзор

Модуль содержит утилиты для генерации платежных ссылок Robokassa, проверки подписи и обработки ответов от Robokassa. Он используется для обеспечения безопасного и надежного приема платежей в Telegram-боте цифрового рынка.

## Подробней

Этот модуль предоставляет функции для работы с платежной системой Robokassa, включая генерацию подписи для платежей, создание платежных ссылок, разбор ответов от Robokassa и проверку подлинности этих ответов. Функции модуля обеспечивают безопасное взаимодействие с Robokassa и позволяют корректно обрабатывать результаты платежей.

## Функции

### `calculate_signature`

```python
def calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False):
    """
    Вычисляет подпись для запросов к Robokassa.

    Args:
        login (str): Логин мерчанта в Robokassa.
        cost (float): Сумма платежа.
        inv_id (int): Номер заказа.
        password (str): Пароль мерчанта в Robokassa.
        user_id (int): ID пользователя в системе.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_result (bool): Флаг, указывающий, что подпись вычисляется для Result URL. По умолчанию `False`.

    Returns:
        str: Вычисленная подпись в формате MD5 hash.

    Как работает функция:
    - Определяет строку для вычисления подписи в зависимости от значения `is_result`.
    - Добавляет дополнительные параметры (ID пользователя, Telegram ID пользователя и ID продукта) к строке для вычисления подписи.
    - Вычисляет MD5 hash от полученной строки и возвращает его в шестнадцатеричном формате.
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
        is_test (int): Флаг тестового режима (1 - тест, 0 - боевой режим). По умолчанию `1`.
        robokassa_payment_url (str): URL для оплаты Robokassa. По умолчанию 'https://auth.robokassa.ru/Merchant/Index.aspx'.

    Returns:
        str: Ссылка на страницу оплаты.

    Как работает функция:
    - Вычисляет подпись с использованием функции `calculate_signature`.
    - Формирует словарь с данными для запроса к Robokassa, включая логин мерчанта, сумму, номер заказа, описание, подпись, флаг тестового режима и дополнительные параметры.
    - Кодирует параметры в URL-строку и объединяет её с базовым URL Robokassa.
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
    - Извлекает параметры из URL запроса с использованием `urllib.parse.urlparse` и `urllib.parse.parse_qsl`.
    - Преобразует список пар ключ-значение в словарь и возвращает его.
    """
```

### `check_signature_result`

```python
def check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id) -> bool:
    """
    Проверяет подпись для Result URL.

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

    Как работает функция:
    - Вычисляет подпись с использованием функции `calculate_signature` и флага `is_result=True`.
    - Сравнивает вычисленную подпись с полученной подписью (без учета регистра) и возвращает результат сравнения.
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
        str: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

    Как работает функция:
    - Извлекает параметры из запроса с использованием функции `parse_response`.
    - Извлекает сумму, номер заказа, подпись и ID пользователя/товара из параметров.
    - Проверяет подпись с использованием функции `check_signature_result` и пароля `settings.MRH_PASS_2`.
    - Возвращает 'OK' + номер заказа, если подпись верна, иначе возвращает "bad sign".
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
        str: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

    Как работает функция:
    - Извлекает параметры из запроса с использованием функции `parse_response`.
    - Извлекает сумму, номер заказа, подпись и ID пользователя/товара из параметров.
    - Проверяет подпись с использованием функции `check_signature_result` и пароля `settings.MRH_PASS_1`.
    - Возвращает сообщение об успешной оплате, если подпись верна, иначе возвращает "bad sign".
    """