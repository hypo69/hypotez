# Tiny Person Module

## Overview

This module defines the `TinyPerson` class, a fundamental component of the `tinytroupe` library. `TinyPerson` represents a conversational AI agent with customizable characteristics and the ability to interact with users.

## Details

The `TinyPerson` class is designed to facilitate natural language interactions with AI agents. It allows developers to define the agent's personality, background, and capabilities through simple attribute settings. This module leverages the `tinytroupe.agent` module to implement core agent functionality. 

## Classes

### `TinyPerson`

**Description**:  This class represents a conversational AI agent with customizable characteristics.

**Inherits**:  `tinytroupe.agent.Agent`

**Attributes**:

- `name` (str): The agent's name.
- `characteristics` (dict): A dictionary storing the agent's defined characteristics, such as age, occupation, nationality, and skills.

**Methods**:

- `define(key: str, value: Any)`: Defines a new characteristic for the agent.
- `listen(text: str)`: Receives a user's message and updates the interaction history.
- `act()`: Processes the received message and generates a response using the `tinytroupe.agent.Agent` class.
- `pp_current_interactions()`: Prints a formatted representation of the current interaction history.

## Functions

### `load_dotenv()`

**Purpose**:  Loads environment variables from a `.env` file.

**Parameters**: None

**Returns**: None

**Raises Exceptions**:

- `OSError`: If there is an error while reading the `.env` file.

**How the Function Works**:

- This function uses the `dotenv` library to load environment variables from the `.env` file.
- The `.env` file should contain environment variables in the format `KEY=VALUE`.

**Examples**:

- `load_dotenv()`: Loads environment variables from the `.env` file in the current directory.

### `os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")`

**Purpose**:  Sets the `OPENAI_API_KEY` environment variable from the `.env` file.

**Parameters**: None

**Returns**: None

**Raises Exceptions**:

- `KeyError`: If the `OPENAI_API_KEY` environment variable is not found in the `.env` file.

**How the Function Works**:

- This code snippet sets the `OPENAI_API_KEY` environment variable to the value retrieved from the `.env` file using `os.getenv()`.
- The `OPENAI_API_KEY` is essential for interacting with OpenAI's API.

**Examples**:

- Assuming the `.env` file contains `OPENAI_API_KEY=your_api_key`, this code will set the `OPENAI_API_KEY` environment variable to `your_api_key`.

## Parameter Details

- `name` (str): The agent's name. It should be a string representing the chosen name for the conversational agent.
- `key` (str): The key for the agent's characteristic. It should be a string identifying the type of characteristic (e.g., 'age', 'occupation', 'nationality').
- `value` (Any): The value associated with the characteristic. It can be a string, a list, or any other data type suitable for the characteristic.
- `text` (str): The user's message. It should be a string containing the text input from the user.

## Examples

```python
from tinytroupe.agent import TinyPerson

# Create a TinyPerson instance
john = TinyPerson(name="John")

# Define some characteristics
john.define("age", 35)
john.define("occupation", "Software Engineer")
john.define("nationality", "American")
john.define("skills", [{"skill": "Coding in python"}])

# Interact with the agent
john.listen("Hello, John! How are you today?")
john.act()
john.pp_current_interactions()
```
```python
```
```python
```
```python
```
```python
```
```python