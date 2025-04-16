## \\file /src/endpoints/bots/telegram/webhooks.py

# Модуль вебхуков Telegram

```rst
.. module:: src.endpoints.bots.telegram.webhooks
    :platform: Windows, Unix
    :synopsis: Функции вебхуков Телеграма

```

Этот модуль содержит функции для обработки входящих вебхуков от Telegram.

## Обзор

Модуль `src.endpoints.bots.telegram.webhooks` предоставляет функции для обработки входящих вебхуков от Telegram, используя FastAPI и библиотеку `python-telegram-bot`.

## Функции

### `telegram_webhook`

```python
def telegram_webhook(request: Request, application: Application):
```

**Назначение**: Обрабатывает входящие запросы вебхуков (синхронная обертка для асинхронной функции).

**Параметры**:

*   `request` (Request): Объект запроса FastAPI.
*   `application` (Application): Экземпляр класса `telegram.ext.Application`.

**Как работает функция**:

1.  Запускает асинхронную функцию `telegram_webhook_async` с использованием `asyncio.run`.

### `telegram_webhook_async`

```python
async def telegram_webhook_async(request: Request, application: Application):
```

**Назначение**: Асинхронно обрабатывает входящие запросы вебхуков.

**Параметры**:

*   `request` (Request): Объект запроса FastAPI.
*   `application` (Application): Экземпляр класса `telegram.ext.Application`.

**Возвращает**:

*   `Response`: Объект ответа FastAPI.

**Как работает функция**:

1.  Пытается извлечь данные из JSON-тела запроса.
2.  Преобразует данные в объект `Update` с использованием `Update.de_json`.
3.  Обрабатывает обновление, используя `application.process_update`.
4.  В случае успеха возвращает объект `Response` с кодом состояния 200.
5.  В случае ошибки декодирования JSON возвращает объект `Response` с кодом состояния 400 и сообщением об ошибке.
6.  В случае других ошибок возвращает объект `Response` с кодом состояния 500 и сообщением об ошибке.