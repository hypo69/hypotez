# Модуль утилит для бота Telegram
## Overview
Этот модуль содержит набор утилитных функций, используемых для обработки платежей, генерации ссылок и проверки подписи для бота Telegram.

## Details
В модуле реализованы следующие функции:
- `calculate_signature`: вычисляет MD5-хеш для подписи платежной операции.
- `generate_payment_link`: генерирует ссылку на страницу оплаты через Robokassa с использованием необходимых параметров.
- `parse_response`: разбирает строку запроса на параметры.
- `check_signature_result`: проверяет подпись результата платежа.
- `result_payment`: обрабатывает результат платежа (ResultURL).
- `check_success_payment`: проверяет успешность платежа (SuccessURL).

## Functions
### `calculate_signature`
#### Purpose
Функция вычисляет MD5-хеш для подписи платежной операции.

#### Parameters
- `login` (str): Логин продавца.
- `cost` (float): Стоимость товара.
- `inv_id` (int): Номер заказа.
- `password` (str): Пароль продавца.
- `user_id` (int): ID пользователя.
- `user_telegram_id` (int): Telegram ID пользователя.
- `product_id` (int): ID товара.
- `is_result` (bool, optional): Флаг, указывающий, является ли подпись для Result URL (True) или для Initial/Success URL (False). По умолчанию - False.

#### Returns
- `str`: MD5-хеш подписи.

#### How the Function Works
- В зависимости от значения `is_result`, функция формирует базовую строку для вычисления хеша.
- В базовую строку добавляются дополнительные параметры (`Shp_user_id`, `Shp_user_telegram_id`, `Shp_product_id`) в отсортированном порядке.
- Вычисляется MD5-хеш от закодированной в UTF-8 базовой строки.
- Функция возвращает полученный хеш в виде шестнадцатеричной строки.

### `generate_payment_link`
#### Purpose
Функция генерирует ссылку для оплаты через Robokassa с обязательными параметрами.

#### Parameters
- `cost` (float): Стоимость товара.
- `number` (int): Номер заказа.
- `description` (str): Описание заказа.
- `user_id` (int): ID пользователя.
- `user_telegram_id` (int): Telegram ID пользователя.
- `product_id` (int): ID товара.
- `is_test` (int, optional): Флаг тестового режима (1 - тест, 0 - боевой режим). По умолчанию - 1 (тестовый режим).
- `robokassa_payment_url` (str, optional): URL для оплаты Robokassa. По умолчанию - 'https://auth.robokassa.ru/Merchant/Index.aspx'.

#### Returns
- `str`: Ссылка на страницу оплаты.

#### How the Function Works
- Вызывается функция `calculate_signature` для получения подписи.
- Формируется словарь `data` с параметрами платежа, включая полученную подпись.
- Ссылка на страницу оплаты формируется путем конкатенации URL Robokassa с закодированными параметрами из словаря `data`.
- Функция возвращает сформированную ссылку.

### `parse_response`
#### Purpose
Функция разбирает строку запроса на параметры.

#### Parameters
- `request` (str): Строка запроса.

#### Returns
- `dict`: Словарь с параметрами запроса.

#### How the Function Works
- Используется функция `parse.parse_qsl` из модуля `urllib.parse` для разбора строки запроса.
- Функция возвращает словарь, где ключи - это имена параметров, а значения - соответствующие значения.

### `check_signature_result`
#### Purpose
Функция проверяет подпись результата платежа.

#### Parameters
- `out_sum` (float): Сумма платежа.
- `inv_id` (int): Номер заказа.
- `received_signature` (str): Полученная подпись результата платежа.
- `password` (str): Пароль продавца.
- `user_id` (int): ID пользователя.
- `user_telegram_id` (int): Telegram ID пользователя.
- `product_id` (int): ID товара.

#### Returns
- `bool`: True, если подпись верна, иначе False.

#### How the Function Works
- Вызывается функция `calculate_signature` для вычисления правильной подписи с использованием `is_result=True`.
- Сравниваются полученная подпись (`received_signature`) и вычисленная подпись (`signature`) в нижнем регистре.
- Функция возвращает True, если подписи совпадают, иначе False.

### `result_payment`
#### Purpose
Функция обрабатывает результат платежа (ResultURL).

#### Parameters
- `request` (str): Строка запроса с параметрами оплаты.

#### Returns
- `str`: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

#### How the Function Works
- Используется функция `parse_response` для разбора строки запроса.
- Вызывается функция `check_signature_result` для проверки подписи.
- Если подпись верна, функция возвращает 'OK' + номер заказа.
- В противном случае функция возвращает 'bad sign'.

### `check_success_payment`
#### Purpose
Функция проверяет успешность платежа (SuccessURL).

#### Parameters
- `request` (str): Строка запроса с параметрами оплаты.

#### Returns
- `str`: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

#### How the Function Works
- Используется функция `parse_response` для разбора строки запроса.
- Вызывается функция `check_signature_result` для проверки подписи.
- Если подпись верна, функция возвращает сообщение об успешной оплате.
- В противном случае функция возвращает 'bad sign'.

## Parameter Details
- `login` (str): Логин продавца в Robokassa.
- `cost` (float): Сумма платежа.
- `inv_id` (int): Номер заказа.
- `password` (str): Пароль продавца в Robokassa.
- `user_id` (int): ID пользователя в системе.
- `user_telegram_id` (int): Telegram ID пользователя.
- `product_id` (int): ID товара в системе.
- `is_test` (int, optional): Флаг тестового режима (1 - тест, 0 - боевой режим). По умолчанию - 1 (тестовый режим).
- `robokassa_payment_url` (str, optional): URL для оплаты Robokassa. По умолчанию - 'https://auth.robokassa.ru/Merchant/Index.aspx'.
- `out_sum` (float): Сумма платежа, полученная от Robokassa.
- `received_signature` (str): Подпись, полученная от Robokassa.
- `request` (str): Строка запроса с параметрами оплаты.

## Examples
```python
# Генерация ссылки на оплату
payment_link = generate_payment_link(cost=100.0, number=12345, description='Покупка товара', user_id=1, user_telegram_id=123456789, product_id=1)
print(payment_link)

# Обработка результата платежа
result_request = 'https://example.com/result?OutSum=100.0&InvId=12345&SignatureValue=abc1234567890abcdef&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1'
result = result_payment(result_request)
print(result) # Выведет 'OK12345' если оплата прошла успешно, или 'bad sign' в случае ошибки

# Проверка успешности платежа
success_request = 'https://example.com/success?OutSum=100.0&InvId=12345&SignatureValue=abc1234567890abcdef&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1'
success = check_success_payment(success_request)
print(success) # Выведет 'Thank you for using our service' если оплата прошла успешно, или 'bad sign' в случае ошибки
```