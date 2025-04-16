# Модуль Telegram-бота с использованием Pyrogram

## Обзор

Модуль `src.endpoints.bots.telegram.bot_pyogram` представляет собой Telegram-бота, реализованного с использованием библиотеки Pyrogram.

## Подробней

Модуль предоставляет функциональность для эхо-ответа на текстовые сообщения и обработки команды `/start`.

## Переменные

*   `API_ID` (int): ID API Telegram.
*   `API_HASH` (str): Хэш API Telegram.
*   `BOT_TOKEN` (str): Токен Telegram-бота.
*   `app` (Client): Экземпляр клиента Pyrogram.

## Функции

### `start_command`

```python
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Привет! Я простой бот на Pyrogram.")
```

**Назначение**: Обрабатывает команду `/start`.

**Как работает функция**:

1.  Отправляет приветственное сообщение пользователю.

### `echo_message`

```python
@app.on_message(filters.text & ~filters.command)
def echo_message(client, message):
    message.reply_text(message.text)
```

**Назначение**: Обрабатывает все текстовые сообщения (кроме команд).

**Как работает функция**:

1.  Отправляет пользователю сообщение, повторяющее его текст.

### `__main__`

```python
if __name__ == "__main__":
    print("Бот запущен...")
    app.run()
```

**Назначение**: Запускает Telegram-бота.

**Как работает функция**:

1.  Выводит сообщение о запуске бота.
2.  Запускает бота, используя метод `app.run`.

## Использование

Для запуска бота необходимо:

1.  Установить библиотеку Pyrogram: `pip install pyrogram`.
2.  Получить `API_ID`, `API_HASH` и `BOT_TOKEN` от BotFather в Telegram.
3.  Задать переменные окружения `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` и `TELEGRAM_TOKEN`.
4.  Запустить файл `bot_pyogram.py`.

После запуска бот будет доступен в Telegram, и пользователи смогут взаимодействовать с ним, отправляя команды и текстовые сообщения.