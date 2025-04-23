# Модуль для управления Telegram-ботом через long polling
## Обзор
Модуль `bot_long_polling.py` предоставляет класс `TelegramBot` для создания и управления Telegram-ботом. Бот использует long polling для получения обновлений от Telegram и предоставляет набор обработчиков для различных команд и типов сообщений.

## Подробнее
Модуль содержит класс `TelegramBot`, который инициализирует и запускает Telegram-бота с заданным токеном. Класс регистрирует обработчики для команд `/start`, `/help`, `/sendpdf`, текстовых сообщений, голосовых сообщений и документов.
Он использует библиотеку `telegram.ext` для обработки обновлений и управления ботом. Также, модуль использует `BotHandler` из `src.endpoints.bots.telegram.handlers` для обработки логики команд и сообщений.

## Классы
### `TelegramBot`
Описание класса для взаимодействия с Telegram ботом.

**Атрибуты:**
- `application` (Application): Экземпляр приложения Telegram.
- `handler` (BotHandler): Экземпляр обработчика бота.

**Методы:**
- `__init__(self, token: str)`: Инициализирует экземпляр класса `TelegramBot`.
- `register_handlers(self) -> None`: Регистрирует обработчики команд и сообщений бота.
- `replace_message_handler(self, new_handler: Callable) -> None`: Заменяет текущий обработчик текстовых сообщений на новый.
- `start(self, update: Update, context: CallbackContext) -> None`: Обрабатывает команду `/start`.

### `__init__(self, token: str)`
Инициализация класса Telegram бота.
**Параметры:**
- `token` (str): Токен Telegram бота. Пример: `gs.credentials.telegram.bot.kazarinov`.

****
- Инициализирует экземпляр класса `TelegramBot` с заданным токеном.
- Создает экземпляр `Application` из библиотеки `telegram.ext` с использованием предоставленного токена.
- Инициализирует обработчик бота `BotHandler`.
- Регистрирует обработчики команд и сообщений, вызывая метод `register_handlers`.

**Примеры:**
```python
# Пример создания экземпляра класса TelegramBot
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
```

### `register_handlers(self) -> None`
Регистрирует обработчики команд и сообщений для Telegram бота.

****
- Регистрирует обработчики для команд `/start`, `/help` и `/sendpdf`, используя `CommandHandler`.
- Регистрирует обработчик для текстовых сообщений, используя `MessageHandler` и фильтры `filters.TEXT` и `~filters.COMMAND`.
- Сохраняет ссылку на исходный обработчик сообщений в `self._original_message_handler`.
- Регистрирует обработчик для голосовых сообщений, используя `MessageHandler` и фильтр `filters.VOICE`.
- Регистрирует обработчик для документов, используя `MessageHandler` и фильтр `filters.Document.ALL`.

**Примеры:**
```python
# Пример регистрации обработчиков
bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.register_handlers()
```

### `replace_message_handler(self, new_handler: Callable) -> None`
Заменяет текущий обработчик текстовых сообщений на новый.

**Параметры:**
- `new_handler` (Callable): Новая функция для обработки сообщений.

****

1.  **Удаление старого обработчика:**
    *   Проверяет, существует ли текущий обработчик сообщений (`self._original_message_handler`) в списке обработчиков приложения (`self.application.handlers[0]`).
    *   Если существует, удаляет его из списка.
2.  **Создание нового обработчика:**
    *   Создает новый обработчик сообщений `MessageHandler`, используя переданную функцию `new_handler` и фильтры `filters.TEXT & ~filters.COMMAND`.
3.  **Регистрация нового обработчика:**
    *   Добавляет новый обработчик в список обработчиков приложения.

**Примеры:**

```python
# Пример замены обработчика сообщений
def my_new_handler(update: Update, context: CallbackContext) -> None:
    """Новая функция для обработки сообщений."""
    update.message.reply_text("Новый обработчик сообщений!")

bot = TelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN')
bot.replace_message_handler(my_new_handler)
```

### `start(self, update: Update, context: CallbackContext) -> None`
Обрабатывает команду `/start`.

**Параметры:**
- `update` (Update): Объект обновления от Telegram.
- `context` (CallbackContext): Контекст обратного вызова.

****
- Логирует информацию о запуске бота пользователем с использованием `logger.info`.
- Отправляет приветственное сообщение пользователю с помощью `update.message.reply_text`.

**Примеры:**
```python
# Пример обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text('Привет! Я ваш простой бот. Введите /help, чтобы увидеть доступные команды.')
```