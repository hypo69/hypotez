# Модуль обработки статуса ответа

## Обзор

Модуль предназначен для проверки статуса HTTP-ответа и генерации исключения в случае, если статус указывает на ошибку. Он обрабатывает различные типы контента (JSON, HTML, текст) и предоставляет информативные сообщения об ошибках.

## Подробней

Данный модуль используется для централизованной обработки HTTP-ответов в проекте `hypotez`. Он позволяет унифицировать логику проверки статуса и обработки ошибок, что упрощает отладку и поддержку кода. Модуль автоматически пытается извлечь сообщение об ошибке из JSON-ответа, если это возможно, или предоставляет текстовое представление ответа.

## Функции

### `raise_for_status`

```python
async def raise_for_status(response: Union[StreamResponse, ClientResponse], message: str = None):
    """Проверяет статус HTTP-ответа и вызывает исключение, если статус указывает на ошибку.

    Args:
        response (Union[StreamResponse, ClientResponse]): Объект ответа, который может быть либо `StreamResponse`, либо `ClientResponse` из библиотеки `aiohttp`.
        message (str, optional): Пользовательское сообщение об ошибке. Если не указано, функция попытается извлечь сообщение из тела ответа. По умолчанию `None`.

    Raises:
        ResponseStatusError: Вызывается, если статус ответа не является успешным (response.ok == False). Содержит сообщение об ошибке, полученное из тела ответа (если возможно) или сгенерированное на основе текстового содержимого ответа.

    Как работает функция:
    1. Проверяет, является ли статус ответа успешным (`response.ok`). Если да, функция завершает свою работу.
    2. Если статус ответа не является успешным, функция пытается получить тип контента из заголовков ответа.
    3. Если тип контента начинается с `application/json`, функция пытается извлечь сообщение об ошибке из JSON-тела ответа. Если в JSON есть поле `error` или `message`, его значение используется в качестве сообщения об ошибке.
    4. Если не удалось извлечь сообщение об ошибке из JSON или тип контента не `application/json`, функция получает текстовое содержимое ответа.
    5. Если тип контента начинается с `text/html` или текстовое содержимое начинается с `<!DOCTYPE`, сообщение об ошибке устанавливается как `"HTML content"`. В противном случае используется текстовое содержимое ответа.
    6. Функция вызывает исключение `ResponseStatusError` с сообщением об ошибке и статусом ответа.

    ASCII flowchart:
    A: Проверка response.ok
    |
    B: Получение content_type из headers
    |
    C: content_type.startswith("application/json")?
    |       |
    |       D: Извлечение error/message из JSON
    |       |
    |       E: Получение response.text()
    |       |
    |       F: content_type.startswith("text/html") или text.startswith("<!DOCTYPE")
    |       |
    |       G: Генерация сообщения об ошибке
    |
    H: Вызов исключения ResponseStatusError

    Примеры:
    Пример 1: Успешный ответ
    >>> response = MockResponse(status=200, ok=True)
    >>> await raise_for_status(response) # Ничего не произойдет

    Пример 2: Ответ с ошибкой и JSON-сообщением об ошибке
    >>> response = MockResponse(status=400, ok=False, content_type="application/json", json_data={"error": "Invalid request"})
    >>> try:
    ...     await raise_for_status(response)
    ... except ResponseStatusError as ex:
    ...     print(ex)
    Response 400: Invalid request

    Пример 3: Ответ с ошибкой и HTML-содержимым
    >>> response = MockResponse(status=500, ok=False, content_type="text/html", text="<!DOCTYPE html><html>...</html>")
    >>> try:
    ...     await raise_for_status(response)
    ... except ResponseStatusError as ex:
    ...     print(ex)
    Response 500: HTML content
    """
```

### `raise_for_status` как она есть

Функция `raise_for_status` асинхронно проверяет, успешен ли HTTP-ответ. Если ответ не успешен, она пытается извлечь сообщение об ошибке из тела ответа, в зависимости от типа контента. Если тип контента — JSON, она ищет поля `error` или `message`. В противном случае она возвращает весь текст ответа или `"HTML content"`, если ответ является HTML-страницей. Затем вызывается исключение `ResponseStatusError` с соответствующим сообщением.

**Параметры**:
- `response` (Union[StreamResponse, ClientResponse]): HTTP-ответ для проверки.
- `message` (str, optional): Пользовательское сообщение об ошибке. По умолчанию `None`.

**Возвращает**:
- None

**Вызывает исключения**:
- `ResponseStatusError`: Если статус ответа не является успешным.

```python
    if response.ok:
        return
```

Если HTTP статус в норме - функция завершается.

```python
    content_type = response.headers.get("content-type", "")
```

Из заголовков ответа получаем значение `content-type`. Если заголовок отсутствует, переменной присваивается пустая строка.

```python
    if content_type.startswith("application/json"):
        try:
            data = await response.json()
            message = data.get("error", data.get("message", message))
            message = message.split(" <a ")[0]
        except Exception:
            pass
```

Если тип контента — JSON, пытаемся распарсить JSON из тела ответа.  Если удается распарсить JSON, пытаемся извлечь сообщение об ошибке из полей `error` или `message`. Если какое-либо из этих полей присутствует, его значение присваивается переменной `message`.
Если при чтении или обработке JSON возникает исключение, оно игнорируется, и функция переходит к следующему шагу.

```python
    if not message:
        text = await response.text()
        is_html = response.headers.get("content-type", "").startswith("text/html") or text.startswith("<!DOCTYPE")
        message = "HTML content" if is_html else text
```

Если сообщение об ошибке не было получено из JSON, получаем текстовое содержимое ответа. Проверяем, является ли контент HTML-страницей, анализируя заголовок `content-type` или начало текстового содержимого. Если это HTML-страница, то `message` устанавливается в `"HTML content"`. В противном случае `message` устанавливается в текстовое содержимое ответа.

```python
    raise ResponseStatusError(f"Response {response.status}: {message}")
```

Вызывается исключение `ResponseStatusError` с сообщением, содержащим статус ответа и сообщение об ошибке.