# Модуль `DuckDuckGo`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo AI через библиотеку `duckduckgo_search`. Он позволяет генерировать ответы на основе предоставленных сообщений, используя различные модели, поддерживаемые DuckDuckGo. Модуль также включает поддержку авторизации через `nodriver` для получения необходимых токенов.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-моделями, предоставляемыми DuckDuckGo. Он использует библиотеку `duckduckgo_search` для взаимодействия с API DuckDuckGo и `nodriver` для авторизации.

Модуль предоставляет асинхронный генератор, который позволяет получать ответы от чат-бота DuckDuckGo по частям, что полезно для потоковой передачи больших объемов текста.

## Классы

### `DuckDuckGo`

**Описание**: Класс `DuckDuckGo` предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo AI. Он поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Duck.ai (duckduckgo_search)"`.
- `url` (str): URL чат-бота DuckDuckGo, `"https://duckduckgo.com/aichat"`.
- `api_base` (str): Базовый URL API DuckDuckGo, `"https://duckduckgo.com/duckchat/v1/"`.
- `working` (bool): Указывает, работает ли провайдер, `False`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу, `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения, `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений, `True`.
- `default_model` (str): Модель, используемая по умолчанию, `"gpt-4o-mini"`.
- `models` (list[str]): Список поддерживаемых моделей.
- `ddgs` (DDGS): Инстанс класса `DDGS` из библиотеки `duckduckgo_search`.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:
Класс использует библиотеку `duckduckgo_search` для взаимодействия с API DuckDuckGo. Он предоставляет метод `create_async_generator`, который создает асинхронный генератор для получения ответов от чат-бота. Класс также поддерживает авторизацию через `nodriver` для получения необходимых токенов.

### Методы класса

#### `create_async_generator`

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
            model (str): Название модели для использования.
            messages (Messages): Список сообщений для отправки чат-боту.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            timeout (int, optional): Максимальное время ожидания ответа в секундах. По умолчанию `60`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от чат-бота.

        Raises:
            ImportError: Если не установлена библиотека `duckduckgo_search`.

        
        - Проверяет, установлена ли библиотека `duckduckgo_search`. Если нет, вызывает исключение `ImportError`.
        - Инициализирует инстанс `DDGS` (если он еще не инициализирован) с использованием предоставленного прокси и времени ожидания.
        - Получает название модели, используя метод `get_model`.
        - Итерируется по ответам, возвращаемым методом `chat_yield` инстанса `DDGS`, и передает их в генератор.

        Внутренние функции:
        - Отсутствуют

        Примеры:
            >>> async for chunk in DuckDuckGo.create_async_generator(model="gpt-4o-mini", messages=[{"role": "user", "content": "Hello"}]):
            ...     print(chunk)
        """
        ...
```

#### `nodriver_auth`

```python
    @classmethod
    async def nodriver_auth(cls, proxy: str = None):
        """Аутентифицируется на сайте DuckDuckGo с использованием `nodriver` для получения токенов.

        Args:
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        
        - Запускает браузер с использованием `get_nodriver`.
        - Определяет функцию `on_request`, которая перехватывает запросы к API DuckDuckGo и извлекает токены `X-Vqd-4`, `X-Vqd-Hash-1` и `F-Fe-Version`.
        - Включает перехват запросов в браузере.
        - Добавляет обработчик для перехвата запросов.
        - Открывает страницу чат-бота DuckDuckGo.
        - Ожидает, пока не будет получен токен `_chat_vqd`.
        - Закрывает страницу и останавливает браузер.

        Внутренние функции:
        - `on_request(event: nodriver.cdp.network.RequestWillBeSent, page=None)`:
            - Перехватывает запросы к API DuckDuckGo.
            - Извлекает токены `X-Vqd-4`, `X-Vqd-Hash-1` и `F-Fe-Version` из заголовков запроса.
            - Присваивает извлеченные токены атрибутам `_chat_vqd`, `_chat_vqd_hash` и `_chat_xfe` инстанса `ddgs`.

        Примеры:
            >>> await DuckDuckGo.nodriver_auth(proxy="http://proxy:8080")
        """
        ...
```

## Параметры класса

- `label` (str): Метка провайдера.
- `url` (str): URL чат-бота DuckDuckGo.
- `api_base` (str): Базовый URL API DuckDuckGo.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.
- `ddgs` (DDGS): Инстанс класса `DDGS` из библиотеки `duckduckgo_search`.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

## Примеры

```python
# Пример использования класса DuckDuckGo
import asyncio
from typing import List, Dict

from g4f.Provider.DuckDuckGo import DuckDuckGo

async def main():
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello"}]
    model: str = "gpt-4o-mini"
    async for chunk in DuckDuckGo.create_async_generator(model=model, messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())