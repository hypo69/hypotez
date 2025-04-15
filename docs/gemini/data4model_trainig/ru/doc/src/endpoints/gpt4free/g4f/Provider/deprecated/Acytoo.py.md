# Модуль для работы с провайдером Acytoo (Устаревший)

## Обзор

Модуль предоставляет класс `Acytoo`, который является асинхронным генераторным провайдером для взаимодействия с сервисом chat.acytoo.com. Этот класс устарел. Он поддерживает GPT-3.5 Turbo и предоставляет функциональность для работы с историей сообщений.

## Подробней

Модуль предназначен для организации асинхронного взаимодействия с API Acytoo. Он использует `aiohttp` для выполнения HTTP-запросов и предоставляет методы для создания и отправки запросов к API. Модуль также включает функции для формирования заголовков и полезной нагрузки запросов.

## Классы

### `Acytoo`

**Описание**: Класс `Acytoo` является асинхронным генераторным провайдером для взаимодействия с API chat.acytoo.com.

**Наследует**:
- `AsyncGeneratorProvider`: Наследует от базового класса `AsyncGeneratorProvider`.

**Атрибуты**:
- `url` (str): URL-адрес сервиса chat.acytoo.com.
- `working` (bool): Указывает, работает ли провайдер в данный момент. Всегда `False`, так как класс устарел.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API.

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
    """Создает асинхронный генератор для взаимодействия с API Acytoo.

    Args:
        cls (Acytoo): Ссылка на класс.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Как работает функция:
    - Создает асинхронную сессию `aiohttp.ClientSession` с заголовками, полученными из `_create_header()`.
    - Отправляет POST-запрос к API `f'{cls.url}/api/completions'` с использованием `session.post()`.
    - В случае успешного ответа, итерируется по содержимому ответа (`response.content.iter_any()`) и декодирует каждый чанк (`stream.decode()`).
    - Возвращает декодированные чанки в виде асинхронного генератора.

    Примеры:
        >>> async for message in Acytoo.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
        ...     print(message)
    """
    ...
```

## Функции

### `_create_header`

```python
def _create_header() -> dict:
    """Создает заголовки для HTTP-запроса.

    Returns:
        dict: Словарь с заголовками.

    Как работает функция:
    - Формирует словарь с заголовками `accept` и `content-type`.
    - Возвращает словарь.
    """
    ...
```

### `_create_payload`

```python
def _create_payload(messages: Messages, temperature: float = 0.5, **kwargs) -> dict:
    """Создает полезную нагрузку (payload) для HTTP-запроса.

    Args:
        messages (Messages): Список сообщений для отправки.
        temperature (float, optional): Температура для генерации текста. По умолчанию `0.5`.
        **kwargs: Дополнительные аргументы.

    Returns:
        dict: Словарь с данными для отправки в теле запроса.

    Как работает функция:
    - Формирует словарь с параметрами `key`, `model`, `messages`, `temperature` и `password`.
    - Возвращает словарь.
    """
    ...