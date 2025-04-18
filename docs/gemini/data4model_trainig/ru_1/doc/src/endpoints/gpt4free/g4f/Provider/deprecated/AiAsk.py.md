# Модуль AiAsk

## Обзор

Модуль `AiAsk` предоставляет асинхронный генератор для взаимодействия с сервисом AiAsk (e.aiask.me). Он поддерживает ведение истории сообщений и модель GPT-3.5 Turbo.

## Подробней

Модуль предназначен для асинхронного обмена сообщениями с использованием API AiAsk. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет результаты в виде асинхронного генератора.

## Классы

### `AiAsk(AsyncGeneratorProvider)`

**Описание**: Класс `AiAsk` является провайдером для асинхронной генерации ответов от модели AiAsk.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует функциональность асинхронного генератора провайдера.

**Атрибуты**:
- `url` (str): URL сервиса AiAsk (`https://e.aiask.me`).
- `supports_message_history` (bool): Указывает, что провайдер поддерживает историю сообщений (значение `True`).
- `supports_gpt_35_turbo` (bool): Указывает, что провайдер поддерживает модель GPT-3.5 Turbo (значение `True`).
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии (значение `False`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для обмена сообщениями с AiAsk.

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
    """
    Создает асинхронный генератор для обмена сообщениями с AiAsk.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от AiAsk.

    Raises:
        RuntimeError: Если достигнут лимит запросов (Rate limit reached).

    """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API AiAsk.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Модель, которую необходимо использовать.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): Адрес прокси-сервера (если требуется). По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, такие как `temperature`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, предоставляющий ответы от AiAsk.

**Как работает функция**:

1. **Подготовка заголовков**: Определяются заголовки HTTP-запроса, включая `accept`, `origin` и `referer`.
2. **Создание сессии**: Используется `aiohttp.ClientSession` для выполнения асинхронных запросов.
3. **Формирование данных**: Подготавливаются данные для отправки в теле запроса, включая историю сообщений, параметры модели и прочие настройки.
4. **Выполнение запроса**: Отправляется POST-запрос к API AiAsk (`/v1/chat/gpt/`) с использованием указанных заголовков, данных и прокси (если указан).
5. **Обработка ответа**: Читаются данные из ответа чанками, декодируются и передаются через генератор. Проверяется наличие сообщения о достижении лимита запросов.
6. **Обработка лимита запросов**: Если достигнут лимит запросов, выбрасывается исключение `RuntimeError`.

**Примеры**:

Пример использования асинхронного генератора:

```python
async def main():
    messages = [{"role": "user", "content": "Hello, AiAsk!"}]
    async for message in AiAsk.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

# Запуск примера
# import asyncio
# asyncio.run(main())
```

## Параметры класса

- `url` (str): URL сервиса AiAsk.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `supports_gpt_35_turbo` (bool): Поддержка модели GPT-3.5 Turbo.
- `working` (bool): Статус работы провайдера.