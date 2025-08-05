# Модуль telegram_bot_trainger

## Обзор

Модуль предоставляет функциональность для создания и управления Telegram-ботом, способным обрабатывать текстовые и голосовые сообщения, а также документы. Бот использует библиотеку `python-telegram-bot` для взаимодействия с Telegram API и модель `Model` из модуля `src.llm.openai.model.training` для обработки сообщений.

## Подробней

Этот модуль позволяет создать простого Telegram-бота, который может отвечать на текстовые и голосовые сообщения, а также обрабатывать текстовые файлы, обучая на них модель. Он использует `python-telegram-bot` для обработки входящих сообщений и команд, а также модуль `src.llm.openai.model.training` для отправки сообщений и обучения модели.

## Классы

В данном модуле не реализованы отдельные классы.

## Функции

### `start`

```python
async def start(update: Update, context: CallbackContext) -> None:
    """ Handle the /start command."""
    await update.message.reply_text('Hello! I am your simple bot. Type /help to see available commands.')
```

**Назначение**:
Обрабатывает команду `/start`, отправляя приветственное сообщение пользователю.

**Параметры**:
- `update` (Update): Объект, представляющий входящее обновление от Telegram.
- `context` (CallbackContext): Объект, содержащий информацию о контексте обработчика.

**Возвращает**:
- `None`

**Как работает функция**:
Функция `start` отправляет текстовое сообщение в ответ на команду `/start`, используя метод `reply_text` объекта `update.message`. Сообщение содержит приветствие и инструкцию для пользователя.

**Примеры**:
```python
# Пример вызова функции start
# При вызове команды /start бот ответит приветственным сообщением
```

### `help_command`

```python
async def help_command(update: Update, context: CallbackContext) -> None:
    """ Handle the /help command."""
    await update.message.reply_text('Available commands:\\n/start - Start the bot\\n/help - Show this help message')
```

**Назначение**:
Обрабатывает команду `/help`, отправляя пользователю список доступных команд.

**Параметры**:
- `update` (Update): Объект, представляющий входящее обновление от Telegram.
- `context` (CallbackContext): Объект, содержащий информацию о контексте обработчика.

**Возвращает**:
- `None`

**Как работает функция**:
Функция `help_command` отправляет текстовое сообщение в ответ на команду `/help`, используя метод `reply_text` объекта `update.message`. Сообщение содержит список доступных команд и их описание.

**Примеры**:
```python
# Пример вызова функции help_command
# При вызове команды /help бот ответит списком доступных команд
```

### `handle_document`

```python
async def handle_document(update: Update, context: CallbackContext):
    """ Функция обработки документов, отправленных пользователем."""
    # Получаем файл
    file = await update.message.document.get_file()
    #tmp_file_path = f"{tempfile.gettempdir()}/received.txt"
    tmp_file_path = await file.download_to_drive()  # Сохраняем файл локально

    # Читаем содержимое файла
    with open(tmp_file_path, 'r') as f:
        file_content = f.read()

    response = model.send_message(f"Обучение модели на следующем содержимом:{file_content}")
    await update.message.reply_text(response)
    #tts_file_path = await text_to_speech (response)
    #await update.message.reply_audio(audio=open(tts_file_path, 'rb'))
```

**Назначение**:
Обрабатывает документы, отправленные пользователем, обучая на них модель.

**Параметры**:
- `update` (Update): Объект, представляющий входящее обновление от Telegram.
- `context` (CallbackContext): Объект, содержащий информацию о контексте обработчика.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция извлекает файл из объекта `update.message.document` с использованием метода `get_file()`.
2. Сохраняет файл локально, используя метод `download_to_drive()`.
3. Открывает и считывает содержимое файла.
4. Отправляет содержимое файла в модель для обучения, используя метод `send_message()`.
5. Отправляет ответ пользователю, используя метод `reply_text()`.

**Примеры**:
```python
# Пример вызова функции handle_document
# При отправке документа бот обучится на его содержимом и ответит сообщением
```

### `handle_message`

```python
async def handle_message(update: Update, context: CallbackContext) -> None:
    """ Handle any text message."""
    text_received = update.message.text
    response = model.send_message(text_received)
    await update.message.reply_text(response)
    #tts_file_path = await text_to_speech (response)
    #await update.message.reply_audio(audio=open(tts_file_path, 'rb'))
```

**Назначение**:
Обрабатывает текстовые сообщения, отправленные пользователем, и отправляет ответ.

**Параметры**:
- `update` (Update): Объект, представляющий входящее обновление от Telegram.
- `context` (CallbackContext): Объект, содержащий информацию о контексте обработчика.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция извлекает текст сообщения из объекта `update.message.text`.
2. Отправляет текст сообщения в модель, используя метод `send_message()`.
3. Отправляет ответ пользователю, используя метод `reply_text()`.

**Примеры**:
```python
# Пример вызова функции handle_message
# При отправке текстового сообщения бот ответит сообщением, сгенерированным моделью
```

### `handle_voice`

```python
async def handle_voice(update: Update, context: CallbackContext) -> None:
    """ Handle voice messages."""
    voice_file = await update.message.voice.get_file()
    message = recognizer(audio_url=voice_file.file_path)
    response = model.send_message(message)
    await update.message.reply_text(response)
    tts_file_path = await text_to_speech (response)
    await update.message.reply_audio(audio=open(tts_file_path, 'rb'))
```

**Назначение**:
Обрабатывает голосовые сообщения, отправленные пользователем, преобразует их в текст и отправляет ответ.

**Параметры**:
- `update` (Update): Объект, представляющий входящее обновление от Telegram.
- `context` (CallbackContext): Объект, содержащий информацию о контексте обработчика.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция извлекает голосовой файл из объекта `update.message.voice` с использованием метода `get_file()`.
2. Использует функцию `recognizer` из модуля `src.utils.convertors.tts` для преобразования голосового сообщения в текст.
3. Отправляет текст сообщения в модель, используя метод `send_message()`.
4. Отправляет ответ пользователю, используя метод `reply_text()`.
5. Преобразует текст ответа в голосовое сообщение, используя функцию `text_to_speech` из модуля `src.utils.convertors.tts`.
6. Отправляет голосовое сообщение пользователю, используя метод `reply_audio()`.

**Примеры**:
```python
# Пример вызова функции handle_voice
# При отправке голосового сообщения бот преобразует его в текст, отправит в модель, получит ответ и отправит его пользователю в виде голосового сообщения
```

### `main`

```python
def main() -> None:
    """ Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    # Register message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    # Start the bot
    application.run_polling()
```

**Назначение**:
Запускает Telegram-бота, регистрирует обработчики команд и сообщений.

**Параметры**:
- `None`

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция создает экземпляр класса `Application` с использованием токена, хранящегося в переменной `TELEGRAM_TOKEN`.
2. Регистрирует обработчики команд `/start` и `/help`, используя метод `add_handler()` и классы `CommandHandler`.
3. Регистрирует обработчики текстовых, голосовых сообщений и документов, используя метод `add_handler()` и классы `MessageHandler`.
4. Запускает бота, используя метод `run_polling()`.

**Примеры**:
```python
# Пример вызова функции main
# При запуске скрипта будет запущен Telegram-бот