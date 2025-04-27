# Module for testing all models from `g4f` library.
## Overview
This module provides a set of tests for different models from the `g4f` library, which is a Python wrapper for the GPT-4Free API. The primary function of this module is to assess the functionality of the models by sending specific requests and observing the results. It's essentially a diagnostic tool to confirm if the models are operational and responsive.
## Details
This file is designed to run a series of tests on different models from the `g4f` library. The `test` function sends a simple text prompt to the specified model and evaluates the response. The models are then categorized as "working" or "not working" based on the success of the test. It's essential to note that this module is not a comprehensive evaluation of the models' capabilities but rather a basic check for their responsiveness.
## Functions
### `test`
**Purpose**: This function tests a given `g4f` model by sending a simple request and analyzing the response. The test sends a prompt requesting a poem about a tree and checks for a successful response.
**Parameters**:
- `model` (`g4f.Model`): The `g4f` model to be tested.
**Returns**:
- `bool`: Returns `True` if the test is successful, `False` otherwise.
**Raises Exceptions**:
- `Exception`: Raises an exception if there's an error during the request or response handling.
**How the Function Works**:
- The function first attempts to use the synchronous `g4f.ChatCompletion.create` function to send the request.
- If this attempt fails, it then uses the asynchronous `g4f.ChatCompletion.create_async` function.
- The function prints the response to the console and returns `True` if both attempts are successful.
- If either attempt fails, the function prints an error message and returns `False`.
**Examples**:
```python
>>> import g4f
>>> from hypotez.src.endpoints.gpt4free.etc.testing.test_all import test
>>> model = g4f.models.gpt_35_turbo
>>> result = asyncio.run(test(model))
>>> print(result)
True
```
### `start_test`
**Purpose**: This function runs a series of tests on a predefined list of `g4f` models and prints the results to the console.
**Parameters**: None
**Returns**: None
**Raises Exceptions**: None
**How the Function Works**:
- The function defines a list of `g4f` models to test, including `gpt_35_turbo` and `gpt_4`.
- It then iterates through the list, calling the `test` function for each model.
- If the test is successful, the model's name is added to a list of "working models".
- Finally, the function prints the list of "working models" to the console.
**Examples**:
```python
>>> from hypotez.src.endpoints.gpt4free.etc.testing.test_all import start_test
>>> asyncio.run(start_test())
working models: ['gpt-3.5-turbo', 'gpt-4']
```
## Parameter Details
- `model` (`g4f.Model`): The `g4f` model to be tested. The model object represents a specific language model from the `g4f` library. For example: `g4f.models.gpt_35_turbo` or `g4f.models.gpt_4`.
- `response` (`str`): The response received from the model. This response is printed to the console and analyzed by the `test` function to determine if the model is working.
- `messages` (`list`): A list of messages to be sent to the model. In this case, the list only contains a single message with the role "user" and the content "write a poem about a tree".
- `temperature` (`float`): This parameter controls the creativity of the model's responses. A higher temperature value results in more creative and diverse responses.
- `stream` (`bool`): This parameter enables the streaming of responses. If `True`, the response is received in chunks as it's being generated, allowing for real-time output.
- `models_to_test` (`list`): A list of `g4f` models to be tested. The list defines which models should be included in the test suite.
- `models_working` (`list`): A list of models that have successfully passed the test. This list tracks the models that are considered operational.
## Examples
```python
# Example 1: Testing a specific model (GPT-3.5)
>>> import g4f
>>> from hypotez.src.endpoints.gpt4free.etc.testing.test_all import test
>>> model = g4f.models.gpt_35_turbo
>>> result = asyncio.run(test(model))
>>> print(result)
True

# Example 2: Running the full test suite
>>> from hypotez.src.endpoints.gpt4free.etc.testing.test_all import start_test
>>> asyncio.run(start_test())
working models: ['gpt-3.5-turbo', 'gpt-4']
```