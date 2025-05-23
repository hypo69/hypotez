## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует функции для работы с платежной системой Robokassa. Он предоставляет инструменты для:

* **Генерации платежной ссылки:** создание ссылки для перехода на сайт Robokassa для оплаты товара.
* **Проверки подписи:** валидации подписи, получаемой от Robokassa, чтобы убедиться, что платеж был обработан системой.
* **Обработки результата оплаты:** получение и обработка информации об успешной оплате товара.

Шаги выполнения
-------------------------
1. **Генерация платежной ссылки:**
    - Используется функция `generate_payment_link`, которая принимает на вход информацию о товаре, пользователе и платежной системе.
    - Функция генерирует подпись (`signature`) для ссылки, используя функцию `calculate_signature`.
    - Ссылка формируется с помощью `parse.urlencode`, которая кодирует словарь данных в URL-параметры.
2. **Проверка подписи:**
    - Функция `check_signature_result` проверяет корректность подписи, полученной от Robokassa.
    - Используется функция `calculate_signature` для вычисления собственной подписи по данным, полученным от Robokassa.
    - Сравнение полученной подписи с вычисленной: если они совпадают, платеж считается валидным.
3. **Обработка результата оплаты:**
    - Функции `result_payment` и `check_success_payment` обрабатывают результат оплаты от Robokassa.
    - Используются функции `parse_response` и `check_signature_result` для извлечения и проверки данных из запроса.
    - Если подпись верна, то возвращается сообщение об успешной оплате, иначе возвращается сообщение об ошибке.

Пример использования
-------------------------

```python
from bot.app.utils import generate_payment_link, result_payment

# Данные о товаре, пользователе и платежной системе
cost = 10.0  # Стоимость товара
number = 1234  # Номер заказа
description = "Оплата товара"
user_id = 123  # ID пользователя
user_telegram_id = 1234567890  # Telegram ID пользователя
product_id = 567  # ID товара

# Генерация платежной ссылки
payment_link = generate_payment_link(cost, number, description, user_id, user_telegram_id, product_id)

# Вывод ссылки для пользователя
print(f"Перейдите по этой ссылке для оплаты: {payment_link}")

# Обработка результата оплаты
request_from_robokassa = "https://www.example.com/?OutSum=10.0&InvId=1234&SignatureValue=signature_value&Shp_user_id=123&Shp_user_telegram_id=1234567890&Shp_product_id=567"
result = result_payment(request_from_robokassa)

# Вывод результата оплаты
print(f"Результат оплаты: {result}")
```