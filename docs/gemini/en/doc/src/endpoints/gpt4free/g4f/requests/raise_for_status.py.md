# Модуль для обработки ошибок в ответе от GPT-4Free API

## Обзор

Этот модуль предоставляет функции для обработки различных типов ошибок, которые могут возникать при взаимодействии с GPT-4Free API. 

## Детали

Функции `raise_for_status_async` и `raise_for_status` предназначены для проверки статуса ответа от сервера GPT-4Free и генерации соответствующего исключения в случае ошибки.

## Классы

### `CloudflareError`

**Описание**: Исключение, генерируемое при обнаружении ошибки Cloudflare.

**Наследует**: `ResponseStatusError`

## Функции

### `is_cloudflare`

**Назначение**: Функция проверяет, является ли текст HTML-кодом, который указывает на ошибку Cloudflare.

**Параметры**:
- `text` (str): Текст, который необходимо проверить.

**Возвращает**:
- `bool`: `True`, если текст содержит признаки ошибки Cloudflare, иначе `False`.

**Примеры**:
```python
>>> is_cloudflare('<p id="cf-spinner-please-wait">')
True
>>> is_cloudflare('some random text')
False
```

### `is_openai`

**Назначение**: Функция проверяет, является ли текст HTML-кодом, который указывает на ошибку OpenAI.

**Параметры**:
- `text` (str): Текст, который необходимо проверить.

**Возвращает**:
- `bool`: `True`, если текст содержит признаки ошибки OpenAI, иначе `False`.

**Примеры**:
```python
>>> is_openai('<p>Unable to load site</p>')
True
>>> is_openai('some random text')
False
```

### `raise_for_status_async`

**Назначение**: Асинхронная функция, которая анализирует статус ответа и генерирует соответствующее исключение, если в ответе обнаружена ошибка.

**Параметры**:
- `response` (Union[StreamResponse, ClientResponse]): Ответ от сервера GPT-4Free.
- `message` (str, optional): Дополнительное сообщение об ошибке. По умолчанию `None`.

**Возвращает**:
- `None`: Функция не возвращает значение.

**Исключения**:
- `MissingAuthError`: Возникает, если код ответа равен 401 (неавторизованный доступ).
- `CloudflareError`: Возникает, если код ответа равен 403 и текст ответа указывает на ошибку Cloudflare.
- `ResponseStatusError`: Возникает, если код ответа равен 403 и текст ответа указывает на ошибку OpenAI или равен 502 (Bad Gateway).
- `RateLimitError`: Возникает, если код ответа равен 429, 402 или 504 (Gateway Timeout).
- `ResponseStatusError`: Возникает, если код ответа не соответствует вышеперечисленным случаям.

**Примеры**:
```python
>>> async def test_raise_for_status_async():
...     response = StreamResponse(status=401, text='Unauthorized')
...     await raise_for_status_async(response)
...
Traceback (most recent call last):
  ...
MissingAuthError: Response 401: Unauthorized

>>> async def test_raise_for_status_async():
...     response = StreamResponse(status=403, text='Cloudflare detected')
...     await raise_for_status_async(response)
...
Traceback (most recent call last):
  ...
CloudflareError: Response 403: Cloudflare detected
```

### `raise_for_status`

**Назначение**: Синхронная функция, которая анализирует статус ответа и генерирует соответствующее исключение, если в ответе обнаружена ошибка.

**Параметры**:
- `response` (Union[Response, StreamResponse, ClientResponse, RequestsResponse]): Ответ от сервера GPT-4Free.
- `message` (str, optional): Дополнительное сообщение об ошибке. По умолчанию `None`.

**Возвращает**:
- `None`: Функция не возвращает значение.

**Исключения**:
- `MissingAuthError`: Возникает, если код ответа равен 401 (неавторизованный доступ).
- `CloudflareError`: Возникает, если код ответа равен 403 и текст ответа указывает на ошибку Cloudflare.
- `ResponseStatusError`: Возникает, если код ответа равен 403 и текст ответа указывает на ошибку OpenAI или равен 502 (Bad Gateway).
- `RateLimitError`: Возникает, если код ответа равен 429, 402 или 504 (Gateway Timeout).
- `ResponseStatusError`: Возникает, если код ответа не соответствует вышеперечисленным случаям.

**Примеры**:
```python
>>> response = RequestsResponse()
>>> response.status_code = 401
>>> response.text = 'Unauthorized'
>>> raise_for_status(response)
Traceback (most recent call last):
  ...
MissingAuthError: Response 401: Unauthorized

>>> response = RequestsResponse()
>>> response.status_code = 403
>>> response.text = 'Cloudflare detected'
>>> raise_for_status(response)
Traceback (most recent call last):
  ...
CloudflareError: Response 403: Cloudflare detected
```