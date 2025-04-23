# Модуль `ChatAnywhere`

## Обзор

Модуль `ChatAnywhere` предоставляет асинхронный генератор для взаимодействия с сервисом `chatanywhere.cn`. Он поддерживает модель `gpt-3.5-turbo` и сохраняет историю сообщений.

## Подробней

Модуль предназначен для интеграции с сервисом `chatanywhere.cn` для получения ответов от языковой модели. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов.

## Классы

### `ChatAnywhere`

**Описание**: Класс `ChatAnywhere` является асинхронным провайдером генератора.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL сервиса `chatanywhere.cn`.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от сервиса.

## Методы класса

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
    """Создает асинхронный генератор для получения ответов от сервиса chatanywhere.cn.

    Args:
        cls: Ссылка на класс.
        model (str): Модель для использования (в данном случае всегда gpt-3.5-turbo).
        messages (Messages): Список сообщений для отправки в запросе.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа в секундах. По умолчанию 120.
        temperature (float, optional): Температура модели. По умолчанию 0.5.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от сервиса.

    Raises:
        Exception: В случае ошибки при выполнении HTTP-запроса.

    Принцип работы:
        - Формирует заголовки запроса, включая `User-Agent`, `Content-Type` и `Authorization`.
        - Создает сессию `aiohttp.ClientSession` с заданными заголовками и таймаутом.
        - Формирует данные запроса в формате JSON, включая список сообщений, идентификатор, заголовок, температуру и модель.
        - Выполняет POST-запрос к сервису `chatanywhere.cn/v1/chat/gpt/`.
        - Итерируется по чанкам ответа и декодирует их, выдавая в виде асинхронного генератора.

    Внутренние функции:
        - Отсутствуют

    """
```

## Параметры класса

- `model` (str): Модель для использования. В данном коде ожидается `gpt-3.5-turbo`.
- `messages` (Messages): Список сообщений, отправляемых в запросе.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `timeout` (int, optional): Максимальное время ожидания ответа в секундах. По умолчанию 120.
- `temperature` (float, optional): Параметр температуры, влияющий на случайность генерируемого текста. По умолчанию 0.5.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы.

## Примеры

Пример вызова функции `create_async_generator`:

```python
# from src.endpoints.gpt4free.g4f.Provider.deprecated import ChatAnywhere
# messages = [{"role": "user", "content": "Hello, World!"}]
# async for chunk in ChatAnywhere.create_async_generator(model="gpt-3.5-turbo", messages=messages):
#     print(chunk, end="")