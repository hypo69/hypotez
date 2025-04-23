### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор юнит-тестов для проверки функциональности `AsyncClient` при работе с различными провайдерами изображений, включая обработку ошибок, пропуск неработающих провайдеров и корректную обработку ответов.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `asyncio`, `unittest`, `AsyncClient`, `ImagesResponse` и различные моки провайдеров (`YieldImageResponseProviderMock`, `MissingAuthProviderMock`, `AsyncRaiseExceptionProviderMock`, `YieldNoneProviderMock`).
2. **Определение константы**: Определяется константа `DEFAULT_MESSAGES` для использования в тестах.
3. **Создание тестового класса**: Создается класс `TestIterListProvider`, наследующийся от `unittest.IsolatedAsyncioTestCase`, который позволяет запускать асинхронные тесты.
4. **Тест `test_skip_provider`**:
   - Инициализируется `AsyncClient` с `IterListProvider`, который содержит `MissingAuthProviderMock` (мокирующий отсутствующую авторизацию) и `YieldImageResponseProviderMock` (мокирующий успешный ответ).
   - Вызывается `client.images.generate` для генерации изображения.
   - Проверяется, что полученный ответ является экземпляром `ImagesResponse` и что URL первого изображения в ответе равен "Hello". Это показывает, что тест успешно пропустил `MissingAuthProviderMock` и использовал `YieldImageResponseProviderMock`.
5. **Тест `test_only_one_result`**:
   - Инициализируется `AsyncClient` с `IterListProvider`, который содержит два `YieldImageResponseProviderMock`.
   - Вызывается `client.images.generate` для генерации изображения.
   - Проверяется, что полученный ответ является экземпляром `ImagesResponse` и что URL первого изображения в ответе равен "Hello". Это показывает, что клиент берет результат только из первого успешного провайдера.
6. **Тест `test_skip_none`**:
   - Инициализируется `AsyncClient` с `IterListProvider`, который содержит `YieldNoneProviderMock` (мокирующий возврат `None`) и `YieldImageResponseProviderMock`.
   - Вызывается `client.images.generate` для генерации изображения.
   - Проверяется, что полученный ответ является экземпляром `ImagesResponse` и что URL первого изображения в ответе равен "Hello". Это показывает, что тест успешно пропустил `YieldNoneProviderMock` и использовал `YieldImageResponseProviderMock`.
7. **Тест `test_raise_exception`**:
   - Определяется асинхронная функция `run_exception`, которая инициализирует `AsyncClient` с `IterListProvider`, содержащим `YieldNoneProviderMock` и `AsyncRaiseExceptionProviderMock` (мокирующий выбрасывание исключения).
   - Вызывается `client.images.generate`, который должен вызвать исключение.
   - Проверяется, что при запуске `run_exception` через `asyncio.run` выбрасывается исключение `RuntimeError`.
8. **Запуск тестов**: Если скрипт запускается напрямую, запускаются все тесты с помощью `unittest.main()`.

Пример использования
-------------------------

```python
import asyncio
import unittest

from g4f.client import AsyncClient, ImagesResponse
from g4f.providers.retry_provider import IterListProvider
from unittest.mock import MagicMock

DEFAULT_MESSAGES = [{'role': 'user', 'content': 'Hello'}]

class MockImageResponse:
    def __init__(self, data):
        self.data = data

class MockProvider:
    async def generate(self, prompt: str, model: str = None, **kwargs) -> MockImageResponse:
        return MockImageResponse([MagicMock(url=prompt)])

class TestIterListProvider(unittest.IsolatedAsyncioTestCase):

    async def test_skip_provider(self):
        client = AsyncClient(image_provider=IterListProvider([MockProvider(), MockProvider()], False))
        response = await client.images.generate("Hello", "", response_format="orginal")
        self.assertIsInstance(response, ImagesResponse)
        self.assertEqual("Hello", response.data[0].url)

if __name__ == '__main__':
    unittest.main()