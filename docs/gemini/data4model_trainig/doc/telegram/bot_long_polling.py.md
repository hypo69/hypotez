# Модуль Telegram-бота с использованием Long Polling

## Обзор

Модуль `src.endpoints.bots.telegram.bot_long_polling` представляет собой Telegram-бота, реализованного с использованием библиотеки python-telegram-bot и использующего механизм Long Polling для получения обновлений.

## Подробней

Модуль предоставляет класс `TelegramBot`, который позволяет:

*   Обрабатывать команды и сообщения пользователей.
*   Использовать Long Polling для получения обновлений от Telegram.

## Классы

### `TelegramBot`

**Описание**: Класс для управления Telegram-ботом.

**Атрибуты**:

*   `application` (Application): Экземпляр класса `telegram.ext.Application`.
*   `handler` (BotHandler): Экземпляр класса `BotHandler` для обработки сообщений.
*   `_original_message_handler` (MessageHandler): Оригинальный обработчик текстовых сообщений.

**Методы**:

*   `__init__(self, token: str)`: Инициализирует объект `TelegramBot`.
*   `register_handlers(self) -> None`: Регистрирует обработчики команд и сообщений.
*   `replace_message_handler(self, new_handler: Callable) -> None`: Заменяет текущий обработчик текстовых сообщений на новый.
*   `start(self, update: Update, context: CallbackContext) -> None`: Обрабатывает команду `/start`.

## Методы класса `TelegramBot`

### `__init__`

```python
def __init__(self, token: str):
```

**Назначение**: Инициализирует объект `TelegramBot`.

**Параметры**:

*   `token` (str): Токен Telegram-бота, например, `gs.credentials.telegram.bot.kazarinov`.

**Как работает функция**:

1.  Создает экземпляр класса `telegram.ext.Application`.
2.  Создает экземпляр класса `BotHandler`.
3.  Регистрирует обработчики по умолчанию.

### `register_handlers`

```python
def register_handlers(self) -> None:
```

**Назначение**: Регистрирует обработчики команд и сообщений.

**Как работает функция**:

1.  Регистрирует обработчики для команд `/start`, `/help` и `/sendpdf`.
2.  Регистрирует обработчики для текстовых и голосовых сообщений, а также документов.

### `replace_message_handler`

```python
def replace_message_handler(self, new_handler: Callable) -> None:
```

**Назначение**: Заменяет текущий обработчик текстовых сообщений на новый.

**Параметры**:

*   `new_handler` (Callable): Новая функция для обработки сообщений.

**Как работает функция**:

1.  Удаляет текущий обработчик текстовых сообщений.
2.  Создает новый обработчик текстовых сообщений.
3.  Регистрирует новый обработчик.

### `start`

```python
async def start(self, update: Update, context: CallbackContext) -> None:
```

**Назначение**: Обрабатывает команду `/start`.

**Параметры**:

*   `update` (Update): Объект обновления Telegram.
*   `context` (CallbackContext): Контекст обратного вызова.

**Как работает функция**:

1.  Логирует информацию о запуске бота пользователем.
2.  Отправляет приветственное сообщение пользователю и информирует о доступных командах.