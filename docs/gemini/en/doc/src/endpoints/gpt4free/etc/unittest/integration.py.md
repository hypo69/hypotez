## Модуль Integration Tests для gpt4free

## Обзор

Этот модуль содержит интеграционные тесты для проверки правильной работы клиента gpt4free с разными поставщиками (Copilot и DDG). Тесты проверяют, что клиент может успешно выполнить запросы к API и получить корректный ответ в формате JSON. 

## Детали

Этот модуль используется для тестирования взаимодействия клиента gpt4free с различными поставщиками, такими как Copilot и DDG.  Он проверяет, что клиент может успешно выполнять запросы к API и получать корректный ответ в формате JSON.

## Классы

### `TestProviderIntegration`

**Описание**:  Этот класс содержит тесты для проверки интеграции клиента gpt4free с поставщиками Copilot и DDG в синхронном режиме.

**Атрибуты**:

- `self`: Ссылка на текущий объект класса.

**Методы**:

- `test_bing()`: Проверка интеграции клиента gpt4free с Copilot.
- `test_openai()`: Проверка интеграции клиента gpt4free с DDG.

### `TestChatCompletionAsync`

**Описание**:  Этот класс содержит тесты для проверки интеграции клиента gpt4free с поставщиками Copilot и DDG в асинхронном режиме.

**Атрибуты**:

- `self`: Ссылка на текущий объект класса.

**Методы**:

- `test_bing()`: Проверка интеграции асинхронного клиента gpt4free с Copilot.
- `test_openai()`: Проверка интеграции асинхронного клиента gpt4free с DDG.


## Функции

## Класс-методы

### `test_bing()` 

**Purpose**: Проверка правильной работы клиента gpt4free с поставщиком Copilot в синхронном режиме.

**Parameters**:

- `self`: Ссылка на текущий объект класса.

**Returns**:

-  `None`: Функция не возвращает значения, но проводит тест.

**Raises Exceptions**:

- `AssertionError`:  Если тест не пройден, генерирует исключение `AssertionError`.

**How the Function Works**:

-  Функция создает экземпляр клиента gpt4free с поставщиком Copilot.
-  Использует метод `client.chat.completions.create()` для отправки запроса к API.
-  Проверяет, что ответ является объектом класса `ChatCompletion`.
-  Проверяет, что в полученном ответе присутствует ключ "success" в JSON-объекте.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.etc.unittest.integration import TestProviderIntegration
>>> test = TestProviderIntegration()
>>> test.test_bing() # Выполнить тест
```

### `test_openai()` 

**Purpose**: Проверка правильной работы клиента gpt4free с поставщиком DDG в синхронном режиме.

**Parameters**:

- `self`: Ссылка на текущий объект класса.

**Returns**:

-  `None`: Функция не возвращает значения, но проводит тест.

**Raises Exceptions**:

- `AssertionError`:  Если тест не пройден, генерирует исключение `AssertionError`.

**How the Function Works**:

-  Функция создает экземпляр клиента gpt4free с поставщиком DDG.
-  Использует метод `client.chat.completions.create()` для отправки запроса к API.
-  Проверяет, что ответ является объектом класса `ChatCompletion`.
-  Проверяет, что в полученном ответе присутствует ключ "success" в JSON-объекте.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.etc.unittest.integration import TestProviderIntegration
>>> test = TestProviderIntegration()
>>> test.test_openai() # Выполнить тест
```

### `test_bing()` 

**Purpose**: Проверка правильной работы асинхронного клиента gpt4free с поставщиком Copilot.

**Parameters**:

- `self`: Ссылка на текущий объект класса.

**Returns**:

-  `None`: Функция не возвращает значения, но проводит тест.

**Raises Exceptions**:

- `AssertionError`:  Если тест не пройден, генерирует исключение `AssertionError`.

**How the Function Works**:

-  Функция создает экземпляр асинхронного клиента gpt4free с поставщиком Copilot.
-  Использует метод `client.chat.completions.create()` для отправки запроса к API.
-  Проверяет, что ответ является объектом класса `ChatCompletion`.
-  Проверяет, что в полученном ответе присутствует ключ "success" в JSON-объекте.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.etc.unittest.integration import TestChatCompletionAsync
>>> test = TestChatCompletionAsync()
>>> await test.test_bing() # Выполнить тест
```


### `test_openai()` 

**Purpose**: Проверка правильной работы асинхронного клиента gpt4free с поставщиком DDG.

**Parameters**:

- `self`: Ссылка на текущий объект класса.

**Returns**:

-  `None`: Функция не возвращает значения, но проводит тест.

**Raises Exceptions**:

- `AssertionError`:  Если тест не пройден, генерирует исключение `AssertionError`.

**How the Function Works**:

-  Функция создает экземпляр асинхронного клиента gpt4free с поставщиком DDG.
-  Использует метод `client.chat.completions.create()` для отправки запроса к API.
-  Проверяет, что ответ является объектом класса `ChatCompletion`.
-  Проверяет, что в полученном ответе присутствует ключ "success" в JSON-объекте.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.etc.unittest.integration import TestChatCompletionAsync
>>> test = TestChatCompletionAsync()
>>> await test.test_openai() # Выполнить тест
```