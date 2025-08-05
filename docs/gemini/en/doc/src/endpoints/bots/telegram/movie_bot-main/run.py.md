#  Telegram Movie Bot Run File

## Overview

This module defines the entry point for the Telegram movie bot application. It sets up the bot, dispatcher, and event loop, allowing the bot to receive and respond to user messages.

## Details

This file orchestrates the bot's functionality. It establishes a connection to the Telegram API, configures the dispatcher for handling incoming messages, and starts the polling loop to continuously check for new messages.

## Classes

### `None`

This module doesn't have any defined classes.

## Functions

### `main`

```python
async def main() -> None:
    """
    Основная функция, запускающая Telegram-бота.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: В случае возникновения ошибок во время работы бота.
    """
    bot = Bot(os.getenv('TOKEN'),)
    dp.message.middleware(ThrottlingMiddleware())
    dp.include_router(router)
    await dp.start_polling(bot)
```

**Purpose**: This function sets up and runs the Telegram movie bot.

**Parameters**:
- None

**Returns**:
- None

**Raises Exceptions**:
- Exception: If any errors occur during the bot's operation.

**How the Function Works**:
1. **Bot Initialization**:
   - Creates a `Bot` instance using the Telegram API token retrieved from the environment variable `TOKEN`.
2. **Middleware Application**:
   - Applies the `ThrottlingMiddleware` to the dispatcher. This middleware helps prevent rate limiting issues by limiting the number of requests the bot can send to the Telegram API within a specific time frame.
3. **Router Inclusion**:
   - Includes the `router` object, which defines the bot's logic for handling incoming messages.
4. **Polling Start**:
   - Initiates the polling loop using `dp.start_polling(bot)`. This loop constantly checks for new messages from Telegram and triggers the corresponding handlers within the `router` to process them.

**Examples**:
-  ```python
    asyncio.run(main())
   ```

## Inner Functions

### `None`

This function doesn't have any inner functions. 

## Parameter Details

- `TOKEN` (str): The Telegram API token required to authenticate the bot. It is retrieved from the environment variable.

## Examples

```python
logging.basic_colorized_config(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - '
           '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
    datefmt='%H:%M:%S'
)
asyncio.run(main())
```

This code demonstrates how to configure basic logging and run the main function. It sets up the logging level, format, and date format, and then uses `asyncio.run(main())` to execute the `main` function asynchronously.