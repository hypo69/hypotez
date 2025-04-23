# Модуль `Liaobots.py`

## Обзор

Модуль предназначен для взаимодействия с провайдером Liaobots для получения ответов от языковых моделей, таких как GPT-3.5 Turbo и GPT-4. Он включает в себя функции для создания запросов к API Liaobots и обработки ответов.

## Подробнее

Модуль содержит конфигурацию для подключения к API Liaobots, определения поддерживаемых моделей и параметров запросов. Он использует библиотеку `requests` для выполнения HTTP-запросов и возвращает ответы в виде потока текста.

## Параметры модуля

- `url` (str): URL API Liaobots (`https://liaobots.com`).
- `model` (list): Список поддерживаемых моделей (`gpt-3.5-turbo`, `gpt-4`).
- `supports_stream` (bool): Поддержка потоковой передачи ответов (`True`).
- `needs_auth` (bool): Необходимость аутентификации (`True`).
- `models` (dict): Словарь с информацией о поддерживаемых моделях, включая их идентификаторы, имена, максимальную длину и лимит токенов.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """Создает запрос к API Liaobots и возвращает ответ в виде потока текста.

    Args:
        model (str): Идентификатор используемой модели (`gpt-3.5-turbo` или `gpt-4`).
        messages (list): Список сообщений для отправки в запросе.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи ответов.
        **kwargs: Дополнительные параметры, такие как ключ аутентификации.

    Returns:
        Generator[str, None, None]: Генератор, возвращающий токены ответа в виде текста.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при выполнении HTTP-запроса.
        Exception: Если возникает ошибка при обработке ответа.

    Внутренние функции:
        Отсутствуют
    
    
        Функция `_create_completion` отправляет POST-запрос к API Liaobots для создания завершения на основе предоставленных параметров. Она формирует заголовок и полезную нагрузку JSON, включая conversationId, модель, сообщения и ключ.Затем функция выполняет POST-запрос к API `https://liaobots.com/api/chat` с указанными заголовками и данными JSON, устанавливая `stream=True` для потоковой передачи ответа.
        После этого итерируется по содержимому ответа, читая его по частям (размером 2046 байт). Каждая часть декодируется из `utf-8` и передается через `yield`, что позволяет возвращать ответ в виде потока.

    Примеры:
        Пример 1: Создание запроса с моделью 'gpt-3.5-turbo' и списком сообщений.
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
        >>> stream = True
        >>> auth_key = 'your_auth_key'  # Replace with your actual auth key
        >>> generator = _create_completion(model=model, messages=messages, stream=stream, auth=auth_key)
        >>> for token in generator:
        ...     print(token)

        Пример 2: Использование модели 'gpt-4' с аутентификацией.
        >>> model = 'gpt-4'
        >>> messages = [{'role': 'user', 'content': 'Tell me a joke.'}]
        >>> stream = False
        >>> auth_key = 'your_auth_key'  # Replace with your actual auth key
        >>> generator = _create_completion(model=model, messages=messages, stream=stream, auth=auth_key)
        >>> for token in generator:
        ...     print(token)
    """
    headers = {
        'authority': 'liaobots.com',
        'content-type': 'application/json',
        'origin': 'https://liaobots.com',
        'referer': 'https://liaobots.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-auth-code': kwargs.get('auth')
    }

    json_data = {
        'conversationId': str(uuid.uuid4()),
        'model': models[model],
        'messages': messages,
        'key': '',
        'prompt': "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
    }

    response = requests.post('https://liaobots.com/api/chat', 
                             headers=headers, json=json_data, stream=True)

    for token in response.iter_content(chunk_size=2046):
        yield (token.decode('utf-8'))
```

## Параметры

- `params` (str): Строка, содержащая информацию о поддерживаемых параметрах функции `_create_completion`.