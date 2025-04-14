# Модуль CodeLinkAva
## Обзор

Модуль `CodeLinkAva` предоставляет асинхронный генератор для взаимодействия с API CodeLink Ava. Он используется для получения ответов от языковой модели в режиме реального времени (стриминга).

## Подробнее

Модуль содержит класс `CodeLinkAva`, который наследуется от `AsyncGeneratorProvider` и предназначен для работы с API CodeLink Ava. Он отправляет запросы к API и генерирует ответы, получаемые в режиме реального времени.
Располагается в `hypotez/src/endpoints/gpt4free/g4f/Provider/deprecated/` и служит для предоставления одного из способов взаимодействия с языковой моделью, в данном случае через CodeLink Ava.

## Классы

### `CodeLinkAva`

**Описание**: Класс `CodeLinkAva` предоставляет асинхронный генератор для взаимодействия с API CodeLink Ava.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL API CodeLink Ava.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `working` (bool): Указывает, работает ли провайдер в данный момент.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от API.

## Методы класса

### `create_async_generator`

```python
async def create_async_generator(
    cls,
    model: str,
    messages: list[dict[str, str]],
    **kwargs
) -> AsyncGenerator:
    """Создает асинхронный генератор для получения ответов от API CodeLink Ava.

    Args:
        cls: Ссылка на класс.
        model (str): Название модели.
        messages (list[dict[str, str]]): Список сообщений для отправки в API.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        AsyncGenerator: Асинхронный генератор, выдающий контент ответов от API.

    Raises:
        aiohttp.ClientResponseError: Если возникает HTTP ошибка при запросе к API.

    Как работает функция:
    - Формирует заголовки запроса, включая User-Agent, Accept и Referer.
    - Открывает асинхронную сессию с использованием aiohttp.ClientSession.
    - Формирует данные запроса, включая сообщения, температуру и флаг стриминга.
    - Отправляет POST запрос к API CodeLink Ava.
    - Обрабатывает ответ, декодирует его и извлекает контент из JSON.
    - Генерирует контент ответа, пока не получит сообщение о завершении.

    Внутренние функции:
        Отсутствуют.

    Примеры:
        Пример 1:
        ```python
        model = "gpt-3.5-turbo"
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        async for content in CodeLinkAva.create_async_generator(model, messages):
            print(content, end="")
        ```
    """
    ...
```
## Параметры класса

- `url` (str): URL API CodeLink Ava. Значение по умолчанию: `"https://ava-ai-ef611.web.app"`.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo. Значение по умолчанию: `True`.
- `working` (bool): Указывает, работает ли провайдер в данный момент. Значение по умолчанию: `False`.