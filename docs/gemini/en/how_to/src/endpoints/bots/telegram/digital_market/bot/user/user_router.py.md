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
The code block defines a Telegram bot user router that handles user interactions. It includes the following functions:

- `cmd_start`: Handles the `/start` command. Checks if the user exists in the database. If not, it registers the user and sends a welcome message. Otherwise, it sends a message with the main user keyboard.
- `page_home`: Handles the "home" callback query. It answers the user with "Главная страница" and sends a message with the main user keyboard.
- `page_about`: Handles the "about" callback query. It answers the user with "О магазине" and sends a message with information about the bot and contact details.
- `page_my_profile`: Handles the "my_profile" callback query. It answers the user with "Профиль" and displays the user's purchase statistics.
- `page_user_purchases`: Handles the "purchases" callback query. It displays the user's purchase history.

Execution Steps
-------------------------
1. The code defines a `user_router` using `aiogram.Router`. 
2. Each function is decorated with `@user_router.message` or `@user_router.callback_query` to handle specific events:
    - The `cmd_start` function handles the `/start` command.
    - The `page_home` function handles the "home" callback query.
    - The `page_about` function handles the "about" callback query.
    - The `page_my_profile` function handles the "my_profile" callback query.
    - The `page_user_purchases` function handles the "purchases" callback query.
3. Each function performs actions based on the corresponding event:
    - `cmd_start`: Registers the user or sends a welcome message.
    - `page_home`: Displays the main user keyboard.
    - `page_about`: Displays information about the bot.
    - `page_my_profile`: Displays the user's purchase statistics.
    - `page_user_purchases`: Displays the user's purchase history.

Usage Example
-------------------------

```python
from src.endpoints.bots.telegram.digital_market.bot.user.user_router import user_router

# Example usage within the bot's main loop:
from aiogram import Dispatcher

async def setup_user_router(dp: Dispatcher):
    dp.include_router(user_router)

# ... rest of the bot code ...
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".