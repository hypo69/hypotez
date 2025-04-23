# Документация модуля Gravityengine

## Обзор

Модуль `Gravityengine` предназначен для взаимодействия с сервисом `gpt4.gravityengine.cc` для получения ответов от моделей GPT. Он предоставляет функцию `_create_completion`, которая отправляет запросы к API и возвращает сгенерированный контент. Модуль поддерживает потоковую передачу данных и не требует аутентификации.

## Подробней

Модуль содержит функции для отправки запросов к API `gpt4.gravityengine.cc` и получения ответов от моделей GPT.
Он использует библиотеку `requests` для отправки HTTP-запросов и модуль `json` для обработки JSON-ответов.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция создает запрос к API для получения ответа от GPT модели.

    Args:
        model (str): Идентификатор модели, используемой для генерации ответа.
        messages (list): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
        **kwargs: Дополнительные параметры.

    Returns:
        Generator[str, None, None]: Генератор, возвращающий контент ответа от модели.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    Как работает функция:
        1. Определяет заголовки запроса, указывая тип контента как JSON.
        2. Формирует данные запроса, включая модель, температуру, штраф за присутствие и сообщения.
        3. Отправляет POST-запрос к API `gpt4.gravityengine.cc`.
        4. Перебирает ответ и извлекает контент из JSON-ответа.
        5. Возвращает извлеченный контент с использованием `yield`, что позволяет передавать данные потоково.

    Внутренние функции:
        В данной функции нет внутренних функций.

    Примеры:
        >>> model = 'gpt-3.5-turbo-16k'
        >>> messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
        >>> stream = True
        >>> result = _create_completion(model, messages, stream)
        >>> for chunk in result:
        ...     print(chunk)
        'Hello! As an AI...'

    """
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({0})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
```

- **Назначение**: Формирует строку с информацией о поддерживаемых параметрах функции `_create_completion`.

- **Описание**: Строка `params` содержит информацию о поддерживаемых параметрах функции `_create_completion`. Она формируется путем извлечения имен параметров и их типов из аннотаций типов функции `_create_completion`.