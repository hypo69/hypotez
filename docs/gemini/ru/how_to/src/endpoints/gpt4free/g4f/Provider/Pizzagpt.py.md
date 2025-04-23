### Как использовать блок кода Pizzagpt
=========================================================================================

Описание
-------------------------
Этот код определяет класс `Pizzagpt`, который является асинхронным провайдером для генерации текста на основе модели `gpt-4o-mini`. Он использует API `pizzagpt.it` для отправки запросов и получения ответов.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `__future__`, `ClientSession` из `aiohttp`, `AsyncResult` и `Messages` из `..typing`, `AsyncGeneratorProvider` и `ProviderModelMixin` из `.base_provider`, `format_prompt` из `.helper`, `FinishReason` из `..providers.response`.
2. **Определение класса `Pizzagpt`**:
   - Класс `Pizzagpt` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
   - Определяются атрибуты класса: `url` (базовый URL), `api_endpoint` (endpoint для API), `working` (флаг работоспособности), `default_model` (модель по умолчанию) и `models` (список поддерживаемых моделей).
3. **Реализация метода `create_async_generator`**:
   - Этот метод является асинхронным генератором, который отправляет запросы к API и возвращает результаты.
   - Формируются заголовки запроса, включая `accept`, `accept-language`, `content-type`, `origin`, `referer`, `user-agent` и `x-secret`.
   - Создается асинхронная сессия `ClientSession` с заданными заголовками.
   - Форматируется промпт с использованием функции `format_prompt`.
   - Формируются данные запроса в формате JSON, содержащие отформатированный промпт.
   - Отправляется POST-запрос к API с использованием `session.post`.
   - Обрабатывается ответ от API:
     - Проверяется статус ответа с помощью `response.raise_for_status()`.
     - Извлекается JSON из ответа.
     - Извлекается содержимое ответа из поля `answer.content` или непосредственно из JSON.
     - Если содержимое присутствует, проверяется наличие сообщения об обнаружении злоупотреблений, и если оно есть, вызывается исключение `ValueError`.
     - Содержимое ответа передается через `yield`, делая метод генератором.
     - В конце генерируется `FinishReason("stop")`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    messages: Messages = [
        {"role": "system", "content": "Ты полезный ассистент."},
        {"role": "user", "content": "Как тебя зовут?"}
    ]
    
    async for response in Pizzagpt.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())