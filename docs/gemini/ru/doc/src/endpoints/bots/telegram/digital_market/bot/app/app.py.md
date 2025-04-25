# Модуль для обработки вебхуков и запросов от Робокассы

## Обзор

Модуль содержит набор обработчиков для различных вебхуков и запросов, в том числе:

- Обработчик вебхуков от Telegram бота.
- Обработчик запросов от Робокассы для ResultURL.
- Обработчик запросов от Робокассы для FailURL.
- Функция для отображения главной страницы (Hello, World!).

## Подробнее

### Обработчики вебхуков и запросов:

- `handle_webhook`: Обрабатывает webhook-запросы от Telegram бота.
- `robokassa_result`: Обрабатывает запрос от Робокассы на ResultURL.
- `robokassa_fail`: Обрабатывает запрос от Робокассы на FailURL.

### Главная страница:

- `home_page`: Отображает главную страницу с информацией о сервисе.

## Функции

### `handle_webhook`

**Назначение**: Обрабатывает webhook-запросы от Telegram бота.

**Параметры**:

- `request (web.Request)`: HTTP-запрос.

**Возвращает**:

- `web.Response`: HTTP-ответ с кодом 200 (успешно) или 500 (ошибка).

**Пример**:

```python
from aiohttp import web
from aiogram.types import Update

# ...

async def handle_webhook(request: web.Request):
    try:
        update = Update(**await request.json())
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {e}")
        return web.Response(status=500)
```

**Как работает функция**:

- Получает данные из тела HTTP-запроса в формате JSON.
- Преобразует полученные данные в объект `Update` библиотеки `aiogram`.
- Передает полученный объект `Update` в обработчик обновлений Telegram бота `dp.feed_update`.
- Возвращает HTTP-ответ с кодом 200 (успешно).
- Если возникает ошибка, функция логгирует ее и возвращает HTTP-ответ с кодом 500 (ошибка).

### `home_page`

**Назначение**: Отображает главную страницу с информацией о сервисе.

**Параметры**:

- `request (web.Request)`: HTTP-запрос.

**Возвращает**:

- `web.Response`: HTTP-ответ с HTML-содержимым.

**Пример**:

```python
from aiohttp import web
import datetime

# ...

async def home_page(request: web.Request) -> web.Response:
    """
    Обработчик для отображения главной страницы с информацией о сервисе.
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
```

**Как работает функция**:

- Формирует HTML-контент с информацией о сервисе и текущем времени.
- Возвращает HTTP-ответ с сгенерированным HTML-контентом.

### `robokassa_result`

**Назначение**: Обрабатывает запрос от Робокассы на ResultURL.

**Параметры**:

- `request (web.Request)`: HTTP-запрос.

**Возвращает**:

- `web.Response`: HTTP-ответ с текстовым сообщением (OK{inv_id} - успешная проверка подписи, bad sign - неверная подпись).

**Пример**:

```python
from aiohttp import web
from bot.app.utils import check_signature_result
from bot.config import settings
from bot.dao.database import async_session_maker
from bot.user.utils import successful_payment_logic

# ...

async def robokassa_result(request: web.Request) -> web.Response:
    """
    Обрабатывает запрос от Робокассы на ResultURL.

    :param request: HTTP-запрос
    :return: Текстовый ответ с результатами проверки
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
```

**Как работает функция**:

- Получает данные из тела HTTP-запроса от Робокассы.
- Извлекает необходимые параметры из запроса: `signature`, `out_sum`, `inv_id`, `user_id`, `user_telegram_id`, `product_id`.
- Проверяет подпись запроса с помощью функции `check_signature_result`.
- Если подпись верна, сохраняет информацию о платеже в базу данных и возвращает "OK{inv_id}".
- Если подпись неверна, возвращает "bad sign".

### `robokassa_fail`

**Назначение**: Обрабатывает запрос от Робокассы на FailURL.

**Параметры**:

- `request (web.Request)`: HTTP-запрос.

**Возвращает**:

- `web.Response`: HTTP-ответ с текстовым сообщением "Платеж не удался".

**Пример**:

```python
from aiohttp import web

# ...

async def robokassa_fail(request):
    # Получаем параметры из GET-запроса
    inv_id = request.query.get('InvId')
    out_sum = request.query.get('OutSum')
    print(f"Неудачный платеж: сумма {out_sum}, ID {inv_id}")
    return web.Response(text="Платеж не удался", content_type='text/html')
```

**Как работает функция**:

- Получает параметры `inv_id` и `out_sum` из GET-запроса.
- Выводит сообщение о неудачном платеже в консоль.
- Возвращает HTTP-ответ с текстовым сообщением "Платеж не удался".

## Внутренние функции

### `check_signature_result`

**Назначение**: Проверяет подпись запроса от Робокассы.

**Параметры**:

- `out_sum (str)`: Сумма платежа.
- `inv_id (str)`: ID платежа.
- `received_signature (str)`: Полученная подпись.
- `password (str)`: Пароль для проверки подписи.
- `user_id (str)`: ID пользователя.
- `user_telegram_id (str)`: Telegram ID пользователя.
- `product_id (str)`: ID товара.

**Возвращает**:

- `bool`: `True` - подпись верна, `False` - подпись неверна.

**Как работает функция**:

- Формирует строку для проверки подписи с использованием предоставленных параметров.
- Сравнивает полученную подпись с рассчитанной.
- Возвращает `True`, если подписи совпадают, и `False` в противном случае.

## Параметры

### `bot`

- **Описание**: Экземпляр бота Telegram.

### `dp`

- **Описание**: Обработчик обновлений Telegram бота.

### `settings`

- **Описание**: Объект с конфигурационными настройками приложения.

### `async_session_maker`

- **Описание**: Функция для создания асинхронной сессии базы данных.