# Модуль Hashnode

## Обзор

Модуль `Hashnode` предоставляет асинхронный генератор для взаимодействия с сервисом Hashnode. Он позволяет выполнять поисковые запросы и получать ответы от AI моделей через API Hashnode. Модуль поддерживает GPT-3.5 Turbo и может использовать историю сообщений.

## Подробнее

Этот модуль предназначен для интеграции с платформой Hashnode, используя её API для обработки запросов к AI моделям. Он включает в себя функциональность для выполнения веб-поиска и получения результатов, которые затем используются для генерации ответов.

## Классы

### `Hashnode`

**Описание**: Класс `Hashnode` является асинхронным провайдером генератора, который взаимодействует с API Hashnode для получения ответов от AI моделей.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL сервиса Hashnode ("https://hashnode.com").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (в данном случае `True`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку GPT-3.5 Turbo (в данном случае `True`).
- `_sources` (list): Список источников, полученных в результате поиска.

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для получения ответов от AI моделей Hashnode.
- `get_sources`: Возвращает список источников, использованных для генерации ответа.

### `SearchTypes`
**Описание**: Класс содержит типы поиска, которые могут быть использованы в модуле.
**Атрибуты**:
- `quick` (str): Тип быстрого поиска
- `code` (str): Тип поиска кода
- `websearch` (str): Тип веб-поиска

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    search_type: str = SearchTypes.websearch,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от AI моделей Hashnode.

    Args:
        model (str): Название используемой модели AI.
        messages (Messages): Список сообщений, представляющих историю разговора.
        search_type (str, optional): Тип поиска, который будет использоваться. По умолчанию `SearchTypes.websearch`.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий чанки данных ответа.

    Raises:
        aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP запроса.

    Как работает функция:
    - Функция устанавливает заголовки для HTTP-запроса.
    - Извлекает последний запрос пользователя из истории сообщений.
    - Выполняет поиск, если `search_type` равен "websearch".
    - Формирует данные для запроса к API Hashnode.
    - Отправляет POST-запрос к API Hashnode и получает ответ в виде асинхронного генератора чанков данных.
    """
```

### `get_sources`

```python
@classmethod
def get_sources(cls) -> list:
    """
    Возвращает список источников, использованных для генерации ответа.

    Returns:
        list: Список словарей, содержащих информацию об источниках (название и URL).

    Как работает функция:
    - Функция преобразует список `cls._sources` в список словарей, содержащих название и URL источника.
    """
```

## Параметры класса

- `model` (str): Название используемой модели AI.
- `messages` (Messages): Список сообщений, представляющих историю разговора.
- `search_type` (str, optional): Тип поиска, который будет использоваться. По умолчанию `SearchTypes.websearch`.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.

## Примеры

```python
# Пример использования create_async_generator
# (Код для примера, требует наличия асинхронного контекста)
# async def main():
#     model = "gpt-3.5-turbo"
#     messages = [{"role": "user", "content": "What is the capital of France?"}]
#     async for chunk in Hashnode.create_async_generator(model=model, messages=messages):
#         print(chunk, end="")

# Пример использования get_sources
# sources = Hashnode.get_sources()
# print(sources)