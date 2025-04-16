## \\file /src/endpoints/bots/telegram/telegram_webhooks.py

# Модуль Telegram-бота с использованием FastAPI через RPC

```rst
.. module:: src.endpoints.bots.telegram.telegram_webhooks
    :platform: Windows, Unix
    :synopsis: Телеграм бот с сервером FAST API Через RPC

```

Этот модуль реализует Telegram-бота, который взаимодействует с сервером FAST API через RPC.

## Обзор

Модуль `src.endpoints.bots.telegram.telegram_webhooks` предоставляет реализацию Telegram-бота, использующего вебхуки для получения обновлений и RPC для взаимодействия с сервером FastAPI.

## Подробней

Модуль содержит класс `TelegramBot`, который инициализирует бота, регистрирует обработчики и запускает вебхук.

## Классы

### `TelegramBot`

**Описание**: Класс для управления Telegram-ботом.

**Атрибуты**:

*   `token` (str): Токен Telegram-бота.
*   `port` (int): Порт для вебхука (по умолчанию 443).
*   `route` (str): Маршрут для вебхука FastAPI (по умолчанию `'telegram_webhook'`).
*   `config` (SimpleNamespace): Конфигурация, загруженная из JSON-файла.
*   `bot` (Bot): Экземпляр класса `aiogram.Bot`.
*   `dp` (Dispatcher): Экземпляр класса `aiogram.Dispatcher`.
*   `bot_handler` (BotHandler): Экземпляр класса `BotHandler` для обработки сообщений.
*   `app` (Optional[web.Application]): Экземпляр веб-приложения `aiohttp.web.Application` (может быть `None`).
*   `rpc_client` (Optional[ServerProxy]): Экземпляр клиента RPC для взаимодействия с сервером FastAPI (может быть `None`).

**Методы**:

*   `__init__(self, token: str, route: str = 'telegram_webhook')`: Инициализирует объект `TelegramBot`.
*   `run(self)`: Запускает бота, инициализирует RPC и вебхук.
*   `_register_default_handlers(self)`: Регистрирует обработчики по умолчанию, используя экземпляр класса `BotHandler`.
*   `_handle_message(self, update: Update, context: CallbackContext) -> None`: Обрабатывает текстовые сообщения.
*   `initialize_bot_webhook(self, route: str)`: Инициализирует вебхук бота.
*   `_register_route_via_rpc(self, rpc_client: ServerProxy)`: Регистрирует маршрут Telegram webhook через RPC.
*   `stop(self)`: Останавливает бота и удаляет вебхук.

## Методы класса `TelegramBot`

### `__init__`

```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
```

**Назначение**: Инициализирует объект `TelegramBot`.

**Параметры**:

*   `token` (str): Токен Telegram-бота.
*   `route` (str, optional): Маршрут для вебхука FastAPI. Defaults to `'telegram_webhook'`.

**Как работает функция**:

1.  Сохраняет токен и маршрут.
2.  Загружает конфигурацию из JSON-файла.
3.  Создает экземпляры классов `aiogram.Bot` и `aiogram.Dispatcher`.
4.  Создает экземпляр класса `BotHandler`.
5.  Регистрирует обработчики по умолчанию.

### `run`

```python
def run(self):
```

**Назначение**: Запускает бота, инициализирует RPC и вебхук.

**Как работает функция**:

1.  Инициализирует RPC-клиент для взаимодействия с сервером FastAPI.
2.  Регистрирует маршрут через RPC.
3.  Инициализирует вебхук Telegram-бота.
4.  Запускает веб-приложение `aiohttp` для обработки вебхуков или запускает бота в режиме опроса (polling), если не удалось инициализировать вебхук.

### `_register_default_handlers`

```python
def _register_default_handlers(self):
```

**Назначение**: Регистрирует обработчики по умолчанию, используя экземпляр класса `BotHandler`.

**Как работает функция**:

1.  Регистрирует обработчики для команд `/start`, `/help` и `/sendpdf`.
2.  Регистрирует обработчики для текстовых и голосовых сообщений, а также документов.

### `_handle_message`

```python
async def _handle_message(self, update: Update, context: CallbackContext) -> None:
```

**Назначение**: Обрабатывает текстовые сообщения.

**Параметры**:

*   `update` (Update): Объект обновления Telegram.
*   `context` (CallbackContext): Контекст обратного вызова.

**Как работает функция**:

1.  Вызывает метод `handle_message` объекта `bot_handler` для обработки сообщения.

### `initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
```

**Назначение**: Инициализирует вебхук бота.

**Параметры**:

*   `route` (str): Маршрут для вебхука.

**Как работает функция**:

1.  Формирует URL вебхука.
2.  Использует `requests.post` для отправки запроса на указанный webhook_url
3.  Устанавливает вебхук, используя метод `bot.set_webhook`.

### `_register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
```

**Назначение**: Регистрирует маршрут Telegram webhook через RPC.

**Параметры**:

*   `rpc_client` (ServerProxy): Экземпляр клиента RPC.

**Как работает функция**:

1.  Регистрирует маршрут на сервере FastAPI, используя метод `rpc_client.add_new_route`.

### `stop`

```python
def stop(self):
```

**Назначение**: Останавливает бота и удаляет вебхук.

**Как работает функция**:

1.  Останавливает приложение.
2.  Удаляет вебхук Telegram, используя метод `bot.delete_webhook`.

## Запуск бота

Для запуска бота необходимо:

1.  Установить необходимые библиотеки, указанные в `requirements.txt`.
2.  Задать токен Telegram-бота в переменной окружения `TELEGRAM_TOKEN`.
3.  Запустить файл `telegram_webhooks.py`.

После запуска бот будет доступен в Telegram, и пользователи смогут взаимодействовать с ним, отправляя команды и сообщения.