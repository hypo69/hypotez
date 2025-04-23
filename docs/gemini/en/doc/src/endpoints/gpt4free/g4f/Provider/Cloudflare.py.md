# Документация для модуля `Cloudflare`

## Обзор

Модуль `Cloudflare` предназначен для взаимодействия с API Cloudflare AI. Он предоставляет асинхронный генератор для получения ответов от моделей Cloudflare AI. Модуль поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

## Более подробно

Модуль использует `nodriver` для получения аргументов сессии, если он доступен. В противном случае используются стандартные заголовки и куки. Модуль также кэширует аргументы сессии в файле для повторного использования.
В модуле реализована поддержка подмены моделей.

## Классы

### `Cloudflare`

**Описание**: Класс `Cloudflare` предоставляет асинхронный генератор для получения ответов от моделей Cloudflare AI.
**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.
- `AuthFileMixin`: Обеспечивает аутентификацию через файл.

**Атрибуты**:
- `label` (str): Метка провайдера ("Cloudflare AI").
- `url` (str): URL главной страницы Cloudflare AI ("https://playground.ai.cloudflare.com").
- `working` (bool): Флаг, указывающий, работает ли провайдер (True).
- `use_nodriver` (bool): Флаг, указывающий, использовать ли `nodriver` для получения аргументов сессии (True).
- `api_endpoint` (str): URL API для получения ответов ("https://playground.ai.cloudflare.com/api/inference").
- `models_url` (str): URL для получения списка моделей ("https://playground.ai.cloudflare.com/api/models").
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу ответов (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("@cf/meta/llama-3.3-70b-instruct-fp8-fast").
- `model_aliases` (dict): Псевдонимы моделей.
- `_args` (dict): Аргументы сессии.

**Принцип работы**:
1. При инициализации класса проверяется наличие кэшированных аргументов сессии.
2. Если кэшированные аргументы отсутствуют, модуль пытается получить их с помощью `nodriver`.
3. Если `nodriver` недоступен, используются стандартные заголовки и куки.
4. При создании асинхронного генератора отправляется POST-запрос к API Cloudflare AI.
5. Ответы от API передаются через асинхронный генератор.
6. Аргументы сессии кэшируются в файле для повторного использования.

### Методы класса
- `get_models(cls) -> str`: Получает список доступных моделей.
- `create_async_generator(...) -> AsyncResult`: Создает асинхронный генератор для получения ответов от моделей Cloudflare AI.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls) -> str:
    """
    Получает список доступных моделей из API Cloudflare.

    Args:
        cls: Класс Cloudflare.

    Returns:
        str: Список доступных моделей.

    Как работает функция:
    - Функция проверяет, если список моделей уже был получен и сохранен в атрибуте `cls.models`.
    - Если список моделей не был получен, функция пытается получить его из API Cloudflare.
    - Если `nodriver` доступен, функция использует его для получения аргументов сессии.
    - Если `nodriver` недоступен, используются стандартные заголовки и куки.
    - Функция отправляет GET-запрос к API Cloudflare и получает список моделей в формате JSON.
    - Список моделей сохраняется в атрибуте `cls.models` для повторного использования.
    """
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
    max_tokens: int = 2048,
    cookies: Cookies = None,
    timeout: int = 300,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от моделей Cloudflare AI.

    Args:
        cls: Класс Cloudflare.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 2048.
        cookies (Cookies, optional): Куки для отправки в API. По умолчанию None.
        timeout (int, optional): Время ожидания ответа от API. По умолчанию 300.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор для получения ответов от моделей Cloudflare AI.

    Как работает функция:
    - Функция создает асинхронный генератор, который отправляет POST-запрос к API Cloudflare и получает ответы в потоковом режиме.
    - Функция использует `nodriver` для получения аргументов сессии, если он доступен.
    - Функция кэширует аргументы сессии в файле для повторного использования.
    - Функция обрабатывает ответы от API и передает их через асинхронный генератор.
    - Функция обрабатывает ошибки, которые могут возникнуть при отправке запроса или получении ответа.

    Внутренние функции:
        - Нет внутренних функций.
    """
    ...
```

## Параметры класса

- `label` (str): Метка провайдера ("Cloudflare AI").
- `url` (str): URL главной страницы Cloudflare AI ("https://playground.ai.cloudflare.com").
- `working` (bool): Флаг, указывающий, работает ли провайдер (True).
- `use_nodriver` (bool): Флаг, указывающий, использовать ли `nodriver` для получения аргументов сессии (True).
- `api_endpoint` (str): URL API для получения ответов ("https://playground.ai.cloudflare.com/api/inference").
- `models_url` (str): URL для получения списка моделей ("https://playground.ai.cloudflare.com/api/models").
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу ответов (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель, используемая по умолчанию ("@cf/meta/llama-3.3-70b-instruct-fp8-fast").
- `model_aliases` (dict): Псевдонимы моделей.
- `_args` (dict): Аргументы сессии.

## Примеры

```python
# Пример использования класса Cloudflare
import asyncio

from src.endpoints.gpt4free.g4f.Provider.Cloudflare import Cloudflare
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    async for message in Cloudflare.create_async_generator(model="llama-2-7b", messages=messages):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())