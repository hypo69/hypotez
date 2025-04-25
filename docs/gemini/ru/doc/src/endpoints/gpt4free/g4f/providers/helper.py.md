# Модуль helper

## Обзор

Модуль `helper` предоставляет набор функций, которые упрощают работу с API GPT-4Free и улучшают взаимодействие с моделью.

## Функции

### `to_string`

**Назначение**: Преобразует различный тип данных в строку, чтобы использовать его в запросе к модели.

**Параметры**:

- `value`: Строка, словарь, список или любой объект, который нужно преобразовать в строку.

**Возвращает**:

- `str`: Строка, полученная из `value`.

**Как работает функция**:

- Функция `to_string` проверяет тип `value`. 
- Если `value` является строкой, она возвращается без изменений.
- Если `value` является словарем, функция проверяет наличие ключей `name`, `bucket_id` и `type`.
- Если `value` является списком, функция проходит по элементам списка и рекурсивно вызывает себя, чтобы преобразовать их в строки.
- В противном случае функция пытается преобразовать `value` в строку с помощью `str(value)`.

**Примеры**:

```python
>>> to_string("Hello, World!")
'Hello, World!'
>>> to_string({"name": "Alice", "age": 30})
''
>>> to_string({"bucket_id": "my_bucket"})
'bucket content'
>>> to_string({"type": "text", "text": "Hello, World!"})
'Hello, World!'
>>> to_string(["Hello", "World", {"type": "text", "text": "!"}])
'HelloWorld!'
```

### `format_prompt`

**Назначение**: Форматирует список сообщений в строку, чтобы использовать его в запросе к модели.

**Параметры**:

- `messages`: Список словарей с сообщениями, каждый из которых содержит `role` и `content`.
- `add_special_tokens`: (опционально) Флаг, который добавляет специальные токены в начало и конец сообщения. По умолчанию `False`.
- `do_continue`: (опционально) Флаг, который указывает, нужно ли добавлять в конец сообщения строку `Assistant:`. По умолчанию `False`.

**Возвращает**:

- `str`: Форматированная строка, содержащая все сообщения.

**Как работает функция**:

- Функция `format_prompt` преобразует все сообщения в строку, используя функцию `to_string`.
- Если установлен флаг `add_special_tokens`, функция добавляет специальные токены в начало и конец сообщения.
- Если установлен флаг `do_continue`, функция добавляет в конец сообщения строку `Assistant:`.
- Если установлен флаг `include_system`, функция добавляет в начало сообщения строку `System:`.

**Примеры**:

```python
>>> format_prompt([
...     {"role": "user", "content": "Hello, World!"},
...     {"role": "assistant", "content": "Hello, World!"},
... ])
'User: Hello, World!\nAssistant: Hello, World!\nAssistant:'
>>> format_prompt([
...     {"role": "user", "content": "Hello, World!"},
...     {"role": "assistant", "content": "Hello, World!"},
... ], add_special_tokens=True)
'<|start|>\nUser: Hello, World!\nAssistant: Hello, World!\n<|end|>'
>>> format_prompt([
...     {"role": "user", "content": "Hello, World!"},
...     {"role": "assistant", "content": "Hello, World!"},
... ], do_continue=True)
'User: Hello, World!\nAssistant: Hello, World!\nAssistant'
```

### `get_system_prompt`

**Назначение**: Извлекает текст системного сообщения из списка сообщений.

**Параметры**:

- `messages`: Список словарей с сообщениями, каждый из которых содержит `role` и `content`.

**Возвращает**:

- `str`: Текст системного сообщения.

**Как работает функция**:

- Функция `get_system_prompt` проходит по списку сообщений и возвращает строку с текстом системных сообщений.

**Пример**:

```python
>>> get_system_prompt([
...     {"role": "system", "content": "You are a helpful assistant."},
...     {"role": "user", "content": "Hello, World!"},
...     {"role": "assistant", "content": "Hello, World!"},
... ])
'You are a helpful assistant.'
```

### `get_last_user_message`

**Назначение**: Извлекает текст последнего пользовательского сообщения из списка сообщений.

**Параметры**:

- `messages`: Список словарей с сообщениями, каждый из которых содержит `role` и `content`.

**Возвращает**:

- `str`: Текст последнего пользовательского сообщения.

**Как работает функция**:

- Функция `get_last_user_message` проходит по списку сообщений в обратном порядке и возвращает строку с текстом последнего пользовательского сообщения.

**Пример**:

```python
>>> get_last_user_message([
...     {"role": "system", "content": "You are a helpful assistant."},
...     {"role": "user", "content": "Hello, World!"},
...     {"role": "assistant", "content": "Hello, World!"},
...     {"role": "user", "content": "What is your name?"},
... ])
'What is your name?'
```

### `format_image_prompt`

**Назначение**: Форматирует запрос для модели, который включает в себя изображение.

**Параметры**:

- `messages`: Список словарей с сообщениями, каждый из которых содержит `role` и `content`.
- `prompt`: (опционально) Текст запроса для модели. По умолчанию `None`.

**Возвращает**:

- `str`: Форматированный текст запроса.

**Как работает функция**:

- Если `prompt` не задан, функция возвращает текст последнего пользовательского сообщения.
- В противном случае функция возвращает `prompt`.

**Примеры**:

```python
>>> format_image_prompt([
...     {"role": "user", "content": "What is this image?"},
...     {"role": "assistant", "content": "This is a picture of a cat."},
... ])
'What is this image?'
>>> format_image_prompt([
...     {"role": "user", "content": "What is this image?"},
...     {"role": "assistant", "content": "This is a picture of a cat."},
... ], prompt="Describe this image in detail.")
'Describe this image in detail.'
```

### `format_prompt_max_length`

**Назначение**: Обрезает текст запроса до максимальной длины.

**Параметры**:

- `messages`: Список словарей с сообщениями, каждый из которых содержит `role` и `content`.
- `max_lenght`: Максимальная длина текста запроса.

**Возвращает**:

- `str`: Обрезанный текст запроса.

**Как работает функция**:

- Функция `format_prompt_max_length` сначала форматирует текст запроса с помощью функции `format_prompt`.
- Затем функция проверяет длину текста запроса и, если она превышает `max_lenght`, обрезает текст, удаляя сообщения из середины, а затем из начала, пока длина текста не станет меньше `max_lenght`.
- Функция выводит в лог информацию о том, как изменилась длина текста.

**Пример**:

```python
>>> format_prompt_max_length([
...     {"role": "user", "content": "Hello, World!"},
...     {"role": "assistant", "content": "Hello, World!"},
...     {"role": "user", "content": "What is your name?"},
...     {"role": "assistant", "content": "My name is Bard."},
...     {"role": "user", "content": "What is your favorite color?"},
...     {"role": "assistant", "content": "My favorite color is blue."},
...     {"role": "user", "content": "What is your favorite animal?"},
...     {"role": "assistant", "content": "My favorite animal is a cat."},
... ], max_lenght=50)
'Messages trimmed from: 114 to: 50\nUser: What is your favorite animal?\nAssistant: My favorite animal is a cat.\nAssistant:'
```

### `get_random_string`

**Назначение**: Генерирует случайную строку заданной длины.

**Параметры**:

- `length`: (опционально) Длина случайной строки. По умолчанию `10`.

**Возвращает**:

- `str`: Случайная строка заданной длины.

**Как работает функция**:

- Функция `get_random_string` использует модуль `random` для генерации случайной строки заданной длины, которая состоит из строчных букв и цифр.

**Пример**:

```python
>>> get_random_string()
'd29fh7843s'
>>> get_random_string(length=15)
'1b3d9y5g2f4w0r'
```

### `get_random_hex`

**Назначение**: Генерирует случайную шестнадцатеричную строку заданной длины.

**Параметры**:

- `length`: (опционально) Длина случайной строки. По умолчанию `32`.

**Возвращает**:

- `str`: Случайная шестнадцатеричная строка заданной длины.

**Как работает функция**:

- Функция `get_random_hex` использует модуль `random` для генерации случайной строки заданной длины, которая состоит из шестнадцатеричных цифр.

**Пример**:

```python
>>> get_random_hex()
'a8f432e9a1632384f46955c4a97b4a92'
>>> get_random_hex(length=16)
'1d854a2b347821'
```

### `filter_none`

**Назначение**: Фильтрует словарь, удаляя элементы с значением `None`.

**Параметры**:

- `**kwargs`: Словарь, который нужно отфильтровать.

**Возвращает**:

- `dict`: Отфильтрованный словарь.

**Как работает функция**:

- Функция `filter_none` проходит по всем элементам словаря `kwargs` и добавляет в новый словарь только те элементы, которые не равны `None`.

**Пример**:

```python
>>> filter_none(a=1, b=None, c="Hello", d=None)
{'a': 1, 'c': 'Hello'}
```

### `async_concat_chunks`

**Назначение**: Объединяет асинхронный итератор в строку.

**Параметры**:

- `chunks`: Асинхронный итератор, который нужно объединить.

**Возвращает**:

- `str`: Строка, полученная из объединения элементов итератора.

**Как работает функция**:

- Функция `async_concat_chunks` использует асинхронный цикл `for` для получения всех элементов итератора `chunks`.
- Затем функция `async_concat_chunks` вызывает функцию `concat_chunks` для объединения всех элементов в строку.

**Пример**:

```python
>>> async def async_generator():
...     yield "Hello"
...     yield " "
...     yield "World"
...
>>> async_concat_chunks(async_generator())
'Hello World'
```

### `concat_chunks`

**Назначение**: Объединяет итератор в строку.

**Параметры**:

- `chunks`: Итератор, который нужно объединить.

**Возвращает**:

- `str`: Строка, полученная из объединения элементов итератора.

**Как работает функция**:

- Функция `concat_chunks` проходит по всем элементам итератора `chunks` и добавляет их в строку.

**Пример**:

```python
>>> concat_chunks(["Hello", " ", "World"])
'Hello World'
```

### `format_cookies`

**Назначение**: Форматирует словарь с куки в строку.

**Параметры**:

- `cookies`: Словарь с куки.

**Возвращает**:

- `str`: Строка, полученная из форматирования словаря с куки.

**Как работает функция**:

- Функция `format_cookies` проходит по всем элементам словаря `cookies` и добавляет их в строку в формате `key=value`.

**Пример**:

```python
>>> format_cookies({"session": "123456", "user_id": "789012"})
'session=123456; user_id=789012'
```