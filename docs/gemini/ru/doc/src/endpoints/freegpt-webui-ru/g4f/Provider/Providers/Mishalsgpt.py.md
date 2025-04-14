# Модуль Mishalsgpt

## Обзор

Модуль `Mishalsgpt` предоставляет интерфейс для взаимодействия с API `mishalsgpt.vercel.app` для получения ответов от моделей, таких как `gpt-3.5-turbo-16k-0613` и `gpt-3.5-turbo`. Он поддерживает потоковую передачу данных и не требует аутентификации.

## Подробней

Модуль содержит функции для создания запросов к API и обработки ответов. Он использует библиотеку `requests` для отправки HTTP-запросов и возвращает контент в формате JSON.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к API для получения ответа от модели.

    Args:
        model (str): Идентификатор модели для использования.
        messages (list): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
        **kwargs: Дополнительные параметры.

    Yields:
        str: Контент ответа от API.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса.

    Example:
        >>> model_id = 'gpt-3.5-turbo'
        >>> messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
        >>> stream = True
        >>> response = _create_completion(model_id, messages, stream)
        >>> for chunk in response:
        ...     print(chunk)
    """
    ...
```

**Назначение**:
Функция `_create_completion` отправляет запрос к API `mishalsgpt.vercel.app` и возвращает ответ от модели.

**Параметры**:
- `model` (str): Идентификатор модели, которую необходимо использовать (например, `'gpt-3.5-turbo-16k-0613'`).
- `messages` (list): Список сообщений, отправляемых в API. Каждое сообщение представляет собой словарь с ключами `'role'` и `'content'`.
- `stream` (bool): Флаг, определяющий, использовать ли потоковую передачу данных. Если `True`, функция возвращает генератор, выдающий данные по частям.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в API.

**Возвращает**:
- `Generator[str, None, None]`: Генератор, выдающий контент ответа от API.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: Если возникает ошибка при отправке запроса.

**Как работает функция**:
1. Функция формирует заголовок `headers` с указанием типа контента `'application/json'`.
2. Формирует тело запроса `data` в виде словаря, включающего идентификатор модели (`model`), температуру (`temperature`), и список сообщений (`messages`).
3. Отправляет POST-запрос к API `url + '/api/openai/v1/chat/completions'` с использованием библиотеки `requests`. Указывается, что запрос должен быть потоковым (`stream=True`).
4. Получает ответ от API и извлекает контент из JSON-структуры ответа.
5. Возвращает генератор, который выдает контент ответа.

**Примеры**:

```python
model_id = 'gpt-3.5-turbo'
messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
stream = True
response = _create_completion(model_id, messages, stream)
for chunk in response:
    print(chunk)
```

## Переменные

- `url` (str): URL-адрес API `mishalsgpt.vercel.app`.
- `model` (list): Список поддерживаемых моделей (например, `gpt-3.5-turbo-16k-0613`, `gpt-3.5-turbo`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (в данном случае `True`).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (в данном случае `False`).
- `params` (str): Строка, содержащая информацию о поддерживаемых типах параметров функции `_create_completion`.