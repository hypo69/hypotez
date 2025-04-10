# Модуль defaults.py

## Обзор

Модуль `defaults.py` содержит определения стандартных заголовков HTTP-запросов, используемых в проекте `hypotez` для взаимодействия с различными сервисами, в частности, с gpt4free.

## Подробней

Этот модуль определяет два набора заголовков: `DEFAULT_HEADERS` и `WEBVIEW_HAEDERS`. `DEFAULT_HEADERS` используются для обычных запросов, а `WEBVIEW_HAEDERS` — для запросов, выполняемых из веб-интерфейса (webview). Наличие библиотеки `brotli` определяет, будет ли поддержка сжатия brotli включена в заголовки.

## Переменные

### `has_brotli`

```python
try:
    import brotli
    has_brotli = True
except ImportError:
    has_brotli = False
```

Флаг, указывающий, установлена ли библиотека `brotli`. Если `brotli` установлена, то `has_brotli` устанавливается в `True`, иначе — в `False`.

**Как работает переменная**:

1.  Пытается импортировать библиотеку `brotli`.
2.  Если импорт успешен, устанавливает `has_brotli` в `True`.
3.  Если возникает исключение `ImportError` (т.е. библиотека `brotli` не установлена), устанавливает `has_brotli` в `False`.

### `DEFAULT_HEADERS`

```python
DEFAULT_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate" + (", br" if has_brotli else ""),
    "accept-language": "en-US",
    "referer": "",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}
```

Словарь, содержащий стандартные HTTP-заголовки.

**Описание параметров**:

-   `"accept"`: Типы контента, которые клиент может принять.
-   `"accept-encoding"`: Методы сжатия, поддерживаемые клиентом (`gzip`, `deflate`, и `br` если `has_brotli` is `True`).
-   `"accept-language"`: Предпочитаемый язык.
-   `"referer"`: URL страницы, с которой был сделан запрос.
-   `"sec-ch-ua"`: Информация о браузере клиента.
-   `"sec-ch-ua-mobile"`: Указывает, является ли клиент мобильным устройством.
-   `"sec-ch-ua-platform"`: Платформа клиента.
-   `"sec-fetch-dest"`: Назначение запроса.
-   `"sec-fetch-mode"`: Режим запроса.
-   `"sec-fetch-site"`: Сайт, с которого был сделан запрос.
-   `"user-agent"`: Строка, идентифицирующая браузер клиента.

### `WEBVIEW_HAEDERS`

```python
WEBVIEW_HAEDERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "",
    "Referer": "",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "",
}
```

Словарь, содержащий HTTP-заголовки для запросов, выполняемых из веб-интерфейса (webview).

**Описание параметров**:

-   `"Accept"`: Типы контента, которые клиент может принять.
-   `"Accept-Encoding"`: Методы сжатия, поддерживаемые клиентом (`gzip`, `deflate`, `br`).
-   `"Accept-Language"`: Предпочитаемый язык.
-   `"Referer"`: URL страницы, с которой был сделан запрос.
-   `"Sec-Fetch-Dest"`: Назначение запроса.
-   `"Sec-Fetch-Mode"`: Режим запроса.
-   `"Sec-Fetch-Site"`: Сайт, с которого был сделан запрос.
-   `"User-Agent"`: Строка, идентифицирующая браузер клиента.