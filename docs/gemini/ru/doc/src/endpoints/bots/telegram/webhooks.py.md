# Модуль обработки вебхуков Telegram

## Обзор

Этот модуль предназначен для обработки входящих вебхуков от Telegram через сервер FastAPI. Он использует библиотеку `telegram.ext` для интеграции с Telegram Bot API и асинхронные функции для эффективной обработки запросов.

## Подробнее

Модуль содержит функции для приема и обработки входящих вебхуков от Telegram. Вебхук позволяет Telegram боту получать обновления в реальном времени, отправляя HTTP POST запросы на указанный URL. Этот модуль обрабатывает эти запросы, преобразует их в объекты `Update` из библиотеки `telegram`, и передает их на обработку в приложение Telegram.

## Функции

### `telegram_webhook`

**Назначение**: Обрабатывает входящие вебхуки Telegram (синхронная обертка для асинхронной функции).

```python
def telegram_webhook(request: Request, application: Application):
    """
    Args:
        request (Request): Объект запроса FastAPI.
        application (Application): Объект приложения telegram.ext.
    """
    asyncio.run(telegram_webhook_async(request, application))
```

**Параметры**:
- `request` (Request): Объект запроса FastAPI, содержащий данные от Telegram.
- `application` (Application): Объект приложения `telegram.ext`, используемый для обработки обновлений.

**Возвращает**:
- None: Функция не возвращает значения напрямую, но запускает асинхронную обработку вебхука.

**Как работает функция**:
- Функция `telegram_webhook` является синхронной оберткой для асинхронной функции `telegram_webhook_async`. Она использует `asyncio.run` для запуска асинхронной функции в синхронном контексте. Это необходимо, поскольку FastAPI может вызывать эту функцию синхронно.

**Примеры**:
```python
# Пример использования функции в FastAPI (необходим ASGI сервер, например, uvicorn)
# @app.post("/telegram_webhook")
# async def webhook(request: Request):
#     return telegram_webhook(request, application)
```

---

### `telegram_webhook_async`

**Назначение**: Асинхронно обрабатывает входящие вебхуки Telegram.

```python
async def telegram_webhook_async(request: Request, application: Application):
    """Handle incoming webhook requests."""
    return request

    try:
        data = await request.json()
        async with application:
            update = Update.de_json(data, application.bot)
            await application.process_update(update)
        return Response(status_code=200)
    except json.JSONDecodeError as ex:
        logger.error(f'Error decoding JSON: ', ex)
        return Response(status_code=400, content=f'Invalid JSON: {ex}')
    except Exception as ex:
        logger.error(f'Error processing webhook: {type(ex)} - {ex}')
        return Response(status_code=500, content=f'Error processing webhook: {ex}')
```

**Параметры**:
- `request` (Request): Объект запроса FastAPI, содержащий данные от Telegram.
- `application` (Application): Объект приложения `telegram.ext`, используемый для обработки обновлений.

**Возвращает**:
- `Response`: Объект ответа FastAPI с кодом состояния 200 в случае успешной обработки, 400 в случае ошибки разбора JSON, и 500 в случае общей ошибки.

**Как работает функция**:

1.  **Извлечение данных**: Извлекает JSON-данные из объекта запроса `request`.
2.  **Обработка данных**:
    *   Использует `application.bot` для преобразования JSON-данных в объект `Update`.
    *   Запускает обработку обновления с помощью `application.process_update(update)`.
3.  **Обработка ошибок**:
    *   В случае ошибки декодирования JSON возвращает ответ с кодом состояния 400 и сообщением об ошибке.
    *   В случае любой другой ошибки возвращает ответ с кодом состояния 500 и сообщением об ошибке.
4.  **Логирование**:
    *   При возникновении `json.JSONDecodeError` логирует ошибку, используя `logger.error`.
    *   При возникновении других исключений логирует ошибку, используя `logger.error`, и включает информацию об исключении (`exc_info=True`).

**Примеры**:

```python
# Пример использования функции в FastAPI
# @app.post("/telegram_webhook")
# async def webhook(request: Request):
#     return await telegram_webhook_async(request, application)
```