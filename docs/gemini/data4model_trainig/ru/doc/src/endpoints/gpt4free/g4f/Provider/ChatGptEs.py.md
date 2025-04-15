# Модуль для работы с ChatGptEs
=====================================

Модуль :mod:`ChatGptEs` предоставляет асинхронный генератор для взаимодействия с сервисом ChatGptEs. Он включает в себя функциональность для обхода Cloudflare, отправки запросов и обработки ответов.

## Обзор

Модуль предназначен для работы с сервисом ChatGptEs для генерации текста на основе предоставленных сообщений. Он использует библиотеку `curl_cffi` для выполнения HTTP-запросов и обхода защиты Cloudflare.

## Подробней

Модуль предоставляет класс `ChatGptEs`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он поддерживает стриминг, но не поддерживает системные сообщения и историю сообщений.

## Классы

### `ChatGptEs`

**Описание**: Класс для взаимодействия с сервисом ChatGptEs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса ChatGptEs.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку стриминга.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o`).
- `models` (List[str]): Список поддерживаемых моделей (`gpt-4`, `gpt-4o`, `gpt-4o-mini`).
- `SYSTEM_PROMPT` (str): Системный запрос, используемый для форматирования сообщений.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от ChatGptEs.

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
    Создает асинхронный генератор для получения ответов от ChatGptEs.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от ChatGptEs.

    Raises:
        MissingRequirementsError: Если не установлен пакет `curl_cffi`.
        ValueError: Если получен неожиданный статус код или формат ответа.

    Как работает функция:
        1. Проверяет наличие установленного пакета `curl_cffi`.
        2. Получает название модели.
        3. Форматирует запрос, добавляя системное сообщение.
        4. Создает сессию `curl_cffi` с необходимыми заголовками.
        5. Если указан прокси, добавляет его в сессию.
        6. Отправляет первый запрос для получения `nonce` и `post_id`.
        7. Извлекает `nonce` и `post_id` из ответа, используя регулярные выражения.
        8. Генерирует `client_id`.
        9. Подготавливает данные для отправки в POST-запросе.
        10. Выполняет POST-запрос к API.
        11. Проверяет статус код ответа.
        12. Извлекает данные из JSON-ответа и передает их через генератор.

    """
    ...
```

## Параметры класса

- `model` (str): Название используемой модели (`gpt-4`, `gpt-4o`, `gpt-4o-mini`).
- `messages` (Messages): Список сообщений для отправки в формате `List[dict]`, где каждый словарь содержит ключи `role` и `content`.
- `proxy` (str, optional): URL прокси-сервера для использования при отправке запроса. По умолчанию `None`.

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator

async def main():
    model: str = "gpt-4o"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    proxy: str = "http://your_proxy:8080"  # Замените на ваш прокси-сервер

    try:
        async for response in ChatGptEs.create_async_generator(model=model, messages=messages, proxy=proxy):
            print(f"Response: {response}")
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    asyncio.run(main())