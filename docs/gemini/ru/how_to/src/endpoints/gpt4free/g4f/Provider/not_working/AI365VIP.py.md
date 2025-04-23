### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `AI365VIP`, который является асинхронным провайдером для взаимодействия с API AI365VIP. Он наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет ему асинхронно генерировать ответы и поддерживать различные модели. Класс предназначен для отправки запросов к API чата AI365VIP и получения ответов в виде асинхронного генератора.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `__future__`, `ClientSession` из `aiohttp`, `AsyncResult`, `Messages` из `...typing`, `AsyncGeneratorProvider`, `ProviderModelMixin` из `..base_provider` и `format_prompt` из `..helper`.

2. **Определение класса `AI365VIP`**:
   - Определяется класс `AI365VIP`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Устанавливаются атрибуты класса, такие как `url`, `api_endpoint`, `working`, `default_model`, `models` и `model_aliases`.

3. **Определение метода `create_async_generator`**:
   - Определяется асинхронный классовый метод `create_async_generator`, который принимает параметры `model`, `messages`, `proxy` и `kwargs`.
   - Формируются HTTP-заголовки для запроса.
   - Создается асинхронная сессия `ClientSession` с заданными заголовками.
   - Формируется тело запроса `data` с информацией о модели, сообщении и параметрах.
   - Отправляется POST-запрос к API AI365VIP с использованием `session.post`.
   - Обрабатывается ответ от API и извлекаются чанки данных.
   - Каждый полученный чанк данных декодируется и возвращается как часть асинхронного генератора.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.not_working.AI365VIP import AI365VIP
from src.typing import Messages
import asyncio

async def main():
    model = "gpt-3.5-turbo"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = None  # Замените на ваш прокси, если необходимо

    async for chunk in AI365VIP.create_async_generator(model=model, messages=messages, proxy=proxy):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())