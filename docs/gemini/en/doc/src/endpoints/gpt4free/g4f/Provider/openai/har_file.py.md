# Модуль для работы с файлами HAR

## Обзор

Модуль содержит классы и функции для работы с файлами HAR, которые используются для хранения информации о сетевых запросах и ответах. Он предоставляет функциональность для чтения и парсинга файлов HAR, извлечения информации о куки, токенах доступа и других параметрах, а также для генерации запросов к защищенным серверам.

## Детали

Этот модуль предназначен для взаимодействия с веб-сервисами, которые используют механизм защиты от ботов с использованием файлов HAR. HAR (HTTP Archive) - это стандартный формат, используемый для записи и анализа трафика HTTP.

## Классы

### `RequestConfig`

**Описание**: Класс, хранящий конфигурацию запроса к серверу.

**Атрибуты**:

- `cookies` (dict): Словарь с куки, полученными из файла HAR.
- `headers` (dict): Словарь с заголовками запроса, полученными из файла HAR.
- `access_token` (str): Токен доступа, полученный из файла HAR.
- `proof_token` (list): Список токенов подтверждения, полученных из файла HAR.
- `turnstile_token` (str): Токен Turnstile, полученный из файла HAR.
- `arkose_request` (arkReq): Объект `arkReq`, содержащий информацию о запросе к серверу Arkose.
- `arkose_token` (str): Токен Arkose, полученный после успешного запроса к серверу Arkose.
- `data_build` (str): Идентификатор сборки данных.

### `arkReq`

**Описание**: Класс, хранящий информацию о запросе к серверу Arkose.

**Атрибуты**:

- `arkURL` (str): URL-адрес сервера Arkose.
- `arkBx` (str): Зашифрованная строка с информацией о запросе.
- `arkHeader` (dict): Словарь с заголовками запроса к серверу Arkose.
- `arkBody` (dict): Словарь с телом запроса к серверу Arkose.
- `arkCookies` (dict): Словарь с куки, используемыми при запросе к серверу Arkose.
- `userAgent` (str): Строка User-Agent, используемая при запросе к серверу Arkose.

## Функции

### `get_har_files()`

**Цель**: Функция возвращает список путей к файлам HAR в директории с куки.

**Параметры**: 

- None.

**Возвращает**:

- `list[str]`: Список путей к файлам HAR.

**Возникающие исключения**:

- `NoValidHarFileError`: Если директория с куки не доступна для чтения или не содержит файлов HAR.

**Пример**:

```python
>>> get_har_files()
['/home/user/.config/hypotez/har_and_cookies/2023-12-01_12-00-00.har']
```

### `readHAR(request_config: RequestConfig)`

**Цель**: Функция читает файлы HAR и извлекает информацию о куки, токенах доступа, токенах Arkose и других параметрах.

**Параметры**:

- `request_config` (`RequestConfig`): Объект `RequestConfig`, в который записываются извлеченные данные.

**Возвращает**:

- `None`: Функция не возвращает значение.

**Возникающие исключения**:

- `NoValidHarFileError`: Если не найдены валидные файлы HAR или не найден `proof_token`.

**Пример**:

```python
>>> request_config = RequestConfig()
>>> readHAR(request_config)
```

### `get_headers(entry)`

**Цель**: Функция возвращает словарь с заголовками запроса, исключая `Content-Length`, `Cookie` и заголовки, начинающиеся с `:`.

**Параметры**:

- `entry` (dict): Словарь с информацией о запросе, полученной из файла HAR.

**Возвращает**:

- `dict`: Словарь с заголовками запроса.

**Пример**:

```python
>>> entry = {'request': {'headers': [{'name': 'User-Agent', 'value': 'Mozilla/5.0'}]}}
>>> get_headers(entry)
{'user-agent': 'Mozilla/5.0'}
```

### `parseHAREntry(entry)`

**Цель**: Функция парсит запись из файла HAR и возвращает объект `arkReq`.

**Параметры**:

- `entry` (dict): Словарь с информацией о запросе, полученной из файла HAR.

**Возвращает**:

- `arkReq`: Объект `arkReq`, содержащий информацию о запросе к серверу Arkose.

**Пример**:

```python
>>> entry = {'request': {'url': 'https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147', 'headers': [{'name': 'User-Agent', 'value': 'Mozilla/5.0'}]}}
>>> parseHAREntry(entry)
<arkReq: arkURL='https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147', arkBx='...', arkHeader='...', arkBody='...', arkCookies='...', userAgent='Mozilla/5.0'>
```

### `genArkReq(chatArk: arkReq)`

**Цель**: Функция генерирует новый объект `arkReq`, заменяя значение `bda` и `rnd`, а также обновляя заголовок `x-ark-esync-value`.

**Параметры**:

- `chatArk` (`arkReq`): Объект `arkReq`, содержащий информацию о запросе к серверу Arkose.

**Возвращает**:

- `arkReq`: Объект `arkReq`, с измененными значениями.

**Возникающие исключения**:

- `RuntimeError`: Если файл HAR не валидный.

**Пример**:

```python
>>> chatArk = arkReq(arkURL='https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147', arkBx='...', arkHeader='...', arkBody='...', arkCookies='...', userAgent='Mozilla/5.0')
>>> genArkReq(chatArk)
<arkReq: arkURL='https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147', arkBx='...', arkHeader='...', arkBody='...', arkCookies='...', userAgent='Mozilla/5.0'>
```

### `sendRequest(tmpArk: arkReq, proxy: str = None)`

**Цель**: Функция отправляет запрос к серверу Arkose и возвращает токен Arkose.

**Параметры**:

- `tmpArk` (`arkReq`): Объект `arkReq`, содержащий информацию о запросе к серверу Arkose.
- `proxy` (str): Прокси-сервер для отправки запроса.

**Возвращает**:

- `str`: Токен Arkose.

**Возникающие исключения**:

- `RuntimeError`: Если не сгенерирован валидный токен Arkose.

**Пример**:

```python
>>> tmpArk = arkReq(arkURL='https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147', arkBx='...', arkHeader='...', arkBody='...', arkCookies='...', userAgent='Mozilla/5.0')
>>> sendRequest(tmpArk, proxy='http://127.0.0.1:8080')
'sup=1|rid=...'
```

### `getBDA(arkReq: arkReq)`

**Цель**: Функция генерирует зашифрованную строку `bda` и строку `bw`, используя информацию из объекта `arkReq`.

**Параметры**:

- `arkReq` (`arkReq`): Объект `arkReq`, содержащий информацию о запросе к серверу Arkose.

**Возвращает**:

- `tuple[str, str]`: Кортеж, содержащий зашифрованную строку `bda` и строку `bw`.

**Пример**:

```python
>>> arkReq = arkReq(arkURL='https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147', arkBx='...', arkHeader='...', arkBody='...', arkCookies='...', userAgent='Mozilla/5.0')
>>> getBDA(arkReq)
('...', '...')
```

### `getBt()`

**Цель**: Функция возвращает текущее время в секундах.

**Параметры**:

- None.

**Возвращает**:

- `int`: Текущее время в секундах.

**Пример**:

```python
>>> getBt()
1701587200
```

### `getBw(bt: int)`

**Цель**: Функция возвращает строку `bw`, которая представляет собой timestamp, округленный до 21600 секунд (6 часов).

**Параметры**:

- `bt` (int): Timestamp в секундах.

**Возвращает**:

- `str`: Строка `bw`.

**Пример**:

```python
>>> getBw(1701587200)
'1701575600'
```

### `getN()`

**Цель**: Функция генерирует строку `n`, которая представляет собой base64-закодированное текущее время в секундах.

**Параметры**:

- None.

**Возвращает**:

- `str`: Строка `n`.

**Пример**:

```python
>>> getN()
'MTYwMTU4NzIwMA=='
```

### `get_request_config(request_config: RequestConfig, proxy: str)`

**Цель**: Функция получает конфигурацию запроса, считывает информацию из файлов HAR, генерирует токен Arkose и обновляет объект `RequestConfig`.

**Параметры**:

- `request_config` (`RequestConfig`): Объект `RequestConfig`, который необходимо обновить.
- `proxy` (str): Прокси-сервер для отправки запросов.

**Возвращает**:

- `RequestConfig`: Объект `RequestConfig` с обновленной информацией.

**Пример**:

```python
>>> request_config = RequestConfig()
>>> get_request_config(request_config, proxy='http://127.0.0.1:8080')
<RequestConfig: cookies='...', headers='...', access_token='...', proof_token='...', turnstile_token='...', arkose_request='...', arkose_token='...', data_build='prod-db8e51e8414e068257091cf5003a62d3d4ee6ed0'>
```