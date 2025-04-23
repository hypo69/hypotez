# Модуль `Bing.py`

## Обзор

Модуль `Bing.py` предоставляет реализацию взаимодействия с Bing AI для генерации текста. Он использует веб-сокеты для потоковой передачи ответов и включает механизмы для создания и управления диалогом с Bing AI.

## Подробнее

Модуль содержит функции для установки соединения с Bing AI, отправки запросов и получения потоковых ответов. Он также включает классы для определения наборов опций и настроек по умолчанию, что позволяет гибко настраивать поведение Bing AI.

## Классы

### `optionsSets`

**Описание**: Класс предназначен для определения наборов опций, используемых при взаимодействии с Bing AI.

**Атрибуты**:
- `optionSet` (dict): Словарь, определяющий структуру набора опций.
- `jailbreak` (dict): Словарь, содержащий набор опций для "jailbreak"-режима.

### `Defaults`

**Описание**: Класс, содержащий значения по умолчанию для различных параметров, используемых при взаимодействии с Bing AI.

**Атрибуты**:
- `delimiter` (str): Разделитель, используемый для разделения сообщений в потоке данных.
- `ip_address` (str): IP-адрес, используемый для обхода географических ограничений.
- `allowedMessageTypes` (list): Список допустимых типов сообщений.
- `sliceIds` (list): Список идентификаторов срезов.
- `location` (dict): Словарь, содержащий информацию о местоположении.

## Функции

### `_format`

```python
def _format(msg: dict) -> str:
    """Функция преобразует словарь в JSON-строку и добавляет разделитель.

    Args:
        msg (dict): Словарь для преобразования.

    Returns:
        str: JSON-строка с добавленным разделителем.

    Как работает функция:
    - Функция принимает словарь `msg`.
    - Преобразует словарь в JSON-строку с помощью `json.dumps`, отключая экранирование ASCII символов.
    - Добавляет к JSON-строке разделитель `Defaults.delimiter`.

    Примеры:
        >>> Defaults.delimiter = '\\x1e'
        >>> _format({'key': 'value'})
        '{"key": "value"}\\x1e'
    """
```

### `create_conversation`

```python
async def create_conversation():
    """Функция создает новый разговор с Bing AI.

    Returns:
        tuple: Кортеж, содержащий conversationId, clientId и conversationSignature.

    Raises:
        Exception: Если не удается создать разговор после нескольких попыток.

    Как работает функция:
    - Функция пытается создать разговор с Bing AI, отправляя GET-запрос к `https://www.bing.com/turing/conversation/create`.
    - Запрос отправляется несколько раз (до 5), чтобы обработать возможные сбои.
    - Если после нескольких попыток не удается получить conversationId, clientId и conversationSignature, выбрасывается исключение.

    Примеры:
        # Пример вызова функции (в асинхронном контексте)
        >>> import asyncio
        >>> async def main():
        ...     conversation_data = await create_conversation()
        ...     print(conversation_data)
        >>> asyncio.run(main())
        ('conversationId', 'clientId', 'conversationSignature')
    """
```

### `stream_generate`

```python
async def stream_generate(prompt: str, mode: optionsSets.optionSet = optionsSets.jailbreak, context: bool or str = False):
    """Функция генерирует текст с использованием Bing AI в потоковом режиме.

    Args:
        prompt (str): Запрос пользователя.
        mode (optionsSets.optionSet, optional): Набор опций для запроса. По умолчанию optionsSets.jailbreak.
        context (bool | str, optional): Контекст для запроса. По умолчанию False.

    Yields:
        str: Часть ответа от Bing AI.

    Raises:
        Exception: Если возникает ошибка при получении ответа от Bing AI.

    Как работает функция:
    - Функция устанавливает соединение с Bing AI через веб-сокет.
    - Отправляет запрос пользователя и получает ответ в потоковом режиме.
    - Возвращает части ответа по мере их поступления.

    Примеры:
        # Пример вызова функции (в асинхронном контексте)
        >>> import asyncio
        >>> async def main():
        ...     async for chunk in stream_generate("Hello, Bing!"):
        ...         print(chunk)
        >>> asyncio.run(main())
        Привет! Чем я могу помочь вам сегодня?
    """
```

### `run`

```python
def run(generator):
    """Функция запускает асинхронный генератор и возвращает значения.

    Args:
        generator: Асинхронный генератор.

    Yields:
        Any: Значения, возвращаемые генератором.

    Как работает функция:
    - Функция принимает асинхронный генератор.
    - Запускает генератор в цикле, пока не будет достигнут конец генератора.
    - Возвращает значения, генерируемые генератором.

    Примеры:
        >>> def async_generator():
        ...     yield asyncio.sleep(1)
        ...     yield 1
        >>> for value in run(async_generator()):
        ...     print(value)
        1
    """
```

### `convert`

```python
def convert(messages):
    """Функция преобразует список сообщений в контекст.

    Args:
        messages (list): Список сообщений.

    Returns:
        str: Контекст для запроса.

    Как работает функция:
    - Функция принимает список сообщений.
    - Преобразует список сообщений в строку контекста, добавляя роль и содержимое каждого сообщения.

    Примеры:
        >>> messages = [{'role': 'user', 'content': 'Hello'}, {'role': 'bot', 'content': 'Hi'}]
        >>> convert(messages)
        '[user](#message)\\nHello\\n\\n[bot](#message)\\nHi\\n\\n'
    """
```

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """Функция создает запрос на завершение текста с использованием Bing AI.

    Args:
        model (str): Имя модели.
        messages (list): Список сообщений.
        stream (bool): Флаг, указывающий, следует ли использовать потоковый режим.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Часть ответа от Bing AI.

    Как работает функция:
    - Функция принимает модель, список сообщений и флаг потокового режима.
    - Создает запрос на завершение текста с использованием Bing AI.
    - Возвращает ответ в потоковом режиме.

    Примеры:
        # Пример вызова функции
        >>> messages = [{'role': 'user', 'content': 'Hello'}]
        >>> for token in _create_completion('gpt-4', messages, True):
        ...     print(token)
        Привет!
    """
```

## Параметры

- `params` (str): Строка, содержащая информацию о поддерживаемых параметрах функции `_create_completion`.