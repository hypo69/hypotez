# Модуль для работы с ChatGPT Free

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с сервисом ChatGPT Free. Он позволяет отправлять запросы к модели и получать ответы в виде асинхронного генератора. Модуль поддерживает выбор модели, передачу прокси и cookies.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с сервисом ChatGPT Free. Он использует асинхронные запросы для эффективного взаимодействия с API и предоставляет удобный интерфейс для получения ответов в виде генератора.

## Классы

### `ChatgptFree`

**Описание**: Класс `ChatgptFree` предоставляет асинхронный интерфейс для взаимодействия с сервисом ChatGPT Free.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Добавляет поддержку выбора и управления моделями.

**Атрибуты**:
- `url` (str): URL сервиса ChatGPT Free.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `_post_id` (str | None): ID поста, используемый для запросов.
- `_nonce` (str | None): Nonce, используемый для защиты от CSRF.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от ChatGPT Free.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    cookies: dict = None,
    **kwargs
) -> AsyncGenerator[str, None]:
    """Создает асинхронный генератор для получения ответов от ChatGPT Free.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Максимальное время ожидания ответа в секундах. По умолчанию 120.
        cookies (dict, optional): Cookie для отправки с запросом. По умолчанию `None`.

    Returns:
        AsyncGenerator[str, None]: Асинхронный генератор, выдающий части ответа от ChatGPT Free.

    Raises:
        RuntimeError: Если не удается получить `post_id` или `nonce` со страницы.
        Exception: Если возникает ошибка при выполнении запроса.

    Внутренние функции:
        Нет
    Как работает функция:
        1.  Устанавливает заголовки запроса, включая User-Agent, Referer и Origin.
        2.  Инициализирует асинхронную сессию с использованием `StreamSession` из `requests`.
        3.  Если `_nonce` не установлен, выполняет GET-запрос на главную страницу для получения `post_id` и `nonce`.
        4.  Форматирует запросы, используя функцию `format_prompt` из `helper`.
        5.  Выполняет POST-запрос к API ChatGPT Free с данными, включая `_wpnonce`, `post_id`, `message` и другие параметры.
        6.  Обрабатывает ответ, получая данные из потока и извлекая содержимое из JSON.
        7.  Если ответ приходит в формате `data: [DONE]`, завершает генератор.
        8.  В случае ошибок декодирования JSON или других проблем, продолжает обработку.
    """
    ...
```

## Параметры класса

- `url` (str): URL сервиса ChatGPT Free.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `_post_id` (str | None): ID поста, используемый для запросов.
- `_nonce` (str | None): Nonce, используемый для защиты от CSRF.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

## Примеры

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working import ChatgptFree
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for message in ChatgptFree.create_async_generator(model="gpt-4o-mini-2024-07-18", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())