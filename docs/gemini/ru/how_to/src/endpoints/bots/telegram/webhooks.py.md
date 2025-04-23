### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Данный блок кода содержит функции для обработки входящих вебхуков от Telegram через сервер FastAPI. Функция `telegram_webhook` является синхронной оберткой для асинхронной функции `telegram_webhook_async`, которая обрабатывает данные, полученные от Telegram, и передает их для дальнейшей обработки в приложение Telegram Bot.

Шаги выполнения
-------------------------
1. **Прием запроса**: Функция `telegram_webhook_async` принимает объект `Request` от FastAPI, содержащий данные вебхука.
2. **Извлечение данных**: Извлекаются JSON данные из запроса с использованием `await request.json()`.
3. **Обработка данных**:
   - Создается объект `Update` из полученных JSON данных с использованием `Update.de_json(data, application.bot)`. Этот объект представляет собой обновление от Telegram.
   -  `process_update` запускает обработку обновления с помощью `await application.process_update(update)`.
4. **Обработка ошибок**:
   - Если при декодировании JSON возникает ошибка (`json.JSONDecodeError`), функция логирует ошибку и возвращает HTTP-ответ с кодом 400 (Bad Request).
   - Если возникает любая другая ошибка, функция логирует ошибку и возвращает HTTP-ответ с кодом 500 (Internal Server Error).
5. **Отправка ответа**: В случае успешной обработки функция возвращает HTTP-ответ с кодом 200 (OK).

Пример использования
-------------------------

```python
import asyncio
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application
import json
from src.logger import logger

app = FastAPI()

# Инициализация приложения Telegram Bot (пример)
# TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# bot = Application.builder().token(TOKEN).build()

# async def echo(update: Update, context):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# bot.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

@app.post("/telegram_webhook")
async def handle_webhook(request: Request):
    """
    Обрабатывает входящие webhook запросы от Telegram.
    """
    # await telegram_webhook_async(request, bot)
    try:
        data = await request.json()
        # async with application:
        #     update = Update.de_json(data, application.bot)
        #     await application.process_update(update)
        return Response(status_code=200)
    except json.JSONDecodeError as ex:
        logger.error(f'Error decoding JSON: ', ex)
        return Response(status_code=400, content=f'Invalid JSON: {ex}')
    except Exception as ex:
        logger.error(f'Error processing webhook: {type(ex)} - {ex}')
        return Response(status_code=500, content=f'Error processing webhook: {ex}')
```