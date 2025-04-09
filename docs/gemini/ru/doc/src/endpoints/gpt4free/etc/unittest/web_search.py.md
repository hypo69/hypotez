# Модуль для тестирования веб-поиска

## Обзор

Этот модуль содержит юнит-тесты для проверки функциональности веб-поиска, используемой в проекте `hypotez`. Он проверяет интеграцию с поисковой системой DuckDuckGo и асинхронным клиентом `g4f`.

## Подробнее

Модуль `web_search.py` предназначен для автоматизированного тестирования возможностей веб-поиска в рамках проекта `hypotez`. Он включает в себя тесты для проверки правильности выполнения поисковых запросов и обработки результатов.

Модуль использует библиотеку `duckduckgo_search` для выполнения поисковых запросов и `BeautifulSoup` для парсинга HTML-контента, полученного из результатов поиска. Также, он использует `AsyncClient` из библиотеки `g4f` для асинхронного взаимодействия с веб-сервисами.

## Классы

### `TestIterListProvider`

**Описание**: Класс, представляющий собой набор асинхронных юнит-тестов для проверки функциональности веб-поиска.

**Наследует**: `unittest.IsolatedAsyncioTestCase`

**Методы**:

- `setUp()`: Подготавливает тестовое окружение перед каждым тестом. Проверяет наличие необходимых зависимостей (библиотек) и пропускает тест, если они не установлены.
- `test_search()`: Проверяет выполнение поискового запроса с указанием дополнительных параметров, таких как `max_results`, `max_words`, `backend`, `add_text`, `timeout` и `region`.
- `test_search2()`: Проверяет выполнение поискового запроса с минимальным набором параметров (только `query`).
- `test_search3()`: Проверяет выполнение поискового запроса с передачей параметров в формате JSON.

## Функции

### `setUp`

```python
    def setUp(self) -> None:
        """Подготавливает тестовое окружение перед каждым тестом.
        Проверяет наличие необходимых зависимостей (библиотек) и пропускает тест, если они не установлены.

        Args:
            None

        Returns:
            None

        Raises:
            unittest.SkipTest: Если необходимые зависимости не установлены.
        """
```

**Назначение**: Настройка тестового окружения перед выполнением каждого теста.

**Как работает функция**:

1.  Проверяет, установлены ли необходимые библиотеки (`duckduckgo_search`, `bs4`).
2.  Если хотя бы одна из библиотек отсутствует, тест пропускается с сообщением об отсутствии необходимых зависимостей.

**Примеры**:

```python
# Пример использования (внутри класса TestIterListProvider):
class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        if not has_requirements:
            self.skipTest('web search requirements not passed')
```

### `test_search`

```python
    async def test_search(self):
        """Проверяет выполнение поискового запроса с указанием дополнительных параметров.
        Проверяет, что ответ содержит ожидаемую строку "Using the provided web search results".

        Args:
            None

        Returns:
            None

        Raises:
            unittest.SkipTest: Если возникает исключение `DuckDuckGoSearchException`.
        """
```

**Назначение**: Проверка выполнения поискового запроса с полным набором параметров и анализ результата.

**Как работает функция**:

1.  Создает экземпляр `AsyncClient` с моковым провайдером (`YieldProviderMock`).
2.  Определяет параметры поискового запроса в виде `tool_calls`, включая `query`, `max_results`, `max_words`, `backend`, `add_text`, `timeout`, `region` и `instructions`.
3.  Выполняет поисковый запрос с использованием `client.chat.completions.create`.
4.  Проверяет, содержит ли ответ ожидаемую строку "Using the provided web search results".
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

```
    Начало теста
    │
    Создание AsyncClient с YieldProviderMock
    │
    Определение параметров поискового запроса (tool_calls)
    │
    Попытка выполнения поискового запроса с помощью client.chat.completions.create
    │
    Успех: Проверка наличия "Using the provided web search results" в ответе
    │
    Ошибка: Пропуск теста, если DuckDuckGoSearchException
    │
    Конец теста
```

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
    except DuckDuckGoSearchException as e:
        self.skipTest(f'DuckDuckGoSearchException: {e}')
```

### `test_search2`

```python
    async def test_search2(self):
        """Проверяет выполнение поискового запроса с минимальным набором параметров (только `query`).
        Проверяет, что ответ содержит ожидаемую строку "Using the provided web search results".

        Args:
            None

        Returns:
            None

        Raises:
            unittest.SkipTest: Если возникает исключение `DuckDuckGoSearchException`.
        """
```

**Назначение**: Проверка выполнения поискового запроса с минимальным набором параметров (только `query`).

**Как работает функция**:

1.  Создает экземпляр `AsyncClient` с моковым провайдером (`YieldProviderMock`).
2.  Определяет параметры поискового запроса в виде `tool_calls`, содержащего только параметр `query`.
3.  Выполняет поисковый запрос с использованием `client.chat.completions.create`.
4.  Проверяет, содержит ли ответ ожидаемую строку "Using the provided web search results".
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

```
    Начало теста
    │
    Создание AsyncClient с YieldProviderMock
    │
    Определение параметров поискового запроса (tool_calls) с минимальным набором параметров
    │
    Попытка выполнения поискового запроса с помощью client.chat.completions.create
    │
    Успех: Проверка наличия "Using the provided web search results" в ответе
    │
    Ошибка: Пропуск теста, если DuckDuckGoSearchException
    │
    Конец теста
```

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
    except DuckDuckGoSearchException as e:
        self.skipTest(f'DuckDuckGoSearchException: {e}')
```

### `test_search3`

```python
    async def test_search3(self):
        """Проверяет выполнение поискового запроса с передачей параметров в формате JSON.
        Проверяет, что ответ содержит ожидаемую строку "Using the provided web search results".

        Args:
            None

        Returns:
            None

        Raises:
            unittest.SkipTest: Если возникает исключение `DuckDuckGoSearchException`.
        """
```

**Назначение**: Проверка выполнения поискового запроса с параметрами, переданными в формате JSON.

**Как работает функция**:

1.  Создает экземпляр `AsyncClient` с моковым провайдером (`YieldProviderMock`).
2.  Определяет параметры поискового запроса в виде JSON-строки, содержащей `query`, `max_results` и `max_words`.
3.  Выполняет поисковый запрос с использованием `client.chat.completions.create`.
4.  Проверяет, содержит ли ответ ожидаемую строку "Using the provided web search results".
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

```
    Начало теста
    │
    Создание AsyncClient с YieldProviderMock
    │
    Определение параметров поискового запроса (tool_calls) в формате JSON
    │
    Попытка выполнения поискового запроса с помощью client.chat.completions.create
    │
    Успех: Проверка наличия "Using the provided web search results" в ответе
    │
    Ошибка: Пропуск теста, если DuckDuckGoSearchException
    │
    Конец теста
```

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
    except DuckDuckGoSearchException as e:
        self.skipTest(f'DuckDuckGoSearchException: {e}')