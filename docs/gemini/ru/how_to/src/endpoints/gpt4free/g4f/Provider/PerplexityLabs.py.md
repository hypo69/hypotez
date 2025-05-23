## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует класс `PerplexityLabs`, который представляет собой асинхронный генератор ответов с использованием модели Perplexity AI. Класс наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, которые обеспечивают базовую функциональность асинхронного генератора и управление моделями. 

Шаги выполнения
-------------------------
1. **Инициализация**: Создается новый экземпляр класса `PerplexityLabs` с использованием `PerplexityLabs(model="r1-1776", messages=messages)`.
2. **Создание асинхронного генератора**: Метод `create_async_generator` создает асинхронный генератор для получения ответов от модели. Он принимает в качестве параметров:
    - `model`: имя модели, например, "r1-1776", "sonar", "sonar-pro" и т. д.
    - `messages`: список сообщений, которые отправляются в модель.
    - `proxy`: (опционально) прокси-сервер, который будет использоваться для соединения.
3. **Обработка websocket-соединения**: Метод подключается к серверу Perplexity AI через websocket. 
4. **Отправка запроса**: Отправляется запрос с информацией о модели и сообщениями.
5. **Получение ответа**: Генератор получает ответ от модели по частям и возвращает их.
6. **Обработка окончания ответа**: Если получен полный ответ, генератор сообщает об этом, возвращая `FinishReason("stop")`.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PerplexityLabs import PerplexityLabs
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "Хорошо, а у тебя?"},
]

provider = PerplexityLabs(model="r1-1776", messages=messages)

async def main():
    async for response in provider.create_async_generator():
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Важное замечание:** 
- Метод `create_async_generator` возвращает асинхронный генератор, который нужно использовать в асинхронном контексте.
- Для корректной работы необходимо установить библиотеку `websockets`.