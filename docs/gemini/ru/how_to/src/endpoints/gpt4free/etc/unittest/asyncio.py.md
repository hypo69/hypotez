## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода содержит набор юнит-тестов для класса `ChatCompletion` из модуля `g4f`. Он проверяет корректность работы функций `create`, `create_async` и `create_generator` в различных сценариях, включая работу с асинхронным кодом и использование библиотеки `nest_asyncio`.

Шаги выполнения
-------------------------
1. **Проверка наличия `nest_asyncio`**: Проверяется наличие библиотеки `nest_asyncio` в среде. Если библиотека не доступна, тесты, использующие ее, пропускаются.
2. **Инициализация `ChatCompletion`**: В тестах создаются экземпляры класса `ChatCompletion` с использованием различных типов провайдеров (синхронный, асинхронный, асинхронный с использованием генератора).
3. **Проверка исключений**: Тест `test_exception` проверяет, что в случае отсутствия `nest_asyncio` при вызове функции `create` с асинхронным провайдером возникает исключение `g4f.errors.NestAsyncioError`.
4. **Проверка корректности возвращаемого значения**: Тесты `test_create`, `test_create_generator`, `test_base`, `test_async`, `test_create_generator` и `test_create` проверяют, что функции `create`, `create_async` и `create_generator` возвращают ожидаемые значения, которые в данном случае - строка "Mock".
5. **Проверка асинхронных функций**: В тестах `test_await_callback`, `test_base`, `test_async`, `test_create_generator` и `test_create` проверяется корректность работы функций `create_async`, `create_generator` и `create` при использовании асинхронных провайдеров.
6. **Проверка работы с `nest_asyncio`**: Тесты `test_create` и `_test_nested` проверяют работу функций `create` и `create_async` при использовании асинхронных провайдеров с включенным `nest_asyncio`.

Пример использования
-------------------------

```python
import unittest
import asyncio

import g4f
from g4f import ChatCompletion
from g4f.client import Client
from .mocks import ProviderMock, AsyncProviderMock, AsyncGeneratorProviderMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class TestChatCompletion(unittest.TestCase):

    async def run_exception(self):
        return ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncProviderMock)

    def test_exception(self):
        # Проверяем, что исключение `NestAsyncioError` возникает, если `nest_asyncio` не установлен
        self.assertRaises(g4f.errors.NestAsyncioError, asyncio.run, self.run_exception())

    def test_create(self):
        # Проверяем корректность работы функции `create` с синхронным провайдером
        result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, ProviderMock)
        self.assertEqual("Mock", result)

    def test_create_generator(self):
        # Проверяем корректность работы функции `create` с асинхронным провайдером с использованием генератора
        result = ChatCompletion.create(g4f.models.default, DEFAULT_MESSAGES, AsyncGeneratorProviderMock)
        self.assertEqual("Mock", result)

    def test_await_callback(self):
        # Проверяем корректность работы функции `create` в асинхронном режиме
        client = Client(provider=AsyncGeneratorProviderMock)
        response = client.chat.completions.create(DEFAULT_MESSAGES, "", max_tokens=0)
        self.assertEqual("Mock", response.choices[0].message.content)

if __name__ == '__main__':
    unittest.main()
```