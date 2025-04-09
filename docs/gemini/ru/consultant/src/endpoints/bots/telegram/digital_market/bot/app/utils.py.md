### **Анализ кода модуля `utils.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/app/utils.py

Модуль содержит функции для работы с Robokassa, включая генерацию платежных ссылок, проверку подписи и обработку ответов от Robokassa.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура функций.
  - Использование `hashlib` для расчета подписи.
  - Разделение логики на отдельные функции для генерации ссылок, проверки подписи и обработки ответов.
- **Минусы**:
  - Отсутствие документации модуля.
  - Docstring функций на английском языке.
  - Нет аннотаций типов для параметров и возвращаемых значений функций.
  - Не используется `logger` для логирования ошибок и отладки.

**Рекомендации по улучшению**:

1.  **Добавить документацию модуля**:
    - В начале файла добавить общее описание модуля, его назначения и примеры использования.

2.  **Перевести docstring на русский язык**:
    - Все docstring должны быть переведены на русский язык для соответствия стандартам проекта.

3.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех параметров и возвращаемых значений функций.

4.  **Использовать `logger` для логирования**:
    - Добавить логирование ошибок и важных событий с использованием модуля `logger` из `src.logger`.

5.  **Улучшить форматирование**:
    - Использовать константы для параметров, которые часто используются (например, коды ошибок).

6.  **Упростить логику `calculate_signature`**:
    - Сделать функцию более читаемой, разделив логику на несколько этапов.

7.  **Проверять типы данных**:
    - Добавить проверки типов данных для входных параметров, чтобы избежать неожиданных ошибок.

**Оптимизированный код**:

```python
"""
Модуль содержит функции для работы с Robokassa.
==================================================

Модуль включает функции для генерации платежных ссылок, проверки подписи и обработки ответов от Robokassa.

Пример использования
----------------------

>>> from bot.config import settings
>>> payment_link = generate_payment_link(100.0, 12345, "Test Payment", 1, 123, 1)
>>> print(payment_link)
https://auth.robokassa.ru/Merchant/Index.aspx?...
"""
import hashlib
from urllib import parse
from urllib.parse import urlparse
from bot.config import settings
from src.logger import logger

def calculate_signature(
    login: str,
    cost: float,
    inv_id: int,
    password: str,
    user_id: int,
    user_telegram_id: int,
    product_id: int,
    is_result: bool = False
) -> str:
    """
    Вычисляет подпись для запросов к Robokassa.

    Args:
        login (str): Логин магазина в Robokassa.
        cost (float): Сумма платежа.
        inv_id (int): Номер заказа.
        password (str): Пароль магазина в Robokassa.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID продукта.
        is_result (bool, optional): Флаг, указывающий, что подпись вычисляется для Result URL. Defaults to False.

    Returns:
        str: MD5-хеш, представляющий подпись.

    Example:
        >>> calculate_signature('login', 100.0, 12345, 'password', 1, 123, 1)
        'e10adc3949ba59abbe56e057f20f883e'
    """
    try:
        if is_result:
            base_string = f'{cost}:{inv_id}:{password}'  # Для Result URL
        else:
            base_string = f'{login}:{cost}:{inv_id}:{password}'  # Для initital URL и Success URL

        additional_params = {
            'Shp_user_id': user_id,
            'Shp_user_telegram_id': user_telegram_id,
            'Shp_product_id': product_id
        }
        for key, value in sorted(additional_params.items()):
            base_string += f':{key}={value}'

        return hashlib.md5(base_string.encode('utf-8')).hexdigest()
    except Exception as ex:
        logger.error('Ошибка при вычислении подписи', ex, exc_info=True)
        return ''


def generate_payment_link(
    cost: float,
    number: int,
    description: str,
    user_id: int,
    user_telegram_id: int,
    product_id: int,
    is_test: int = 1,
    robokassa_payment_url: str = 'https://auth.robokassa.ru/Merchant/Index.aspx'
) -> str:
    """
    Генерирует ссылку для оплаты через Robokassa с обязательными параметрами.

    Args:
        cost (float): Стоимость товара.
        number (int): Номер заказа.
        description (str): Описание заказа.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_test (int, optional): Флаг тестового режима (1 - тест, 0 - боевой режим). Defaults to 1.
        robokassa_payment_url (str, optional): URL для оплаты Robokassa. Defaults to 'https://auth.robokassa.ru/Merchant/Index.aspx'.

    Returns:
        str: Ссылка на страницу оплаты.

    Example:
        >>> from bot.config import settings
        >>> payment_link = generate_payment_link(100.0, 12345, "Test Payment", 1, 123, 1)
        >>> print(payment_link)
        https://auth.robokassa.ru/Merchant/Index.aspx?...
    """
    try:
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
    except Exception as ex:
        logger.error('Ошибка при генерации платежной ссылки', ex, exc_info=True)
        return ''


def parse_response(request: str) -> dict:
    """
    Разбирает строку запроса на параметры.

    Args:
        request (str): Строка запроса.

    Returns:
        dict: Словарь с параметрами.

    Example:
        >>> request = 'https://example.com?param1=value1&param2=value2'
        >>> parse_response(request)
        {'param1': 'value1', 'param2': 'value2'}
    """
    try:
        return dict(parse.parse_qsl(urlparse(request).query))
    except Exception as ex:
        logger.error('Ошибка при разборе строки запроса', ex, exc_info=True)
        return {}


def check_signature_result(
    out_sum: float,
    inv_id: int,
    received_signature: str,
    password: str,
    user_id: int,
    user_telegram_id: int,
    product_id: int
) -> bool:
    """
    Проверяет подпись для ResultURL.

    Args:
        out_sum (float): Сумма платежа.
        inv_id (int): Номер заказа.
        received_signature (str): Полученная подпись.
        password (str): Пароль магазина в Robokassa.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID продукта.

    Returns:
        bool: True, если подпись верна, иначе False.

    Example:
        >>> check_signature_result(100.0, 12345, 'signature', 'password', 1, 123, 1)
        False
    """
    try:
        signature = calculate_signature(
            settings.MRH_LOGIN,
            out_sum,
            inv_id,
            password,
            user_id,
            user_telegram_id,
            product_id,
            is_result=True  # Важный флаг для Result URL
        )
        return signature.lower() == received_signature.lower()
    except Exception as ex:
        logger.error('Ошибка при проверке подписи', ex, exc_info=True)
        return False


def result_payment(request: str) -> str:
    """
    Обрабатывает результат оплаты (ResultURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

    Example:
        >>> result_payment('https://example.com?OutSum=100.0&InvId=12345&SignatureValue=signature&Shp_user_id=1&Shp_user_telegram_id=123&Shp_product_id=1')
        'bad sign'
    """
    try:
        params = parse_response(request)
        out_sum = params['OutSum']
        inv_id = params['InvId']
        signature = params['SignatureValue']
        user_id = params['Shp_user_id']
        user_telegram_id = params['Shp_user_telegram_id']
        product_id = params['Shp_product_id']

        if check_signature_result(out_sum, inv_id, signature, settings.MRH_PASS_2, user_id, user_telegram_id, product_id):
            return f'OK{inv_id}'
        return 'bad sign'
    except Exception as ex:
        logger.error('Ошибка при обработке результата оплаты', ex, exc_info=True)
        return 'bad sign'


def check_success_payment(request: str) -> str:
    """
    Проверяет успешность оплаты (SuccessURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

    Example:
        >>> check_success_payment('https://example.com?OutSum=100.0&InvId=12345&SignatureValue=signature&Shp_user_id=1&Shp_user_telegram_id=123&Shp_product_id=1')
        'bad sign'
    """
    try:
        params = parse_response(request)
        out_sum = params['OutSum']
        inv_id = params['InvId']
        signature = params['SignatureValue']
        user_id = params['Shp_user_id']
        user_telegram_id = params['Shp_user_telegram_id']
        product_id = params['Shp_product_id']

        if check_signature_result(out_sum, inv_id, signature, settings.MRH_PASS_1, user_id, user_telegram_id, product_id):
            return 'Thank you for using our service'
        return 'bad sign'
    except Exception as ex:
        logger.error('Ошибка при проверке успешности оплаты', ex, exc_info=True)
        return 'bad sign'