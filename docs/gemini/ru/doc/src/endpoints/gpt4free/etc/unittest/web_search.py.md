# Модуль для тестирования веб-поиска

## Обзор

Этот модуль содержит юнит-тесты для проверки функциональности веб-поиска, используемого в проекте `hypotez`. Он проверяет интеграцию асинхронного клиента с различными параметрами поиска и обрабатывает исключения, связанные с поисковой системой DuckDuckGo.

## Подробней

Этот модуль содержит набор тестов, проверяющих функциональность веб-поиска. Здесь проверяется корректность обработки поисковых запросов, параметров поиска (таких как `max_results`, `max_words`, `backend` и `add_text`) и интеграцию с асинхронным клиентом. Модуль использует моки для имитации ответов провайдера и проверяет, что результаты поиска правильно включаются в ответ. Тесты также обрабатывают исключения, возникающие при использовании DuckDuckGo Search.

## Классы

### `TestIterListProvider`

**Описание**: Класс, содержащий асинхронные юнит-тесты для проверки функциональности веб-поиска.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Атрибуты**:
- `has_requirements` (bool): Флаг, указывающий, установлены ли необходимые зависимости для веб-поиска.

**Методы**:
- `setUp()`: Подготовка к тестам, проверяет наличие необходимых зависимостей.
- `test_search()`: Тест для проверки базовой функциональности поиска с различными параметрами.
- `test_search2()`: Тест для проверки поиска с минимальным набором параметров.
- `test_search3()`: Тест для проверки поиска с параметрами, переданными в формате JSON.

## Методы класса

### `setUp`

```python
    def setUp(self) -> None:
        if not has_requirements:
            self.skipTest(\'web search requirements not passed\')
```

**Назначение**: Метод подготовки к тестам. Проверяет, установлены ли необходимые зависимости для веб-поиска. Если зависимости не установлены, тест пропускается.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Как работает функция**:
- Функция проверяет, установлены ли необходимые зависимости для веб-поиска, используя флаг `has_requirements`.
- Если зависимости не установлены, вызывается метод `self.skipTest()` для пропуска теста.

**Примеры**:
```python
# Пример использования внутри класса TestIterListProvider
class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        if not has_requirements:
            self.skipTest('web search requirements not passed')
```

### `test_search`

```python
    async def test_search(self):
        client = AsyncClient(provider=YieldProviderMock)
        tool_calls = [
            {
                "function": {
                    "arguments": {
                        "query": "search query", # content of last message: messages[-1]["content"]
                        "max_results": 5, # maximum number of search results
                        "max_words": 500, # maximum number of used words from search results for generating the response
                        "backend": "html", # or "lite", "api": change it to pypass rate limits
                        "add_text": True, # do scraping websites
                        "timeout": 5, # in seconds for scraping websites
                        "region": "wt-wt",
                        "instructions": "Using the provided web search results, to write a comprehensive reply to the user request.\\n"\
                                        "Make sure to add the sources of cites using [[Number]](Url) notation after the reference. Example: [[0]](http://google.com)",
                    },
                    "name": "search_tool"\
                },\
                "type": "function"\
            }\
        ]\
        try:\
            response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)\
            self.assertIn("Using the provided web search results", response.choices[0].message.content)\
        except DuckDuckGoSearchException as e:\
            self.skipTest(f\'DuckDuckGoSearchException: {e}\')
```

**Назначение**: Асинхронный тест для проверки базовой функциональности поиска с различными параметрами.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Вызывает исключения**:
- `DuckDuckGoSearchException`: Если возникает ошибка при выполнении поиска через DuckDuckGo.

**Как работает функция**:
1. Создает экземпляр `AsyncClient` с моковым провайдером `YieldProviderMock`.
2. Определяет структуру `tool_calls`, содержащую параметры поиска, такие как запрос, максимальное количество результатов, максимальное количество слов, бэкенд, флаг добавления текста, таймаут, регион и инструкции.
3. Вызывает метод `client.chat.completions.create()` для выполнения поискового запроса.
4. Проверяет, что ответ содержит ожидаемый текст "Using the provided web search results".
5. Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

**Примеры**:
```python
# Пример использования внутри класса TestIterListProvider
class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
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
                        "instructions": "Using the provided web search results, to write a comprehensive reply to the user request.\\n"\
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
        except DuckDuckGoSearchException as e:
            self.skipTest(f'DuckDuckGoSearchException: {e}')
```

### `test_search2`

```python
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
        ]\
        try:\
            response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)\
            self.assertIn("Using the provided web search results", response.choices[0].message.content)\
        except DuckDuckGoSearchException as e:\
            self.skipTest(f\'DuckDuckGoSearchException: {e}\')
```

**Назначение**: Асинхронный тест для проверки поиска с минимальным набором параметров.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Вызывает исключения**:
- `DuckDuckGoSearchException`: Если возникает ошибка при выполнении поиска через DuckDuckGo.

**Как работает функция**:
1. Создает экземпляр `AsyncClient` с моковым провайдером `YieldProviderMock`.
2. Определяет структуру `tool_calls`, содержащую только параметр запроса.
3. Вызывает метод `client.chat.completions.create()` для выполнения поискового запроса.
4. Проверяет, что ответ содержит ожидаемый текст "Using the provided web search results".
5. Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

**Примеры**:
```python
# Пример использования внутри класса TestIterListProvider
class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
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
        except DuckDuckGoSearchException as e:
            self.skipTest(f'DuckDuckGoSearchException: {e}')
```

### `test_search3`

```python
    async def test_search3(self):
        client = AsyncClient(provider=YieldProviderMock)
        tool_calls = [
            {
                "function": {
                    "arguments": json.dumps({\
                        "query": "search query", # content of last message: messages[-1]["content"]
                        "max_results": 5, # maximum number of search results
                        "max_words": 500, # maximum number of used words from search results for generating the response
                    }),\
                    "name": "search_tool"\
                },\
                "type": "function"\
            }\
        ]\
        try:\
            response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)\
            self.assertIn("Using the provided web search results", response.choices[0].message.content)\
        except DuckDuckGoSearchException as e:\
            self.skipTest(f\'DuckDuckGoSearchException: {e}\')
```

**Назначение**: Асинхронный тест для проверки поиска с параметрами, переданными в формате JSON.

**Параметры**:
- Нет

**Возвращает**:
- `None`

**Вызывает исключения**:
- `DuckDuckGoSearchException`: Если возникает ошибка при выполнении поиска через DuckDuckGo.

**Как работает функция**:
1. Создает экземпляр `AsyncClient` с моковым провайдером `YieldProviderMock`.
2. Определяет структуру `tool_calls`, содержащую параметры поиска в формате JSON.
3. Вызывает метод `client.chat.completions.create()` для выполнения поискового запроса.
4. Проверяет, что ответ содержит ожидаемый текст "Using the provided web search results".
5. Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

**Примеры**:
```python
# Пример использования внутри класса TestIterListProvider
class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
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
        except DuckDuckGoSearchException as e:
            self.skipTest(f'DuckDuckGoSearchException: {e}')
```

## Параметры класса

- `has_requirements` (bool): Флаг, указывающий, установлены ли необходимые зависимости для веб-поиска.

## Методы
- `setUp()`: Проверяет наличие необходимых зависимостей.
- `test_search()`: Проверяет базовую функциональность поиска с различными параметрами.
- `test_search2()`: Проверяет поиск с минимальным набором параметров.
- `test_search3()`: Проверяет поиск с параметрами, переданными в формате JSON.