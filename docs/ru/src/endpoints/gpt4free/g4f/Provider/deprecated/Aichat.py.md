# Модуль `Aichat`

## Обзор

Модуль `Aichat` предоставляет класс `Aichat`, который является асинхронным провайдером для взаимодействия с API `chat-gpt.org`. Он позволяет отправлять запросы к API и получать ответы. Модуль использует библиотеку `requests` для выполнения HTTP-запросов.

## Подробнее

Модуль предназначен для использования в проектах, требующих взаимодействия с API `chat-gpt.org`. Он предоставляет удобный интерфейс для отправки запросов и обработки ответов.  Анализ показывает, что модуль отвечает за асинхронное взаимодействие с API `chat-gpt.org` для получения текстовых ответов на основе предоставленных сообщений. Он использует куки для аутентификации и прокси при необходимости, а также обрабатывает возможные ошибки при запросах.

## Классы

### `Aichat`

**Описание**: Класс `Aichat` является асинхронным провайдером для взаимодействия с API `chat-gpt.org`.

**Наследует**:
- `AsyncProvider`: Наследует функциональность асинхронного провайдера.

**Атрибуты**:
- `url` (str): URL API `chat-gpt.org`.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.

**Методы**:
- `create_async`: Отправляет асинхронный запрос к API `chat-gpt.org` и возвращает ответ.

## Функции

### `create_async`

```python
    async def create_async(
        model: str,
        messages: Messages,
        proxy: str = None, **kwargs) -> str:
        """
        Отправляет асинхронный запрос к API `chat-gpt.org` и возвращает ответ.

        Args:
            model (str): Имя модели, используемой для генерации ответа.
            messages (Messages): Список сообщений, отправляемых в API.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы, такие как `cookies`, `temperature`, `top_p`.

        Returns:
            str: Текстовый ответ от API.

        Raises:
            RuntimeError: Если не удалось получить куки для `chat-gpt.org`.
            Exception: Если API возвращает ошибку.
        """
```

**Назначение**: Функция `create_async` отправляет асинхронный запрос к API `chat-gpt.org` и возвращает текстовый ответ.

**Параметры**:
- `model` (str): Имя модели, используемой для генерации ответа.
- `messages` (Messages): Список сообщений, отправляемых в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, такие как `cookies`, `temperature`, `top_p`.

**Возвращает**:
- `str`: Текстовый ответ от API.

**Вызывает исключения**:
- `RuntimeError`: Если не удалось получить куки для `chat-gpt.org`.
- `Exception`: Если API возвращает ошибку.

**Как работает функция**:

1. **Получение куки**: Функция пытается получить куки для домена `chat-gpt.org`. Если куки не предоставлены в `kwargs`, она использует функцию `get_cookies`. Если получить куки не удается, выбрасывается исключение `RuntimeError`.
2. **Формирование заголовков**: Функция формирует заголовки HTTP-запроса, включая `authority`, `accept`, `content-type` и другие.
3. **Создание сессии**: Функция создает асинхронную сессию с использованием `StreamSession` из библиотеки `requests`. В сессию передаются заголовки, куки, таймаут, прокси (если указан) и другие параметры.
4. **Формирование данных запроса**: Функция формирует JSON-данные для отправки в API. Данные включают сообщения, температуру и другие параметры.
5. **Отправка запроса**: Функция отправляет POST-запрос к API `chat-gpt.org/api/text` с использованием созданной сессии и JSON-данных.
6. **Обработка ответа**: Функция обрабатывает ответ от API. Если ответ содержит ошибку, выбрасывается исключение `Exception`. Если ответ успешен, функция возвращает текстовое сообщение.

**ASII flowchart**:

```
A: Получение куки
|
B: Формирование заголовков
|
C: Создание асинхронной сессии
|
D: Формирование данных запроса
|
E: Отправка POST-запроса
|
F: Обработка ответа
```

**Примеры**:

```python
# Пример вызова функции create_async
import asyncio
from typing import List, Dict

async def main():
    model = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = None
    kwargs = {"temperature": 0.7, "top_p": 0.9}

    try:
        response = await Aichat.create_async(model, messages, proxy, **kwargs)
        print(f"Response: {response}")
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример вызова функции create_async с прокси и куки
import asyncio
from typing import List, Dict

async def main():
    model = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Translate to french: Hello, how are you?"}]
    proxy = "http://your_proxy:8080"
    cookies = {"cookie_name": "cookie_value"}
    kwargs = {"temperature": 0.7, "top_p": 0.9, "cookies": cookies}

    try:
        response = await Aichat.create_async(model, messages, proxy, **kwargs)
        print(f"Response: {response}")
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    asyncio.run(main())