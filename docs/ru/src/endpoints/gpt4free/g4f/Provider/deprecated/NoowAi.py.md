# Модуль `NoowAi`

## Обзор

Модуль `NoowAi` предоставляет асинхронный генератор для взаимодействия с моделью NoowAI. Он поддерживает историю сообщений и модель GPT-3.5 Turbo. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов к API NoowAI.

## Подробней

Этот модуль предназначен для интеграции с сервисом NoowAI для генерации текста на основе предоставленных сообщений. Он отправляет запросы к API NoowAI и обрабатывает ответы в режиме реального времени, предоставляя результаты в виде асинхронного генератора.

## Классы

### `NoowAi`

**Описание**: Класс `NoowAi` предоставляет функциональность для взаимодействия с API NoowAI.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует от `AsyncGeneratorProvider`, что позволяет использовать его как асинхронный генератор.

**Атрибуты**:
- `url` (str): URL сервиса NoowAI (`https://noowai.com`).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (в данном случае `True`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo (в данном случае `True`).
- `working` (bool): Указывает, работает ли провайдер (в данном случае `False`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API NoowAI.

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
    """Создает асинхронный генератор для взаимодействия с API NoowAI.

    Args:
        cls (NoowAi): Класс NoowAi.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API NoowAI.

    Raises:
        RuntimeError: Если происходит ошибка при обработке ответа от API NoowAI.
    """
```

**Назначение**: Создает асинхронный генератор, который отправляет сообщения в API NoowAI и возвращает ответы в реальном времени.

**Параметры**:
- `cls` (NoowAi): Ссылка на класс `NoowAi`.
- `model` (str): Идентификатор используемой модели.
- `messages` (Messages): Список сообщений, отправляемых в API NoowAI.
- `proxy` (str, optional): Адрес прокси-сервера для использования (если необходимо). По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от API NoowAI.

**Вызывает исключения**:
- `RuntimeError`: Если возникает ошибка при обработке ответа от API NoowAI.

**Как работает функция**:

1. **Определение заголовков**:
   - Определяются заголовки HTTP-запроса, включая `User-Agent`, `Accept`, `Accept-Language`, `Referer`, `Content-Type`, `Origin`, `Alt-Used`, и `Connection`.

2. **Создание сессии `aiohttp`**:
   - Создается асинхронная сессия `aiohttp` с заданными заголовками.

3. **Подготовка данных**:
   - Формируется словарь `data` с параметрами запроса, включая `botId`, `customId`, `session`, `chatId`, `contextId`, `messages`, `newMessage`, и `stream`.

4. **Отправка POST-запроса**:
   - Отправляется POST-запрос к API NoowAI (`f"{cls.url}/wp-json/mwai-ui/v1/chats/submit`) с данными в формате JSON.

5. **Обработка ответа**:
   - Читаются строки из ответа в асинхронном режиме.
   - Если строка начинается с `b"data: "`:
     - Извлекается JSON из строки и проверяется наличие ключа `"type"`.
     - Если `line["type"] == "live"`, извлекаются данные (`line["data"]`) и возвращаются через генератор.
     - Если `line["type"] == "end"`, завершается работа генератора.
     - Если `line["type"] == "error"`, вызывается исключение `RuntimeError` с данными об ошибке.

```
A: Определение заголовков и создание сессии aiohttp
|
B: Формирование данных запроса
|
C: Отправка POST-запроса к API NoowAI
|
D: Обработка ответа от API NoowAI
|
E: Извлечение данных из ответа
|
F: Генерация данных или завершение
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import AsyncGenerator, List, Dict

async def process_noowai_response(model: str, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """Пример обработки ответа от NoowAi."""
    async for response in NoowAi.create_async_generator(model=model, messages=messages):
        yield response

async def main():
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for message in process_noowai_response(model="default", messages=messages):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())