### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор функций для работы с платежной системой Robokassa. Он включает в себя функции для генерации платежных ссылок, проверки подписи, обработки ответов от Robokassa и проверки статуса оплаты.

Шаги выполнения
-------------------------
1. **`calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False)`**:
   - Функция вычисляет подпись для запросов к Robokassa.
   - Функция принимает параметры, такие как логин, стоимость, ID заказа, пароль, ID пользователя, ID пользователя в Telegram и ID товара.
   - Функция использует алгоритм MD5 для генерации подписи на основе переданных параметров.
   - Если `is_result` установлен в `True`, функция использует другой формат строки для вычисления подписи (для Result URL).
   - Функция возвращает вычисленную подпись в виде шестнадцатеричной строки.

2. **`generate_payment_link(cost, number, description, user_id, user_telegram_id, product_id, is_test=1, robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx')`**:
   - Функция генерирует ссылку для оплаты через Robokassa.
   - Функция принимает параметры, такие как стоимость, номер заказа, описание заказа, ID пользователя, ID пользователя в Telegram, ID товара, флаг тестового режима и URL Robokassa.
   - Функция вызывает `calculate_signature` для генерации подписи.
   - Функция формирует словарь с параметрами для передачи в Robokassa.
   - Функция кодирует параметры в URL и объединяет их с базовым URL Robokassa.
   - Функция возвращает готовую ссылку для оплаты.

3. **`parse_response(request)`**:
   - Функция разбирает строку запроса на параметры.
   - Функция принимает строку запроса в качестве параметра.
   - Функция использует `urllib.parse.parse_qsl` и `urllib.parse.urlparse` для извлечения параметров из строки запроса.
   - Функция возвращает словарь с параметрами.

4. **`check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id)`**:
   - Функция проверяет подпись, полученную от Robokassa.
   - Функция принимает параметры, такие как сумма оплаты, ID заказа, полученная подпись, пароль, ID пользователя, ID пользователя в Telegram и ID товара.
   - Функция вызывает `calculate_signature` для вычисления подписи на основе полученных параметров.
   - Функция сравнивает вычисленную подпись с полученной подписью (без учета регистра).
   - Функция возвращает `True`, если подписи совпадают, и `False` в противном случае.

5. **`result_payment(request)`**:
   - Функция обрабатывает результат оплаты (ResultURL).
   - Функция принимает строку запроса с параметрами оплаты.
   - Функция вызывает `parse_response` для извлечения параметров из строки запроса.
   - Функция вызывает `check_signature_result` для проверки подписи.
   - Если подпись верна, функция возвращает `'OK' + номер заказа`, иначе возвращает `'bad sign'`.

6. **`check_success_payment(request)`**:
   - Функция проверяет успешность оплаты (SuccessURL).
   - Функция принимает строку запроса с параметрами оплаты.
   - Функция вызывает `parse_response` для извлечения параметров из строки запроса.
   - Функция вызывает `check_signature_result` для проверки подписи.
   - Если подпись верна, функция возвращает сообщение об успешной оплате, иначе возвращает `'bad sign'`.

Пример использования
-------------------------

```python
from bot.config import settings
from urllib import parse
import hashlib

def calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False):
    if is_result:
        base_string = f"{cost}:{inv_id}:{password}"  # Для Result URL
    else:
        base_string = f"{login}:{cost}:{inv_id}:{password}"  # Для initital URL и Success URL

    additional_params = {
        'Shp_user_id': user_id,
        'Shp_user_telegram_id': user_telegram_id,
        'Shp_product_id': product_id
    }
    for key, value in sorted(additional_params.items()):
        base_string += f":{key}={value}"

    return hashlib.md5(base_string.encode('utf-8')).hexdigest()


def generate_payment_link(cost: float, number: int, description: str,
                          user_id: int, user_telegram_id: int, product_id: int,
                          is_test=1, robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx') -> str:
    """
    Функция генерирует ссылку для оплаты через Robokassa с обязательными параметрами.

    Args:
        cost (float): Стоимость товара.
        number (int): Номер заказа.
        description (str): Описание заказа.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_test (int): Флаг тестового режима (1 - тест, 0 - боевой режим).
        robokassa_payment_url (str): URL для оплаты Robokassa.

    Returns:
        str: Ссылка на страницу оплаты.
    """
    signature = calculate_signature(
        settings.MRH_LOGIN,
        cost,
        number,
        settings.MRH_PASS_1,
        user_id,
        user_telegram_id,
        product_id
    )

    data = {
        'MerchantLogin': settings.MRH_LOGIN,
        'OutSum': cost,
        'InvId': number,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test,
        'Shp_user_id': user_id,
        'Shp_user_telegram_id': user_telegram_id,
        'Shp_product_id': product_id
    }

    return f'{robokassa_payment_url}?{parse.urlencode(data)}'


# Пример использования generate_payment_link
payment_link = generate_payment_link(
    cost=100.0,
    number=123,
    description="Test Order",
    user_id=1,
    user_telegram_id=123456789,
    product_id=1
)

print(f"Payment Link: {payment_link}")