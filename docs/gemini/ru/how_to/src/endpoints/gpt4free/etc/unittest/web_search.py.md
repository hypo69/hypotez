### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит модульные тесты для проверки функциональности поиска в веб-среде с использованием библиотеки `duckduckgo_search` и асинхронного клиента `AsyncClient`. Тесты проверяют, что поисковые запросы выполняются корректно и результаты поиска используются для генерации ответов.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `json`, `unittest`.
   - Из `duckduckgo_search` импортируются `DDGS` и `DuckDuckGoSearchException`.
   - Из `bs4` импортируется `BeautifulSoup`.
   - Из `g4f.client` импортируется `AsyncClient`.
   - Из `.mocks` импортируется `YieldProviderMock`.

2. **Определение класса тестов `TestIterListProvider`**:
   - Класс наследуется от `unittest.IsolatedAsyncioTestCase` для выполнения асинхронных тестов.
   - Определяется метод `setUp`, который проверяет наличие необходимых зависимостей (`has_requirements`). Если зависимости не установлены, тест пропускается.

3. **Тест `test_search`**:
   - Инициализируется `AsyncClient` с использованием `YieldProviderMock`.
   - Определяется структура `tool_calls`, содержащая параметры для поискового инструмента (`search_tool`), такие как `query`, `max_results`, `max_words`, `backend`, `add_text`, `timeout`, `region` и `instructions`.
   - Вызывается метод `client.chat.completions.create` с передачей структуры `tool_calls`.
   - Проверяется, что ответ содержит фразу "Using the provided web search results".
   - Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

4. **Тест `test_search2`**:
   - Аналогичен `test_search`, но содержит минимальный набор параметров для поискового инструмента (`search_tool`), ограничиваясь только параметром `query`.
   - Вызывается метод `client.chat.completions.create` с передачей структуры `tool_calls`.
   - Проверяется, что ответ содержит фразу "Using the provided web search results".
   - Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

5. **Тест `test_search3`**:
   - Аналогичен `test_search`, но параметры для поискового инструмента (`search_tool`) передаются в формате JSON.
   - Вызывается метод `client.chat.completions.create` с передачей структуры `tool_calls`.
   - Проверяется, что ответ содержит фразу "Using the provided web search results".
   - Если возникает исключение `DuckDuckGoSearchException`, тест пропускается.

Пример использования
-------------------------

```python
import unittest
from g4f.client import AsyncClient
from .mocks import YieldProviderMock

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):
    async def test_search(self):
        client = AsyncClient(provider=YieldProviderMock)
        tool_calls = [
            {
                "function": {
                    "arguments": {
                        "query": "search query",
                        "max_results": 5,
                    },
                    "name": "search_tool"
                },
                "type": "function"
            }
        ]
        try:
            response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)
            self.assertIn("Using the provided web search results", response.choices[0].message.content)
        except Exception as e:
            self.skipTest(f'Exception: {e}')