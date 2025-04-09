# Модуль для модульного тестирования веб-поиска

## Обзор

Этот модуль содержит набор тестов для проверки функциональности веб-поиска, используемого в проекте `hypotez`. Он использует `unittest` для организации и выполнения тестов, а также `duckduckgo_search` для выполнения веб-поиска.

## Подробнее

Модуль проверяет интеграцию веб-поиска с `AsyncClient` и убеждается, что результаты поиска правильно включаются в ответы. Если необходимые зависимости для веб-поиска не установлены, тесты пропускаются. В случае возникновения исключений при выполнении веб-поиска, тесты также пропускаются.

## Классы

### `TestIterListProvider`

**Описание**: Класс `TestIterListProvider` предназначен для модульного тестирования функциональности веб-поиска.

**Наследует**:
- `unittest.IsolatedAsyncioTestCase`: Наследует от этого класса для создания асинхронных тестов.

**Атрибуты**:
- `has_requirements` (bool): Указывает, установлены ли все необходимые зависимости для веб-поиска.

**Методы**:
- `setUp()`: Настраивает тестовую среду, проверяя наличие необходимых зависимостей.
- `test_search()`: Проверяет выполнение веб-поиска с полным набором параметров.
- `test_search2()`: Проверяет выполнение веб-поиска с минимальным набором параметров.
- `test_search3()`: Проверяет выполнение веб-поиска с параметрами, переданными в формате JSON.

## Функции

### `setUp`

```python
def setUp(self) -> None:
    """
    Настраивает тестовую среду перед выполнением каждого теста.

    Args:
        self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        unittest.SkipTest: Если не установлены необходимые зависимости для веб-поиска.

    Как работает функция:
    1. Проверяет, установлены ли все необходимые зависимости для веб-поиска.
    2. Если зависимости не установлены, тест пропускается.
    """
```

**Как работает функция**:

1.  Функция `setUp` проверяет, установлены ли все необходимые зависимости для веб-поиска, такие как `duckduckgo_search` и `BeautifulSoup`.
2.  Если хотя бы одна из зависимостей не установлена, вызывается `self.skipTest()`, что приводит к пропуску всех тестов в классе.

```
Проверка зависимостей
    │
    └──→ Зависимости установлены?
         │
         ├──→ Да: Завершение
         │
         └──→ Нет: Пропуск тестов
```

### `test_search`

```python
async def test_search(self):
    """
    Проверяет выполнение веб-поиска с полным набором параметров.

    Args:
        self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        unittest.SkipTest: Если возникает исключение `DuckDuckGoSearchException` при выполнении веб-поиска.

    Как работает функция:
    1. Создает экземпляр `AsyncClient` с мок-провайдером.
    2. Определяет параметры для веб-поиска, включая запрос, максимальное количество результатов, максимальное количество слов, бэкенд, флаг добавления текста, таймаут, регион и инструкции.
    3. Вызывает метод `client.chat.completions.create` с параметрами веб-поиска.
    4. Проверяет, содержит ли ответ строку "Using the provided web search results".
    5. Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.
    """
```

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с мок-провайдером (`YieldProviderMock`).
2.  Определяются параметры для веб-поиска, такие как запрос, максимальное количество результатов, максимальное количество слов и другие.
3.  Вызывается метод `client.chat.completions.create` с параметрами веб-поиска.
4.  Проверяется, содержит ли ответ строку "Using the provided web search results", чтобы убедиться, что результаты поиска были включены в ответ.
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

```
Создание клиента
    │
    └──→ Определение параметров поиска
         │
         └──→ Вызов chat.completions.create
              │
              └──→ Проверка наличия строки "Using the provided web search results" в ответе
                   │
                   ├──→ Строка найдена: Завершение
                   │
                   └──→ Строка не найдена: Ошибка
```

### `test_search2`

```python
async def test_search2(self):
    """
    Проверяет выполнение веб-поиска с минимальным набором параметров.

    Args:
        self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        unittest.SkipTest: Если возникает исключение `DuckDuckGoSearchException` при выполнении веб-поиска.

    Как работает функция:
    1. Создает экземпляр `AsyncClient` с мок-провайдером.
    2. Определяет минимальные параметры для веб-поиска, включая только запрос.
    3. Вызывает метод `client.chat.completions.create` с параметрами веб-поиска.
    4. Проверяет, содержит ли ответ строку "Using the provided web search results".
    5. Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.
    """
```

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с мок-провайдером (`YieldProviderMock`).
2.  Определяются минимальные параметры для веб-поиска, включая только запрос.
3.  Вызывается метод `client.chat.completions.create` с параметрами веб-поиска.
4.  Проверяется, содержит ли ответ строку "Using the provided web search results", чтобы убедиться, что результаты поиска были включены в ответ.
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

```
Создание клиента
    │
    └──→ Определение параметров поиска (минимальный набор)
         │
         └──→ Вызов chat.completions.create
              │
              └──→ Проверка наличия строки "Using the provided web search results" в ответе
                   │
                   ├──→ Строка найдена: Завершение
                   │
                   └──→ Строка не найдена: Ошибка
```

### `test_search3`

```python
async def test_search3(self):
    """
    Проверяет выполнение веб-поиска с параметрами, переданными в формате JSON.

    Args:
        self (TestIterListProvider): Экземпляр класса `TestIterListProvider`.

    Returns:
        None

    Raises:
        unittest.SkipTest: Если возникает исключение `DuckDuckGoSearchException` при выполнении веб-поиска.

    Как работает функция:
    1. Создает экземпляр `AsyncClient` с мок-провайдером.
    2. Определяет параметры для веб-поиска в формате JSON, включая запрос, максимальное количество результатов и максимальное количество слов.
    3. Вызывает метод `client.chat.completions.create` с параметрами веб-поиска.
    4. Проверяет, содержит ли ответ строку "Using the provided web search results".
    5. Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.
    """
```

**Как работает функция**:

1.  Создается экземпляр `AsyncClient` с мок-провайдером (`YieldProviderMock`).
2.  Определяются параметры для веб-поиска в формате JSON, такие как запрос, максимальное количество результатов и максимальное количество слов.
3.  Вызывается метод `client.chat.completions.create` с параметрами веб-поиска.
4.  Проверяется, содержит ли ответ строку "Using the provided web search results", чтобы убедиться, что результаты поиска были включены в ответ.
5.  Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

```
Создание клиента
    │
    └──→ Определение параметров поиска в формате JSON
         │
         └──→ Вызов chat.completions.create
              │
              └──→ Проверка наличия строки "Using the provided web search results" в ответе
                   │
                   ├──→ Строка найдена: Завершение
                   │
                   └──→ Строка не найдена: Ошибка
```

**Примеры**:

```python
import unittest
from unittest.mock import MagicMock
from duckduckgo_search import DDGS
from g4f.client import AsyncClient

# Мок для DuckDuckGoSearchException
class MockDuckDuckGoSearchException(Exception):
    pass

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_search_success(self):
        # Мокируем DDGS и AsyncClient
        ddgs_mock = MagicMock()
        ddgs_mock.text.return_value = [{"body": "test"}]
        
        async_client_mock = MagicMock()
        async_client_mock.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="Using the provided web search results"))])

        # Подменяем DDGS и AsyncClient
        import sys
        sys.modules['duckduckgo_search'] = MagicMock(DDGS=lambda *args, **kwargs: ddgs_mock)
        from g4f.client import AsyncClient  # Re-import чтобы использовать моки
        
        client = AsyncClient(provider=MagicMock())
        client.chat.completions = async_client_mock.chat.completions

        tool_calls = [{
            "function": {
                "arguments": {"query": "search query"},
                "name": "search_tool"
            },
            "type": "function"
        }]
        
        response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)
        self.assertIn("Using the provided web search results", response.choices[0].message.content)

    async def test_search_ddg_exception(self):
        # Мокируем DuckDuckGoSearchException
        ddgs_mock = MagicMock()
        ddgs_mock.text.side_effect = MockDuckDuckGoSearchException("Search failed")

        # Подменяем DDGS
        import sys
        sys.modules['duckduckgo_search'] = MagicMock(DDGS=lambda *args, **kwargs: ddgs_mock)
        from g4f.client import AsyncClient  # Re-import чтобы использовать моки
        
        client = AsyncClient(provider=MagicMock())

        tool_calls = [{
            "function": {
                "arguments": {"query": "search query"},
                "name": "search_tool"
            },
            "type": "function"
        }]
        
        with self.assertRaises(MockDuckDuckGoSearchException):
            await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)

if __name__ == '__main__':
    unittest.main()