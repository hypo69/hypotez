# Минибот для обслуживания запросов на создание прайс-листа для Казаринова

## Обзор

Модуль `src.endpoints.kazarinov.minibot` представляет собой минибота, предназначенного для обработки запросов на создание прайс-листа для Сергея Казаринова.

## Подробней

Модуль использует библиотеку `telebot` для создания Telegram-бота, который принимает URL-адрес OneTab, извлекает информацию о товарах и создает прайс-лист.

## Классы

### `Config`

**Описание**: Класс конфигурации для бота.

**Атрибуты**:

*   `ENDPOINT` (str): Конечная точка (значение: `'kazarinov'`).
*   `MODE` (str): Определяет режим работы бота (`'PRODUCTION'` или `'DEV'`).
*   `BOT_TOKEN` (str): Токен Telegram-бота. Зависит от значения `MODE`.
*   `CHANNEL_ID` (str): ID канала Telegram (значение: `'@onela'`).
*   `PHOTO_DIR` (Path): Каталог с фотографиями (путь к `src/endpoints/kazarinov/assets`).
*   `COMMAND_INFO` (str): Информация о боте.
*   `UNKNOWN_COMMAND_MESSAGE` (str): Сообщение об неизвестной команде.
*   `START_MESSAGE` (str): Сообщение при старте бота.
*   `HELP_MESSAGE` (str): Сообщение со списком доступных команд.
*    `WINDOW_MODE` (str): Режим отображения веб-драйвера.

**Принцип работы**:

Класс `Config` определяет параметры конфигурации для работы бота. Он использует переменные окружения, если `USE_ENV` установлен в `True`, иначе использует значения из базы данных паролей `keepass`. В зависимости от значения `MODE` устанавливаются различные токены бота.

### `BotHandler`

**Описание**: Исполнитель команд, полученных ботом.

**Атрибуты**:

*   `base_dir` (Path): Базовый каталог для хранения ресурсов бота (путь к `src/endpoints/kazarinov`).
*   `questions_list` (list[str]): Список вопросов для случайного выбора.
*   `model` (GoogleGenerativeAi): Экземпляр класса `GoogleGenerativeAi` для взаимодействия с моделью Gemini.

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
    logger.info(f'User {message.from_user.username} send document message')
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
    logger.info(f'User {message.from_user.username} sent message: {message.text}')
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
    logger.info(f'User {message.from_user.username} send unknown command: {message.text}')
    bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)
```

**Назначение**: Обрабатывает неизвестные команды.

**Как работает функция**:

1.  Логирует информацию об отправке неизвестной команды.
2.  Отправляет сообщение об неизвестной команде пользователю.

### `run_bot()`

```python
def run_bot() -> None:
    """
    Запускает polling-бота в бесконечном цикле с автоматическим восстановлением при ошибках.

    При возникновении исключений выполняется остановка бота и повторный запуск через 10 секунд.

    Raises:
        Exception: Повторно пробрасывается при фатальной ошибке, если бот не может быть запущен.
    """
    try:
        logger.info(f'Starting bot in {Config.MODE} mode')
        bot.infinity_polling()
        

    except Exception as ex:
        logger.error('Error during bot polling', ex, exc_info=True)

        try:
            bot.stop_bot()
        except Exception as ex:
            logger.error('Ошибка останова бота', ex, exc_info=True)

        logger.debug('Повторный запуск через 10 секунд')
        time.sleep(10)
        run_bot()
```

**Назначение**: Обеспечивает надежный запуск и автоматическое восстановление Telegram-бота.

**Как работает функция**:

1.  Запускает бота в бесконечном цикле, используя метод `bot.infinity_polling()`.
2.  В случае возникновения исключения:
    *   Логирует информацию об ошибке.
    *   Пытается остановить бота.
    *   Выжидает 10 секунд.
    *   Повторно вызывает `run_bot()` для перезапуска бота.

## Запуск бота

Для запуска бота необходимо выполнить файл `minibot.py`.