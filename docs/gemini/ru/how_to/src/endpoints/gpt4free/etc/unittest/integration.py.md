## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода представляет собой набор интеграционных тестов для проверки функциональности класса `Client` и `AsyncClient` из библиотеки `g4f`. Тесты проверяют, что объекты `ChatCompletion` создаются корректно и возвращают правильный ответ в формате JSON.

Шаги выполнения
-------------------------
1. **Инициализация клиента:** Создается объект `Client` или `AsyncClient` с использованием провайдера `Copilot` (Bing) или `DDG` (OpenAI).
2. **Создание запроса:** Вызывается метод `chat.completions.create` для создания запроса к API чат-бота. В качестве аргументов передаются список сообщений `DEFAULT_MESSAGES`, пустая строка (как запрос) и формат ответа `response_format` (JSON).
3. **Проверка типа ответа:** Проверяется, что полученный ответ имеет тип `ChatCompletion`.
4. **Проверка содержимого ответа:** Извлекается содержимое ответа в формате JSON и проверяется наличие ключа "success".

Пример использования
-------------------------

```python
import unittest
import json

from g4f.client import Client, AsyncClient, ChatCompletion
from g4f.Provider import Copilot, DDG

DEFAULT_MESSAGES = [{"role": "system", "content": 'Response in json, Example: {"success": false}'},
                    {"role": "user", "content": "Say success true in json"}]

class TestProviderIntegration(unittest.TestCase):

    def test_bing(self):
        client = Client(provider=Copilot)
        response = client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))

    def test_openai(self):
        client = Client(provider=DDG)
        response = client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))

class TestChatCompletionAsync(unittest.IsolatedAsyncioTestCase):

    async def test_bing(self):
        client = AsyncClient(provider=Copilot)
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))

    async def test_openai(self):
        client = AsyncClient(provider=DDG)
        response = await client.chat.completions.create(DEFAULT_MESSAGES, "", response_format={"type": "json_object"})
        self.assertIsInstance(response, ChatCompletion)
        self.assertIn("success", json.loads(response.choices[0].message.content))

if __name__ == '__main__':
    unittest.main()
```