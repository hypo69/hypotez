## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода определяет значения заголовков по умолчанию (DEFAULT_HEADERS) и заголовков для WebView (WEBVIEW_HAEDERS), которые будут использоваться в запросах к API GPT4Free. 

Шаги выполнения
-------------------------
1. Проверяется доступность библиотеки brotli.
2. Если brotli доступна, к значению `accept-encoding` в заголовках по умолчанию добавляется ", br".
3. Определяются заголовки по умолчанию (DEFAULT_HEADERS) с заданными значениями:
    - `accept`: "*/*"
    - `accept-encoding`: "gzip, deflate" + (", br" если brotli доступна)
    - `accept-language`: "en-US"
    - `referer`: ""
    - `sec-ch-ua`: "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\""
    - `sec-ch-ua-mobile`: "?0"
    - `sec-ch-ua-platform`: "\"Windows\""
    - `sec-fetch-dest`: "empty"
    - `sec-fetch-mode`: "cors"
    - `sec-fetch-site`: "same-origin"
    - `user-agent`: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
4. Определяются заголовки для WebView (WEBVIEW_HAEDERS) с заданными значениями:
    - `Accept`: "*/*"
    - `Accept-Encoding`: "gzip, deflate, br"
    - `Accept-Language`: ""
    - `Referer`: ""
    - `Sec-Fetch-Dest`: "empty"
    - `Sec-Fetch-Mode`: "cors"
    - `Sec-Fetch-Site`: "same-origin"
    - `User-Agent`: ""

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.requests.defaults import DEFAULT_HEADERS

# Используйте DEFAULT_HEADERS в качестве заголовков для запросов к API GPT4Free
response = requests.post(url, headers=DEFAULT_HEADERS, data=payload) 
```