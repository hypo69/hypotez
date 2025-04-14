### **Анализ кода модуля `app.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/app/app.py

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `logger` для логирования.
    - Обработка исключений в `handle_webhook`.
    - Понятная структура обработчиков HTTP-запросов.
    - Использование асинхронности (`async` и `await`).
- **Минусы**:
    - Отсутствуют аннотации типов для параметров функций `robokassa_fail`.
    - `print` вместо `logger.info` в функции `robokassa_fail`.
    - Не все переменные аннотированы типами.

#### **Рекомендации по улучшению**:

1. **Добавить аннотации типов**:
   - Добавить аннотации типов для параметров функций, например, в `robokassa_fail`.
   - Добавить аннотации для всех переменных.

2. **Улучшить логирование**:
   - Заменить `print` на `logger.info` в функции `robokassa_fail`.
   - Добавить более информативные сообщения в логи.

3. **Улучшить docstring**:
   - Перевести docstring на русский язык.
   - Добавить более подробное описание работы каждой функции.

4. **Оптимизировать обработку данных**:
   - Явное преобразование типов для параметров, полученных из запроса, чтобы избежать ошибок.

#### **Оптимизированный код**:

```python
import datetime

from aiohttp import web
from aiogram.types import Update
from loguru import logger

from bot.app.utils import check_signature_result
from bot.config import bot, dp, settings
from bot.dao.database import async_session_maker
from bot.user.utils import successful_payment_logic


async def handle_webhook(request: web.Request) -> web.Response:
    """
    Обрабатывает входящий вебхук от Telegram.

    Args:
        request (web.Request): Объект HTTP-запроса от aiohttp.

    Returns:
        web.Response: HTTP-ответ с кодом 200 в случае успеха или 500 в случае ошибки.
    """
    try:
        update: Update = Update(**await request.json())  # Преобразует JSON-данные запроса в объект Update
        await dp.feed_update(bot, update)  # Передает обновление в диспетчер бота
        return web.Response(status=200)  # Возвращает успешный HTTP-ответ
    except Exception as ex:
        logger.error('Ошибка при обработке вебхука', ex, exc_info=True)  # Логирует ошибку
        return web.Response(status=500)  # Возвращает HTTP-ответ с кодом ошибки


async def home_page(request: web.Request) -> web.Response:
    """
    Отображает главную страницу с информацией о сервисе.

    Args:
        request (web.Request): Объект HTTP-запроса от aiohttp.

    Returns:
        web.Response: HTTP-ответ с HTML-содержимым главной страницы.
    """
    current_time: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Получает текущее время

    html_content: str = f"""
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
    return web.Response(text=html_content, content_type='text/html')  # Возвращает HTML-ответ


async def robokassa_result(request: web.Request) -> web.Response:
    """
    Обрабатывает результат от Робокассы после проведения платежа.

    Args:
        request (web.Request): Объект HTTP-запроса от aiohttp.

    Returns:
        web.Response: HTTP-ответ с результатом проверки подписи.
    """
    logger.success('Получен ответ от Робокассы!')  # Логирует получение ответа
    data: dict = await request.post()  # Получает данные из POST-запроса

    signature: str | None = data.get('SignatureValue')  # Извлекает подпись
    out_sum: str | None = data.get('OutSum')  # Извлекает сумму платежа
    inv_id: str | None = data.get('InvId')  # Извлекает ID платежа
    user_id: str | None = data.get('Shp_user_id')  # Извлекает ID пользователя
    user_telegram_id: str | None = data.get('Shp_user_telegram_id')  # Извлекает ID пользователя в Telegram
    product_id: str | None = data.get('Shp_product_id')  # Извлекает ID продукта

    if check_signature_result(  # Проверяет подпись
        out_sum=out_sum,
        inv_id=inv_id,
        received_signature=signature,
        password=settings.MRH_PASS_2,
        user_id=user_id,
        user_telegram_id=user_telegram_id,
        product_id=product_id
    ):
        result: str = f'OK{inv_id}'  # Формирует успешный ответ
        logger.info(f'Успешная проверка подписи для InvId: {inv_id}')  # Логирует успешную проверку

        payment_data: dict = {  # Формирует данные о платеже
            'user_id': int(user_id),
            'payment_id': signature,
            'price': int(out_sum),
            'product_id': int(product_id),
            'payment_type': 'robocassa'
        }
        async with async_session_maker() as session:  # Создает асинхронную сессию
            await successful_payment_logic(  # Выполняет логику успешного платежа
                session=session,
                payment_data=payment_data,
                currency='₽',
                user_tg_id=int(user_telegram_id),
                bot=bot
            )
            await session.commit()  # Применяет изменения в базе данных
    else:
        result: str = 'bad sign'  # Формирует ответ о неудачной проверке
        logger.warning(f'Неверная подпись для InvId: {inv_id}')  # Логирует неудачную проверку

    logger.info(f'Ответ: {result}')  # Логирует ответ
    return web.Response(text=result)  # Возвращает HTTP-ответ


async def robokassa_fail(request: web.Request) -> web.Response:
    """
    Обрабатывает ситуацию неуспешной оплаты через Робокассу.

    Args:
        request (web.Request): Объект HTTP-запроса от aiohttp.

    Returns:
        web.Response: HTTP-ответ с сообщением об ошибке.
    """
    inv_id: str | None = request.query.get('InvId')  # Получает ID платежа из параметров запроса
    out_sum: str | None = request.query.get('OutSum')  # Получает сумму платежа из параметров запроса
    logger.info(f'Неудачный платеж: сумма {out_sum}, ID {inv_id}')  # Логирует информацию о неудачном платеже
    return web.Response(text='Платеж не удался', content_type='text/html')  # Возвращает HTTP-ответ