### **Анализ кода модуля `app.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/app/app.py

Модуль содержит основные обработчики для веб-приложения, включая обработку вебхуков от Telegram, главной страницы и взаимодействие с Robokassa.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура обработчиков.
  - Использование `logger` для логирования.
  - Обработка исключений.
- **Минусы**:
  - Отсутствуют аннотации типов для параметров функций `robokassa_fail` и `handle_webhook`.
  - Не используется `j_loads` для загрузки конфигурационных файлов.
  - Не все docstring переведены на русский язык.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов:**
    - Добавить аннотации типов для параметров функций `robokassa_fail` и `handle_webhook`, чтобы улучшить читаемость и предотвратить возможные ошибки.
2.  **Использовать `j_loads`:**
    - Если используются конфигурационные файлы, заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
3.  **Перевести docstring на русский язык:**
    - Перевести все docstring на русский язык для соответствия требованиям.
4.  **Более точные описания в комментариях и docstring:**
    -  Избегай расплывчатых терминов, таких как *«получить»* или *«делать»*. Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.

**Оптимизированный код:**

```python
import datetime

from aiohttp import web
from aiogram.types import Update
from loguru import logger

# from bot.app.utils import check_signature_result
from bot.app.utils import check_signature_result
from bot.config import bot, dp, settings
from bot.dao.database import async_session_maker
from bot.user.utils import successful_payment_logic


async def handle_webhook(request: web.Request) -> web.Response:
    """
    Обрабатывает вебхук от Telegram.

    Args:
        request (web.Request): HTTP-запрос.

    Returns:
        web.Response: HTTP-ответ.
    """
    try:
        update = Update(**await request.json())
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as ex:
        logger.error("Ошибка при обработке вебхука", ex, exc_info=True)  # Логируем ошибку
        return web.Response(status=500)


# Функция для обработки запроса на эндпоинт "Hello, World!"
async def home_page(request: web.Request) -> web.Response:
    """
    Обработчик для отображения главной страницы с информацией о сервисе.

    Args:
        request (web.Request): HTTP-запрос.

    Returns:
        web.Response: HTTP-ответ с HTML-контентом.

    Example:
        >>> from aiohttp import web
        >>> request = web.Request(method='GET', url='/', app=web.Application())
        >>> response = await home_page(request)
        >>> print(response.status)
        200
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>aiohttp Демонстрация</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            .info {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Привет, меня зовут Яковенко Алексей</h1>
        <p>Тут вы видите то, что aiohttp способен вполне себе рендерить и HTML странички.</p>
        <div class="info">
            <p>Через aiohttp в данном проекте обрабатываются:</p>
            <ul>
                <li>Хуки от телеграмм бота</li>
                <li>Хуки для обработки ответов от робокассы</li>
            </ul>
        </div>
        <p>Текущее время сервера: {current_time}</p>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')


async def robokassa_result(request: web.Request) -> web.Response:
    """
    Обрабатывает запрос от Робокассы на ResultURL.

    Args:
        request (web.Request): HTTP-запрос.

    Returns:
        web.Response: Текстовый ответ с результатами проверки.

    Raises:
        Exception: Если возникает ошибка при обработке данных или проверке подписи.

    Example:
        >>> from aiohttp import web
        >>> request = web.Request(method='POST', url='/robokassa_result', app=web.Application())
        >>> response = await robokassa_result(request)
        >>> print(response.status)
        200
    """
    logger.success("Получен ответ от Робокассы!")
    data = await request.post()

    # Извлекаем параметры из запроса
    signature = data.get('SignatureValue')
    out_sum = data.get('OutSum')
    inv_id = data.get('InvId')
    user_id = data.get('Shp_user_id')
    user_telegram_id = data.get('Shp_user_telegram_id')
    product_id = data.get('Shp_product_id')

    # Проверяем подпись
    if check_signature_result(
        out_sum=out_sum,
        inv_id=inv_id,
        received_signature=signature,
        password=settings.MRH_PASS_2,
        user_id=user_id,
        user_telegram_id=user_telegram_id,
        product_id=product_id
    ):
        result = f"OK{inv_id}"
        logger.info(f"Успешная проверка подписи для InvId: {inv_id}")

        payment_data = {
            'user_id': int(user_id),
            'payment_id': signature,
            'price': int(out_sum),
            'product_id': int(product_id),
            'payment_type': "robocassa"
        }
        async with async_session_maker() as session:
            await successful_payment_logic(
                session=session,
                payment_data=payment_data,
                currency="₽",
                user_tg_id=int(user_telegram_id),
                bot=bot
            )
            await session.commit()
    else:
        result = "bad sign"
        logger.warning(f"Неверная подпись для InvId: {inv_id}")

    logger.info(f"Ответ: {result}")
    return web.Response(text=result)


async def robokassa_fail(request: web.Request) -> web.Response:
    """
    Обрабатывает запрос при неудачном платеже через Robokassa.

    Args:
        request (web.Request): HTTP-запрос.

    Returns:
        web.Response: HTTP-ответ с информацией о неудачном платеже.

    Example:
        >>> from aiohttp import web
        >>> request = web.Request(method='GET', url='/robokassa_fail?InvId=123&OutSum=100', app=web.Application())
        >>> response = await robokassa_fail(request)
        >>> print(response.status)
        200
    """
    # Получаем параметры из GET-запроса
    inv_id = request.query.get('InvId')
    out_sum = request.query.get('OutSum')
    print(f"Неудачный платеж: сумма {out_sum}, ID {inv_id}")
    return web.Response(text="Платеж не удался", content_type='text/html')