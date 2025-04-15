# Модуль `DarkAI.py`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с моделью DarkAI. Он позволяет генерировать текст на основе предоставленных сообщений, используя API DarkAI. Поддерживается потоковая передача данных.

## Подробней

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется генерация текста с использованием моделей DarkAI. Он обеспечивает асинхронное взаимодействие, что позволяет избежать блокировки основного потока выполнения.  Модуль использует `aiohttp` для асинхронных HTTP-запросов и `json` для обработки данных в формате JSON.

## Классы

### `DarkAI`

**Описание**: Класс `DarkAI` предоставляет функциональность для взаимодействия с API DarkAI. Он поддерживает асинхронную генерацию текста и потоковую передачу данных.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров, генерирующих данные.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями, такими как получение модели по имени.

**Атрибуты**:
- `url` (str): URL для взаимодействия с DarkAI.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения текста от DarkAI.

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
    """
    Создает асинхронный генератор для получения текста от DarkAI.

    Args:
        cls (DarkAI): Класс DarkAI.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в DarkAI.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий текст от DarkAI.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    Как работает функция:
    - Получает модель, используя `cls.get_model(model)`.
    - Формирует заголовки запроса, включая `accept`, `content-type` и `user-agent`.
    - Создает сессию `aiohttp.ClientSession` с заданными заголовками и таймаутом.
    - Форматирует запросы, используя `format_prompt(messages)`.
    - Отправляет POST-запрос к `cls.api_endpoint` с данными в формате JSON и прокси (если указан).
    - Обрабатывает ответ, читая его частями (chunks) по 1024 байта.
    - Разделяет полученные данные на строки и декодирует их.
    - Извлекает данные из JSON, если строка начинается с `'data: '`.
    - Если `chunk_data['event'] == 'text-chunk'`, извлекает текст и выдает его через `yield`.
    - Если `chunk_data['event'] == 'stream-end'`, завершает генератор.
    - Обрабатывает исключения `json.JSONDecodeError` и `Exception`, возникающие при обработке данных.
    """
    ...
```

**Параметры**:
- `cls` (DarkAI): Класс DarkAI.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для отправки в DarkAI.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, DarkAI!"}]
async for chunk in DarkAI.create_async_generator(model='gpt-3.5-turbo', messages=messages):
    print(chunk, end="")
```
```python
# Пример использования create_async_generator с прокси
messages = [{"role": "user", "content": "Hello, DarkAI!"}]
async for chunk in DarkAI.create_async_generator(model='gpt-3.5-turbo', messages=messages, proxy="http://proxy.example.com"):
    print(chunk, end="")