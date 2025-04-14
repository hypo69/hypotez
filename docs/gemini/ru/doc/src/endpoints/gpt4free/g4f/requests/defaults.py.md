# Модуль defaults.py

## Обзор

Модуль `defaults.py` определяет стандартные HTTP-заголовки, используемые в запросах библиотеки `g4f` (gpt4free). Он также включает проверку наличия библиотеки `brotli` для поддержки сжатия `br`.

## Подробней

Этот модуль важен для настройки HTTP-запросов, отправляемых библиотекой `g4f`. Он обеспечивает отправку запросов со стандартными заголовками, которые могут быть необходимы для правильной работы некоторых провайдеров API. Также модуль определяет поддержку сжатия `brotli`, что позволяет уменьшить размер передаваемых данных и ускорить обмен информацией.

## Переменные

### `has_brotli`

```python
has_brotli = False
```

- **Назначение**: Флаг, указывающий, установлена ли библиотека `brotli`.
- **Тип**: `bool`
- **Значение по умолчанию**: `False`
- **Как работает**:
  - Пытается импортировать библиотеку `brotli`.
  - Если импорт успешен, устанавливает `has_brotli = True`.
  - Если происходит ошибка `ImportError`, оставляет `has_brotli = False`.

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

- **Назначение**: Стандартные HTTP-заголовки, используемые в запросах.
- **Тип**: `dict`
- **Ключи и значения**:
  - `"accept"`: "*/*" (принимает все типы контента).
  - `"accept-encoding"`: `"gzip, deflate"` + (`, br` если `has_brotli` `True`, иначе пустая строка) (указывает, какие типы сжатия поддерживаются).
  - `"accept-language"`: `"en-US"` (предпочтительный язык - английский (США)).
  - `"referer"`: `""` (пустой заголовок `referer`).
  - `"sec-ch-ua"`: `"\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\""` (информация о браузере).
  - `"sec-ch-ua-mobile"`: `"?0"` (указывает, что запрос не с мобильного устройства).
  - `"sec-ch-ua-platform"`: `"\"Windows\""` (платформа - Windows).
  - `"sec-fetch-dest"`: `"empty"` (указывает, что запрос предназначен для получения ресурса без специфического назначения).
  - `"sec-fetch-mode"`: `"cors"` (режим запроса - `cors`).
  - `"sec-fetch-site"`: `"same-origin"` (запрос к тому же домену).
  - `"user-agent"`: `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"` (строка user-agent, имитирующая браузер Chrome).
- **Как работает**:
  - Определяет набор HTTP-заголовков для использования по умолчанию.
  - В зависимости от наличия библиотеки `brotli`, добавляет или не добавляет поддержку сжатия `br` в заголовок `"accept-encoding"`.

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

- **Назначение**: HTTP-заголовки, используемые для запросов, выполняемых в WebView.
- **Тип**: `dict`
- **Ключи и значения**:
  - `"Accept"`: "*/*" (принимает все типы контента).
  - `"Accept-Encoding"`: `"gzip, deflate, br"` (указывает, что поддерживаются типы сжатия gzip, deflate и br).
  - `"Accept-Language"`: `""` (пустой заголовок `accept-language`).
  - `"Referer"`: `""` (пустой заголовок `referer`).
  - `"Sec-Fetch-Dest"`: `"empty"` (указывает, что запрос предназначен для получения ресурса без специфического назначения).
  - `"Sec-Fetch-Mode"`: `"cors"` (режим запроса - `cors`).
  - `"Sec-Fetch-Site"`: `"same-origin"` (запрос к тому же домену).
  - `"User-Agent"`: `""` (пустой заголовок `user-agent`).
- **Как работает**:
  - Определяет набор HTTP-заголовков для использования в WebView.
  - В отличие от `DEFAULT_HEADERS`, всегда включает поддержку сжатия `br`.
  - Некоторые заголовки (`"Accept-Language"`, `"Referer"`, `"User-Agent"`) остаются пустыми и, вероятно, должны быть заполнены динамически при использовании.

## Примеры

```python
# Пример использования DEFAULT_HEADERS при отправке запроса
import requests

response = requests.get("https://example.com", headers=DEFAULT_HEADERS)
print(response.status_code)

# Пример использования WEBVIEW_HAEDERS при отправке запроса в WebView
# (предполагается, что User-Agent и другие параметры задаются отдельно)
webview_headers = WEBVIEW_HAEDERS.copy()
webview_headers["User-Agent"] = "MyWebView/1.0"

response = requests.get("https://example.com", headers=webview_headers)
print(response.status_code)
```