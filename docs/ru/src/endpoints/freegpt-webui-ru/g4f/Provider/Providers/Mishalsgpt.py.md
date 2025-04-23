# Документация модуля `Mishalsgpt.py`

## Обзор

Модуль предоставляет реализацию провайдера `Mishalsgpt` для работы с моделями `gpt-3.5-turbo-16k-0613` и `gpt-3.5-turbo` через API `https://mishalsgpt.vercel.app`. Он позволяет отправлять запросы к моделям и получать ответы в потоковом режиме.

## Подробней

Модуль содержит функции для создания запросов к API `Mishalsgpt` и обработки ответов. Он использует библиотеку `requests` для отправки HTTP-запросов и ожидает ответы в формате JSON. Модуль также определяет параметры, поддерживаемые провайдером, и их типы.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к API Mishalsgpt для получения ответа от модели.

    Args:
        model (str): Имя модели для использования.
        messages (list): Список сообщений для отправки в модель.
        stream (bool): Флаг, указывающий, следует ли возвращать ответ в потоковом режиме.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Часть ответа от модели.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при отправке запроса к API.

    Принцип работы:
        - Функция формирует HTTP-запрос к API `https://mishalsgpt.vercel.app/api/openai/v1/chat/completions` с использованием метода `POST`.
        - Запрос содержит параметры `model`, `temperature` и `messages` в формате JSON.
        - Если запрос успешен, функция возвращает ответ в потоковом режиме, извлекая содержимое сообщения из JSON-ответа.
        - Функция обрабатывает исключения, которые могут возникнуть при отправке запроса, и логирует ошибки.

    Внутренние функции:
        - Отсутствуют

    Примеры:
        >>> model_name = 'gpt-3.5-turbo'
        >>> messages_list = [{'role': 'user', 'content': 'Hello, how are you?'}]
        >>> stream_flag = True
        >>> completion = _create_completion(model_name, messages_list, stream_flag)
        >>> for part in completion:
        ...     print(part)
        I am doing well, thank you for asking. How can I assist you today?
    """
    ...
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

Содержит строку, описывающую поддерживаемые параметры функции `_create_completion`.
```