# Модуль ошибок для gpt4free
## Overview
Модуль содержит ряд исключений, которые используются для обработки ошибок, возникающих при взаимодействии с API-интерфейсом gpt4free. 

## Details
Модуль предоставляет набор пользовательских исключений для явной обработки различных типов ошибок, которые могут возникнуть во время работы с API gpt4free. Эти исключения служат для четкой идентификации причин возникновения ошибок и удобного их обработки в коде.

## Classes
### `ProviderNotFoundError`
**Описание**: Возникает, если не найден соответствующий провайдер.

### `ProviderNotWorkingError`
**Описание**: Возникает, если провайдер не работает.

### `StreamNotSupportedError`
**Описание**: Возникает, если не поддерживается потоковая передача.

### `ModelNotFoundError`
**Описание**: Возникает, если не найдена соответствующая модель.

### `ModelNotAllowedError`
**Описание**: Возникает, если модель недоступна.

### `RetryProviderError`
**Описание**: Возникает, если при попытке перезапуска провайдера произошла ошибка.

### `RetryNoProviderError`
**Описание**: Возникает, если при попытке перезапуска не найдено ни одного провайдера.

### `VersionNotFoundError`
**Описание**: Возникает, если не найдена соответствующая версия.

### `ModelNotSupportedError`
**Описание**: Возникает, если не поддерживается соответствующая модель.

### `MissingRequirementsError`
**Описание**: Возникает, если отсутствуют необходимые требования.

### `NestAsyncioError`
**Описание**: Возникает, если произошла ошибка при вложенном использовании `asyncio`.

### `MissingAuthError`
**Описание**: Возникает, если отсутствует авторизация.

### `PaymentRequiredError`
**Описание**: Возникает, если требуется оплата.

### `NoMediaResponseError`
**Описание**: Возникает, если в ответе не содержится медиа-контент.

### `ResponseError`
**Описание**: Возникает при получении ответа с ошибкой.

### `ResponseStatusError`
**Описание**: Возникает при получении ответа с некорректным статусом.

### `RateLimitError`
**Описание**: Возникает при превышении лимита запросов.

### `NoValidHarFileError`
**Описание**: Возникает, если не найден файл HAR с правильным форматом.

### `TimeoutError`
**Описание**: Возникает при превышении времени ожидания при запросах к API.

```python
    """Raised for timeout errors during API requests."""
```

### `ConversationLimitError`
**Описание**: Возникает при превышении лимита диалогов при запросах к API.

```python
    """Raised for conversation limit during API requests to AI endpoint."""
```

## Parameter Details
- `param` (str): Описание параметра `param`.
- `param1` (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.

## Examples
- `ProviderNotFoundError`:
```python
    from hypotez.src.endpoints.gpt4free.g4f.errors import ProviderNotFoundError
    
    try:
        # Код, который может вызвать ошибку ProviderNotFoundError
        ...
    except ProviderNotFoundError as ex:
        logger.error('Ошибка: не найден провайдер.', ex, exc_info=True)
```

- `ModelNotFoundError`:
```python
    from hypotez.src.endpoints.gpt4free.g4f.errors import ModelNotFoundError
    
    try:
        # Код, который может вызвать ошибку ModelNotFoundError
        ...
    except ModelNotFoundError as ex:
        logger.error('Ошибка: не найдена модель.', ex, exc_info=True)
```

- `TimeoutError`:
```python
    from hypotez.src.endpoints.gpt4free.g4f.errors import TimeoutError
    
    try:
        # Код, который может вызвать ошибку TimeoutError
        ...
    except TimeoutError as ex:
        logger.error('Ошибка: время ожидания истекло.', ex, exc_info=True)
```