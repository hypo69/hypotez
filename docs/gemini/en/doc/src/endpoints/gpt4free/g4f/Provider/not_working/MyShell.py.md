# Module for Interacting with the MyShell AI Service

## Overview

This module implements the `MyShell` class, which allows interaction with the MyShell AI service. It supports GPT-3.5 Turbo and streaming responses. This module is part of the `hypotez` project and is designed to facilitate communication with the MyShell AI platform through its API.

## More details

The `MyShell` class enables sending messages to the MyShell AI service and receiving responses. It uses a WebDriver session to bypass Cloudflare protection and interact with the API. It constructs and sends JSON payloads to the MyShell API endpoint and processes streaming responses to extract content.

## Classes

### `MyShell`

**Description**: Класс для взаимодействия с AI-сервисом MyShell.
**Наследует**:
- `AbstractProvider`: Класс `MyShell` наследуется от `AbstractProvider`, что позволяет интегрировать его в общую систему провайдеров `hypotez`.

**Атрибуты**:
- `url` (str): URL-адрес сервиса MyShell (`https://app.myshell.ai/chat`).
- `working` (bool): Флаг, указывающий, работает ли сервис. По умолчанию `False`.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживается ли модель GPT-3.5 Turbo. Установлен в `True`.
- `supports_stream` (bool): Флаг, указывающий, поддерживается ли потоковая передача ответов. Установлен в `True`.

**Working principle**:
- The class defines static methods and interacts directly with the API MyShell.
- It inherits from `AbstractProvider` to implement a uniform interface for various AI models.
- Uses `WebDriverSession` to bypass Cloudflare and ensure reliable communication with the service.
- Supports sending messages and receiving streaming responses from the MyShell AI service.

## Class Methods

### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    timeout: int = 120,
    webdriver = None,
    **kwargs
) -> CreateResult:
    """ Функция отправляет сообщения в AI-сервис MyShell и возвращает ответ.
    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа. По умолчанию `120`.
        webdriver: Экземпляр веб-драйвера для обхода Cloudflare.
        **kwargs: Дополнительные аргументы.

    Returns:
        CreateResult: Результат создания завершения.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с сервисом.

    """
```

#### Internal functions:

##### `WebDriverSession`
```python
class WebDriverSession:
    """ Класс для управления сессией веб-драйвера.

    Attributes:
        webdriver: Экземпляр веб-драйвера.
        url (str): URL для посещения.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

    """
```

##### `bypass_cloudflare`
```python
def bypass_cloudflare(driver, url: str, timeout: int):
    """ Функция обходит защиту Cloudflare.

    Args:
        driver: Экземпляр веб-драйвера.
        url (str): URL для посещения.
        timeout (int): Время ожидания.

    """
```

#### How the function works:
1. **Initialization**: The function accepts parameters such as model, messages, stream, proxy, timeout and webdriver to configure the call to the MyShell API.
2. **WebDriver Session**: Creates a WebDriver session using the `WebDriverSession` context manager to automate browser interactions, including bypassing Cloudflare.
3. **Bypassing Cloudflare**: Uses the `bypass_cloudflare` function to bypass Cloudflare protection, ensuring access to the MyShell API.
4. **Message Formatting**: The `format_prompt` function formats the message list into a string suitable for sending to the MyShell API.
5. **Data Preparation**: Constructs a JSON payload containing the bot ID, conversation scenario, message, and message type.
6. **Sending a Request**: Uses `driver.execute_script` to send an asynchronous request to the MyShell API endpoint (`https://api.myshell.ai/v1/bot/chat/send_message`). Includes setting necessary headers such as `accept`, `content-type`, `myshell-service-name`, and `visitor-id`.
7. **Streaming Responses**: Reads streaming responses from the API using `TextDecoderStream` and processes each chunk to extract content. The received data is parsed as JSON, and the content is extracted and concatenated.
8. **Return of results**: Uses a loop to continuously read streaming responses, yielding each extracted chunk. Breaks the loop when there is no more data.

#### Examples:

```python
# Example usage of create_completion
messages = [{"role": "user", "content": "Hello, MyShell!"}]
stream = True
model = "gpt-3.5-turbo"
# Assuming 'driver' is an instance of a configured WebDriver
# result_generator = MyShell.create_completion(model=model, messages=messages, stream=stream, webdriver=driver)
# for chunk in result_generator:
#     print(chunk)
```
```python
# Example usage with proxy
messages = [{"role": "user", "content": "Tell me a joke."}]
stream = True
model = "gpt-3.5-turbo"
proxy = "http://your_proxy:8080"
# result_generator = MyShell.create_completion(model=model, messages=messages, stream=stream, proxy=proxy, webdriver=driver)
# for chunk in result_generator:
#     print(chunk)
```
```python
# Example usage without stream
messages = [{"role": "user", "content": "Explain quantum physics."}]
stream = False
model = "gpt-3.5-turbo"
# result = MyShell.create_completion(model=model, messages=messages, stream=stream, webdriver=driver)
# print(result)
```