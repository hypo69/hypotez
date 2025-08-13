from pyrogram import Client, filters
import os

# Replace with your values
API_ID = int(os.environ.get("TELEGRAM_API_ID",''))
API_HASH = os.environ.get("TELEGRAM_API_HASH",'')
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN",'')


# Creation of a client of the client Pyrogram
app = Client(
    "my_simple_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Team handler /Start
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Привет! Я простой бот на Pyrogram.")

# Processor of all text messages (except commands)
@app.on_message(filters.text & ~filters.command)
def echo_message(client, message):
    message.reply_text(message.text)

# Launch of the bot
if __name__ == "__main__":
    print("Бот запущен...")
    app.run()