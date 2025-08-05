# Модуль `minibot`

## Обзор

Модуль `minibot` предназначен для обслуживания запросов на создание прайс-листов для заказчика Казаринова через Telegram-бота. Он включает в себя обработку текстовых и голосовых сообщений, документов, а также интеграцию с Google Gemini для генерации ответов.

## Подробнее

Модуль предоставляет функциональность Telegram-бота, способного отвечать на текстовые и голосовые сообщения, обрабатывать документы и URL, а также генерировать ответы с использованием модели Google Gemini. Он также включает в себя механизм обработки сценариев на основе полученных данных. Модуль использует библиотеку `telebot` для взаимодействия с Telegram API и `asyncio` для асинхронного выполнения задач.

## Классы

### `Config`

**Описание**: Класс `Config` содержит конфигурационные параметры для работы бота.

**Атрибуты**:

-   `ENDPOINT` (str): Имя эндпоинта (по умолчанию `'kazarinov'`).
-   `MODE` (str): Режим работы бота (`'PRODUCTION'` или `'DEV'`). Определяет, какой токен бота использовать.
-   `BOT_TOKEN` (str): Токен Telegram-бота.
-   `CHANNEL_ID` (str): ID канала Telegram.
-   `PHOTO_DIR` (Path): Путь к директории с фотографиями.
-   `COMMAND_INFO` (str): Информация о боте, отображаемая по команде `/info`.
-   `UNKNOWN_COMMAND_MESSAGE` (str): Сообщение, отображаемое при вводе неизвестной команды.
-   `START_MESSAGE` (str): Приветственное сообщение при старте бота.
-   `HELP_MESSAGE` (str): Сообщение со списком доступных команд.
-   `WINDOW_MODE` (str): Режим окна (по умолчанию `'normal'`).

**Принцип работы**:

Класс `Config` определяет параметры, необходимые для работы бота, такие как токен, ID канала, пути к директориям и сообщения. В зависимости от режима работы (`PRODUCTION` или `DEV`), выбирается соответствующий токен бота.

### `BotHandler`

**Описание**: Класс `BotHandler` обрабатывает команды, полученные от бота.

**Атрибуты**:

-   `base_dir` (Path): Базовая директория модуля.
-   `questions_list` (List[str]): Список вопросов для случайного выбора при обработке команды `--next`.
-   `model` (GoogleGenerativeAi): Объект для взаимодействия с моделью Google Gemini.

**Методы**:

-   `__init__(self)`: Инициализирует обработчик событий телеграм-бота.
-   `handle_message(self, bot: telebot, message: 'message')`: Обрабатывает текстовые сообщения.
-   `_send_user_flowchart(self, bot, chat_id)`: Отправляет схему user_flowchart.
-   `_handle_url(self, bot, message: 'message')`: Обрабатывает URL, присланный пользователем.
-   `_handle_next_command(self, bot, message)`: Обрабатывает команду `--next` и её аналоги.
-   `help_command(self, bot, message)`: Обрабатывает команду `/help`.
-   `send_pdf(self, bot, message, pdf_file)`: Обрабатывает команду `/sendpdf` для отправки PDF.
-   `handle_voice(self, bot, message)`: Обрабатывает голосовые сообщения.
-   `_transcribe_voice(self, file_path)`: Транскрибирование голосового сообщения (заглушка).
-   `handle_document(self, bot, message)`: Обрабатывает полученные документы.

## Методы класса `BotHandler`

### `__init__`

```python
def __init__(self):
    """Инициализация обработчика событий телеграм-бота."""
    ...
```

**Назначение**: Инициализирует экземпляр класса `BotHandler`.

**Как работает функция**:

-   Инициализирует список вопросов `self.questions_list`.
-   Создает экземпляр класса `GoogleGenerativeAi` для взаимодействия с моделью Google Gemini.

### `handle_message`

```python
def handle_message(self, bot:telebot, message:'message'):
    """Обработка текстовых сообщений."""
    ...
```

**Назначение**: Обрабатывает текстовые сообщения, поступающие от пользователя.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки сообщений.
-   `message` (message): Объект сообщения, содержащий текст и информацию о чате.

**Как работает функция**:

1.  Извлекает текст сообщения.
2.  Проверяет, является ли текст вопросительным знаком (`?`). Если да, отправляет схему user_flowchart.
3.  Проверяет, является ли текст URL. Если да, обрабатывает URL.
4.  Проверяет, является ли текст командой для запроса следующего вопроса (`--next`, `-next`, `__next`, `-n`, `-q`). Если да, обрабатывает команду.
5.  В противном случае пытается получить ответ от модели Google Gemini и отправляет его пользователю.
6.  В случае ошибки логирует её и отправляет сообщение об ошибке пользователю.

**Примеры**:

```python
# Пример вызова функции
handler = BotHandler()
bot = telebot.TeleBot(Config.BOT_TOKEN)
message = telebot.types.Message()
message.text = "Привет, бот!"
message.chat = telebot.types.Chat()
message.chat.id = 123456789
handler.handle_message(bot, message)
```

### `_send_user_flowchart`

```python
def _send_user_flowchart(self, bot, chat_id):
    """Отправка схемы user_flowchart."""
    ...
```

**Назначение**: Отправляет пользователю схему `user_flowchart`.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки фото.
-   `chat_id` (int): ID чата для отправки сообщения.

**Как работает функция**:

1.  Формирует путь к файлу `user_flowchart.png`.
2.  Пытается открыть файл и отправить его пользователю.
3.  В случае ошибки логирует её и отправляет сообщение об ошибке пользователю.

### `_handle_url`

```python
def _handle_url(self, bot, message:'message'):
    """Обработка URL, присланного пользователем."""
    ...
```

**Назначение**: Обрабатывает URL, присланный пользователем.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки сообщений.
-   `message` (message): Объект сообщения, содержащий URL и информацию о чате.

**Как работает функция**:

1.  Извлекает URL из сообщения.
2.  Проверяет, является ли URL ссылкой на `one-tab.com`. Если нет, отправляет сообщение об ошибке пользователю.
3.  Извлекает цену, имя и список URL из OneTab.
4.  В случае успеха запускает сценарий обработки URL.
5.  В случае ошибки логирует её и отправляет сообщение об ошибке пользователю.

### `_handle_next_command`

```python
def _handle_next_command(self, bot, message):
    """Обработка команды '--next' и её аналогов."""
    ...
```

**Назначение**: Обрабатывает команду `--next` и её аналоги.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки сообщений.
-   `message` (message): Объект сообщения, содержащий информацию о чате.

**Как работает функция**:

1.  Выбирает случайный вопрос из списка `self.questions_list`.
2.  Пытается получить ответ от модели Google Gemini и отправляет вопрос и ответ пользователю.
3.  В случае ошибки логирует её и отправляет сообщение об ошибке пользователю.

### `help_command`

```python
def help_command(self, bot, message):
    """Обработка команды /help."""
    ...
```

**Назначение**: Обрабатывает команду `/help`.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки сообщений.
-   `message` (message): Объект сообщения, содержащий информацию о чате.

**Как работает функция**:

Отправляет пользователю сообщение со списком доступных команд.

### `send_pdf`

```python
def send_pdf(self, bot, message, pdf_file):
    """Обработка команды /sendpdf для отправки PDF."""
    ...
```

**Назначение**: Обрабатывает команду `/sendpdf` для отправки PDF-файла.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки документов.
-   `message` (message): Объект сообщения, содержащий информацию о чате.
-   `pdf_file` (str): Путь к PDF-файлу.

**Как работает функция**:

1.  Пытается открыть PDF-файл и отправить его пользователю.
2.  В случае ошибки логирует её и отправляет сообщение об ошибке пользователю.

### `handle_voice`

```python
def handle_voice(self, bot, message):
    """Обработка голосовых сообщений."""
    ...
```

**Назначение**: Обрабатывает голосовые сообщения.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки сообщений и получения информации о файле.
-   `message` (message): Объект сообщения, содержащий голосовое сообщение и информацию о чате.

**Как работает функция**:

1.  Получает информацию о файле голосового сообщения.
2.  Скачивает файл голосового сообщения.
3.  Сохраняет файл во временную директорию.
4.  Пытается транскрибировать голосовое сообщение (в текущей реализации возвращает заглушку).
5.  Отправляет распознанный текст пользователю.
6.  В случае ошибки логирует её и отправляет сообщение об ошибке пользователю.

### `_transcribe_voice`

```python
def _transcribe_voice(self, file_path):
    """Транскрибирование голосового сообщения (заглушка)."""
    ...
```

**Назначение**: Транскрибирует голосовое сообщение (заглушка).

**Параметры**:

-   `file_path` (str): Путь к файлу голосового сообщения.

**Как работает функция**:

Возвращает сообщение о том, что распознавание голоса ещё не реализовано.

### `handle_document`

```python
def handle_document(self, bot, message):
    """Обработка полученных документов."""
    ...
```

**Назначение**: Обрабатывает полученные документы.

**Параметры**:

-   `bot` (telebot): Объект бота для отправки сообщений и получения информации о файле.
-   `message` (message): Объект сообщения, содержащий документ и информацию о чате.

**Как работает функция**:

1.  Получает информацию о файле документа.
2.  Скачивает файл документа.
3.  Сохраняет файл во временную директорию.
4.  Отправляет пользователю сообщение о том, что файл сохранен.
5.  В случае ошибки логирует её и отправляет сообщение об ошибке пользователю.

## Функции

### `run_bot`

```python
def run_bot() -> None:
    """
    Запускает polling-бота в бесконечном цикле с автоматическим восстановлением при ошибках.

    При возникновении исключений выполняется остановка бота и повторный запуск через 10 секунд.

    Raises:
        Exception: Повторно пробрасывается при фатальной ошибке, если бот не может быть запущен.
    """
    ...
```

**Назначение**: Запускает Telegram-бота в бесконечном цикле с автоматическим восстановлением при ошибках.

**Как работает функция**:

1.  Запускает бота в режиме `infinity_polling`.
2.  В случае возникновения исключения останавливает бота и перезапускает его через 10 секунд.

## Обработчики сообщений

### `command_start`

```python
@bot.message_handler(commands=['start'])
def command_start(message):
    logger.info(f"User {message.from_user.username} send /start command")
    bot.send_message(message.chat.id, config.START_MESSAGE)
```

**Назначение**: Обрабатывает команду `/start`.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Отправляет пользователю приветственное сообщение из конфигурации.

### `command_help`

```python
@bot.message_handler(commands=['help'])
def command_help(message):
    logger.info(f"User {message.from_user.username} send /help command")
    handler.help_command(bot, message)
```

**Назначение**: Обрабатывает команду `/help`.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Вызывает метод `help_command` объекта `handler` для отправки справки пользователю.

### `command_info`

```python
@bot.message_handler(commands=['info'])
def command_info(message):
    logger.info(f"User {message.from_user.username} send /info command")
    bot.send_message(message.chat.id, config.COMMAND_INFO)
```

**Назначение**: Обрабатывает команду `/info`.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Отправляет пользователю информацию о боте из конфигурации.

### `command_time`

```python
@bot.message_handler(commands=['time'])
def command_time(message):
    logger.info(f"User {message.from_user.username} send /time command")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.send_message(message.chat.id, f"Current time: {current_time}")
```

**Назначение**: Обрабатывает команду `/time`.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Получает текущее время и отправляет его пользователю.

### `command_photo`

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

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Пытается отправить пользователю случайную фотографию из директории, указанной в конфигурации.
3.  В случае отсутствия фотографий или директории отправляет сообщение об ошибке.

### `handle_voice_message`

```python
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    logger.info(f"User {message.from_user.username} send voice message")
    handler.handle_voice(bot, message)
```

**Назначение**: Обрабатывает голосовые сообщения.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Вызывает метод `handle_voice` объекта `handler` для обработки голосового сообщения.

### `handle_document_message`

```python
@bot.message_handler(content_types=['document'])
def handle_document_message(message):
    logger.info(f'User {message.from_user.username} send document message')
    handler.handle_document(bot, message)
```

**Назначение**: Обрабатывает сообщения с документами.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Вызывает метод `handle_document` объекта `handler` для обработки документа.

### `handle_text_message`

```python
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message):
    logger.info(f'User {message.from_user.username} sent message: {message.text}')
    handler.handle_message(bot, message )
```

**Назначение**: Обрабатывает текстовые сообщения, не начинающиеся с `/`.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Вызывает метод `handle_message` объекта `handler` для обработки текстового сообщения.

### `handle_unknown_command`

```python
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message):
    logger.info(f'User {message.from_user.username} send unknown command: {message.text}')
    bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)
```

**Назначение**: Обрабатывает неизвестные команды, начинающиеся с `/`.

**Параметры**:

-   `message` (telebot.types.Message): Объект сообщения.

**Как работает функция**:

1.  Логирует информацию об использовании команды.
2.  Отправляет пользователю сообщение о неизвестной команде из конфигурации.