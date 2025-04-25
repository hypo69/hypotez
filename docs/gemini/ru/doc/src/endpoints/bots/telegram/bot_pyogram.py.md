# Модуль бота для Telegram на Pyrogram

## Обзор

Этот модуль реализует простого бота для Telegram, использующего библиотеку Pyrogram. 
Он демонстрирует основные принципы работы с ботами Telegram, включая:

- Создание экземпляра клиента Pyrogram.
- Обработку команд `/start`.
- Эхо-ответ на текстовые сообщения.

## Подробней

Этот модуль представляет собой простой пример бота на Pyrogram, который может быть использован 
как отправная точка для разработки более сложных ботов. 

## Параметры

- `API_ID` (int): Идентификатор приложения Telegram.
- `API_HASH` (str): Хэш приложения Telegram.
- `BOT_TOKEN` (str): Токен бота Telegram.

## Классы

### `Client`

**Описание**: 
    Экземпляр клиента Pyrogram, представляющий собой соединение с Telegram API.

**Наследует**: 
    Pyrogram.Client

**Атрибуты**:

    - `api_id` (int): Идентификатор приложения Telegram.
    - `api_hash` (str): Хэш приложения Telegram.
    - `bot_token` (str): Токен бота Telegram.

**Методы**:

    - `on_message(filters)`: Декоратор для создания обработчика сообщений, который запускается, когда сообщение соответствует заданным фильтрам.
    - `reply_text(text)`: Отправляет текстовое сообщение в ответ на полученное сообщение.
    - `run()`: Запускает бота.


## Функции

### `start_command(client, message)`

**Назначение**:
    Обрабатывает команду `/start` и отправляет приветственное сообщение.

**Параметры**:

    - `client` (Client): Экземпляр клиента Pyrogram.
    - `message` (Message): Полученное сообщение.

**Возвращает**:
    None.

**Вызывает исключения**:
    None.

**Примеры**:

```python
>>> from pyrogram import Client, filters
>>> from hypotez.src.endpoints.bots.telegram.bot_pyogram import API_ID, API_HASH, BOT_TOKEN
>>> app = Client("my_simple_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
>>> app.on_message(filters.command("start"))(start_command)
```

### `echo_message(client, message)`

**Назначение**:
    Обрабатывает текстовые сообщения и отправляет их обратно пользователю.

**Параметры**:

    - `client` (Client): Экземпляр клиента Pyrogram.
    - `message` (Message): Полученное сообщение.

**Возвращает**:
    None.

**Вызывает исключения**:
    None.

**Примеры**:

```python
>>> from pyrogram import Client, filters
>>> from hypotez.src.endpoints.bots.telegram.bot_pyogram import API_ID, API_HASH, BOT_TOKEN
>>> app = Client("my_simple_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
>>> app.on_message(filters.text & ~filters.command)(echo_message)
```

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Пример использования вебдрайвера
close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)