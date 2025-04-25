# Модуль `utils.py` 
## Обзор

Модуль `utils.py` предоставляет вспомогательные функции для работы с платежами через Robokassa в боте Telegram. 
Он включает в себя функции для генерации платежных ссылок, проверки подписи платежей, обработки результатов оплаты
и проверки успешности оплаты.

## Подробности

Модуль `utils.py`  предназначен для взаимодействия с сервисом онлайн-платежей Robokassa.
Он позволяет генерировать платежные ссылки с необходимыми параметрами,
проверять подписи платежей для обеспечения безопасности,
обрабатывать результаты оплаты и  проверять успешность платежа.

## Функции

### `calculate_signature`

**Назначение**: 
Функция `calculate_signature` вычисляет хеш-подпись для платежа, используя 
MD5-алгоритм. Подпись используется для проверки подлинности платежа
и предотвращения подделок.

**Параметры**:

- `login` (str): Логин мерчанта в Robokassa.
- `cost` (float): Стоимость товара.
- `inv_id` (int): Номер заказа.
- `password` (str): Пароль мерчанта в Robokassa (MRH_PASS_1 или MRH_PASS_2 в зависимости от типа ссылки).
- `user_id` (int): ID пользователя.
- `user_telegram_id` (int): Telegram ID пользователя.
- `product_id` (int): ID товара.
- `is_result` (bool): Флаг, указывающий, 
  является ли ссылка Result URL (True) или Initial/Success URL (False).

**Возвращает**:

- `str`: Хеш-подпись платежа в виде шестнадцатеричной строки.

**Как работает функция**:

- Функция строит строку, включающую логин мерчанта, стоимость товара, номер заказа, 
  пароль мерчанта и дополнительные параметры (ID пользователя, Telegram ID пользователя, ID товара). 
- Для Result URL строка включает только стоимость товара, номер заказа и пароль мерчанта. 
- Дополнительные параметры добавляются в строку в отсортированном порядке по ключу.
-  Хеш-подпись вычисляется с помощью `hashlib.md5`.
-  Возвращается шестнадцатеричное представление полученной хеш-подписи.

**Примеры**:

```python
>>> calculate_signature(
    'merchant_login', 100.00, 12345, 'merchant_password', 1, 123456789, 1
)
'8745321f511913b2498841e992c99708'
>>> calculate_signature(
    'merchant_login', 100.00, 12345, 'merchant_password', 1, 123456789, 1, is_result=True
)
'a8740b9d11d12975070a9df9415175d0'
```

### `generate_payment_link`

**Назначение**: 
Функция `generate_payment_link` создает платежную ссылку для Robokassa с
указанными параметрами.

**Параметры**:

- `cost` (float): Стоимость товара.
- `number` (int): Номер заказа.
- `description` (str): Описание заказа.
- `user_id` (int): ID пользователя.
- `user_telegram_id` (int): Telegram ID пользователя.
- `product_id` (int): ID товара.
- `is_test` (int): Флаг тестового режима (1 - тест, 0 - боевой режим).
- `robokassa_payment_url` (str): URL для оплаты Robokassa.

**Возвращает**:

- `str`: Ссылка на страницу оплаты Robokassa.

**Как работает функция**:

-  Функция вычисляет хеш-подпись платежа с помощью `calculate_signature`.
-  Создает словарь `data` с параметрами платежа, включая логин мерчанта, стоимость товара, номер заказа,
  описание, хеш-подпись, флаг тестового режима, ID пользователя, Telegram ID пользователя и ID товара.
-  Объединяет параметры в строку с помощью `parse.urlencode`.
-  Возвращает ссылку на страницу оплаты Robokassa, добавляя строку с параметрами к базовому URL.

**Примеры**:

```python
>>> generate_payment_link(
    100.00, 12345, 'Оплата товара', 1, 123456789, 1
)
'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=merchant_login&OutSum=100.00&InvId=12345&Description=Оплата+товара&SignatureValue=8745321f511913b2498841e992c99708&IsTest=1&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1'
```

### `parse_response`

**Назначение**:
Функция `parse_response` разбирает строку запроса на параметры платежа.

**Параметры**:

- `request` (str): Строка запроса с параметрами платежа.

**Возвращает**:

- `dict`: Словарь с параметрами платежа.

**Как работает функция**:

-  Функция использует `parse.parse_qsl` для разбора строки запроса 
  и создания словаря с параметрами.
-  Возвращает полученный словарь с параметрами платежа.

**Примеры**:

```python
>>> parse_response('https://example.com?MerchantLogin=merchant_login&OutSum=100.00&InvId=12345')
{'MerchantLogin': 'merchant_login', 'OutSum': '100.00', 'InvId': '12345'}
```

### `check_signature_result`

**Назначение**:
Функция `check_signature_result` проверяет подпись платежа
для Result URL.

**Параметры**:

- `out_sum` (float): Стоимость товара.
- `inv_id` (int): Номер заказа.
- `received_signature` (str): Полученная хеш-подпись платежа.
- `password` (str): Пароль мерчанта в Robokassa (MRH_PASS_2).
- `user_id` (int): ID пользователя.
- `user_telegram_id` (int): Telegram ID пользователя.
- `product_id` (int): ID товара.

**Возвращает**:

- `bool`: `True`, если подпись верна, `False` в противном случае.

**Как работает функция**:

-  Функция вычисляет хеш-подпись платежа с помощью `calculate_signature` 
  и сравнивает ее с полученной хеш-подписью.
-  Сравнивает полученные хеш-подписи в нижнем регистре.
-  Возвращает `True`, если подписи совпадают, 
  и `False` в противном случае.

**Примеры**:

```python
>>> check_signature_result(
    100.00, 12345, '8745321f511913b2498841e992c99708', 'merchant_password', 1, 123456789, 1
)
True
>>> check_signature_result(
    100.00, 12345, 'invalid_signature', 'merchant_password', 1, 123456789, 1
)
False
```

### `result_payment`

**Назначение**:
Функция `result_payment` обрабатывает результат оплаты (ResultURL) 
и возвращает сообщение об успешности оплаты.

**Параметры**:

- `request` (str): Строка запроса с параметрами платежа.

**Возвращает**:

- `str`: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

**Как работает функция**:

-  Функция разбирает строку запроса с помощью `parse_response` 
  и извлекает параметры платежа.
-  Проверяет подпись платежа с помощью `check_signature_result`.
-  Возвращает 'OK' + номер заказа, если подпись верна, 
  иначе возвращает 'bad sign'.

**Примеры**:

```python
>>> result_payment('https://example.com?OutSum=100.00&InvId=12345&SignatureValue=8745321f511913b2498841e992c99708&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
'OK12345'
>>> result_payment('https://example.com?OutSum=100.00&InvId=12345&SignatureValue=invalid_signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
'bad sign'
```

### `check_success_payment`

**Назначение**:
Функция `check_success_payment` проверяет успешность оплаты 
(SuccessURL).

**Параметры**:

- `request` (str): Строка запроса с параметрами платежа.

**Возвращает**:

- `str`: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

**Как работает функция**:

-  Функция разбирает строку запроса с помощью `parse_response` 
  и извлекает параметры платежа.
-  Проверяет подпись платежа с помощью `check_signature_result`.
-  Возвращает сообщение об успешной оплате, если подпись верна, 
  иначе возвращает 'bad sign'.

**Примеры**:

```python
>>> check_success_payment('https://example.com?OutSum=100.00&InvId=12345&SignatureValue=8745321f511913b2498841e992c99708&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
'Thank you for using our service'
>>> check_success_payment('https://example.com?OutSum=100.00&InvId=12345&SignatureValue=invalid_signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
'bad sign'
```