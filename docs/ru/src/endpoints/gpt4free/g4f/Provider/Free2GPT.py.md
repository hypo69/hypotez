# Модуль `Free2GPT`

## Обзор

Модуль предоставляет асинхронный класс `Free2GPT`, предназначенный для взаимодействия с сервисом `chat10.free2gpt.xyz`. Он позволяет генерировать ответы на основе предоставленных сообщений, используя модели `gemini-1.5-pro` и `gemini-1.5-flash`. Модуль поддерживает прокси и историю сообщений.

## Подробней

Этот модуль является частью проекта `hypotez` и отвечает за интеграцию с сервисом `Free2GPT` для получения ответов от языковых моделей. Он использует асинхронные запросы для эффективной работы и предоставляет возможность выбора модели.

## Классы

### `Free2GPT`

**Описание**: Асинхронный класс, предоставляющий интерфейс для взаимодействия с сервисом `Free2GPT`.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:

- `url` (str): URL сервиса `Free2GPT` - `https://chat10.free2gpt.xyz`.
- `working` (bool): Индикатор работоспособности провайдера (по умолчанию `True`).
- `supports_message_history` (bool): Поддержка истории сообщений (по умолчанию `True`).
- `default_model` (str): Модель, используемая по умолчанию - `'gemini-1.5-pro'`.
- `models` (List[str]): Список поддерживаемых моделей - `['gemini-1.5-pro', 'gemini-1.5-flash']`.

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для получения ответов от сервиса.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    connector: BaseConnector = None,
    **kwargs,
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от сервиса Free2GPT.

    Args:
        model (str): Модель для использования (например, 'gemini-1.5-pro').
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
        connector (BaseConnector, optional): Aiohttp коннектор. По умолчанию None.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от сервиса.

    Raises:
        RateLimitError: Если достигнут лимит запросов.
        Exception: При других ошибках при выполнении запроса.
    """
```

**Назначение**: Создает асинхронный генератор, который отправляет сообщения в сервис `Free2GPT` и возвращает ответы в виде чанков.

**Параметры**:

- `cls` (class): Ссылка на класс `Free2GPT`.
- `model` (str): Модель для использования (например, 'gemini-1.5-pro').
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `connector (BaseConnector, optional)`: Объект коннектора `aiohttp`. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, возвращающий ответы от сервиса.

**Вызывает исключения**:

- `RateLimitError`: Если достигнут лимит запросов.
- `Exception`: При других ошибках при выполнении запроса.

**Как работает функция**:

1.  **Подготовка заголовков**: Формируются заголовки HTTP-запроса, включая `User-Agent`, `Content-Type`, `Referer` и `Origin`.
2.  **Создание сессии**: Создается асинхронная сессия `aiohttp` с использованием предоставленного коннектора или прокси.
3.  **Формирование данных**: Создается словарь `data`, включающий сообщения, временную метку и подпись, сгенерированную функцией `generate_signature`.
4.  **Отправка запроса**: Отправляется POST-запрос к сервису `Free2GPT` с данными в формате JSON.
5.  **Обработка ответа**:
    *   Проверяется статус ответа. Если статус равен 500 и в тексте ответа содержится "Quota exceeded", выбрасывается исключение `RateLimitError`.
    *   В противном случае, вызывается функция `raise_for_status` для проверки статуса ответа.
    *   Извлекаются чанки из тела ответа и декодируются.
6.  **Генерация результатов**: Каждый декодированный чанк возвращается через `yield`.

```mermaid
graph TD
    A[Подготовка заголовков] --> B(Создание сессии aiohttp);
    B --> C{Формирование данных (messages, time, sign)};
    C --> D[Отправка POST запроса в Free2GPT];
    D --> E{Проверка статуса ответа};
    E -- 500 и "Quota exceeded" --> F[Выброс RateLimitError];
    E -- OK --> G[Извлечение и декодирование чанков];
    G --> H(yield chunk);
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.typing import Messages
from src.endpoints.gpt4free.g4f.Provider.base_provider import AsyncGeneratorProvider

async def main():
    model = "gemini-1.5-pro"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = None
    async for chunk in AsyncGeneratorProvider.create_async_generator(model=model, messages=messages, proxy=proxy):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Функции

### `generate_signature`

```python
def generate_signature(time: int, text: str, secret: str = ""):
    """
    Генерирует подпись для запроса к сервису Free2GPT.

    Args:
        time (int): Временная метка.
        text (str): Текст сообщения.
        secret (str, optional): Секретный ключ. По умолчанию "".

    Returns:
        str: Подпись в виде SHA256 хеша.
    """
```

**Назначение**: Генерирует SHA256 хеш для подписи запроса.

**Параметры**:

- `time` (int): Временная метка.
- `text` (str): Текст сообщения.
- `secret` (str, optional): Секретный ключ. По умолчанию `""`.

**Возвращает**:

- `str`: Подпись в виде SHA256 хеша.

**Как работает функция**:

1.  **Формирование сообщения**: Создается строка `message` путем конкатенации временной метки, текста сообщения и секретного ключа, разделенных символом `:`.
2.  **Кодирование сообщения**: Строка `message` кодируется в байты с использованием кодировки UTF-8.
3.  **Хеширование сообщения**: С использованием модуля `hashlib` вычисляется SHA256 хеш от закодированного сообщения.
4.  **Возврат хеша**: Функция возвращает вычисленный хеш в шестнадцатеричном формате.

```mermaid
graph TD
    A[Формирование сообщения (time:text:secret)] --> B(Кодирование сообщения в UTF-8);
    B --> C[Вычисление SHA256 хеша];
    C --> D(Возврат хеша в hex формате);
```

**Примеры**:

```python
# Пример использования generate_signature
import time

timestamp = int(time.time() * 1e3)
text = "Hello"
signature = generate_signature(timestamp, text)
print(signature)