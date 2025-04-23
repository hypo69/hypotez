# Модуль `GeminiPro.py`

## Обзор

Модуль `GeminiPro.py` предназначен для работы с API Google Gemini. Он предоставляет асинхронный генератор для создания контента с использованием моделей Gemini, поддерживает историю сообщений и системные сообщения. Модуль требует аутентификации через API ключ.

## Более подробно

Модуль предоставляет класс `GeminiPro`, который является асинхронным провайдером и включает в себя методы для получения списка моделей, создания асинхронного генератора для запросов к API Gemini. Он также обрабатывает мультимедийные данные и инструменты для генерации контента.

## Классы

### `GeminiPro`

**Описание**: Класс `GeminiPro` предоставляет функциональность для взаимодействия с API Google Gemini.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Google Gemini API").
- `url` (str): URL главной страницы Google AI ("https://ai.google.dev").
- `login_url` (str): URL для получения API ключа ("https://aistudio.google.com/u/0/apikey").
- `api_base` (str): Базовый URL API ("https://generativelanguage.googleapis.com/v1beta").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (True).
- `default_model` (str): Модель, используемая по умолчанию ("gemini-1.5-pro").
- `default_vision_model` (str): Модель для обработки изображений, используемая по умолчанию (default_model).
- `fallback_models` (list[str]): Список резервных моделей.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:

Класс `GeminiPro` использует API Google Gemini для генерации контента на основе предоставленных сообщений и параметров. Он поддерживает потоковую передачу данных, обработку мультимедийных файлов и использование инструментов для расширения функциональности. Класс также предоставляет методы для получения списка доступных моделей и обработки ошибок аутентификации.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = api_base) -> list[str]:
    """
    Получает список доступных моделей Gemini.

    Args:
        api_key (str, optional): API ключ для аутентификации. По умолчанию None.
        api_base (str, optional): Базовый URL API. По умолчанию значение атрибута класса `api_base`.

    Returns:
        list[str]: Список имен доступных моделей.

    Raises:
        MissingAuthError: Если API ключ недействителен.

    """
```

**Как работает**:

Функция `get_models` отправляет GET-запрос к API Google Gemini для получения списка доступных моделей. Она использует API ключ для аутентификации и обрабатывает ответ, извлекая имена моделей, поддерживающих метод `generateContent`. Если запрос не удался или API ключ недействителен, функция может вернуть список резервных моделей.

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
    Создает асинхронный генератор для взаимодействия с API Gemini.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        stream (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию False.
        proxy (str, optional): URL прокси-сервера. По умолчанию None.
        api_key (str, optional): API ключ для аутентификации. По умолчанию None.
        api_base (str, optional): Базовый URL API. По умолчанию значение атрибута класса `api_base`.
        use_auth_header (bool, optional): Флаг, указывающий на использование заголовка Authorization для аутентификации. По умолчанию False.
        media (MediaListType, optional): Список мультимедийных данных для отправки. По умолчанию None.
        tools (Optional[list], optional): Список инструментов для расширения функциональности. По умолчанию None.
        connector (BaseConnector, optional): HTTP коннектор для использования. По умолчанию None.
        **kwargs: Дополнительные параметры для конфигурации генерации.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты из API.

    Raises:
        MissingAuthError: Если отсутствует API ключ.
        RuntimeError: Если возникает ошибка при взаимодействии с API.

    """
```

**Как работает**:

Функция `create_async_generator` создает асинхронный генератор для взаимодействия с API Gemini. Она принимает модель, список сообщений, параметры потоковой передачи, прокси, API ключ и другие параметры конфигурации. Функция формирует запрос к API, включая сообщения, мультимедийные данные и инструменты, и отправляет его с использованием `aiohttp.ClientSession`. Если потоковая передача включена, функция обрабатывает чанки данных и возвращает их как асинхронный генератор. В случае ошибки функция вызывает исключение `RuntimeError`.

## Примеры

### Пример использования `get_models`

```python
api_key = "<your_api_key>"  # Замените на ваш API ключ
try:
    models = GeminiPro.get_models(api_key=api_key)
    print(f"Доступные модели: {models}")
except MissingAuthError as ex:
    print(f"Ошибка аутентификации: {ex}")
except Exception as ex:
    print(f"Произошла ошибка: {ex}")
```

### Пример использования `create_async_generator`

```python
import asyncio
from src.logger import logger  # Убедитесь, что путь к модулю logger правильный

async def main():
    api_key = "<your_api_key>"  # Замените на ваш API ключ
    messages = [
        {"role": "user", "content": "Напиши короткий рассказ о космосе."}
    ]

    try:
        generator = await GeminiPro.create_async_generator(
            model="gemini-1.5-pro",
            messages=messages,
            api_key=api_key,
            stream=True
        )

        async for chunk in generator:
            print(chunk, end="")

    except MissingAuthError as ex:
        logger.error(f"Ошибка аутентификации: {ex}", ex, exc_info=True)
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}", ex, exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())