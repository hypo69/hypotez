# Модуль Pizzagpt

## Обзор

Модуль `Pizzagpt` предоставляет асинхронный генератор для взаимодействия с API сервиса pizzagpt.it. Он позволяет отправлять запросы к API и получать ответы в виде асинхронного генератора.

## Подробней

Этот модуль используется для интеграции с сервисом pizzagpt.it, предоставляющим API для генерации текста. Модуль отправляет запросы к API с использованием библиотеки `aiohttp` и возвращает результаты в виде асинхронного генератора, что позволяет обрабатывать большие объемы данных потоково и экономить память.
Анализ кода показывает, что модуль предназначен для асинхронного взаимодействия с API pizzagpt.it, предоставляющим сервис генерации текста. Он использует библиотеку `aiohttp` для отправки запросов и обработки ответов. Ключевой особенностью является асинхронная генерация результатов, что позволяет эффективно обрабатывать большие объемы данных. Модуль также включает обработку ошибок и форматирование запросов.
## Классы

### `Pizzagpt`

**Описание**: Класс `Pizzagpt` является асинхронным провайдером и миксином моделей. Он предназначен для взаимодействия с API pizzagpt.it для генерации текста.

**Принцип работы**:
Класс наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он определяет URL, API endpoint, используемую модель и заголовки для взаимодействия с API. Метод `create_async_generator` отправляет запрос к API и возвращает асинхронный генератор, который выдает части сгенерированного текста.

**Аттрибуты**:
- `url` (str): URL сервиса pizzagpt.it.
- `api_endpoint` (str): Endpoint API для отправки запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

## Функции

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
    """
    Создает асинхронный генератор для получения ответов от API pizzagpt.it.

    Args:
        model (str): Модель для генерации текста.
        messages (Messages): Список сообщений для отправки в запросе.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий части сгенерированного текста.

    Raises:
        ValueError: Если в ответе содержится сообщение об обнаружении злоупотребления.
    """
```

**Назначение**: Создание асинхронного генератора для взаимодействия с API pizzagpt.it.

**Параметры**:
- `cls` (type): Ссылка на класс.
- `model` (str): Модель для генерации текста.
- `messages` (Messages): Список сообщений для отправки в запросе.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий части сгенерированного текста.

**Вызывает исключения**:
- `ValueError`: Если в ответе содержится сообщение об обнаружении злоупотребления (`Misuse detected. please get in touch`).

**Как работает функция**:

1. **Подготовка заголовков**: Функция создает заголовки HTTP-запроса, включая `accept`, `accept-language`, `content-type`, `origin`, `referer`, `user-agent` и `x-secret`. Заголовок `x-secret` содержит значение `Marinara`.
2. **Создание сессии**: Используется асинхронный контекстный менеджер `ClientSession` для создания HTTP-сессии с заданными заголовками.
3. **Форматирование промпта**: Функция форматирует сообщения `messages` в строку `prompt` с использованием функции `format_prompt`.
4. **Подготовка данных**: Создается словарь `data`, содержащий отформатированный промт под ключом `"question"`.
5. **Отправка запроса**: Отправляется POST-запрос к API endpoint (`cls.url}{cls.api_endpoint}`) с данными в формате JSON и использованием прокси, если он указан.
6. **Обработка ответа**:
   - Проверяется статус ответа на наличие ошибок с помощью `response.raise_for_status()`.
   - Ответ преобразуется в JSON-формат.
   - Из JSON извлекается содержимое ответа из полей `response_json.get("answer", response_json).get("content")`.
7. **Генерация результата**:
   - Если содержимое присутствует:
     - Проверяется наличие сообщения об обнаружении злоупотребления (`Misuse detected. please get in touch`). Если оно присутствует, вызывается исключение `ValueError`.
     - Содержимое передается в генератор с помощью `yield content`.
     - В генератор передается сигнал остановки (`FinishReason("stop")`) с помощью `yield FinishReason("stop")`.

**Внутренние функции**:
Внутри функции `create_async_generator` не определены внутренние функции.

**ASCII flowchart**:

```
    [Начало]
     |
     v
[Подготовка заголовков]
     |
     v
   [Создание сессии]
     |
     v
[Форматирование промпта]
     |
     v
   [Подготовка данных]
     |
     v
   [Отправка запроса]
     |
     v
   [Обработка ответа]
     |
     v
[Извлечение содержимого]
     |
     v
  [Проверка на злоупотребление]
     |
     v
[Генерация результата] ---> [Выдача содержимого]
     |                       |
     v                       v
   [Сигнал остановки]      [Конец]
     |
     v
   [Конец]
```

**Примеры**:

```python
# Пример вызова функции create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

from g4f.Provider.Pizzagpt import Pizzagpt
from g4f.typing import Messages, AsyncResult, FinishReason

async def main():
    model: str = "gpt-4o-mini"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    proxy: Optional[str] = None

    result: AsyncResult = await Pizzagpt.create_async_generator(model=model, messages=messages, proxy=proxy)

    async for item in result:
        if isinstance(item, str):
            print("Content:", item)
        elif isinstance(item, FinishReason):
            print("Finish Reason:", item)

if __name__ == "__main__":
    asyncio.run(main())

# Пример вызова с прокси
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

from g4f.Provider.Pizzagpt import Pizzagpt
from g4f.typing import Messages, AsyncResult, FinishReason

async def main():
    model: str = "gpt-4o-mini"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    proxy: str = "http://your_proxy:8080"

    result: AsyncResult = await Pizzagpt.create_async_generator(model=model, messages=messages, proxy=proxy)

    async for item in result:
        if isinstance(item, str):
            print("Content:", item)
        elif isinstance(item, FinishReason):
            print("Finish Reason:", item)

if __name__ == "__main__":
    asyncio.run(main())
```