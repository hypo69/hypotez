# Module Documentation

## Overview

This module defines a provider for interacting with the ChatGPT.ai GPT-4 model. It includes functions for creating completions (generating responses) based on user messages.
The module is designed to integrate with the `g4f` framework within the `hypotez` project.

## More details
This code is used to interact with the ChatGPT.ai service, specifically using the GPT-4 model. It extracts necessary parameters from the website and sends a request to generate a response based on the provided chat messages. The module is an implementation of a provider for the `g4f` framework, allowing it to utilize ChatGPT.ai as one of its supported models.
The location of the file indicates that it is an endpoint, a provider to interact with `freegpt-webui-ru` via `g4f`.

## Module Content

### Global Variables

- `url` (str): The URL for the ChatGPT.ai GPT-4 endpoint.
- `model` (list): A list containing the model identifier (`'gpt-4'`).
- `supports_stream` (bool): Indicates whether the provider supports streaming responses (set to `False`).
- `needs_auth` (bool): Indicates whether the provider requires authentication (set to `False`).

## Functions

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает завершение (response) на основе предоставленных сообщений чата, используя ChatGPT.ai.

    Args:
        model (str): Идентификатор модели (например, "gpt-4").
        messages (list): Список сообщений чата, где каждое сообщение представляет собой словарь с ключами 'role' (например, 'user' или 'assistant') и 'content' (содержимое сообщения).
        stream (bool): Указывает, следует ли возвращать ответ в режиме потока (в данном случае всегда `False`).
        **kwargs: Дополнительные параметры.

    Yields:
        str: Сгенерированный ответ от ChatGPT.ai.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса.
        Exception: Если возникает какая-либо другая ошибка в процессе создания завершения.

    How it works:
    1. Функция принимает модель, список сообщений и флаг потоковой передачи.
    2. Формирует строку чата из списка сообщений, объединяя роль и содержимое каждого сообщения.
    3. Выполняет GET-запрос к указанному URL (`https://chatgpt.ai/gpt-4/`) для получения необходимых данных, таких как nonce, post_id и bot_id.
    4. Извлекает nonce, post_id и bot_id из HTML-ответа, используя регулярные выражения.
    5. Определяет заголовки (`headers`) для POST-запроса, включая `authority`, `accept`, `origin` и другие.
    6. Формирует данные (`data`) для POST-запроса, включая nonce, post_id, URL, действие (wpaicg_chat_shortcode_message), сообщение чата и bot_id.
    7. Выполняет POST-запрос к `https://chatgpt.ai/wp-admin/admin-ajax.php` с указанными заголовками и данными.
    8. Извлекает данные ответа в формате JSON и возвращает сгенерированный ответ (response) в виде строки.

    Example:
        >>> messages = [{"role": "user", "content": "Hello, how are you?"}]
        >>> model = "gpt-4"
        >>> stream = False
        >>> for response in _create_completion(model, messages, stream):
        ...     print(response)
        <Response from ChatGPT.ai>
    """
    chat = ''
    for message in messages:
        chat += '%s: %s\n' % (message['role'], message['content'])
    chat += 'assistant: '

    response = requests.get('https://chatgpt.ai/gpt-4/')

    nonce, post_id, _, bot_id = re.findall(r'data-nonce="(.*)"\n     data-post-id="(.*)"\n     data-url="(.*)"\n     data-bot-id="(.*)"\n     data-width', response.text)[0]

    headers = {
        'authority': 'chatgpt.ai',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'origin': 'https://chatgpt.ai',
        'pragma': 'no-cache',
        'referer': 'https://chatgpt.ai/gpt-4/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    data = {
        '_wpnonce': nonce,
        'post_id': post_id,
        'url': 'https://chatgpt.ai/gpt-4',
        'action': 'wpaicg_chat_shortcode_message',
        'message': chat,
        'bot_id': bot_id
    }

    response = requests.post('https://chatgpt.ai/wp-admin/admin-ajax.php',
                            headers=headers, data=data)

    yield (response.json()['data'])
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

This line constructs a string that describes the supported parameters of the `_create_completion` function.
It uses the `get_type_hints` function to dynamically retrieve the type hints for each parameter of the `_create_completion` function.
The result is a string that includes the module name and the parameter names along with their types.

Example:
```text
'g4f.Providers.ChatgptAi supports: (model: str, messages: list, stream: bool)'