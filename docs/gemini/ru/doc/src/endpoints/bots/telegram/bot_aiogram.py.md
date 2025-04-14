# Модуль для работы с Telegram ботом через FastAPI и RPC
====================================================

Модуль содержит класс :class:`TelegramBot`, который используется для создания и управления Telegram ботом.
Бот интегрирован с FastAPI для обработки входящих запросов и использует RPC для взаимодействия с другими сервисами.

Пример использования
----------------------

```python
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()
bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
bot.run()
```

## Обзор

Этот модуль реализует Telegram-бота, интегрированного с FastAPI для обработки входящих webhook-запросов и использующего RPC (Remote Procedure Call) для связи с другими частями системы.

## Подробнее

Модуль `bot_aiogram.py` содержит класс `TelegramBot`, который отвечает за создание, запуск и остановку Telegram-бота. Класс использует библиотеку `aiogram` для работы с Telegram API, `aiohttp` для создания веб-приложения и `xmlrpc.client` для взаимодействия по RPC. 

Бот может работать как через webhook, так и через long polling. Webhook используется, когда бот работает на сервере с публичным IP-адресом, а long polling — когда бот работает на локальной машине или за NAT.

## Классы

### `TelegramBot`

**Описание**: Класс для управления Telegram ботом.

**Атрибуты**:
- `token` (str): Токен Telegram бота.
- `route` (str): Маршрут для webhook. По умолчанию `/telegram_webhook`.
- `port` (int): Порт для веб-приложения. По умолчанию `443`.
- `config` (SimpleNamespace): Конфигурация бота, загруженная из файла `telegram.json`.
- `bot` (Bot): Экземпляр класса `Bot` из библиотеки `aiogram`.
- `dp` (Dispatcher): Экземпляр класса `Dispatcher` из библиотеки `aiogram`.
- `bot_handler` (BotHandler): Экземпляр класса `BotHandler`, обрабатывающий сообщения бота.
- `app` (Optional[web.Application]): Веб-приложение `aiohttp`.
- `rpc_client` (Optional[ServerProxy]): RPC клиент для взаимодействия с сервером.

**Методы**:
- `__init__(self, token: str, route: str = 'telegram_webhook')`: Инициализирует экземпляр класса `TelegramBot`.
- `run(self)`: Запускает бота и инициализирует RPC и webhook.
- `_register_default_handlers(self)`: Регистрирует обработчики по умолчанию.
- `_handle_message(self, message: types.Message)`: Обрабатывает текстовые сообщения.
- `initialize_bot_webhook(self, route: str)`: Инициализирует webhook бота.
- `_register_route_via_rpc(self, rpc_client: ServerProxy)`: Регистрирует маршрут webhook через RPC.
- `stop(self)`: Останавливает бота и удаляет webhook.

#### `__init__`

```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
    """
    Initialize the TelegramBot instance.

    Args:
        token (str): Telegram bot token.
        route (str): Webhook route for FastAPI. Defaults to '/telegram_webhook'.
    """
    ...
```

**Назначение**: Инициализация экземпляра класса `TelegramBot`.

**Параметры**:
- `token` (str): Токен Telegram бота.
- `route` (str, optional): Маршрут для webhook. По умолчанию `/telegram_webhook`.

**Как работает функция**:

1.  Сохраняет переданные значения `token` и `route` в атрибуты экземпляра класса.
2.  Устанавливает `port` равным 443.
3.  Загружает конфигурацию из файла `telegram.json` с помощью `j_loads_ns` и сохраняет её в атрибуте `config`.
4.  Создаёт экземпляры `Bot` и `Dispatcher` из библиотеки `aiogram` и сохраняет их в атрибутах `bot` и `dp` соответственно.
5.  Создаёт экземпляр `BotHandler` и сохраняет его в атрибуте `bot_handler`.
6.  Регистрирует обработчики по умолчанию, вызывая метод `_register_default_handlers`.
7.  Инициализирует атрибуты `app` и `rpc_client` значением `None`.

**Примеры**:

```python
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
bot = TelegramBot(token=token, route='/my_custom_route')
```

#### `run`

```python
def run(self):
    """Run the bot and initialize RPC and webhook."""
    ...
```

**Назначение**: Запуск бота и инициализация RPC и webhook.

**Как работает функция**:

1.  Инициализирует RPC клиент, используя `ServerProxy` для подключения к RPC серверу. Порт RPC сервера определяется как 9000.
2.  Запускает RPC сервер, вызывая метод `start_server` через RPC клиент.
3.  Инициализирует Telegram bot webhook, вызывая метод `initialize_bot_webhook`.
4.  Если `webhook_url` получен успешно, регистрирует маршрут через RPC, вызывая метод `_register_route_via_rpc`.
5.  Создаёт веб-приложение `aiohttp` и регистрирует обработчик webhook, используя `SimpleRequestHandler`.
6.  Запускает веб-приложение, используя `web.run_app`.
7.  Если `webhook_url` не получен, запускает бота в режиме long polling, используя `dp.start_polling`.
8.  Логирует информацию об успешном запуске сервера и ошибках, используя модуль `logger`.

**Параметры**:
- Отсутствуют

**Примеры**:

```python
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
bot = TelegramBot(token=token)
bot.run()
```

#### `_register_default_handlers`

```python
def _register_default_handlers(self):
    """Register the default handlers using the BotHandler instance."""
    ...
```

**Назначение**: Регистрация обработчиков по умолчанию с использованием экземпляра `BotHandler`.

**Как работает функция**:

1.  Регистрирует обработчик команды `/start`, вызывая метод `start` из `bot_handler`.
2.  Регистрирует обработчик команды `/help`, вызывая метод `help_command` из `bot_handler`.
3.  Регистрирует обработчик команды `/sendpdf`, вызывая метод `send_pdf` из `bot_handler`.
4.  Регистрирует обработчик текстовых сообщений, вызывая метод `_handle_message`.
5.  Регистрирует обработчик голосовых сообщений, вызывая метод `handle_voice` из `bot_handler`.
6.  Регистрирует обработчик документов, вызывая метод `handle_document` из `bot_handler`.
7.  Регистрирует обработчик логирования, вызывая метод `handle_log` из `bot_handler`.

**Параметры**:
- Отсутствуют

**Примеры**:

```python
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
bot = TelegramBot(token=token)
bot._register_default_handlers()
```

#### `_handle_message`

```python
async def _handle_message(self, message: types.Message):
    """Handle any text message."""
    ...
```

**Назначение**: Обработка любого текстового сообщения.

**Параметры**:
- `message` (types.Message): Объект сообщения от Telegram.

**Как работает функция**:

1.  Вызывает метод `handle_message` из `bot_handler`, передавая объект сообщения.

**Примеры**:

```python
from aiogram import types
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
bot = TelegramBot(token=token)

async def test_handle_message():
    message = types.Message(message_id=1, from_user=types.User(id=1, is_bot=False, first_name="Test"), chat=types.Chat(id=1, type="private"), date=1, text="Test message")
    await bot._handle_message(message)

asyncio.run(test_handle_message())
```

#### `initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
    """Initialize the bot webhook."""
    ...
```

**Назначение**: Инициализация webhook бота.

**Параметры**:
- `route` (str): Маршрут для webhook.

**Как работает функция**:

1.  Формирует URL для webhook, используя переданный маршрут и хост.
2.  Если хост — `127.0.0.1` или `localhost`, использует `ngrok` для создания публичного URL.
3.  Устанавливает webhook для бота, используя метод `set_webhook` из `aiogram`.
4.  Логирует информацию об успешной установке webhook или ошибке, используя модуль `logger`.

**Примеры**:

```python
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
bot = TelegramBot(token=token)
webhook_url = bot.initialize_bot_webhook(route='/my_custom_route')
```

#### `_register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """Register the Telegram webhook route via RPC."""
    ...
```

**Назначение**: Регистрация маршрута Telegram webhook через RPC.

**Параметры**:
- `rpc_client` (ServerProxy): RPC клиент для взаимодействия с сервером.

**Как работает функция**:

1.  Формирует маршрут для webhook.
2.  Вызывает метод `add_new_route` через RPC клиент для регистрации маршрута на сервере.
3.  Логирует информацию об успешной регистрации маршрута или ошибке, используя модуль `logger`.

**Примеры**:

```python
from xmlrpc.client import ServerProxy
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
bot = TelegramBot(token=token)
rpc_client = ServerProxy(f"http://{gs.host}:9000", allow_none=True)
bot._register_route_via_rpc(rpc_client)
```

#### `stop`

```python
def stop(self):
    """Stop the bot and delete the webhook."""
    ...
```

**Назначение**: Остановка бота и удаление webhook.

**Как работает функция**:

1.  Выключает и очищает веб-приложение, если оно существует.
2.  Удаляет webhook, используя метод `delete_webhook` из `aiogram`.
3.  Логирует информацию об успешной остановке бота или ошибке, используя модуль `logger`.

**Параметры**:
- Отсутствуют

**Примеры**:

```python
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
bot = TelegramBot(token=token)
bot.stop()