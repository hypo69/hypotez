# Модуль `Yqcloud.py`

## Обзор

Модуль предоставляет реализацию для взаимодействия с сервисом Yqcloud для генерации текста. Он использует API `aichatos.cloud` для отправки запросов и получения ответов. Модуль поддерживает потоковую передачу данных и не требует аутентификации.

## Подробнее

Модуль содержит функции для создания запросов к API Yqcloud и обработки ответов. Он предназначен для использования в качестве одного из провайдеров в системе `g4f` для генерации текста.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к API Yqcloud и возвращает ответ.

    Args:
        model (str): Модель для генерации текста (не используется в данной реализации).
        messages (list): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные аргументы (не используются в данной реализации).

    Returns:
        Generator[str, None, None]: Генератор токенов ответа, декодированных в UTF-8.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса.

    Пример:
        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Hello, world!"}]
        >>> stream = True
        >>> generator = _create_completion(model, messages, stream)
        >>> for token in generator:
        ...     print(token, end="")
        # Вывод: сгенерированный текст от Yqcloud
    """
```

**Назначение**: Функция `_create_completion` отправляет запрос к API `aichatos.cloud` для генерации текста на основе предоставленных сообщений и возвращает ответ в виде генератора токенов.

**Параметры**:
- `model` (str): Указывает модель для генерации текста. В данной реализации параметр не используется, но должен быть указан при вызове функции.
- `messages` (list): Список сообщений, отправляемых в API. Каждое сообщение представляет собой словарь с ключами `role` (роль отправителя) и `content` (содержимое сообщения).
- `stream` (bool): Флаг, определяющий, использовать ли потоковую передачу данных. Если `True`, функция возвращает генератор токенов ответа.
- `**kwargs`: Дополнительные именованные аргументы, которые не используются в данной реализации.

**Возвращает**:
- `Generator[str, None, None]`: Генератор, который выдает токены ответа, декодированные в UTF-8.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: Может быть вызвано при проблемах с сетевым запросом, таких как недоступность сервера или проблемы с подключением.

**Как работает функция**:

1.  **Подготовка заголовков**:
    - Определяются HTTP-заголовки, необходимые для запроса к API `aichatos.cloud`. Заголовки включают информацию о `authority`, `origin`, `referer`, и `user-agent`.

2.  **Формирование JSON-данных**:
    - Создается словарь `json_data`, содержащий данные для отправки в API.
    - `prompt`:  Объединяет префикс `'always respond in english |'` с содержимым последнего сообщения из списка `messages`. Это нужно для указания API отвечать на английском языке.
    - `userId`: Генерируется уникальный идентификатор пользователя на основе текущего времени.
    - `network`, `apikey`, `system`, `withoutContext`:  Устанавливаются значения для этих параметров.

3.  **Отправка запроса**:
    - Используется библиотека `requests` для отправки POST-запроса к API `https://api.aichatos.cloud/api/generateStream` с указанными заголовками и JSON-данными. Устанавливается `stream=True` для потоковой передачи данных.

4.  **Обработка потока ответов**:
    - Функция итерируется по содержимому ответа, получая данные небольшими частями (чанками) размером 2046 байт.

5.  **Декодирование и фильтрация токенов**:
    - Каждый чанк проверяется на наличие подстроки `b'always respond in english'`. Если подстрока не найдена, чанк декодируется из UTF-8 и возвращается как токен.

6.  **Генерация токенов**:
    - Функция является генератором, поэтому она возвращает токены по одному, используя `yield`.

**ASCII Flowchart**:

```
    Начало
    ↓
    [Подготовка HTTP-заголовков]
    ↓
    [Формирование JSON-данных (prompt, userId, network, apikey, system, withoutContext)]
    ↓
    [Отправка POST-запроса к API (stream=True)]
    ↓
    [Итерация по чанкам ответа]
    ↓
    [Проверка наличия 'always respond in english' в чанке]
    ├── Нет → [Декодирование чанка в UTF-8] → [yield токен]
    └── Да  → [Пропустить токен]
    ↓
    Конец (генератор завершается, когда нет больше чанков)
```

**Примеры**:

```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Translate to Russian: Hello, world!"}]
stream = True

generator = _create_completion(model=model, messages=messages, stream=stream)
for token in generator:
    print(token, end="")
```

```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Write a short poem about a cat."}]
stream = True

generator = _create_completion(model=model, messages=messages, stream=stream)
for token in generator:
    print(token, end="")
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({0})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
```

**Назначение**: Строка `params` формирует строку, содержащую информацию о поддержке параметров функцией `_create_completion`.

**Как работает**:

1.  **Получение имени файла**:
    - `os.path.basename(__file__)[:-3]` извлекает имя текущего файла (например, "Yqcloud.py") и удаляет последние три символа (".py"), чтобы получить имя модуля ("Yqcloud").

2.  **Формирование списка параметров**:
    - `_create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]` получает имена параметров функции `_create_completion`.
    - `get_type_hints(_create_completion)[name].__name__` получает строковое представление типа каждого параметра.
    - `[f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in ...]` создает список строк, где каждая строка имеет формат "имя_параметра: тип_параметра".

3.  **Объединение параметров в строку**:
    - `', '.join([...])` объединяет строки параметров через запятую и пробел.
    - `'({0})'.format(...)` форматирует строку, вставляя список параметров в скобки.

4.  **Формирование финальной строки**:
    - `f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + ...` объединяет имя провайдера и информацию о поддерживаемых параметрах.

**Пример**:

```python
print(params)
# Вывод: g4f.Providers.Yqcloud supports: (model: str, messages: list, stream: bool, kwargs: dict)