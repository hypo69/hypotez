## Как использовать блок кода `TestIterListProvider`
=========================================================================================

Описание
-------------------------
Блок кода `TestIterListProvider` содержит набор юнит-тестов для проверки работы класса `IterListProvider` из библиотеки `g4f`. Класс `IterListProvider` используется для последовательного вызова нескольких провайдеров, предоставляющих данные для генерации изображений. Тесты проверяют различные сценарии, такие как пропуск провайдеров, обработка пустых результатов, исключений и обработку только одного результата.

Шаги выполнения
-------------------------
1. **Инициализация `AsyncClient`**: Создается экземпляр класса `AsyncClient` с использованием `IterListProvider`, который содержит список из нескольких провайдеров. 
2. **Вызов метода `images.generate`**: Вызывается метод `images.generate` для генерации изображения с заданными параметрами.
3. **Проверка результата**:  Проверяется, что результат является экземпляром класса `ImagesResponse` и содержит ожидаемые данные.
4. **Проверка исключения**: В некоторых тестах проверяется, что при вызове метода `images.generate` возникает определенное исключение (например, `RuntimeError`).

Пример использования
-------------------------

```python
import asyncio
from g4f.client import AsyncClient
from g4f.providers.retry_provider import IterListProvider
from .mocks import YieldImageResponseProviderMock, MissingAuthProviderMock

async def run_test():
    """
    Пример использования `TestIterListProvider`
    """
    # Создаем `IterListProvider` с двумя провайдерами
    image_provider = IterListProvider([MissingAuthProviderMock, YieldImageResponseProviderMock], False)
    # Инициализируем `AsyncClient`
    client = AsyncClient(image_provider=image_provider)
    # Вызываем метод `images.generate`
    response = await client.images.generate("Hello", "", response_format="original")
    # Проверяем результат
    assert isinstance(response, ImagesResponse)
    assert "Hello" in response.data[0].url

if __name__ == '__main__':
    asyncio.run(run_test())
```