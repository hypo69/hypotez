# Module for Providing Access to GetGpt Provider

## Overview

This module facilitates interaction with the GetGpt provider for generating text completions. It includes functions for encrypting data, padding data to match block sizes, and creating completion requests. The module is designed to be used within the `hypotez` project and supports streaming responses.

## More details

The module provides the `_create_completion` function, which sends requests to the GetGpt service and yields the generated content. The encryption and padding functions ensure secure data transmission. The module also specifies supported parameters and their types for the `_create_completion` function.

## Functions

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция создает запрос на завершение текста с использованием GetGpt.

    Args:
        model (str): Идентификатор модели для использования.
        messages (list): Список сообщений для отправки в запросе.
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу.
        **kwargs: Дополнительные параметры для запроса, такие как `frequency_penalty`, `max_tokens`, `presence_penalty`, `temperature` и `top_p`.

    Returns:
        Generator[str, None, None]: Генератор, выдающий текстовые фрагменты из потокового ответа.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса.
        json.JSONDecodeError: Если не удается декодировать JSON из ответа.

    How the function works:
    - Функция `_create_completion` принимает параметры модели, сообщения и потоковую передачу, а также дополнительные параметры.
    - Определяет внутреннюю функцию `encrypt`, которая шифрует данные с использованием AES.
    - Определяет внутреннюю функцию `pad_data`, которая дополняет данные до размера блока AES.
    - Формирует заголовки HTTP-запроса, включая `Content-Type`, `Referer` и `user-agent`.
    - Преобразует данные запроса в JSON-формат, включая сообщения, параметры и UUID.
    - Отправляет POST-запрос на URL-адрес `https://chat.getgpt.world/api/chat/stream` с зашифрованными данными.
    - Итерируется по строкам ответа, декодирует их и извлекает содержимое из JSON, если строка содержит `"content"`.
    - Выдает извлеченное содержимое как часть генератора.

    Internal functions:
    - encrypt: Encrypts the given data using AES encryption.
        Args:
            e (str): The data to be encrypted.
        Returns:
            str: The encrypted data as a hexadecimal string.
    - pad_data: Pads the given data to a multiple of the AES block size.
        Args:
            data (bytes): The data to be padded.
        Returns:
            bytes: The padded data.

    Examples:
        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Hello, GetGpt!"}]
        >>> stream = True
        >>> for chunk in _create_completion(model, messages, stream):
        ...     print(chunk, end="")
    """
    def encrypt(e):
        """Шифрует предоставленные данные с использованием шифрования AES.

        Args:
            e (str): Данные для шифрования.

        Returns:
            str: Зашифрованные данные в виде шестнадцатеричной строки.
        """
        ...

    def pad_data(data: bytes) -> bytes:
        """Дополняет предоставленные данные до размера, кратного размеру блока AES.

        Args:
            data (bytes): Данные для дополнения.

        Returns:
            bytes: Дополненные данные.
        """
        ...
```

### `encrypt` (внутренняя функция `_create_completion`)

```python
def encrypt(e):
    """Шифрует предоставленные данные с использованием шифрования AES.

    Args:
        e (str): Данные для шифрования.

    Returns:
        str: Зашифрованные данные в виде шестнадцатеричной строки.
    """
    ...
```

### `pad_data` (внутренняя функция `_create_completion`)

```python
def pad_data(data: bytes) -> bytes:
    """Дополняет предоставленные данные до размера, кратного размеру блока AES.

    Args:
        data (bytes): Данные для дополнения.

    Returns:
        bytes: Дополненные данные.
    """
    ...
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(\
        [f'{name}: {get_type_hints(_create_completion)[name].__name__}' for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

## Module Parameters

- `url` (str): URL-адрес для службы GetGpt.
- `model` (list): Список поддерживаемых моделей (по умолчанию `['gpt-3.5-turbo']`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (по умолчанию `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (по умолчанию `False`).

## Examples

A basic example of how to use the `_create_completion` function:

```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, GetGpt!"}]
stream = True

for chunk in _create_completion(model, messages, stream):
    print(chunk, end="")
```