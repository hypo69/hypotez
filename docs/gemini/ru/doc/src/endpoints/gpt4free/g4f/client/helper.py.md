# Модуль `helper.py`

## Обзор

Модуль содержит вспомогательные функции для обработки текста, извлечения информации из блоков кода и безопасного закрытия асинхронных генераторов. Он предоставляет инструменты для фильтрации содержимого на основе Markdown и JSON, поиска стоп-слов и обработки аргументов функций.

## Подробнее

Этот модуль предназначен для упрощения задач обработки текста и управления асинхронными операциями в проекте. Он используется для извлечения полезной информации из текстовых блоков, фильтрации данных и безопасного завершения работы с асинхронными генераторами.

## Функции

### `filter_markdown`

```python
def filter_markdown(text: str, allowd_types=None, default=None) -> str:
    """
    Parses code block from a string.

    Args:
        text (str): A string containing a code block.

    Returns:
        dict: A dictionary parsed from the code block.
    """
    ...
```

**Назначение**: Извлекает блок кода из строки, обрамленного Markdown-разметкой.

**Параметры**:
- `text` (str): Строка, содержащая блок кода.
- `allowd_types`: Список допустимых типов блоков кода (например, `['python', 'json']`). Если `None`, допускаются все типы.
- `default`: Значение по умолчанию, которое возвращается, если блок кода не найден или его тип не соответствует `allowd_types`.

**Возвращает**:
- `str`: Извлеченный блок кода (тип `str`). Если блок кода не найден или его тип не соответствует `allowd_types`, возвращается значение `default`.

**Как работает функция**:
Функция использует регулярное выражение для поиска блоков кода, заключенных в тройные обратные кавычки (` ``` `). Если блок найден, проверяется, соответствует ли его тип допустимым типам, указанным в параметре `allowd_types`. Если соответствие есть или `allowd_types` не указан, функция возвращает извлеченный код. В противном случае возвращается значение по умолчанию `default`.

**Примеры**:

```python
text = "```python\nprint('Hello, world!')\n```"
code = filter_markdown(text)
print(code)
# >>> print('Hello, world!')

text = "```json\n{\"key\": \"value\"}\n```"
code = filter_markdown(text, allowd_types=['json'])
print(code)
# >>> {"key": "value"}

text = "Some text without code block"
code = filter_markdown(text, default="No code found")
print(code)
# >>> No code found
```

### `filter_json`

```python
def filter_json(text: str) -> str:
    """
    Parses JSON code block from a string.

    Args:
        text (str): A string containing a JSON code block.

    Returns:
        dict: A dictionary parsed from the JSON code block.
    """
    ...
```

**Назначение**: Извлекает JSON-блок кода из строки.

**Параметры**:
- `text` (str): Строка, содержащая JSON-блок кода.

**Возвращает**:
- `str`: Извлеченный JSON-блок кода. Если блок не найден, возвращается исходная строка с удаленными начальными и конечными символами новой строки и пробелами.

**Как работает функция**:
Функция вызывает `filter_markdown` с параметрами, настроенными для извлечения JSON-блоков кода (типы `""` и `"json"`). Если JSON-блок кода не найден, возвращается исходная строка с удаленными начальными и конечными символами новой строки и пробелами.

**Примеры**:

```python
text = "```json\n{\"key\": \"value\"}\n```"
json_code = filter_json(text)
print(json_code)
# >>> {"key": "value"}

text = "Some text without JSON block"
json_code = filter_json(text)
print(json_code)
# >>> Some text without JSON block
```

### `find_stop`

```python
def find_stop(stop: Optional[list[str]], content: str, chunk: str = None):
    """
    <Тут Ты пишешь что именно делает функция>
    Args:
        stop (Optional[list[str]]): <Тут Ты пишешь что значит параметр>
        content (str): <Тут Ты пишешь что значит параметр>
        chunk (str, optional): <Тут Ты пишешь что значит параметр>. Defaults to None.

    Returns:
        <Тут Ты пишешь что возвращает функция>
    """
    ...
```

**Назначение**: Ищет первое вхождение одного из стоп-слов в строке и обрезает строку до этого вхождения.

**Параметры**:
- `stop` (Optional[list[str]]): Список стоп-слов для поиска. Если `None`, поиск не производится.
- `content` (str): Строка, в которой производится поиск.
- `chunk` (str, optional): Дополнительная строка, которая также обрезается, если стоп-слово найдено. По умолчанию `None`.

**Возвращает**:
- `tuple[int, str, str]`: Кортеж, содержащий:
    - `first` (int): Индекс первого вхождения стоп-слова (или -1, если стоп-слова не найдены).
    - `content` (str): Обрезанная строка `content`.
    - `chunk` (str): Обрезанная строка `chunk` (или `None`, если `chunk` не был передан).

**Как работает функция**:
Функция перебирает список стоп-слов и ищет каждое слово в строке `content`. Если одно из стоп-слов найдено, строка `content` обрезается до этого вхождения. Если также передана строка `chunk`, она также обрезается до первого вхождения стоп-слова (если оно найдено). Функция возвращает индекс первого вхождения стоп-слова, обрезанные строки `content` и `chunk`.

**Примеры**:

```python
stop_words = ["stop", "end"]
content = "This is a test string with a stop word."
chunk = "This is an additional chunk of text."
first, content, chunk = find_stop(stop_words, content, chunk)
print(first, content, chunk)
# >>> 29 This is a test string with a   This is an additional chunk of text.

stop_words = ["stop", "end"]
content = "This is a test string."
chunk = "This is an additional chunk of text with end word."
first, content, chunk = find_stop(stop_words, content, chunk)
print(first, content, chunk)
# >>> -1 This is a test string. This is an additional chunk of text with 
```

### `filter_none`

```python
def filter_none(**kwargs) -> dict:
    """
    <Тут Ты пишешь что именно делает функция>
    Args:
        **kwargs: <Тут Ты пишешь что значит параметр>

    Returns:
        dict: <Тут Ты пишешь что возвращает функция>
    """
    ...
```

**Назначение**: Создает словарь, содержащий только аргументы, значения которых не равны `None`.

**Параметры**:
- `**kwargs`: Произвольный набор именованных аргументов.

**Возвращает**:
- `dict`: Словарь, содержащий только те аргументы, значения которых не равны `None`.

**Как работает функция**:
Функция перебирает все переданные именованные аргументы и добавляет в результирующий словарь только те, значения которых не равны `None`.

**Примеры**:

```python
filtered_dict = filter_none(a=1, b=None, c="test")
print(filtered_dict)
# >>> {'a': 1, 'c': 'test'}

filtered_dict = filter_none(a=None, b=None)
print(filtered_dict)
# >>> {}
```

### `safe_aclose`

```python
async def safe_aclose(generator: AsyncGenerator) -> None:
    """
    <Тут Ты пишешь что именно делает функция>
    Args:
        generator (AsyncGenerator): <Тут Ты пишешь что значит параметр>

    Returns:
        None: <Тут Ты пишешь что возвращает функция>
    """
    ...
```

**Назначение**: Безопасно закрывает асинхронный генератор.

**Параметры**:
- `generator` (AsyncGenerator): Асинхронный генератор, который необходимо закрыть.

**Возвращает**:
- `None`

**Как работает функция**:
Функция проверяет, является ли переданный объект генератором и имеет ли он метод `aclose`. Если да, то вызывается метод `aclose` для закрытия генератора. В случае возникновения исключения при закрытии генератора, информация об ошибке записывается в лог с уровнем `warning`.

**Примеры**:

```python
async def my_generator():
    yield 1
    yield 2

async def main():
    gen = my_generator()
    try:
        async for i in gen:
            print(i)
            break
    finally:
        await safe_aclose(gen)

# Заметка: Для выполнения этого примера требуется асинхронная среда исполнения.