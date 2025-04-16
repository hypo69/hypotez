# Модуль `DuckDuckGo.py`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo, используя библиотеку `duckduckgo_search`. Он позволяет генерировать ответы на основе предоставленных сообщений, поддерживая стриминг, системные сообщения и историю сообщений. Модуль также включает механизм аутентификации через `nodriver` для получения необходимых параметров для запросов к API.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-моделями через DuckDuckGo. Он использует асинхронные генераторы для обработки запросов и предоставляет возможность настройки прокси и таймаутов. Для корректной работы модуля требуется установка дополнительных библиотек, таких как `duckduckgo_search` и `nodriver`.

## Классы

### `DuckDuckGo`

**Описание**: Класс `DuckDuckGo` предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Duck.ai (duckduckgo_search)"`.
- `url` (str): URL чат-бота DuckDuckGo, `"https://duckduckgo.com/aichat"`.
- `api_base` (str): Базовый URL API DuckDuckGo, `"https://duckduckgo.com/duckchat/v1/"`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `False`.
- `supports_stream` (bool): Флаг, указывающий на поддержку стриминга, `True`.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений, `True`.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений, `True`.
- `default_model` (str): Модель по умолчанию, `"gpt-4o-mini"`.
- `models` (list): Список поддерживаемых моделей, `[default_model, "meta-llama/Llama-3.3-70B-Instruct-Turbo", "claude-3-haiku-20240307", "o3-mini", "mistralai/Mistral-Small-24B-Instruct-2501"]`.
- `ddgs` (DDGS): Инстанс класса `DDGS` из библиотеки `duckduckgo_search`, инициализируется при первом использовании.
- `model_aliases` (dict): Словарь псевдонимов моделей для удобства использования.

**Принцип работы**:
Класс `DuckDuckGo` предназначен для асинхронного взаимодействия с API DuckDuckGo. Он использует библиотеку `duckduckgo_search` для отправки запросов и получения ответов. Класс поддерживает стриминг ответов, системные сообщения и историю сообщений. Для корректной работы требуется установка библиотек `duckduckgo_search` и `nodriver`. Аутентификация выполняется через `nodriver` для получения необходимых параметров запроса.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 60,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от чат-бота DuckDuckGo.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в чат-бот.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа в секундах. По умолчанию `60`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий части ответа от чат-бота.

    Raises:
        ImportError: Если не установлена библиотека `duckduckgo_search`.

    Как работает функция:
        1. Проверяет, установлена ли библиотека `duckduckgo_search`. Если нет, вызывает исключение `ImportError`.
        2. Инициализирует `cls.ddgs` (если он еще не инициализирован) с использованием переданных прокси и таймаута.
        3. Получает фактическое название модели, используя метод `cls.get_model`.
        4. Использует `cls.ddgs.chat_yield` для получения асинхронного генератора, который возвращает части ответа от чат-бота.
        5. Передает каждый полученный фрагмент ответа через `yield`.

    """
```

### `nodriver_auth`

```python
@classmethod
async def nodriver_auth(cls, proxy: str = None):
    """Аутентифицируется на сайте DuckDuckGo с использованием `nodriver` для получения необходимых параметров запроса.

    Args:
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

    Как работает функция:
        1. Запускает браузер с использованием `get_nodriver` с переданным прокси.
        2. Устанавливает обработчик событий `on_request` для перехвата сетевых запросов.
        3. Переходит на URL чат-бота DuckDuckGo (`cls.url`).
        4. Ожидает, пока не будет получен параметр `cls.ddgs._chat_vqd` из заголовков запроса.
        5. Закрывает страницу и останавливает браузер.
    """
```

#### `on_request` (внутренняя функция `nodriver_auth`)

```python
def on_request(event: nodriver.cdp.network.RequestWillBeSent, page=None):
    """Обработчик событий для перехвата сетевых запросов и извлечения параметров аутентификации.

    Args:
        event (nodriver.cdp.network.RequestWillBeSent): Объект события сетевого запроса.
        page: Страница браузера (не используется напрямую).

    Как работает функция:
        1. Проверяет, содержит ли URL запроса базовый URL API (`cls.api_base`).
        2. Если содержит, извлекает параметры `X-Vqd-4`, `X-Vqd-Hash-1` и `F-Fe-Version` из заголовков запроса и сохраняет их в атрибутах `cls.ddgs`.
    """
```

## Параметры класса

- `label` (str): Метка провайдера.
- `url` (str): URL чат-бота DuckDuckGo.
- `api_base` (str): Базовый URL API DuckDuckGo.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку стриминга.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `ddgs` (DDGS): Инстанс класса `DDGS` из библиотеки `duckduckgo_search`.
- `model_aliases` (dict): Словарь псевдонимов моделей.

## Примеры

Пример использования класса `DuckDuckGo`:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.DuckDuckGo import DuckDuckGo
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    model = "gpt-4o-mini"

    async for chunk in DuckDuckGo.create_async_generator(model=model, messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())