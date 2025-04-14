# Модуль для работы с Telegram ботом (long polling)

## Обзор

Модуль `bot_long_polling.py` содержит класс `TelegramBot`, который обеспечивает интерфейс для взаимодействия с Telegram ботом. Он отвечает за регистрацию обработчиков команд и сообщений, а также за обработку различных типов входящих данных, таких как текст, голосовые сообщения и документы.

## Подробней

Этот модуль является ключевым компонентом для интеграции Telegram бота в проект `hypotez`. Он использует библиотеку `telegram.ext` для обработки взаимодействий с ботом и включает в себя обработчики для основных команд, таких как `/start` и `/help`, а также для обработки текстовых и голосовых сообщений, и документов. Модуль также предоставляет функциональность для замены обработчика текстовых сообщений во время выполнения, что позволяет динамически изменять поведение бота.

## Классы

### `TelegramBot`

**Описание**: Класс `TelegramBot` предоставляет интерфейс для взаимодействия с Telegram ботом. Он инициализирует бота, регистрирует обработчики команд и сообщений, а также предоставляет методы для управления обработчиками.

**Атрибуты**:
- `application` (Application): Экземпляр класса `Application` из библиотеки `telegram.ext`, который управляет ботом.
- `handler` (BotHandler): Экземпляр класса `BotHandler`, который содержит методы для обработки различных типов входящих данных.
- `_original_message_handler` (MessageHandler): Ссылка на оригинальный обработчик текстовых сообщений.

**Методы**:
- `__init__(token: str)`: Инициализирует Telegram бота.
- `register_handlers()`: Регистрирует обработчики команд и сообщений.
- `replace_message_handler(new_handler: Callable)`: Заменяет текущий обработчик текстовых сообщений на новый.
- `start(update: Update, context: CallbackContext)`: Обрабатывает команду `/start`.

### `TelegramBot.__init__(token: str)`

```python
def __init__(self, token: str):
    """Initialize the Telegram bot.

    Args:
        token (str): Telegram bot token, e.g., `gs.credentials.telegram.bot.kazarinov`.
    """
```

**Назначение**: Инициализирует экземпляр класса `TelegramBot`.

**Параметры**:
- `token` (str): Токен Telegram бота, полученный от BotFather.

**Как работает функция**:
- Создает экземпляр класса `Application` с использованием предоставленного токена.
- Инициализирует обработчик `BotHandler`.
- Регистрирует обработчики команд и сообщений.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
```

### `TelegramBot.register_handlers() -> None`

```python
def register_handlers(self) -> None:
    """Register bot commands and message handlers."""
```

**Назначение**: Регистрирует обработчики команд и сообщений для Telegram бота.

**Как работает функция**:
- Добавляет обработчики для команд `/start`, `/help` и `/sendpdf`, используя `CommandHandler`.
- Сохраняет ссылку на оригинальный обработчик текстовых сообщений `MessageHandler`.
- Добавляет обработчики для голосовых сообщений и документов, используя `MessageHandler`.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.register_handlers()
```

### `TelegramBot.replace_message_handler(new_handler: Callable) -> None`

```python
def replace_message_handler(self, new_handler: Callable) -> None:
    """
    Заменяет текущий обработчик текстовых сообщений на новый.

    Args:
        new_handler (Callable): Новая функция для обработки сообщений.
    """
```

**Назначение**: Заменяет текущий обработчик текстовых сообщений на новый.

**Параметры**:
- `new_handler` (Callable): Новая функция для обработки текстовых сообщений.

**Как работает функция**:
1. Проверяет, существует ли оригинальный обработчик сообщений.
2. Если оригинальный обработчик существует, удаляет его из списка обработчиков.
3. Создает новый обработчик сообщений с использованием предоставленной функции `new_handler`.
4. Регистрирует новый обработчик сообщений.

**Примеры**:
```python
def my_new_handler(update: Update, context: CallbackContext) -> None:
    """Новый обработчик текстовых сообщений."""
    update.message.reply_text('This is the new handler!')

bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.replace_message_handler(my_new_handler)
```

### `TelegramBot.start(update: Update, context: CallbackContext) -> None`

```python
async def start(self, update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
```

**Назначение**: Обрабатывает команду `/start`, отправляя приветственное сообщение пользователю.

**Параметры**:
- `update` (Update): Объект `Update`, представляющий входящее обновление от Telegram.
- `context` (CallbackContext): Объект `CallbackContext`, содержащий информацию о контексте вызова обработчика.

**Как работает функция**:
- Логирует информацию о запуске бота пользователем.
- Отправляет приветственное сообщение пользователю.

**Примеры**:
```python
# Пример вызова обработчика при получении команды /start
async def start_handler(update: Update, context: CallbackContext):
    await TelegramBot.start(update, context)