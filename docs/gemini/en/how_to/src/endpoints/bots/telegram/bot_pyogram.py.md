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
This code snippet creates a simple Telegram bot using the Pyrogram library. The bot responds to the `/start` command with a welcome message and echoes back any other text messages it receives.

Execution Steps
-------------------------
1. Imports necessary modules: `pyrogram` for bot interaction, `os` for environment variable access.
2. Defines environment variables for Telegram API credentials: `API_ID`, `API_HASH`, `BOT_TOKEN`.
3. Creates a `Client` instance using Pyrogram, configuring it with the Telegram API credentials.
4. Defines the `start_command` handler, which responds to the `/start` command with a welcome message.
5. Defines the `echo_message` handler, which echoes back any text message that isn't a command.
6. Starts the bot using `app.run()`.

Usage Example
-------------------------

```python
from pyrogram import Client, filters
import os

# Replace with your own values
API_ID = int(os.environ.get("TELEGRAM_API_ID", ''))
API_HASH = os.environ.get("TELEGRAM_API_HASH", '')
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN", '')

# Create a Pyrogram client instance
app = Client(
    "my_simple_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Handler for the /start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Hello! I'm a simple Pyrogram bot.")

# Handler for all text messages (except commands)
@app.on_message(filters.text & ~filters.command)
def echo_message(client, message):
    message.reply_text(message.text)

# Start the bot
if __name__ == "__main__":
    print("Bot started...")
    app.run()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".