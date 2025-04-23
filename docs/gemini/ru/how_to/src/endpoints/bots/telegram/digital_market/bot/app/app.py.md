Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода содержит набор функций для обработки HTTP-запросов в aiohttp-приложении, включая обработку вебхуков от Telegram, отображение главной страницы и обработку ответов от Robokassa.

Шаги выполнения
-------------------------
1. **Обработка вебхука от Telegram (`handle_webhook`)**:
   - Функция принимает `request: web.Request` в качестве аргумента.
   - Извлекает `update` из JSON тела запроса.
   - Передает `update` в `dp.feed_update(bot, update)` для обработки ботом.
   - Возвращает `web.Response` со статусом 200 в случае успеха или 500 в случае ошибки.

2. **Отображение главной страницы (`home_page`)**:
   - Функция принимает `request: web.Request` в качестве аргумента.
   - Генерирует HTML-контент с информацией о сервисе и текущем времени сервера.
   - Возвращает `web.Response` с HTML-контентом и типом `text/html`.

3. **Обработка ответа от Robokassa (`robokassa_result`)**:
   - Функция принимает `request: web.Request` в качестве аргумента.
   - Извлекает параметры из POST-запроса: `signature`, `out_sum`, `inv_id`, `user_id`, `user_telegram_id`, `product_id`.
   - Проверяет подпись с использованием функции `check_signature_result`.
   - Если подпись верна, формирует данные о платеже `payment_data` и вызывает `successful_payment_logic` для обработки успешного платежа.
   - Возвращает `web.Response` с результатом проверки подписи (`OK{inv_id}` или `"bad sign"`).

4. **Обработка неудачного платежа Robokassa (`robokassa_fail`)**:
   - Функция принимает `request: web.Request` в качестве аргумента.
   - Извлекает параметры `InvId` и `OutSum` из GET-запроса.
   - Выводит информацию о неудачном платеже в консоль.
   - Возвращает `web.Response` с сообщением о неудаче платежа и типом `text/html`.

Пример использования
-------------------------

```python
from aiohttp import web
import asyncio
from bot.app.app import handle_webhook, home_page, robokassa_result, robokassa_fail

async def main():
    app = web.Application()
    app.add_routes([
        web.post('/telegram_webhook', handle_webhook),
        web.get('/', home_page),
        web.post('/robokassa_result', robokassa_result),
        web.get('/robokassa_fail', robokassa_fail),
    ])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())