### Как использовать класс `TelegramBot`
=========================================================================================

Описание
-------------------------
Класс `TelegramBot` представляет собой интерфейс для взаимодействия с Telegram ботом. Он инициализирует бота, регистрирует обработчики команд и сообщений, а также предоставляет методы для управления обработчиками сообщений.

Шаги выполнения
-------------------------
1. **Инициализация бота**: Создается экземпляр класса `TelegramBot` с указанием токена бота.
2. **Регистрация обработчиков**: В конструкторе класса вызывается метод `register_handlers`, который регистрирует обработчики для команд `/start`, `/help`, `/sendpdf`, текстовых сообщений, голосовых сообщений и документов.
3. **Замена обработчика сообщений**: При необходимости можно заменить текущий обработчик текстовых сообщений на новый с помощью метода `replace_message_handler`.
4. **Запуск бота**: Для запуска бота необходимо вызвать метод `start_polling` у объекта `application`.

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.bots.telegram.bot_long_polling import TelegramBot
from telegram import Update
from telegram.ext import CallbackContext

# 1. Инициализация бота
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Замените на токен вашего бота
bot = TelegramBot(TOKEN)

# 2. Пример замены обработчика сообщений
async def new_message_handler(update: Update, context: CallbackContext) -> None:
    """Новый обработчик сообщений."""
    await update.message.reply_text("Это новый обработчик сообщений!")

bot.replace_message_handler(new_message_handler)

# 3. Пример запуска бота (необязательно, если бот запускается в другом месте)
async def main():
    await bot.application.initialize()
    await bot.application.start_polling()
    await bot.application.idle()

if __name__ == '__main__':
    asyncio.run(main())