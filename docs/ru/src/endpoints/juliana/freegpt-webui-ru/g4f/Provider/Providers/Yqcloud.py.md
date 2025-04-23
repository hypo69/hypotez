# Модуль Yqcloud

## Обзор

Модуль `Yqcloud.py` предоставляет реализацию взаимодействия с сервисом `chat9.yqcloud.top` для генерации текста на основе модели `gpt-3.5-turbo`. Он использует библиотеку `requests` для выполнения HTTP-запросов к API и поддерживает потоковую передачу данных.

## Подробней

Этот модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется функциональность генерации текста с использованием указанного сервиса. Он автоматически декодирует токен ответа, попутно удаляя `b'always respond in english'`.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция отправляет запрос к API `chat9.yqcloud.top` для генерации текста на основе предоставленных сообщений.

    Args:
        model (str): Имя используемой модели (в данном случае всегда `gpt-3.5-turbo`).
        messages (list): Список сообщений, используемых для генерации текста. Каждое сообщение представляет собой словарь с ключом `content`, содержащим текст сообщения.
        stream (bool): Указывает, следует ли использовать потоковый режим передачи данных.
        **kwargs: Дополнительные параметры.

    Yields:
        str: Части сгенерированного текста в кодировке UTF-8.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при выполнении HTTP-запроса.
        UnicodeDecodeError: В случае ошибки при декодировании полученных данных.

    Внутренние функции:
        - Отсутствуют

    
    1. Функция определяет заголовки HTTP-запроса, включая `authority`, `origin`, `referer` и `user-agent`.
    2. Формирует JSON-данные для запроса, включающие текст последнего сообщения из списка `messages`, ID пользователя, флаг `network`, ключ API и другие параметры.
    3. Выполняет POST-запрос к API `https://api.aichatos.cloud/api/generateStream` с установленными заголовками и JSON-данными, используя потоковый режим.
    4. Итерируется по содержимому ответа, полученного от сервера, с размером чанка 2046 байт.
    5. Проверяет, содержит ли токен подстроку `b'always respond in english'`.
    6. Если подстрока отсутствует, декодирует токен в кодировке UTF-8 и возвращает его как часть сгенерированного текста.

    Примеры:
        Пример 1:
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'content': 'Напиши стихотворение о весне.'}]
        >>> stream = True
        >>> generator = _create_completion(model, messages, stream)
        >>> for chunk in generator:
        ...     print(chunk, end='')

        Пример 2:
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'content': 'Translate to English: Здравствуй, мир!'}]
        >>> stream = True
        >>> generator = _create_completion(model, messages, stream)
        >>> for chunk in generator:
        ...     print(chunk, end='')
    """
    headers = {
        'authority': 'api.aichatos.cloud',
        'origin': 'https://chat9.yqcloud.top',
        'referer': 'https://chat9.yqcloud.top/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    json_data = {
        'prompt': 'always respond in english | %s' % messages[-1]['content'],
        'userId': f'#/chat/{int(time.time() * 1000)}',
        'network': True,
        'apikey': '',
        'system': '',
        'withoutContext': False,
    }

    response = requests.post('https://api.aichatos.cloud/api/generateStream', headers=headers, json=json_data, stream=True)
    for token in response.iter_content(chunk_size=2046):
        if not b'always respond in english' in token:
            yield (token.decode('utf-8'))
```

## Переменные

- `url` (str): URL сервиса `chat9.yqcloud.top`.
- `model` (list): Список поддерживаемых моделей (в данном случае `gpt-3.5-turbo`).
- `supports_stream` (bool): Указывает на поддержку потоковой передачи данных (в данном случае `True`).
- `needs_auth` (bool): Указывает на необходимость аутентификации (в данном случае `False`).
- `params` (str): Строка, содержащая информацию о поддерживаемых типах данных для функции `_create_completion`.