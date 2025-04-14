# Модуль `MagickPen`

## Обзор

Модуль `MagickPen` предоставляет асинхронный интерфейс для взаимодействия с сервисом MagickPen. Он позволяет генерировать текст на основе предоставленных сообщений, используя API MagickPen. Модуль поддерживает потоковую передачу данных и работу с системными сообщениями и историей сообщений.

## Подробней

Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов. Для получения необходимых API-ключей и параметров, модуль выполняет парсинг JavaScript-файла на стороне сервера. Для обеспечения безопасности, запросы подписываются с использованием хеширования.

## Классы

### `MagickPen`

**Описание**: Класс `MagickPen` предоставляет асинхронный интерфейс для взаимодействия с сервисом MagickPen.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса MagickPen (`https://magickpen.com`).
- `api_endpoint` (str): URL API для отправки запросов (`https://api.magickpen.com/ask`).
- `working` (bool): Указывает, работает ли провайдер. По умолчанию `False`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных. По умолчанию `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения. По умолчанию `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений. По умолчанию `True`.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).
- `models` (List[str]): Список поддерживаемых моделей (`['gpt-4o-mini']`).

**Методы**:
- `fetch_api_credentials()`: Асинхронно получает учетные данные API.
- `create_async_generator()`: Создает асинхронный генератор для отправки запросов и получения ответов от API.

## Методы класса

### `fetch_api_credentials`

```python
@classmethod
async def fetch_api_credentials() -> tuple:
    """Асинхронно получает учетные данные API, необходимые для взаимодействия с сервисом MagickPen.

    Извлекает `X-API-Secret`, `signature`, `timestamp`, `nonce` и `secret` из JavaScript-файла.

    Returns:
        tuple: Кортеж, содержащий `X_API_SECRET`, `signature`, `timestamp`, `nonce` и `secret`.

    Raises:
        Exception: Если не удается извлечь все необходимые данные из JavaScript-файла.
    """
    ...
```

**Как работает функция**:
1. Определяется URL JavaScript-файла, содержащего необходимые параметры.
2. Выполняется GET-запрос к JavaScript-файлу с использованием `aiohttp.ClientSession`.
3. Извлекается текст ответа.
4. С помощью регулярных выражений извлекаются значения `X-API-Secret` и `secret`.
5. Генерируются `timestamp` и `nonce`.
6. Формируется строка `signature_string` путем объединения "TGDBU9zCgM", `timestamp` и `nonce`, сортируется и хешируется с использованием MD5.
7. Проверяется наличие всех необходимых параметров.
8. В случае успеха возвращается кортеж с извлеченными значениями.
9. В случае неудачи вызывается исключение `Exception`.

**Примеры**:

```python
# Пример вызова функции
X_API_SECRET, signature, timestamp, nonce, secret = await MagickPen.fetch_api_credentials()
print(f"X-API-Secret: {X_API_SECRET}")
print(f"Signature: {signature}")
print(f"Timestamp: {timestamp}")
print(f"Nonce: {nonce}")
print(f"Secret: {secret}")
```

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
    """Создает асинхронный генератор для взаимодействия с API MagickPen.

    Args:
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответ от API.
    """
    ...
```

**Как работает функция**:
1. Получает модель с помощью `cls.get_model(model)`.
2. Получает учетные данные API с помощью `cls.fetch_api_credentials()`.
3. Формирует заголовки запроса, включая `nonce`, `origin`, `referer`, `secret`, `signature`, `timestamp` и `x-api-secret`.
4. Форматирует сообщения с помощью `format_prompt(messages)`.
5. Формирует полезную нагрузку (payload) запроса, включая `query`, `turnstileResponse` и `action`.
6. Отправляет POST-запрос к API с использованием `aiohttp.ClientSession`.
7. Получает ответ от API в виде асинхронного генератора, который выдает чанки данных.

**Примеры**:

```python
# Пример вызова функции
model = "gpt-4o-mini"
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
async for chunk in MagickPen.create_async_generator(model, messages):
    print(chunk, end="")
```
```python
# Пример вызова функции с прокси
model = "gpt-4o-mini"
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
proxy = "http://your_proxy:8080"
async for chunk in MagickPen.create_async_generator(model, messages, proxy=proxy):
    print(chunk, end="")