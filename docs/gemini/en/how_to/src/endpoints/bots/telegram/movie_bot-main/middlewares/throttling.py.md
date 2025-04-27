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
This code snippet defines a `ThrottlingMiddleware` class, which is a middleware for the `aiogram` library. This middleware implements a simple rate-limiting mechanism to prevent users from sending too many messages in a short period of time.

Execution Steps
-------------------------
1. The `__init__` method initializes the middleware with a `time_limit` parameter, which sets the minimum time interval between messages from the same user. 
2. The `limit` attribute is initialized as a `TTLCache` object, which stores user IDs and their last message timestamps. The cache has a maximum size of 10,000 entries and a time-to-live (TTL) of `time_limit` seconds.
3. The `__call__` method is invoked when a message is received. It first checks if the user's ID is already in the cache.
4. If the user's ID is in the cache, it means the user has sent a message within the specified time limit, and the middleware returns without processing the message.
5. If the user's ID is not in the cache, the middleware adds the user's ID to the cache and then calls the next handler in the middleware chain.

Usage Example
-------------------------

```python
from aiogram import Dispatcher
from hypotez.src.endpoints.bots.telegram.movie_bot-main.middlewares.throttling import ThrottlingMiddleware

# Initialize the middleware
throttling = ThrottlingMiddleware(time_limit=2)

# Register the middleware to the dispatcher
dp = Dispatcher(...)
dp.middleware.setup(throttling)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".