# Glider.py Module

## Overview

The `Glider.py` module implements the `Glider` class, which represents the Glider.so AI model provider. It inherits from the `OpenaiTemplate` class and provides a specific implementation for interacting with the Glider.so API.

## Details

The Glider class is used to interact with the Glider.so API, which provides access to various large language models (LLMs). It handles sending requests to the API, parsing responses, and providing functionality for accessing and managing models.

This class is used in the `hypotez` project to provide a consistent interface for interacting with different AI providers.

## Classes

### `class Glider`

**Description**: The `Glider` class represents the Glider.so AI model provider. It inherits from the `OpenaiTemplate` class, providing a specific implementation for interacting with the Glider.so API.

**Inherits**: `OpenaiTemplate`

**Attributes**:

- `label (str)`: The label of the provider, which is "Glider".
- `url (str)`: The base URL for the Glider.so website.
- `api_endpoint (str)`: The endpoint for the Glider.so API.
- `working (bool)`: Indicates whether the provider is currently functional.
- `default_model (str)`: The default model to use for interactions with the API.
- `models (List[str])`: A list of available models for the Glider.so API.
- `model_aliases (dict)`: A dictionary mapping aliases to the actual model names for easier use.

**Methods**:

- `__init__(self, **kwargs)`:  The constructor for the `Glider` class, initializing the attributes and inheriting from `OpenaiTemplate`. 
- `__repr__(self)`: Returns a string representation of the `Glider` object.
- `get_model_name(self, model: str) -> str`: Retrieves the actual model name from the aliases dictionary or returns the model name directly if it is not an alias.
- `get_models(self) -> List[str]`: Returns a list of all available models.
- `_prepare_request_data(self, prompt: str, model: str = None, temperature: float = 0.7, top_p: float = 0.95, max_tokens: int = 256, frequency_penalty: float = 0, presence_penalty: float = 0, stop: str = None) -> dict`: Prepares the request data for sending to the Glider.so API, including the prompt and model parameters.
- `_get_response_from_api(self, data: dict) -> dict`: Sends the request data to the Glider.so API and returns the response.
- `get_response(self, prompt: str, model: str = None, temperature: float = 0.7, top_p: float = 0.95, max_tokens: int = 256, frequency_penalty: float = 0, presence_penalty: float = 0, stop: str = None) -> dict`: Sends a request to the Glider.so API with the provided parameters and returns the response.

## Inner Functions

### `_prepare_request_data`

**Purpose**: Преобразует данные запроса в формат, подходящий для отправки на API Glider.so.

**Parameters**:

- `prompt (str)`: Текст запроса, который будет отправлен в API.
- `model (str)`: Имя модели для генерации текста.
- `temperature (float)`: Параметр, управляющий случайностью генерируемого текста.
- `top_p (float)`: Параметр, регулирующий вероятностный выбор слов.
- `max_tokens (int)`: Максимальное количество токенов, которые будут сгенерированы моделью.
- `frequency_penalty (float)`: Штраф за частое повторение слов.
- `presence_penalty (float)`: Штраф за наличие уже использованных слов.
- `stop (str)`: Строка, которая сигнализирует об окончании генерации текста.

**Returns**:

- `dict`: Словарь, содержащий все необходимые параметры для отправки запроса на API.

**How the Function Works**:

- Формирует словарь `data`, который будет отправлен в API. 
- Задает значение `prompt` для `data`.
- Если `model` указан, устанавливает значение `model` для `data`.
- Устанавливает значения для параметров `temperature`, `top_p`, `max_tokens`, `frequency_penalty`, `presence_penalty` и `stop`, если они не указаны по умолчанию.

**Example**:

```python
# Create an instance of the Glider class
glider = Glider()

# Prepare request data with a prompt and a model
data = glider._prepare_request_data(prompt="Tell me a joke.", model="chat-llama-3-1-70b")

# Print the prepared request data
print(data)
```

### `_get_response_from_api`

**Purpose**: Отправляет запрос на API Glider.so и получает ответ в формате JSON.

**Parameters**:

- `data (dict)`: Данные запроса, которые были подготовлены функцией `_prepare_request_data`.

**Returns**:

- `dict`: Словарь, содержащий ответ API в формате JSON.

**How the Function Works**:

- Выполняет отправку HTTP-запроса на API Glider.so с помощью библиотеки `requests`.
- Преобразует ответ API из JSON-формата в словарь Python.

**Example**:

```python
# Prepare request data
data = glider._prepare_request_data(prompt="Tell me a joke.", model="chat-llama-3-1-70b")

# Get the response from the API
response = glider._get_response_from_api(data)

# Print the response
print(response)
```

### `get_response`

**Purpose**: Отправляет запрос на API Glider.so и получает ответ в формате JSON.

**Parameters**:

- `prompt (str)`: Текст запроса, который будет отправлен в API.
- `model (str)`: Имя модели для генерации текста.
- `temperature (float)`: Параметр, управляющий случайностью генерируемого текста.
- `top_p (float)`: Параметр, регулирующий вероятностный выбор слов.
- `max_tokens (int)`: Максимальное количество токенов, которые будут сгенерированы моделью.
- `frequency_penalty (float)`: Штраф за частое повторение слов.
- `presence_penalty (float)`: Штраф за наличие уже использованных слов.
- `stop (str)`: Строка, которая сигнализирует об окончании генерации текста.

**Returns**:

- `dict`: Словарь, содержащий ответ API в формате JSON.

**How the Function Works**:

- Использует `_prepare_request_data` для подготовки данных запроса.
- Использует `_get_response_from_api` для отправки запроса и получения ответа.
- Возвращает полученный ответ.

**Example**:

```python
# Create an instance of the Glider class
glider = Glider()

# Send a request to the API
response = glider.get_response(prompt="Tell me a joke.", model="chat-llama-3-1-70b")

# Print the response
print(response)
```

## Parameter Details

- `prompt (str)`: The text of the query to be sent to the API.
- `model (str)`: The name of the model to use for text generation.
- `temperature (float)`: A parameter that controls the randomness of the generated text.
- `top_p (float)`: A parameter that regulates the probability-based selection of words.
- `max_tokens (int)`: The maximum number of tokens that will be generated by the model.
- `frequency_penalty (float)`: A penalty for the frequent repetition of words.
- `presence_penalty (float)`: A penalty for the presence of already used words.
- `stop (str)`: A string that signals the end of text generation.

## Examples

```python
# Import the Glider class
from hypotez.src.endpoints.gpt4free.g4f.Provider.Glider import Glider

# Create an instance of the Glider class
glider = Glider()

# Get a list of available models
models = glider.get_models()
print(models)

# Send a request to the API with a prompt and a model
response = glider.get_response(prompt="Tell me a joke.", model="chat-llama-3-1-70b")

# Print the response
print(response)
```