# Модуль для управления Telegram ботом через long polling
## Обзор

Модуль `bot_long_polling.py` предназначен для создания и управления Telegram ботом. Он включает в себя настройку обработчиков команд и сообщений, а также обеспечивает взаимодействие с пользователем через Telegram API.
## Подробнее

Этот модуль содержит класс `TelegramBot`, который инициализирует бота, регистрирует обработчики команд и сообщений, а также предоставляет методы для замены обработчиков сообщений. В модуле используются библиотеки `telegram`, `telegram.ext`, `asyncio`, `logging`, а также пользовательские модули `src.endpoints.bots.telegram.handlers`, `src.logger.logger`, `requests`, `src.utils.convertors.tts`, `src.utils.file`.

## Классы

### `TelegramBot`

**Описание**: Класс для управления Telegram ботом.

**Атрибуты**:
- `application` (Application): Экземпляр приложения Telegram.
- `handler` (BotHandler): Экземпляр обработчика бота.
- `_original_message_handler` (MessageHandler): Оригинальный обработчик текстовых сообщений.

**Методы**:
- `__init__(token: str)`: Инициализирует экземпляр класса `TelegramBot`.
- `register_handlers() -> None`: Регистрирует обработчики команд и сообщений бота.
- `replace_message_handler(new_handler: Callable) -> None`: Заменяет текущий обработчик текстовых сообщений на новый.
- `start(update: Update, context: CallbackContext) -> None`: Обрабатывает команду `/start`.

### `__init__`
```python
def __init__(self, token: str):
    """Initialize the Telegram bot.

    Args:
        token (str): Telegram bot token, e.g., `gs.credentials.telegram.bot.kazarinov`.
    """
    self.application = Application.builder().token(token).build()
    self.handler = BotHandler() # Инициализация обработчика в конструкторе
    self._original_message_handler = None
    self.register_handlers()
```
**Назначение**: Инициализация Telegram бота.

**Параметры**:
- `token` (str): Telegram bot token.

**Как работает функция**:
- Создает экземпляр приложения `Application` с использованием предоставленного токена.
- Инициализирует обработчик `BotHandler`.
- Регистрирует обработчики.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_BOT_TOKEN')
```

### `register_handlers`
```python
def register_handlers(self) -> None:
    """Register bot commands and message handlers."""
    self.application.add_handler(CommandHandler('start', self.handler.start))
    self.application.add_handler(CommandHandler('help', self.handler.help_command))
    self.application.add_handler(CommandHandler('sendpdf', self.handler.send_pdf))

    # Сохраняем ссылку
    self._original_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handler.handle_message)
    self.application.add_handler(self._original_message_handler)

    self.application.add_handler(MessageHandler(filters.VOICE, self.handler.handle_voice))
    self.application.add_handler(MessageHandler(filters.Document.ALL, self.handler.handle_document))
```
**Назначение**: Регистрация обработчиков команд и сообщений бота.

**Как работает функция**:
- Добавляет обработчики для команд `/start`, `/help` и `/sendpdf`.
- Регистрирует обработчик для текстовых сообщений, исключая команды.
- Регистрирует обработчики для голосовых сообщений и документов.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_BOT_TOKEN')
bot.register_handlers()
```

### `replace_message_handler`
```python
def replace_message_handler(self, new_handler: Callable) -> None:
    """
    Заменяет текущий обработчик текстовых сообщений на новый.

    Args:
        new_handler (Callable): Новая функция для обработки сообщений.
    """
    # 2. Удаляем старый обработчик
    if self._original_message_handler in self.application.handlers[0]:
        self.application.handlers[0].remove(self._original_message_handler)

    # 3. Создаем новый обработчик
    self._original_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, new_handler)
    # 4. Регистрируем новый обработчик
    self.application.add_handler(self._original_message_handler)
```

**Назначение**: Заменяет текущий обработчик текстовых сообщений на новый.

**Параметры**:
- `new_handler` (Callable): Новая функция для обработки сообщений.

**Как работает функция**:
- Удаляет старый обработчик текстовых сообщений.
- Создает новый обработчик текстовых сообщений с использованием предоставленной функции.
- Регистрирует новый обработчик.

**Примеры**:
```python
def my_new_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('New handler activated!')

bot = TelegramBot(token='YOUR_BOT_TOKEN')
bot.replace_message_handler(my_new_handler)
```

### `start`
```python
async def start(self, update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    logger.info(f"Bot started by user {update.effective_user.id}")
    await update.message.reply_text('Hello! I am your simple bot. Type /help to see available commands.')
```

**Назначение**: Обработка команды `/start`.

**Параметры**:
- `update` (Update): Объект обновления Telegram.
- `context` (CallbackContext): Контекст обратного вызова.

**Как работает функция**:
- Логирует информацию о пользователе, запустившем бота.
- Отправляет приветственное сообщение пользователю.

**Примеры**:
```python
# Пример использования внутри обработчика команды start
async def start(self, update: Update, context: CallbackContext) -> None:
    logger.info(f"Bot started by user {update.effective_user.id}")
    await update.message.reply_text('Hello! I am your simple bot. Type /help to see available commands.')