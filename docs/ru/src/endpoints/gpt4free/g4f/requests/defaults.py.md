# Модуль defaults.py

## Обзор

Модуль `defaults.py` содержит определения стандартных HTTP-заголовков, используемых в запросах к серверам gpt4free. Эти заголовки имитируют запросы от веб-браузера, что помогает избежать блокировок со стороны серверов.

## Подробнее

В данном модуле определены два набора заголовков: `DEFAULT_HEADERS` и `WEBVIEW_HAEDERS`. `DEFAULT_HEADERS` предназначен для использования в обычных запросах, а `WEBVIEW_HAEDERS` — для запросов, имитирующих веб-просмотр. Модуль также проверяет наличие библиотеки `brotli` для поддержки сжатия `br`.

## Переменные

### `has_brotli`
Указывает, установлена ли библиотека `brotli`.
### `DEFAULT_HEADERS`

**Описание**: Стандартные HTTP-заголовки, используемые по умолчанию в запросах.

**Атрибуты**:
- `"accept"` (str): Типы контента, которые клиент может обрабатывать (`"*/*"` означает любой тип).
- `"accept-encoding"` (str): Методы сжатия, поддерживаемые клиентом (`"gzip, deflate"` и, возможно, `", br"` если установлен `brotli`).
- `"accept-language"` (str): Предпочитаемый язык (`"en-US"`).
- `"referer"` (str): URL-адрес страницы, с которой был сделан запрос (по умолчанию пустой).
- `"sec-ch-ua"` (str): Информация о браузере (Chrome).
- `"sec-ch-ua-mobile"` (str): Указывает, является ли устройство мобильным (`"?0"` означает нет).
- `"sec-ch-ua-platform"` (str): Платформа операционной системы (`"Windows"`).
- `"sec-fetch-dest"` (str): Назначение запроса (`"empty"`).
- `"sec-fetch-mode"` (str): Режим запроса (`"cors"`).
- `"sec-fetch-site"` (str): Сайт, с которого был сделан запрос (`"same-origin"`).
- `"user-agent"` (str): Строка User-Agent, идентифицирующая браузер (`"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"`).

**Пример**:

```python
DEFAULT_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US",
    "referer": "",
    "sec-ch-ua": "\\"Not(A:Brand\\";v=\\"99\\", \\"Google Chrome\\";v=\\"133\\", \\"Chromium\\";v=\\"133\\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\\"Windows\\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}
```

### `WEBVIEW_HAEDERS`

**Описание**: HTTP-заголовки, используемые для имитации запросов из WebView.

**Атрибуты**:
- `"Accept"` (str): Типы контента, которые клиент может обрабатывать (`"*/*"` означает любой тип).
- `"Accept-Encoding"` (str): Методы сжатия, поддерживаемые клиентом (`"gzip, deflate, br"`).
- `"Accept-Language"` (str): Языки, предпочитаемые клиентом (пустая строка).
- `"Referer"` (str): URL-адрес страницы, с которой был сделан запрос (пустая строка).
- `"Sec-Fetch-Dest"` (str): Назначение запроса (`"empty"`).
- `"Sec-Fetch-Mode"` (str): Режим запроса (`"cors"`).
- `"Sec-Fetch-Site"` (str): Сайт, с которого был сделан запрос (`"same-origin"`).
- `"User-Agent"` (str): Строка User-Agent, идентифицирующая клиент (пустая строка).

**Пример**:

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