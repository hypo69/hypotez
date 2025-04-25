# Модуль для вспомогательных функций gpt4free
## Обзор

Этот модуль содержит набор вспомогательных функций, используемых в модуле `gpt4free`. Он предоставляет функции для обработки текста, фильтрации JSON-данных и работы с асинхронными генераторами.

## Классы

### `None`

## Функции

### `filter_markdown`

**Назначение**: Извлекает код из Markdown-текста, используя регулярные выражения.

**Параметры**:

- `text` (str): Строка с Markdown-текстом, содержащая код.
- `allowd_types` (Optional[List[str]]): Список допустимых типов кода.
- `default` (Any): Значение по умолчанию, которое возвращается, если код не найден.

**Возвращает**:

- `str`: Строка с кодом, если он найден, иначе `default`.

**Вызывает исключения**:

- `None`

**Как работает функция**:

1. Использует регулярное выражение, чтобы найти блоки кода, заключенные в тройные кавычки `````.
2. Проверяет, соответствует ли тип кода (в строке после `````) допустимым типам, заданным в `allowd_types`.
3. Возвращает текст кода из блока `code`, если код найден, иначе `default`.

**Примеры**:

```python
>>> text = "```python\nprint('Hello world!')\n```\nThis is a test."
>>> filter_markdown(text)
'print(\'Hello world!\')'

>>> text = "```javascript\nconsole.log('Hello world!');\n```\nThis is a test."
>>> filter_markdown(text, allowd_types=["python"])
None

>>> text = "This is a test without code."
>>> filter_markdown(text)
None

>>> text = "```python\nprint('Hello world!')\n```\nThis is a test."
>>> filter_markdown(text, default="No code found")
'print(\'Hello world!\')'
```


### `filter_json`

**Назначение**: Извлекает JSON-код из Markdown-текста, используя функцию `filter_markdown`.

**Параметры**:

- `text` (str): Строка с Markdown-текстом, содержащая JSON-код.

**Возвращает**:

- `str`: JSON-код, извлеченный из текста.

**Вызывает исключения**:

- `None`

**Как работает функция**:

1. Использует `filter_markdown` для поиска блока кода с типом `json`.
2. Возвращает текст кода.

**Примеры**:

```python
>>> text = "```json\n{\"name\": \"John Doe\", \"age\": 30}\n```\nThis is a test."
>>> filter_json(text)
'{\"name\": \"John Doe\", \"age\": 30}'

>>> text = "This is a test without code."
>>> filter_json(text)
'This is a test without code.'
```


### `find_stop`

**Назначение**: Ищет первую позицию заданной стоп-фразы в тексте и обрезает текст до этой позиции.

**Параметры**:

- `stop` (Optional[List[str]]): Список стоп-фраз, которые нужно найти в тексте.
- `content` (str): Текст, в котором нужно искать стоп-фразы.
- `chunk` (str): Часть текста, в котором нужно искать стоп-фразы (используется для отслеживания позиции в исходном тексте).

**Возвращает**:

- `tuple[int, str, str]`: Кортеж из трех элементов: 
    - позиция первой найденной стоп-фразы в тексте, 
    - текст, обрезанный до найденной позиции,
    - часть текста `chunk`, обрезанная до найденной позиции.

**Вызывает исключения**:

- `None`

**Как работает функция**:

1. Проходит по списку стоп-фраз `stop`.
2. Для каждой стоп-фразы:
    - Находит позицию стоп-фразы в тексте `content`.
    - Если позиция найдена, обрезает текст `content` до этой позиции.
    - Обрезает часть текста `chunk` до этой позиции, если `chunk` не равен `None`.
3. Возвращает позицию первой найденной стоп-фразы, обрезанный текст `content` и обрезанную часть `chunk`.

**Примеры**:

```python
>>> find_stop(["stop", "end"], "This is a test stop This is another test.")
(17, 'This is a test stop', 'This is a test stop')

>>> find_stop(["stop", "end"], "This is a test end This is another test.")
(17, 'This is a test end', 'This is a test end')

>>> find_stop(["stop", "end"], "This is a test. This is another test.", chunk="This is a test.")
(17, 'This is a test', 'This is a test')

>>> find_stop(["stop", "end"], "This is a test. This is another test.", chunk="This is another test.")
(0, 'This is a test. This is another test.', 'This is another test.')

>>> find_stop(["stop", "end"], "This is a test. This is another test.")
(-1, 'This is a test. This is another test.', 'This is a test. This is another test.')
```


### `filter_none`

**Назначение**: Фильтрует словарь, удаляя элементы со значением `None`.

**Параметры**:

- `**kwargs`: Словарь, который нужно отфильтровать.

**Возвращает**:

- `dict`: Отфильтрованный словарь, содержащий только элементы со значениями, отличными от `None`.

**Вызывает исключения**:

- `None`

**Как работает функция**:

1. Проходит по элементам словаря `kwargs`.
2. Добавляет элемент в новый словарь, если его значение не равно `None`.
3. Возвращает новый словарь.

**Примеры**:

```python
>>> filter_none(a=1, b=None, c=3)
{'a': 1, 'c': 3}

>>> filter_none()
{}

>>> filter_none(a=None, b=None, c=None)
{}
```


### `safe_aclose`

**Назначение**: Безопасное закрытие асинхронного генератора.

**Параметры**:

- `generator` (AsyncGenerator): Асинхронный генератор, который нужно закрыть.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `None`

**Как работает функция**:

1. Проверяет, не равен ли `generator` `None` и есть ли у него метод `aclose`.
2. Если да, пытается закрыть генератор с помощью метода `aclose`.
3. Если возникает ошибка, выводит предупреждение в лог.

**Примеры**:

```python
>>> async def my_generator():
...     yield 1
...     yield 2
...     yield 3
...
>>> generator = my_generator()
>>> safe_aclose(generator)