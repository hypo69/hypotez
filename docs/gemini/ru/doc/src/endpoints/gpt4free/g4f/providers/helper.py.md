# Модуль helper

## Обзор

Модуль `helper` содержит набор вспомогательных функций, используемых в других модулях проекта `hypotez`. Он включает функции для форматирования строк, работы с сообщениями, генерации случайных строк и обработки cookie.

## Подробней

Этот модуль предоставляет функции для преобразования различных типов данных в строки, форматирования сообщений для AI-моделей, получения системных подсказок и последних сообщений пользователей, а также для генерации случайных строк. Он также содержит функции для обработки cookie и объединения чанков данных.
Все функции модуля реализованы на Python.

## Функции

### `to_string`

```python
def to_string(value) -> str:
    """
    Преобразует значение в строку.

    Args:
        value: Значение для преобразования. Может быть строкой, словарем или списком.

    Returns:
        str: Строковое представление значения.

    Как работает функция:
    - Если значение является строкой, функция возвращает его.
    - Если значение является словарем:
        - Если словарь содержит ключ "name", функция возвращает пустую строку.
        - Если словарь содержит ключ "bucket_id", функция считывает содержимое bucket и возвращает его как строку.
        - Если словарь имеет тип "text", функция возвращает значение ключа "text".
        - В противном случае возвращается пустая строка.
    - Если значение является списком, функция рекурсивно преобразует каждый элемент списка в строку и объединяет их.
    - Если значение не является строкой, словарем или списком, функция преобразует его в строку с помощью str(value).

    Примеры:
    >>> to_string("hello")
    'hello'
    >>> to_string({"bucket_id": "123"})  #  Чтение bucket с id "123"
    'содержимое bucket'
    >>> to_string([{"type": "text", "text": "world"}])
    'world'
    """
    ...
```

### `format_prompt`

```python
def format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False, include_system: bool = True) -> str:
    """
    Форматирует список сообщений в строку, опционально добавляя специальные токены.

    Args:
        messages (Messages): Список словарей сообщений, каждый из которых содержит 'role' и 'content'.
        add_special_tokens (bool): Флаг, указывающий, следует ли добавлять специальные токены форматирования. По умолчанию `False`.
        do_continue (bool): Флаг для продолжения форматирования. По умолчанию `False`.
        include_system (bool): Флаг, указывающий, следует ли включать системные сообщения. По умолчанию `True`.

    Returns:
        str: Отформатированная строка, содержащая все сообщения.

    Как работает функция:
    - Если add_special_tokens имеет значение False и длина списка сообщений меньше или равна 1, функция возвращает содержимое первого сообщения, преобразованное в строку.
    - Фильтрует сообщения, чтобы исключить системные сообщения, если include_system имеет значение False.
    - Форматирует каждое сообщение в виде "Role: Content".
    - Объединяет все отформатированные сообщения в одну строку, разделяя их символом новой строки.
    - Если do_continue имеет значение True, функция возвращает отформатированную строку.
    - В противном случае функция добавляет "Assistant:" в конец отформатированной строки.

    Примеры:
    >>> messages = [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "world"}]
    >>> format_prompt(messages)
    'User: hello\\nAssistant: world\\nAssistant:'
    >>> format_prompt(messages, add_special_tokens=True)
    'User: hello\\nAssistant: world\\nAssistant:'
    """
    ...
```

### `get_system_prompt`

```python
def get_system_prompt(messages: Messages) -> str:
    """
    Извлекает системные сообщения из списка сообщений и объединяет их в одну строку.

    Args:
        messages (Messages): Список словарей сообщений, каждый из которых содержит 'role' и 'content'.

    Returns:
        str: Строка, содержащая все системные сообщения, разделенные символом новой строки.

    Как работает функция:
    - Фильтрует список сообщений, чтобы получить только сообщения с ролью "system".
    - Извлекает содержимое каждого системного сообщения.
    - Объединяет содержимое всех системных сообщений в одну строку, разделяя их символом новой строки.

    Примеры:
    >>> messages = [{"role": "system", "content": "you are a helpful assistant"}, {"role": "user", "content": "hello"}]
    >>> get_system_prompt(messages)
    'you are a helpful assistant'
    >>> messages = [{"role": "user", "content": "hello"}]
    >>> get_system_prompt(messages)
    ''
    """
    ...
```

### `get_last_user_message`

```python
def get_last_user_message(messages: Messages) -> str:
    """
    Извлекает последние сообщения пользователя из списка сообщений и объединяет их в одну строку.

    Args:
        messages (Messages): Список словарей сообщений, каждый из которых содержит 'role' и 'content'.

    Returns:
        str: Строка, содержащая последние сообщения пользователя, разделенные символом новой строки.

    Как работает функция:
    - Копирует список сообщений, чтобы не изменять исходный список.
    - Итерируется по списку сообщений в обратном порядке.
    - Если сообщение имеет роль "user", функция добавляет его содержимое в список user_messages.
    - Если сообщение имеет другую роль, функция возвращает объединенные сообщения пользователя.

    Примеры:
    >>> messages = [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "world"}, {"role": "user", "content": "how are you"}]
    >>> get_last_user_message(messages)
    'how are you'
    >>> messages = [{"role": "assistant", "content": "world"}, {"role": "user", "content": "hello"}]
    >>> get_last_user_message(messages)
    'hello'
    """
    ...
```

### `format_image_prompt`

```python
def format_image_prompt(messages, prompt: str = None) -> str:
    """
    Форматирует подсказку для генерации изображений.

    Args:
        messages: Список сообщений.
        prompt (str, optional): Подсказка для генерации изображений. По умолчанию `None`.

    Returns:
        str: Отформатированная подсказка для генерации изображений.

    Как работает функция:
    - Если `prompt` не указан, функция вызывает `get_last_user_message` для получения последнего сообщения пользователя.
    - Если `prompt` указан, функция возвращает его.

    Примеры:
    >>> messages = [{"role": "user", "content": "a cat"}]
    >>> format_image_prompt(messages)
    'a cat'
    >>> format_image_prompt(messages, prompt="a dog")
    'a dog'
    """
    ...
```

### `format_prompt_max_length`

```python
def format_prompt_max_length(messages: Messages, max_lenght: int) -> str:
    """
    Форматирует подсказку, обрезая ее до максимальной длины.

    Args:
        messages (Messages): Список сообщений.
        max_lenght (int): Максимальная длина подсказки.

    Returns:
        str: Отформатированная подсказка, обрезанная до максимальной длины.

    Как работает функция:
    - Форматирует список сообщений с помощью функции `format_prompt`.
    - Проверяет, превышает ли длина отформатированной подсказки максимальную длину.
    - Если длина подсказки превышает максимальную длину, функция пытается обрезать список сообщений, чтобы уменьшить длину подсказки.
    - Логирует информацию об усечении сообщений.

    Примеры:
    >>> messages = [{"role": "user", "content": "hello" * 1000}]
    >>> format_prompt_max_length(messages, 100)
    'hello... (обрезано)'
    >>> messages = [{"role": "user", "content": "hello"}]
    >>> format_prompt_max_length(messages, 100)
    'User: hello\\nAssistant:'
    """
    ...
```

### `get_random_string`

```python
def get_random_string(length: int = 10) -> str:
    """
    Генерирует случайную строку указанной длины, состоящую из строчных букв и цифр.

    Args:
        length (int, optional): Длина случайной строки для генерации. По умолчанию 10.

    Returns:
        str: Случайная строка указанной длины.

    Как работает функция:
    - Генерирует случайную строку, выбирая символы из строчных букв и цифр.

    Примеры:
    >>> get_random_string(5)
    'a1b2c'
    >>> get_random_string()
    'd4e5f6g7h8'
    """
    ...
```

### `get_random_hex`

```python
def get_random_hex(length: int = 32) -> str:
    """
    Генерирует случайную шестнадцатеричную строку длиной n.

    Returns:
        str: Случайная шестнадцатеричная строка из n символов.

    Как работает функция:
    - Генерирует случайную строку, выбирая символы из шестнадцатеричных цифр (abcdef0123456789).

    Примеры:
    >>> get_random_hex(5)
    'a1b2c'
    >>> get_random_hex()
    'd4e5f6g7h8...'
    """
    ...
```

### `filter_none`

```python
def filter_none(**kwargs) -> dict:
    """
    Фильтрует словарь, удаляя элементы со значением `None`.

    Args:
        **kwargs: Произвольные ключевые аргументы.

    Returns:
        dict: Отфильтрованный словарь, содержащий только элементы со значениями, отличными от `None`.

    Как работает функция:
    - Создает новый словарь, включая только те элементы из входного словаря, значения которых не равны `None`.

    Примеры:
    >>> filter_none(a=1, b=None, c=2)
    {'a': 1, 'c': 2}
    >>> filter_none(a=None, b=None)
    {}
    """
    ...
```

### `async_concat_chunks`

```python
async def async_concat_chunks(chunks: AsyncIterator) -> str:
    """
    Асинхронно объединяет чанки данных в одну строку.

    Args:
        chunks (AsyncIterator): Асинхронный итератор чанков данных.

    Returns:
        str: Объединенная строка из чанков данных.

    Как работает функция:
    - Асинхронно итерируется по чанкам данных.
    - Объединяет все чанки в одну строку.

    Примеры:
    >>> async def generate_chunks():
    ...     yield "hello"
    ...     yield "world"
    >>> async def main():
    ...     result = await async_concat_chunks(generate_chunks())
    ...     print(result)
    >>> import asyncio
    >>> asyncio.run(main())
    helloworld
    """
    ...
```

### `concat_chunks`

```python
def concat_chunks(chunks: Iterator) -> str:
    """
    Объединяет чанки данных в одну строку.

    Args:
        chunks (Iterator): Итератор чанков данных.

    Returns:
        str: Объединенная строка из чанков данных.

    Как работает функция:
    - Итерируется по чанкам данных.
    - Преобразует каждый чанк в строку.
    - Объединяет все чанки в одну строку.

    Примеры:
    >>> chunks = ["hello", "world"]
    >>> concat_chunks(chunks)
    'helloworld'
    >>> chunks = ["hello", Exception("error"), "world"]
    >>> concat_chunks(chunks)
    'helloworld'
    """
    ...
```

### `format_cookies`

```python
def format_cookies(cookies: Cookies) -> str:
    """
    Форматирует словарь cookie в строку для использования в HTTP-запросах.

    Args:
        cookies (Cookies): Словарь cookie, где ключи - это имена cookie, а значения - их значения.

    Returns:
        str: Строка, содержащая cookie в формате "name=value; name=value; ...".

    Как работает функция:
    - Итерируется по словарю cookie.
    - Форматирует каждую пару "ключ-значение" в виде "name=value".
    - Объединяет все отформатированные пары в одну строку, разделяя их символом "; ".

    Примеры:
    >>> cookies = {"name": "john", "age": "30"}
    >>> format_cookies(cookies)
    'name=john; age=30'
    >>> cookies = {}
    >>> format_cookies(cookies)
    ''
    """
    ...