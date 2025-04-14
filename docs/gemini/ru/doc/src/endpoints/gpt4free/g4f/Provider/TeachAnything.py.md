# Модуль для взаимодействия с TeachAnything API

## Обзор

Модуль предоставляет класс `TeachAnything`, который является асинхронным провайдером для работы с API TeachAnything. Он позволяет генерировать текст на основе предоставленных сообщений, используя модели Gemini.

## Подробней

Этот модуль используется для интеграции с сервисом TeachAnything, предоставляя возможность использования моделей Gemini для генерации текста. Он отправляет запросы к API TeachAnything и возвращает сгенерированный текст в асинхронном режиме. Модуль поддерживает работу через прокси и устанавливает таймауты для запросов.

## Классы

### `TeachAnything`

**Описание**: Класс для взаимодействия с API TeachAnything.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `url` (str): URL сервиса TeachAnything.
- `api_endpoint` (str): Endpoint для генерации текста.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (List[str]): Список поддерживаемых моделей (`gemini-1.5-pro`, `gemini-1.5-flash`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения текста от API.
- `_get_headers`: Возвращает словарь с заголовками для HTTP-запросов.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str | None = None,
    **kwargs: Any
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения текста от API TeachAnything.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (Optional[str], optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs (Any): Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий текст от API.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса.

    Как работает функция:
    - Получает заголовки для запроса.
    - Форматирует сообщения для отправки в API.
    - Отправляет POST-запрос к API TeachAnything с использованием `aiohttp.ClientSession`.
    - Получает ответ от API и итерируется по чанкам контента.
    - Декодирует каждый чанк в кодировке UTF-8 и выдает его через генератор.
    - Обрабатывает возможные ошибки декодирования, накапливая данные в буфере, пока не получится декодировать.
    - Если после завершения итерации в буфере остаются данные, пытается их декодировать и выдать.
    - Логирует ошибки при декодировании финального буфера.
    """
    ...
```

**Примеры**:

```python
# Пример вызова функции create_async_generator
model = "gemini-1.5-pro"
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
# async for chunk in TeachAnything.create_async_generator(model=model, messages=messages):
#     print(chunk, end="")
```

### `_get_headers`

```python
@staticmethod
def _get_headers() -> Dict[str, str]:
    """
    Возвращает словарь с заголовками для HTTP-запросов.

    Returns:
        Dict[str, str]: Словарь с заголовками.

    Как работает функция:
    - Возвращает словарь, содержащий набор HTTP-заголовков, необходимых для взаимодействия с API TeachAnything.
    - Заголовки включают Accept, Accept-Language, Cache-Control, Content-Type и другие стандартные заголовки,
      а также специфичные для TeachAnything, такие как Origin, Referer и User-Agent.
    """
    ...
```

## Параметры класса

- `url` (str): URL сервиса TeachAnything.
- `api_endpoint` (str): Endpoint для генерации текста.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (List[str]): Список поддерживаемых моделей (`gemini-1.5-pro`, `gemini-1.5-flash`).

**Примеры**:

```python
# Пример определения класса и работы с классом
# from ..typing import Messages
# messages: Messages = [{"role": "user", "content": "Hello!"}]
# TeachAnything.create_async_generator(model='gemini-1.5-pro', messages=messages)