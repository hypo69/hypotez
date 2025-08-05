**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code block sets up and configures a Telegram bot using the `aiogram` library. It defines a `Settings` class to manage configuration parameters, initializes the bot and dispatcher, and sets up logging and a database connection. 

Execution Steps
-------------------------
1. **Import necessary modules**: Imports modules for bot interaction, logging, and database configuration.
2. **Define `Settings` class**: Creates a class to manage configuration parameters such as bot token, admin IDs, provider token, logging settings, database URL, and website details.
3. **Initialize `Settings`**: Loads configuration parameters from the `.env` file.
4. **Dynamically generate webhook URLs**: Defines two `@property` methods to generate webhook URLs based on the bot token and website URL.
5. **Create bot and dispatcher**: Initializes a `Bot` instance using the bot token and `Dispatcher` instance using `MemoryStorage` for storing bot state.
6. **Set up logging**: Configures logging to a file, `log.txt`, using `loguru` library with custom formatting and rotation settings.
7. **Set up database connection**: Sets up the database connection URL based on the configuration settings.

Usage Example
-------------------------

```python
    # Load settings
    settings = Settings()

    # Access bot instance
    bot = settings.bot

    # Access dispatcher
    dp = settings.dp

    # Access database connection URL
    database_url = settings.DB_URL

    # Send a message to a specific chat ID
    await bot.send_message(chat_id=123456789, text="Hello from the Telegram bot!")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".