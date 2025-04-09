# Модуль Pizzagpt

## Обзор

Модуль `Pizzagpt` предоставляет асинхронный генератор для взаимодействия с API pizzagpt.it. Он позволяет отправлять запросы к модели и получать ответы в виде асинхронного генератора.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с сервисом pizzagpt.it. Он использует асинхронные запросы для взаимодействия с API, что позволяет эффективно обрабатывать ответы. Модуль включает в себя форматирование запроса, отправку его на API и обработку полученного ответа.

## Классы

### `Pizzagpt`

**Описание**: Класс `Pizzagpt` является асинхронным провайдером и миксином моделей.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса `https://www.pizzagpt.it`.
- `api_endpoint` (str): Эндпоинт API `/api/chatx-completion`.
- `working` (bool): Указывает, работает ли провайдер. Изначально `False`.
- `default_model` (str): Модель по умолчанию `'gpt-4o-mini'`.
- `models` (list): Список поддерживаемых моделей `[default_model]`.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от API.

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
    Создает асинхронный генератор для получения ответов от API Pizzagpt.

    Args:
        model (str): Модель для использования в запросе.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        ValueError: Если обнаружено злоупотребление в содержании ответа.
    """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API `Pizzagpt`.

**Параметры**:
- `cls` (type): Ссылка на класс.
- `model` (str): Модель для использования в запросе.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:
- `ValueError`: Если обнаружено злоупотребление в содержании ответа.

**Как работает функция**:

1. **Подготовка заголовков**: Формируются заголовки HTTP-запроса, включая `accept`, `accept-language`, `content-type`, `origin`, `referer` и `user-agent`. Также устанавливается секретный ключ `x-secret` равным `"Marinara"`.
2. **Создание сессии**: Используется `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов с заданными заголовками.
3. **Форматирование запроса**: Список сообщений `messages` форматируется в строку `prompt` с использованием функции `format_prompt`.
4. **Подготовка данных**: Формируется словарь `data`, содержащий отформатированный запрос `prompt` под ключом `"question"`.
5. **Отправка запроса**: Отправляется POST-запрос к API эндпоинту (`cls.url + cls.api_endpoint`) с использованием `session.post`. В запрос передаются данные в формате JSON и, если указано, прокси-сервер.
6. **Обработка ответа**:
   - Проверяется статус ответа с помощью `response.raise_for_status()`, чтобы вызвать исключение в случае ошибки.
   - Полученный JSON-ответ преобразуется в словарь `response_json`.
   - Извлекается содержимое ответа из `response_json.get("answer", response_json).get("content")`.
7. **Генерация ответа**:
   - Если содержимое `content` существует:
     - Проверяется наличие сообщения об обнаружении злоупотребления `"Misuse detected. please get in touch"` в содержимом. Если оно присутствует, вызывается исключение `ValueError`.
     - Содержимое ответа передается через `yield content`, что делает функцию генератором.
     - Передается сигнал остановки `yield FinishReason("stop")`.

**Внутренние функции**: Нет

**ASCII Flowchart**:

```
    Начало
     ↓
Заголовки HTTP
     ↓
   Сессия
     ↓
Форматирование запроса
     ↓
  Подготовка данных
     ↓
   POST-запрос
     ↓
  Обработка ответа
     ↓
 Генерация ответа
     ↓
    Конец
```

**Примеры**:

```python
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

from src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt
from src.endpoints.gpt4free.g4f.typing import Messages, AsyncResult

async def main():
    # Пример 1: Простой запрос
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    async_generator: AsyncResult = Pizzagpt.create_async_generator(model=Pizzagpt.default_model, messages=messages)
    
    async for message in async_generator:
        print(message)

    # Пример 2: Использование прокси (если необходимо)
    messages: Messages = [{"role": "user", "content": "Tell me a joke."}]
    proxy: Optional[str] = "http://your_proxy:8080"  # Замените на свой прокси
    async_generator: AsyncResult = Pizzagpt.create_async_generator(model=Pizzagpt.default_model, messages=messages, proxy=proxy)
    
    async for message in async_generator:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())