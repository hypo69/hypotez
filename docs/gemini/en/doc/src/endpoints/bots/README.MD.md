# Модуль src.endpoints.bots

## Обзор

Модуль `src.endpoints.bots` обеспечивает взаимодействие с ботами, которые обрабатывают запросы.
Данный модуль является частью проекта `hypotez`, который предлагает различные инструменты для управления товарными предложениями, включая взаимодействие с API.

## Детали

Модуль `src.endpoints.bots` предоставляет набор функций для реализации ботов, взаимодействующих с API для выполнения различных задач, связанных с товарами. Например, бот может быть настроен для добавления новых товаров, обновления информации о существующих товарах, удаления товаров и т. д.

## Классы

### `Bot`

**Описание**: Базовый класс для ботов, который предоставляет общий функционал.

**Атрибуты**:
- `token` (str): Токен для аутентификации бота.
- `base_url` (str): Базовый URL для API.
- `headers` (dict): Заголовки запросов для API.

**Методы**:
- `get_data(url: str, params: dict = None) -> dict`: Выполняет GET-запрос к API и возвращает полученные данные в виде словаря.
- `post_data(url: str, data: dict, params: dict = None) -> dict`: Выполняет POST-запрос к API и возвращает ответ.
- `put_data(url: str, data: dict, params: dict = None) -> dict`: Выполняет PUT-запрос к API и возвращает ответ.
- `delete_data(url: str, params: dict = None) -> dict`: Выполняет DELETE-запрос к API и возвращает ответ.

### `TelegramBot`

**Описание**:  Класс для ботов, взаимодействующих с Telegram API.

**Атрибуты**:
- `bot_token` (str): Токен для Telegram бота.
- `chat_id` (str): ID чата, с которым бот взаимодействует.
- `base_url` (str): Базовый URL для Telegram API.

**Методы**:
- `send_message(text: str, parse_mode: str = 'HTML') -> dict`: Отправляет сообщение в Telegram чат.

### `ProductBot`

**Описание**:  Класс для ботов, взаимодействующих с API для управления товарами.

**Атрибуты**:
- `token` (str): Токен для API.
- `base_url` (str): Базовый URL для API.
- `headers` (dict): Заголовки запросов для API.
- `catalog_id` (int): ID каталога.

**Методы**:
- `create_product(data: dict) -> dict`: Создает новый товар в каталоге.
- `get_product(product_id: int) -> dict`: Получает данные о товаре по ID.
- `update_product(product_id: int, data: dict) -> dict`: Обновляет данные о товаре.
- `delete_product(product_id: int) -> dict`: Удаляет товар из каталога.

## Функции

### `get_bot_by_type(bot_type: str, token: str, base_url: str) -> Bot`:

**Назначение**: Возвращает экземпляр бота соответствующего типа.

**Параметры**:
- `bot_type` (str): Тип бота. Возможные значения: `telegram`, `product`.
- `token` (str): Токен для API.
- `base_url` (str): Базовый URL для API.

**Возвращает**:
- `Bot`: Экземпляр бота.

**Raises Exceptions**:
- `ValueError`: Если указан некорректный тип бота.

### `create_bot(bot_type: str, token: str, base_url: str) -> Bot`:

**Назначение**: Создает экземпляр бота соответствующего типа.

**Параметры**:
- `bot_type` (str): Тип бота. Возможные значения: `telegram`, `product`.
- `token` (str): Токен для API.
- `base_url` (str): Базовый URL для API.

**Возвращает**:
- `Bot`: Экземпляр бота.

**Raises Exceptions**:
- `ValueError`: Если указан некорректный тип бота.

## Примеры

```python
# Импорт модуля
from src.endpoints.bots import create_bot, get_bot_by_type

# Создание экземпляра бота для Telegram
telegram_bot = create_bot(bot_type='telegram', token='YOUR_TELEGRAM_BOT_TOKEN', base_url='https://api.telegram.org/bot')

# Отправка сообщения в Telegram чат
telegram_bot.send_message(text='Привет, мир!', chat_id='YOUR_CHAT_ID')

# Создание экземпляра бота для управления товарами
product_bot = get_bot_by_type(bot_type='product', token='YOUR_API_TOKEN', base_url='https://YOUR_API_URL')

# Создание нового товара
product_data = {'name': 'Новый товар', 'price': 100}
product_bot.create_product(data=product_data)

# Получение информации о товаре по ID
product_info = product_bot.get_product(product_id=1)

# Обновление информации о товаре
product_bot.update_product(product_id=1, data={'price': 150})

# Удаление товара
product_bot.delete_product(product_id=1)
```