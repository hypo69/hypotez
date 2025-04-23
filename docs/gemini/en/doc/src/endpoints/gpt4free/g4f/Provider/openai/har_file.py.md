# Module openai.har_file

## Overview

This module is designed to handle the reading and parsing of HAR (HTTP Archive) files to extract necessary configuration parameters for interacting with the OpenAI API. It includes functionality for reading HAR files, extracting headers, and parsing specific entries related to Arkose Labs for generating tokens.

## More details

This module is crucial for automating the retrieval of authentication tokens and configuration details directly from HAR files, which can be obtained from browser developer tools. It simplifies the process of setting up requests to the OpenAI API by automatically extracting and decrypting relevant parameters. The module specifically focuses on handling Arkose Labs tokens, which are used for security and authentication purposes.

## Classes

### `RequestConfig`

**Description**: Класс для хранения конфигурационных параметров запроса, извлеченных из HAR-файлов.

**Attributes**:
- `cookies` (dict): Куки для запросов.
- `headers` (dict): Заголовки для запросов.
- `access_token` (str): Токен доступа для авторизации.
- `proof_token` (list): Токен подтверждения.
- `turnstile_token` (str): Токен Turnstile.
- `arkose_request` (`arkReq`): Объект запроса Arkose.
- `arkose_token` (str): Токен Arkose.
- `data_build` (str): Версия сборки данных.

**Methods**:
- Нет явных методов, только атрибуты.

### `arkReq`

**Description**: Класс для хранения параметров запроса Arkose.

**Attributes**:
- `arkURL` (str): URL для запроса Arkose.
- `arkBx` (str): Зашифрованное тело запроса Arkose.
- `arkHeader` (dict): Заголовки запроса Arkose.
- `arkBody` (dict): Тело запроса Arkose.
- `arkCookies` (dict): Куки запроса Arkose.
- `userAgent` (str): User-Agent для запроса Arkose.

**Parameters**:
- `arkURL` (str): URL для запроса Arkose.
- `arkBx` (str): Зашифрованное тело запроса Arkose.
- `arkHeader` (dict): Заголовки запроса Arkose.
- `arkBody` (dict): Тело запроса Arkose.
- `arkCookies` (dict): Куки запроса Arkose.
- `userAgent` (str): User-Agent для запроса Arkose.

**Working principle**:
Класс используется для хранения и передачи параметров, необходимых для выполнения запросов Arkose. Он инициализируется с параметрами, извлеченными из HAR-файла.

## Functions

### `get_har_files`

**Purpose**: Функция для поиска HAR-файлов в директории с куками.

**Returns**:
- `list`: Список путей к HAR-файлам.

**Raises**:
- `NoValidHarFileError`: Если директория с куками недоступна для чтения или HAR-файлы не найдены.

**How the function works**:
Функция проверяет доступность директории с куками для чтения, затем проходит по всем файлам в этой директории и добавляет пути к HAR-файлам в список. Если HAR-файлы не найдены, выбрасывается исключение.

**Examples**:
```python
try:
    har_files = get_har_files()
    print(f"Found HAR files: {har_files}")
except NoValidHarFileError as ex:
    print(f"Error: {ex}")
```

### `readHAR`

**Purpose**: Функция для чтения HAR-файлов и извлечения конфигурационных параметров запроса.

**Parameters**:
- `request_config` (`RequestConfig`): Объект конфигурации запроса, который будет заполнен данными из HAR-файла.

**Raises**:
- `NoValidHarFileError`: Если `proof_token` не найден в HAR-файлах.

**How the function works**:
Функция проходит по всем HAR-файлам, найденным с помощью `get_har_files`, и извлекает из них данные, необходимые для конфигурации запроса. Извлекаются URL Arkose, токен доступа, заголовки и куки. Если `proof_token` не найден, выбрасывается исключение.

**Examples**:
```python
request_config = RequestConfig()
try:
    readHAR(request_config)
    print(f"Access Token: {request_config.access_token}")
    print(f"Proof Token: {request_config.proof_token}")
except NoValidHarFileError as ex:
    print(f"Error: {ex}")
```

### `get_headers`

**Purpose**: Функция для извлечения заголовков из записи HAR-файла.

**Parameters**:
- `entry` (dict): Запись HAR-файла.

**Returns**:
- `dict`: Словарь заголовков, приведенных к нижнему регистру.

**How the function works**:
Функция извлекает заголовки из записи HAR-файла, приводит их к нижнему регистру и фильтрует заголовки `content-length` и `cookie`, а также заголовки, начинающиеся с `:`.

**Examples**:
```python
entry = {'request': {'headers': [{'name': 'Content-Type', 'value': 'application/json'}, {'name': 'Cookie', 'value': 'test'}]}}
headers = get_headers(entry)
print(f"Headers: {headers}")
```

### `parseHAREntry`

**Purpose**: Функция для разбора записи HAR-файла и извлечения параметров запроса Arkose.

**Parameters**:
- `entry` (dict): Запись HAR-файла.

**Returns**:
- `arkReq`: Объект запроса Arkose.

**How the function works**:
Функция извлекает URL, заголовки, тело и куки запроса из записи HAR-файла и создает объект `arkReq`. Затем она расшифровывает тело запроса Arkose с использованием User-Agent и заголовка `x-ark-esync-value`.

**Examples**:
```python
entry = {
    'request': {
        'url': 'https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147',
        'headers': [{'name': 'User-Agent', 'value': 'test'}],
        'postData': {'params': [{'name': 'bda', 'value': 'test'}]},
        'cookies': []
    }
}
ark_req = parseHAREntry(entry)
print(f"Arkose URL: {ark_req.arkURL}")
```

### `genArkReq`

**Purpose**: Функция для генерации запроса Arkose.

**Parameters**:
- `chatArk` (`arkReq`): Объект запроса Arkose.

**Returns**:
- `arkReq`: Сгенерированный объект запроса Arkose.

**Raises**:
- `RuntimeError`: Если HAR-файл не валиден.

**How the function works**:
Функция создает копию объекта запроса Arkose, генерирует новые параметры `bda` и `bw`, кодирует `bda` в Base64 и устанавливает новые значения заголовков.

**Examples**:
```python
chat_ark = arkReq(arkURL='test', arkBx='test', arkHeader={'User-Agent': 'test'}, arkBody={'bda': 'test'}, arkCookies={}, userAgent='test')
try:
    tmp_ark = genArkReq(chat_ark)
    print(f"Generated Arkose Body: {tmp_ark.arkBody}")
    print(f"Generated Arkose Header: {tmp_ark.arkHeader}")
except RuntimeError as ex:
    print(f"Error: {ex}")
```

### `sendRequest`

**Purpose**: Асинхронная функция для отправки запроса Arkose.

**Parameters**:
- `tmpArk` (`arkReq`): Объект запроса Arkose.
- `proxy` (str, optional): Прокси для запроса. Defaults to `None`.

**Returns**:
- `str`: Токен Arkose.

**Raises**:
- `RuntimeError`: Если не удалось сгенерировать валидный токен Arkose.

**How the function works**:
Функция отправляет POST-запрос с использованием `StreamSession` с заголовками, куками и телом запроса, полученными из объекта `arkReq`. После получения ответа извлекается токен Arkose.

**Examples**:
```python
import asyncio
async def main():
    tmp_ark = arkReq(arkURL='test', arkBx='test', arkHeader={'User-Agent': 'test'}, arkBody={'bda': 'test'}, arkCookies={}, userAgent='test')
    try:
        arkose_token = await sendRequest(tmp_ark)
        print(f"Arkose Token: {arkose_token}")
    except RuntimeError as ex:
        print(f"Error: {ex}")

asyncio.run(main())
```

### `getBDA`

**Purpose**: Функция для получения параметров `bda` и `bw`.

**Parameters**:
- `arkReq` (`arkReq`): Объект запроса Arkose.

**Returns**:
- `tuple`: Зашифрованный `bx` и `bw`.

**How the function works**:
Функция заменяет значение ключа `"n"` в `bx` на новое значение, генерирует новый UUID и заменяет старый UUID на новый, вычисляет `bw` и шифрует `bx` с использованием User-Agent и `bw`.

**Examples**:
```python
ark_req = arkReq(arkURL='test', arkBx='"key":"n","value":"old"', arkHeader={'User-Agent': 'test'}, arkBody={'bda': 'test'}, arkCookies={}, userAgent='test')
encrypted_bx, bw = getBDA(ark_req)
print(f"Encrypted BX: {encrypted_bx}")
print(f"BW: {bw}")
```

### `getBt`

**Purpose**: Функция для получения текущего времени в формате Unix timestamp.

**Returns**:
- `int`: Текущее время в формате Unix timestamp.

**How the function works**:
Функция возвращает текущее время, полученное с помощью `time.time()`, в виде целого числа.

**Examples**:
```python
bt = getBt()
print(f"BT: {bt}")
```

### `getBw`

**Purpose**: Функция для получения значения `bw`.

**Parameters**:
- `bt` (int): Время в формате Unix timestamp.

**Returns**:
- `str`: Значение `bw`.

**How the function works**:
Функция вычисляет значение `bw` путем вычитания остатка от деления `bt` на 21600 из `bt`.

**Examples**:
```python
bt = int(time.time())
bw = getBw(bt)
print(f"BW: {bw}")
```

### `getN`

**Purpose**: Функция для получения значения `n`.

**Returns**:
- `str`: Значение `n`, закодированное в Base64.

**How the function works**:
Функция получает текущее время в формате timestamp, кодирует его в Base64 и возвращает результат.

**Examples**:
```python
n = getN()
print(f"N: {n}")
```

### `get_request_config`

**Purpose**: Асинхронная функция для получения конфигурации запроса.

**Parameters**:
- `request_config` (`RequestConfig`): Объект конфигурации запроса.
- `proxy` (str): Прокси для запроса.

**Returns**:
- `RequestConfig`: Объект конфигурации запроса с заполненными данными.

**How the function works**:
Функция сначала проверяет, установлен ли `proof_token`. Если нет, вызывает `readHAR` для чтения HAR-файлов. Затем, если `arkose_request` установлен, вызывает `sendRequest` для получения токена Arkose.

**Examples**:
```python
import asyncio
async def main():
    request_config = RequestConfig()
    proxy = None
    request_config = await get_request_config(request_config, proxy)
    print(f"Access Token: {request_config.access_token}")
    print(f"Arkose Token: {request_config.arkose_token}")

asyncio.run(main())