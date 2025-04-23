# Модуль FakeGpt

## Обзор

Модуль `FakeGpt` предоставляет асинхронный генератор для взаимодействия с сервисом `chat-shared2.zhile.io`. Он имитирует GPT и использует API для генерации текстовых ответов на основе входных сообщений. Этот модуль предназначен для использования в качестве одного из провайдеров в системе, где требуется асинхронная генерация текста.

## Детали

Модуль содержит класс `FakeGpt`, который является асинхронным генератором. Он поддерживает модель `gpt-3.5-turbo` и использует `aiohttp` для выполнения HTTP-запросов. Для работы требуется получение токена доступа и управление cookie.

## Классы

### `FakeGpt`

**Описание**: Класс `FakeGpt` является асинхронным провайдером, который взаимодействует с API `chat-shared2.zhile.io` для генерации текста.

**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров.

**Атрибуты**:
- `url` (str): URL сервиса `chat-shared2.zhile.io`.
- `supports_gpt_35_turbo` (bool): Указывает, что провайдер поддерживает модель `gpt-3.5-turbo`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `_access_token` (str | None): Токен доступа для авторизации запросов.
- `_cookie_jar` (aiohttp.CookieJar | None): Хранилище cookie для сессии.

**Принцип работы**:
1. Класс использует URL `https://chat-shared2.zhile.io` для взаимодействия с сервером.
2. При первом запросе, если отсутствует токен доступа (`_access_token`), он получает список токенов (`token_ids`) с сервера.
3. Выбирает случайный `token_key` из списка и получает `session_password`.
4. Выполняет POST-запрос для аутентификации (`/auth/login`) с использованием `token_key` и `session_password`.
5. После успешной аутентификации получает токен доступа (`accessToken`) из `/api/auth/session`.
6. Для каждого запроса на генерацию текста формирует JSON-запрос с использованием предоставленных сообщений (`messages`).
7. Отправляет POST-запрос на `/api/conversation` с заголовками, включающими токен доступа.
8. Получает ответ в виде event-stream и извлекает сгенерированный текст из каждого события.
9. Генерирует текст асинхронно, возвращая его частями.

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
        """ Создает асинхронный генератор для получения ответов от FakeGpt.

        Args:
            model (str): Модель для генерации текста.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий сгенерированный текст.

        Raises:
            RuntimeError: Если не получен допустимый ответ.

        Как работает функция:
        1. Функция принимает модель, список сообщений и прокси (опционально) в качестве аргументов.
        2. Формирует заголовки (`headers`) для HTTP-запросов, включая User-Agent, Referer и другие необходимые параметры.
        3. Использует асинхронную сессию (`ClientSession`) для выполнения запросов.
        4. Если отсутствует токен доступа (`cls._access_token`), выполняет следующие действия:
           - Получает список токенов с сервера (`/api/loads`).
           - Выбирает случайный токен и пароль сессии.
           - Выполняет POST-запрос для аутентификации (`/auth/login`).
           - Получает токен доступа из `/api/auth/session`.
           - Обновляет хранилище cookie (`cls._cookie_jar`) для сессии.
        5. Формирует JSON-запрос (`data`) с использованием предоставленных сообщений.
        6. Отправляет POST-запрос на `/api/conversation` с заголовками, включающими токен доступа.
        7. Получает ответ в виде event-stream и извлекает сгенерированный текст из каждого события.
        8. Генерирует текст асинхронно, возвращая его частями.
        9. Если не получен допустимый ответ, вызывает исключение `RuntimeError`.

        Примеры:
            Пример 1: Генерация текста с использованием FakeGpt без прокси.

            ```python
            model = "gpt-3.5-turbo"
            messages = [{"role": "user", "content": "Hello, how are you?"}]
            generator = FakeGpt.create_async_generator(model=model, messages=messages)
            ```

            Пример 2: Генерация текста с использованием FakeGpt с прокси.

            ```python
            model = "gpt-3.5-turbo"
            messages = [{"role": "user", "content": "What is the capital of France?"}]
            proxy = "http://your_proxy_url"
            generator = FakeGpt.create_async_generator(model=model, messages=messages, proxy=proxy)
            ```
        """
```

## Параметры класса

- `url` (str): URL сервиса `chat-shared2.zhile.io`.
- `supports_gpt_35_turbo` (bool): Указывает, что провайдер поддерживает модель `gpt-3.5-turbo`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `_access_token` (str | None): Токен доступа для авторизации запросов.
- `_cookie_jar` (aiohttp.CookieJar | None): Хранилище cookie для сессии.

## Примеры

Пример 1: Создание и использование асинхронного генератора `FakeGpt`.

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated import FakeGpt

async def main():
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Tell me a joke."}]
    async for message in FakeGpt.create_async_generator(model=model, messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

Пример 2: Использование прокси с асинхронным генератором `FakeGpt`.

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated import FakeGpt

async def main():
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Translate 'hello' to French."}]
    proxy = "http://your_proxy_url"  # Замените на URL вашего прокси-сервера
    async for message in FakeGpt.create_async_generator(model=model, messages=messages, proxy=proxy):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```