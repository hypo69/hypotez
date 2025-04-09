# Модуль ChatAnywhere

## Обзор

Модуль `ChatAnywhere` предоставляет асинхронный генератор для взаимодействия с сервисом `chatanywhere.cn`. Он поддерживает модель `gpt-3.5-turbo` и сохранение истории сообщений. Этот модуль предназначен для использования в асинхронных приложениях, требующих потоковой обработки ответов от чат-бота.

## Подробнее

Модуль реализует класс `ChatAnywhere`, который наследуется от `AsyncGeneratorProvider`. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов к API `chatanywhere.cn`. Модуль предназначен для интеграции в систему, где требуется асинхронное взаимодействие с чат-ботом через API.

## Классы

### `ChatAnywhere`

**Описание**:
Класс `ChatAnywhere` предоставляет асинхронный генератор для взаимодействия с API `chatanywhere.cn`.

**Наследует**:
`AsyncGeneratorProvider` - базовый класс для асинхронных провайдеров генераторов.

**Атрибуты**:
- `url` (str): URL сервиса `chatanywhere.cn`.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.
- `supports_message_history` (bool): Флаг, указывающий на поддержку сохранения истории сообщений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.

**Методы**:
- `create_async_generator`: Создаёт асинхронный генератор для взаимодействия с API.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    temperature: float = 0.5,
    **kwargs
) -> AsyncResult:
    """
    Создаёт асинхронный генератор для взаимодействия с API `chatanywhere.cn`.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа в секундах. По умолчанию 120.
        temperature (float, optional): Температура генерации текста. По умолчанию 0.5.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий чанки данных ответа.

    Raises:
        Exception: В случае ошибок при выполнении HTTP-запроса.
    """
```

**Назначение**:
Функция `create_async_generator` создает асинхронный генератор, который отправляет сообщения в API `chatanywhere.cn` и возвращает чанки данных ответа.

**Параметры**:
- `cls`: Класс, для которого вызывается метод.
- `model` (str): Модель, используемая для генерации ответа.
- `messages` (Messages): Список сообщений, отправляемых в API.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `timeout` (int, optional): Максимальное время ожидания ответа от сервера в секундах. По умолчанию 120.
- `temperature` (float, optional): Параметр, контролирующий случайность генерации текста. Значение по умолчанию равно 0.5.
- `**kwargs`: Дополнительные аргументы, которые могут быть переданы в функцию.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий чанки данных ответа.

**Вызывает исключения**:
- `Exception`: В случае возникновения ошибок при выполнении HTTP-запроса.

**Как работает функция**:

1.  **Определение заголовков**: Функция начинает с определения необходимых HTTP-заголовков, включая `User-Agent`, `Accept`, `Content-Type` и другие.

2.  **Создание сессии `aiohttp`**: Создается асинхронная сессия `aiohttp` с заданными заголовками и временем ожидания. Использование `ClientSession` позволяет переиспользовать соединение для нескольких запросов, что повышает эффективность.

3.  **Формирование данных запроса**: Формируются данные запроса в формате JSON, включающие список сообщений, идентификатор, заголовок, температуру и другие параметры.

4.  **Выполнение POST-запроса**: Выполняется асинхронный POST-запрос к API `chatanywhere.cn` с использованием `session.post`. В случае возникновения HTTP-ошибки, выбрасывается исключение `response.raise_for_status()`.

5.  **Получение и обработка чанков данных**: Функция итерируется по чанкам данных, полученным из ответа сервера, и декодирует каждый чанк, после чего передает его через `yield`.

```
Определение заголовков и данных запроса
│
ClientSession(headers=headers, timeout=ClientTimeout(timeout))
│
POST-запрос к API chatanywhere.cn
│
Получение и обработка чанков данных
│
Выдача чанков данных через yield
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import AsyncGenerator, List, Dict

async def main():
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Привет, как дела?"}]
    proxy = None
    timeout = 120
    temperature = 0.5

    generator: AsyncGenerator[str, None] = await ChatAnywhere.create_async_generator(
        model=model,
        messages=messages,
        proxy=proxy,
        timeout=timeout,
        temperature=temperature
    )

    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример использования create_async_generator c прокси
import asyncio
from typing import AsyncGenerator, List, Dict

async def main():
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Привет, как дела?"}]
    proxy = "http://your.proxy:8080"  # Замените на ваш прокси
    timeout = 120
    temperature = 0.5

    generator: AsyncGenerator[str, None] = await ChatAnywhere.create_async_generator(
        model=model,
        messages=messages,
        proxy=proxy,
        timeout=timeout,
        temperature=temperature
    )

    async for chunk in generator:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())