### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код содержит набор интеграционных тестов для проверки работоспособности различных провайдеров (Copilot, DDG) с использованием как синхронного, так и асинхронного клиентов. Он проверяет, что провайдеры могут правильно формировать ответы в формате JSON и возвращать ожидаемые данные.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `unittest`, `json`, а также классы `Client`, `AsyncClient`, `ChatCompletion` и провайдеры `Copilot`, `DDG` из библиотеки `g4f`.

2. **Определение тестовых данных**:
   - Определяется константа `DEFAULT_MESSAGES`, содержащая список сообщений для отправки провайдерам. Эти сообщения указывают провайдеру вернуть ответ в формате JSON с полем "success".

3. **Создание класса для синхронных тестов**:
   - Создается класс `TestProviderIntegration`, наследующийся от `unittest.TestCase`, для выполнения синхронных тестов.

4. **Создание синхронного теста для Bing (Copilot)**:
   - В методе `test_bing` создается синхронный клиент `Client` с провайдером `Copilot`.
   - Отправляется запрос `chat.completions.create` с предопределенными сообщениями и указанием формата ответа "json_object".
   - Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
   - Проверяется, что ответ содержит поле "success" после его десериализации из JSON.

5. **Создание синхронного теста для OpenAI (DDG)**:
   - В методе `test_openai` создается синхронный клиент `Client` с провайдером `DDG`.
   - Отправляется запрос `chat.completions.create` с предопределенными сообщениями и указанием формата ответа "json_object".
   - Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
   - Проверяется, что ответ содержит поле "success" после его десериализации из JSON.

6. **Создание класса для асинхронных тестов**:
   - Создается класс `TestChatCompletionAsync`, наследующийся от `unittest.IsolatedAsyncioTestCase`, для выполнения асинхронных тестов.

7. **Создание асинхронного теста для Bing (Copilot)**:
   - В методе `test_bing` создается асинхронный клиент `AsyncClient` с провайдером `Copilot`.
   - Отправляется асинхронный запрос `chat.completions.create` с предопределенными сообщениями и указанием формата ответа "json_object".
   - Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
   - Проверяется, что ответ содержит поле "success" после его десериализации из JSON.

8. **Создание асинхронного теста для OpenAI (DDG)**:
   - В методе `test_openai` создается асинхронный клиент `AsyncClient` с провайдером `DDG`.
   - Отправляется асинхронный запрос `chat.completions.create` с предопределенными сообщениями и указанием формата ответа "json_object".
   - Проверяется, что полученный ответ является экземпляром класса `ChatCompletion`.
   - Проверяется, что ответ содержит поле "success" после его десериализации из JSON.

9. **Запуск тестов**:
   - В блоке `if __name__ == '__main__':` вызывается `unittest.main()` для запуска всех определенных тестов.

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