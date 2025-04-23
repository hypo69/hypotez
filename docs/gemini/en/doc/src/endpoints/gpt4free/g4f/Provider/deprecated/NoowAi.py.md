# Module `NoowAi.py`

## Обзор

Модуль `NoowAi.py` представляет собой асинхронный провайдер для взаимодействия с сервисом NoowAi. Он позволяет генерировать ответы от модели GPT-3.5 Turbo и поддерживает историю сообщений. Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов.

## More details

Модуль предназначен для работы с API NoowAi, предоставляя функциональность для отправки сообщений и получения потоковых ответов. В модуле реализована поддержка прокси, что позволяет использовать его в различных сетевых конфигурациях.
Анализ кода показывает, что он отправляет POST-запросы к API NoowAi и обрабатывает потоковые ответы, разбирая JSON-формат данных.

## Classes

### `NoowAi`

**Описание**:
Класс `NoowAi` является асинхронным провайдером, который взаимодействует с API NoowAi для генерации ответов на основе модели GPT-3.5 Turbo.

**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров, генерирующих ответы.

**Атрибуты**:
- `url` (str): URL сервиса NoowAi.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.

**Working principle**:
Класс использует `aiohttp.ClientSession` для отправки асинхронных POST-запросов к API NoowAi. Он формирует заголовки и данные запроса, включая идентификаторы бота и чата, а также сообщения для модели. Полученные потоковые ответы разбираются, и извлекаются данные для генерации ответа.

## Class Methods

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
    Создает асинхронный генератор для взаимодействия с API NoowAi.

    Args:
        cls: Ссылка на класс.
        model (str): Используемая модель (например, "gpt-3.5-turbo").
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. Defaults to None.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        RuntimeError: Если получен некорректный ответ от API.
    """
    ...
```

**How the function works**:

1.  Формируются заголовки запроса, включая User-Agent, Accept, Referer и Content-Type.
2.  Создается `aiohttp.ClientSession` с заданными заголовками.
3.  Формируются данные запроса в формате JSON, включая идентификаторы бота и чата, контекст и сообщения.
4.  Отправляется POST-запрос к API NoowAi.
5.  Обрабатываются потоковые ответы, проверяется наличие префикса `data: `.
6.  JSON-ответ разбирается, проверяется наличие поля `type`.
7.  В зависимости от значения поля `type` генерируются данные, завершается генерация или выбрасывается исключение.

**Examples**:

```python
# Пример использования create_async_generator
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Привет, как дела?"}]
proxy = "http://proxy.example.com"

async for response in NoowAi.create_async_generator(model=model, messages=messages, proxy=proxy):
    print(response)
```

## Class Parameters

-   `url` (str): URL сервиса NoowAi, используемый для формирования запросов.
-   `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений для контекста диалога.
-   `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель GPT-3.5 Turbo.
-   `working` (bool): Флаг, указывающий, находится ли провайдер в рабочем состоянии.