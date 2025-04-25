## Как использовать вебхук Телеграма через FastAPI
=========================================================================================

Описание
-------------------------
Данный код реализует вебхук для Телеграм-бота, работающий через сервер FastAPI. Он принимает JSON-данные от Телеграма, обрабатывает их в виде `Update`-объекта и передает их в приложение `Application` для дальнейшего обработки.

Шаги выполнения
-------------------------
1. **Принимает входящий запрос**: Получает JSON-данные от Телеграм-бота через вебхук.
2. **Преобразует данные в объект `Update`**: Декодирует полученные JSON-данные в `Update`-объект, который используется для работы с ботом.
3. **Обрабатывает обновление**: Передает полученный `Update`-объект в `Application` для обработки ботом.
4. **Возвращает ответ**: Возвращает HTTP-ответ с кодом 200, подтверждая успешную обработку вебхука.
5. **Обработка ошибок**: Логирует ошибки декодирования JSON и обработки вебхука, возвращая соответствующие HTTP-ответы с кодами 400 и 500.

Пример использования
-------------------------

```python
from fastapi import FastAPI
from telegram.ext import Application, CommandHandler
from src.endpoints.bots.telegram.webhooks import telegram_webhook_async

# Создание приложения FastAPI
app = FastAPI()

# Создание приложения Телеграма
application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

# Регистрация обработчика команды /start
application.add_handler(CommandHandler("start", start_command))

# Маршрут для обработки вебхука
@app.post("/webhook")
async def handle_webhook(request: Request):
    return await telegram_webhook_async(request, application)

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Описание функций:**

* **`telegram_webhook(request: Request, application: Application)`**:
    - Декоратор `asyncio.run()` запускает асинхронную функцию `telegram_webhook_async()`.
* **`telegram_webhook_async(request: Request, application: Application)`**:
    - Принимает входящий запрос `request` от FastAPI и `application` - объект Telegram Application.
    - Декодирует JSON-данные из запроса и создает объект `Update` для Telegram.
    - Передает обновление `Update` в приложение `application` для обработки.
    - Возвращает HTTP-ответ с кодом 200, подтверждая успешную обработку запроса.
    - Логирует ошибки, возникающие во время декодирования JSON и обработки запроса.
* **`start_command(update: Update, context: CallbackContext)`**:
    - Определяет команду `/start` для Telegram-бота, которую можно использовать для запуска бота.
    - При обработке команды, отправляет сообщение пользователю, приветствуя его. 

**Важно:**

* Убедитесь, что вы заменили `"YOUR_TELEGRAM_BOT_TOKEN"` на ваш реальный токен Telegram-бота.
* Настройте вебхук в Telegram BotFather, указав URL вашего сервера FastAPI и путь к обработчику вебхука (`/webhook`).
* Убедитесь, что ваш сервер FastAPI доступен по указанному URL.
* Используйте функцию `telegram_webhook_async()` для обработки входящих запросов от Телеграма.
* Используйте объект `application` для обработки `Update`-объектов и управления ботом.