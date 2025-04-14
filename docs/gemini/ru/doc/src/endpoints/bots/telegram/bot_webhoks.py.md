# Модуль для управления Telegram-ботом через FastAPI с использованием RPC
=====================================================================

Модуль `telegram_webhooks` предоставляет класс `TelegramBot`, который позволяет запускать Telegram-бота, интегрированного с сервером FastAPI через RPC.

## Обзор

Модуль содержит класс `TelegramBot`, предназначенный для управления Telegram-ботом через сервер FastAPI с использованием RPC. Он включает в себя настройку вебхуков, регистрацию обработчиков команд и сообщений, а также взаимодействие с сервером FastAPI для обработки входящих запросов.

## Подробнее

Этот модуль обеспечивает взаимодействие между Telegram-ботом и сервером FastAPI. Он использует RPC для регистрации маршрутов и запуска сервера, а также предоставляет функциональность для обработки различных типов сообщений от пользователей Telegram. Модуль также включает в себя механизм для автоматической настройки вебхуков с использованием ngrok, если бот запускается локально.

## Классы

### `TelegramBot`

**Описание**: Класс для управления Telegram-ботом через FastAPI с использованием RPC.

**Атрибуты**:
- `token` (str): Токен Telegram-бота.
- `port` (int): Порт для вебхука. По умолчанию 443.
- `route` (str): Маршрут вебхука для FastAPI. По умолчанию 'telegram_webhook'.
- `config` (SimpleNamespace): Конфигурация бота, загруженная из файла `telegram.json`.
- `application` (Application): Экземпляр класса `Application` из библиотеки `telegram.ext`.
- `handler` (BotHandler): Экземпляр класса `BotHandler` для обработки команд и сообщений.

**Методы**:
- `__init__(self, token: str, route: str = 'telegram_webhook')`: Инициализирует экземпляр класса `TelegramBot`.
- `run(self)`: Запускает бота, инициализирует RPC и вебхук.
- `_register_default_handlers(self)`: Регистрирует обработчики команд по умолчанию.
- `_handle_message(self, update: Update, context: CallbackContext) -> None`: Обрабатывает текстовые сообщения.
- `initialize_bot_webhook(self, route: str)`: Инициализирует вебхук бота.
- `_register_route_via_rpc(self, rpc_client: ServerProxy)`: Регистрирует маршрут вебхука Telegram через RPC.
- `stop(self)`: Останавливает бота и удаляет вебхук.

#### `__init__`
```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
    """
    Инициализирует экземпляр класса `TelegramBot`.

    Args:
        token (str): Токен Telegram-бота.
        route (str): Webhook route for FastAPI. Defaults to '/telegram_webhook'.
    """
    ...
```
**Назначение**: Инициализация экземпляра класса `TelegramBot`.
**Параметры**:
- `token` (str): Токен Telegram-бота.
- `route` (str, optional): Маршрут вебхука для FastAPI. По умолчанию '/telegram_webhook'.

**Как работает функция**:
- Присваивает значения атрибутам экземпляра класса.
- Загружает конфигурацию из файла `telegram.json` с использованием `j_loads_ns`.
- Создает экземпляр `Application` из библиотеки `telegram.ext`.
- Создает экземпляр `BotHandler` для обработки команд и сообщений.
- Вызывает метод `_register_default_handlers` для регистрации обработчиков команд по умолчанию.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN', route='/custom_route')
```

#### `run`
```python
def run(self):
    """Запускает бота и инициализирует RPC и вебхук."""
    ...
```
**Назначение**: Запускает бота, инициализирует RPC и вебхук.

**Как работает функция**:
- Инициализирует RPC клиент для взаимодействия с сервером FastAPI.
- Запускает сервер через RPC.
- Регистрирует маршрут через RPC, добавляя новый маршрут для обработки входящих сообщений от Telegram.
- Инициализирует вебхук Telegram-бота.
- Запускает приложение `telegram.ext.Application` в режиме вебхука или опрашивает сервер, если не удалось установить вебхук.
- Логирует успешный запуск сервера и приложения, а также возможные ошибки при инициализации.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.run()
```

#### `_register_default_handlers`
```python
def _register_default_handlers(self):
    """Регистрирует обработчики команд по умолчанию, используя экземпляр BotHandler."""
    ...
```
**Назначение**: Регистрирует обработчики команд по умолчанию, используя экземпляр `BotHandler`.

**Как работает функция**:
- Добавляет обработчики команд `start`, `help`, `sendpdf` к приложению `telegram.ext.Application`.
- Добавляет обработчики для текстовых сообщений, голосовых сообщений и документов.
- Использует `MessageHandler` для фильтрации сообщений по типу и регистрации соответствующих обработчиков из экземпляра `BotHandler`.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot._register_default_handlers()
```

#### `_handle_message`
```python
async def _handle_message(self, update: Update, context: CallbackContext) -> None:
    """Обрабатывает любое текстовое сообщение."""
    ...
```
**Назначение**: Обрабатывает любое текстовое сообщение.

**Параметры**:
- `update` (Update): Объект `Update` от Telegram.
- `context` (CallbackContext): Контекст обратного вызова.

**Как работает функция**:
- Вызывает метод `handle_message` из экземпляра `BotHandler` для обработки текстового сообщения.

**Примеры**:
```python
# Пример использования внутри обработчика
await bot._handle_message(update, context)
```

#### `initialize_bot_webhook`
```python
def initialize_bot_webhook(self, route: str):
    """Инициализирует вебхук бота."""
    ...
```
**Назначение**: Инициализирует вебхук бота.

**Параметры**:
- `route` (str): Маршрут вебхука.

**Как работает функция**:
- Формирует URL вебхука на основе хоста и маршрута.
- Если хост `127.0.0.1` или `localhost`, использует `ngrok` для создания туннеля.
- Устанавливает вебхук для бота с использованием `self.application.bot.set_webhook`.
- Логирует URL для получения информации о вебхуке.
- Возвращает URL вебхука или `False` в случае ошибки.

**Примеры**:
```python
webhook_url = bot.initialize_bot_webhook(route='/telegram_webhook')
```

#### `_register_route_via_rpc`
```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """Регистрирует маршрут вебхука Telegram через RPC."""
    ...
```
**Назначение**: Регистрирует маршрут вебхука Telegram через RPC.

**Параметры**:
- `rpc_client` (ServerProxy): RPC клиент.

**Как работает функция**:
- Формирует маршрут вебхука.
- Вызывает метод `add_new_route` через RPC для регистрации маршрута на сервере FastAPI.
- Логирует успешную регистрацию маршрута или ошибку в случае неудачи.

**Примеры**:
```python
bot._register_route_via_rpc(rpc_client)
```

#### `stop`
```python
def stop(self):
    """Останавливает бота и удаляет вебхук."""
    ...
```
**Назначение**: Останавливает бота и удаляет вебхук.

**Как работает функция**:
- Останавливает приложение `telegram.ext.Application`.
- Удаляет вебхук для бота.
- Логирует остановку бота и возможные ошибки при удалении вебхука.

**Примеры**:
```python
bot.stop()
```

## Области применения

- Создание и управление Telegram-ботами, интегрированными с сервером FastAPI.
- Автоматическая настройка вебхуков для обработки сообщений от пользователей Telegram.
- Регистрация маршрутов для обработки входящих запросов через RPC.