# Модуль простого Telegram-бота для emil-design.com

## Обзор

Модуль `src.endpoints.emil.minibot` представляет собой простого Telegram-бота, обслуживающего запросы для `emil-design.com`. Он позволяет обрабатывать текстовые и голосовые сообщения, а также документы.

## Подробней

Модуль предоставляет функциональность для взаимодействия с пользователями через Telegram, включая обработку URL-адресов, распознавание речи и отправку файлов.

## Классы

### `BotHandler`

**Описание**: Исполнитель команд, полученных ботом.

**Атрибуты**:

*   `base_dir` (Path): Базовый каталог для хранения ресурсов бота (путь к `src/endpoints/kazarinov`).
*   `scenario` (Scenario): Экземпляр класса `Scenario` для выполнения сценариев.
*   `model` (GoogleGenerativeAi): Экземпляр класса `GoogleGenerativeAi` для взаимодействия с моделью Gemini.
*   `questions_list` (list[str]): Список вопросов для случайного выбора.

**Методы**:

*   `__init__()`: Инициализирует обработчик событий телеграм-бота.
*   `handle_message(bot: telebot, message: 'message')`: Обрабатывает текстовые сообщения.
*   `_send_user_flowchart(bot, chat_id)`: Отправляет схему user\_flowchart.
*   `_handle_url(bot, message: 'message')`: Обрабатывает URL, присланный пользователем.
*   `_handle_next_command(bot, message)`: Обрабатывает команду '--next' и её аналоги.
*   `help_command(bot, message)`: Обрабатывает команду /help.
*   `send_pdf(bot, message, pdf_file)`: Обрабатывает команду /sendpdf для отправки PDF.
*   `handle_voice(bot, message)`: Обрабатывает голосовые сообщения.
*   `_transcribe_voice(file_path)`: Транскрибирование голосового сообщения (заглушка).
*   `handle_document(bot, message)`: Обрабатывает полученные документы.

### `Config`

**Описание**: Класс конфигурации для бота.

**Атрибуты**:

*   `BOT_TOKEN` (str): Токен Telegram-бота.
*   `CHANNEL_ID` (str): ID канала Telegram.
*   `PHOTO_DIR` (Path): Каталог с фотографиями для отправки.
*   `COMMAND_INFO` (str): Информация о боте.
*   `UNKNOWN_COMMAND_MESSAGE` (str): Сообщение об неизвестной команде.
*   `START_MESSAGE` (str): Сообщение при старте бота.
*   `HELP_MESSAGE` (str): Сообщение со списком доступных команд.

## Функции

### `command_start(message)`

```python
@bot.message_handler(commands=['start'])
def command_start(message):
    logger.info(f"User {message.from_user.username} send /start command")
    bot.send_message(message.chat.id, config.START_MESSAGE)
```

**Назначение**: Обрабатывает команду `/start`.

**Как работает функция**:

1.  Логирует информацию об использовании команды `/start`.
2.  Отправляет стартовое сообщение пользователю.

### `command_help(message)`

```python
@bot.message_handler(commands=['help'])
def command_help(message):
    logger.info(f"User {message.from_user.username} send /help command")
    handler.help_command(bot, message)
```

**Назначение**: Обрабатывает команду `/help`.

**Как работает функция**:

1.  Логирует информацию об использовании команды `/help`.
2.  Вызывает метод `help_command` класса `BotHandler` для отправки справки пользователю.

### `command_info(message)`

```python
@bot.message_handler(commands=['info'])
def command_info(message):
    logger.info(f"User {message.from_user.username} send /info command")
    bot.send_message(message.chat.id, config.COMMAND_INFO)
```

**Назначение**: Обрабатывает команду `/info`.

**Как работает функция**:

1.  Логирует информацию об использовании команды `/info`.
2.  Отправляет информацию о боте пользователю.

### `command_time(message)`

```python
@bot.message_handler(commands=['time'])
def command_time(message):
    logger.info(f"User {message.from_user.username} send /time command")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"Current time: {current_time}")
```

**Назначение**: Обрабатывает команду `/time`.

**Как работает функция**:

1.  Логирует информацию об использовании команды `/time`.
2.  Получает текущее время и отправляет его пользователю.

### `command_photo(message)`

```python
@bot.message_handler(commands=['photo'])
def command_photo(message):
    logger.info(f"User {message.from_user.username} send /photo command")
    try:
        photo_files = os.listdir(config.PHOTO_DIR)
        if photo_files:
            random_photo = random.choice(photo_files)
            photo_path = os.path.join(config.PHOTO_DIR, random_photo)
            with open(photo_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, "No photos in the folder.")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Photo directory not found.")
```

**Назначение**: Обрабатывает команду `/photo`.

**Как работает функция**:

1.  Логирует информацию об использовании команды `/photo`.
2.  Отправляет случайную фотографию из каталога `config.PHOTO_DIR` пользователю.

### `handle_voice_message(message)`

```python
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    logger.info(f"User {message.from_user.username} send voice message")
    handler.handle_voice(bot, message)
```

**Назначение**: Обрабатывает голосовые сообщения.

**Как работает функция**:

1.  Логирует информацию об отправке голосового сообщения.
2.  Вызывает метод `handle_voice` класса `BotHandler` для обработки голосового сообщения.

### `handle_document_message(message)`

```python
@bot.message_handler(content_types=['document'])
def handle_document_message(message):
    logger.info(f"User {message.from_user.username} send document message")
    handler.handle_document(bot, message)
```

**Назначение**: Обрабатывает документы.

**Как работает функция**:

1.  Логирует информацию об отправке документа.
2.  Вызывает метод `handle_document` класса `BotHandler` для обработки документа.

### `handle_text_message(message)`

```python
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message):
    logger.info(f"User {message.from_user.username} sent message: {message.text}")
    handler.handle_message(bot, message)
```

**Назначение**: Обрабатывает текстовые сообщения.

**Как работает функция**:

1.  Логирует информацию об отправке текстового сообщения.
2.  Вызывает метод `handle_message` класса `BotHandler` для обработки текстового сообщения.

### `handle_unknown_command(message)`

```python
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message):
    logger.info(f"User {message.from_user.username} send unknown command: {message.text}")
    bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)
```

**Назначение**: Обрабатывает неизвестные команды.

**Как работает функция**:

1.  Логирует информацию об отправке неизвестной команды.
2.  Отправляет сообщение о неизвестной команде пользователю.

## Запуск бота

Для запуска бота необходимо выполнить файл `minibot.py`.