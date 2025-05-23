## Как использовать бот на Pyrogram
=========================================================================================

Описание
-------------------------
Данный код демонстрирует создание простого бота в Telegram с использованием библиотеки Pyrogram. Бот реагирует на команду `/start` и пересылает текстовые сообщения обратно пользователю.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей:**
    - `pyrogram` для взаимодействия с Telegram API
    - `os` для работы с переменными окружения
2. **Настройка переменных окружения:**
    - Задайте значения для `API_ID`, `API_HASH` и `BOT_TOKEN`, которые необходимы для аутентификации бота в Telegram.
3. **Создание экземпляра клиента Pyrogram:**
    - Создайте объект `Client` с именем "my_simple_bot" и используйте полученные значения для `api_id`, `api_hash` и `bot_token`.
4. **Определение обработчика команды `/start`:**
    - Используя декоратор `@app.on_message` с фильтром `filters.command("start")`, создайте функцию `start_command`, которая будет вызываться при получении команды `/start`.
    - Функция `start_command` отвечает на сообщение пользователя текстом "Привет! Я простой бот на Pyrogram.".
5. **Определение обработчика текстовых сообщений:**
    - Используя декоратор `@app.on_message` с фильтром `filters.text & ~filters.command`, создайте функцию `echo_message`, которая будет вызываться при получении текстового сообщения, не являющегося командой.
    - Функция `echo_message` пересылает полученное сообщение обратно пользователю.
6. **Запуск бота:**
    - В блоке `if __name__ == "__main__":` выводится сообщение "Бот запущен..." и запускается метод `app.run()`, который начинает работу бота.

Пример использования
-------------------------

```python
# Замените на свои значения
API_ID = int(os.environ.get("TELEGRAM_API_ID", ''))
API_HASH = os.environ.get("TELEGRAM_API_HASH", '')
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN", '')

# Создаем экземпляр клиента Pyrogram
app = Client(
    "my_simple_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Обработчик команды /start
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Привет! Я простой бот на Pyrogram.")

# Обработчик всех текстовых сообщений (кроме команд)
@app.on_message(filters.text & ~filters.command)
def echo_message(client, message):
    message.reply_text(message.text)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    app.run()
```

**Замечания:**

- Перед запуском бота убедитесь, что вы установили переменные окружения с правильными значениями для `API_ID`, `API_HASH` и `BOT_TOKEN`.
- Для получения `API_ID` и `API_HASH`  зарегистрируйтесь на сайте https://my.telegram.org/auth.
- Для получения `BOT_TOKEN` создайте нового бота в Telegram.