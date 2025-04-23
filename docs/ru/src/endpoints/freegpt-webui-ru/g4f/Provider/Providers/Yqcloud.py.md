# Модуль Yqcloud.py

## Обзор

Модуль `Yqcloud.py` предоставляет интерфейс для взаимодействия с облачным сервисом Yqcloud для генерации текста. Он использует API `api.aichatos.cloud` для отправки запросов и получения ответов в потоковом режиме. Модуль поддерживает модель `gpt-3.5-turbo` и требует установки библиотеки `requests`.

## Подробней

Модуль содержит функции для создания запросов к API Yqcloud и обработки потоковых ответов. Он предназначен для использования в проектах, требующих генерации текста на основе модели `gpt-3.5-turbo`.

## Параметры

- `url` (str): URL для взаимодействия с сервисом Yqcloud (`https://chat9.yqcloud.top/`).
- `model` (list): Список поддерживаемых моделей (в данном случае `gpt-3.5-turbo`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потокового режима (`True`).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (`False`).

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Функция создает запрос к API Yqcloud и возвращает генератор для потокового получения ответа.

    Args:
        model (str): Название модели для генерации текста.
        messages (list): Список сообщений, используемых в качестве контекста для генерации.
        stream (bool): Флаг, указывающий на необходимость потокового режима.
        **kwargs: Дополнительные параметры.

    Returns:
        generator: Генератор, возвращающий части ответа от API Yqcloud.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при отправке запроса к API.

    Внутренние функции:
        Нет

    
        1. Функция определяет заголовки запроса, включая `authority`, `origin`, `referer` и `user-agent`.
        2. Функция формирует JSON-данные для запроса, включая `prompt`, `userId`, `network`, `apikey`, `system` и `withoutContext`.
           `prompt` содержит последнее сообщение из списка `messages` с префиксом "always respond in english | ".
           `userId` формируется на основе текущего времени.
        3. Функция отправляет POST-запрос к API `https://api.aichatos.cloud/api/generateStream` с указанными заголовками и JSON-данными.
        4. Функция итерируется по содержимому ответа в потоковом режиме, используя `response.iter_content(chunk_size=2046)`.
        5. Для каждой части ответа (token) проверяется наличие подстроки `b'always respond in english'`.
           Если подстрока отсутствует, часть ответа декодируется в UTF-8 и возвращается через `yield`.

    Примеры:
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'content': 'Hello, how are you?'}]
        >>> stream = True
        >>> generator = _create_completion(model, messages, stream)
        >>> for token in generator:
        ...     print(token)
    """
    ...
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({0})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
```

Описание:
Строка `params` формируется для отображения информации о поддержке параметров функцией `_create_completion`.

Как работает строка кода:
1. `os.path.basename(__file__)[:-3]` - извлекает имя текущего файла (например, "Yqcloud.py") и удаляет расширение ".py".
2. `g4f.Providers.{os.path.basename(__file__)[:-3]} supports:` - формирует начальную часть строки с указанием провайдера.
3. `_create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]` - получает список имен параметров функции `_create_completion`.
4. `get_type_hints(_create_completion)[name].__name__` - для каждого параметра извлекает его тип и преобразует в строковое представление.
5. `', '.join([...])` - объединяет имена параметров и их типы в строку, разделенную запятыми.
6. `'({0})'.format(...)` - форматирует строку, вставляя информацию о параметрах в скобки.

Пример:
```python
print(params)
# g4f.Providers.Yqcloud supports: (model: str, messages: list, stream: bool, kwargs: Dict)
```