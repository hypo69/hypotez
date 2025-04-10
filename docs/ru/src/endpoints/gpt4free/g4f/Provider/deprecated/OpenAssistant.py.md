# Модуль OpenAssistant

## Обзор

Модуль `OpenAssistant` предоставляет асинхронный генератор для взаимодействия с Open Assistant API. Он позволяет отправлять сообщения и получать ответы в режиме реального времени, используя асинхронные запросы. Модуль требует аутентификации и использует cookies для поддержания сессии.

## Подробней

Этот модуль предназначен для интеграции с платформой Open Assistant, предоставляя функциональность чат-бота. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов к API Open Assistant. Модуль включает в себя функции для форматирования промптов, получения cookies и обработки ответов от сервера.

## Классы

### `OpenAssistant`

**Описание**: Класс `OpenAssistant` является провайдером асинхронного генератора для взаимодействия с Open Assistant API.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует от базового класса `AsyncGeneratorProvider`.

**Атрибуты**:
- `url` (str): URL для взаимодействия с Open Assistant API.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с API.
- `working` (bool): Указывает, находится ли провайдер в рабочем состоянии.
- `model` (str): Модель, используемая по умолчанию, `"OA_SFT_Llama_30B_6"`.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для отправки сообщений и получения ответов от Open Assistant API.

## Функции

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
        """Создает асинхронный генератор для взаимодействия с Open Assistant API.

        Args:
            model (str): Модель, используемая для генерации ответа.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
            cookies (dict, optional): Cookies для аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные параметры, передаваемые в API.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.

        Raises:
            RuntimeError: Если в ответе от API содержится сообщение об ошибке.
            aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.
        """
```

**Назначение**: Функция `create_async_generator` создает и возвращает асинхронный генератор, который взаимодействует с API Open Assistant для получения ответов на основе предоставленных сообщений.

**Параметры**:
- `cls`: Ссылка на класс `OpenAssistant`.
- `model` (str): Модель, используемая для генерации ответа.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
- `cookies` (dict, optional): Cookies для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, передаваемые в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:
- `RuntimeError`: Если в ответе от API содержится сообщение об ошибке.
- `aiohttp.ClientResponseError`: Если возникает ошибка при выполнении HTTP-запроса.

**Как работает функция**:

1. **Получение Cookies**: Если cookies не предоставлены, функция пытается получить их с домена `"open-assistant.io"`.
2. **Создание сессии**: Создается асинхронная сессия `aiohttp.ClientSession` с использованием cookies и заголовка User-Agent.
3. **Получение chat_id**: Отправляется POST-запрос к `"https://open-assistant.io/api/chat"` для получения идентификатора чата.
4. **Форматирование промпта**: Форматируются входные сообщения с использованием функции `format_prompt`.
5. **Отправка сообщения пользователя**: Отправляется POST-запрос к `"https://open-assistant.io/api/chat/prompter_message"` с отформатированным сообщением пользователя для получения `parent_id`.
6. **Отправка сообщения ассистента**: Отправляется POST-запрос к `"https://open-assistant.io/api/chat/assistant_message"` с данными, включающими `chat_id`, `parent_id`, модель и параметры выборки, для получения `message_id`.
7. **Обработка ошибок**: Если в ответе содержится сообщение об ошибке, вызывается исключение `RuntimeError`.
8. **Получение событий**: Отправляется POST-запрос к `"https://open-assistant.io/api/chat/events"` для получения событий в режиме реального времени.
9. **Генерация токенов**: Функция декодирует каждую строку ответа, извлекает текст токена и возвращает его через генератор.
10. **Удаление чата**: После завершения генерации токенов функция отправляет DELETE-запрос к `"https://open-assistant.io/api/chat"` для удаления чата.

**Внутренние функции**: Нет.

**Примеры**:

```python
# Пример использования функции create_async_generator
import asyncio
from typing import AsyncGenerator, List, Dict

from g4f.Provider.deprecated.OpenAssistant import OpenAssistant
from g4f.typing import Messages

async def main():
    model = "OA_SFT_Llama_30B_6"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = None
    cookies = None
    kwargs = {}

    generator: AsyncGenerator = await OpenAssistant.create_async_generator(
        model=model, messages=messages, proxy=proxy, cookies=cookies, **kwargs
    )

    async for message in generator:
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

```
Инициализация сессии aiohttp
    |
    --> Запрос chat_id
    |
    --> Форматирование сообщений
    |
    --> Запрос parent_id
    |
    --> Запрос message_id
    |
    --> Запрос events
    |
    --> Генерация ответа (токены)
    |
    --> Удаление чата