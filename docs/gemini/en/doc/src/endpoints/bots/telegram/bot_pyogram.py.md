# Module Name

## Overview

The code provided defines a simple Telegram bot using the Pyrogram library. The bot responds to the `/start` command with a greeting message and echoes back any other text messages it receives.

## More details

This module sets up a basic Telegram bot that can be extended with more complex functionality. It uses environment variables for sensitive information like API credentials and the bot token. The bot is initialized with these credentials and then set up to handle specific commands and text messages. This code serves as a starting point for creating more interactive and feature-rich Telegram bots within the `hypotez` project.

## Classes

This code does not contain any classes.

## Functions

### `start_command`

```python
def start_command(client, message):
    """
    Обработчик команды /start.

    Args:
        client: Экземпляр клиента Pyrogram.
        message: Объект сообщения, содержащий информацию о полученном сообщении.

    Returns:
        None

    Raises:
        None
    """
    # Функция отправляет приветственное сообщение в ответ на команду /start
    message.reply_text("Привет! Я простой бот на Pyrogram.")
```

**Purpose**: Обрабатывает команду `/start`, отправляя приветственное сообщение пользователю.

**Parameters**:
- `client`: Экземпляр клиента Pyrogram.
- `message`: Объект сообщения, содержащий информацию о полученном сообщении.

**Returns**:
- `None`

**Raises**:
- None

**How the function works**:
- Функция принимает объект `message`, содержащий информацию о сообщении, и использует метод `reply_text` для отправки ответа с текстом "Привет! Я простой бот на Pyrogram.".

**Examples**:
```python
# Пример вызова функции (обычно вызывается автоматически Pyrogram при получении команды /start)
start_command(client, message)
```

### `echo_message`

```python
def echo_message(client, message):
    """
    Обработчик всех текстовых сообщений (кроме команд).

    Args:
        client: Экземпляр клиента Pyrogram.
        message: Объект сообщения, содержащий информацию о полученном сообщении.

    Returns:
        None

    Raises:
        None
    """
    # Функция повторяет полученное текстовое сообщение в ответ
    message.reply_text(message.text)
```

**Purpose**: Повторяет все текстовые сообщения, отправленные боту (кроме команд).

**Parameters**:
- `client`: Экземпляр клиента Pyrogram.
- `message`: Объект сообщения, содержащий информацию о полученном сообщении.

**Returns**:
- `None`

**Raises**:
- None

**How the function works**:
- Функция принимает объект `message`, содержащий информацию о сообщении, и использует метод `reply_text` для отправки ответа, содержащего текст исходного сообщения (`message.text`).

**Examples**:
```python
# Пример вызова функции (обычно вызывается автоматически Pyrogram при получении текстового сообщения)
echo_message(client, message)
```