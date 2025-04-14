# Модуль Yqcloud для gpt4free

## Обзор

Модуль `Yqcloud` представляет собой асинхронный провайдер генерации текста, использующий API сервиса `chat9.yqcloud.top`. Он предназначен для интеграции с библиотекой `gpt4free` и обеспечивает возможность получения потоковых ответов от языковой модели. Модуль поддерживает модель `gpt-3.5-turbo`.

## Подробней

Модуль `Yqcloud` предоставляет асинхронный интерфейс для взаимодействия с API `chat9.yqcloud.top`. Он использует `StreamSession` для отправки запросов и получения потоковых ответов. Важной особенностью является обработка возможных блокировок IP-адресов из-за обнаружения злоупотреблений. Модуль автоматически формирует необходимые заголовки и полезную нагрузку для запросов к API.

## Функции

### `create_async_generator`

```python
async def create_async_generator(
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    **kwargs,
) -> AsyncResult:
    """Создает асинхронный генератор для получения потоковых ответов от Yqcloud.

    Args:
        model (str): Идентификатор модели.
        messages (Messages): Список сообщений для отправки в запросе.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа в секундах. По умолчанию `120`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий чанки текста.

    Raises:
        RuntimeError: Если IP-адрес заблокирован из-за обнаружения злоупотреблений.

    Как работает функция:
    1. Функция создает сессию `StreamSession` с заданными заголовками, прокси и таймаутом.
    2. Формируется полезная нагрузка `payload` на основе переданных сообщений и дополнительных параметров.
    3. Отправляется `POST` запрос к API `https://api.aichatos.cloud/api/generateStream` с сформированной полезной нагрузкой.
    4. Функция итерируется по чанкам ответа, декодирует их и проверяет наличие сообщения о блокировке IP-адреса.
    5. Если IP-адрес заблокирован, выбрасывается исключение `RuntimeError`.
    6. Каждый чанк ответа выдается как часть асинхронного генератора.

    flowchart ASCII:

    Создание сессии StreamSession --> Формирование payload --> POST запрос к API --> Итерация по чанкам ответа --> Проверка блокировки IP --> Выдача чанка ответа

    Примеры:
        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Hello, Yqcloud!"}]
        >>> async for chunk in Yqcloud.create_async_generator(model, messages):
        ...     print(chunk, end="")
        <ответ от Yqcloud>

        >>> model = "gpt-3.5-turbo"
        >>> messages = [{"role": "user", "content": "Translate to French: Hello, Yqcloud!"}]
        >>> proxy = "http://your_proxy:8080"
        >>> async for chunk in Yqcloud.create_async_generator(model, messages, proxy=proxy):
        ...     print(chunk, end="")
        <переведенный ответ от Yqcloud>
    """
    ...
```

### `_create_header`

```python
def _create_header() -> dict:
    """Создает словарь с заголовками для HTTP-запроса.

    Returns:
        dict: Словарь с заголовками.

    Как работает функция:
    Функция возвращает статический словарь с необходимыми заголовками для запроса к API `chat9.yqcloud.top`.

    flowchart ASCII:
    Возврат словаря с заголовками

    Примеры:
        >>> headers = _create_header()
        >>> print(headers)
        {'accept': 'application/json, text/plain, */*', 'content-type': 'application/json', 'origin': 'https://chat9.yqcloud.top', 'referer': 'https://chat9.yqcloud.top/'}
    """
    ...
```

### `_create_payload`

```python
def _create_payload(
    messages: Messages,
    system_message: str = "",
    user_id: int = None,
    **kwargs
) -> dict:
    """Создает словарь с полезной нагрузкой для HTTP-запроса.

    Args:
        messages (Messages): Список сообщений для отправки в запросе.
        system_message (str, optional): Системное сообщение. По умолчанию "".
        user_id (int, optional): Идентификатор пользователя. Если не указан, генерируется случайный. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        dict: Словарь с полезной нагрузкой.

    Как работает функция:
    1. Если `user_id` не предоставлен, генерируется случайный `user_id`.
    2. Форматируется `prompt` из списка сообщений с помощью `format_prompt`.
    3. Создается словарь с полезной нагрузкой, включающий `prompt`, флаги `network` и `stream`, а также `userId`.

    flowchart ASCII:
    Проверка user_id --> Генерация user_id (если отсутствует) --> Форматирование prompt --> Создание payload

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello, Yqcloud!"}]
        >>> payload = _create_payload(messages)
        >>> print(payload)
        {'prompt': 'Hello, Yqcloud!', 'network': True, 'system': '', 'withoutContext': False, 'stream': True, 'userId': '#/chat/1785648765432'}

        >>> messages = [{"role": "user", "content": "Hello"}]
        >>> system_message = "You are a helpful assistant."
        >>> user_id = 1234567890
        >>> payload = _create_payload(messages, system_message=system_message, user_id=user_id)
        >>> print(payload)
        {'prompt': 'Hello', 'network': True, 'system': 'You are a helpful assistant.', 'withoutContext': False, 'stream': True, 'userId': '#/chat/1234567890'}
    """
    ...