# Модуль `Opchatgpts.py`

## Обзор

Модуль предоставляет класс `Opchatgpts`, который является асинхронным генератором для взаимодействия с моделью Opchatgpts. Он поддерживает историю сообщений и GPT-3.5 Turbo.

## Подробней

Этот модуль предназначен для асинхронного взаимодействия с сервисом Opchatgpts, предоставляя функциональность для генерации ответов на основе предоставленных сообщений. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и обрабатывает потоковые ответы от сервера.

## Классы

### `Opchatgpts`

**Описание**: Класс `Opchatgpts` предоставляет асинхронный генератор для взаимодействия с моделью Opchatgpts.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL сервиса Opchatgpts.
- `working` (bool): Указывает, работает ли сервис.
- `supports_message_history` (bool): Поддерживает ли сервис историю сообщений.
- `supports_gpt_35_turbo` (bool): Поддерживает ли сервис GPT-3.5 Turbo.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от Opchatgpts.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None, **kwargs) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от Opchatgpts.

    Args:
        cls (Type[Opchatgpts]): Ссылка на класс.
        model (str): Название модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от Opchatgpts.

    Raises:
        RuntimeError: Если получен поврежденный ответ от сервера.

    Как работает функция:
    - Функция формирует заголовки запроса, включая User-Agent, Accept и Referer.
    - Создается сессия `aiohttp.ClientSession` с заданными заголовками.
    - Формируются данные для отправки в теле запроса, включая `botId`, `chatId`, `contextId`, `messages` и другие параметры.
    - Выполняется POST-запрос к API Opchatgpts.
    - Функция асинхронно обрабатывает ответ, проверяя каждую строку на наличие префикса `data: `.
    - Если строка содержит данные, она преобразуется из JSON и проверяется наличие ключа `type`.
    - В зависимости от типа (`live` или `end`) данные возвращаются через генератор или завершают его работу.
    - При возникновении ошибок в процессе обработки ответа, вызывается исключение `RuntimeError`.
    """
```

## Параметры класса

- `url` (str): URL сервиса Opchatgpts.
- `working` (bool): Указывает, работает ли сервис.
- `supports_message_history` (bool): Поддерживает ли сервис историю сообщений.
- `supports_gpt_35_turbo` (bool): Поддерживает ли сервис GPT-3.5 Turbo.

## Примеры

Пример использования класса `Opchatgpts` для создания асинхронного генератора:

```python
# Этот код является только демонстрацией и не может быть выполнен без соответствующей инфраструктуры.
# from src.endpoints.gpt4free.g4f.Provider.deprecated.Opchatgpts import Opchatgpts
# messages = [{"role": "user", "content": "Hello, world!"}]
# async for message in Opchatgpts.create_async_generator(model="gpt-3.5-turbo", messages=messages):
#     print(message)