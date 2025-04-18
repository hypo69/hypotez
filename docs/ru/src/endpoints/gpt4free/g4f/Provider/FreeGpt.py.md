# Модуль `FreeGpt`

## Обзор

Модуль `FreeGpt` предоставляет асинхронтный генератор для взаимодействия с сервисом FreeGpt. Он поддерживает историю сообщений, системные сообщения и позволяет генерировать текст на основе предоставленных подсказок, используя модели `gemini-1.5-pro` и `gemini-1.5-flash`. Модуль также обрабатывает ошибки, связанные с ограничением скорости запросов.

## Подробней

Модуль предназначен для использования в асинхронных приложениях, где требуется генерация текста на основе заданных параметров и моделей. Он использует `StreamSession` для отправки запросов и обработки потоковых ответов, что позволяет эффективно работать с большими объемами данных.  `FreeGpt` является частью проекта `hypotez` и интегрируется с другими модулями проекта. В частности, для обработки ошибок используется `RateLimitError` из модуля `hypotez.src.errors`, а для работы с прокси и таймаутами – параметры `proxy` и `timeout`.

## Классы

### `FreeGpt`

**Описание**:
Класс `FreeGpt` предоставляет методы для взаимодействия с сервисом FreeGpt. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет ему поддерживать асинхронную генерацию и управление моделями.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для управления моделями.

**Атрибуты**:
- `url` (str): URL для доступа к сервису FreeGpt.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).
- `models` (list): Список поддерживаемых моделей (`gemini-1.5-pro`, `gemini-1.5-flash`).

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для получения ответов от сервиса FreeGpt.
- `_build_request_data`: Статический метод для построения данных запроса.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: Optional[str] = None,
    timeout: int = 120,
    **kwargs: Any
) -> AsyncGenerator[str, None]:
    """
    Создает асинхронный генератор для получения ответов от сервиса FreeGpt.

    Args:
        model (str): Используемая модель (`gemini-1.5-pro` или `gemini-1.5-flash`).
        messages (Messages): Список сообщений для отправки.
        proxy (Optional[str], optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
        **kwargs (Any): Дополнительные параметры.

    Returns:
        AsyncGenerator[str, None]: Асинхронный генератор, выдающий чанки текста ответа.

    Raises:
        RateLimitError: Если достигнут лимит запросов.
        Exception: Если возникает ошибка при выполнении запроса.
    """
```

**Назначение**:
Метод `create_async_generator` создает асинхронный генератор, который отправляет запросы к API FreeGpt и возвращает ответы в виде потока чанков текста. Этот метод позволяет взаимодействовать с API FreeGpt асинхронно, обрабатывая ответы по мере их поступления.

**Параметры**:
- `cls`: Ссылка на класс `FreeGpt`.
- `model` (str): Идентификатор используемой модели (`gemini-1.5-pro` или `gemini-1.5-flash`).
- `messages` (Messages): Список сообщений, отправляемых в запросе. Обычно содержит историю разговора и текущий запрос.
- `proxy` (Optional[str], optional): Адрес прокси-сервера, если необходимо использовать прокси для подключения к API. По умолчанию `None`.
- `timeout` (int, optional): Максимальное время ожидания ответа от API в секундах. По умолчанию 120.
- `**kwargs` (Any): Дополнительные именованные аргументы, которые могут быть переданы в метод (не используются в текущей реализации).

**Возвращает**:
- `AsyncGenerator[str, None]`: Асинхронный генератор, который выдает части (чанки) текста ответа от API FreeGpt.

**Вызывает исключения**:
- `RateLimitError`: Вызывается, если достигнут лимит запросов к API (сообщение об ошибке: `"当前地区当日额度已消耗完"`).
- `Exception`: Может быть вызвано при возникновении других ошибок при выполнении запроса, таких как проблемы с сетью, неверные параметры запроса и т.д.

**Как работает функция**:

1. **Подготовка данных**: Извлекается последний запрос пользователя из списка сообщений `messages` и текущее время в формате timestamp.
2. **Построение запроса**: Вызывается статический метод `_build_request_data` для формирования данных запроса, включая подпись (sign).
3. **Выбор домена**: Случайно выбирается один из доступных доменов из списка `DOMAINS`.
4. **Отправка запроса**: Используется `StreamSession` для отправки асинхронного POST-запроса к API FreeGpt с использованием выбранного домена, сформированных данных и параметров прокси и таймаута.
5. **Обработка ответа**:
   - Проверяется статус ответа с помощью `raise_for_status`. Если статус указывает на ошибку, выбрасывается исключение.
   - Читаются данные ответа по частям (чанкам) с использованием `response.iter_content()`.
   - Каждый чанк декодируется в строку с использованием кодировки `errors="ignore"`, чтобы избежать проблем с некорректными символами.
   - Если в декодированном чанке содержится сообщение об ограничении скорости запросов (`RATE_LIMIT_ERROR_MESSAGE`), выбрасывается исключение `RateLimitError`.
   - Каждый декодированный чанк возвращается через `yield`, делая функцию генератором.

```ascii
Начало
   │
   ├───> Извлечение запроса и времени (prompt, timestamp)
   │
   ├───> Построение данных запроса (_build_request_data)
   │
   ├───> Выбор домена (domain)
   │
   ├───> Отправка POST-запроса (session.post)
   │
   ├───> Обработка ответа
   │      │
   │      ├───> Проверка статуса ответа (raise_for_status)
   │      │
   │      ├───> Чтение данных по частям (response.iter_content)
   │      │
   │      ├───> Декодирование чанка (chunk.decode)
   │      │
   │      ├───> Проверка на ограничение скорости (RATE_LIMIT_ERROR_MESSAGE)
   │      │
   │      └───> Возврат чанка (yield chunk_decoded)
   │
Конец
```

**Примеры**:

```python
import asyncio
from typing import AsyncGenerator

async def main():
    messages = [{"role": "user", "content": "Напиши стихотворение про осень"}]
    model = "gemini-1.5-pro"

    generator: AsyncGenerator[str, None] = FreeGpt.create_async_generator(model=model, messages=messages)
    
    try:
        async for chunk in generator:
            print(chunk, end="")
    except RateLimitError as ex:
        print(f"Ошибка: Достигнут лимит запросов: {ex}")
    except Exception as ex:
        print(f"Произошла ошибка: {ex}")

if __name__ == "__main__":
    asyncio.run(main())
```

### `_build_request_data`

```python
    @staticmethod
    def _build_request_data(messages: Messages, prompt: str, timestamp: int, secret: str = "") -> Dict[str, Any]:
        """
        Создает словарь с данными запроса, необходимыми для отправки в API FreeGpt.

        Args:
            messages (Messages): Список сообщений для отправки.
            prompt (str): Последний запрос пользователя.
            timestamp (int): Временная метка запроса.
            secret (str, optional): Секретный ключ для подписи запроса. По умолчанию "".

        Returns:
            Dict[str, Any]: Словарь с данными запроса.
        """
```

**Назначение**:
Статический метод `_build_request_data` предназначен для формирования структуры данных запроса, который будет отправлен в API FreeGpt. Он собирает все необходимые параметры, такие как сообщения, временную метку и подпись, и формирует из них словарь.

**Параметры**:
- `messages` (Messages): Список сообщений, представляющих историю разговора.
- `prompt` (str): Последнее сообщение пользователя, которое является запросом к модели.
- `timestamp` (int): Временная метка запроса, используемая для генерации подписи.
- `secret` (str, optional): Секретный ключ, используемый для генерации подписи запроса. По умолчанию пустая строка.

**Возвращает**:
- `Dict[str, Any]`: Словарь, содержащий данные запроса в формате, ожидаемом API FreeGpt.

**Как работает функция**:

1. **Формирование данных**: Создается словарь, включающий следующие ключи:
   - `"messages"`: Список сообщений `messages`.
   - `"time"`: Временная метка `timestamp`.
   - `"pass"`: Всегда `None` (как указано в коде).
   - `"sign"`: Подпись запроса, сгенерированная функцией `generate_signature` на основе временной метки, сообщения и секретного ключа.

```ascii
Начало
   │
   ├───> Формирование словаря данных
   │      │
   │      ├───> "messages": messages
   │      │
   │      ├───> "time": timestamp
   │      │
   │      ├───> "pass": None
   │      │
   │      └───> "sign": generate_signature(timestamp, prompt, secret)
   │
   └───> Возврат словаря данных
   │
Конец
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Привет"}]
prompt = "Привет"
timestamp = int(time.time())
data = FreeGpt._build_request_data(messages, prompt, timestamp)
print(data)
```

### `generate_signature`

```python
def generate_signature(timestamp: int, message: str, secret: str = "") -> str:
    """
    Генерирует подпись для запроса на основе временной метки, сообщения и секретного ключа.

    Args:
        timestamp (int): Временная метка запроса.
        message (str): Сообщение для подписи.
        secret (str, optional): Секретный ключ. По умолчанию "".

    Returns:
        str: Подпись запроса в виде шестнадцатеричной строки.
    """
```

**Назначение**:
Функция `generate_signature` генерирует подпись (signature) для запроса к API. Подпись используется для проверки целостности и подлинности запроса. Она создается на основе временной метки, сообщения и секретного ключа с использованием алгоритма SHA256.

**Параметры**:
- `timestamp` (int): Временная метка запроса.
- `message` (str): Сообщение, которое необходимо подписать.
- `secret` (str, optional): Секретный ключ, используемый для генерации подписи. Если не указан, используется пустая строка.

**Возвращает**:
- `str`: Подпись запроса в виде шестнадцатеричной строки (hex digest).

**Как работает функция**:

1. **Конкатенация данных**: Формируется строка данных путем конкатенации временной метки, сообщения и секретного ключа через двоеточие: `f"{timestamp}:{message}:{secret}"`.
2. **Кодирование**: Строка данных кодируется в байты с использованием кодировки UTF-8.
3. **Вычисление SHA256**: Вычисляется хеш SHA256 от закодированной строки данных с использованием `hashlib.sha256()`.
4. **Форматирование в hex**: Полученный хеш преобразуется в шестнадцатеричную строку с помощью `hexdigest()`.

```ascii
Начало
   │
   ├───> Конкатенация данных (timestamp, message, secret)
   │
   ├───> Кодирование строки в байты (encode)
   │
   ├───> Вычисление хеша SHA256 (hashlib.sha256)
   │
   ├───> Преобразование хеша в hex-строку (hexdigest)
   │
Конец
```

**Примеры**:

```python
timestamp = int(time.time())
message = "Привет"
signature = generate_signature(timestamp, message)
print(signature)