# Модуль: OpenaiTemplate

## Обзор

Модуль `OpenaiTemplate` предоставляет шаблон для взаимодействия с API OpenAI. Он включает в себя асинхронную поддержку генерации текста и изображений, обработку ошибок и другие полезные функции. Модуль является частью проекта `hypotez` и предназначен для упрощения интеграции с различными моделями OpenAI.

## Подробнее

Модуль содержит класс `OpenaiTemplate`, который наследуется от `AsyncGeneratorProvider`, `ProviderModelMixin` и `RaiseErrorMixin`. Он предоставляет методы для получения списка моделей, создания асинхронного генератора для запросов к API OpenAI и формирования заголовков запросов.

## Классы

### `OpenaiTemplate`

**Описание**: Класс предоставляет шаблон для взаимодействия с API OpenAI.

**Наследуется от**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Содержит методы для работы с моделями.
- `RaiseErrorMixin`: Добавляет функциональность обработки ошибок.

**Атрибуты**:
- `api_base` (str): Базовый URL API OpenAI.
- `api_key` (str): Ключ API для аутентификации.
- `api_endpoint` (str): Конечная точка API для запросов.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `supports_system_message` (bool): Поддержка системных сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `fallback_models` (list[str]): Список моделей для переключения в случае ошибки.
- `sort_models` (bool): Флаг для сортировки моделей.
- `ssl` (bool): Флаг для проверки SSL.

**Принцип работы**:
Класс `OpenaiTemplate` предназначен для упрощения взаимодействия с API OpenAI. Он предоставляет методы для получения списка доступных моделей, создания асинхронных генераторов для отправки запросов и обработки ответов от API. Класс также обрабатывает ошибки и предоставляет возможность использования прокси и других параметров запроса.

**Методы**:
- `get_models(api_key: str = None, api_base: str = None) -> list[str]`: Возвращает список доступных моделей.
- `create_async_generator(...) -> AsyncResult`: Создает асинхронный генератор для запросов к API OpenAI.
- `get_headers(stream: bool, api_key: str = None, headers: dict = None) -> dict`: Формирует заголовки запроса.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = None) -> list[str]:
    """
    Получает список доступных моделей из API OpenAI.

    Args:
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API OpenAI. По умолчанию `None`.

    Returns:
        list[str]: Список доступных моделей.

    Raises:
        Exception: Если происходит ошибка при получении списка моделей.
    """
    # Функция извлекает список моделей из API OpenAI.
    # Если список моделей еще не был получен, функция выполняет запрос к API.
    # В случае ошибки возвращается список fallback_models.
    ...
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    media: MediaListType = None,
    api_key: str = None,
    api_endpoint: str = None,
    api_base: str = None,
    temperature: float = None,
    max_tokens: int = None,
    top_p: float = None,
    stop: Union[str, list[str]] = None,
    stream: bool = False,
    prompt: str = None,
    headers: dict = None,
    impersonate: str = None,
    extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"],
    extra_data: dict = {},
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для запросов к API OpenAI.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `120`.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        api_endpoint (str, optional): Конечная точка API для запросов. По умолчанию `None`.
        api_base (str, optional): Базовый URL API OpenAI. По умолчанию `None`.
        temperature (float, optional): Температура для контроля случайности генерации. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
        top_p (float, optional): Top P для контроля случайности генерации. По умолчанию `None`.
        stop (Union[str, list[str]], optional): Список стоп-слов. По умолчанию `None`.
        stream (bool, optional): Использовать потоковую передачу данных. По умолчанию `False`.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.
        impersonate (str, optional): Имя пользователя для имитации. По умолчанию `None`.
        extra_parameters (list[str], optional): Список дополнительных параметров.
        extra_data (dict, optional): Дополнительные данные для отправки. По умолчанию `{}`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от API.

    Raises:
        MissingAuthError: Если отсутствует ключ API.
        ResponseError: Если получен неподдерживаемый тип контента.
    """
    # Функция создает асинхронный генератор для отправки запросов к API OpenAI.
    # Она обрабатывает различные параметры запроса, такие как модель, сообщения, прокси и т. д.
    # В случае успеха возвращается асинхронный генератор, который позволяет получать ответы от API в потоковом режиме.
    ...
```

### `get_headers`

```python
@classmethod
def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
    """
    Формирует заголовки запроса.

    Args:
        stream (bool): Использовать потоковую передачу данных.
        api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.

    Returns:
        dict: Словарь с заголовками запроса.
    """
    # Функция формирует заголовки запроса, включая Accept и Content-Type.
    # Если указан ключ API, добавляется заголовок Authorization.
    # Дополнительные заголовки объединяются с основными.
    ...
```

## Параметры класса

- `api_base` (str): Базовый URL API OpenAI.
- `api_key` (str): Ключ API для аутентификации.
- `api_endpoint` (str): Конечная точка API для запросов.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `supports_system_message` (bool): Поддержка системных сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `fallback_models` (list[str]): Список моделей для переключения в случае ошибки.
- `sort_models` (bool): Флаг для сортировки моделей.
- `ssl` (bool): Флаг для проверки SSL.

## Примеры

Пример использования класса `OpenaiTemplate` для получения списка моделей:

```python
from src.endpoints.gpt4free.g4f.Provider.template.OpenaiTemplate import OpenaiTemplate

models = OpenaiTemplate.get_models(api_key="ваш_api_ключ")
print(models)
```

Пример использования класса `OpenaiTemplate` для создания асинхронного генератора:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.template.OpenaiTemplate import OpenaiTemplate

async def main():
    messages = [{"role": "user", "content": "Hello, world!"}]
    generator = await OpenaiTemplate.create_async_generator(model="gpt-3.5-turbo", messages=messages, api_key="ваш_api_ключ")
    async for message in generator:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())