# Модуль H2o.py для работы с провайдером H2O AI

## Обзор

Модуль предоставляет функциональность для взаимодействия с моделями H2O AI, такими как falcon-40b, falcon-7b и llama-13b, через API gpt-gm.h2o.ai. Модуль поддерживает стриминг ответов и не требует аутентификации.

## Подробнее

Этот модуль предназначен для интеграции с другими компонентами `hypotez`, использующими большие языковые модели. Он обеспечивает возможность отправки запросов к моделям H2O AI и получения ответов в режиме реального времени.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к API H2O AI для получения ответа от языковой модели.

    Args:
        model (str): Идентификатор модели, которую необходимо использовать (например, 'falcon-40b').
        messages (list): Список сообщений в формате [{"role": "user" или "assistant", "content": "текст сообщения"}].
        stream (bool): Определяет, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные параметры, такие как temperature, truncate, max_new_tokens, do_sample, repetition_penalty, return_full_text, id, response_id.

    Returns:
        Generator[str, None, None]: Генератор токенов ответа, если `stream=True`.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса.

    Example:
        >>> model_name = 'falcon-7b'
        >>> messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
        >>> stream = True
        >>> for token in _create_completion(model_name, messages, stream):
        ...     print(token, end='')
        I am doing well, thank you for asking.
    """
```

**Назначение**: Функция `_create_completion` отправляет запрос к API H2O AI, чтобы получить ответ от выбранной языковой модели на основе предоставленных сообщений и параметров.

**Параметры**:
- `model` (str): Идентификатор модели, например, 'falcon-40b'.
- `messages` (list): Список сообщений для модели. Каждое сообщение содержит роль (`user` или `assistant`) и контент.
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
- `**kwargs`: Дополнительные параметры, такие как `temperature` (температура модели), `truncate` (максимальная длина входного текста), `max_new_tokens` (максимальное количество новых токенов в ответе), `do_sample` (использовать ли sampling), `repetition_penalty` (штраф за повторения), `return_full_text` (возвращать ли полный текст), `id` (идентификатор запроса) и `response_id` (идентификатор ответа).

**Возвращает**:
- `Generator[str, None, None]`: Генератор токенов ответа, если включен режим потоковой передачи (`stream=True`).

**Как работает функция**:

1.  Формирует строку `conversation`, объединяя все сообщения из списка `messages`.
2.  Создает HTTP-клиент `client` на основе `requests.Session()` и устанавливает необходимые заголовки.
3.  Выполняет GET-запрос к `https://gpt-gm.h2o.ai/`, чтобы установить cookie.
4.  Выполняет POST-запрос к `https://gpt-gm.h2o.ai/settings` для установки настроек.
5.  Выполняет POST-запрос к `https://gpt-gm.h2o.ai/conversation` для получения `conversationId`.
6.  Выполняет POST-запрос к `https://gpt-gm.h2o.ai/conversation/{conversationId}` с параметром `stream=True` для получения ответа в режиме потока.
7.  Итерируется по строкам ответа, извлекая токены и передавая их через `yield`.

**Примеры**:

```python
model_name = 'falcon-7b'
messages = [{'role': 'user', 'content': 'Напиши небольшое стихотворение о Москве.'}]
stream = True

for token in _create_completion(model_name, messages, stream, temperature=0.5, max_new_tokens=50):
    print(token, end='')
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

**Назначение**: Строка `params` формирует сообщение о поддерживаемых параметрах функции `_create_completion`.

**Как работает**:
1.  Получает имя текущего файла без расширения `.py`.
2.  Использует `get_type_hints` для получения аннотаций типов параметров функции `_create_completion`.
3.  Формирует строку, перечисляющую имена параметров и их типы.

**Пример**:

```python
print(params)
# g4f.Providers.H2o supports: (model: str, messages: list, stream: bool, kwargs: dict)