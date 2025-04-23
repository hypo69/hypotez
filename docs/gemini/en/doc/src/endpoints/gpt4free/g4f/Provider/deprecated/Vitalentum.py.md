# Документация для модуля Vitalentum

## Обзор

Модуль `Vitalentum` предназначен для работы с асинхронным генератором, предоставляющим ответы от модели GPT-3.5 Turbo через API сервиса Vitalentum.io. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет функциональность для взаимодействия с API Vitalentum.

## Детали

Модуль содержит класс `Vitalentum`, который наследуется от `AsyncGeneratorProvider` и реализует метод `create_async_generator` для создания асинхронного генератора, возвращающего ответы от модели GPT-3.5 Turbo.

## Классы

### `Vitalentum`

**Описание**: Класс для взаимодействия с API Vitalentum и получения ответов от модели GPT-3.5 Turbo.
**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров генераторов.

**Атрибуты**:
- `url` (str): URL сервиса Vitalentum.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели GPT-3.5 Turbo.

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
    """Создает асинхронный генератор для получения ответов от модели GPT-3.5 Turbo.

    Args:
        cls (Vitalentum): Ссылка на класс `Vitalentum`.
        model (str): Имя модели, которую необходимо использовать (в данном случае GPT-3.5 Turbo).
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Как работает функция:
        1. Формирует заголовки HTTP-запроса, включая User-Agent, Accept, Origin и Referer.
        2. Преобразует список сообщений в формат, требуемый API Vitalentum.
        3. Формирует данные для отправки в API, включая историю разговора и температуру.
        4. Отправляет POST-запрос к API `https://app.vitalentum.io/api/converse-edge` с использованием `aiohttp.ClientSession`.
        5. Обрабатывает ответы, получаемые от API в формате `text/event-stream`.
        6. Извлекает содержимое ответа и передает его через генератор.

    Примеры:
        Пример вызова функции:

        ```python
        messages = [{"role": "user", "content": "Hello, Vitalentum!"}]
        async for message in Vitalentum.create_async_generator(model="gpt-3.5-turbo", messages=messages):
            print(message)
        ```
    """
```

## Параметры класса

- `url` (str): URL сервиса Vitalentum.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.

**Примеры**
```python
messages = [{"role": "user", "content": "Привет, Vitalentum!"}]
async for message in Vitalentum.create_async_generator(model="gpt-3.5-turbo", messages=messages):
    print(message)