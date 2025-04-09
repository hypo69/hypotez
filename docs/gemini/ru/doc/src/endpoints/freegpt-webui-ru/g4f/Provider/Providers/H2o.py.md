# Модуль для работы с провайдером H2o
## Обзор

Модуль предоставляет класс для взаимодействия с провайдером H2o, позволяя генерировать текст на основе различных моделей, таких как `falcon-40b`, `falcon-7b` и `llama-13b`.
Модуль использует requests для отправки запросов к API H2o и поддерживает потоковую передачу данных.

## Подробнее

Модуль содержит функции для создания запросов к API H2o и обработки ответов. Он поддерживает потоковую передачу данных, что позволяет получать результаты генерации текста по частям.
Модуль также определяет параметры, поддерживаемые провайдером.
Расположение файла в проекте указывает на то, что он является частью системы, предоставляющей доступ к различным провайдерам для генерации текста,
используемым в проекте `hypotez`.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция создает запрос к API H2o для генерации текста на основе предоставленных сообщений.
    Args:
        model (str): Имя используемой модели.
        messages (list): Список сообщений для генерации текста.
            Каждое сообщение должно быть словарем с ключами `role` и `content`.
        stream (bool): Определяет, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные параметры, такие как `temperature`, `truncate`, `max_new_tokens`, `do_sample`, `repetition_penalty`, `return_full_text`, `id`, `response_id`.

    Returns:
        Generator[str, None, None]: Генератор токенов, если `stream` установлен в `True`.

    Raises:
        Exception: Если возникает ошибка при отправке запроса к API H2o.

    """
```

**Назначение**: Создание запроса к API H2o для генерации текста на основе предоставленных сообщений.

**Параметры**:

-   `model` (str): Имя используемой модели (`falcon-40b`, `falcon-7b`, `llama-13b`).
-   `messages` (list): Список сообщений для генерации текста. Каждое сообщение должно быть словарем с ключами `role` и `content`.
-   `stream` (bool): Определяет, использовать ли потоковую передачу данных.
-   `**kwargs`: Дополнительные параметры, такие как `temperature`, `truncate`, `max_new_tokens`, `do_sample`, `repetition_penalty`, `return_full_text`, `id`, `response_id`.

**Возвращает**:

-   `Generator[str, None, None]`: Генератор токенов, если `stream` установлен в `True`.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при отправке запроса к API H2o.

**Как работает функция**:

1.  Функция формирует строку `conversation` из списка сообщений, добавляя к каждому сообщению роль (`user` или `assistant`) и содержимое.
2.  Создается сессия `client` с помощью `requests.Session()`.
3.  Устанавливаются заголовки для сессии, включая `authority`, `origin`, `referer` и `user-agent`.
4.  Выполняется GET запрос к `https://gpt-gm.h2o.ai/`.
5.  Выполняется POST запрос к `https://gpt-gm.h2o.ai/settings` для установки параметров, таких как `ethicsModalAccepted` и `activeModel`.
6.  Устанавливаются дополнительные заголовки для последующих запросов.
7.  Выполняется POST запрос к `https://gpt-gm.h2o.ai/conversation` для получения `conversationId`.
8.  Выполняется POST запрос к `https://gpt-gm.h2o.ai/conversation/{conversationId}` с параметром `stream=True` для получения сгенерированного текста в потоковом режиме.
9.  Функция итерируется по строкам ответа, извлекая токены и возвращая их с помощью `yield`.
10. Если токен равен `<|endoftext|>`, генерация завершается.

```
A: Формирование conversation
|
B: Создание сессии client
|
C: Установка заголовков
|
D: GET запрос к https://gpt-gm.h2o.ai/
|
E: POST запрос к https://gpt-gm.h2o.ai/settings
|
F: POST запрос к https://gpt-gm.h2o.ai/conversation
|
G: POST запрос к https://gpt-gm.h2o.ai/conversation/{conversationId} (stream=True)
|
H: Итерация по строкам ответа
|
I: Извлечение токенов и возврат с помощью yield
|
J: Завершение генерации, если токен == '<|endoftext|>'
```

**Примеры**:

```python
# Пример вызова функции _create_completion с минимальными параметрами
messages = [{'role': 'user', 'content': 'Hello'}]
generator = _create_completion(model='falcon-7b', messages=messages, stream=True)
for token in generator:
    print(token, end='')

# Пример вызова функции _create_completion с дополнительными параметрами
messages = [{'role': 'user', 'content': 'Tell me a story'}]
generator = _create_completion(
    model='falcon-40b',
    messages=messages,
    stream=True,
    temperature=0.7,
    max_new_tokens=500
)
for token in generator:
    print(token, end='')
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

**Назначение**: Формирование строки с информацией о поддерживаемых параметрах функции `_create_completion`.

**Как работает**:

1.  Извлекает имя файла текущего модуля (без расширения `.py`) с помощью `os.path.basename(__file__)[:-3]`.
2.  Получает аннотации типов параметров функции `_create_completion` с помощью `get_type_hints(_create_completion)`.
3.  Формирует строку, содержащую имена параметров и их типы, объединяя их через запятую.
4.  Создает строку `params`, содержащую информацию о поддерживаемых параметрах, и присваивает ее переменной `params`.

**Примеры**:

```python
print(params)
# g4f.Providers.H2o supports: (model: str, messages: list, stream: bool, kwargs: dict)