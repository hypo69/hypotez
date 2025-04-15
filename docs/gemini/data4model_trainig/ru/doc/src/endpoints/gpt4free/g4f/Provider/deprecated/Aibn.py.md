# Модуль для работы с провайдером Aibn (Deprecated)

## Обзор

Модуль `Aibn` предоставляет асинхронный генератор для взаимодействия с сервисом `aibn.cc`. Он предназначен для обмена сообщениями с использованием определенной модели, поддерживая историю сообщений и GPT-3.5 Turbo. Модуль использует асинхронные запросы для генерации ответов и включает функциональность для создания подписи запросов.

## Подробнее

Этот модуль является частью устаревшего кода (deprecated), что означает, что он может быть удален или заменен в будущих версиях. Он предоставляет класс `Aibn`, который наследуется от `AsyncGeneratorProvider` и реализует асинхронную генерацию ответов на основе предоставленных сообщений.

## Классы

### `Aibn`

**Описание**: Класс `Aibn` предоставляет интерфейс для взаимодействия с сервисом `aibn.cc`. Он поддерживает асинхронную генерацию ответов на основе предоставленных сообщений.
**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес сервиса `aibn.cc`.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.

**Методы**:

- `create_async_generator`
- `generate_signature`

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
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от сервиса Aibn.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа в секундах. По умолчанию 120.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий части ответа от сервиса.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса.

    Принцип работы:
    - Создается сессия с использованием `StreamSession` для асинхронной отправки запросов.
    - Формируются данные для отправки, включающие сообщения, временную метку и подпись.
    - Отправляется POST-запрос к сервису `aibn.cc` с использованием сформированных данных.
    - Полученные чанки ответа декодируются и возвращаются через асинхронный генератор.

    Внутренние функции:
        отсутствуют

    """
    ...
```

### `generate_signature`

```python
def generate_signature(timestamp: int, message: str, secret: str = "undefined"):
    """Генерирует подпись для запроса к сервису Aibn.

    Args:
        timestamp (int): Временная метка запроса.
        message (str): Сообщение для подписи.
        secret (str, optional): Секретный ключ для подписи. По умолчанию "undefined".

    Returns:
        str: Сгенерированная подпись в виде шестнадцатеричной строки.

    Принцип работы:
    - Формируется строка данных, включающая временную метку, сообщение и секретный ключ.
    - Вычисляется SHA256-хеш от сформированной строки.
    - Возвращается шестнадцатеричное представление вычисленного хеша.
    Внутренние функции:
        отсутствуют
    """
    ...
```

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

# from g4f.Provider.Aibn import Aibn  # Предполагается, что Aibn уже импортирован
# from g4f.typing import Messages, AsyncResult  # Предполагается, что Messages и AsyncResult определены


async def main():
    model = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Hello, Aibn!"}
    ]
    proxy: Optional[str] = None
    timeout: int = 120

    generator: AsyncGenerator[str, None] = Aibn.create_async_generator(
        model=model, messages=messages, proxy=proxy, timeout=timeout
    )

    async for chunk in generator:
        print(chunk, end="")


if __name__ == "__main__":
    asyncio.run(main())


# Пример использования generate_signature
import hashlib

def generate_signature(timestamp: int, message: str, secret: str = "undefined") -> str:
    """
    Генерирует подпись для запроса.

    Args:
        timestamp (int): Временная метка.
        message (str): Сообщение.
        secret (str, optional): Секретный ключ. По умолчанию "undefined".

    Returns:
        str: Подпись в виде SHA256-хеша.
    """
    data = f"{timestamp}:{message}:{secret}"
    return hashlib.sha256(data.encode()).hexdigest()


# Пример вызова функции
timestamp = 1678886400  # Пример временной метки
message = "Hello, world!"
signature = generate_signature(timestamp, message)
print(f"Signature: {signature}")