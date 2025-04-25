# Провайдер Yqcloud

## Обзор

Данный модуль предоставляет реализацию провайдера `Yqcloud` для `freegpt-webui-ru`. Провайдер использует API от `Yqcloud` для генерации текста.

## Подробности

В коде используются следующие функции и переменные:

- `url`: URL-адрес API `Yqcloud`.
- `model`: Список поддерживаемых моделей для генерации текста.
- `supports_stream`: Флаг, указывающий, поддерживается ли потоковая передача данных.
- `needs_auth`: Флаг, указывающий, требуется ли авторизация для использования API.
- `_create_completion`: Функция, которая генерирует текст с помощью API `Yqcloud`.

## Классы

### `Yqcloud`

**Описание**: Класс, представляющий провайдера `Yqcloud` для `freegpt-webui-ru`.

**Атрибуты**:

- `model`: Список поддерживаемых моделей.
- `supports_stream`: Флаг, указывающий, поддерживается ли потоковая передача данных.
- `needs_auth`: Флаг, указывающий, требуется ли авторизация для использования API.
- `_create_completion`: Функция, которая генерирует текст с помощью API `Yqcloud`.

**Методы**:

- `_create_completion`: Функция, которая генерирует текст с помощью API `Yqcloud`.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Функция, которая генерирует текст с помощью API `Yqcloud`.

    Args:
        model (str): Имя модели.
        messages (list): Список сообщений, которые будут использоваться для генерации текста.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные аргументы для функции.

    Returns:
        Generator[str, None, None]: Генератор строк, представляющих сгенерированный текст.

    Raises:
        Exception: Если возникает ошибка при вызове API `Yqcloud`.
    """
```

**Назначение**: Функция отправляет запрос к API `Yqcloud` для генерации текста.

**Параметры**:

- `model` (str): Имя модели, которая будет использоваться для генерации текста.
- `messages` (list): Список сообщений, которые будут использоваться для генерации текста.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу данных.

**Возвращает**:

- `Generator[str, None, None]`: Генератор строк, представляющих сгенерированный текст.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при вызове API `Yqcloud`.

**Как работает функция**:

- Функция создает запрос к API `Yqcloud`, используя `requests.post`.
- В заголовке запроса указываются `authority`, `origin`, `referer` и `user-agent`.
- В теле запроса передаются следующие данные:
    - `prompt`: Последнее сообщение из списка `messages`.
    - `userId`: Идентификатор пользователя.
    - `network`: Флаг, указывающий, использовать ли сеть.
    - `apikey`: API-ключ.
    - `system`: Системный текст.
    - `withoutContext`: Флаг, указывающий, использовать ли контекст.
- После получения ответа от API `Yqcloud`, функция итерирует по частям ответа и возвращает сгенерированный текст в виде генератора.

**Примеры**:

```python
# Пример вызова функции _create_completion
messages = [
    {'role': 'user', 'content': 'Hello, world!'},
]
_create_completion(model='gpt-3.5-turbo', messages=messages, stream=True)
```

## Параметры класса

- `model`: Список поддерживаемых моделей для генерации текста.
- `supports_stream`: Флаг, указывающий, поддерживается ли потоковая передача данных.
- `needs_auth`: Флаг, указывающий, требуется ли авторизация для использования API.

## Примеры

```python
# Пример создания инстанса класса Yqcloud
from hypotez.src.endpoints.juliana.freegpt-webui-ru.g4f.Provider.Providers.Yqcloud import Yqcloud

yqcloud_provider = Yqcloud()

# Пример использования функции _create_completion
messages = [
    {'role': 'user', 'content': 'Hello, world!'},
]
for token in yqcloud_provider._create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token)
```