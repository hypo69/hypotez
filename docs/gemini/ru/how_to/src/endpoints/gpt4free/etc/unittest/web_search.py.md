## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой набор тестов для проверки работы инструмента `search_tool`, который выполняет веб-поиск с помощью `DuckDuckGo`. 

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
    -  `json` - для работы с JSON-форматом.
    -  `unittest` - для проведения юнит-тестов.
    -  `duckduckgo_search` - для поиска по DuckDuckGo.
    -  `bs4` - для парсинга HTML-кода.
    -  `g4f.client` - для использования клиента GPT-4.
    -  `YieldProviderMock` - мок для имитации провайдера данных.
2. **Определение тестового класса:**
    - Создается класс `TestIterListProvider`, который наследуется от `unittest.IsolatedAsyncioTestCase`.
    - Класс содержит три асинхронных тестовых метода: `test_search`, `test_search2`, `test_search3`.
3. **Проведение тестов**:
    - В каждом методе создается экземпляр клиента `AsyncClient` с использованием `YieldProviderMock` для имитации провайдера данных.
    - Создается список инструментов `tool_calls`, который содержит `search_tool`.
    - `search_tool` принимает различные аргументы для веб-поиска:
        - `query`: текст запроса.
        - `max_results`: максимальное количество результатов поиска.
        - `max_words`: максимальное количество слов, используемых из результатов поиска.
        - `backend`: тип бекенда DuckDuckGo (html, lite, api).
        - `add_text`: включение/отключение соскабливания веб-сайтов.
        - `timeout`: время ожидания для соскабливания веб-сайтов.
        - `region`: регион поиска.
        - `instructions`: инструкции для GPT-4 по использованию результатов поиска.
    - Используя метод `client.chat.completions.create`, выполняются запросы к GPT-4 с использованием `tool_calls`.
    - Проверяется наличие ожидаемого текста (`Using the provided web search results`) в ответе от GPT-4.
    - В случае возникновения ошибки `DuckDuckGoSearchException`, тест пропускается.

Пример использования
-------------------------

```python
# Пример использования search_tool
tool_calls = [
    {
        "function": {
            "arguments": {
                "query": "What is the capital of France?",
                "max_results": 5,
                "backend": "html",
                "add_text": True,
            },
            "name": "search_tool"
        },
        "type": "function"
    }
]

# Выполнение запроса к GPT-4 с использованием search_tool
response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)

# Вывод ответа
print(response.choices[0].message.content)
```