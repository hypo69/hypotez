# Модуль обработки статусов ответов от GPT4Free

## Обзор

Этот модуль содержит функции для обработки статусов ответов от сервиса GPT4Free. Он включает в себя:

- Класс `CloudflareError`, представляющий ошибку, возникающую при обнаружении защиты Cloudflare.
- Функцию `is_cloudflare`, которая определяет, является ли текст ответом от Cloudflare.
- Функцию `is_openai`, которая определяет, является ли текст ответом от OpenAI.
- Асинхронную функцию `raise_for_status_async` для проверки статусов асинхронных ответов.
- Синхронную функцию `raise_for_status` для проверки статусов синхронных ответов.

## Подробней

Этот модуль предоставляет механизм проверки статусов ответов от GPT4Free и обработки различных типов ошибок, которые могут возникать:

- **CloudflareError**: Эта ошибка возникает, если сервер GPT4Free обнаруживает защиту Cloudflare. 
- **RateLimitError**: Возникает, если запросы ограничены из-за превышения лимита.
- **MissingAuthError**:  Возникает, если отсутствует необходимая авторизация.
- **ResponseStatusError**: Возникает при получении ответа с ошибкой от GPT4Free.

## Классы

### `CloudflareError`

**Описание**: Класс ошибки, которая возникает, если сервер GPT4Free обнаруживает защиту Cloudflare.
**Наследует**: `ResponseStatusError`

## Функции

### `is_cloudflare`

**Назначение**:  Проверяет, является ли текст ответом от Cloudflare.

**Параметры**:
- `text` (str): Текст ответа от сервиса.

**Возвращает**:
- `bool`: `True`, если текст отвечает заголовкам Cloudflare, `False` - в противном случае.

**Примеры**:
```python
>>> text = '<p id="cf-spinner-please-wait">Just a moment...</p>'
>>> is_cloudflare(text)
True
>>> text = 'This is a normal response.'
>>> is_cloudflare(text)
False
```

### `is_openai`

**Назначение**: Проверяет, является ли текст ответом от OpenAI.

**Параметры**:
- `text` (str): Текст ответа от сервиса.

**Возвращает**:
- `bool`: `True`, если текст отвечает заголовкам OpenAI, `False` - в противном случае.

**Примеры**:
```python
>>> text = '<p>Unable to load site</p>'
>>> is_openai(text)
True
>>> text = 'This is a normal response.'
>>> is_openai(text)
False
```

### `raise_for_status_async`

**Назначение**: Асинхронная функция для проверки статусов асинхронных ответов.

**Параметры**:
- `response` (Union[StreamResponse, ClientResponse]): Асинхронный ответ от GPT4Free.
- `message` (str): Сообщение с описанием ошибки, если оно получено в ответе.

**Возвращает**:
- `None`: Если статус ответа успешный.
- `Raises` (ResponseStatusError, RateLimitError, MissingAuthError, CloudflareError): Поднимает исключения в зависимости от типа ошибки.

**Как работает функция**:

- Функция проверяет статус асинхронного ответа.
- В случае ошибки пытается извлечь сообщение из ответа.
- Если ошибка не связана с Cloudflare, OpenAI или RateLimit, то поднимается `ResponseStatusError`.

**Примеры**:
```python
>>> response = await get_response_from_gpt4free()
>>> try:
>>>     await raise_for_status_async(response)
>>> except RateLimitError as ex:
>>>     print(f"Rate Limit Error: {ex}")
```

### `raise_for_status`

**Назначение**: Синхронная функция для проверки статусов синхронных ответов.

**Параметры**:
- `response` (Union[Response, StreamResponse, ClientResponse, RequestsResponse]): Синхронный ответ от GPT4Free.
- `message` (str): Сообщение с описанием ошибки, если оно получено в ответе.

**Возвращает**:
- `None`: Если статус ответа успешный.
- `Raises` (ResponseStatusError, RateLimitError, MissingAuthError, CloudflareError): Поднимает исключения в зависимости от типа ошибки.

**Как работает функция**:

- Функция проверяет статус синхронного ответа.
- В случае ошибки пытается извлечь сообщение из ответа.
- Если ошибка не связана с Cloudflare, OpenAI или RateLimit, то поднимается `ResponseStatusError`.

**Примеры**:
```python
>>> response = get_response_from_gpt4free()
>>> try:
>>>     raise_for_status(response)
>>> except CloudflareError as ex:
>>>     print(f"Cloudflare Error: {ex}")
```