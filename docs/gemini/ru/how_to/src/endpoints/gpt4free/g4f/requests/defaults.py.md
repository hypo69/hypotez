### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода выполняет следующие задачи:
1. **Определяет поддержку Brotli**: Проверяет, установлена ли библиотека `brotli`, и устанавливает флаг `has_brotli` в `True` или `False` в зависимости от результата.
2. **Определяет заголовки по умолчанию**: Устанавливает два набора HTTP-заголовков (`DEFAULT_HEADERS` и `WEBVIEW_HAEDERS`), которые используются при выполнении HTTP-запросов. Заголовки включают информацию о кодировке, языке, источнике запроса и User-Agent.

Шаги выполнения
-------------------------
1. **Импорт библиотеки Brotli**:
   - Пытается импортировать библиотеку `brotli`.
   - Если импорт успешен, устанавливает `has_brotli = True`.
   - Если возникает `ImportError`, устанавливает `has_brotli = False`.
2. **Определение `DEFAULT_HEADERS`**:
   - Создает словарь `DEFAULT_HEADERS`, содержащий основные HTTP-заголовки:
     - `"accept"`: "*/*" (принимает все типы контента).
     - `"accept-encoding"`: "gzip, deflate" + (", br" если `has_brotli` `True` иначе ""). Указывает поддерживаемые методы сжатия.
     - `"accept-language"`: "en-US" (принимает английский язык).
     - `"referer"`: "" (пустой Referer).
     - `"sec-ch-ua"`: Информация о браузере Chrome.
     - `"sec-ch-ua-mobile"`: "?0" (не мобильное устройство).
     - `"sec-ch-ua-platform"`: `"Windows"` (платформа Windows).
     - `"sec-fetch-dest"`: "empty" (пустой запрос).
     - `"sec-fetch-mode"`: "cors" (междоменный запрос).
     - `"sec-fetch-site"`: "same-origin" (запрос с того же источника).
     - `"user-agent"`: Информация об агенте пользователя Chrome.
3. **Определение `WEBVIEW_HAEDERS`**:
   - Создает словарь `WEBVIEW_HAEDERS`, содержащий HTTP-заголовки для WebView:
     - `"Accept"`: "*/*" (принимает все типы контента).
     - `"Accept-Encoding"`: "gzip, deflate, br" (поддерживает сжатие gzip, deflate и br).
     - `"Accept-Language"`: "" (пустой Accept-Language).
     - `"Referer"`: "" (пустой Referer).
     - `"Sec-Fetch-Dest"`: "empty" (пустой запрос).
     - `"Sec-Fetch-Mode"`: "cors" (междоменный запрос).
     - `"Sec-Fetch-Site"`: "same-origin" (запрос с того же источника).
     - `"User-Agent"`: "" (пустой User-Agent).

Пример использования
-------------------------

```python
try:
    import brotli
    has_brotli = True
except ImportError:
    has_brotli = False

DEFAULT_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate" + (", br" if has_brotli else ""),\
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

# Пример использования DEFAULT_HEADERS при выполнении HTTP-запроса:
import requests
response = requests.get("https://example.com", headers=DEFAULT_HEADERS)
print(response.status_code)

# Пример использования WEBVIEW_HAEDERS:
response = requests.get("https://example.com", headers=WEBVIEW_HAEDERS)
print(response.headers)