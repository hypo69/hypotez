# Модуль DuckDuckGo

## Обзор

Модуль `DuckDuckGo.py` предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo AI через библиотеку `duckduckgo_search`. Он позволяет генерировать ответы чат-бота на основе предоставленных сообщений, используя различные модели, поддерживаемые DuckDuckGo.

## Более подробно

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, требующими доступа к возможностям чат-бота DuckDuckGo. Модуль использует библиотеку `duckduckgo_search` для выполнения запросов к API DuckDuckGo и асинхронные генераторы для обработки ответов в режиме реального времени.

## Классы

### `DuckDuckGo`

**Описание**: Класс `DuckDuckGo` предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo AI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Duck.ai (duckduckgo_search)").
- `url` (str): URL чат-бота DuckDuckGo ("https://duckduckgo.com/aichat").
- `api_base` (str): Базовый URL API DuckDuckGo ("https://duckduckgo.com/duckchat/v1/").
- `working` (bool): Указывает, работает ли провайдер (False).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель по умолчанию ("gpt-4o-mini").
- `models` (List[str]): Список поддерживаемых моделей.
- `ddgs` (DDGS): Экземпляр класса `DDGS` из библиотеки `duckduckgo_search` (инициализируется при первом использовании).
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:
Класс `DuckDuckGo` использует библиотеку `duckduckgo_search` для взаимодействия с API DuckDuckGo. Он предоставляет метод `create_async_generator` для создания асинхронного генератора, который возвращает ответы чат-бота. Класс также поддерживает авторизацию через `nodriver` для получения необходимых токенов для работы с API.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от чат-бота DuckDuckGo.
- `nodriver_auth`: Выполняет авторизацию через `nodriver` для получения токенов API.

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
        cls (DuckDuckGo): Ссылка на класс `DuckDuckGo`.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в чат-бот.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Максимальное время ожидания ответа в секундах. По умолчанию 60.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы чат-бота.

    Raises:
        ImportError: Если не установлена библиотека `duckduckgo_search`.
        DuckDuckGoSearchException: Если возникает ошибка при взаимодействии с API DuckDuckGo.

    Как работает функция:
    - Проверяет, установлена ли библиотека `duckduckgo_search`. Если нет, вызывает исключение `ImportError`.
    - Если `cls.ddgs` не инициализирован, создает экземпляр `DDGS` с указанными параметрами прокси и таймаута.
    - Получает название модели, используя метод `get_model`.
    - Извлекает последнее сообщение пользователя из списка сообщений с помощью функции `get_last_user_message`.
    - Вызывает метод `chat_yield` объекта `cls.ddgs` для получения асинхронного генератора ответов.
    - Передает каждый полученный фрагмент ответа через `yield`.

    Пример:
        >>> async for chunk in DuckDuckGo.create_async_generator(model="gpt-4o-mini", messages=[{"role": "user", "content": "Привет"}]):
        ...     print(chunk)
    """
```

### `nodriver_auth`

```python
@classmethod
async def nodriver_auth(cls, proxy: str = None):
    """Выполняет авторизацию через `nodriver` для получения токенов API.

    Args:
        cls (DuckDuckGo): Ссылка на класс `DuckDuckGo`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

    Raises:
        Exception: Если возникает ошибка при авторизации.

    Как работает функция:
    - Запускает браузер с помощью функции `get_nodriver` с указанным прокси.
    - Определяет функцию `on_request`, которая вызывается при каждом запросе.
    - Внутри `on_request` проверяет, содержит ли URL запроса `cls.api_base`.
    - Если содержит, извлекает значения заголовков "X-Vqd-4", "X-Vqd-Hash-1" и "F-Fe-Version" и сохраняет их в атрибутах `cls.ddgs._chat_vqd`, `cls.ddgs._chat_vqd_hash` и `cls.ddgs._chat_xfe` соответственно.
    - Включает перехват сетевых запросов в браузере с помощью `page.send(nodriver.cdp.network.enable())`.
    - Добавляет обработчик `on_request` для события `nodriver.cdp.network.RequestWillBeSent`.
    - Переходит по URL `cls.url` с помощью `browser.get(cls.url)`.
    - Ожидает, пока атрибут `cls.ddgs._chat_vqd` не будет установлен.
    - Закрывает страницу и останавливает браузер.

    Пример:
        >>> await DuckDuckGo.nodriver_auth()
    """
```

## Параметры класса

- `label` (str): Метка провайдера ("Duck.ai (duckduckgo_search)").
- `url` (str): URL чат-бота DuckDuckGo ("https://duckduckgo.com/aichat").
- `api_base` (str): Базовый URL API DuckDuckGo ("https://duckduckgo.com/duckchat/v1/").
- `working` (bool): Указывает, работает ли провайдер (False).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель по умолчанию ("gpt-4o-mini").
- `models` (List[str]): Список поддерживаемых моделей.
- `ddgs` (DDGS): Экземпляр класса `DDGS` из библиотеки `duckduckgo_search` (инициализируется при первом использовании).
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

## Примеры

Пример использования класса `DuckDuckGo` для получения ответа от чат-бота:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.DuckDuckGo import DuckDuckGo

async def main():
    async for chunk in DuckDuckGo.create_async_generator(model="gpt-4o-mini", messages=[{"role": "user", "content": "Привет"}]):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())