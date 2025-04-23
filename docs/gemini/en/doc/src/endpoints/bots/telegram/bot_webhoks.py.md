# Модуль telegram_webhooks

## Обзор

Модуль реализует телеграм-бота через сервер FastAPI с использованием RPC.

## Подробнее

Модуль содержит класс `TelegramBot`, который является интерфейсом для работы с телеграм-ботом.
Он инициализирует бота, регистрирует обработчики команд и сообщений, а также запускает вебхук для получения обновлений от Telegram.
Для взаимодействия с сервером FastAPI используется RPC.

## Классы

### `TelegramBot`

**Описание**:
Класс `TelegramBot` представляет собой интерфейс для работы с телеграм-ботом.

**Наследует**:
Класс не наследует от других классов.

**Атрибуты**:
- `token` (str): Токен телеграм-бота.
- `port` (int): Порт для вебхука. По умолчанию 443.
- `route` (str): Маршрут для вебхука FastAPI. По умолчанию 'telegram_webhook'.
- `config` (SimpleNamespace): Конфигурация бота, загружаемая из файла `telegram.json`.
- `application` (Application): Объект `Application` из библиотеки `python-telegram-bot`.
- `handler` (BotHandler): Обработчик бота, экземпляр класса `BotHandler`.

**Методы**:
- `__init__(self, token: str, route: str = 'telegram_webhook')`: Инициализирует экземпляр класса `TelegramBot`.
- `run(self)`: Запускает бота, инициализирует RPC и вебхук.
- `_register_default_handlers(self)`: Регистрирует обработчики команд по умолчанию, используя экземпляр `BotHandler`.
- `_handle_message(self, update: Update, context: CallbackContext) -> None`: Обрабатывает текстовые сообщения.
- `initialize_bot_webhook(self, route: str)`: Инициализирует вебхук бота.
- `_register_route_via_rpc(self, rpc_client: ServerProxy)`: Регистрирует маршрут Telegram webhook через RPC.
- `stop(self)`: Останавливает бота и удаляет вебхук.

### `TelegramBot.__init__`

```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
    """
    Initialize the TelegramBot instance.

    Args:
        token (str): Telegram bot token.
        route (str): Webhook route for FastAPI. Defaults to '/telegram_webhook'.
    """
```

**Описание**:
Инициализирует экземпляр класса `TelegramBot`.

**Параметры**:
- `token` (str): Токен телеграм-бота.
- `route` (str, optional): Маршрут для вебхука FastAPI. По умолчанию '/telegram_webhook'.

**Возвращает**:
- None

**Пример**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN', route='/custom_webhook')
```

### `TelegramBot.run`

```python
def run(self):
    """Run the bot and initialize RPC and webhook."""
```

**Описание**:
Запускает бота, инициализирует RPC и вебхук.

**Параметры**:
- None

**Возвращает**:
- None

**Как работает**:
- Инициализирует RPC клиент для связи с сервером FastAPI.
- Запускает сервер через RPC.
- Регистрирует маршрут через RPC для обработки вебхуков от Telegram.
- Инициализирует и запускает вебхук Telegram, либо запускает режим polling, если не удалось установить вебхук.

**Пример**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
bot.run()
```

### `TelegramBot._register_default_handlers`

```python
def _register_default_handlers(self):
    """Register the default handlers using the BotHandler instance."""
```

**Описание**:
Регистрирует обработчики команд по умолчанию, используя экземпляр `BotHandler`.

**Параметры**:
- None

**Возвращает**:
- None

**Как работает**:
- Добавляет обработчики для команд `/start`, `/help`, `/sendpdf`.
- Добавляет обработчики для текстовых сообщений, голосовых сообщений и документов.
- Использует экземпляр `BotHandler` для обработки сообщений.

**Пример**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
bot._register_default_handlers()
```

### `TelegramBot._handle_message`

```python
async def _handle_message(self, update: Update, context: CallbackContext) -> None:
    """Handle any text message."""
```

**Описание**:
Обрабатывает текстовые сообщения.

**Параметры**:
- `update` (Update): Объект `Update` от `python-telegram-bot`, содержащий информацию об обновлении.
- `context` (CallbackContext): Объект `CallbackContext` от `python-telegram-bot`, содержащий информацию о контексте.

**Возвращает**:
- None

**Как работает**:
- Вызывает метод `handle_message` у экземпляра `BotHandler` для обработки сообщения.

**Пример**:
```python
# Внутри обработчика
await bot._handle_message(update, context)
```

### `TelegramBot.initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
    """Initialize the bot webhook."""
```

**Описание**:
Инициализирует вебхук бота.

**Параметры**:
- `route` (str): Маршрут для вебхука.

**Возвращает**:
- `webhook_url` (str): URL вебхука, если успешно установлен.
- `False`: В случае ошибки.

**Как работает**:
- Формирует URL вебхука на основе хоста и маршрута.
- Если хост - localhost или 127.0.0.1, использует ngrok для создания публичного URL.
- Устанавливает вебхук для бота с использованием `application.bot.set_webhook`.
- Логирует информацию об установке вебхука.

**Пример**:
```python
webhook_url = bot.initialize_bot_webhook(route='/telegram_webhook')
```

### `TelegramBot._register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """Register the Telegram webhook route via RPC."""
```

**Описание**:
Регистрирует маршрут Telegram webhook через RPC.

**Параметры**:
- `rpc_client` (ServerProxy): Объект RPC клиента для взаимодействия с сервером FastAPI.

**Возвращает**:
- None

**Как работает**:
- Формирует маршрут для вебхука.
- Вызывает метод `add_new_route` на сервере FastAPI через RPC для регистрации маршрута.
- Логирует информацию о регистрации маршрута.

**Пример**:
```python
bot._register_route_via_rpc(rpc_client)
```

### `TelegramBot.stop`

```python
def stop(self):
    """Stop the bot and delete the webhook."""
```

**Описание**:
Останавливает бота и удаляет вебхук.

**Параметры**:
- None

**Возвращает**:
- None

**Как работает**:
- Останавливает приложение Telegram бота.
- Удаляет вебхук, установленный для бота.
- Логирует информацию об остановке бота.

**Пример**:
```python
bot.stop()
```

## Запуск бота

В блоке `if __name__ == "__main__":` выполняется запуск бота.
Загружаются переменные окружения из файла `.dotenv`, создается экземпляр класса `TelegramBot` и вызывается метод `run` для запуска бота.

```python
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
    bot.run()
```