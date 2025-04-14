# Модуль для работы с Meta AI Account
## Обзор

Модуль `MetaAIAccount.py` предназначен для аутентификации и взаимодействия с Meta AI с использованием учетной записи. Он расширяет функциональность класса `MetaAI` и реализует методы для создания асинхронного генератора, который отправляет запросы к Meta AI с использованием предоставленных учетных данных (cookies).

## Подробней

Этот модуль является частью системы, которая обеспечивает доступ к различным моделям искусственного интеллекта через API. Он специализируется на работе с Meta AI, требующей аутентификации через cookies. Модуль использует `get_cookies` для получения cookies из домена `.meta.ai`, а затем использует их для аутентифицированных запросов.

## Классы

### `MetaAIAccount`

**Описание**: Класс `MetaAIAccount` расширяет класс `MetaAI` и предоставляет функциональность для взаимодействия с Meta AI с использованием аутентификации через учетную запись (cookies).

**Наследует**: `MetaAI`

**Атрибуты**:
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования данного провайдера. Всегда `True` для `MetaAIAccount`.
- `parent` (str): Указывает родительский класс. Всегда `"MetaAI"` для `MetaAIAccount`.
- `image_models` (list[str]): Список поддерживаемых моделей изображений. Содержит `"meta"`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с Meta AI.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    cookies: Cookies = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с Meta AI.

    Args:
        cls (MetaAIAccount): Ссылка на класс.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в Meta AI.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от Meta AI.

    Как работает функция:
        1. Проверяет, предоставлены ли cookies. Если нет, пытается получить их из домена `.meta.ai`.
        2. Создает экземпляр класса `MetaAIAccount` с использованием прокси (если указан).
        3. Форматирует список сообщений для отправки в Meta AI.
        4. Отправляет запрос к Meta AI через метод `prompt`.
        5. Возвращает асинхронный генератор, который выдает чанки ответов от Meta AI.

    """
    cookies = get_cookies(".meta.ai", True, True) if cookies is None else cookies
    async for chunk in cls(proxy).prompt(format_prompt(messages), cookies):
        yield chunk
```

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для отправки в Meta AI.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от Meta AI.

**Примеры**:

```python
# Пример вызова функции create_async_generator
model_name = "meta-model"
messages_list = [{"role": "user", "content": "Hello, Meta AI!"}]
proxy_address = "http://proxy.example.com"
cookies_dict = {"session_id": "12345", "user_token": "abcdef"}

async def main():
    generator = MetaAIAccount.create_async_generator(
        model=model_name,
        messages=messages_list,
        proxy=proxy_address,
        cookies=cookies_dict
    )
    async for chunk in await generator:
        print(chunk)

# Запуск примера (в асинхронном контексте)
# import asyncio
# asyncio.run(main())