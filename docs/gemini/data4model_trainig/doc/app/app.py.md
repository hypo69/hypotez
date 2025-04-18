# Модуль обработки вебхуков и платежей

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.app.app` предназначен для обработки вебхуков Telegram-бота и запросов от платежной системы Robokassa.

## Подробней

Модуль содержит функции для обработки входящих вебхуков Telegram, отображения главной страницы и обработки результатов платежей Robokassa.

## Функции

### `handle_webhook`

```python
async def handle_webhook(request: web.Request):
```

**Назначение**: Обрабатывает входящие запросы вебхуков от Telegram.

**Параметры**:

*   `request` (web.Request): Объект запроса aiohttp.

**Возвращает**:

*   `web.Response`: Объект ответа aiohttp.

**Как работает функция**:

1.  Извлекает данные из JSON-тела запроса.
2.  Преобразует данные в объект `Update` с использованием `Update.de_json`.
3.  Обрабатывает обновление с использованием `dp.feed_update`.
4.  В случае успеха возвращает объект `Response` с кодом состояния 200.
5.  В случае ошибки логирует информацию об ошибке и возвращает объект `Response` с кодом состояния 500.

### `home_page`

```python
async def home_page(request: web.Request) -> web.Response:
```

**Назначение**: Обрабатывает запрос на эндпоинт "Hello, World!".

**Параметры**:

*   `request` (web.Request): Объект запроса aiohttp.

**Возвращает**:

*   `web.Response`: Объект ответа aiohttp с HTML-содержимым.

**Как работает функция**:

1.  Получает текущее время сервера.
2.  Формирует HTML-содержимое с информацией о сервисе и текущем времени.
3.  Возвращает объект `Response` с HTML-содержимым.

### `robokassa_result`

```python
async def robokassa_result(request: web.Request) -> web.Response:
```

**Назначение**: Обрабатывает запрос от Робокассы на ResultURL.

**Параметры**:

*   `request` (web.Request): HTTP-запрос.

**Возвращает**:

*   `web.Response`: Текстовый ответ с результатами проверки.

**Как работает функция**:

1.  Извлекает параметры из POST-запроса.
2.  Проверяет подпись запроса, используя функцию `check_signature_result`.
3.  Если подпись верна:
    *   Формирует текст ответа "OK{InvId}".
    *   Логирует информацию об успешной проверке подписи.
    *   Вызывает функцию `successful_payment_logic` для обработки данных платежа.
4.  Если подпись неверна:

    *   Формирует текст ответа "bad sign".
    *   Логирует информацию о неверной подписи.
5.  Возвращает объект `web.Response` с текстом ответа.

### `robokassa_fail`

```python
async def robokassa_fail(request):
```

**Назначение**: Обрабатывает запрос от Робокассы при неудачном платеже.

**Параметры**:

*   `request`: HTTP-запрос.

**Возвращает**:

*   `web.Response`: Текстовый ответ с информацией о неудачном платеже.

**Как работает функция**:

1.  Получает параметры из GET-запроса.
2.  Выводит информацию о неудачном платеже в консоль.
3.  Возвращает объект `web.Response` с текстом "Платеж не удался".