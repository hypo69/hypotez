# Документация для модуля Pizzagpt

## Обзор

Модуль `Pizzagpt` представляет собой асинхронный провайдер для взаимодействия с API сервиса Pizzagpt, который предоставляет доступ к языковой модели `gpt-4o-mini`. Модуль позволяет отправлять запросы к API и получать ответы в асинхронном режиме.

## Подробнее

Модуль предназначен для интеграции с другими компонентами проекта `hypotez`, требующими доступа к языковым моделям. Он обеспечивает возможность отправки текстовых запросов и получения сгенерированного текста в ответ.

## Классы

### `Pizzagpt`

**Описание**: Класс `Pizzagpt` является асинхронным провайдером и миксином для работы с API Pizzagpt.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL сервиса Pizzagpt (`https://www.pizzagpt.it`).
- `api_endpoint` (str): Endpoint API для отправки запросов (`/api/chatx-completion`).
- `working` (bool): Флаг, показывающий работоспособность провайдера (по умолчанию `False`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).
- `models` (list[str]): Список поддерживаемых моделей (содержит только `default_model`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

## Методы класса

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
    """Создает асинхронный генератор для получения ответов от API Pizzagpt.

    Args:
        cls (Pizzagpt): Ссылка на класс Pizzagpt.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий текст ответа от API.

    Raises:
        ValueError: Если в ответе от API обнаружено сообщение о злоупотреблении.
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    
    1. Функция устанавливает заголовки запроса, включая User-Agent, Origin, Referer и X-Secret.
    2. Форматирует список сообщений в строку запроса.
    3. Отправляет POST-запрос к API Pizzagpt с использованием `aiohttp.ClientSession`.
    4. Обрабатывает ответ от API, извлекая содержимое ответа.
    5. Если в содержимом ответа обнаружено сообщение "Misuse detected. please get in touch", выбрасывается исключение `ValueError`.
    6. Функция является генератором, который возвращает части ответа и FinishReason("stop").
    """

    async def post(session: ClientSession, url: str, data: dict, proxy: str = None) -> dict:
        """Внутренняя функция отправляет POST-запрос к API Pizzagpt.

        Args:
            session (ClientSession): Асинхронная сессия для выполнения запросов.
            url (str): URL для отправки запроса.
            data (dict): Данные для отправки в теле запроса.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Returns:
            dict: JSON-ответ от API.

        Raises:
            Exception: Если возникает ошибка при отправке запроса или обработке ответа.
        """

    async def get_content(response_json: dict) -> str | None:
        """Внутренняя функция извлекает содержимое ответа из JSON-ответа API.

        Args:
            response_json (dict): JSON-ответ от API.

        Returns:
            str | None: Текст ответа, если он присутствует, иначе `None`.
        """
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": cls.url,
        "referer": f"{cls.url}/en",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "x-secret": "Marinara"
    }
    async with ClientSession(headers=headers) as session:
        prompt = format_prompt(messages)
        data = {
            "question": prompt
        }
        async with session.post(f"{cls.url}{cls.api_endpoint}", json=data, proxy=proxy) as response:
            response.raise_for_status()
            response_json = await response.json()
            content = response_json.get("answer", response_json).get("content")
            if content:
                if "Misuse detected. please get in touch" in content:
                    raise ValueError(content)
                yield content
                yield FinishReason("stop")
```

## Примеры

Пример использования класса `Pizzagpt` и его метода `create_async_generator`:

```python
from src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    messages: Messages = [{"role": "user", "content": "Напиши стихотворение про осень."}]
    model = "gpt-4o-mini"
    async for response in Pizzagpt.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())