# Модуль с настройками запросов к gpt4free

## Обзор

Модуль предоставляет значения по умолчанию для заголовков HTTP-запросов, используемых при работе с сервисом gpt4free. 

## Подробней

Модуль `defaults.py` определяет два словаря: `DEFAULT_HEADERS` и `WEBVIEW_HAEDERS`. Они содержат значения заголовков HTTP-запросов, которые могут использоваться для взаимодействия с gpt4free. 

- `DEFAULT_HEADERS`: Словарь содержит значения заголовков по умолчанию.
- `WEBVIEW_HAEDERS`: Словарь содержит значения заголовков для запросов из `webview`. 

## Константы

### `DEFAULT_HEADERS`

**Описание**: Словарь с заголовками HTTP-запросов по умолчанию для gpt4free. 

**Параметры**:

- `accept`:  "accept" - " */* " 
- `accept-encoding`:  "accept-encoding" - " gzip, deflate " + (", br" if has_brotli else "" ) 
- `accept-language`:  "accept-language" - " en-US " 
- `referer`:  "referer" - "" 
- `sec-ch-ua`:  "sec-ch-ua" - "\\"Not(A:Brand\\";v=\\"99\\", \\"Google Chrome\\";v=\\"133\\", \\"Chromium\\";v=\\"133\\"" 
- `sec-ch-ua-mobile`:  "sec-ch-ua-mobile" - "?0" 
- `sec-ch-ua-platform`:  "sec-ch-ua-platform" - "\\"Windows\\"" 
- `sec-fetch-dest`:  "sec-fetch-dest" - "empty" 
- `sec-fetch-mode`:  "sec-fetch-mode" - "cors" 
- `sec-fetch-site`:  "sec-fetch-site" - "same-origin" 
- `user-agent`:  "user-agent" - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" 

**Примеры**:

```python
>>> import requests
>>> import hypotez.src.endpoints.gpt4free.g4f.requests.defaults as defaults
>>> headers = defaults.DEFAULT_HEADERS
>>> headers['referer'] = 'https://gpt4free.com/'
>>> response = requests.get('https://gpt4free.com/', headers=headers)
>>> print(response.status_code)
200
```
### `WEBVIEW_HAEDERS`

**Описание**: Словарь с заголовками HTTP-запросов для `webview`. 

**Параметры**:

- `Accept`:  "Accept" - " */* " 
- `Accept-Encoding`:  "Accept-Encoding" - " gzip, deflate, br " 
- `Accept-Language`:  "Accept-Language" - "" 
- `Referer`:  "Referer" - "" 
- `Sec-Fetch-Dest`:  "Sec-Fetch-Dest" - "empty" 
- `Sec-Fetch-Mode`:  "Sec-Fetch-Mode" - "cors" 
- `Sec-Fetch-Site`:  "Sec-Fetch-Site" - "same-origin" 
- `User-Agent`:  "User-Agent" - "" 

**Примеры**:

```python
>>> import requests
>>> import hypotez.src.endpoints.gpt4free.g4f.requests.defaults as defaults
>>> headers = defaults.WEBVIEW_HAEDERS
>>> headers['referer'] = 'https://gpt4free.com/'
>>> response = requests.get('https://gpt4free.com/', headers=headers)
>>> print(response.status_code)
200
```

## Как работает

- Модуль проверяет наличие библиотеки `brotli`. Если она установлена, то добавляет "br" в заголовок `accept-encoding`.
- Заголовки в `WEBVIEW_HAEDERS` используются для запросов из `webview`.
- Используй значения в этих словарях для настройки HTTP-запросов при взаимодействии с сервисом gpt4free. 

## Примеры

- **Пример использования `DEFAULT_HEADERS`**:

```python
>>> import requests
>>> import hypotez.src.endpoints.gpt4free.g4f.requests.defaults as defaults
>>> headers = defaults.DEFAULT_HEADERS
>>> headers['referer'] = 'https://gpt4free.com/'
>>> response = requests.get('https://gpt4free.com/', headers=headers)
>>> print(response.status_code)
200
```

- **Пример использования `WEBVIEW_HAEDERS`**:

```python
>>> import requests
>>> import hypotez.src.endpoints.gpt4free.g4f.requests.defaults as defaults
>>> headers = defaults.WEBVIEW_HAEDERS
>>> headers['referer'] = 'https://gpt4free.com/'
>>> response = requests.get('https://gpt4free.com/', headers=headers)
>>> print(response.status_code)
200
```

## Внутренние функции

- **`has_brotli`**: 
    - **Назначение**: Проверяет наличие библиотеки `brotli`.
    - **Возвращает**: `bool` - `True`, если библиотека `brotli` установлена, иначе `False`.
    - **Пример**:

```python
>>> import hypotez.src.endpoints.gpt4free.g4f.requests.defaults as defaults
>>> defaults.has_brotli()
True