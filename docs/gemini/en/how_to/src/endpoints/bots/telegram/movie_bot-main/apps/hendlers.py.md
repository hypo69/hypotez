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
This code block defines handlers for a Telegram bot that searches for movies and series. It allows users to specify the type of content (film or series) and then search by name. 

Execution Steps
-------------------------
1. **Import Libraries**: Imports necessary libraries like `aiogram` for Telegram bot interactions, `apps.keyboard` for handling keyboard interactions, and `apps.search` for movie search functionality.
2. **Define Constants**: Defines the `type_movies` dictionary mapping movie types to their corresponding textual representations.
3. **Define States**: Creates a `Params` state group with two states: `type_movie` to store the type of movie being searched and `name` to store the name of the movie or series.
4. **Start Command Handler**: Defines a handler for the `/start` command, which greets the user and presents them with the "Find Movie" option.
5. **Movie Type Handler**: Defines a handler for the "New Movies" callback query, which prompts the user to specify whether they are looking for a film or a series.
6. **Series/Film Handler**: Defines handlers for the "Series" and "Film" callback queries, which record the user's selection and transition to the state where the user inputs the name.
7. **Name Handler**: Defines a handler for the `Params.name` state, which handles the user's input of the movie or series name. It retrieves the saved `type_movie` and `name` data, performs the search using the `search_query` function, and provides feedback to the user about the search results. It then presents the "Find New Movie" option and clears the state. 

Usage Example
-------------------------

```python
# Example usage in the Telegram bot:
from aiogram import Bot, Dispatcher
from aiogram.utils import executor

bot = Bot(token='YOUR_BOT_TOKEN')
dp = Dispatcher(bot)

# Add the handlers from this code block to the dispatcher:
dp.include_router(router)

executor.start_polling(dp, skip_updates=True)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".