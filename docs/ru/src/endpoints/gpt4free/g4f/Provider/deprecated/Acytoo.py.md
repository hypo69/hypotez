# Модуль для работы с Acytoo API
======================================

Модуль предоставляет асинхронный генератор для взаимодействия с API Acytoo.
Он поддерживает ведение истории сообщений и работу с моделью `gpt-3.5-turbo`.

## Обзор

Модуль `Acytoo` предоставляет класс `Acytoo`, который является асинхронным провайдером генератора для взаимодействия с API Acytoo.
Этот модуль позволяет отправлять запросы к Acytoo API и получать ответы в виде асинхронного генератора.

## Подробнее

Модуль предназначен для упрощения взаимодействия с Acytoo API. Он предоставляет удобный интерфейс для отправки сообщений и получения ответов в асинхронном режиме.
Этот модуль используется для интеграции с сервисами, требующими взаимодействия с Acytoo API.

## Классы

### `Acytoo`

**Описание**: Класс `Acytoo` является асинхронным провайдером, который взаимодействует с API Acytoo.

**Принцип работы**:
Класс использует `aiohttp.ClientSession` для отправки асинхронных POST-запросов к API Acytoo и получает ответы в виде асинхронного генератора.

**Аттрибуты**:
- `url` (str): URL API Acytoo.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.

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
        Создает асинхронный генератор для взаимодействия с API Acytoo.

        Args:
            cls (Acytoo): Класс Acytoo.
            model (str): Модель для использования (в данном случае всегда 'gpt-3.5-turbo').
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.

        Raises:
            aiohttp.ClientResponseError: Если возникает HTTP ошибка при запросе к API.

        Как работает функция:
        1. Создает `aiohttp.ClientSession` с заголовками, полученными из `_create_header()`.
        2. Отправляет POST-запрос к API Acytoo (`f'{cls.url}/api/completions'`) с использованием `session.post()`.
        3. Передает прокси-сервер, если он указан.
        4. Формирует JSON-тело запроса с использованием `_create_payload()`.
        5. Обрабатывает ответ от API и генерирует поток данных, декодируя каждый чанк.

        ASCII flowchart:

        Создание сессии aiohttp
        │
        └──> Отправка POST-запроса к API Acytoo
             │
             └──> Обработка ответа и генерация потока данных

        Примеры:
            Пример 1: Создание асинхронного генератора без прокси.
            >>> async for message in Acytoo.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
            ...     print(message)

            Пример 2: Создание асинхронного генератора с прокси.
            >>> async for message in Acytoo.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], proxy='http://proxy.example.com'):
            ...     print(message)
        """
        async with ClientSession(
            headers=_create_header()
        ) as session:
            async with session.post(
                f'{cls.url}/api/completions',
                proxy=proxy,
                json=_create_payload(messages, **kwargs)
            ) as response:
                response.raise_for_status()
                async for stream in response.content.iter_any():
                    if stream:
                        yield stream.decode()
```

**Параметры**:
- `model` (str): Модель для использования (в данном случае всегда `gpt-3.5-turbo`).
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Если возникает HTTP ошибка при запросе к API.

## Функции

### `_create_header`

```python
def _create_header():
    """
    Создает заголовок для HTTP-запроса.

    Returns:
        dict: Словарь с заголовками.

    Как работает функция:

    Функция возвращает словарь, содержащий заголовки HTTP-запроса, необходимые для взаимодействия с API.

    ASCII flowchart:

    Создание заголовков
    │
    └──> Возврат словаря с заголовками

    Примеры:
        >>> _create_header()
        {'accept': '*/*', 'content-type': 'application/json'}
    """
    return {
        'accept': '*/*',
        'content-type': 'application/json',
    }
```

**Назначение**: Создает заголовок для HTTP-запроса.

**Возвращает**:
- `dict`: Словарь с заголовками.

**Как работает функция**:

Функция возвращает словарь, содержащий заголовки HTTP-запроса, необходимые для взаимодействия с API.

**ASCII flowchart**:

```
Создание заголовков
│
└──> Возврат словаря с заголовками
```

**Примеры**:

```python
>>> _create_header()
{'accept': '*/*', 'content-type': 'application/json'}
```

### `_create_payload`

```python
def _create_payload(messages: Messages, temperature: float = 0.5, **kwargs):
    """
    Создает полезную нагрузку (payload) для POST-запроса.

    Args:
        messages (Messages): Список сообщений для отправки.
        temperature (float, optional): Температура для генерации текста. По умолчанию 0.5.
        **kwargs: Дополнительные аргументы.

    Returns:
        dict: Словарь с полезной нагрузкой.

    Как работает функция:

    Функция формирует словарь, представляющий полезную нагрузку для POST-запроса к API. Она включает в себя ключ API, модель, сообщения и температуру.

    ASCII flowchart:

    Создание полезной нагрузки
    │
    └──> Формирование словаря с параметрами
         │
         └──> Возврат словаря

    Примеры:
        >>> _create_payload(messages=[{'role': 'user', 'content': 'Hello'}])
        {'key': '', 'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'Hello'}], 'temperature': 0.5, 'password': ''}
    """
    return {
        'key'         : '',
        'model'       : 'gpt-3.5-turbo',
        'messages'    : messages,
        'temperature' : temperature,
        'password'    : ''
    }
```

**Назначение**: Создает полезную нагрузку (payload) для POST-запроса.

**Параметры**:
- `messages` (Messages): Список сообщений для отправки.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию 0.5.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `dict`: Словарь с полезной нагрузкой.

**Как работает функция**:

Функция формирует словарь, представляющий полезную нагрузку для POST-запроса к API. Она включает в себя ключ API, модель, сообщения и температуру.

**ASCII flowchart**:

```
Создание полезной нагрузки
│
└──> Формирование словаря с параметрами
     │
     └──> Возврат словаря
```

**Примеры**:

```python
>>> _create_payload(messages=[{'role': 'user', 'content': 'Hello'}])
{'key': '', 'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'Hello'}], 'temperature': 0.5, 'password': ''}