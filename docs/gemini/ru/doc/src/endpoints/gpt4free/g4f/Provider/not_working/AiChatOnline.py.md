# Модуль AiChatOnline

## Обзор

Модуль `AiChatOnline` предоставляет класс `AiChatOnline`, реализующий асинхронный генератор ответов от модели `AiChatOnline` с использованием `aiohttp`. 

## Подробнее

- Модуль использует `aiohttp` для асинхронных запросов.
- Класс `AiChatOnline` реализует методы для получения токена, создания асинхронного генератора и отправки запросов.
- Модуль использует `format_prompt` для форматирования запросов и `get_random_string` для генерации уникальных идентификаторов.

## Классы

### `class AiChatOnline`

**Описание**: Класс `AiChatOnline` реализует асинхронный генератор ответов от модели `AiChatOnline`.

**Наследует**: 
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов ответов.
- `ProviderModelMixin`: Миксин, предоставляющий методы для работы с моделями.

**Атрибуты**:
- `site_url (str)`: URL-адрес сайта `AiChatOnline`.
- `url (str)`: URL-адрес API `AiChatOnline`.
- `api_endpoint (str)`: Точка входа API для чата.
- `working (bool)`: Флаг, указывающий на работоспособность модели.
- `default_model (str)`:  Название модели по умолчанию.

**Методы**:

- `grab_token(session: ClientSession, proxy: str)`: Асинхронный метод для получения токена.
    **Параметры**:
        - `session (ClientSession)`: Сессия `aiohttp` для отправки запросов.
        - `proxy (str)`: Прокси-сервер для запросов.
    **Возвращает**:
        - `str`: Токен доступа.
    **Вызывает исключения**:
        - `aiohttp.ClientError`: Если возникает ошибка при отправке запроса.

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Асинхронный метод для создания генератора ответов.
    **Параметры**:
        - `model (str)`:  Название модели.
        - `messages (Messages)`:  Список сообщений.
        - `proxy (str)`: Прокси-сервер для запросов.
    **Возвращает**:
        - `AsyncResult`: Асинхронный генератор ответов.
    **Вызывает исключения**:
        - `aiohttp.ClientError`: Если возникает ошибка при отправке запроса.
- `_get_response(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:  Асинхронный метод для отправки запроса к API.
    **Параметры**:
        - `model (str)`:  Название модели.
        - `messages (Messages)`:  Список сообщений.
        - `proxy (str)`: Прокси-сервер для запросов.
    **Возвращает**:
        - `AsyncResult`: Асинхронный генератор ответов.
    **Вызывает исключения**:
        - `aiohttp.ClientError`: Если возникает ошибка при отправке запроса.

## Параметры класса

- `site_url (str)`: URL-адрес сайта `AiChatOnline`.
- `url (str)`: URL-адрес API `AiChatOnline`.
- `api_endpoint (str)`: Точка входа API для чата.
- `working (bool)`: Флаг, указывающий на работоспособность модели.
- `default_model (str)`:  Название модели по умолчанию.

**Примеры**:

```python
# Создание инстанса класса
aichatonline = AiChatOnline(model='gpt-4o-mini')

# Создание асинхронного генератора ответов
async_generator = aichatonline.create_async_generator(
    model='gpt-4o-mini',
    messages=[
        {'role': 'user', 'content': 'Hello, world!'}
    ]
)

# Получение ответов из генератора
async for response in async_generator:
    print(f'Response: {response}')
```