### **Анализ кода модуля `utils.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/app/utils.py

Модуль содержит функции для работы с Robokassa, включая генерацию платежных ссылок, проверку подписи и обработку ответов от Robokassa.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован.
  - Функции имеют docstring, описывающие их назначение и параметры.
  - Используется hashlib для вычисления MD5 хеша.
- **Минусы**:
  - Не все переменные аннотированы типами.
  - В docstring есть англоязычные элементы.
  - Жестко заданы значения параметров, таких как `is_test=1` и URL `robokassa_payment_url`.
  - Используется устаревший способ форматирования строк (f-strings предпочтительнее).

**Рекомендации по улучшению:**

1.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и возвращаемых значений функций.

2.  **Комментарии и документация**:
    - Перевести все docstring на русский язык и привести к единообразному стилю.
    - Уточнить комментарии, где это необходимо.

3.  **Конфигурация**:
    - Вынести URL `robokassa_payment_url` в настройки (settings) и использовать его оттуда.

4.  **Форматирование строк**:
    - Использовать f-strings для конкатенации строк, где это применимо.

5.  **Безопасность**:
    - Рассмотреть возможность использования более безопасного алгоритма хеширования, чем MD5 (хотя это может потребовать изменений на стороне Robokassa).

6. **Логирование**:
    - Добавить логирование для важных событий, таких как генерация ссылки и проверка подписи.

**Оптимизированный код:**

```python
import hashlib
from urllib import parse
from urllib.parse import urlparse

from bot.config import settings
from typing import Dict, Union
from src.logger import logger


def calculate_signature(login: str, cost: float, inv_id: int, password: str, user_id: int,
                        user_telegram_id: int, product_id: int, is_result: bool = False) -> str:
    """
    Вычисляет подпись для Robokassa.

    Args:
        login (str): Логин мерчанта.
        cost (float): Сумма платежа.
        inv_id (int): ID заказа.
        password (str): Пароль мерчанта.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID продукта.
        is_result (bool): Флаг, указывающий, что это Result URL. По умолчанию False.

    Returns:
        str: MD5-хеш, представляющий подпись.

    """
    # Формируем строку для хеширования в зависимости от типа URL (Result или Success)
    if is_result:
        base_string = f'{cost}:{inv_id}:{password}'  # Для Result URL
    else:
        base_string = f'{login}:{cost}:{inv_id}:{password}'  # Для initial URL и Success URL

    # Дополнительные параметры
    additional_params: Dict[str, int] = {
        'Shp_user_id': user_id,
        'Shp_user_telegram_id': user_telegram_id,
        'Shp_product_id': product_id
    }

    # Добавляем параметры в строку, сортируем ключи для консистентности
    for key, value in sorted(additional_params.items()):
        base_string += f':{key}={value}'

    # Вычисляем MD5-хеш от строки в кодировке UTF-8 и возвращаем в шестнадцатеричном формате
    signature = hashlib.md5(base_string.encode('utf-8')).hexdigest()
    logger.info(f'Подпись успешно вычислена: {signature}')
    return signature


def generate_payment_link(cost: float, number: int, description: str,
                          user_id: int, user_telegram_id: int, product_id: int,
                          is_test: int = 1, robokassa_payment_url: str = settings.ROBOKASSA_PAYMENT_URL) -> str:
    """
    Генерирует ссылку для оплаты через Robokassa с обязательными параметрами.

    Args:
        cost (float): Стоимость товара.
        number (int): Номер заказа.
        description (str): Описание заказа.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID товара.
        is_test (int): Флаг тестового режима (1 - тест, 0 - боевой режим). По умолчанию 1.
        robokassa_payment_url (str): URL для оплаты Robokassa. По умолчанию берется из настроек.

    Returns:
        str: Ссылка на страницу оплаты.

    """
    # Вычисляем подпись для запроса
    signature: str = calculate_signature(
        settings.MRH_LOGIN,
        cost,
        number,
        settings.MRH_PASS_1,
        user_id,
        user_telegram_id,
        product_id
    )

    # Формируем словарь с данными для запроса
    data: Dict[str, Union[int, float, str]] = {
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

    # Формируем URL для оплаты
    payment_link: str = f'{robokassa_payment_url}?{parse.urlencode(data)}'
    logger.info(f'Сгенерирована ссылка для оплаты: {payment_link}')
    return payment_link


def parse_response(request: str) -> Dict[str, str]:
    """
    Разбирает строку запроса на параметры.

    Args:
        request (str): Строка запроса.

    Returns:
        Dict[str, str]: Словарь с параметрами.

    """
    # Парсим строку запроса и возвращаем словарь с параметрами
    parsed_response: Dict[str, str] = dict(parse.parse_qsl(urlparse(request).query))
    logger.debug(f'Строка запроса успешно разобрана: {parsed_response}')
    return parsed_response


def check_signature_result(out_sum: float, inv_id: int, received_signature: str, password: str,
                           user_id: int, user_telegram_id: int, product_id: int) -> bool:
    """
    Проверяет подпись для ResultURL.

    Args:
        out_sum (float): Сумма платежа.
        inv_id (int): ID заказа.
        received_signature (str): Полученная подпись.
        password (str): Пароль мерчанта.
        user_id (int): ID пользователя.
        user_telegram_id (int): Telegram ID пользователя.
        product_id (int): ID продукта.

    Returns:
        bool: True, если подпись верна, иначе False.

    """
    # Вычисляем подпись на основе параметров
    signature: str = calculate_signature(
        settings.MRH_LOGIN,
        out_sum,
        inv_id,
        password,
        user_id,
        user_telegram_id,
        product_id,
        is_result=True  # Важный флаг для Result URL
    )

    # Сравниваем вычисленную подпись с полученной, приводя обе к нижнему регистру
    is_valid: bool = signature.lower() == received_signature.lower()
    if is_valid:
        logger.info('Подпись ResultURL верна.')
    else:
        logger.warning('Подпись ResultURL неверна.')
    return is_valid


def result_payment(request: str) -> str:
    """
    Обрабатывает результат оплаты (ResultURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: 'OK' + номер заказа, если оплата прошла успешно, иначе 'bad sign'.

    """
    # Получаем параметры из запроса
    params: Dict[str, str] = parse_response(request)
    out_sum: str = params['OutSum']
    inv_id: str = params['InvId']
    signature: str = params['SignatureValue']
    user_id: str = params['Shp_user_id']
    user_telegram_id: str = params['Shp_user_telegram_id']
    product_id: str = params['Shp_product_id']

    # Проверяем подпись
    if check_signature_result(float(out_sum), int(inv_id), signature, settings.MRH_PASS_2, int(user_id),
                              int(user_telegram_id), int(product_id)):
        result: str = f'OK{inv_id}'
        logger.info(f'Успешная обработка ResultURL: {result}')
        return result
    logger.warning('Неверная подпись ResultURL.')
    return "bad sign"


def check_success_payment(request: str) -> str:
    """
    Проверяет успешность оплаты (SuccessURL).

    Args:
        request (str): Строка запроса с параметрами оплаты.

    Returns:
        str: Сообщение об успешной оплате или 'bad sign' при неверной подписи.

    """
    # Получаем параметры из запроса
    params: Dict[str, str] = parse_response(request)
    out_sum: str = params['OutSum']
    inv_id: str = params['InvId']
    signature: str = params['SignatureValue']
    user_id: str = params['Shp_user_id']
    user_telegram_id: str = params['Shp_user_telegram_id']
    product_id: str = params['Shp_product_id']

    # Проверяем подпись
    if check_signature_result(float(out_sum), int(inv_id), signature, settings.MRH_PASS_1, int(user_id),
                              int(user_telegram_id), int(product_id)):
        message: str = "Thank you for using our service"
        logger.info(f'Успешная проверка SuccessURL: {message}')
        return message
    logger.warning('Неверная подпись SuccessURL.')
    return "bad sign"