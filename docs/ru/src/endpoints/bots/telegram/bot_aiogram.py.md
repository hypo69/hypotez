# Модуль `bot_aiogram.py`: Телеграм бот через FastAPI и RPC

## Обзор

Модуль реализует телеграм-бота, взаимодействующего с сервером FastAPI через RPC. Он использует библиотеку `aiogram` для обработки логики бота и `xmlrpc.client` для взаимодействия с RPC-сервером.

## Подробнее

Этот модуль создает экземпляр телеграм-бота, регистрирует обработчики команд и сообщений, инициализирует вебхук для получения обновлений от телеграма и запускает RPC-клиент для взаимодействия с сервером. Он также обеспечивает возможность остановки бота и удаления вебхука.

## Классы

### `TelegramBot`

**Описание**: Класс, представляющий интерфейс телеграм-бота, реализованный как Singleton.

**Атрибуты**:
- `token` (str): Токен телеграм-бота.
- `port` (int): Порт для вебхука (по умолчанию 443).
- `route` (str): Маршрут для вебхука FastAPI (по умолчанию 'telegram_webhook').
- `config` (SimpleNamespace): Конфигурация бота, загруженная из JSON-файла.
- `bot` (Bot): Экземпляр бота aiogram.
- `dp` (Dispatcher): Диспетчер aiogram.
- `bot_handler` (BotHandler): Обработчик команд и сообщений бота.
- `app` (Optional[web.Application]): Веб-приложение aiohttp для обработки вебхуков.
- `rpc_client` (Optional[ServerProxy]): RPC-клиент для взаимодействия с сервером.

**Методы**:
- `__init__(token: str, route: str = 'telegram_webhook')`: Инициализирует экземпляр `TelegramBot`.
- `run()`: Запускает бота, инициализирует RPC и вебхук.
- `_register_default_handlers()`: Регистрирует обработчики команд по умолчанию.
- `_handle_message(message: types.Message)`: Обрабатывает текстовые сообщения.
- `initialize_bot_webhook(route: str)`: Инициализирует вебхук бота.
- `_register_route_via_rpc(rpc_client: ServerProxy)`: Регистрирует маршрут вебхука телеграм через RPC.
- `stop()`: Останавливает бота и удаляет вебхук.

### `__init__`

```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
    """
    Инициализирует экземпляр TelegramBot.

    Args:
        token (str): Токен телеграм-бота.
        route (str): Маршрут вебхука для FastAPI. По умолчанию '/telegram_webhook'.
    """
    ...
```

### `run`

```python
def run(self):
    """
    Запускает бота и инициализирует RPC и вебхук.
    """
    ...
```
**Как работает функция**:
- Инициализируется RPC-клиент для взаимодействия с сервером по порту 9000.
- Запускается RPC-сервер.
- Инициализируется вебхук телеграм-бота.
- Регистрируется маршрут через RPC.
- Запускается веб-приложение aiohttp для обработки вебхуков.
- Если не удалось инициализировать вебхук, запускается polling.

### `_register_default_handlers`

```python
def _register_default_handlers(self):
    """
    Регистрирует обработчики команд по умолчанию, используя экземпляр BotHandler.
    """
    ...
```

**Как работает функция**:
Регистрирует обработчики для команд `/start`, `/help`, `/sendpdf`, а также обработчики для голосовых сообщений, документов, текстовых сообщений и логов.

### `_handle_message`

```python
async def _handle_message(self, message: types.Message):
    """
    Обрабатывает любое текстовое сообщение.

    Args:
        message (types.Message): Объект сообщения.
    """
    ...
```

**Как работает функция**:
Передает сообщение обработчику `handle_message` из `BotHandler`.

### `initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
    """
    Инициализирует вебхук бота.

    Args:
        route (str): Маршрут для вебхука.

    Returns:
        str | bool: URL вебхука в случае успеха, `False` в случае ошибки.
    """
    ...
```

**Как работает функция**:
- Формирует URL вебхука на основе переданного маршрута и хоста.
- Если хост - localhost, использует ngrok для создания туннеля.
- Устанавливает вебхук для бота.
- Возвращает URL вебхука в случае успеха, `False` в случае ошибки.

### `_register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """
    Регистрирует маршрут вебхука телеграм через RPC.

    Args:
        rpc_client (ServerProxy): RPC-клиент.
    """
    ...
```

**Как работает функция**:
Регистрирует маршрут вебхука через RPC-клиент, используя метод `add_new_route`.

### `stop`

```python
def stop(self):
    """
    Останавливает бота и удаляет вебхук.
    """
    ...
```

**Как работает функция**:
- Останавливает веб-приложение aiohttp, если оно запущено.
- Удаляет вебхук телеграм-бота.

## Примеры

```python
from dotenv import load_dotenv
import os
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot

load_dotenv()
bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
bot.run()
```
## Анализ структуры

-  `src.endpoints.bots.telegram.telegram_webhooks` - указывает на расположение модуля в структуре проекта. Это телеграм бот, который реализован с использованием `FastAPI` и `RPC`.
-  Импортируется `header`, `gs`, `bot_handlers`, `logger`, `j_loads_ns`, которые используются в коде. Ранее они были подробно проанализированны и сейчас используются.
- Класс `TelegramBot` инкапсулирует в себе всю логику телеграм бота
- Метод `_register_route_via_rpc` указывает на то, что вебхук регистрируется через RPC, что позволяет взаимодействовать с другими частями системы