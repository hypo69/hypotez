# Модуль `Bing.py`

## Обзор

Модуль `Bing.py` предоставляет интерфейс для взаимодействия с чат-ботом Bing AI. Он позволяет генерировать ответы на основе предоставленных подсказок, используя асинхронный стриминг для получения ответа в реальном времени. Модуль поддерживает различные опции настройки поведения чат-бота и использует `aiohttp` для асинхронных запросов.

## Детали

Модуль определяет несколько классов и функций, необходимые для установления соединения с Bing AI, отправки запросов и обработки ответов. Он включает в себя:

- Классы `optionsSets` и `Defaults`, определяющие параметры запросов и настройки по умолчанию.
- Функцию `create_conversation` для создания нового диалога с Bing AI.
- Функцию `stream_generate` для отправки запроса и получения потока ответов.
- Функцию `_create_completion` для подготовки запроса на основе списка сообщений.

## Содержание

- [Классы](#classes)
  - [optionsSets](#optionssets)
  - [Defaults](#defaults)
- [Функции](#functions)
  - [\_format](#_format)
  - [create\_conversation](#create_conversation)
  - [stream\_generate](#stream_generate)
  - [run](#run)
  - [convert](#convert)
  - [\_create_completion](#_create_completion)

## Классы

### `optionsSets`

Класс `optionsSets` предназначен для хранения наборов опций, используемых при взаимодействии с Bing AI.

**Атрибуты:**

- `optionSet` (dict): Словарь, определяющий структуру набора опций.
  - `tone` (str): Строковое значение для тональности.
  - `optionsSets` (list): Список наборов опций.

- `jailbreak` (dict): Словарь с предопределенными наборами опций для "взлома" (jailbreak) Bing AI.

### `Defaults`

Класс `Defaults` содержит значения по умолчанию для различных параметров, используемых при взаимодействии с Bing AI.

**Атрибуты:**

- `delimiter` (str): Разделитель, используемый для разделения сообщений в потоке данных (`\x1e`).
- `ip_address` (str): IP-адрес, используемый для подмены в запросах (генерируется случайным образом).
- `allowedMessageTypes` (list): Список разрешенных типов сообщений.
- `sliceIds` (list): Список идентификаторов срезов.
- `location` (dict): Информация о местоположении пользователя (en-US, California, Los Angeles).

## Функции

### `_format`

```python
def _format(msg: dict) -> str:
    """ Форматирует сообщение в JSON-формат с добавлением разделителя.

    Args:
        msg (dict): Словарь с сообщением для форматирования.

    Returns:
        str: JSON-представление сообщения с добавленным разделителем.

    Как работает функция:
    - Преобразует словарь `msg` в JSON-строку, убедившись, что не ASCII символы будут корректно обработаны.
    - Добавляет к полученной строке разделитель `Defaults.delimiter`.

    Пример:
    ```python
    >>> _format({'ключ': 'значение'})
    '{"ключ": "значение"}\\x1e'
    ```
    """
    ...
```

### `create_conversation`

```python
async def create_conversation():
    """ Создает новый разговор с Bing AI.

    Returns:
        tuple: Кортеж, содержащий `conversationId`, `clientId` и `conversationSignature`.

    Raises:
        Exception: Если не удается создать разговор после нескольких попыток.

    Как работает функция:
    - Выполняет несколько попыток (`range(5)`) запроса к `https://www.bing.com/turing/conversation/create` для создания нового разговора.
    - Извлекает из JSON-ответа `conversationId`, `clientId` и `conversationSignature`.
    - Если после нескольких попыток не удается получить все необходимые идентификаторы, выбрасывает исключение.

    Пример:
    ```python
    conversation_id, client_id, conversation_signature = await create_conversation()
    print(f"ID разговора: {conversation_id}")
    ```
    """
    ...
```

### `stream_generate`

```python
async def stream_generate(prompt: str, mode: optionsSets.optionSet = optionsSets.jailbreak, context: bool or str = False):
    """ Генерирует ответ от Bing AI в режиме стриминга.

    Args:
        prompt (str): Текст запроса.
        mode (optionsSets.optionSet, optional): Набор опций для запроса. По умолчанию `optionsSets.jailbreak`.
        context (bool | str, optional): Контекст для запроса. По умолчанию `False`.

    Yields:
        str: Части ответа от Bing AI.

    Raises:
        Exception: Если возникает ошибка при обработке ответа от Bing AI.

    Как работает функция:
    - Устанавливает асинхронное соединение с сервером Bing AI через WebSocket.
    - Отправляет запрос с заданным текстом (`prompt`) и параметрами (`mode`, `context`).
    - Получает ответ частями и возвращает их через `yield`.
    - Обрабатывает различные типы сообщений, включая текстовые ответы и сообщения об ошибках.
    - Закрывает соединение WebSocket после получения финального ответа.

    Пример:
    ```python
    async for part in stream_generate("Привет, Bing!"):
        print(part)
    ```
    """
    ...
```

### `run`

```python
def run(generator):
    """ Запускает асинхронный генератор и возвращает значения.

    Args:
        generator: Асинхронный генератор.

    Yields:
        Any: Значения, возвращаемые генератором.

    Как работает функция:
    - Получает event loop.
    - Выполняет асинхронный генератор до тех пор, пока не будут получены все значения.
    - Перехватывает исключение `StopAsyncIteration`, когда генератор завершает работу.

    Пример:
    ```python
    def my_generator():
        yield 1
        yield 2
        yield 3

    for value in run(my_generator()):
        print(value)
    ```
    """
    ...
```

### `convert`

```python
def convert(messages):
    """ Преобразует список сообщений в контекст для запроса.

    Args:
        messages (list): Список сообщений.

    Returns:
        str: Контекст для запроса в виде строки.

    Как работает функция:
    - Форматирует каждое сообщение из списка в строку определенного формата, используя роль и содержимое сообщения.
    - Объединяет все отформатированные сообщения в одну строку, разделяя их символами новой строки.

    Пример:
    ```python
    messages = [
        {'role': 'user', 'content': 'Привет!'},
        {'role': 'bot', 'content': 'Здравствуйте!'}
    ]
    context = convert(messages)
    print(context)
    ```
    """
    ...
```

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Создает запрос на основе списка сообщений.

    Args:
        model (str): Имя модели.
        messages (list): Список сообщений.
        stream (bool): Флаг стриминга.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Части ответа от Bing AI.

    Как работает функция:
    - Извлекает текст запроса из последнего сообщения в списке.
    - Преобразует предыдущие сообщения в контекст.
    - Вызывает функцию `stream_generate` для отправки запроса и получения потока ответов.

    Пример:
    ```python
    messages = [
        {'role': 'user', 'content': 'Привет!'}
    ]
    for token in _create_completion(model="gpt-4", messages=messages, stream=True):
        print(token)
    ```
    """
    ...
```