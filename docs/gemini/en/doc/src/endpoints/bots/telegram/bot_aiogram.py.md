# Модуль `bot_aiogram.py`

## Обзор

Модуль `bot_aiogram.py` реализует телеграм-бота с использованием фреймворка `aiogram` и сервера `FastAPI` через `RPC`. Он обеспечивает взаимодействие с пользователями через телеграм, обрабатывает команды и сообщения, а также поддерживает интеграцию с другими сервисами через удаленный вызов процедур (RPC).

## Более подробно

Этот модуль создает экземпляр телеграм-бота, регистрирует обработчики команд и сообщений, настраивает вебхук для получения обновлений от телеграма и запускает `FastAPI`-сервер для обработки входящих запросов.

## Классы

### `TelegramBot`

**Описание**:
Класс `TelegramBot` представляет собой интерфейс телеграм-бота. Он инициализирует бота, регистрирует обработчики, настраивает вебхук и управляет жизненным циклом бота.

**Атрибуты**:
- `token` (str): Токен телеграм-бота.
- `port` (int): Порт для вебхука (по умолчанию 443).
- `route` (str): Маршрут вебхука для `FastAPI` (по умолчанию `telegram_webhook`).
- `config` (SimpleNamespace): Конфигурация бота, загруженная из файла `telegram.json`.
- `bot` (Bot): Экземпляр бота `aiogram`.
- `dp` (Dispatcher): Диспетчер `aiogram` для обработки обновлений.
- `bot_handler` (BotHandler): Обработчик команд и сообщений бота.
- `app` (Optional[web.Application]): Веб-приложение `aiohttp` для вебхука.
- `rpc_client` (Optional[ServerProxy]): RPC-клиент для взаимодействия с сервером.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `TelegramBot`.
- `run`: Запускает бота, инициализирует `RPC` и вебхук.
- `_register_default_handlers`: Регистрирует обработчики команд по умолчанию.
- `_handle_message`: Обрабатывает текстовые сообщения.
- `initialize_bot_webhook`: Инициализирует вебхук бота.
- `_register_route_via_rpc`: Регистрирует маршрут телеграм-вебхука через `RPC`.
- `stop`: Останавливает бота и удаляет вебхук.

### `TelegramBot.__init__`

```python
    def __init__(self, token: str, route: str = 'telegram_webhook'):
        """
        Инициализация экземпляра класса TelegramBot.

        Args:
            token (str): Токен телеграм-бота.
            route (str): Webhook route for FastAPI. Defaults to '/telegram_webhook'.
        """
```

**Параметры**:
- `token` (str): Токен телеграм-бота.
- `route` (str): Маршрут вебхука для `FastAPI`. По умолчанию '/telegram_webhook'.

**Описание работы**:
- Инициализирует атрибуты экземпляра класса, включая токен, маршрут, конфигурацию, бота, диспетчер, обработчик бота, веб-приложение и `RPC`-клиент.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN', route='/custom_webhook')
```

### `TelegramBot.run`

```python
    def run(self):
        """Запуск бота и инициализация RPC и вебхука."""
```

**Описание работы**:
- Пытается инициализировать `RPC`-клиент и запустить `RPC`-сервер.
- Инициализирует вебхук телеграм-бота.
- Регистрирует маршрут через `RPC`.
- Запускает веб-приложение для обработки вебхука или запускает поллинг, если не удалось установить вебхук.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
bot.run()
```

### `TelegramBot._register_default_handlers`

```python
    def _register_default_handlers(self):
        """Регистрация обработчиков по умолчанию с использованием экземпляра BotHandler."""
```

**Описание работы**:
- Регистрирует обработчики команд `/start`, `/help`, `/sendpdf`, а также обработчики текстовых сообщений, голосовых сообщений и документов.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
bot._register_default_handlers()
```

### `TelegramBot._handle_message`

```python
    async def _handle_message(self, message: types.Message):
        """Обработка любого текстового сообщения."""
```

**Параметры**:
- `message` (types.Message): Объект сообщения от `aiogram`.

**Описание работы**:
- Вызывает метод `handle_message` у экземпляра `BotHandler` для обработки текстового сообщения.

**Примеры**:
```python
async def some_function(message: types.Message):
    bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
    await bot._handle_message(message)
```

### `TelegramBot.initialize_bot_webhook`

```python
    def initialize_bot_webhook(self, route: str):
        """Инициализация вебхука бота."""
```

**Параметры**:
- `route` (str): Маршрут вебхука.

**Описание работы**:
- Формирует URL вебхука на основе хоста и маршрута.
- Если хост локальный, использует `ngrok` для создания публичного URL.
- Устанавливает вебхук для бота и возвращает URL вебхука.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
webhook_url = bot.initialize_bot_webhook(route='/telegram_webhook')
```

### `TelegramBot._register_route_via_rpc`

```python
    def _register_route_via_rpc(self, rpc_client: ServerProxy):
        """Регистрация маршрута телеграм-вебхука через RPC."""
```

**Параметры**:
- `rpc_client` (ServerProxy): `RPC`-клиент.

**Описание работы**:
- Регистрирует маршрут телеграм-вебхука через `RPC`-сервер.

**Примеры**:
```python
from xmlrpc.client import ServerProxy
rpc_client = ServerProxy(f"http://{gs.host}:{port}", allow_none=True)
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
bot._register_route_via_rpc(rpc_client)
```

### `TelegramBot.stop`

```python
    def stop(self):
        """Остановка бота и удаление вебхука."""
```

**Описание работы**:
- Останавливает веб-приложение и удаляет вебхук телеграм-бота.

**Примеры**:
```python
bot = TelegramBot(token='YOUR_TELEGRAM_TOKEN')
bot.stop()
```

## Запуск бота

```python
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
    bot.run()
```

**Описание работы**:
- Загружает переменные окружения из файла `.env`.
- Создает экземпляр класса `TelegramBot` с использованием токена из переменной окружения `TELEGRAM_TOKEN`.
- Запускает бота.

**Примеры**:
Установите `TELEGRAM_TOKEN` в `.env` файл и запустите скрипт.
```bash
TELEGRAM_TOKEN=YOUR_TELEGRAM_TOKEN python src/endpoints/bots/telegram/bot_aiogram.py