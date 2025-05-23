# Модуль Cromicle

## Обзор

Модуль Cromicle представляет собой асинхронный провайдер для взаимодействия с сервисом Cromicle.top.
Он использует `aiohttp` для выполнения асинхронных HTTP-запросов. Модуль предназначен для генерации
текста на основе предоставленных сообщений, имитируя работу с API Cromicle.

## Подробней

Модуль содержит класс `Cromicle`, который наследует `AsyncGeneratorProvider` и переопределяет
метод `create_async_generator` для отправки запросов к API Cromicle и получения потоковых ответов.
Также в модуле определены две вспомогательные функции: `_create_header` для создания заголовков запроса
и `_create_payload` для формирования полезной нагрузки запроса.

## Классы

### `Cromicle`

**Описание**: Класс `Cromicle` является асинхронным провайдером, предназначенным для взаимодействия
с сервисом Cromicle.top. Он наследует функциональность от `AsyncGeneratorProvider`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url` (str): URL-адрес сервиса Cromicle.top.
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo` (по умолчанию `True`).

**Методы**:

- `create_async_generator`: Асинхронный генератор для создания потока данных из API Cromicle.

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
    """ Функция создает асинхронный генератор для взаимодействия с API Cromicle.

    Args:
        cls: Ссылка на класс.
        model (str): Модель, используемая для генерации.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования при отправке запроса. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий данные из API.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса.

    
    - Функция принимает модель, сообщения и прокси (опционально).
    - Создает заголовок запроса с помощью функции `_create_header`.
    - Отправляет POST-запрос к API Cromicle с использованием `aiohttp.ClientSession`.
    - Формирует JSON-тело запроса с помощью функции `_create_payload`.
    - Итерирует по потоку данных, полученному от API, и декодирует каждый чанк.
    - Возвращает асинхронный генератор, который выдает декодированные чанки данных.

    Внутренние функции:
        Отсутствуют

    Примеры:
        Примеры вызова со всем спектром параметров. которы можно передать в функцию. В данном коде примеров нет.
    """
    ...
```

## Функции

### `_create_header`

```python
def _create_header() -> Dict[str, str]:
    """ Функция создает заголовок запроса для API Cromicle.

    Returns:
        Dict[str, str]: Словарь с заголовками запроса.

    
    - Функция создает словарь с заголовками `accept` и `content-type`.
    - Возвращает этот словарь.

    Внутренние функции:
        Отсутствуют

    Примеры:
        Примеры вызова со всем спектром параметров. которы можно передать в функцию. В данном коде примеров нет.
    """
    ...
```

### `_create_payload`

```python
def _create_payload(message: str) -> Dict[str, str]:
    """ Функция создает полезную нагрузку (payload) для запроса к API Cromicle.

    Args:
        message (str): Сообщение для отправки в API.

    Returns:
        Dict[str, str]: Словарь с данными для отправки в теле запроса.

    
    - Функция принимает сообщение.
    - Создает SHA256-хеш из конкатенации строки 'abc' и сообщения.
    - Формирует словарь с сообщением, токеном 'abc' и вычисленным хешем.
    - Возвращает этот словарь.

    Внутренние функции:
        Отсутствуют

    Примеры:
        Примеры вызова со всем спектром параметров. которы можно передать в функцию. В данном коде примеров нет.
    """
    ...
```