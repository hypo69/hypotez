# Модуль `GeminiPro.py`

## Обзор

Модуль `GeminiPro.py` предназначен для взаимодействия с API Google Gemini. Он предоставляет асинхронный генератор для получения ответов от модели Gemini, поддерживает историю сообщений и системные подсказки. Модуль требует аутентификации через API-ключ и может работать с мультимедийными данными.

## Подробней

Этот модуль является частью проекта `hypotez` и отвечает за интеграцию с моделями Google Gemini. Он предоставляет функциональность для отправки запросов к API Gemini и получения ответов в асинхронном режиме. Модуль поддерживает как потоковую, так и не потоковую генерацию контента, а также позволяет передавать мультимедийные данные вместе с текстовыми сообщениями.

## Классы

### `GeminiPro`

**Описание**: Класс `GeminiPro` предоставляет интерфейс для взаимодействия с API Google Gemini.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера "Google Gemini API".
- `url` (str): URL главной страницы Google AI.
- `login_url` (str): URL для получения API-ключа.
- `api_base` (str): Базовый URL API Gemini.
- `working` (bool): Индикатор работоспособности провайдера (True).
- `supports_message_history` (bool): Поддержка истории сообщений (True).
- `supports_system_message` (bool): Поддержка системных сообщений (True).
- `needs_auth` (bool): Требуется аутентификация (True).
- `default_model` (str): Модель по умолчанию ("gemini-1.5-pro").
- `default_vision_model` (str): Модель для работы с изображениями (совпадает с `default_model`).
- `fallback_models` (list[str]): Список запасных моделей.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:
Класс `GeminiPro` использует асинхронные запросы для взаимодействия с API Google Gemini. Он поддерживает как потоковую, так и не потоковую генерацию контента. Для аутентификации требуется API-ключ, который можно получить на сайте Google AI Studio. Класс также поддерживает отправку мультимедийных данных вместе с текстовыми сообщениями.

**Методы**:
- `get_models()`: Получает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от модели Gemini.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = api_base) -> list[str]:
    """
    Получает список доступных моделей Gemini.

    Args:
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API. По умолчанию используется значение атрибута `api_base` класса.

    Returns:
        list[str]: Список доступных моделей.

    Raises:
        MissingAuthError: Если `api_key` не указан и не удается получить список моделей.

    Example:
        >>> GeminiPro.get_models(api_key='YOUR_API_KEY')
        ['gemini-1.5-pro', 'gemini-pro', ...]
    """
    ...
```

**Назначение**: Получение списка доступных моделей Gemini.

**Параметры**:
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL API. По умолчанию используется значение атрибута `api_base` класса.

**Возвращает**:
- `list[str]`: Список доступных моделей.

**Вызывает исключения**:
- `MissingAuthError`: Если `api_key` не указан и не удается получить список моделей.

**Как работает функция**:
Функция `get_models` отправляет GET-запрос к API Gemini для получения списка доступных моделей. Если API-ключ не указан, функция пытается использовать запасные модели. Если запрос завершается неудачей и API-ключ не указан, вызывается исключение `MissingAuthError`.

**Примеры**:
```python
# Пример получения списка моделей с использованием API-ключа
models = GeminiPro.get_models(api_key='YOUR_API_KEY')
print(models)

# Пример получения списка моделей без API-ключа (используются запасные модели)
models = GeminiPro.get_models()
print(models)
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = False,
    proxy: str = None,
    api_key: str = None,
    api_base: str = api_base,
    use_auth_header: bool = False,
    media: MediaListType = None,
    tools: Optional[list] = None,
    connector: BaseConnector = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от модели Gemini.

    Args:
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в модель.
        stream (bool, optional): Флаг, указывающий на использование потоковой генерации. По умолчанию `False`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API. По умолчанию используется значение атрибута `api_base` класса.
        use_auth_header (bool, optional): Флаг, указывающий на использование заголовка авторизации. По умолчанию `False`.
        media (MediaListType, optional): Список мультимедийных данных для отправки. По умолчанию `None`.
        tools (Optional[list], optional): Список инструментов для использования. По умолчанию `None`.
        connector (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в модель.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели Gemini.

    Raises:
        MissingAuthError: Если `api_key` не указан.
        RuntimeError: Если возникает ошибка при запросе к API.

    Example:
        >>> async for response in GeminiPro.create_async_generator(model='gemini-1.5-pro', messages=[{'role': 'user', 'content': 'Hello'}], api_key='YOUR_API_KEY'):
        ...     print(response)
    """
    ...
```

**Назначение**: Создание асинхронного генератора для получения ответов от модели Gemini.

**Параметры**:
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки в модель.
- `stream` (bool, optional): Флаг, указывающий на использование потоковой генерации. По умолчанию `False`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL API. По умолчанию используется значение атрибута `api_base` класса.
- `use_auth_header` (bool, optional): Флаг, указывающий на использование заголовка авторизации. По умолчанию `False`.
- `media` (MediaListType, optional): Список мультимедийных данных для отправки. По умолчанию `None`.
- `tools` (Optional[list], optional): Список инструментов для использования. По умолчанию `None`.
- `connector` (BaseConnector, optional): Aiohttp коннектор. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для передачи в модель.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от модели Gemini.

**Вызывает исключения**:
- `MissingAuthError`: Если `api_key` не указан.
- `RuntimeError`: Если возникает ошибка при запросе к API.

**Как работает функция**:
Функция `create_async_generator` создает асинхронный генератор для взаимодействия с API Google Gemini. Она принимает список сообщений, модель для использования, флаг потоковой генерации, URL прокси-сервера и API-ключ. Функция формирует запрос к API Gemini и возвращает асинхронный генератор, который возвращает ответы от модели. Если происходит ошибка при запросе к API, вызывается исключение `RuntimeError`.

Внутренние действия функции включают:
1. Проверка наличия `api_key` и вызов исключения `MissingAuthError`, если ключ отсутствует.
2. Определение способа аутентификации (через заголовок или параметры запроса).
3. Формирование структуры данных для отправки в API, включая сообщения, мультимедийные данные и инструменты.
4. Отправка POST-запроса к API Gemini с использованием `aiohttp.ClientSession`.
5. Обработка ответа от API:
   - Если включена потоковая генерация (`stream=True`), функция обрабатывает чанки данных и возвращает их через генератор.
   - Если потоковая генерация отключена (`stream=False`), функция возвращает ответ целиком.
6. В случае ошибки при запросе к API, функция вызывает исключение `RuntimeError`.

**Примеры**:
```python
# Пример создания асинхронного генератора и получения ответов
async def main():
    messages = [{'role': 'user', 'content': 'Напиши небольшое стихотворение о весне.'}]
    async for response in GeminiPro.create_async_generator(model='gemini-1.5-pro', messages=messages, api_key='YOUR_API_KEY'):
        print(response)

import asyncio
asyncio.run(main())
```

## Параметры класса

- `label` (str): Метка провайдера "Google Gemini API".
- `url` (str): URL главной страницы Google AI.
- `login_url` (str): URL для получения API-ключа.
- `api_base` (str): Базовый URL API Gemini.
- `working` (bool): Индикатор работоспособности провайдера (True).
- `supports_message_history` (bool): Поддержка истории сообщений (True).
- `supports_system_message` (bool): Поддержка системных сообщений (True).
- `needs_auth` (bool): Требуется аутентификация (True).
- `default_model` (str): Модель по умолчанию ("gemini-1.5-pro").
- `default_vision_model` (str): Модель для работы с изображениями (совпадает с `default_model`).
- `fallback_models` (list[str]): Список запасных моделей.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.