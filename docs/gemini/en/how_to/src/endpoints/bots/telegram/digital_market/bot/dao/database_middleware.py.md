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
This code block defines two middleware classes: `DatabaseMiddlewareWithoutCommit` and `DatabaseMiddlewareWithCommit`. These classes are designed to be used with Aiogram's middleware system, enabling efficient interaction with a database within Telegram bot handlers. 

Execution Steps
-------------------------
1. **Initialization:** The middleware is initialized with an asynchronous session maker (`async_session_maker`) provided from the database module.

2. **Session Setup:** When the middleware is called, it opens a new database session and sets it within the handler data dictionary. 

3. **Handler Execution:** The handler is executed, allowing the bot to process user interactions.

4. **Post-Handler Actions:** Depending on the middleware subclass:
    - `DatabaseMiddlewareWithoutCommit` does not commit the session changes.
    - `DatabaseMiddlewareWithCommit` commits the session changes, ensuring database persistence.

5. **Session Closure:** The middleware finally closes the database session.

Usage Example
-------------------------

```python
from bot.dao.database_middleware import DatabaseMiddlewareWithCommit

# Initialize the middleware with a session maker
middleware = DatabaseMiddlewareWithCommit(async_session_maker)

# Add the middleware to the dispatcher
dp.middleware.setup(middleware)

# Create a handler that uses the database session
@dp.message_handler(commands=['start'])
async def start_handler(message: Message, data: dict):
    # Access the database session from the data dictionary
    session = data['session_with_commit']

    # Perform database operations using the session
    # ...

    # Return a response to the user
    await message.answer('Welcome!')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".