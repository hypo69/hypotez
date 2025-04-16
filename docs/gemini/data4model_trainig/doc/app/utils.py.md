# Модуль утилит для обработки платежей Robokassa

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.app.utils` предоставляет набор утилитных функций для работы с платежами через Robokassa.

## Подробней

Модуль содержит функции для генерации ссылок для оплаты, проверки подписи Robokassa и обработки результатов оплаты.

## Функции

### `calculate_signature`

```python
def calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False):
```

**Назначение**: Вычисляет подпись для Robokassa.

**Параметры**:

*   `login` (str): Логин магазина в Robokassa.
*   `cost` (float): Стоимость товара.
*   `inv_id` (int): Номер заказа.
*   `password` (str): Пароль магазина в Robokassa.
*   `user_id` (int): ID пользователя.
*   `user_telegram_id` (int): Telegram ID пользователя.
*   `product_id` (int): ID товара.
*   `is_result` (bool, optional): Флаг, указывающий на Result URL (по умолчанию `False`).

**Возвращает**:

*   `str`: Вычисленная подпись в виде MD5-хеша.

**Как работает функция**:

1.  Формирует строку для хеширования в зависимости от значения `is_result`.
2.  Добавляет дополнительные параметры (user\_id, user\_telegram\_id, product\_id) в строку.
3.  Вычисляет MD5-хеш от строки в кодировке UTF-8.
4.  Возвращает хеш в шестнадцатеричном формате.

### `generate_payment_link`

```python
def generate_payment_link(cost: float, number: int, description: str,
                          user_id: int, user_telegram_id: int, product_id: int,
                          is_test=1, robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx') -> str:
```

**Назначение**: Генерирует ссылку для оплаты через Robokassa с обязательными параметрами.

**Параметры**:

*   `cost` (float): Стоимость товара.
*   `number` (int): Номер заказа.
*   `description` (str): Описание заказа.
*   `user_id` (int): ID пользователя.
*   `user_telegram_id` (int): Telegram ID пользователя.
*   `product_id` (int): ID товара.
*   `is_test` (int, optional): Флаг тестового режима (1 - тест, 0 - боевой режим) (по умолчанию 1).
*   `robokassa_payment_url` (str, optional): URL для оплаты Robokassa (по умолчанию `'https://auth.robokassa.ru/Merchant/Index.aspx'`).

**Возвращает**:

*   `str`: Ссылка на страницу оплаты.

**Как работает функция**:

1.  Вычисляет подпись, используя функцию `calculate_signature`.
2.  Формирует словарь с параметрами для отправки в Robokassa.
3.  Кодирует параметры в URL-строку с использованием `urllib.parse.urlencode`.
4.  Возвращает URL-адрес с параметрами.

### `parse_response`

```python
def parse_response(request: str) -> dict:
```

**Назначение**: Разбирает строку запроса на параметры.

**Параметры**:

*   `request` (str): Строка запроса.

**Возвращает**:

*   `dict`: Словарь с параметрами.

**Как работает функция**:

1.  Использует `urllib.parse.urlparse` для разбора URL.
2.  Использует `urllib.parse.parse_qsl` для разбора параметров запроса.
3.  Возвращает словарь с параметрами.

### `check_signature_result`

```python
def check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id) -> bool:
```

**Назначение**: Проверяет подпись Robokassa для ResultURL.

**Параметры**:

*   `out_sum` (str): Сумма платежа.
*   `inv_id` (str): ID заказа.
*   `received_signature` (str): Полученная подпись.
*   `password` (str): Пароль 2 из настроек Робокассы.
*   `user_id` (int): ID пользователя.
*   `user_telegram_id` (int): Telegram ID пользователя.
*   `product_id` (int): ID товара.

**Возвращает**:

*   `bool`: `True`, если подпись верна, `False` в противном случае.

**Как работает функция**:

1.  Вычисляет подпись, используя функцию `calculate_signature` и флаг `is_result=True`.
2.  Сравнивает вычисленную подпись с полученной подписью (без учета регистра).
3.  Возвращает результат сравнения.

### `result_payment`

```python
def result_payment(request: str) -> str:
```

**Назначение**: Обрабатывает результат оплаты (ResultURL).

**Параметры**:

*   `request` (str): Строка запроса с параметрами оплаты.

**Возвращает**:

*   `str`: `"OK{номер заказа}"`, если оплата прошла успешно, иначе `"bad sign"`.

**Как работает функция**:

1.  Разбирает строку запроса на параметры, используя функцию `parse_response`.
2.  Извлекает параметры оплаты из словаря.
3.  Проверяет подпись, используя функцию `check_signature_result`.
4.  Возвращает `"OK{номер заказа}"`, если подпись верна, иначе `"bad sign"`.

### `check_success_payment`

```python
def check_success_payment(request: str) -> str:
```

**Назначение**: Проверяет успешность оплаты (SuccessURL).

**Параметры**:

*   `request` (str): Строка запроса с параметрами оплаты.

**Возвращает**:

*   `str`: Сообщение об успешной оплате или `"bad sign"`, если подпись неверна.

**Как работает функция**:

1.  Разбирает строку запроса на параметры, используя функцию `parse_response`.
2.  Извлекает параметры оплаты из словаря.
3.  Проверяет подпись, используя функцию `check_signature_result`.
4.  Возвращает сообщение об успешной оплате, если подпись верна, иначе `"bad sign"`.