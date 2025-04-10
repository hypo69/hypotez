# Модуль `helper`

## Обзор

Модуль `helper` содержит набор вспомогательных функций, используемых в проекте `hypotez` для обработки и форматирования текстовых данных, генерации случайных строк, работы с cookies, а также для подготовки промптов для моделей GPT4Free.

## Подробнее

Этот модуль предоставляет функции для преобразования различных типов данных в строки, форматирования сообщений для моделей, получения системных промптов, извлечения последних сообщений пользователей, форматирования промптов изображений, усечения промптов до максимальной длины, генерации случайных строк и шестнадцатеричных чисел, фильтрации `None` значений из словаря, а также объединения чанков из асинхронных и синхронных итераторов в строки.

## Функции

### `to_string`

```python
def to_string(value) -> str:
    """ Функция преобразует входное значение в строку.

    Args:
        value: Значение для преобразования.

    Returns:
        str: Строковое представление входного значения.

    Как работает функция:
    1. Проверяет, является ли входное значение строкой. Если да, возвращает его без изменений.
    2. Если значение является словарем, проверяет наличие ключа "name". Если он есть, возвращает пустую строку.
    3. Если в словаре есть ключ "bucket_id", пытается прочитать содержимое bucket'а и объединить его в строку.
    4. Если значение - словарь и его тип "text", возвращает текст из словаря.
    5. Если значение - список, рекурсивно вызывает `to_string` для каждого элемента и объединяет результаты в строку.
    6. Если ни одно из условий не выполнено, преобразует значение в строку с помощью `str()`.

    ASCII flowchart:
    Value -> Is String? -> Return Value
      |
      No
      |
      Value -> Is Dict? -> Has "name"? -> Return ""
        |           |
        No          No
        |           |
        Has "bucket_id"? -> Read Bucket -> Join -> Return
          |
          No
          |
          Type == "text"? -> Return Text
            |
            No
            |
            Return str(Value)

    Примеры:
    >>> to_string("example")
    'example'
    >>> to_string({"bucket_id": "test_bucket"})
    ''  # Возвращает содержимое bucket'а, если он существует
    >>> to_string({"type": "text", "text": "some text"})
    'some text'
    """
    ...
```

### `format_prompt`

```python
def format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False, include_system: bool = True) -> str:
    """ Форматирует последовательность сообщений в одну строку, с возможностью добавления специальных токенов.

    Args:
        messages (Messages): Список словарей сообщений, каждый из которых содержит 'role' и 'content'.
        add_special_tokens (bool): Флаг для добавления специальных токенов форматирования. По умолчанию `False`.
        do_continue (bool): Флаг для продолжения форматирования. По умолчанию `False`.
        include_system (bool): Флаг для включения системных сообщений. По умолчанию `True`.

    Returns:
        str: Отформатированная строка, содержащая все сообщения.

    Как работает функция:
    1. Если `add_special_tokens` равно `False` и количество сообщений меньше или равно 1, возвращает содержимое первого сообщения, преобразованное в строку.
    2. Фильтрует сообщения, исключая системные, если `include_system` равно `False`.
    3. Форматирует каждое сообщение в виде '{role.capitalize()}: {content}'.
    4. Объединяет отформатированные сообщения в одну строку, разделяя их символом новой строки.
    5. Если `do_continue` равно `True`, возвращает отформатированную строку.
    6. Иначе добавляет "Assistant:" в конец строки и возвращает результат.

    ASCII flowchart:
    Messages -> add_special_tokens == False and len(messages) <= 1? -> to_string(messages[0]["content"])
      |
      No
      |
      Filter messages (exclude system if include_system == False) -> Format each message -> Join messages with newline -> do_continue == True? -> Return formatted
                                                                                                                            |
                                                                                                                            No
                                                                                                                            |
                                                                                                                            Append "Assistant:" -> Return

    Примеры:
    >>> messages = [{"role": "user", "content": "Hello"}]
    >>> format_prompt(messages)
    'User: Hello\\nAssistant:'
    >>> messages = [{"role": "system", "content": "You are helpful"}]
    >>> format_prompt(messages, include_system=False)
    '\\nAssistant:'
    """
    ...
```

### `get_system_prompt`

```python
def get_system_prompt(messages: Messages) -> str:
    """ Извлекает системные промпты из списка сообщений.

    Args:
        messages (Messages): Список словарей сообщений, каждый из которых содержит 'role' и 'content'.

    Returns:
        str: Строка, содержащая все системные промпты, объединенные символом новой строки.

    Как работает функция:
    1. Фильтрует сообщения, оставляя только те, у которых роль равна "system".
    2. Извлекает содержимое каждого системного сообщения.
    3. Объединяет содержимое всех системных сообщений в одну строку, разделяя их символом новой строки.

    ASCII flowchart:
    Messages -> Filter (role == "system") -> Extract content -> Join with newline -> Return

    Примеры:
    >>> messages = [{"role": "system", "content": "You are helpful"}, {"role": "user", "content": "Hello"}]
    >>> get_system_prompt(messages)
    'You are helpful'
    """
    ...
```

### `get_last_user_message`

```python
def get_last_user_message(messages: Messages) -> str:
    """ Извлекает последнее сообщение пользователя из списка сообщений.

    Args:
        messages (Messages): Список словарей сообщений, каждый из которых содержит 'role' и 'content'.

    Returns:
        str: Строка, содержащая последнее сообщение пользователя.

    Как работает функция:
    1. Создает копию списка сообщений.
    2. Итерируется по сообщениям в обратном порядке.
    3. Если роль сообщения равна "user", добавляет его содержимое в список сообщений пользователя.
    4. Если встречает сообщение с другой ролью, возвращает объединенные сообщения пользователя.
    5. Если все сообщения просмотрены, возвращает объединенные сообщения пользователя.

    ASCII flowchart:
    Messages -> Copy -> Iterate in reverse -> Role == "user"? -> Append content to user_messages
                                                  |
                                                  No
                                                  |
                                                  Return "\\n".join(user_messages[::-1])
    Примеры:
    >>> messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}, {"role": "user", "content": "How are you?"}]
    >>> get_last_user_message(messages)
    'How are you?'
    """
    ...
```

### `format_image_prompt`

```python
def format_image_prompt(messages, prompt: str = None) -> str:
    """ Форматирует промпт для генерации изображений.

    Args:
        messages: Список сообщений.
        prompt (str, optional): Промпт. Если `None`, используется последнее сообщение пользователя. По умолчанию `None`.

    Returns:
        str: Отформатированный промпт.

    Как работает функция:
    1. Если `prompt` не задан, использует `get_last_user_message` для получения последнего сообщения пользователя.
    2. Возвращает `prompt` или последнее сообщение пользователя.

    ASCII flowchart:
    Prompt is None? -> get_last_user_message(messages)
      |
      No
      |
      Return prompt
    Примеры:
    >>> messages = [{"role": "user", "content": "Cat"}]
    >>> format_image_prompt(messages)
    'Cat'
    """
    ...
```

### `format_prompt_max_length`

```python
def format_prompt_max_length(messages: Messages, max_lenght: int) -> str:
    """ Форматирует промпт и обрезает его до максимальной длины.

    Args:
        messages (Messages): Список сообщений.
        max_lenght (int): Максимальная длина промпта.

    Returns:
        str: Отформатированный и обрезанный промпт.

    Как работает функция:
    1. Форматирует промпт с помощью `format_prompt`.
    2. Если длина промпта превышает `max_lenght`, пытается укоротить его, используя разные стратегии:
        - Если сообщений больше 6, оставляет только первые 3 и последние 3.
        - Если длина все еще превышает `max_lenght`, оставляет только системные сообщения и последнее сообщение пользователя.
        - Если длина все еще превышает `max_lenght`, оставляет только последнее сообщение пользователя.
    3. Логирует информацию об усечении промпта.

    ASCII flowchart:
    Format prompt -> Length > max_length? -> Length > 6? -> Use messages[:3] + messages[-3:]
                                          |                |
                                          No               No
                                          |                |
                                          Use system + last message
                                          |
                                          Length > max_length? -> Use last message
                                          |
                                          No
                                          |
                                          Return prompt

    Примеры:
    >>> messages = [{"role": "user", "content": "A" * 200}]
    >>> format_prompt_max_length(messages, 100)
    'A' * 200 # Будет усечено, если необходимо
    """
    ...
```

### `get_random_string`

```python
def get_random_string(length: int = 10) -> str:
    """ Генерирует случайную строку указанной длины, содержащую строчные буквы и цифры.

    Args:
        length (int, optional): Длина случайной строки. По умолчанию 10.

    Returns:
        str: Случайная строка указанной длины.

    Как работает функция:
    1. Использует `random.choice` для выбора случайных символов из набора строчных букв и цифр.
    2. Повторяет выбор символов `length` раз.
    3. Объединяет выбранные символы в строку.

    ASCII flowchart:
    For i in range(length): -> random.choice(lowercase + digits) -> Append to result
    Return result
    Примеры:
    >>> get_random_string(5)
    'a1b2c'  # Пример случайной строки
    """
    ...
```

### `get_random_hex`

```python
def get_random_hex(length: int = 32) -> str:
    """ Генерирует случайную шестнадцатеричную строку длиной n.

    Args:
        length (int, optional): Длина шестнадцатеричной строки. По умолчанию 32.

    Returns:
        str: Случайная шестнадцатеричная строка длиной n символов.

    Как работает функция:
    1. Использует `random.choice` для выбора случайных символов из набора шестнадцатеричных символов (a-f и 0-9).
    2. Повторяет выбор символов `length` раз.
    3. Объединяет выбранные символы в строку.

    ASCII flowchart:
    For i in range(length): -> random.choice("abcdef" + digits) -> Append to result
    Return result
    Примеры:
    >>> get_random_hex(8)
    'a1b2c3d4'  # Пример случайной шестнадцатеричной строки
    """
    ...
```

### `filter_none`

```python
def filter_none(**kwargs) -> dict:
    """ Фильтрует словарь, удаляя элементы со значением `None`.

    Args:
        **kwargs: Произвольный набор именованных аргументов.

    Returns:
        dict: Новый словарь, содержащий только элементы, значения которых не равны `None`.

    Как работает функция:
    1. Создает новый словарь.
    2. Итерируется по входному словарю.
    3. Если значение элемента не равно `None`, добавляет элемент в новый словарь.
    4. Возвращает новый словарь.

    ASCII flowchart:
    For key, value in kwargs.items(): -> value is not None? -> Add (key, value) to new dict
    Return new dict
    Примеры:
    >>> filter_none(a=1, b=None, c=2)
    {'a': 1, 'c': 2}
    """
    ...
```

### `async_concat_chunks`

```python
async def async_concat_chunks(chunks: AsyncIterator) -> str:
    """ Асинхронно объединяет чанки из асинхронного итератора в строку.

    Args:
        chunks (AsyncIterator): Асинхронный итератор, возвращающий чанки.

    Returns:
        str: Строка, содержащая все чанки, объединенные в одну строку.

    Как работает функция:
    1. Использует асинхронное включение списка для сбора всех чанков из асинхронного итератора.
    2. Вызывает `concat_chunks` для объединения собранных чанков в строку.

    ASCII flowchart:
    AsyncIterator -> [chunk async for chunk in chunks] -> concat_chunks -> Return

    Примеры:
    >>> async def generate_chunks():
    ...     yield "Hello"
    ...     yield "World"
    >>> async def main():
    ...     result = await async_concat_chunks(generate_chunks())
    ...     print(result)
    >>> # asyncio.run(main())  # Hello World
    """
    ...
```

### `concat_chunks`

```python
def concat_chunks(chunks: Iterator) -> str:
    """ Объединяет чанки из итератора в строку.

    Args:
        chunks (Iterator): Итератор, возвращающий чанки.

    Returns:
        str: Строка, содержащая все чанки, объединенные в одну строку.

    Как работает функция:
    1. Использует включение списка для преобразования каждого чанка в строку.
    2. Фильтрует чанки, исключая пустые чанки и экземпляры исключений.
    3. Объединяет отфильтрованные чанки в одну строку.

    ASCII flowchart:
    Iterator -> [str(chunk) for chunk in chunks if chunk and not isinstance(chunk, Exception)] -> "".join() -> Return

    Примеры:
    >>> concat_chunks(["Hello", "World", None, Exception()])
    'HelloWorld'
    """
    ...
```

### `format_cookies`

```python
def format_cookies(cookies: Cookies) -> str:
    """ Форматирует словарь cookies в строку.

    Args:
        cookies (Cookies): Словарь cookies.

    Returns:
        str: Строка, содержащая cookies в формате "key=value; key=value; ...".

    Как работает функция:
    1. Итерируется по словарю cookies.
    2. Для каждой пары ключ-значение формирует строку "key=value".
    3. Объединяет полученные строки в одну строку, разделяя их "; ".

    ASCII flowchart:
    For k, v in cookies.items(): -> Format "k=v" -> Join with "; " -> Return

    Примеры:
    >>> cookies = {"name": "value", "name2": "value2"}
    >>> format_cookies(cookies)
    'name=value; name2=value2'
    """
    ...