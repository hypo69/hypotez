# Module for working with GPT4Free helper functions
===============================================================

The module provides helper functions for interacting with GPT4Free models, including formatting prompts, managing messages, and generating random strings.

## Table of Contents
- [Functions](#functions)
    - [`to_string`](#to_string)
    - [`format_prompt`](#format_prompt)
    - [`get_system_prompt`](#get_system_prompt)
    - [`get_last_user_message`](#get_last_user_message)
    - [`format_image_prompt`](#format_image_prompt)
    - [`format_prompt_max_length`](#format_prompt_max_length)
    - [`get_random_string`](#get_random_string)
    - [`get_random_hex`](#get_random_hex)
    - [`filter_none`](#filter_none)
    - [`async_concat_chunks`](#async_concat_chunks)
    - [`concat_chunks`](#concat_chunks)
    - [`format_cookies`](#format_cookies)

## Functions

### `to_string`

```python
def to_string(value) -> str:
    """Преобразует различные типы данных в строку.

    Args:
        value: Значение для преобразования.

    Returns:
        str: Преобразованная строка.
    """
    ...
```

### `format_prompt`

```python
def format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False, include_system: bool = True) -> str:
    """Форматирует серию сообщений в одну строку, опционально добавляя специальные токены.

    Args:
        messages (Messages): Список словарей сообщений, каждый из которых содержит 'role' и 'content'.
        add_special_tokens (bool): Флаг, указывающий, следует ли добавлять специальные токены форматирования.
        do_continue (bool): Флаг, указывающий, следует ли использовать формат `do_continue`.

    Returns:
        str: Форматированная строка, содержащая все сообщения.
    """
    ...
```

### `get_system_prompt`

```python
def get_system_prompt(messages: Messages) -> str:
    """Извлекает системный запрос из списка сообщений.

    Args:
        messages (Messages): Список словарей сообщений.

    Returns:
        str: Системный запрос.
    """
    ...
```

### `get_last_user_message`

```python
def get_last_user_message(messages: Messages) -> str:
    """Извлекает последнее сообщение от пользователя из списка сообщений.

    Args:
        messages (Messages): Список словарей сообщений.

    Returns:
        str: Последнее сообщение от пользователя.
    """
    ...
```

### `format_image_prompt`

```python
def format_image_prompt(messages, prompt: str = None) -> str:
    """Форматирует запрос для изображения.

    Args:
        messages: Список сообщений.
        prompt: Дополнительный запрос.

    Returns:
        str: Форматированный запрос.
    """
    ...
```

### `format_prompt_max_length`

```python
def format_prompt_max_length(messages: Messages, max_lenght: int) -> str:
    """Форматирует запрос с ограничением по длине.

    Args:
        messages (Messages): Список сообщений.
        max_lenght (int): Максимальная длина запроса.

    Returns:
        str: Форматированный запрос.
    """
    ...
```

### `get_random_string`

```python
def get_random_string(length: int = 10) -> str:
    """Генерирует случайную строку заданной длины, содержащую строчные буквы и цифры.

    Args:
        length (int, optional): Длина генерируемой строки. По умолчанию 10.

    Returns:
        str: Случайная строка заданной длины.
    """
    ...
```

### `get_random_hex`

```python
def get_random_hex(length: int = 32) -> str:
    """Генерирует случайную шестнадцатеричную строку с n длиной.

    Returns:
        str: Случайная шестнадцатеричная строка n символов.
    """
    ...
```

### `filter_none`

```python
def filter_none(**kwargs) -> dict:
    """Удаляет пары ключ-значение, где значение равно None.

    Args:
        **kwargs: Ключ-значение для фильтрации.

    Returns:
        dict: Словарь без пар ключ-значение, где значение равно None.
    """
    ...
```

### `async_concat_chunks`

```python
async def async_concat_chunks(chunks: AsyncIterator) -> str:
    """Асинхронно конкатенирует чанки из асинхронного итератора.

    Args:
        chunks (AsyncIterator): Асинхронный итератор чанков.

    Returns:
        str: Конкатенированная строка.
    """
    ...
```

### `concat_chunks`

```python
def concat_chunks(chunks: Iterator) -> str:
    """Конкатенирует чанки из итератора.

    Args:
        chunks (Iterator): Итератор чанков.

    Returns:
        str: Конкатенированная строка.
    """
    ...
```

### `format_cookies`

```python
def format_cookies(cookies: Cookies) -> str:
    """Форматирует cookie в строку.

    Args:
        cookies (Cookies): Словарь cookie.

    Returns:
        str: Форматированная строка cookie.
    """
    ...
```