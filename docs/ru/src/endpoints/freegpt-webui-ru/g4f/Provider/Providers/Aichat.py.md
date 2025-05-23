# Модуль `Aichat.py`

## Обзор

Модуль предоставляет интерфейс для взаимодействия с провайдером Aichat через API `chat-gpt.org`. Он позволяет отправлять запросы к модели `gpt-3.5-turbo` и получать ответы.

## Подробнее

Модуль содержит функцию `_create_completion`, которая формирует запрос на основе предоставленных сообщений и отправляет его к API. Результат возвращается в виде генератора.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция отправляет запрос к API chat-gpt.org и возвращает ответ.

    Args:
        model (str): Идентификатор модели, используемый для генерации ответа.
        messages (list): Список сообщений, представляющих историю диалога.
                         Каждое сообщение - словарь с ключами 'role' (роль отправителя) и 'content' (содержание сообщения).
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
                       В данном случае всегда `False`, так как `supports_stream = False`.
        **kwargs: Дополнительные параметры, которые могут быть переданы в API.

    Yields:
        str: Сгенерированный ответ от API.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при отправке запроса к API.
        json.JSONDecodeError: В случае ошибки при декодировании JSON-ответа от API.

    
    - Функция итерируется по списку сообщений, формируя строку `base`, которая содержит роль и контент каждого сообщения, разделенные символом новой строки.
    - Далее, формируются HTTP-заголовки `headers` для запроса к API, включающие информацию о браузере, типе контента и источнике запроса.
    - Подготавливается JSON-тело запроса `json_data`, содержащее сформированное сообщение `base`, параметры температуры, штрафов за присутствие и частоту, а также верхний предел вероятности.
    - Функция отправляет POST-запрос к API `https://chat-gpt.org/api/text` с использованием библиотеки `requests`.
    - Полученный ответ преобразуется в формат JSON и извлекается значение ключа `message`, которое возвращается как результат работы функции.

    Примеры:
        >>> messages = [{'role': 'user', 'content': 'Hello'}]; model = 'gpt-3.5-turbo'; stream = False
        >>> for response in _create_completion(model, messages, stream):
        ...     print(response)
        ...
        {'message': 'Hello assistant!'}

    """
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({0})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
```

**Назначение**: Строка `params` формируется для отображения информации о поддерживаемых параметрах функции `_create_completion`.

## Переменные

-   `url` (str): URL для взаимодействия с API `chat-gpt.org`.
-   `model` (list): Список поддерживаемых моделей (`gpt-3.5-turbo`).
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (в данном случае `False`).
-   `needs_auth` (bool): Указывает, требуется ли аутентификация для взаимодействия с API (в данном случае `False`).