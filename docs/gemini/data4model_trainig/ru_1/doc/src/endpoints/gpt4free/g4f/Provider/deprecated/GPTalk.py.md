# Модуль GPTalk

## Обзор

Модуль `GPTalk` предоставляет асинхронный генератор для взаимодействия с GPT моделями через API gptalk.net. Он поддерживает модель `gpt-3.5-turbo` и использует асинхронные запросы для получения ответов от модели.

## Подробней

Модуль предназначен для интеграции с сервисом gptalk.net, предоставляющим доступ к языковым моделям. Он автоматически управляет аутентификацией, повторно использует токены и отправляет запросы для получения потоковых ответов.

## Классы

### `GPTalk`

**Описание**: Класс `GPTalk` является асинхронным провайдером генератора для взаимодействия с API gptalk.net.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL сервиса gptalk.net.
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo` (по умолчанию `True`).
- `_auth` (Optional[dict]): Словарь, содержащий данные аутентификации.
- `used_times` (int): Счетчик использования токена аутентификации.

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для получения ответов от GPT модели.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от GPT модели.

    Args:
        cls (GPTalk): Ссылка на класс.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в модель.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Raises:
        aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP запроса.

    Как работает функция:
    1. Проверяет и устанавливает модель по умолчанию, если не указана.
    2. Формирует timestamp для заголовков.
    3. Определяет заголовки для HTTP-запросов, включая user-agent, appid и timestamp.
    4. Использует `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.
    5. Проверяет необходимость обновления токена аутентификации. Если токен отсутствует, устарел или был использован 5 раз,
       выполняет запрос на логин для получения нового токена.
    6. Формирует данные запроса, включая отформатированные сообщения, параметры модели и другие метаданные.
    7. Отправляет POST-запрос к API для получения текстового ответа.
    8. Извлекает токен из ответа.
    9. Увеличивает счетчик использования токена.
    10. Отправляет GET-запрос к API для получения потоковых данных.
    11. Итерируется по каждой строке ответа и извлекает содержимое сообщения, возвращая его через генератор.

    Внутренние функции:
        Отсутствуют.
    """
    ...
```

## Параметры класса

- `url` (str): URL сервиса gptalk.net.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.
- `_auth` (Optional[dict]): Словарь, содержащий данные аутентификации.
- `used_times` (int): Счетчик использования токена аутентификации.

## Примеры

Пример использования класса `GPTalk`:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated.GPTalk import GPTalk
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Привет, как дела?"}]
    async for message in GPTalk.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())