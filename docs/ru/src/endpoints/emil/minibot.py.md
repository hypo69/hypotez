# Модуль `minibot.py`

## Обзор

Модуль `minibot.py` представляет собой реализацию простого Telegram-бота, предназначенного для обработки запросов пользователей, связанных с веб-сайтом emil-design.com. Бот способен обрабатывать текстовые и голосовые сообщения, URL-адреса, а также отправлять PDF-файлы. Он использует модель Google Gemini для генерации ответов на текстовые запросы.

## Подробнее

Модуль содержит классы `BotHandler` и `Config`, а также основные обработчики сообщений для Telegram-бота. `BotHandler` отвечает за обработку различных типов сообщений, включая текст, URL-адреса и голосовые сообщения. Класс `Config` содержит настройки бота, такие как токен API, ID канала и пути к файлам.

## Содержание

- [Классы](#классы)
  - [`BotHandler`](#botHandler)
  - [`Config`](#config)
- [Функции](#функции)
  - [`command_start`](#command_start)
  - [`command_help`](#command_help)
  - [`command_info`](#command_info)
  - [`command_time`](#command_time)
  - [`command_photo`](#command_photo)
  - [`handle_voice_message`](#handle_voice_message)
  - [`handle_document_message`](#handle_document_message)
  - [`handle_text_message`](#handle_text_message)
  - [`handle_unknown_command`](#handle_unknown_command)

## Классы

### `BotHandler`

**Описание**:
Класс `BotHandler` предназначен для обработки команд и сообщений, получаемых от Telegram-бота. Он включает методы для обработки текста, URL-адресов, голосовых сообщений и документов.

**Принцип работы**:
Класс инициализируется с использованием экземпляра класса `Scenario` и `GoogleGenerativeAI`. Он содержит методы для обработки различных типов сообщений, отправки ответов пользователю и выполнения сценариев.

**Атрибуты**:
- `base_dir` (Path): Базовый путь к директории сценариев (`__root__ / 'src' / 'endpoints' / 'kazarinov'`).
- `scenario` (Scenario): Экземпляр класса `Scenario` для выполнения сценариев.
- `model` (GoogleGenerativeAI): Экземпляр класса `GoogleGenerativeAI` для взаимодействия с моделью Gemini.
- `questions_list` (List[str]): Список вопросов, используемых при обработке команды `--next`.

**Методы**:
- [`__init__`](#__init__)
- [`handle_message`](#handle_message)
- [`_send_user_flowchart`](#_send_user_flowchart)
- [`_handle_url`](#_handle_url)
- [`_handle_next_command`](#_handle_next_command)
- [`help_command`](#help_command)
- [`send_pdf`](#send_pdf)
- [`handle_voice`](#handle_voice)
- [`_transcribe_voice`](#_transcribe_voice)
- [`handle_document`](#handle_document)

### `Config`

**Описание**:
Класс `Config` предназначен для хранения конфигурационных параметров Telegram-бота, таких как токен API, ID канала и пути к файлам.

**Принцип работы**:
Класс инициализируется с использованием переменных окружения или значений из базы данных (в зависимости от значения `USE_ENV`).

**Атрибуты**:
- `BOT_TOKEN` (str): Токен API Telegram-бота.
- `CHANNEL_ID` (str): ID канала Telegram.
- `PHOTO_DIR` (Path): Путь к директории с фотографиями.
- `COMMAND_INFO` (str): Информация о боте, отображаемая по команде `/info`.
- `UNKNOWN_COMMAND_MESSAGE` (str): Сообщение, отображаемое при получении неизвестной команды.
- `START_MESSAGE` (str): Сообщение, отображаемое при старте бота.
- `HELP_MESSAGE` (str): Сообщение справки, отображаемое по команде `/help`.

## Функции

### `__init__`

```python
def __init__(self):
    """Инициализация обработчика событий телеграм-бота."""
    ...
```

**Назначение**: Инициализация экземпляра класса `BotHandler`.

**Как работает функция**:
1. Инициализирует атрибут `scenario` экземпляром класса `Scenario`.
2. Инициализирует атрибут `model` экземпляром класса `GoogleGenerativeAI`, передавая в него значение переменной окружения `GEMINI_API`.
3. Инициализирует атрибут `questions_list` списком строк с вопросами.

```
Инициализация BotHandler
│
├── Создание экземпляра Scenario
│   │
│   └── scenario = Scenario()
│
├── Создание экземпляра GoogleGenerativeAI
│   │
│   └── model = GoogleGenerativeAI(os.getenv('GEMINI_API'))
│
└── Инициализация списка вопросов
    │
    └── questions_list = ['Я не понял?', 'Объясни пожалуйста']
```

### `handle_message`

```python
def handle_message(self, bot: telebot, message: 'message'):
    """Обработка текстовых сообщений."""
    ...
```

**Назначение**: Обработка текстовых сообщений, полученных от пользователя.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `message` (message): Объект сообщения, содержащий текст сообщения и другую информацию.

**Как работает функция**:
1. Извлекает текст из сообщения.
2. Если текст равен `?`, вызывает метод `_send_user_flowchart` для отправки схемы user_flowchart.
3. Если текст является URL-адресом, вызывает метод `_handle_url` для обработки URL.
4. Если текст является одной из команд (`--next`, `-next`, `__next`, `-n`, `-q`), вызывает метод `_handle_next_command` для обработки команды.
5. В противном случае пытается получить ответ от модели Gemini и отправляет его пользователю.

```
Обработка текстового сообщения
│
├── Извлечение текста из сообщения
│   │
│   └── text = message.text
│
├── Проверка на команду "?"
│   │
│   └── if text == '?':
│       └── _send_user_flowchart(bot, message.chat.id)
│
├── Проверка на URL
│   │
│   └── elif is_url(text):
│       └── _handle_url(bot, message)
│
├── Проверка на команду "--next"
│   │
│   └── elif text in ('--next', '-next', '__next', '-n', '-q'):
│       └── _handle_next_command(bot, message)
│
└── Получение ответа от модели Gemini
    │
    ├── answer = self.model.chat(text)
    │
    └── Отправка ответа пользователю
        │
        └── bot.send_message(message.chat.id, answer)
```

### `_send_user_flowchart`

```python
def _send_user_flowchart(self, bot, chat_id):
    """Отправка схемы user_flowchart."""
    ...
```

**Назначение**: Отправка пользователю схемы `user_flowchart.png`.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `chat_id` (int): ID чата пользователя.

**Как работает функция**:
1. Формирует путь к файлу `user_flowchart.png`.
2. Открывает файл и отправляет его пользователю в виде фотографии.
3. Обрабатывает исключение `FileNotFoundError`, если файл не найден.

```
Отправка схемы user_flowchart
│
├── Формирование пути к файлу
│   │
│   └── photo_path = self.base_dir / 'assets' / 'user_flowchart.png'
│
├── Открытие файла
│   │
│   └── with open(photo_path, 'rb') as photo:
│       └── Отправка фотографии пользователю
│           │
│           └── bot.send_photo(chat_id, photo)
│
└── Обработка исключения FileNotFoundError
    │
    └── logger.error(f"File not found: {photo_path}")
        └── Отправка сообщения об ошибке пользователю
            │
            └── bot.send_message(chat_id, "Схема не найдена.")
```

### `_handle_url`

```python
def _handle_url(self, bot, message: 'message'):
    """Обработка URL, присланного пользователем."""
    ...
```

**Назначение**: Обработка URL, присланного пользователем.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `message` (message): Объект сообщения, содержащий URL-адрес.

**Как работает функция**:
1. Извлекает URL из сообщения.
2. Проверяет, начинается ли URL с `https://one-tab.com` или `https://www.one-tab.com`.
3. Если URL не соответствует формату, отправляет пользователю сообщение об ошибке.
4. Извлекает цену, название товара и список URL-адресов из страницы OneTab.
5. Запускает асинхронный сценарий с полученными данными.
6. Обрабатывает исключения, возникающие при извлечении данных или выполнении сценария.

```
Обработка URL
│
├── Извлечение URL из сообщения
│   │
│   └── url = message.text
│
├── Проверка формата URL
│   │
│   └── if not url.startswith(('https://one-tab.com', 'https://www.one-tab.com')):
│       └── Отправка сообщения об ошибке пользователю
│           │
│           └── bot.send_message(message.chat.id, 'Мне на вход нужен URL `https://one-tab.com` Проверь, что ты мне посылаешь')
│
├── Извлечение данных из страницы OneTab
│   │
│   └── price, mexiron_name, urls = fetch_target_urls_onetab(url)
│       └── Отправка сообщения о полученном товаре
│           │
│           └── bot.send_message(message.chat.id, f'Получил мехирон {mexiron_name} - {price} шек')
│
└── Запуск асинхронного сценария
    │
    └── asyncio.run(self.scenario.run_scenario(bot=bot, chat_id=message.chat.id, urls=list(urls), price=price, mexiron_name=mexiron_name))
```

### `_handle_next_command`

```python
def _handle_next_command(self, bot, message):
    """Обработка команды '--next' и её аналогов."""
    ...
```

**Назначение**: Обработка команды `--next` и её аналогов.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `message` (message): Объект сообщения.

**Как работает функция**:
1. Выбирает случайный вопрос из списка `questions_list`.
2. Получает ответ от модели Gemini на выбранный вопрос.
3. Отправляет вопрос и ответ пользователю.
4. Обрабатывает исключения, возникающие при чтении вопросов или взаимодействии с моделью.

```
Обработка команды "--next"
│
├── Выбор случайного вопроса
│   │
│   └── question = random.choice(self.questions_list)
│
├── Получение ответа от модели Gemini
│   │
│   └── answer = self.model.ask(question)
│
└── Отправка вопроса и ответа пользователю
    │
    ├── bot.send_message(message.chat.id, question)
    │
    └── bot.send_message(message.chat.id, answer)
```

### `help_command`

```python
def help_command(self, bot, message):
    """Обработка команды /help."""
    ...
```

**Назначение**: Обработка команды `/help`.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `message` (message): Объект сообщения.

**Как работает функция**:
1. Отправляет пользователю сообщение со списком доступных команд.

```
Обработка команды /help
│
└── Отправка сообщения со списком команд
    │
    └── bot.send_message(message.chat.id, 'Available commands:\n/start - Start the bot\n/help - Show this help message\n/sendpdf - Send a PDF file')
```

### `send_pdf`

```python
def send_pdf(self, bot, message, pdf_file):
    """Обработка команды /sendpdf для отправки PDF."""
    ...
```

**Назначение**: Обработка команды `/sendpdf` для отправки PDF-файла.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `message` (message): Объект сообщения.
- `pdf_file` (str): Путь к PDF-файлу.

**Как работает функция**:
1. Открывает PDF-файл.
2. Отправляет файл пользователю.
3. Обрабатывает исключения, возникающие при открытии или отправке файла.

```
Обработка команды /sendpdf
│
├── Открытие PDF-файла
│   │
│   └── with open(pdf_file, 'rb') as pdf_file_obj:
│       └── Отправка файла пользователю
│           │
│           └── bot.send_document(message.chat.id, document=pdf_file_obj)
│
└── Обработка исключения
    │
    └── logger.error(f'Ошибка при отправке PDF-файла: {ex}')
        └── Отправка сообщения об ошибке пользователю
            │
            └── bot.send_message(message.chat.id, 'Произошла ошибка при отправке PDF-файла. Попробуй ещё раз.')
```

### `handle_voice`

```python
def handle_voice(self, bot, message):
    """Обработка голосовых сообщений."""
    ...
```

**Назначение**: Обработка голосовых сообщений.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `message` (message): Объект сообщения.

**Как работает функция**:
1. Получает информацию о файле голосового сообщения.
2. Скачивает файл.
3. Сохраняет файл во временную директорию.
4. Транскрибирует голосовое сообщение (используется заглушка).
5. Отправляет распознанный текст пользователю.
6. Обрабатывает исключения, возникающие при обработке голосового сообщения.

```
Обработка голосового сообщения
│
├── Получение информации о файле
│   │
│   └── file_info = bot.get_file(message.voice.file_id)
│
├── Скачивание файла
│   │
│   └── file = bot.download_file(file_info.file_path)
│
├── Сохранение файла во временную директорию
│   │
│   └── file_path = gs.path.temp / f'{message.voice.file_id}.ogg'
│       └── with open(file_path, 'wb') as f:
│           └── f.write(file)
│
├── Транскрибирование голосового сообщения
│   │
│   └── transcribed_text = self._transcribe_voice(file_path)
│
└── Отправка распознанного текста пользователю
    │
    └── bot.send_message(message.chat.id, f'Распознанный текст: {transcribed_text}')
```

### `_transcribe_voice`

```python
def _transcribe_voice(self, file_path):
    """Транскрибирование голосового сообщения (заглушка)."""
    ...
```

**Назначение**: Транскрибирование голосового сообщения (заглушка).

**Параметры**:
- `file_path` (str): Путь к файлу голосового сообщения.

**Как работает функция**:
1. Возвращает строку `'Распознавание голоса ещё не реализовано.'`.

```
Транскрибирование голосового сообщения
│
└── Возврат заглушки
    │
    └── return 'Распознавание голоса ещё не реализовано.'
```

### `handle_document`

```python
def handle_document(self, bot, message):
    """Обработка полученных документов."""
    ...
```

**Назначение**: Обработка полученных документов.

**Параметры**:
- `bot` (telebot): Экземпляр Telegram-бота.
- `message` (message): Объект сообщения.

**Как работает функция**:
1. Получает информацию о файле документа.
2. Скачивает файл.
3. Сохраняет файл во временную директорию.
4. Отправляет пользователю сообщение о сохранении файла.
5. Обрабатывает исключения, возникающие при обработке документа.

```
Обработка полученного документа
│
├── Получение информации о файле
│   │
│   └── file_info = bot.get_file(message.document.file_id)
│
├── Скачивание файла
│   │
│   └── file = bot.download_file(file_info.file_path)
│
├── Сохранение файла во временную директорию
│   │
│   └── tmp_file_path = gs.path.temp / message.document.file_name
│       └── with open(tmp_file_path, 'wb') as f:
│           └── f.write(file)
│
└── Отправка сообщения о сохранении файла пользователю
    │
    └── bot.send_message(message.chat.id, f'Файл сохранен в {tmp_file_path}')
```

### `command_start`

```python
@bot.message_handler(commands=['start'])
def command_start(message):
    """Обработка команды /start."""
    ...
```

**Назначение**: Обработка команды `/start`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий информацию о команде.

**Как работает функция**:
1. Логирует информацию об использовании команды `/start`.
2. Отправляет пользователю приветственное сообщение из конфигурации.

```
Обработка команды /start
│
├── Логирование использования команды
│   │
│   └── logger.info(f"User {message.from_user.username} send /start command")
│
└── Отправка приветственного сообщения
    │
    └── bot.send_message(message.chat.id, config.START_MESSAGE)
```

### `command_help`

```python
@bot.message_handler(commands=['help'])
def command_help(message):
    """Обработка команды /help."""
    ...
```

**Назначение**: Обработка команды `/help`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий информацию о команде.

**Как работает функция**:
1. Логирует информацию об использовании команды `/help`.
2. Вызывает метод `help_command` класса `BotHandler` для отправки справки пользователю.

```
Обработка команды /help
│
├── Логирование использования команды
│   │
│   └── logger.info(f"User {message.from_user.username} send /help command")
│
└── Вызов метода help_command класса BotHandler
    │
    └── handler.help_command(bot, message)
```

### `command_info`

```python
@bot.message_handler(commands=['info'])
def command_info(message):
    """Обработка команды /info."""
    ...
```

**Назначение**: Обработка команды `/info`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий информацию о команде.

**Как работает функция**:
1. Логирует информацию об использовании команды `/info`.
2. Отправляет пользователю информацию о боте из конфигурации.

```
Обработка команды /info
│
├── Логирование использования команды
│   │
│   └── logger.info(f"User {message.from_user.username} send /info command")
│
└── Отправка информации о боте
    │
    └── bot.send_message(message.chat.id, config.COMMAND_INFO)
```

### `command_time`

```python
@bot.message_handler(commands=['time'])
def command_time(message):
    """Обработка команды /time."""
    ...
```

**Назначение**: Обработка команды `/time`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий информацию о команде.

**Как работает функция**:
1. Логирует информацию об использовании команды `/time`.
2. Получает текущее время.
3. Отправляет пользователю текущее время.

```
Обработка команды /time
│
├── Логирование использования команды
│   │
│   └── logger.info(f"User {message.from_user.username} send /time command")
│
├── Получение текущего времени
│   │
│   └── now = datetime.datetime.now()
│       └── current_time = now.strftime("%H:%M:%S")
│
└── Отправка текущего времени пользователю
    │
    └── bot.send_message(message.chat.id, f"Current time: {current_time}")
```

### `command_photo`

```python
@bot.message_handler(commands=['photo'])
def command_photo(message):
    """Обработка команды /photo."""
    ...
```

**Назначение**: Обработка команды `/photo`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий информацию о команде.

**Как работает функция**:
1. Логирует информацию об использовании команды `/photo`.
2. Получает список файлов фотографий из директории, указанной в конфигурации.
3. Выбирает случайную фотографию.
4. Отправляет фотографию пользователю.
5. Обрабатывает исключения, возникающие при доступе к директории или отсутствии файлов.

```
Обработка команды /photo
│
├── Логирование использования команды
│   │
│   └── logger.info(f"User {message.from_user.username} send /photo command")
│
├── Получение списка файлов фотографий
│   │
│   └── photo_files = os.listdir(config.PHOTO_DIR)
│
├── Выбор случайной фотографии
│   │
│   └── random_photo = random.choice(photo_files)
│       └── photo_path = os.path.join(config.PHOTO_DIR, random_photo)
│
└── Отправка фотографии пользователю
    │
    └── with open(photo_path, 'rb') as photo:
        └── bot.send_photo(message.chat.id, photo)
```

### `handle_voice_message`

```python
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    """Обработка голосовых сообщений."""
    ...
```

**Назначение**: Обработка голосовых сообщений.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий голосовое сообщение.

**Как работает функция**:
1. Логирует информацию об отправке голосового сообщения.
2. Вызывает метод `handle_voice` класса `BotHandler` для обработки голосового сообщения.

```
Обработка голосового сообщения
│
├── Логирование отправки голосового сообщения
│   │
│   └── logger.info(f"User {message.from_user.username} send voice message")
│
└── Вызов метода handle_voice класса BotHandler
    │
    └── handler.handle_voice(bot, message)
```

### `handle_document_message`

```python
@bot.message_handler(content_types=['document'])
def handle_document_message(message):
    """Обработка полученных документов."""
    ...
```

**Назначение**: Обработка полученных документов.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий документ.

**Как работает функция**:
1. Логирует информацию об отправке документа.
2. Вызывает метод `handle_document` класса `BotHandler` для обработки документа.

```
Обработка полученного документа
│
├── Логирование отправки документа
│   │
│   └── logger.info(f"User {message.from_user.username} send document message")
│
└── Вызов метода handle_document класса BotHandler
    │
    └── handler.handle_document(bot, message)
```

### `handle_text_message`

```python
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message):
    """Обработка текстовых сообщений."""
    ...
```

**Назначение**: Обработка текстовых сообщений, не начинающихся с символа `/`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий текстовое сообщение.

**Как работает функция**:
1. Логирует информацию об отправке текстового сообщения.
2. Вызывает метод `handle_message` класса `BotHandler` для обработки текстового сообщения.

```
Обработка текстового сообщения
│
├── Логирование отправки текстового сообщения
│   │
│   └── logger.info(f"User {message.from_user.username} sent message: {message.text}")
│
└── Вызов метода handle_message класса BotHandler
    │
    └── handler.handle_message(bot, message)
```

### `handle_unknown_command`

```python
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message):
    """Обработка неизвестных команд."""
    ...
```

**Назначение**: Обработка неизвестных команд, начинающихся с символа `/`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий неизвестную команду.

**Как работает функция**:
1. Логирует информацию об отправке неизвестной команды.
2. Отправляет пользователю сообщение о неизвестной команде из конфигурации.

```
Обработка неизвестной команды
│
├── Логирование отправки неизвестной команды
│   │
│   └── logger.info(f"User {message.from_user.username} send unknown command: {message.text}")
│
└── Отправка сообщения о неизвестной команде
    │
    └── bot.send_message(message.chat.id, config.UNKNOWN_COMMAND_MESSAGE)