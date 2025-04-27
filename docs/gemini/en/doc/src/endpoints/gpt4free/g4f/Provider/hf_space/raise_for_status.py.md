# Module for Handling Response Status Errors

## Overview

This module contains the `raise_for_status` function, which is responsible for handling HTTP response status errors. The function analyzes the response from an HTTP request and raises a `ResponseStatusError` if the response status code indicates an error. This function is essential for gracefully handling errors that occur during communication with external APIs or services. 

## Details

The `raise_for_status` function checks the response status code from an HTTP request. If the status code is not `200 OK`, it analyzes the response content, attempting to extract a more specific error message. If the content type is "application/json", it attempts to parse the JSON data and extract an error message. If the content type is "text/html" or the response starts with "<!DOCTYPE", it assumes HTML content and sets the error message accordingly. Otherwise, it uses the plain response text as the error message. Finally, it raises a `ResponseStatusError` with the extracted error message and the HTTP status code.

## Functions

### `raise_for_status`

```python
async def raise_for_status(response: Union[StreamResponse, ClientResponse], message: str = None):
    """
    Проверяет HTTP-ответ на наличие ошибок и генерирует исключение в случае ошибки.

    Args:
        response (Union[StreamResponse, ClientResponse]): HTTP-ответ, полученный от запроса.
        message (str, optional): Дополнительное сообщение об ошибке. Defaults to None.

    Raises:
        ResponseStatusError: Если в HTTP-ответе содержится ошибка (код состояния не 200 OK).

    Example:
        >>> response = await get_data_from_api()
        >>> await raise_for_status(response)
        >>> data = await response.json()  # Продолжаем работу с данными, если нет ошибки

    """
    ...
```

**Purpose**: This function checks the HTTP response for errors and raises an exception if an error occurs.

**Parameters**:

- `response` (Union[StreamResponse, ClientResponse]): The HTTP response received from the request.
- `message` (str, optional): An additional error message. Defaults to None.

**Returns**:
- None: If the response is successful (status code 200 OK).

**Raises Exceptions**:
- `ResponseStatusError`: If there is an error in the HTTP response (status code is not 200 OK).

**How the Function Works**:

1. The function first checks if the response status code is `200 OK`. If it is, the function returns without doing anything.
2. If the response status code is not `200 OK`, the function attempts to extract an error message from the response content. It first checks if the content type is "application/json". If it is, the function attempts to parse the JSON data and extract an error message.
3. If the content type is not "application/json", the function checks if the content type is "text/html" or if the response starts with "<!DOCTYPE". If it is, the function assumes HTML content and sets the error message accordingly.
4. If the content type is not "application/json" or "text/html", the function uses the plain response text as the error message.
5. Finally, the function raises a `ResponseStatusError` with the extracted error message and the HTTP status code.

**Examples**:

```python
# Example 1: Successful response
>>> response = await get_data_from_api() # Function returning the response
>>> await raise_for_status(response)
>>> data = await response.json() # Processing data if there is no error

# Example 2: Error response with JSON content
>>> response = await get_data_from_api() 
>>> await raise_for_status(response)
Traceback (most recent call last):
  ...
ResponseStatusError: Response 400: Invalid request parameters

# Example 3: Error response with HTML content
>>> response = await get_data_from_api()
>>> await raise_for_status(response)
Traceback (most recent call last):
  ...
ResponseStatusError: Response 500: HTML content

# Example 4: Error response with plain text content
>>> response = await get_data_from_api()
>>> await raise_for_status(response)
Traceback (most recent call last):
  ...
ResponseStatusError: Response 404: Not Found
```

**Inner Functions**: None.

**Parameter Details**:

- `response` (Union[StreamResponse, ClientResponse]): This parameter represents the HTTP response object received from the request. It can be either a `StreamResponse` object, which represents a stream of data, or a `ClientResponse` object, which represents a full response. The function uses the `response` object to access its attributes, such as the status code, headers, and content.

- `message` (str, optional): This parameter is an optional additional error message. It can be used to provide more context or details about the error. For example, if the function detects a specific error condition, it can set this parameter to a descriptive message that explains the error. The function uses the `message` parameter to augment the error message that it ultimately raises.

**How the Function Works**:

- The function first checks if the response is successful. If it is (the response status code is 200 OK), the function simply returns without doing anything.
- If the response is not successful, the function attempts to extract a more specific error message from the response content. 
- First, it tries to extract a JSON error message. If successful, it extracts the `error` or `message` key from the JSON data.
- If there is no JSON content, the function checks if the response is HTML. If it is, the function assumes that the error message is contained in the HTML content. 
- Otherwise, the function uses the plain response text as the error message.
- Finally, the function raises a `ResponseStatusError` with the extracted error message and the HTTP status code.