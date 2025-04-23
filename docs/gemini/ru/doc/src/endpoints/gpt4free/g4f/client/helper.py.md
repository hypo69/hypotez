# Модуль `helper`

## Обзор

Модуль `helper` содержит набор вспомогательных функций для обработки текста, включая фильтрацию кода из markdown блоков, поиск стоп-слов и безопасное закрытие асинхронных генераторов.

## Подробнее

Модуль предоставляет инструменты для извлечения полезной информации из текстовых данных, что может быть полезно при работе с API или другими источниками, возвращающими текст в формате markdown.

## Функции

### `filter_markdown`

**Назначение**: Извлекает код из markdown блока в строке.

**Параметры**:
- `text` (str): Строка, содержащая markdown блок кода.
- `allowd_types` (list[str], optional): Список разрешенных типов кода. Если `None`, разрешены все типы. По умолчанию `None`.
- `default` (str, optional): Значение по умолчанию, возвращаемое, если код не найден или тип кода не разрешен. По умолчанию `None`.

**Возвращает**:
- `str`: Код, извлеченный из markdown блока, или значение `default`, если код не найден или его тип не разрешен.

**Как работает функция**:
1. Использует регулярное выражение для поиска markdown блока кода в строке.
2. Проверяет, разрешен ли тип кода (если `allowd_types` не `None`).
3. Если код найден и тип разрешен, возвращает извлеченный код.
4. В противном случае возвращает значение `default`.

**Примеры**:

```python
text = "```python\nprint('Hello, world!')\n```"
code = filter_markdown(text, allowd_types=['python'])
print(code)  # Вывод: print('Hello, world!')

text = "```javascript\nconsole.log('Hello, world!');\n```"
code = filter_markdown(text, allowd_types=['python'])
print(code)  # Вывод: None

text = "```json\n{'key': 'value'}\n```"
code = filter_markdown(text)
print(code)  # Вывод: {'key': 'value'}
```

### `filter_json`

**Назначение**: Извлекает JSON из markdown блока в строке.

**Параметры**:
- `text` (str): Строка, содержащая JSON в markdown блоке.

**Возвращает**:
- `str`: JSON, извлеченный из markdown блока, или исходный текст, если JSON не найден.

**Как работает функция**:
1. Вызывает функцию `filter_markdown` с параметрами `allowd_types=['', 'json']` и `default=text.strip('^\n ')`.
2. Возвращает результат вызова `filter_markdown`.

**Примеры**:

```python
text = "```json\n{'key': 'value'}\n```"
json_code = filter_json(text)
print(json_code)  # Вывод: {'key': 'value'}

text = "{'key': 'value'}"
json_code = filter_json(text)
print(json_code)  # Вывод: {'key': 'value'}
```

### `find_stop`

**Назначение**: Находит первое вхождение стоп-слова в строке и обрезает строку до этого слова.

**Параметры**:
- `stop` (list[str], optional): Список стоп-слов. Если `None`, функция ничего не обрезает. По умолчанию `None`.
- `content` (str): Строка, в которой нужно искать стоп-слова.
- `chunk` (str, optional): Дополнительная строка, которая также обрезается, если стоп-слово найдено. По умолчанию `None`.

**Возвращает**:
- `tuple[int, str, str]`: Кортеж, содержащий:
  - `first` (int): Индекс первого найденного стоп-слова или -1, если стоп-слова не найдены.
  - `content` (str): Обрезанная строка `content`.
  - `chunk` (str): Обрезанная строка `chunk` или `None`, если `chunk` был `None`.

**Как работает функция**:
1. Если `stop` не `None`, функция итерируется по списку стоп-слов.
2. Для каждого стоп-слова функция ищет его в строке `content`.
3. Если стоп-слово найдено, функция обрезает строку `content` до этого слова.
4. Если также предоставлена строка `chunk`, она также обрезается до найденного стоп-слова.
5. Функция возвращает индекс первого найденного стоп-слова и обрезанные строки `content` и `chunk`.

**Примеры**:

```python
stop_words = ['stop', 'end']
content = 'This is a stop word.'
chunk = 'This is a chunk of text.'
first, content, chunk = find_stop(stop_words, content, chunk)
print(first, content, chunk)  # Вывод: 10 This is a   This is a chunk of text.

stop_words = ['stop', 'end']
content = 'This is a test.'
chunk = 'This is a chunk of text.'
first, content, chunk = find_stop(stop_words, content, chunk)
print(first, content, chunk)  # Вывод: -1 This is a test. This is a chunk of text.
```

### `filter_none`

**Назначение**: Создает словарь, содержащий только элементы с не-`None` значениями.

**Параметры**:
- `**kwargs`: Произвольный набор именованных аргументов.

**Возвращает**:
- `dict`: Словарь, содержащий только элементы с не-`None` значениями.

**Как работает функция**:
1. Итерируется по всем переданным именованным аргументам.
2. Создает новый словарь, добавляя только те элементы, у которых значение не равно `None`.
3. Возвращает новый словарь.

**Примеры**:

```python
filtered_dict = filter_none(a=1, b=None, c=3)
print(filtered_dict)  # Вывод: {'a': 1, 'c': 3}
```

### `safe_aclose`

**Назначение**: Безопасно закрывает асинхронный генератор.

**Параметры**:
- `generator` (AsyncGenerator): Асинхронный генератор, который нужно закрыть.

**Возвращает**:
- `None`

**Как работает функция**:
1. Проверяет, что генератор не `None` и имеет метод `aclose`.
2. Пытается вызвать метод `aclose` генератора.
3. Если во время закрытия возникает исключение, логирует предупреждение.

**Примеры**:

```python
import asyncio
import logging

async def my_generator():
    yield 1
    yield 2

async def main():
    gen = my_generator()
    async for i in gen:
        print(i)
    await safe_aclose(gen)

if __name__ == "__main__":
    asyncio.run(main())
```