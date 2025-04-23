# Модуль Aichat

## Обзор

Модуль `Aichat.py` предоставляет функциональность для взаимодействия с API `chat-gpt.org` с целью генерации текста на основе предоставленных сообщений. Он включает функцию `_create_completion`, которая отправляет запрос к API и возвращает сгенерированный текст.

## Подробней

Модуль предназначен для использования в качестве провайдера в проекте `hypotez`. Он определяет параметры подключения к API `chat-gpt.org` и обрабатывает запросы к нему.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает завершение текста на основе предоставленных сообщений, используя API chat-gpt.org.

    Args:
        model (str): Имя модели, используемой для генерации текста.
        messages (list): Список сообщений, используемых в качестве контекста для генерации.
                         Каждое сообщение должно быть словарем с ключами 'role' (роль отправителя) и 'content' (содержимое сообщения).
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
        **kwargs: Дополнительные аргументы.

    Returns:
        generator: Генератор, выдающий сгенерированный текст.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса к API.
        json.JSONDecodeError: Если не удается декодировать JSON-ответ от API.

    Как работает функция:
    - Функция принимает список сообщений и преобразует его в строку, где каждое сообщение форматируется как "role: content".
    - Затем формируются заголовки HTTP-запроса, включающие информацию о типе контента, источнике запроса и User-Agent.
    - Подготавливается JSON-данные с сообщением, температурой, штрафами за присутствие и частоту, а также вероятностью top_p.
    - Отправляется POST-запрос к API chat-gpt.org/api/text с указанными заголовками и данными.
    - Функция возвращает ответ, декодированный из JSON, извлекая поле 'message', при помощи yield.

    Примеры:
        Пример 1:
        model = "gpt-3.5-turbo"
        messages = [{"role": "user", "content": "Hello!"}]
        stream = False
        completion = _create_completion(model=model, messages=messages, stream=stream)
        for item in completion:
            print(item)
        
        Пример 2:
        model = "gpt-3.5-turbo"
        messages = [{"role": "user", "content": "Как дела?"}, {"role":"assistant", "content":"Отлично!"}]
        stream = False
        completion = _create_completion(model=model, messages=messages, stream=stream)
        for item in completion:
            print(item)
    """
    base = ''
    for message in messages:
        base += '%s: %s\n' % (message['role'], message['content'])
    base += 'assistant:'

    headers = {
        'authority': 'chat-gpt.org',
        'accept': '*/*',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://chat-gpt.org',
        'pragma': 'no-cache',
        'referer': 'https://chat-gpt.org/chat',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    json_data = {
        'message': base,
        'temperature': 1,
        'presence_penalty': 0,
        'top_p': 1,
        'frequency_penalty': 0
    }

    response = requests.post('https://chat-gpt.org/api/text', headers=headers, json=json_data)
    yield response.json()['message']
```

## Параметры

- `url` (str): URL API `chat-gpt.org`.
- `model` (list): Список поддерживаемых моделей (`gpt-3.5-turbo`).
- `supports_stream` (bool): Указывает, поддерживается ли потоковая передача данных (`False`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (`False`).
- `params` (str): Строка, содержащая информацию о поддерживаемых типах параметров функции `_create_completion`.