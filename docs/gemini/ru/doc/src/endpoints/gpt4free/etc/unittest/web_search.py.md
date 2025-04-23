# Модуль тестирования веб-поиска

## Обзор

Этот модуль содержит тесты для проверки функциональности веб-поиска, используемой в проекте `hypotez`. Он использует библиотеку `duckduckgo_search` для выполнения поисковых запросов и `BeautifulSoup` для парсинга HTML-контента. Модуль предназначен для проверки интеграции веб-поиска с асинхронным клиентом `AsyncClient` и имитирует ответы провайдера `YieldProviderMock`.

## Подробней

Модуль тестирует возможность выполнения поисковых запросов с различными параметрами конфигурации, такими как максимальное количество результатов, максимальное количество слов и использование скрапинга веб-сайтов. Он также проверяет, что результаты поиска правильно интегрируются в ответы, генерируемые клиентом `AsyncClient`.

## Классы

### `TestIterListProvider`

**Описание**: Класс, содержащий асинхронные тесты для проверки функциональности веб-поиска.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Атрибуты**:

-   `has_requirements` (bool): Флаг, указывающий, установлены ли необходимые зависимости (например, `duckduckgo_search` и `BeautifulSoup`).

**Методы**:

-   `setUp()`: Подготовка к тестам, проверка наличия необходимых зависимостей.
-   `test_search()`: Тест для проверки выполнения поискового запроса с полным набором параметров.
-   `test_search2()`: Тест для проверки выполнения поискового запроса с минимальным набором параметров.
-   `test_search3()`: Тест для проверки выполнения поискового запроса с параметрами, переданными в формате JSON.

## Методы класса

### `setUp`

```python
    def setUp(self) -> None:
        """Подготовка к тестам, проверка наличия необходимых зависимостей."""
```

**Назначение**: Выполняет настройку перед каждым тестом. Проверяет, установлены ли необходимые зависимости (`duckduckgo_search` и `BeautifulSoup`). Если зависимости не установлены, тест пропускается.

**Параметры**:

-   `None`

**Возвращает**:

-   `None`

**Примеры**:

```python
    # Пример использования (внутри класса TestIterListProvider):
    def setUp(self):
        if not has_requirements:
            self.skipTest('web search requirements not passed')
```

### `test_search`

```python
    async def test_search(self):
        """Тест для проверки выполнения поискового запроса с полным набором параметров."""
```

**Назначение**: Тестирует выполнение поискового запроса с полным набором параметров, включая `query`, `max_results`, `max_words`, `backend`, `add_text`, `timeout`, `region` и `instructions`. Проверяет, что ответ содержит ожидаемый текст "Using the provided web search results".

**Параметры**:

-   `None`

**Возвращает**:

-   `None`

**Вызывает исключения**:

-   `DuckDuckGoSearchException`: Если возникает ошибка при выполнении поискового запроса.

**Как работает функция**:

1.  Создает экземпляр `AsyncClient` с имитированным провайдером `YieldProviderMock`.
2.  Определяет параметры для вызова инструмента поиска (`search_tool`), включая поисковый запрос, максимальное количество результатов, максимальное количество слов, используемый бэкенд, необходимость скрапинга веб-сайтов, таймаут, регион и инструкции.
3.  Вызывает метод `client.chat.completions.create` с передачей параметров инструмента поиска.
4.  Проверяет, содержит ли ответ ожидаемый текст "Using the provided web search results".
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

**Примеры**:

```python
    # Пример использования (внутри класса TestIterListProvider):
    async def test_search(self):
        client = AsyncClient(provider=YieldProviderMock)
        tool_calls = [
            {
                "function": {
                    "arguments": {
                        "query": "search query",
                        "max_results": 5,
                        "max_words": 500,
                        "backend": "html",
                        "add_text": True,
                        "timeout": 5,
                        "region": "wt-wt",
                        "instructions": "Using the provided web search results, to write a comprehensive reply to the user request.\n"
                                        "Make sure to add the sources of cites using [[Number]](Url) notation after the reference. Example: [[0]](http://google.com)",
                    },
                    "name": "search_tool"
                },
                "type": "function"
            }
        ]
        try:
            response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)
            self.assertIn("Using the provided web search results", response.choices[0].message.content)
        except DuckDuckGoSearchException as ex:
            self.skipTest(f'DuckDuckGoSearchException: {ex}')
```

### `test_search2`

```python
    async def test_search2(self):
        """Тест для проверки выполнения поискового запроса с минимальным набором параметров."""
```

**Назначение**: Тестирует выполнение поискового запроса с минимальным набором параметров, включающим только `query`. Проверяет, что ответ содержит ожидаемый текст "Using the provided web search results".

**Параметры**:

-   `None`

**Возвращает**:

-   `None`

**Вызывает исключения**:

-   `DuckDuckGoSearchException`: Если возникает ошибка при выполнении поискового запроса.

**Как работает функция**:

1.  Создает экземпляр `AsyncClient` с имитированным провайдером `YieldProviderMock`.
2.  Определяет параметры для вызова инструмента поиска (`search_tool`), включая только поисковый запрос.
3.  Вызывает метод `client.chat.completions.create` с передачей параметров инструмента поиска.
4.  Проверяет, содержит ли ответ ожидаемый текст "Using the provided web search results".
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

**Примеры**:

```python
    # Пример использования (внутри класса TestIterListProvider):
    async def test_search2(self):
        client = AsyncClient(provider=YieldProviderMock)
        tool_calls = [
            {
                "function": {
                    "arguments": {
                        "query": "search query",
                    },
                    "name": "search_tool"
                },
                "type": "function"
            }
        ]
        try:
            response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)
            self.assertIn("Using the provided web search results", response.choices[0].message.content)
        except DuckDuckGoSearchException as ex:
            self.skipTest(f'DuckDuckGoSearchException: {ex}')
```

### `test_search3`

```python
    async def test_search3(self):
        """Тест для проверки выполнения поискового запроса с параметрами, переданными в формате JSON."""
```

**Назначение**: Тестирует выполнение поискового запроса с параметрами, переданными в формате JSON. Проверяет, что ответ содержит ожидаемый текст "Using the provided web search results".

**Параметры**:

-   `None`

**Возвращает**:

-   `None`

**Вызывает исключения**:

-   `DuckDuckGoSearchException`: Если возникает ошибка при выполнении поискового запроса.

**Как работает функция**:

1.  Создает экземпляр `AsyncClient` с имитированным провайдером `YieldProviderMock`.
2.  Определяет параметры для вызова инструмента поиска (`search_tool`), включая поисковый запрос, максимальное количество результатов и максимальное количество слов, переданные в формате JSON.
3.  Вызывает метод `client.chat.completions.create` с передачей параметров инструмента поиска.
4.  Проверяет, содержит ли ответ ожидаемый текст "Using the provided web search results".
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

**Примеры**:

```python
    # Пример использования (внутри класса TestIterListProvider):
    async def test_search3(self):
        client = AsyncClient(provider=YieldProviderMock)
        tool_calls = [
            {
                "function": {
                    "arguments": json.dumps({
                        "query": "search query",
                        "max_results": 5,
                        "max_words": 500,
                    }),
                    "name": "search_tool"
                },
                "type": "function"
            }
        ]
        try:
            response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)
            self.assertIn("Using the provided web search results", response.choices[0].message.content)
        except DuckDuckGoSearchException as ex:
            self.skipTest(f'DuckDuckGoSearchException: {ex}')