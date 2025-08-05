# Hendlers Module

## Overview

This module contains the handlers for the movie bot, responsible for processing user interactions and providing relevant information. It leverages the Aiogram framework for asynchronous event handling in Telegram bots.

## Details

The module utilizes state machines (`Params`) to manage user interactions and gather information for movie searches. It interacts with the `search_query` function from the `apps.search` module to fetch movie data based on user input. The module defines a `router` instance to handle various user commands and callbacks.

## Classes

### `Params`

**Description**: This class defines a state machine for tracking user input during the movie search process.

**Inherits**:  `aiogram.fsm.state.StatesGroup` 

**Attributes**:

- `type_movie (State)`: State for selecting the type of movie (film or series).
- `name (State)`: State for entering the name of the movie.

## Functions

### `command_start_handler`

**Purpose**: Handles the `/start` command, welcoming the user and presenting a menu to find a movie.

**Parameters**:

- `message (Message)`:  The incoming message object containing user details and the message text.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- Welcomes the user with a message including their full name.
- Sends a message prompting the user to find a movie and provides a menu (`kb.find_movie`) to initiate the search.


### `movie_handler`

**Purpose**: Handles the callback query when the user selects "New Movies" from the initial menu.

**Parameters**:

- `callback (CallbackQuery)`: The incoming callback query object containing the user's selection.
- `state (FSMContext)`: Context object for managing the state machine.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- Sets the state to `Params.type_movie`, prompting the user to choose between "Film" or "Series."
- Edits the previous message to ask for the type of movie and presents a choice menu (`kb.choice`).

### `series_handler`

**Purpose**: Handles the callback query when the user selects "Series" from the type selection menu.

**Parameters**:

- `callback (CallbackQuery)`: The incoming callback query object containing the user's selection.
- `state (FSMContext)`: Context object for managing the state machine.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- Deletes the previous message.
- Updates the state data to indicate that the user has selected "Series" (`type_movie='series'`).
- Transitions to the `Params.name` state, prompting the user to enter the series name.
- Sends a message asking the user to input the series name.

### `film_handler`

**Purpose**: Handles the callback query when the user selects "Film" from the type selection menu.

**Parameters**:

- `callback (CallbackQuery)`: The incoming callback query object containing the user's selection.
- `state (FSMContext)`: Context object for managing the state machine.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- Deletes the previous message.
- Updates the state data to indicate that the user has selected "Film" (`type_movie='film'`).
- Transitions to the `Params.name` state, prompting the user to enter the film name.
- Sends a message asking the user to input the film name.

### `name_handler`

**Purpose**: Handles the message received from the user after they have entered the movie name.

**Parameters**:

- `message (Message)`: The incoming message object containing the movie name.
- `state (FSMContext)`: Context object for managing the state machine.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- Updates the state data with the movie name (`name=message.text`).
- Retrieves the stored state data.
- Calls `search_query` to search for the movie based on name and type.
- Displays the movie name and type to the user.
- If a movie is found, it displays the movie title, description, and link.
- If no movie is found, it informs the user that the movie was not found.
- Provides a message to find another movie and presents the initial movie search menu (`kb.find_movie`).
- Clears the state machine.

## Inner Functions: None 

## Examples

**Example 1: Starting the bot:**

```
/start
```

**Output:**

```
Добро пожаловать, **[User's Full Name]** 😎
Найти интересующий фильм
```

**Example 2: Searching for a series:**

```
/start
Найти интересующий фильм
Series
Введите название
Game of Thrones
```

**Output:**

```
Название: **Game of Thrones**
Тип: **Сериал**
По вашему запросу найдено ✨✨✨:
**[Series Title]**
[Series Description]
[Series Link]
Найти новый фильм
```

**Example 3: Searching for a film that doesn't exist:**

```
/start
Найти интересующий фильм
Film
The Nonexistent Movie
```

**Output:**

```
Название: **The Nonexistent Movie**
Тип: **Фильм**
Ваш Фильм не найден 😢
Найти новый фильм
```