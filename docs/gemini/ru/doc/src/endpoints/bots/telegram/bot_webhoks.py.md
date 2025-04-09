# Модуль для работы с Telegram ботом через FastAPI и RPC
====================================================

Модуль содержит класс :class:`TelegramBot`, который используется для взаимодействия с Telegram API,
регистрации обработчиков, запуска вебхука и обработки сообщений через FastAPI с использованием RPC.

Пример использования
----------------------

```python
from src.endpoints.bots.telegram.telegram_webhooks import TelegramBot
import os
from dotenv import load_dotenv
load_dotenv()
bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
bot.run()
```

## Обзор

Модуль `src.endpoints.bots.telegram.telegram_webhooks` предоставляет класс `TelegramBot` для создания и управления Telegram-ботом, использующим FastAPI для обработки входящих запросов через вебхуки и RPC для взаимодействия с другими сервисами.
Этот модуль обеспечивает регистрацию обработчиков команд и сообщений, инициализацию вебхука, а также запуск и остановку бота.

## Подробней

Этот модуль является частью системы, где Telegram-бот интегрирован с FastAPI для обеспечения обработки сообщений и команд. Класс `TelegramBot` управляет жизненным циклом бота, регистрирует обработчики,
инициализирует вебхук и взаимодействует с FastAPI через RPC. Он использует библиотеку `python-telegram-bot` для взаимодействия с Telegram API и `xmlrpc.client` для RPC-коммуникаций.

## Классы

### `TelegramBot`

**Описание**: Класс для управления Telegram-ботом.

**Атрибуты**:
- `token` (str): Токен Telegram-бота.
- `port` (int): Порт для вебхука. По умолчанию: 443.
- `route` (str): Маршрут вебхука для FastAPI. По умолчанию: 'telegram_webhook'.
- `config` (SimpleNamespace): Конфигурация бота, загруженная из JSON-файла.
- `application` (Application): Экземпляр приложения `telegram.ext.Application`.
- `handler` (BotHandler): Экземпляр класса `BotHandler` для обработки команд и сообщений.

**Методы**:
- `__init__(self, token: str, route: str = 'telegram_webhook')`: Инициализирует экземпляр класса `TelegramBot`.
- `run(self)`: Запускает бота, инициализирует RPC и вебхук.
- `_register_default_handlers(self)`: Регистрирует обработчики команд по умолчанию.
- `_handle_message(self, update: Update, context: CallbackContext) -> None`: Обрабатывает текстовые сообщения.
- `initialize_bot_webhook(self, route: str)`: Инициализирует вебхук бота.
- `_register_route_via_rpc(self, rpc_client: ServerProxy)`: Регистрирует маршрут вебхука через RPC.
- `stop(self)`: Останавливает бота и удаляет вебхук.

#### Принцип работы:

Класс `TelegramBot` является центральным элементом для управления Telegram-ботом в данном модуле. При инициализации класса загружается конфигурация бота, создается экземпляр `telegram.ext.Application`,
регистрируются обработчики команд и сообщений. Метод `run` запускает бота, инициализирует RPC для взаимодействия с сервером FastAPI и настраивает вебхук для приема входящих сообщений.
Для локальной разработки используется `ngrok` для создания публичного URL, который используется для вебхука.

## Методы класса

### `__init__`

```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
    """
    Инициализирует экземпляр класса TelegramBot.

    Args:
        token (str): Telegram bot token.
        route (str): Webhook route for FastAPI. Defaults to '/telegram_webhook'.
    """
```

**Назначение**: Инициализирует экземпляр класса `TelegramBot`.

**Параметры**:
- `token` (str): Токен Telegram-бота.
- `route` (str, optional): Маршрут вебхука для FastAPI. По умолчанию '/telegram_webhook'.

**Как работает функция**:
- Сохраняет токен бота и маршрут вебхука.
- Загружает конфигурацию бота из `telegram.json`.
- Инициализирует экземпляр `telegram.ext.Application` с использованием токена.
- Создает экземпляр класса `BotHandler`.
- Регистрирует обработчики команд по умолчанию.

### `run`

```python
def run(self):
    """Запускает бота и инициализирует RPC и вебхук."""
```

**Назначение**: Запускает бота, инициализирует RPC и вебхук.

**Как работает функция**:
- Инициализирует RPC-клиента для связи с сервером FastAPI.
- Вызывает RPC для запуска сервера FastAPI.
- Вызывает RPC для регистрации маршрута вебхука.
- Инициализирует вебхук Telegram-бота.
- Запускает приложение `telegram.ext.Application` с использованием вебхука.
- Логирует информацию о запуске сервера и приложения.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
bot.run()
```

### `_register_default_handlers`

```python
def _register_default_handlers(self):
    """Регистрирует обработчики команд по умолчанию, используя экземпляр BotHandler."""
```

**Назначение**: Регистрирует обработчики команд по умолчанию, используя экземпляр `BotHandler`.

**Как работает функция**:
- Добавляет обработчики команд `/start`, `/help`, `/sendpdf`.
- Добавляет обработчик текстовых сообщений.
- Добавляет обработчик голосовых сообщений.
- Добавляет обработчик документов.
- Добавляет обработчик для логирования сообщений.

### `_handle_message`

```python
async def _handle_message(self, update: Update, context: CallbackContext) -> None:
    """Обрабатывает любое текстовое сообщение."""
```

**Назначение**: Обрабатывает текстовые сообщения.

**Параметры**:
- `update` (Update): Объект `telegram.Update`, представляющий входящее сообщение.
- `context` (CallbackContext): Объект `telegram.ext.CallbackContext`, содержащий контекст обработчика.

**Как работает функция**:
- Вызывает метод `handle_message` экземпляра `BotHandler` для обработки сообщения.

### `initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
    """Инициализирует вебхук бота."""
```

**Назначение**: Инициализирует вебхук бота.

**Параметры**:
- `route` (str): Маршрут вебхука.

**Как работает функция**:
- Формирует URL вебхука на основе хоста и маршрута.
- Если хост локальный, использует `ngrok` для создания публичного URL.
- Устанавливает вебхук для бота с использованием полученного URL.
- Логирует информацию об установке вебхука.

**Возвращает**:
- `str`: URL вебхука в случае успеха.
- `False`: В случае ошибки.

### `_register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """Регистрирует маршрут вебхука Telegram через RPC."""
```

**Назначение**: Регистрирует маршрут вебхука Telegram через RPC.

**Параметры**:
- `rpc_client` (ServerProxy): RPC-клиент для связи с сервером FastAPI.

**Как работает функция**:
- Формирует маршрут вебхука.
- Вызывает RPC для добавления нового маршрута в FastAPI.
- Логирует информацию о регистрации маршрута.

### `stop`

```python
def stop(self):
    """Останавливает бота и удаляет вебхук."""
```

**Назначение**: Останавливает бота и удаляет вебхук.

**Как работает функция**:
- Останавливает приложение `telegram.ext.Application`.
- Удаляет вебхук бота.
- Логирует информацию об остановке бота.

## Примеры

**Инициализация и запуск бота**:

```python
from src.endpoints.bots.telegram.telegram_webhooks import TelegramBot
import os
from dotenv import load_dotenv
load_dotenv()
bot = TelegramBot(token=os.getenv('TELEGRAM_TOKEN'))
bot.run()