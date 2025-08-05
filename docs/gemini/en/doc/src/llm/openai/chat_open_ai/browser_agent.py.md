# Module: `src.ai.openai.chat_openai.browser_agent`

## Overview

This module provides a Python class `AIBrowserAgent` that encapsulates the functionality of using a web browser to perform tasks through a conversational interface powered by OpenAI's large language models. The class is designed to work with both custom WebDriver instances and the default Playwright driver provided by the `browser_use` library. 

## Details

The module is designed to help developers quickly setup and run an AI agent capable of searching for information on Google and analyzing web pages. 

## Classes

### `AIBrowserAgent`

**Description**: This class is used to create an agent that uses a web browser to perform tasks.

**Attributes**:

- `api_key` (str): OpenAI API key (optional). If not provided, the key from environment variables will be used.
- `model_name` (str): Name of the OpenAI language model to use (default: "gpt-4o-mini").
- `search_engine` (str): Search engine to use (default: "google").
- `llm` (ChatOpenAI): Initialized LLM instance using the specified `model_name` and `api_key`.
- `custom_driver` (Optional[object]): Optionally injected WebDriver instance, defaults to `None` (browser_use default).

**Methods**:

- `__init__(self, api_key: str, model_name: str = "gpt-4o-mini", search_engine: str = "google", custom_driver: Optional[object] = None)`: Initializes the `AIBrowserAgent` class.
- `run_task(self, task_prompt: str) -> Optional[str]`: Runs the agent to perform the given task.
- `find_product_alternatives(self, product_url: Optional[str] = None, sku: Optional[str] = None) -> Optional[str]`: Searches the web for product alternatives based on the provided URL or SKU.
- `ask(self, q: str) -> Optional[str]`: Synchronous wrapper for the asynchronous method `ask_async`. Not recommended for use.
- `ask_async(self, q: str) -> Optional[str]`: Answers the given question, using web search if necessary.

**Principle of Operation**:

The `AIBrowserAgent` class works by combining the power of OpenAI's language models with the capability of web browsing. The core functionality is implemented through the `run_task` method, which takes a task prompt as input and uses the `browser_use` library's `Agent` class to execute the task. The `Agent` class automatically manages the web browser and interacts with the provided LLM to perform the tasks. The class can also be used with custom WebDriver instances, which allows developers to use specific browsers and customize the browsing experience.

**How the Function Works**:

- The `run_task` method first sets up the browser driver based on whether a custom driver is provided or the default `browser_use` driver should be used.
- It then creates an instance of the `Agent` class from `browser_use`, passing the task prompt, the initialized OpenAI LLM, and the driver.
- The `Agent` class runs the task and returns the results. 
- The method attempts to close the driver after the task is complete.

**Examples**:

```python
from src.ai.openai.chat_openai.browser_agent import AIBrowserAgent

# Replace with your actual method of obtaining the API key
api_key = None  

# Initialize the agent with the default Playwright driver
agent = AIBrowserAgent(api_key=api_key, model_name="gpt-4o-mini")

# Example of finding product alternatives
sku = "1493001"
product_url = None 
alternatives = await agent.find_product_alternatives(product_url=product_url, sku=sku)
if alternatives:
    print("Найденные аналоги:")
    print(alternatives)
else:
    print("Не удалось найти аналоги.")

# Example of answering a question
question = "Какая сейчас погода в Москве?"
answer = await agent.ask_async(question)  # Use asynchronous method directly
if answer:
    print("Ответ на вопрос:")
    print(answer)
else:
    print("Не удалось получить ответ на вопрос.")

```

## Functions

### `main()`

**Purpose**: This asynchronous function provides an example of how to use the `AIBrowserAgent` class.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- The function first initializes the `AIBrowserAgent` class with an API key, model name, and optionally a custom WebDriver instance.
- It then demonstrates two use cases:
    - Finding product alternatives based on a SKU.
    - Answering a question using web search.
- The results are printed to the console.

**Examples**:

```python
# ... (code for main() function from the input file)
```