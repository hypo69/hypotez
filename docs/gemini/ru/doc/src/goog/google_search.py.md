# Модуль GoogleHtmlParser

## Обзор

Модуль `src/goog/google_search.py` содержит класс `GoogleHtmlParser`, который используется для парсинга HTML-кода поисковой выдачи Google и извлечения из него структурированных данных. Класс парсит как мобильные, так и десктопные версии результатов поиска Google.

## Подробней

Этот модуль используется в проекте `hypotez` для обработки результатов поиска Google. Он парсит HTML-код результатов поиска и извлекает из него следующие данные:

- **Количество результатов поиска**: Извлекает числовое значение с приблизительным количеством результатов.
- **Featured snippet**: Извлекает заголовок и URL featured snippet, если он присутствует.
- **Карточка знаний**: Извлекает карточку знаний с заголовком, подзаголовком, описанием и дополнительной информацией.
- **Органические результаты**: Извлекает список органических результатов поиска, включая URL, заголовок и описание.
- **Скроллируемые виджеты**: Извлекает данные из скроллируемых виджетов (например, топовые истории или твиты).

## Классы

### `GoogleHtmlParser`

**Описание**: Класс для парсинга HTML с Google Search.

**Атрибуты**:

- `tree (html.Element)`: Дерево документа, полученное через `html.fromstring()`.
- `user_agent (str)`: User agent, использованный для получения HTML Google Search.

**Методы**:

- `__init__(self, html_str: str, user_agent: str = 'desktop') -> None`: Инициализация парсера. Создает дерево документа из строки HTML.

- `_clean(self, content: str) -> str`: Очистка строки от лишних символов. Очищает строку от пробелов и лишних символов.

- `_normalize_dict_key(self, content: str) -> str`: Нормализация строки для использования в качестве ключа словаря. Заменяет пробелы на подчеркивания, убирает двоеточия, приводит к нижнему регистру.

- `_get_estimated_results(self) -> int`: Получение количества результатов поиска. Возвращает количество найденных результатов для десктопной версии Google Search.

- `_get_organic(self) -> list`: Получение органических результатов поиска. Возвращает список органических результатов без дополнительных фич (snippet, featured snippet и т.д.).

- `_get_featured_snippet(self) -> dict | None`: Получение featured snippet. Если существует, возвращает featured snippet с заголовком и URL.

- `_get_knowledge_card(self) -> dict | None`: Получение карточки знаний. Возвращает карточку знаний с заголовком, подзаголовком и описанием, если существует.

- `_get_scrolling_sections(self) -> list`: Получение данных из скроллируемых виджетов. Возвращает список данных из виджетов, например, топовые истории или твиты.

- `get_data(self) -> dict`: Получение итоговых данных с поисковой страницы. Собирает данные с результатов поиска: органические результаты, карточка знаний и др.

## Функции

### `_clean(self, content: str) -> str`

**Назначение**: Очистка строки от лишних символов.

**Параметры**:

- `content (str)`: Строка для очистки.

**Возвращает**:

- `str`: Очищенная строка.

**Как работает функция**:

Функция принимает строку в качестве параметра `content`. Она очищает ее от лишних символов, таких как пробелы в начале и конце, а также лишние пробелы между словами.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('  Example  string  ')
>>> parser._clean('  Example  string  ')
'Example string'

>>> parser._clean('   Another  string  with extra spaces   ')
'Another string with extra spaces'
```

### `_normalize_dict_key(self, content: str) -> str`

**Назначение**: Нормализация строки для использования в качестве ключа словаря.

**Параметры**:

- `content (str)`: Строка для нормализации.

**Возвращает**:

- `str`: Нормализованная строка.

**Как работает функция**:

Функция принимает строку в качестве параметра `content` и нормализует ее для использования в качестве ключа словаря. Она заменяет пробелы на подчеркивания, убирает двоеточия, приводит к нижнему регистру и удаляет лишние подчеркивания в начале и конце строки.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('')
>>> parser._normalize_dict_key('Example string')
'example_string'

>>> parser._normalize_dict_key('  Another string with spaces: ')
'another_string_with_spaces'
```

### `_get_estimated_results(self) -> int`

**Назначение**: Получение количества результатов поиска.

**Параметры**:

- Нет.

**Возвращает**:

- `int`: Число результатов поиска.

**Как работает функция**:

Функция извлекает количество результатов поиска с HTML-страницы. Она использует XPath для поиска элемента, содержащего информацию о количестве результатов, и извлекает из него числовое значение.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('')
>>> parser._get_estimated_results()
0 # если не найдено значение - возвращается 0

>>> parser = GoogleHtmlParser('')
>>> parser._get_estimated_results()
1000000 # пример, если на странице указано 1 000 000 результатов поиска
```

### `_get_organic(self) -> list`

**Назначение**: Получение органических результатов поиска.

**Параметры**:

- Нет.

**Возвращает**:

- `list`: Список словарей с органическими результатами.

**Как работает функция**:

Функция извлекает список органических результатов поиска с HTML-страницы. Она использует XPath для поиска элементов, соответствующих органическим результатам, и извлекает из них информацию о URL, заголовке и описании.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('')
>>> parser._get_organic()
[
    {'url': 'https://example.com/page1', 'title': 'Example Page 1', 'snippet': 'This is a description of the first page.', 'rich_snippet': None},
    {'url': 'https://example.com/page2', 'title': 'Example Page 2', 'snippet': 'This is a description of the second page.', 'rich_snippet': None},
    # ... и так далее, для каждого результата
]
```

### `_get_featured_snippet(self) -> dict | None`

**Назначение**: Получение featured snippet.

**Параметры**:

- Нет.

**Возвращает**:

- `dict | None`: Словарь с заголовком и URL или None.

**Как работает функция**:

Функция проверяет наличие featured snippet на HTML-странице. Если он есть, она извлекает из него заголовок и URL.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('')
>>> parser._get_featured_snippet()
None # если не найдено значение - возвращается None

>>> parser = GoogleHtmlParser('')
>>> parser._get_featured_snippet()
{'title': 'Featured Snippet Title', 'url': 'https://example.com/featured_snippet'}
```

### `_get_knowledge_card(self) -> dict | None`

**Назначение**: Получение карточки знаний.

**Параметры**:

- Нет.

**Возвращает**:

- `dict | None`: Словарь с данными карточки знаний или None.

**Как работает функция**:

Функция проверяет наличие карточки знаний на HTML-странице. Если она есть, она извлекает из нее заголовок, подзаголовок, описание и дополнительную информацию.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('')
>>> parser._get_knowledge_card()
None # если не найдено значение - возвращается None

>>> parser = GoogleHtmlParser('')
>>> parser._get_knowledge_card()
{'title': 'Knowledge Card Title', 'subtitle': 'Knowledge Card Subtitle', 'description': 'This is a description of the knowledge card.', 'more_info': [{'key1': 'value1'}, {'key2': 'value2'}]}
```

### `_get_scrolling_sections(self) -> list`

**Назначение**: Получение данных из скроллируемых виджетов.

**Параметры**:

- Нет.

**Возвращает**:

- `list`: Список словарей с данными из виджетов.

**Как работает функция**:

Функция извлекает данные из скроллируемых виджетов на HTML-странице. Она использует XPath для поиска элементов, соответствующих виджетам, и извлекает из них информацию о заголовке и URL.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('')
>>> parser._get_scrolling_sections()
[
    {'section_title': 'Top Stories', 'section_data': [{'title': 'Story 1', 'url': 'https://example.com/story1'}, {'title': 'Story 2', 'url': 'https://example.com/story2'}]},
    {'section_title': 'Tweets', 'section_data': [{'title': 'Tweet 1', 'url': 'https://twitter.com/tweet1'}, {'title': 'Tweet 2', 'url': 'https://twitter.com/tweet2'}]}
]
```

### `get_data(self) -> dict`

**Назначение**: Получение итоговых данных с поисковой страницы.

**Параметры**:

- Нет.

**Возвращает**:

- `dict`: Словарь с данными поисковой страницы.

**Как работает функция**:

Функция собирает все данные, извлеченные из HTML-страницы, в один словарь. Она включает в себя информацию о количестве результатов поиска, featured snippet, карточке знаний, органических результатах и скроллируемых виджетах.

**Примеры**:

```python
>>> parser = GoogleHtmlParser('')
>>> parser.get_data()
{
    'estimated_results': 1000000,
    'featured_snippet': {'title': 'Featured Snippet Title', 'url': 'https://example.com/featured_snippet'},
    'knowledge_card': {'title': 'Knowledge Card Title', 'subtitle': 'Knowledge Card Subtitle', 'description': 'This is a description of the knowledge card.', 'more_info': [{'key1': 'value1'}, {'key2': 'value2'}]},
    'organic_results': [
        {'url': 'https://example.com/page1', 'title': 'Example Page 1', 'snippet': 'This is a description of the first page.', 'rich_snippet': None},
        {'url': 'https://example.com/page2', 'title': 'Example Page 2', 'snippet': 'This is a description of the second page.', 'rich_snippet': None},
        # ... и так далее, для каждого результата
    ],
    'scrolling_widgets': [
        {'section_title': 'Top Stories', 'section_data': [{'title': 'Story 1', 'url': 'https://example.com/story1'}, {'title': 'Story 2', 'url': 'https://example.com/story2'}]},
        {'section_title': 'Tweets', 'section_data': [{'title': 'Tweet 1', 'url': 'https://twitter.com/tweet1'}, {'title': 'Tweet 2', 'url': 'https://twitter.com/tweet2'}]}
    ]
}
```