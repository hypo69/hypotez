# Модуль для работы с Telegram ботом для emil-design.com

## Обзор

Модуль `minibot.py` предоставляет простой Telegram бот, предназначенный для обслуживания запросов emil-design.com. 
Он включает в себя обработку текстовых сообщений, URL-адресов, голосовых сообщений и документов. 
Бот использует Google Gemini AI для обработки текста и выполняет сценарии, связанные с URL-адресами OneTab.

## Подробнее

Этот модуль содержит классы и функции для обработки сообщений, поступающих в Telegram бот, 
включая команды, текст, URL-адреса, голосовые сообщения и документы. Он использует Google Gemini AI для ответа на текстовые запросы.
Модуль также включает конфигурацию бота и обработчики для различных типов сообщений.

## Классы

### `BotHandler`

**Описание**: Класс `BotHandler` предназначен для обработки команд, получаемых от Telegram бота.

**Атрибуты**:
- `base_dir` (Path): Базовая директория для хранения ресурсов, таких как схема user_flowchart.
- `scenario` (Scenario): Объект класса `Scenario` для выполнения различных сценариев.
- `model` (GoogleGenerativeAi): Объект класса `GoogleGenerativeAi` для взаимодействия с моделью Google Gemini AI.
- `questions_list` (List[str]): Список вопросов, используемых для обработки команды `--next`.

**Методы**:
- `__init__`: Инициализация обработчика событий телеграм-бота.
- `handle_message`: Обработка текстовых сообщений.
- `_send_user_flowchart`: Отправка схемы user_flowchart.
- `_handle_url`: Обработка URL, присланного пользователем.
- `_handle_next_command`: Обработка команды `--next` и её аналогов.
- `help_command`: Обработка команды `/help`.
- `send_pdf`: Обработка команды `/sendpdf` для отправки PDF.
- `handle_voice`: Обработка голосовых сообщений.
- `_transcribe_voice`: Транскрибирование голосового сообщения (заглушка).
- `handle_document`: Обработка полученных документов.

**Принцип работы**:
Класс `BotHandler` инициализируется с объектами `Scenario` и `GoogleGenerativeAi`, а также списком вопросов.
Он содержит методы для обработки различных типов сообщений, отправки файлов и взаимодействия с AI моделью.

### `Config`

**Описание**: Класс `Config` содержит конфигурационные параметры для Telegram бота.

**Атрибуты**:
- `BOT_TOKEN` (str): Токен Telegram бота, полученный из переменной окружения или credentials.
- `CHANNEL_ID` (str): ID канала Telegram.
- `PHOTO_DIR` (Path): Путь к директории с фотографиями.
- `COMMAND_INFO` (str): Информация о боте, отображаемая по команде `/info`.
- `UNKNOWN_COMMAND_MESSAGE` (str): Сообщение об неизвестной команде.
- `START_MESSAGE` (str): Приветственное сообщение при старте бота.
- `HELP_MESSAGE` (str): Сообщение справки, отображаемое по команде `/help`.

**Принцип работы**:
Класс `Config` содержит статические параметры конфигурации, такие как токен бота, ID канала и пути к различным ресурсам.
Он инициализируется при запуске бота и используется для настройки его поведения.

## Методы класса `BotHandler`

### `handle_message`

```python
def handle_message(self, bot: telebot, message: 'message'):
    """Обработка текстовых сообщений."""
```

**Назначение**: Обрабатывает текстовые сообщения, полученные от пользователя.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `message` (message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `handle_message` проверяет, является ли сообщение командой `?`, URL-адресом, командой `--next` или обычным текстом.
В зависимости от типа сообщения вызываются соответствующие обработчики:
- `_send_user_flowchart`, если сообщение равно `?`.
- `_handle_url`, если сообщение является URL-адресом.
- `_handle_next_command`, если сообщение является одной из команд `--next`.
- В противном случае, текст отправляется в модель `GoogleGenerativeAi` для получения ответа, который отправляется пользователю.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# Допустим, что bot - это экземпляр telebot.TeleBot, а message - экземпляр telebot.types.Message
# bot_handler.handle_message(bot, message)
```

### `_send_user_flowchart`

```python
def _send_user_flowchart(self, bot, chat_id):
    """Отправка схемы user_flowchart."""
```

**Назначение**: Отправляет схему user_flowchart пользователю.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `chat_id` (int): ID чата пользователя.

**Как работает функция**:
Функция `_send_user_flowchart` пытается открыть и отправить фотографию `user_flowchart.png` из директории `assets`.
Если файл не найден, отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# bot_handler._send_user_flowchart(bot, chat_id)
```

### `_handle_url`

```python
def _handle_url(self, bot, message: 'message'):
    """Обработка URL, присланного пользователем."""
```

**Назначение**: Обрабатывает URL-адрес, присланный пользователем.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `message` (message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `_handle_url` проверяет, является ли URL-адрес ссылкой на `one-tab.com`.
Если это так, извлекает данные (цену, название и список URL) с помощью функции `fetch_target_urls_onetab`.
Затем запускает сценарий `run_scenario` с полученными данными.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# bot_handler._handle_url(bot, message)
```

### `_handle_next_command`

```python
def _handle_next_command(self, bot, message):
    """Обработка команды '--next' и её аналогов."""
```

**Назначение**: Обрабатывает команду `--next` и её аналоги.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `message` (message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `_handle_next_command` выбирает случайный вопрос из списка `questions_list`, отправляет его пользователю
и запрашивает у модели `GoogleGenerativeAi` ответ на этот вопрос, который также отправляется пользователю.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# bot_handler._handle_next_command(bot, message)
```

### `help_command`

```python
def help_command(self, bot, message):
    """Обработка команды /help."""
```

**Назначение**: Обрабатывает команду `/help`.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `message` (message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `help_command` отправляет пользователю сообщение со списком доступных команд.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# bot_handler.help_command(bot, message)
```

### `send_pdf`

```python
def send_pdf(self, bot, message, pdf_file):
    """Обработка команды /sendpdf для отправки PDF."""
```

**Назначение**: Обрабатывает команду `/sendpdf` для отправки PDF файла.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `message` (message): Объект сообщения от пользователя.
- `pdf_file` (str): Путь к PDF файлу.

**Как работает функция**:
Функция `send_pdf` пытается открыть PDF файл и отправить его пользователю. Если происходит ошибка, отправляет сообщение об ошибке.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# bot_handler.send_pdf(bot, message, 'path/to/pdf_file.pdf')
```

### `handle_voice`

```python
def handle_voice(self, bot, message):
    """Обработка голосовых сообщений."""
```

**Назначение**: Обрабатывает голосовые сообщения, полученные от пользователя.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `message` (message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `handle_voice` получает информацию о файле голосового сообщения, скачивает его и сохраняет во временный файл.
Затем вызывает функцию `_transcribe_voice` для транскрибирования сообщения и отправляет распознанный текст пользователю.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# bot_handler.handle_voice(bot, message)
```

### `_transcribe_voice`

```python
def _transcribe_voice(self, file_path):
    """Транскрибирование голосового сообщения (заглушка)."""
```

**Назначение**: Транскрибирует голосовое сообщение (заглушка).

**Параметры**:
- `file_path` (str): Путь к файлу голосового сообщения.

**Как работает функция**:
Функция `_transcribe_voice` в текущей реализации возвращает заглушку "Распознавание голоса ещё не реализовано.".

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# transcribed_text = bot_handler._transcribe_voice('path/to/voice_file.ogg')
```

### `handle_document`

```python
def handle_document(self, bot, message):
    """Обработка полученных документов."""
```

**Назначение**: Обрабатывает документы, полученные от пользователя.

**Параметры**:
- `bot` (telebot): Объект бота Telebot.
- `message` (message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `handle_document` получает информацию о файле документа, скачивает его и сохраняет во временный файл.
Затем отправляет пользователю сообщение о том, куда был сохранен файл.

**Примеры**:
```python
# Пример вызова функции
bot_handler = BotHandler()
# bot_handler.handle_document(bot, message)
```

## Методы класса `Config`

Класс `Config` содержит только атрибуты и не имеет методов.

## Функции

### `command_start`

```python
@bot.message_handler(commands=['start'])
def command_start(message):
    """Обработка команды /start."""
```

**Назначение**: Обрабатывает команду `/start`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `command_start` отправляет пользователю приветственное сообщение, используя текст из `config.START_MESSAGE`.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# command_start(message)
```

### `command_help`

```python
@bot.message_handler(commands=['help'])
def command_help(message):
    """Обработка команды /help."""
```

**Назначение**: Обрабатывает команду `/help`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `command_help` вызывает метод `help_command` объекта `handler` для отправки пользователю сообщения справки.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# command_help(message)
```

### `command_info`

```python
@bot.message_handler(commands=['info'])
def command_info(message):
    """Обработка команды /info."""
```

**Назначение**: Обрабатывает команду `/info`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `command_info` отправляет пользователю информацию о боте, используя текст из `config.COMMAND_INFO`.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# command_info(message)
```

### `command_time`

```python
@bot.message_handler(commands=['time'])
def command_time(message):
    """Обработка команды /time."""
```

**Назначение**: Обрабатывает команду `/time`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `command_time` получает текущее время и отправляет его пользователю.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# command_time(message)
```

### `command_photo`

```python
@bot.message_handler(commands=['photo'])
def command_photo(message):
    """Обработка команды /photo."""
```

**Назначение**: Обрабатывает команду `/photo`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `command_photo` выбирает случайную фотографию из директории `config.PHOTO_DIR` и отправляет ее пользователю.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# command_photo(message)
```

### `handle_voice_message`

```python
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    """Обработка голосовых сообщений."""
```

**Назначение**: Обрабатывает голосовые сообщения.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `handle_voice_message` вызывает метод `handle_voice` объекта `handler` для обработки голосового сообщения.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# handle_voice_message(message)
```

### `handle_document_message`

```python
@bot.message_handler(content_types=['document'])
def handle_document_message(message):
    """Обработка полученных документов."""
```

**Назначение**: Обрабатывает документы, отправленные пользователем.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `handle_document_message` вызывает метод `handle_document` объекта `handler` для обработки документа.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# handle_document_message(message)
```

### `handle_text_message`

```python
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message):
    """Обработка текстовых сообщений."""
```

**Назначение**: Обрабатывает текстовые сообщения, не являющиеся командами.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `handle_text_message` вызывает метод `handle_message` объекта `handler` для обработки текстового сообщения.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# handle_text_message(message)
```

### `handle_unknown_command`

```python
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message):
    """Обработка неизвестных команд."""
```

**Назначение**: Обрабатывает неизвестные команды.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения от пользователя.

**Как работает функция**:
Функция `handle_unknown_command` отправляет пользователю сообщение о том, что команда неизвестна, используя текст из `config.UNKNOWN_COMMAND_MESSAGE`.

**Примеры**:
```python
# Пример вызова функции (обычно вызывается автоматически Telebot)
# handle_unknown_command(message)
```