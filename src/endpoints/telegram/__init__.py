from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Обработчик входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # Выводим в консоль
    print(f"Сообщение от пользователя: {user_text}")
    print(f"Chat ID: {chat_id}")

    # Отправляем ответ пользователю
    await update.message.reply_text(f"Ты написал: '{user_text}'\nТвой chat_id: {chat_id}")

# Основная функция запуска
def main():
    app = ApplicationBuilder().token("ХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХХ").build()

    # Обрабатываем любые текстовые сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен. Нажми Ctrl+C для выхода.")
    app.run_polling()

if __name__ == "__main__":
    main()
