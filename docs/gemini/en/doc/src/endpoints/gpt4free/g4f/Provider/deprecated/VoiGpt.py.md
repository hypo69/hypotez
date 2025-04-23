# Module `VoiGpt.py`

## Overview

This module implements the `VoiGpt` class, which is a provider for the VoiGpt.com service. The module is designed to interact with the VoiGpt API for generating responses based on provided messages. It handles the process of obtaining CSRF tokens and sending requests to the VoiGpt server.

## More details

This module facilitates communication with the VoiGpt.com service, managing the complexities of session tokens and request formatting. It is essential for integrating the VoiGpt service into larger applications within the `hypotez` project. The class inherits from `AbstractProvider`, providing a standardized interface for different providers.

## Classes

### `VoiGpt`

**Description**:
The `VoiGpt` class is a provider that interacts with the VoiGpt.com service to generate responses based on user messages.

**Inherits**:
- `AbstractProvider`: Inherits from the `AbstractProvider` class, which likely defines a common interface for different providers in the `hypotez` project.

**Attributes**:
- `url` (str): The base URL for the VoiGpt.com service.
- `working` (bool): A flag indicating whether the provider is currently working (likely deprecated).
- `supports_gpt_35_turbo` (bool): A flag indicating whether the provider supports the "gpt-3.5-turbo" model.
- `supports_message_history` (bool): A flag indicating whether the provider supports message history.
- `supports_stream` (bool): A flag indicating whether the provider supports streaming responses.
- `_access_token` (str): An internal attribute to store the CSRF access token.

**Methods**:
- `create_completion()`: Method for generating a completion from the VoiGpt service.

**Working principle**:
The `VoiGpt` class works by first obtaining a CSRF token from the VoiGpt.com website. This token is then used in subsequent requests to the API. The `create_completion` method sends a payload containing the user's messages to the VoiGpt API and yields the response.

## Class Methods

### `create_completion`

```python
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    access_token: str = None,
    **kwargs
) -> CreateResult:
    """ Функция выполняет запрос к VoiGpt.com для генерации ответа на основе предоставленных сообщений.

    Args:
        cls: Класс, для которого вызывается метод.
        model (str): Имя модели, используемой для генерации ответа.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу.
        proxy (str, optional): Адрес прокси-сервера для использования. По умолчанию `None`.
        access_token (str, optional): Токен доступа для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы ключевого слова.

    Returns:
        CreateResult: Результат создания завершения.

    Raises:
        RuntimeError: Если получен неожиданный ответ от сервера.

    Example:
        >>> VoiGpt.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}], stream=False)
        <generator object VoiGpt.create_completion at 0x...>
    """
```

**Parameters**:
- `model` (str): The name of the model to use for generating the response. If not provided, defaults to "gpt-3.5-turbo".
- `messages` (Messages): A list of messages to send to the VoiGpt API.
- `stream` (bool): A flag indicating whether to use streaming.
- `proxy` (str, optional): The address of a proxy server to use. Defaults to `None`.
- `access_token` (str, optional): The access token for authentication. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**How the function works**:
1. Sets the default model to "gpt-3.5-turbo" if no model is provided.
2. Checks if an access token is provided; if not, it tries to use the class's `_access_token`.
3. If no access token is available, it retrieves a CSRF token from the VoiGpt.com website by sending a GET request and parsing the cookies.
4. Sets up headers for the POST request, including the CSRF token.
5. Constructs a payload with the messages.
6. Sends a POST request to the `/generate_response/` endpoint of the VoiGpt.com API.
7. Parses the JSON response and yields the "response" field.
8. Raises a `RuntimeError` if the response cannot be parsed or if an error occurs.

**Examples**:

```python
# Example call
VoiGpt.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}], stream=False)