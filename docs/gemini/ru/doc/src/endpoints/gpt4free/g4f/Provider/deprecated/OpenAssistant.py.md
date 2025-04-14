# Модуль для работы с OpenAssistant (устаревший)

## Обзор

Модуль `OpenAssistant` предоставляет класс `OpenAssistant`, который является асинхронным провайдером для взаимодействия с моделью OpenAssistant. Этот модуль позволяет отправлять запросы к OpenAssistant API и получать ответы в виде асинхронного генератора. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и требует аутентификации.
Модуль помечен как устаревший.

## Подробней

Модуль предназначен для интеграции с OpenAssistant API, предоставляя удобный интерфейс для отправки сообщений и получения ответов в асинхронном режиме. Он включает в себя обработку cookies, формирование запросов и обработку ответов от API.
Основная задача этого модуля – обеспечить возможность взаимодействия с OpenAssistant API для получения ответов от модели в виде асинхронного генератора.
В модуле реализована поддержка прокси и передача дополнительных параметров в запросах.

## Классы

### `OpenAssistant`

**Описание**: Класс `OpenAssistant` является асинхронным провайдером для взаимодействия с моделью OpenAssistant.

**Наследует**:
- `AsyncGeneratorProvider`: базовый класс для асинхронных генераторов провайдеров.

**Атрибуты**:
- `url` (str): URL для взаимодействия с OpenAssistant API.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `working` (bool): Указывает, работает ли провайдер.
- `model` (str): Название используемой модели OpenAssistant.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от OpenAssistant API.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        cookies: dict = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от OpenAssistant API.

        Args:
            model (str): Название модели, которую нужно использовать.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            cookies (dict, optional): Словарь cookies для аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные параметры для настройки sampling_parameters.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий ответы от API.

        Raises:
            RuntimeError: Если в ответе от API содержится сообщение об ошибке.
            aiohttp.ClientResponseError: Если при выполнении запроса произошла HTTP-ошибка.

        Принцип работы:
        1. Проверяет наличие cookies, и если их нет, получает их с сайта open-assistant.io.
        2. Создает сессию aiohttp.ClientSession с использованием cookies и заголовков User-Agent.
        3. Отправляет POST-запрос к API для создания чата и получает chat_id.
        4. Формирует и отправляет сообщение пользователя (prompter_message) с использованием полученного chat_id и форматированного списка сообщений. Получает parent_id.
        5. Формирует и отправляет запрос assistant_message с использованием chat_id, parent_id, model и sampling_parameters.
        6. Получает message_id из ответа.
        7. Отправляет POST-запрос к API для получения событий чата (events) и генерирует ответы на основе полученных токенов.
        8. Удаляет чат после завершения получения ответов.

        Внутренние функции:
            отсутствуют
        """
```

## Параметры класса

- `cls`: Ссылка на класс `OpenAssistant`.
- `model` (str): Название модели, которую нужно использовать.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `cookies` (dict, optional): Словарь cookies для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для настройки sampling_parameters.

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

async def main():
    model_name = "OA_SFT_Llama_30B_6"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    proxy_url: Optional[str] = None
    cookies_data: Optional[Dict[str, str]] = None

    async def print_generator(generator: AsyncGenerator[str, None]) -> None:
        async for item in generator:
            print(item, end="")

    try:
        generator = await OpenAssistant.create_async_generator(
            model=model_name,
            messages=messages,
            proxy=proxy_url,
            cookies=cookies_data
        )
        await print_generator(generator)
    except Exception as ex:
        print(f"An error occurred: {ex}")

if __name__ == "__main__":
    asyncio.run(main())