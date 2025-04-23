# Модуль `bot_aiogram.py`

## Обзор

Модуль предоставляет класс `TelegramBot` для создания и управления Telegram-ботом с использованием библиотеки `aiogram` и интеграции с сервером FastAPI через RPC. Он поддерживает обработку сообщений, команд и различных типов контента, а также установку и удаление вебхуков для получения обновлений от Telegram.

## Подробнее

Этот модуль является частью системы для интеграции Telegram-бота с другими компонентами системы через RPC. Он использует библиотеку `aiogram` для обработки Telegram API и `aiohttp` для создания веб-сервера, который принимает вебхуки от Telegram. RPC используется для связи с другими сервисами, такими как регистрация новых маршрутов для обработки сообщений.

## Классы

### `TelegramBot`

**Описание**: Класс для управления Telegram-ботом.

**Атрибуты**:

- `token` (str): Токен Telegram-бота.
- `port` (int): Порт для веб-сервера. По умолчанию `443`.
- `route` (str): Маршрут вебхука для FastAPI. По умолчанию `'telegram_webhook'`.
- `config` (SimpleNamespace): Конфигурация бота, загруженная из файла `telegram.json`.
- `bot` (Bot): Экземпляр бота aiogram.
- `dp` (Dispatcher): Диспетчер aiogram для обработки обновлений.
- `bot_handler` (BotHandler): Обработчик бота для обработки различных типов сообщений и команд.
- `app` (Optional[web.Application]): Веб-приложение aiohttp.
- `rpc_client` (Optional[ServerProxy]): RPC-клиент для взаимодействия с сервером.

**Методы**:

- `__init__(self, token: str, route: str = 'telegram_webhook')`: Инициализирует экземпляр класса `TelegramBot`.
- `run(self)`: Запускает бота, инициализирует RPC и вебхук.
- `_register_default_handlers(self)`: Регистрирует обработчики по умолчанию, используя экземпляр `BotHandler`.
- `_handle_message(self, message: types.Message)`: Обрабатывает любое текстовое сообщение.
- `initialize_bot_webhook(self, route: str)`: Инициализирует вебхук бота.
- `_register_route_via_rpc(self, rpc_client: ServerProxy)`: Регистрирует маршрут вебхука Telegram через RPC.
- `stop(self)`: Останавливает бота и удаляет вебхук.

## Методы класса

### `__init__`

```python
def __init__(self, token: str, route: str = 'telegram_webhook'):
    """
    Инициализирует экземпляр класса TelegramBot.

    Args:
        token (str): Токен Telegram-бота.
        route (str): Маршрут вебхука для FastAPI. По умолчанию '/telegram_webhook'.
    """
    self.token: str = token
    self.port: int = 443
    self.route: str = route
    self.config: SimpleNamespace = j_loads_ns(__root__ / 'src/endpoints/bots/telegram/telegram.json')
    self.bot: Bot = Bot(token=self.token)
    self.dp: Dispatcher = Dispatcher()
    self.bot_handler: BotHandler = BotHandler()
    self._register_default_handlers()
    self.app: Optional[web.Application] = None
    self.rpc_client: Optional[ServerProxy] = None
```

**Назначение**: Инициализация объекта `TelegramBot`.

**Параметры**:

- `token` (str): Токен, выданный Telegram боту.
- `route` (str): Маршрут для вебхука (по умолчанию: `'telegram_webhook'`).

**Как работает функция**:

- Функция инициализирует атрибуты класса, такие как токен, порт и маршрут вебхука.
- Загружает конфигурацию из файла `telegram.json` в объект `SimpleNamespace`.
- Создает экземпляры `Bot` и `Dispatcher` из библиотеки `aiogram`.
- Создает экземпляр класса `BotHandler`, который содержит обработчики для различных типов сообщений и команд.
- Регистрирует обработчики по умолчанию с помощью метода `_register_default_handlers`.
- Устанавливает атрибуты `app` и `rpc_client` в `None`.

**Примеры**:

```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN', route='/custom_webhook')
```

### `run`

```python
def run(self):
    """Запускает бота и инициализирует RPC и вебхук."""
    try:
        # Initialize RPC client
        port = 9000

        self.rpc_client = ServerProxy(f"http://{gs.host}:{port}", allow_none=True)

        # Start the server via RPC
        self.rpc_client.start_server(port, gs.host)

        # Register the route via RPC
        logger.success(f'RPC Server running at http://{gs.host}:{port}/')
    except Exception as ex:
        logger.error(f"Ошибка FastApiServer: ", ex, exc_info=True)
        sys.exit()

    # Initialize the Telegram bot webhook
    webhook_url = self.initialize_bot_webhook(self.route)

    if webhook_url:
        self._register_route_via_rpc(self.rpc_client)
        try:
            # Use web application for webhook
            self.app = web.Application()
            webhook_requests_handler = SimpleRequestHandler(
                dispatcher=self.dp,
                bot=self.bot,
            )

            webhook_requests_handler.register(self.app, path=self.route)
            setup_application(self.app, self.dp, bot=self.bot)
            web.run_app(self.app, host="0.0.0.0", port=self.port)
            logger.info(f"Application started: {self.bot.id}")

        except Exception as ex:
            logger.error(f"Ошибка установки вебхука: ", ex, exc_info=True)

    else:
        asyncio.run(self.dp.start_polling(self.bot))
```

**Назначение**: Запуск бота и инициализация RPC и вебхука.

**Как работает функция**:

- Пытается инициализировать RPC-клиент для взаимодействия с сервером.
    - Определяет порт для RPC-сервера (по умолчанию 9000).
    - Создает экземпляр `ServerProxy` для RPC-соединения.
    - Вызывает RPC-метод `start_server` для запуска сервера.
    - Логирует успешный запуск RPC-сервера.
- В случае ошибки при инициализации RPC-клиента, логирует ошибку и завершает работу программы.
- Инициализирует вебхук Telegram-бота.
    - Вызывает метод `initialize_bot_webhook` для установки вебхука и получения URL.
- Если URL вебхука получен успешно:
    - Регистрирует маршрут вебхука через RPC.
    - Создает веб-приложение `aiohttp` и регистрирует обработчик для приема запросов от Telegram.
    - Запускает веб-приложение на указанном порту (по умолчанию 443).
    - Логирует информацию о запуске приложения.
- Если не удалось установить вебхук, запускает бота в режиме опроса (polling).

**Примеры**:

```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.run()
```

### `_register_default_handlers`

```python
def _register_default_handlers(self):
    """Регистрирует обработчики по умолчанию, используя экземпляр BotHandler."""
    self.dp.message.register(self.bot_handler.start, Command('start'))
    self.dp.message.register(self.bot_handler.help_command, Command('help'))
    self.dp.message.register(self.bot_handler.send_pdf, Command('sendpdf'))
    self.dp.message.register(self._handle_message)
    self.dp.message.register(self.bot_handler.handle_voice, lambda message: message.voice is not None)
    self.dp.message.register(self.bot_handler.handle_document, lambda message: message.document is not None)
    self.dp.message.register(self.bot_handler.handle_log, lambda message: message.text is not None)
```

**Назначение**: Регистрация обработчиков по умолчанию для различных типов сообщений и команд.

**Как работает функция**:

- Регистрирует обработчики для следующих событий:
    - Команда `/start`: вызывает метод `start` из `bot_handler`.
    - Команда `/help`: вызывает метод `help_command` из `bot_handler`.
    - Команда `/sendpdf`: вызывает метод `send_pdf` из `bot_handler`.
    - Любое текстовое сообщение: вызывает метод `_handle_message`.
    - Голосовое сообщение: вызывает метод `handle_voice` из `bot_handler`.
    - Документ: вызывает метод `handle_document` из `bot_handler`.
    - Текстовое сообщение: вызывает метод `handle_log` из `bot_handler`.

**Примеры**:

```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot._register_default_handlers()
```

### `_handle_message`

```python
async def _handle_message(self, message: types.Message):
    """Обрабатывает любое текстовое сообщение."""
    await self.bot_handler.handle_message(message)
```

**Назначение**: Обработка любого текстового сообщения, полученного ботом.

**Параметры**:

- `message` (types.Message): Объект сообщения, полученный от Telegram.

**Как работает функция**:

- Передает сообщение на обработку в метод `handle_message` объекта `bot_handler`.

**Примеры**:

```python
# Пример вызова внутри класса TelegramBot при получении сообщения
async def on_message(self, message: types.Message):
    await self._handle_message(message)
```

### `initialize_bot_webhook`

```python
def initialize_bot_webhook(self, route: str):
    """Инициализирует вебхук бота."""
    route = route if route.startswith('/') else f'/{route}'
    host = gs.host

    if host in ('127.0.0.1', 'localhost'):
        from pyngrok import ngrok
        ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN", ""))
        http_tunnel = ngrok.connect(self.port)
        host = http_tunnel.public_url

    host = host if host.startswith('http') else f'https://{host}'
    webhook_url = f'{host}{route}'

    try:
        asyncio.run(self.bot.set_webhook(url=webhook_url))
        logger.success(f'https://api.telegram.org/bot{self.token}/getWebhookInfo')
        return webhook_url
    except Exception as ex:
        logger.error(f'Error setting webhook: ', ex, exc_info=True)
        return False
```

**Назначение**: Инициализация вебхука для Telegram-бота.

**Параметры**:

- `route` (str): Маршрут, по которому Telegram будет отправлять обновления.

**Как работает функция**:

- Формирует URL вебхука на основе переданного маршрута и хоста.
- Если хост указан как `127.0.0.1` или `localhost`, использует `ngrok` для создания публичного URL.
- Устанавливает вебхук для бота, используя метод `set_webhook` из библиотеки `aiogram`.
- Логирует успешную установку вебхука и возвращает URL вебхука.
- В случае ошибки логирует ошибку и возвращает `False`.

**Примеры**:

```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
webhook_url = bot.initialize_bot_webhook(route='/telegram_webhook')
if webhook_url:
    print(f"Webhook URL: {webhook_url}")
```

### `_register_route_via_rpc`

```python
def _register_route_via_rpc(self, rpc_client: ServerProxy):
    """Регистрирует маршрут вебхука Telegram через RPC."""
    try:
        route = self.route if self.route.startswith('/') else f'/{self.route}'
        rpc_client.add_new_route(
            route,
            'self.bot_handler.handle_message',
            ['POST']
        )
        logger.info(f"Route {self.route} registered via RPC.")
    except Exception as ex:
        logger.error(f"Failed to register route via RPC:", ex, exc_info=True)
```

**Назначение**: Регистрация маршрута вебхука Telegram через RPC.

**Параметры**:

- `rpc_client` (ServerProxy): Клиент RPC для взаимодействия с сервером.

**Как работает функция**:

- Формирует маршрут, добавляя `/` в начале, если это необходимо.
- Вызывает RPC-метод `add_new_route` для регистрации маршрута на сервере.
    - Передает маршрут, имя обработчика (`self.bot_handler.handle_message`) и метод (`POST`).
- Логирует успешную регистрацию маршрута.
- В случае ошибки логирует ошибку.

**Примеры**:

```python
# Пример вызова внутри класса TelegramBot после инициализации RPC-клиента
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.rpc_client = ServerProxy(f"http://{gs.host}:9000", allow_none=True)
bot._register_route_via_rpc(bot.rpc_client)
```

### `stop`

```python
def stop(self):
    """Останавливает бота и удаляет вебхук."""
    if self.app:
        asyncio.run(self.app.shutdown())
        asyncio.run(self.app.cleanup())
    try:
        asyncio.run(self.bot.delete_webhook())
        logger.info("Bot stopped.")
    except Exception as ex:
        logger.error(f'Error deleting webhook:', ex, exc_info=True)
```

**Назначение**: Остановка бота и удаление вебхука.

**Как работает функция**:

- Если веб-приложение `app` было создано, останавливает и очищает его.
- Пытается удалить вебхук, используя метод `delete_webhook` из библиотеки `aiogram`.
- Логирует информацию об остановке бота.
- В случае ошибки логирует ошибку.

**Примеры**:

```python
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.stop()
```

## Параметры класса

- `token` (str): Токен, выданный Telegram боту.
- `route` (str): Маршрут для вебхука (по умолчанию: `'telegram_webhook'`).
- `port` (int): Порт для веб-сервера (по умолчанию: 443).
- `config` (SimpleNamespace): Конфигурация бота, загруженная из файла `telegram.json`.
- `bot` (Bot): Экземпляр бота aiogram.
- `dp` (Dispatcher): Диспетчер aiogram для обработки обновлений.
- `bot_handler` (BotHandler): Обработчик бота для обработки различных типов сообщений и команд.
- `app` (Optional[web.Application]): Веб-приложение aiohttp.
- `rpc_client` (Optional[ServerProxy]): RPC-клиент для взаимодействия с сервером.

## Примеры

Пример создания и запуска Telegram-бота:

```python
from dotenv import load_dotenv
import os
from src.endpoints.bots.telegram.bot_aiogram import TelegramBot

load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
if token:
    bot = TelegramBot(token=token)
    bot.run()
else:
    print("Необходимо установить TELEGRAM_TOKEN в переменные окружения")