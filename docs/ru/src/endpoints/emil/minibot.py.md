# Модуль `minibot.py`

## Обзор

Модуль представляет собой простой Telegram-бот, предназначенный для обработки запросов, связанных с сайтом emil-design.com. Он использует библиотеку `telebot` для взаимодействия с Telegram API, а также включает функциональность для обработки текста, URL-адресов, голосовых сообщений и документов. Бот способен взаимодействовать с Google Gemini для генерации ответов на текстовые запросы.

## Подробнее

Бот обрабатывает различные типы сообщений, включая текстовые команды, URL-адреса, голосовые сообщения и документы. Он может отправлять ответы на текстовые запросы, обрабатывать URL-адреса, извлекать информацию из OneTab, выполнять сценарии на основе полученных данных, а также обрабатывать голосовые сообщения и документы.

## Классы

### `BotHandler`

**Описание**: Класс `BotHandler` предназначен для обработки команд, полученных от Telegram-бота. Он содержит методы для обработки текстовых сообщений, URL-адресов, команды "/next", голосовых сообщений и документов.

**Атрибуты**:

- `base_dir` (Path): Базовая директория для хранения файлов, связанных с ботом.
- `scenario` (Scenario): Экземпляр класса `Scenario` для выполнения различных сценариев.
- `model` (GoogleGenerativeAi): Экземпляр класса `GoogleGenerativeAi` для взаимодействия с моделью Google Gemini.
- `questions_list` (List[str]): Список вопросов, используемых для обработки команды "/next".

**Методы**:

- `handle_message(bot: telebot, message: 'message')`: Обрабатывает текстовые сообщения.
- `_send_user_flowchart(bot, chat_id)`: Отправляет схему user_flowchart.
- `_handle_url(bot, message: 'message')`: Обрабатывает URL, присланный пользователем.
- `_handle_next_command(bot, message)`: Обрабатывает команду '--next' и её аналоги.
- `help_command(bot, message)`: Обрабатывает команду /help.
- `send_pdf(bot, message, pdf_file)`: Обрабатывает команду /sendpdf для отправки PDF.
- `handle_voice(bot, message)`: Обрабатывает голосовые сообщения.
- `_transcribe_voice(file_path)`: Транскрибирование голосового сообщения (заглушка).
- `handle_document(bot, message)`: Обрабатывает полученные документы.

### `Config`

**Описание**: dataclass, определяющий параметры конфигурации бота.

**Атрибуты**:

- `BOT_TOKEN` (str): Токен Telegram-бота, получаемый из переменной окружения или базы данных.
- `CHANNEL_ID` (str): ID канала Telegram.
- `PHOTO_DIR` (Path): Путь к директории с фотографиями.
- `COMMAND_INFO` (str): Информация о боте, отображаемая по команде `/info`.
- `UNKNOWN_COMMAND_MESSAGE` (str): Сообщение об неизвестной команде.
- `START_MESSAGE` (str): Сообщение, отправляемое при старте бота.
- `HELP_MESSAGE` (str): Сообщение со списком доступных команд.

## Методы класса `BotHandler`

### `handle_message`

```python
def handle_message(self, bot: telebot, message: 'message'):
    """Обработка текстовых сообщений.

    Args:
        bot (telebot): Экземпляр бота telebot.
        message (message): Объект сообщения от пользователя.

    Raises:
        Exception: Если происходит ошибка при взаимодействии с моделью.
    """
```

**Назначение**: Метод обрабатывает текстовые сообщения, полученные от пользователя. Если сообщение содержит "?", отправляется схема user_flowchart. Если сообщение содержит URL, вызывается метод `_handle_url`. Если сообщение содержит команду для запроса следующего вопроса, вызывается метод `_handle_next_command`. В противном случае сообщение отправляется в модель для получения ответа, который затем отправляется пользователю.
Если во время обработки возникает ошибка, она логируется, и пользователю отправляется сообщение об ошибке.

**Как работает функция**:
- Извлекается текст сообщения.
- Проверяется, является ли текст командой "?", URL-адресом или командой для запроса следующего вопроса.
- В зависимости от типа сообщения вызывается соответствующий метод для обработки.
- Если сообщение не является командой или URL-адресом, оно отправляется в модель для получения ответа.
- Полученный ответ отправляется пользователю.

```python
def handle_message(self, bot: telebot, message: 'message'):
    text = message.text
    if text == '?':
        self._send_user_flowchart(bot, message.chat.id)
    elif is_url(text):
        self._handle_url(bot, message)
    elif text in ('--next', '-next', '__next', '-n', '-q'):
        self._handle_next_command(bot, message)
    else:
        try:
            answer = self.model.chat(text)
            bot.send_message(message.chat.id, answer)
        except Exception as ex:
            logger.error(f"Error during model interaction: {ex}")
            bot.send_message(message.chat.id, "Произошла ошибка при обработке сообщения.")
```

**Примеры**:

```python
# Пример обработки сообщения с текстом "?"
# Бот отправляет схему user_flowchart пользователю.

# Пример обработки сообщения с URL-адресом
# Бот обрабатывает URL-адрес и отправляет информацию пользователю.

# Пример обработки сообщения с командой "--next"
# Бот отправляет следующий вопрос пользователю.

# Пример обработки обычного текстового сообщения
# Бот отправляет сообщение в модель для получения ответа, который затем отправляется пользователю.
```

### `_send_user_flowchart`

```python
def _send_user_flowchart(self, bot, chat_id):
    """Отправка схемы user_flowchart.

    Args:
        bot (telebot): Экземпляр бота telebot.
        chat_id (int): ID чата для отправки сообщения.
    """
```

**Назначение**: Метод отправляет схему `user_flowchart` пользователю. Схема загружается из файла `user_flowchart.png`, расположенного в директории `assets`. Если файл не найден, логируется ошибка, и пользователю отправляется сообщение об ошибке.

**Как работает функция**:
- Формируется путь к файлу `user_flowchart.png`.
- Файл открывается в режиме чтения байтов.
- Схема отправляется пользователю с использованием метода `send_photo` объекта `bot`.

```python
def _send_user_flowchart(self, bot, chat_id):
    photo_path = self.base_dir / 'assets' / 'user_flowchart.png'
    try:
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id, photo)
    except FileNotFoundError as ex:
        logger.error(f"File not found: {photo_path} {ex}")
        bot.send_message(chat_id, "Схема не найдена.")
```

**Примеры**:

```python
# Пример отправки схемы user_flowchart пользователю с ID чата 123456789
# _send_user_flowchart(bot, 123456789)
```

### `_handle_url`

```python
def _handle_url(self, bot, message: 'message'):
    """Обработка URL, присланного пользователем.

    Args:
        bot (telebot): Экземпляр бота telebot.
        message (message): Объект сообщения от пользователя.

    Raises:
        Exception: Если происходит ошибка при получении данных из OneTab или при выполнении сценария.
    """
```

**Назначение**: Метод обрабатывает URL-адрес, присланный пользователем. Если URL не начинается с `https://one-tab.com` или `https://www.one-tab.com`, пользователю отправляется сообщение об ошибке. В противном случае из URL извлекаются данные (цена, название товара, список URL комплектующих) с использованием функции `fetch_target_urls_onetab`. Если данные получены успешно, пользователю отправляется сообщение с информацией о товаре. Затем выполняется сценарий с использованием полученных данных.
Если во время обработки возникает ошибка, она логируется, и пользователю отправляется сообщение об ошибке.

**Как работает функция**:
- Извлекается URL-адрес из сообщения.
- Проверяется, начинается ли URL-адрес с `https://one-tab.com` или `https://www.one-tab.com`.
- Если URL-адрес не соответствует ожидаемому формату, пользователю отправляется сообщение об ошибке.
- В противном случае из URL-адреса извлекаются данные с использованием функции `fetch_target_urls_onetab`.
- Если данные получены успешно, пользователю отправляется сообщение с информацией о товаре.
- Выполняется сценарий с использованием полученных данных.

```python
def _handle_url(self, bot, message: 'message'):
    url = message.text
    if not url.startswith(('https://one-tab.com', 'https://www.one-tab.com')):
        bot.send_message(message.chat.id, 'Мне на вход нужен URL `https://one-tab.com` Проверь, что ты мне посылаешь')
        return

    try:
       price, mexiron_name, urls = fetch_target_urls_onetab(url)
       bot.send_message(message.chat.id, f'Получил мехирон {mexiron_name} - {price} шек')
    except Exception as ex:
        logger.error(f"Error fetching URLs from OneTab: {ex}")
        bot.send_message(message.chat.id, "Произошла ошибка при получении данных из OneTab.")
        return
    if not urls:
        bot.send_message(message.chat.id, 'Некорректные данные. Не получил список URL комплектующих')
        return

    try:
        asyncio.run(
            self.scenario.run_scenario(
                    bot=bot,
                    chat_id=message.chat.id,
                    urls=list(urls), 
                    price=price,
                    mexiron_name=mexiron_name
            ))

    except Exception as ex:
        logger.error(f"Error during scenario execution: {ex}")
        bot.send_message(message.chat.id, f"Произошла ошибка при выполнении сценария. {print(ex.args)}")
```

**Примеры**:

```python
# Пример обработки URL-адреса "https://one-tab.com/XXXXXXXXX"
# Бот извлекает данные из URL-адреса и отправляет информацию пользователю.
# Затем выполняется сценарий с использованием полученных данных.
```

### `_handle_next_command`

```python
def _handle_next_command(self, bot, message):
    """Обработка команды '--next' и её аналогов.

    Args:
        bot (telebot): Экземпляр бота telebot.
        message (message): Объект сообщения от пользователя.

    Raises:
        Exception: Если происходит ошибка при чтении вопросов.
    """
```

**Назначение**: Метод обрабатывает команду '--next' и её аналоги. Метод выбирает случайный вопрос из списка `self.questions_list`, отправляет его пользователю, а затем запрашивает ответ у модели и отправляет его пользователю.
Если во время обработки возникает ошибка, она логируется, и пользователю отправляется сообщение об ошибке.

**Как работает функция**:
- Выбирается случайный вопрос из списка `self.questions_list`.
- Вопрос отправляется пользователю.
- Запрашивается ответ у модели на выбранный вопрос.
- Ответ отправляется пользователю.

```python
def _handle_next_command(self, bot, message):
    try:
        question = random.choice(self.questions_list)
        answer = self.model.ask(question)
        bot.send_message(message.chat.id, question)
        bot.send_message(message.chat.id, answer)
    except Exception as ex:
        logger.error(f'Ошибка чтения вопросов: {ex}')
        bot.send_message(message.chat.id, 'Произошла ошибка при чтении вопросов.')
```

**Примеры**:

```python
# Пример обработки команды "--next"
# Бот выбирает случайный вопрос, отправляет его пользователю, а затем отправляет ответ на этот вопрос.
```

### `help_command`

```python
def help_command(self, bot, message):
    """Обработка команды /help.

    Args:
        bot (telebot): Экземпляр бота telebot.
        message (message): Объект сообщения от пользователя.
    """
```

**Назначение**: Метод обрабатывает команду `/help`. Метод отправляет пользователю сообщение со списком доступных команд и их описанием.

**Как работает функция**:
- Формируется сообщение со списком доступных команд и их описанием.
- Сообщение отправляется пользователю.

```python
def help_command(self, bot, message):
    bot.send_message(
        message.chat.id,
        'Available commands:\n'
        '/start - Start the bot\n'
        '/help - Show this help message\n'
        '/sendpdf - Send a PDF file'
    )
```

**Примеры**:

```python
# Пример обработки команды "/help"
# Бот отправляет сообщение со списком доступных команд и их описанием.
```

### `send_pdf`

```python
def send_pdf(self, bot, message, pdf_file):
    """Обработка команды /sendpdf для отправки PDF.

    Args:
        bot (telebot): Экземпляр бота telebot.
        message (message): Объект сообщения от пользователя.
        pdf_file (str): Путь к PDF-файлу.

    Raises:
        Exception: Если происходит ошибка при отправке PDF-файла.
    """
```

**Назначение**: Метод обрабатывает команду `/sendpdf` для отправки PDF-файла пользователю. Метод открывает PDF-файл в режиме чтения байтов и отправляет его пользователю с использованием метода `send_document` объекта `bot`.
Если во время обработки возникает ошибка, она логируется, и пользователю отправляется сообщение об ошибке.

**Как работает функция**:
- Открывается PDF-файл в режиме чтения байтов.
- PDF-файл отправляется пользователю с использованием метода `send_document` объекта `bot`.

```python
def send_pdf(self, bot, message, pdf_file):
    try:
        with open(pdf_file, 'rb') as pdf_file_obj:
            bot.send_document(message.chat.id, document=pdf_file_obj)
    except Exception as ex:
        logger.error(f'Ошибка при отправке PDF-файла: {ex}')
        bot.send_message(message.chat.id, 'Произошла ошибка при отправке PDF-файла. Попробуй ещё раз.')
```

**Примеры**:

```python
# Пример обработки команды "/sendpdf"
# Бот отправляет PDF-файл "example.pdf" пользователю.
# send_pdf(bot, message, "example.pdf")
```

### `handle_voice`

```python
def handle_voice(self, bot, message):
    """Обработка голосовых сообщений.

    Args:
        bot (telebot): Экземпляр бота telebot.
        message (message): Объект сообщения от пользователя.

    Raises:
        Exception: Если происходит ошибка при обработке голосового сообщения.
    """
```

**Назначение**: Метод обрабатывает голосовые сообщения, полученные от пользователя. Метод получает информацию о файле голосового сообщения, скачивает файл, сохраняет его во временный файл, транскрибирует голосовое сообщение (с использованием заглушки `_transcribe_voice`) и отправляет распознанный текст пользователю.
Если во время обработки возникает ошибка, она логируется, и пользователю отправляется сообщение об ошибке.

**Как работает функция**:
- Получается информация о файле голосового сообщения.
- Файл скачивается с использованием метода `download_file` объекта `bot`.
- Файл сохраняется во временный файл.
- Голосовое сообщение транскрибируется с использованием заглушки `_transcribe_voice`.
- Распознанный текст отправляется пользователю.

```python
def handle_voice(self, bot, message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)
        file_path = gs.path.temp / f'{message.voice.file_id}.ogg'
        with open(file_path, 'wb') as f:
            f.write(file)
        transcribed_text = self._transcribe_voice(file_path)
        bot.send_message(message.chat.id, f'Распознанный текст: {transcribed_text}')
    except Exception as ex:
        logger.error(f'Ошибка при обработке голосового сообщения: {ex}')
        bot.send_message(message.chat.id, 'Произошла ошибка при обработке голосового сообщения. Попробуй ещё раз.')
```

**Примеры**:

```python
# Пример обработки голосового сообщения
# Бот скачивает голосовое сообщение, сохраняет его во временный файл,
# транскрибирует его и отправляет распознанный текст пользователю.
```

### `_transcribe_voice`

```python
def _transcribe_voice(self, file_path):
    """Транскрибирование голосового сообщения (заглушка).

    Args:
        file_path (str): Путь к файлу голосового сообщения.

    Returns:
        str: Распознанный текст (в данном случае - заглушка).
    """
```

**Назначение**: Метод транскрибирует голосовое сообщение. В текущей реализации метод является заглушкой и возвращает сообщение о том, что распознавание голоса ещё не реализовано.

**Как работает функция**:
- Возвращается сообщение о том, что распознавание голоса ещё не реализовано.

```python
def _transcribe_voice(self, file_path):
    return 'Распознавание голоса ещё не реализовано.'
```

**Примеры**:

```python
# Пример транскрибирования голосового сообщения
# Метод возвращает сообщение о том, что распознавание голоса ещё не реализовано.
```

### `handle_document`

```python
def handle_document(self, bot, message):
    """Обработка полученных документов.

    Args:
        bot (telebot): Экземпляр бота telebot.
        message (message): Объект сообщения от пользователя.

    Returns:
        bool: True в случае успешной обработки, False в случае ошибки.

    Raises:
        Exception: Если происходит ошибка при обработке документа.
    """
```

**Назначение**: Метод обрабатывает полученные от пользователя документы. Метод получает информацию о файле документа, скачивает файл, сохраняет его во временный файл и отправляет пользователю сообщение о том, что файл сохранен.
Если во время обработки возникает ошибка, она логируется, и пользователю отправляется сообщение об ошибке.

**Как работает функция**:
- Получается информация о файле документа.
- Файл скачивается с использованием метода `download_file` объекта `bot`.
- Файл сохраняется во временный файл.
- Пользователю отправляется сообщение о том, что файл сохранен.

```python
def handle_document(self, bot, message):
    try:
        file_info = bot.get_file(message.document.file_id)
        file = bot.download_file(file_info.file_path)
        tmp_file_path = gs.path.temp / message.document.file_name
        with open(tmp_file_path, 'wb') as f:
            f.write(file)
        bot.send_message(message.chat.id, f'Файл сохранен в {tmp_file_path}')
        return True
    except Exception as ex:
        logger.error(f'Ошибка при обработке документа: {ex}')
        bot.send_message(message.chat.id, 'Произошла ошибка при обработке документа. Попробуй ещё раз.')
        return False
```

**Примеры**:

```python
# Пример обработки документа
# Бот скачивает документ, сохраняет его во временный файл и отправляет пользователю сообщение о том, что файл сохранен.
```

## Параметры класса `Config`

- `BOT_TOKEN` (str): Токен Telegram-бота. Получается из переменной окружения `TELEGRAM_BOT_TOKEN` если `USE_ENV` имеет значение `True`, иначе берется из `gs.credentials.telegram.hypo69_emil_design_bot`.
- `CHANNEL_ID` (str): ID Telegram-канала.
- `PHOTO_DIR` (Path): Путь к директории с фотографиями. Определяется как `__root__ / 'endpoints' / 'kazarinov' / 'assets'`.
- `COMMAND_INFO` (str): Информация о боте, отображаемая по команде `/info`.
- `UNKNOWN_COMMAND_MESSAGE` (str): Сообщение об неизвестной команде.
- `START_MESSAGE` (str): Сообщение, отправляемое при старте бота.
- `HELP_MESSAGE` (str): Сообщение со списком доступных команд.

## Обработчики сообщений

### `command_start`

```python
@bot.message_handler(commands=['start'])
def command_start(message):
    """Обработка команды /start.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик команды `/start`. Отправляет пользователю приветственное сообщение, хранящееся в `config.START_MESSAGE`.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Отправляет приветственное сообщение пользователю, используя `bot.send_message`.

**Примеры**:

```python
# Пользователь отправляет команду /start
# Бот отвечает приветственным сообщением.
```

### `command_help`

```python
@bot.message_handler(commands=['help'])
def command_help(message):
    """Обработка команды /help.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик команды `/help`. Вызывает метод `help_command` класса `BotHandler` для отображения справки.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Вызывает метод `handler.help_command` для отправки справки.

**Примеры**:

```python
# Пользователь отправляет команду /help
# Бот отображает список доступных команд.
```

### `command_info`

```python
@bot.message_handler(commands=['info'])
def command_info(message):
    """Обработка команды /info.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик команды `/info`. Отправляет пользователю информацию о боте, хранящуюся в `config.COMMAND_INFO`.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Отправляет информацию о боте пользователю, используя `bot.send_message`.

**Примеры**:

```python
# Пользователь отправляет команду /info
# Бот отвечает информацией о боте.
```

### `command_time`

```python
@bot.message_handler(commands=['time'])
def command_time(message):
    """Обработка команды /time.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик команды `/time`. Отправляет пользователю текущее время.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Получает текущее время.
- Отправляет текущее время пользователю, используя `bot.send_message`.

**Примеры**:

```python
# Пользователь отправляет команду /time
# Бот отвечает текущим временем.
```

### `command_photo`

```python
@bot.message_handler(commands=['photo'])
def command_photo(message):
    """Обработка команды /photo.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик команды `/photo`. Отправляет пользователю случайную фотографию из директории `config.PHOTO_DIR`.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Получает список файлов в директории с фотографиями.
- Выбирает случайную фотографию.
- Отправляет фотографию пользователю, используя `bot.send_photo`.

**Примеры**:

```python
# Пользователь отправляет команду /photo
# Бот отправляет случайную фотографию.
```

### `handle_voice_message`

```python
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    """Обработка голосовых сообщений.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик голосовых сообщений. Вызывает метод `handle_voice` класса `BotHandler` для обработки голосового сообщения.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Вызывает метод `handler.handle_voice` для обработки голосового сообщения.

**Примеры**:

```python
# Пользователь отправляет голосовое сообщение
# Бот обрабатывает голосовое сообщение.
```

### `handle_document_message`

```python
@bot.message_handler(content_types=['document'])
def handle_document_message(message):
    """Обработка сообщений с документами.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик сообщений с документами. Вызывает метод `handle_document` класса `BotHandler` для обработки документа.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Вызывает метод `handler.handle_document` для обработки документа.

**Примеры**:

```python
# Пользователь отправляет документ
# Бот обрабатывает документ.
```

### `handle_text_message`

```python
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text_message(message):
    """Обработка текстовых сообщений, не начинающихся с '/'.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик текстовых сообщений, не начинающихся с `/`. Вызывает метод `handle_message` класса `BotHandler` для обработки текстового сообщения.
Сообщение о том, какой пользователь написал логируется.

**Как работает функция**:
- Вызывает метод `handler.handle_message` для обработки текстового сообщения.

**Примеры**:

```python
# Пользователь отправляет текстовое сообщение
# Бот обрабатывает текстовое сообщение.
```

### `handle_unknown_command`

```python
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/'))
def handle_unknown_command(message):
    """Обработка неизвестных команд.

    Args:
        message (telebot.types.Message): Объект сообщения от пользователя.
    """
```

**Назначение**: Обработчик неизвестных команд. Отправляет пользователю сообщение об неизвестной команде, хранящееся в `config.UNKNOWN_COMMAND_MESSAGE`.
Сообщение о том, какой пользователь вызвал команду логируется.

**Как работает функция**:
- Отправляет сообщение об неизвестной команде пользователю, используя `bot.send_message`.

**Примеры**:

```python
# Пользователь отправляет неизвестную команду
# Бот отвечает сообщением об неизвестной команде.