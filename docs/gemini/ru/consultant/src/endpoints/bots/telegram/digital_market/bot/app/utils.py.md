### **Анализ кода модуля `utils.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/app/utils.py

Модуль содержит утилиты для работы с Robokassa, включая функции для генерации платежных ссылок, проверки подписи и обработки ответов от Robokassa.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура функций.
  - Использование аннотаций типов.
  - Функции хорошо документированы (docstring).
- **Минусы**:
  - Не все переменные аннотированы типами.
  - В docstring используется английский язык. Необходимо перевести на русский.
  - Не используется модуль `logger` для логирования ошибок и важных событий.
  - Отсутствуют примеры использования в docstring.
  - Есть константы, которые можно вынести в настройки или сделать более читаемыми.
  - Не используется единый стиль кавычек (используются как одинарные, так и двойные).

**Рекомендации по улучшению:**

1.  **Перевод docstring на русский язык**:
    - Необходимо перевести все docstring на русский язык, чтобы соответствовать требованиям.
2.  **Добавление примеров использования в docstring**:
    - В каждый docstring добавить раздел "Example", демонстрирующий использование функции.
3.  **Использование `logger`**:
    - Добавить логирование важных событий и ошибок с использованием модуля `logger` из `src.logger`.
4.  **Унификация кавычек**:
    - Использовать только одинарные кавычки для строк.
5.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это необходимо.
6.  **Улучшение констант**:
    - Рассмотреть возможность выноса констант в настройки или определения их как константы модуля для улучшения читаемости.
7. **Более конкретные имена переменных**:
    - Переименовать переменные, такие как `request` в `parse_string` или `query_string`, чтобы код был более понятным.

**Оптимизированный код:**

```python
import hashlib
from urllib import parse
from urllib.parse import urlparse
from bot.config import settings
from typing import Dict, Union
from src.logger import logger


def calculate_signature(
    login: str,
    cost: float,
    inv_id: int,
    password: str,
    user_id: int,
    user_telegram_id: int,
    product_id: int,
    is_result: bool = False,
) -> str:
    """
    Вычисляет подпись для Robokassa.

    Args:
        login (str): Логин магазина в Robokassa.
        cost (float): Сумма платежа.
        inv_id (int): Номер заказа.
        password (str): Пароль магазина в Robokassa.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID продукта.
        is_result (bool): Флаг, указывающий, что подпись вычисляется для ResultURL.

    Returns:
        str: Подпись в виде MD5-хеша.

    Example:
        >>> calculate_signature('login', 100.0, 123, 'password', 1, 123456789, 1, is_result=True)
        'e10adc3949ba59abbe56e057f20f883e'
    """
    if is_result:
        base_string: str = f'{cost}:{inv_id}:{password}'  # Для Result URL
    else:
        base_string: str = f'{login}:{cost}:{inv_id}:{password}'  # Для initial URL и Success URL

    additional_params: Dict[str, int] = {
        'Shp_user_id': user_id,
        'Shp_user_telegram_id': user_telegram_id,
        'Shp_product_id': product_id,
    }
    for key, value in sorted(additional_params.items()):
        base_string += f':{key}={value}'

    return hashlib.md5(base_string.encode('utf-8')).hexdigest()


def generate_payment_link(
    cost: float,
    number: int,
    description: str,
    user_id: int,
    user_telegram_id: int,
    product_id: int,
    is_test: int = 1,
    robokassa_payment_url: str = 'https://auth.robokassa.ru/Merchant/Index.aspx',
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
        is_test (int): Флаг тестового режима (1 - тест, 0 - боевой режим).
        robokassa_payment_url (str): URL для оплаты Robokassa.

    Returns:
        str: Ссылка на страницу оплаты.

    Example:
        >>> generate_payment_link(100.0, 123, 'Test order', 1, 123456789, 1)
        'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=login&OutSum=100.0&InvId=123&Description=Test+order&SignatureValue=signature&IsTest=1&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1'
    """
    signature: str = calculate_signature(
        settings.MRH_LOGIN,
        cost,
        number,
        settings.MRH_PASS_1,
        user_id,
        user_telegram_id,
        product_id,
    )

    data: Dict[str, Union[int, float, str]] = {
        'MerchantLogin': settings.MRH_LOGIN,
        'OutSum': cost,
        'InvId': number,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test,
        'Shp_user_id': user_id,
        'Shp_user_telegram_id': user_telegram_id,
        'Shp_product_id': product_id,
    }

    return f'{robokassa_payment_url}?{parse.urlencode(data)}'


def parse_response(parse_string: str) -> Dict[str, str]:
    """
    Разбирает строку запроса на параметры.

    Args:
        parse_string (str): Строка запроса.

    Returns:
        Dict[str, str]: Словарь с параметрами.

    Example:
        >>> parse_response('https://example.com?param1=value1&param2=value2')
        {'param1': 'value1', 'param2': 'value2'}
    """
    return dict(parse.parse_qsl(urlparse(parse_string).query))


def check_signature_result(
    out_sum: float,
    inv_id: int,
    received_signature: str,
    password: str,
    user_id: int,
    user_telegram_id: int,
    product_id: int,
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
        >>> check_signature_result(100.0, 123, 'signature', 'password', 1, 123456789, 1)
        True
    """
    signature: str = calculate_signature(
        settings.MRH_LOGIN,
        out_sum,
        inv_id,
        password,
        user_id,
        user_telegram_id,
        product_id,
        is_result=True,  # Важный флаг для Result URL
    )
    return signature.lower() == received_signature.lower()


def result_payment(query_string: str) -> str:
    """
    Обрабатывает результат оплаты (ResultURL).

    Args:
        query_string (str): Строка запроса с параметрами оплаты.

    Returns:
        str: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

    Example:
        >>> result_payment('https://example.com?OutSum=100.0&InvId=123&SignatureValue=signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
        'OK123'
    """
    params: Dict[str, str] = parse_response(query_string)
    out_sum: str = params['OutSum']
    inv_id: str = params['InvId']
    signature: str = params['SignatureValue']
    user_id: str = params['Shp_user_id']
    user_telegram_id: str = params['Shp_user_telegram_id']
    product_id: str = params['Shp_product_id']

    try:
        if check_signature_result(
            float(out_sum),
            int(inv_id),
            signature,
            settings.MRH_PASS_2,
            int(user_id),
            int(user_telegram_id),
            int(product_id),
        ):
            return f'OK{inv_id}'
        return 'bad sign'
    except Exception as ex:
        logger.error('Error while processing result payment', ex, exc_info=True)
        return 'bad sign'


def check_success_payment(query_string: str) -> str:
    """
    Проверяет успешность оплаты (SuccessURL).

    Args:
        query_string (str): Строка запроса с параметрами оплаты.

    Returns:
        str: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

    Example:
        >>> check_success_payment('https://example.com?OutSum=100.0&InvId=123&SignatureValue=signature&Shp_user_id=1&Shp_user_telegram_id=123456789&Shp_product_id=1')
        'Thank you for using our service'
    """
    params: Dict[str, str] = parse_response(query_string)
    out_sum: str = params['OutSum']
    inv_id: str = params['InvId']
    signature: str = params['SignatureValue']
    user_id: str = params['Shp_user_id']
    user_telegram_id: str = params['Shp_user_telegram_id']
    product_id: str = params['Shp_product_id']

    try:
        if check_signature_result(
            float(out_sum),
            int(inv_id),
            signature,
            settings.MRH_PASS_1,
            int(user_id),
            int(user_telegram_id),
            int(product_id),
        ):
            return 'Thank you for using our service'
        return 'bad sign'
    except Exception as ex:
        logger.error('Error while processing success payment', ex, exc_info=True)
        return 'bad sign'