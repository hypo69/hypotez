# Модуль `ChatAnywhere.py`

## Обзор

Модуль `ChatAnywhere.py` предоставляет асинхронный генератор для взаимодействия с сервисом ChatAnywhere (<https://chatanywhere.cn>).
Он поддерживает модель GPT-3.5 Turbo и хранение истории сообщений. Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов.

## Подробнее

Этот модуль предназначен для интеграции с сервисом ChatAnywhere, позволяя отправлять запросы и получать ответы в асинхронном режиме.
Он особенно полезен для приложений, требующих потоковой обработки ответов от языковой модели.

## Классы

### `ChatAnywhere`

**Описание**:
Класс `ChatAnywhere` является провайдером асинхронного генератора. Он определяет URL, поддерживает GPT-3.5 Turbo и хранение истории сообщений.

**Наследует**:
- `AsyncGeneratorProvider`: Этот класс наследуется от `AsyncGeneratorProvider` и предоставляет функциональность асинхронной генерации.

**Атрибуты**:
- `url` (str): URL сервиса ChatAnywhere (`https://chatanywhere.cn`).
- `supports_gpt_35_turbo` (bool): Поддержка модели GPT-3.5 Turbo (всегда `True`).
- `supports_message_history` (bool): Поддержка хранения истории сообщений (всегда `True`).
- `working` (bool): Указывает, работает ли провайдер (изначально `False`).

**Принцип работы**:

Класс предоставляет метод `create_async_generator`, который отправляет сообщения в ChatAnywhere API и возвращает асинхронный генератор, который выдает чанки данных из ответа.

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
    """Создает асинхронный генератор для взаимодействия с ChatAnywhere.

    Args:
        cls (type[ChatAnywhere]): Ссылка на класс `ChatAnywhere`.
        model (str): Имя модели (не используется).
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания HTTP-запроса в секундах. По умолчанию 120.
        temperature (float, optional): Температура для генерации текста. По умолчанию 0.5.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий чанки данных из ответа.

    Raises:
        Exception: Если возникает ошибка при выполнении HTTP-запроса.
    """
```

**Параметры**:
- `cls` (type[ChatAnywhere]): Ссылка на класс `ChatAnywhere`.
- `model` (str): Имя модели (не используется).
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания HTTP-запроса в секундах. По умолчанию 120.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию 0.5.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий чанки данных из ответа.

**Как работает функция**:

Функция `create_async_generator` создает асинхронный генератор для взаимодействия с API ChatAnywhere. Она выполняет следующие шаги:

1. **Формирует заголовки HTTP-запроса**:
   - Устанавливает User-Agent, Accept, Accept-Language, Content-Type, Referer, Origin и другие необходимые заголовки.

2. **Создает асинхронную сессию `aiohttp`**:
   - Использует `ClientSession` для выполнения HTTP-запросов с заданными заголовками и временем ожидания.

3. **Формирует данные запроса**:
   - Создает словарь `data`, содержащий список сообщений, идентификатор, заголовок, температуру и другие параметры.

4. **Выполняет POST-запрос к API**:
   - Отправляет POST-запрос к `f"{cls.url}/v1/chat/gpt/"` с данными в формате JSON.

5. **Обрабатывает ответ**:
   - Итерируется по чанкам данных из ответа и декодирует их.
   - Выдает декодированные чанки данных через генератор.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, ChatAnywhere!"}]
async def example():
    async for chunk in ChatAnywhere.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(chunk, end="")

import asyncio
asyncio.run(example())