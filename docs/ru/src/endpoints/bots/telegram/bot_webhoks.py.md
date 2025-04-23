# Модуль telegram_webhooks

## Обзор

Модуль `telegram_webhooks` предоставляет реализацию Telegram-бота через сервер FastAPI с использованием RPC. Он включает в себя функциональность для обработки входящих сообщений, регистрации обработчиков команд и интеграции с Telegram API.

## Подробнее

Этот модуль является частью системы, которая позволяет взаимодействовать с Telegram-ботом через FastAPI, используя RPC для связи между компонентами. Модуль содержит класс `TelegramBot`, который управляет основными аспектами работы бота, такими как регистрация обработчиков, инициализация вебхука и запуск бота.

## Классы

### `TelegramBot`

**Описание**: Класс `TelegramBot` представляет собой интерфейс для взаимодействия с Telegram ботом. Он инициализирует бота, регистрирует обработчики команд и запускает вебхук для приема обновлений от Telegram.

**Атрибуты**:

- `token` (str): Токен Telegram бота.
- `port` (int): Порт для вебхука (по умолчанию 443).
- `route` (str): Маршрут для вебхука FastAPI (по умолчанию 'telegram_webhook').
- `config` (SimpleNamespace): Конфигурация бота, загруженная из файла `telegram.json`.
- `application` (Application): Объект `Application` из библиотеки `python-telegram-bot`, используемый для управления ботом.
- `handler` (BotHandler): Объект `BotHandler`, содержащий обработчики команд бота.

**Методы**:

- `__init__(self, token: str, route: str = 'telegram_webhook')`: Инициализирует экземпляр класса `TelegramBot`.
- `run(self)`: Запускает бота, инициализирует RPC и вебхук.
- `_register_default_handlers(self)`: Регистрирует обработчики команд по умолчанию, используя экземпляр `BotHandler`.
- `_handle_message(self, update: Update, context: CallbackContext) -> None`: Обрабатывает текстовые сообщения.
- `initialize_bot_webhook(self, route: str)`: Инициализирует вебхук бота.
- `_register_route_via_rpc(self, rpc_client: ServerProxy)`: Регистрирует маршрут вебхука Telegram через RPC.
- `stop(self)`: Останавливает бота и удаляет вебхук.

### `TelegramBot.__init__`

```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
    """
    Инициализирует экземпляр класса TelegramBot.

    Args:
        token (str): Токен Telegram бота.
        route (str): Webhook route для FastAPI. По умолчанию '/telegram_webhook'.
    """
    ...
```

### `TelegramBot.run`

```python
def run(self):
    """Запускает бота и инициализирует RPC и вебхук."""
    ...
```

### `TelegramBot._register_default_handlers`

```python
def _register_default_handlers(self):
    """Регистрирует обработчики команд по умолчанию, используя экземпляр BotHandler."""
    ...
```

### `TelegramBot._handle_message`

```python
async def _handle_message(self, update: Update, context: CallbackContext) -> None:
    """Обрабатывает любое текстовое сообщение."""
    ...
```

### `TelegramBot.initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
    """Инициализирует вебхук бота."""
    ...
```

### `TelegramBot._register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """Регистрирует маршрут вебхука Telegram через RPC."""
    ...
```

### `TelegramBot.stop`

```python
def stop(self):
    """Останавливает бота и удаляет вебхук."""
    ...
```

## Методы класса

### `_handle_message`

```python
async def _handle_message(self, update: Update, context: CallbackContext) -> None:
    """
    Функция обрабатывает текстовые сообщения, переданные боту.

    Args:
        update (Update): Объект `Update`, содержащий информацию о полученном обновлении от Telegram.
        context (CallbackContext): Объект `CallbackContext`, содержащий информацию о контексте обработки обновления.

    Returns:
        None

    
    - Вызывает метод `handle_message` объекта `self.bot_handler` для обработки полученного сообщения.

    """
    await self.bot_handler.handle_message(update, context)
```

### `initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
    """
    Инициализирует и устанавливает вебхук для Telegram бота.

    Args:
        route (str): Маршрут, по которому Telegram будет отправлять обновления.

    Returns:
        str | bool: URL вебхука в случае успешной установки, `False` в случае ошибки.

    
    - Формирует URL вебхука на основе переданного маршрута и хоста.
    - Если хост указывает на локальную машину (`127.0.0.1` или `localhost`), использует `ngrok` для создания публичного URL.
    - Пытается установить вебхук с использованием метода `set_webhook` объекта `self.application.bot`.
    - Логирует информацию об установке вебхука и возвращает URL вебхука в случае успеха или `False` в случае ошибки.
    """
    ...
```

### `_register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """
    Регистрирует маршрут вебхука Telegram через RPC (Remote Procedure Call).

    Args:
        rpc_client (ServerProxy): Объект для вызова удаленных процедур через RPC.

    Returns:
        None

    
    - Формирует маршрут, добавляя `/`, если он отсутствует.
    - Вызывает удаленную процедуру `add_new_route` через `rpc_client` для регистрации маршрута.
    - Логирует информацию об успешной регистрации маршрута или ошибке в случае неудачи.
    """
    ...
```

### `stop`

```python
def stop(self):
    """
    Останавливает бота и удаляет вебхук.

    Args:
        None

    Returns:
        None

    
    - Останавливает приложение с помощью метода `self.application.stop()`.
    - Удаляет вебхук, вызывая метод `delete_webhook()` объекта `self.application.bot`.
    - Логирует сообщение об остановке бота или информацию об ошибке в случае неудачи.
    """
    ...
```

## Параметры класса

- `token` (str): Токен Telegram бота, используемый для аутентификации бота в Telegram API.
- `route` (str): Маршрут для вебхука FastAPI, определяющий, по какому URL Telegram будет отправлять обновления. По умолчанию равен `'telegram_webhook'`.
- `port` (int): Порт, на котором будет прослушиваться вебхук. Используется для приема входящих сообщений от Telegram. По умолчанию равен `443`.

## Примеры

Пример инициализации и запуска бота:

```python
from dotenv import load_dotenv
import os

load_dotenv()
bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
bot.run()