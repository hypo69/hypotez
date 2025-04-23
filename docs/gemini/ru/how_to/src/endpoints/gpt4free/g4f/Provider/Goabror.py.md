Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `Goabror`, который является асинхронным провайдером для работы с API goabror.uz. Он позволяет отправлять запросы к API и получать ответы в виде асинхронного генератора.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `json`, `aiohttp.ClientSession`, а также классы и функции из других модулей проекта, такие как `AsyncResult`, `Messages`, `AsyncGeneratorProvider`, `ProviderModelMixin`, `raise_for_status`, `format_prompt` и `get_system_prompt`.
2. **Определение класса `Goabror`**: Класс наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.
3. **Установка атрибутов класса**:
   - `url`: URL веб-сайта goabror.uz.
   - `api_endpoint`: URL API для отправки запросов.
   - `working`: Флаг, указывающий, работает ли провайдер.
   - `default_model`: Модель, используемая по умолчанию (`gpt-4`).
   - `models`: Список поддерживаемых моделей (в данном случае только `default_model`).
4. **Определение асинхронного генератора `create_async_generator`**: Этот метод создает асинхронный генератор, который отправляет запросы к API и возвращает ответы.
   - Принимает параметры: `model` (модель для использования), `messages` (сообщения для отправки), `proxy` (прокси-сервер, если необходимо) и `kwargs` (дополнительные аргументы).
   - Формирует заголовки (`headers`) для HTTP-запроса, включая `accept`, `accept-language` и `user-agent`.
   - Создает асинхронную сессию `ClientSession` с заданными заголовками.
   - Формирует параметры (`params`) для запроса, используя функции `format_prompt` и `get_system_prompt` для форматирования сообщений.
   - Отправляет GET-запрос к API (`cls.api_endpoint`) с заданными параметрами и прокси-сервером.
   - Проверяет статус ответа с помощью `raise_for_status`.
   - Получает текст ответа (`text_response`).
   - Пытается распарсить текст ответа как JSON. Если успешно, извлекает данные из поля `data` и возвращает их через `yield`. Если поле `data` отсутствует, возвращает весь текст ответа.
   - Если происходит ошибка `json.JSONDecodeError`, возвращает текст ответа как есть.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.Goabror import Goabror
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    model = "gpt-4"
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    proxy = None  # Замените на свой прокси, если необходимо

    async for response in Goabror.create_async_generator(model=model, messages=messages, proxy=proxy):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())