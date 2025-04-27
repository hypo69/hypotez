# Module: src.endpoints.hypo69.code_assistant.onela_bot

## Overview

The module provides functionality for interacting with the programmer's assistant model through Telegram chat. It contains the `OnelaBot` class, which is responsible for handling text messages and documents.

## Details

The `OnelaBot` class inherits from the `TelegramBot` class and uses the `GoogleGenerativeAi` model for processing messages. It handles both text messages and uploaded documents. The module utilizes the `src.llm.gemini` module to interact with Google Gemini and the `src.logger.logger` module for logging errors.

## Classes

### `OnelaBot`

**Description:** This class implements the functionality of a Telegram bot that interacts with a programmer's assistant model. 

**Inherits:** `TelegramBot`

**Attributes:**

- `model (GoogleGenerativeAi):` An instance of the Google Gemini model for generating responses.

**Methods:**

- `__init__()`: Initializes the `OnelaBot` object.
- `handle_message(update: Update, context: CallbackContext)`: Handles text messages received through Telegram.
- `handle_document(update: Update, context: CallbackContext)`: Handles uploaded documents received through Telegram.

## Class Methods

### `__init__()`

```python
    def __init__(self) -> None:
        """
        Инициализация объекта OnelaBot.
        """
        super().__init__(gs.credentials.telegram.onela_bot)
```

**Purpose:** Initializes the `OnelaBot` object.

**Parameters:**

- None

**Returns:**

- None

**How the Function Works:**

- Calls the `__init__` method of the parent `TelegramBot` class, passing the Telegram bot token from the `gs.credentials.telegram.onela_bot` configuration.

**Examples:**

```python
bot = OnelaBot()
```

### `handle_message(update: Update, context: CallbackContext)`

```python
    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        """
        Обработка текстовых сообщений.

        Args:
            update (Update): Данные обновления Telegram.
            context (CallbackContext): Контекст выполнения.
        """
        q: str = update.message.text
        user_id: int = update.effective_user.id
        try:
            # Получение ответа от модели
            answer: str = await self.model.chat(q)
            await update.message.reply_text(answer)
        except Exception as ex:
            logger.error('Ошибка обработки текстового сообщения: ', ex)
            ...
```

**Purpose:** Handles text messages received from Telegram users.

**Parameters:**

- `update (Update)`: The Telegram update object containing information about the message.
- `context (CallbackContext)`: The context of the update.

**Returns:**

- None

**How the Function Works:**

1. Extracts the message text (`q`) and the user ID (`user_id`) from the `update` object.
2. Calls the `chat` method of the `GoogleGenerativeAi` model (`self.model`) to obtain a response to the message.
3. Replies to the user with the generated response.
4. Logs any exceptions that occur during processing.

**Examples:**

```python
# Assuming the bot instance is named 'bot'
update = ...  # Sample Telegram update object
context = ...  # Sample context object
await bot.handle_message(update, context)
```

### `handle_document(update: Update, context: CallbackContext)`

```python
    async def handle_document(self, update: Update, context: CallbackContext) -> None:
        """
        Обработка загруженных документов.

        Args:
            update (Update): Данные обновления Telegram.
            context (CallbackContext): Контекст выполнения.
        """
        try:
            file = await update.message.document.get_file()
            tmp_file_path: Path = await file.download_to_drive()  # Сохранение файла локально
            answer: str = await update.message.reply_text(file)
            update.message.reply_text(answer)
        except Exception as ex:
            logger.error('Ошибка обработки документа: ', ex)
            ...
```

**Purpose:** Handles uploaded documents from Telegram users.

**Parameters:**

- `update (Update)`: The Telegram update object containing information about the uploaded document.
- `context (CallbackContext)`: The context of the update.

**Returns:**

- None

**How the Function Works:**

1. Retrieves the uploaded document file object from the `update` object.
2. Downloads the file to the local drive and stores it in `tmp_file_path`.
3. Sends a message to the user confirming the receipt of the file.
4. Logs any exceptions that occur during processing.

**Examples:**

```python
# Assuming the bot instance is named 'bot'
update = ...  # Sample Telegram update object
context = ...  # Sample context object
await bot.handle_document(update, context)
```

## Parameter Details

- `update (Update)`: Represents the Telegram update object, containing information about the received message or document.
- `context (CallbackContext)`: Represents the context of the Telegram update, providing access to the user's data and other relevant information.
- `q (str)`: The text of the message received from the user.
- `user_id (int)`: The Telegram user ID.
- `file (telegram.File)`: The uploaded file object.
- `tmp_file_path (Path)`: The path to the downloaded file on the local drive.
- `answer (str)`: The response generated by the `GoogleGenerativeAi` model.

## Examples

```python
# Creating a bot instance
bot = OnelaBot()

# Running the bot in polling mode
asyncio.run(bot.application.run_polling())
```