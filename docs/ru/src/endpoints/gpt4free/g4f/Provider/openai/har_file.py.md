# Модуль для работы с HAR-файлами и Arkose Labs

## Обзор

Модуль `har_file.py` предназначен для обработки HAR (HTTP Archive) файлов, содержащих информацию о HTTP-запросах и ответах, а также для взаимодействия с Arkose Labs, системой защиты от ботов. Он используется для извлечения и анализа данных из HAR-файлов, необходимых для аутентификации и обхода защиты Arkose Labs при взаимодействии с API.

## Подробней

Этот модуль играет важную роль в автоматизации взаимодействия с сервисами, защищенными Arkose Labs, такими как ChatGPT. Он позволяет извлекать необходимые токены и параметры из HAR-файлов, сгенерированных в браузере, и использовать их для создания запросов к API. Это позволяет обходить защиту от ботов и получать доступ к функциональности сервиса.

## Классы

### `RequestConfig`

**Описание**: Класс, предназначенный для хранения конфигурационных данных запроса, таких как cookies, заголовки, access token, proof token, turnstile token, а также информации, связанной с Arkose Labs.

**Атрибуты**:

-   `cookies` (dict): Словарь с cookies запроса.
-   `headers` (dict): Словарь с заголовками запроса.
-   `access_token` (str): Access token для аутентификации.
-   `proof_token` (list): Список proof token'ов.
-   `turnstile_token` (str): Turnstile token.
-   `arkose_request` (arkReq): Объект `arkReq`, содержащий информацию для запроса к Arkose Labs.
-   `arkose_token` (str): Токен, полученный от Arkose Labs.
-   `data_build` (str): Строка, содержащая информацию о сборке данных.

### `arkReq`

**Описание**: Класс, предназначенный для хранения данных, необходимых для выполнения запросов к Arkose Labs.

**Атрибуты**:

-   `arkURL` (str): URL для запроса к Arkose Labs.
-   `arkBx` (str): Зашифрованное значение, используемое в запросах к Arkose Labs.
-   `arkHeader` (dict): Заголовки запроса к Arkose Labs.
-   `arkBody` (dict): Тело запроса к Arkose Labs.
-   `arkCookies` (dict): Cookies для запроса к Arkose Labs.
-   `userAgent` (str): User-Agent, используемый в запросах.

## Функции

### `get_har_files`

```python
def get_har_files() -> list[str]:
    """
    Находит все HAR-файлы в директории с cookies.

    Args:
        None

    Returns:
        list[str]: Список путей к найденным HAR-файлам.

    Raises:
        NoValidHarFileError: Если директория с cookies не читаема или не найдено ни одного HAR-файла.
    """
```

**Назначение**: Функция находит все файлы с расширением `.har` в директории, предназначенной для хранения cookies и HAR-файлов.

**Как работает функция**:

1.  Проверяет, доступна ли директория с cookies для чтения. Если нет, вызывает исключение `NoValidHarFileError`.
2.  Проходит по всем файлам в директории и ее поддиректориях.
3.  Если файл имеет расширение `.har`, добавляет его путь в список `harPath`.
4.  Если список `harPath` пуст, вызывает исключение `NoValidHarFileError`.
5.  Сортирует список `harPath` по времени изменения файла (от старых к новым).
6.  Возвращает отсортированный список путей к HAR-файлам.

**Примеры**:

```python
try:
    har_files = get_har_files()
    print(f"Found HAR files: {har_files}")
except NoValidHarFileError as ex:
    print(f"Error: {ex}")
```

### `readHAR`

```python
def readHAR(request_config: RequestConfig) -> None:
    """
    Извлекает данные из HAR-файлов и сохраняет их в объекте RequestConfig.

    Args:
        request_config (RequestConfig): Объект RequestConfig для хранения извлеченных данных.

    Returns:
        None

    Raises:
        NoValidHarFileError: Если не найден proof_token в HAR-файлах.
    """
```

**Назначение**: Функция читает HAR-файлы и извлекает из них необходимые данные, такие как access token, proof token, turnstile token, cookies и информацию для запросов к Arkose Labs.

**Как работает функция**:

1.  Получает список HAR-файлов с помощью функции `get_har_files()`.
2.  Перебирает HAR-файлы в списке.
3.  Для каждого HAR-файла пытается прочитать его содержимое как JSON.
4.  Перебирает записи (entries) в HAR-файле.
5.  Если URL записи соответствует `arkose_url`, парсит запись с помощью функции `parseHAREntry()` и сохраняет результат в `request_config.arkose_request`.
6.  Если URL записи начинается с `start_url`, извлекает access token, proof token, turnstile token и cookies из заголовков и тела ответа.
7.  Если не найден `proof_token` ни в одном из HAR-файлов, вызывает исключение `NoValidHarFileError`.

**Примеры**:

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

```python
def get_headers(entry: dict) -> dict:
    """
    Извлекает заголовки из записи HAR-файла.

    Args:
        entry (dict): Запись HAR-файла.

    Returns:
        dict: Словарь с заголовками запроса в нижнем регистре.
    """
```

**Назначение**: Функция извлекает заголовки из записи HAR-файла и возвращает их в виде словаря, приводя имена заголовков к нижнему регистру.

**Как работает функция**:

1.  Извлекает список заголовков из записи HAR-файла.
2.  Фильтрует заголовки, исключая `content-length`, `cookie` и заголовки, начинающиеся с `:`.
3.  Создает словарь, в котором ключами являются имена заголовков в нижнем регистре, а значениями - значения заголовков.
4.  Возвращает полученный словарь.

**Примеры**:

```python
entry = {
    'request': {
        'headers': [
            {'name': 'Content-Type', 'value': 'application/json'},
            {'name': 'Content-Length', 'value': '123'},
            {'name': 'Cookie', 'value': 'sessionid=12345'},
            {'name': 'Authorization', 'value': 'Bearer mytoken'}
        ]
    }
}
headers = get_headers(entry)
print(headers)
# Expected output: {'content-type': 'application/json', 'authorization': 'Bearer mytoken'}
```

### `parseHAREntry`

```python
def parseHAREntry(entry: dict) -> arkReq:
    """
    Парсит запись HAR-файла для извлечения данных, необходимых для запросов к Arkose Labs.

    Args:
        entry (dict): Запись HAR-файла.

    Returns:
        arkReq: Объект arkReq с извлеченными данными.
    """
```

**Назначение**: Функция парсит запись HAR-файла и извлекает из нее данные, необходимые для запросов к Arkose Labs, такие как URL, заголовки, тело запроса и cookies.

**Как работает функция**:

1.  Создает объект `arkReq` и заполняет его поля данными из записи HAR-файла.
2.  Извлекает `bda` из тела запроса и `bw` из заголовка `x-ark-esync-value`.
3.  Дешифрует `bda` с использованием `userAgent` и `bw` с помощью функции `decrypt()`.
4.  Возвращает объект `arkReq`.

**Примеры**:

```python
entry = {
    'request': {
        'url': 'https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147',
        'headers': [
            {'name': 'User-Agent', 'value': 'Mozilla/5.0'},
            {'name': 'X-Ark-Esync-Value', 'value': '12345'}
        ],
        'postData': {
            'params': [
                {'name': 'bda', 'value': 'encrypted_bda'},
                {'name': 'rnd', 'value': '0.123'}
            ]
        },
        'cookies': [
            {'name': 'ark_cookie', 'value': 'cookie_value'}
        ]
    }
}
ark_req = parseHAREntry(entry)
print(f"Arkose URL: {ark_req.arkURL}")
print(f"Arkose Bx: {ark_req.arkBx}")
```

### `genArkReq`

```python
def genArkReq(chatArk: arkReq) -> arkReq:
    """
    Генерирует новый объект arkReq с обновленными параметрами для запроса к Arkose Labs.

    Args:
        chatArk (arkReq): Объект arkReq с исходными данными.

    Returns:
        arkReq: Новый объект arkReq с обновленными параметрами.

    Raises:
        RuntimeError: Если входной объект arkReq недействителен.
    """
```

**Назначение**: Функция генерирует новый объект `arkReq` с обновленными параметрами для запроса к Arkose Labs. Она обновляет значения `bda`, `rnd` и `x-ark-esync-value` в теле и заголовках запроса.

**Как работает функция**:

1.  Создает глубокую копию входного объекта `arkReq`.
2.  Проверяет, является ли копия `tmpArk` валидной (не `None` и содержит ли тело и заголовки запроса). Если нет, вызывает исключение `RuntimeError`.
3.  Получает новые значения `bda` и `bw` с помощью функции `getBDA()`.
4.  Кодирует `bda` в base64 и обновляет значение `bda` в теле запроса.
5.  Генерирует случайное число и обновляет значение `rnd` в теле запроса.
6.  Обновляет значение `x-ark-esync-value` в заголовках запроса.
7.  Возвращает обновленный объект `arkReq`.

**Примеры**:

```python
chat_ark = arkReq(
    arkURL='https://example.com',
    arkBx='encrypted_bx',
    arkHeader={'User-Agent': 'Mozilla/5.0', 'x-ark-esync-value': 'old_bw'},
    arkBody={'bda': 'old_bda'},
    arkCookies={},
    userAgent='Mozilla/5.0'
)
try:
    new_ark_req = genArkReq(chat_ark)
    print(f"New BDA: {new_ark_req.arkBody['bda']}")
    print(f"New X-Ark-Esync-Value: {new_ark_req.arkHeader['x-ark-esync-value']}")
except RuntimeError as ex:
    print(f"Error: {ex}")
```

### `sendRequest`

```python
async def sendRequest(tmpArk: arkReq, proxy: str = None) -> str:
    """
    Отправляет запрос к Arkose Labs и получает токен.

    Args:
        tmpArk (arkReq): Объект arkReq с данными для запроса.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.

    Returns:
        str: Токен, полученный от Arkose Labs.

    Raises:
        RuntimeError: Если не удалось сгенерировать валидный arkose token.
    """
```

**Назначение**: Функция отправляет запрос к Arkose Labs с использованием данных из объекта `arkReq` и получает токен Arkose.

**Как работает функция**:

1.  Создает асинхронную сессию с использованием `StreamSession` с заданными заголовками, cookies и прокси (если указан).
2.  Отправляет POST-запрос к `tmpArk.arkURL` с данными из `tmpArk.arkBody`.
3.  Получает JSON-ответ и извлекает значение токена из поля `token`.
4.  Проверяет, содержит ли токен подстроку `sup=1|rid=`. Если нет, вызывает исключение `RuntimeError`.
5.  Возвращает полученный токен.

**Примеры**:

```python
import asyncio

async def main():
    tmp_ark = arkReq(
        arkURL='https://example.com/arkose',
        arkBx='encrypted_bx',
        arkHeader={'User-Agent': 'Mozilla/5.0'},
        arkBody={'bda': 'base64_bda'},
        arkCookies={},
        userAgent='Mozilla/5.0'
    )
    try:
        arkose_token = await sendRequest(tmp_ark, proxy='http://proxy:8080')
        print(f"Arkose Token: {arkose_token}")
    except RuntimeError as ex:
        print(f"Error: {ex}")

asyncio.run(main())
```

### `getBDA`

```python
def getBDA(arkReq: arkReq) -> tuple[str, str]:
    """
    Обновляет и шифрует данные bx для запроса к Arkose Labs.

    Args:
        arkReq (arkReq): Объект arkReq с данными для запроса.

    Returns:
        tuple[str, str]: Кортеж, содержащий зашифрованное значение bx и bw.
    """
```

**Назначение**: Функция обновляет и шифрует данные `bx` для запроса к Arkose Labs. Она заменяет UUID, получает новые значения `bt` и `bw`, шифрует `bx` и возвращает зашифрованное значение и `bw`.

**Как работает функция**:

1.  Извлекает `bx` из объекта `arkReq`.
2.  Заменяет значение ключа `"key":"n","value":"\\S*?"` в `bx` на новое значение, полученное с помощью функции `getN()`.
3.  Ищет старый UUID в `bx` и заменяет его на новый, сгенерированный с помощью `uuid.uuid4()`.
4.  Получает значение `bw` с помощью функций `getBt()` и `getBw()`.
5.  Шифрует `bx` с использованием `userAgent` и `bw` с помощью функции `encrypt()`.
6.  Возвращает зашифрованное значение `bx` и `bw`.

**Примеры**:

```python
ark_req = arkReq(
    arkURL='https://example.com/arkose',
    arkBx='{"key":"4b4b269e68","value":"old_uuid"}{"key":"n","value":"old_n"}',
    arkHeader={'User-Agent': 'Mozilla/5.0'},
    arkBody={},
    arkCookies={},
    userAgent='Mozilla/5.0'
)
encrypted_bx, bw = getBDA(ark_req)
print(f"Encrypted BX: {encrypted_bx}")
print(f"BW: {bw}")
```

### `getBt`

```python
def getBt() -> int:
    """
    Получает текущее время в формате timestamp.

    Args:
        None

    Returns:
        int: Текущее время в формате timestamp.
    """
```

**Назначение**: Функция возвращает текущее время в формате timestamp (количество секунд, прошедших с начала эпохи Unix).

**Как работает функция**:

1.  Вызывает функцию `time.time()`, которая возвращает текущее время в секундах.
2.  Преобразует полученное значение в целое число.
3.  Возвращает полученное целое число.

**Примеры**:

```python
bt = getBt()
print(f"Current Timestamp: {bt}")
```

### `getBw`

```python
def getBw(bt: int) -> str:
    """
    Вычисляет значение bw на основе timestamp bt.

    Args:
        bt (int): Timestamp.

    Returns:
        str: Вычисленное значение bw.
    """
```

**Назначение**: Функция вычисляет значение `bw` на основе timestamp `bt`.

**Как работает функция**:

1.  Вычисляет остаток от деления `bt` на 21600.
2.  Вычитает полученный остаток из `bt`.
3.  Преобразует результат в строку.
4.  Возвращает полученную строку.

**Примеры**:

```python
bt = 1678886400
bw = getBw(bt)
print(f"BW: {bw}")
```

### `getN`

```python
def getN() -> str:
    """
    Генерирует base64-encoded timestamp.

    Args:
        None

    Returns:
        str: Сгенерированный base64-encoded timestamp.
    """
```

**Назначение**: Функция генерирует timestamp, кодирует его в base64 и возвращает закодированное значение в виде строки.

**Как работает функция**:

1.  Получает текущее время в виде timestamp с помощью функции `time.time()`.
2.  Преобразует timestamp в строку.
3.  Кодирует строку в base64.
4.  Декодирует base64-encoded значение в строку.
5.  Возвращает полученную строку.

**Примеры**:

```python
n = getN()
print(f"N: {n}")
```

### `get_request_config`

```python
async def get_request_config(request_config: RequestConfig, proxy: str) -> RequestConfig:
    """
    Получает конфигурацию запроса, включая токены Arkose Labs.

    Args:
        request_config (RequestConfig): Объект RequestConfig для хранения конфигурации.
        proxy (str): Адрес прокси-сервера.

    Returns:
        RequestConfig: Обновленный объект RequestConfig с токенами Arkose Labs.
    """
```

**Назначение**: Функция получает конфигурацию запроса, включая токены Arkose Labs.

**Как работает функция**:

1.  Если `request_config.proof_token` не установлен, читает HAR-файлы с помощью функции `readHAR()` и заполняет `request_config`.
2.  Если `request_config.arkose_request` установлен, генерирует и отправляет запрос Arkose Labs с помощью функций `genArkReq()` и `sendRequest()`, и сохраняет полученный токен в `request_config.arkose_token`.
3.  Возвращает обновленный объект `request_config`.

**Примеры**:

```python
import asyncio

async def main():
    request_config = RequestConfig()
    proxy = 'http://proxy:8080'
    updated_config = await get_request_config(request_config, proxy)
    print(f"Arkose Token: {updated_config.arkose_token}")

asyncio.run(main())
```