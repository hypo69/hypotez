# Модуль для работы с HAR-файлами для OpenAI

## Обзор

Модуль предоставляет функциональность для чтения, парсинга и обработки HAR-файлов (HTTP Archive) с целью извлечения необходимой информации для взаимодействия с API OpenAI. Он включает в себя функции для поиска и чтения HAR-файлов, извлечения токенов доступа, proof_token, turnstile_token, а также парсинга данных для запросов Arkose Labs.

## Подробней

Этот модуль предназначен для автоматического извлечения конфигурационных данных из HAR-файлов, которые могут быть получены при взаимодействии с веб-сайтом OpenAI. Собранные данные используются для аутентификации и авторизации при отправке запросов к API OpenAI, а также для решения задач, связанных с Arkose Labs (FunCaptcha). Это позволяет обходить различные защиты и ограничения, используемые OpenAI.

## Классы

### `RequestConfig`

**Описание**: Класс, предназначенный для хранения конфигурационных данных, необходимых для выполнения запросов к API OpenAI.

**Атрибуты**:
- `cookies` (dict): Словарь с куками, полученными из HAR-файла.
- `headers` (dict): Словарь с заголовками, полученными из HAR-файла.
- `access_token` (str): Токен доступа для API OpenAI.
- `proof_token` (list): Список, представляющий собой proof_token.
- `turnstile_token` (str): Turnstile токен.
- `arkose_request` (arkReq): Объект класса `arkReq`, содержащий данные для запроса к Arkose Labs.
- `arkose_token` (str): Токен, полученный от Arkose Labs.
- `data_build` (str): Строка, представляющая собой версию сборки данных.

### `arkReq`

**Описание**: Класс, предназначенный для хранения данных, необходимых для выполнения запросов к Arkose Labs (FunCaptcha).

**Атрибуты**:
- `arkURL` (str): URL для запроса к Arkose Labs.
- `arkBx` (str): Зашифрованное значение, используемое для Arkose Labs.
- `arkHeader` (dict): Словарь с заголовками для запроса к Arkose Labs.
- `arkBody` (dict): Словарь с данными тела запроса для Arkose Labs.
- `arkCookies` (dict): Словарь с куками для запроса к Arkose Labs.
- `userAgent` (str): User-Agent, используемый для запроса к Arkose Labs.

## Функции

### `get_har_files`

```python
def get_har_files() -> list[str]:
    """
    Находит все HAR-файлы в директории с куками.

    Args:
        None

    Returns:
        list[str]: Список путей к HAR-файлам.

    Raises:
        NoValidHarFileError: Если директория с HAR-файлами недоступна для чтения или не содержит HAR-файлов.

    """
```

**Назначение**: Функция выполняет поиск всех файлов с расширением `.har` в директории, указанной как директория для хранения куки, и возвращает список путей к этим файлам.

**Как работает функция**:
1. Проверяет, доступна ли директория для чтения. Если нет, вызывает исключение `NoValidHarFileError`.
2. Обходит директорию и все её поддиректории в поисках файлов с расширением `.har`.
3. Добавляет пути к найденным файлам в список `harPath`.
4. Если список `harPath` пуст (т.е. HAR-файлы не найдены), вызывает исключение `NoValidHarFileError`.
5. Сортирует список `harPath` по дате изменения файла (от старых к новым).
6. Возвращает отсортированный список путей к HAR-файлам.

```
A: Проверка доступности директории для чтения
|
B: Обход директории и поиск HAR-файлов
|
C: Проверка, найдены ли HAR-файлы
|
D: Сортировка HAR-файлов по дате изменения
|
E: Возврат списка HAR-файлов
```

**Примеры**:

```python
try:
    har_files = get_har_files()
    print(f"Найденные HAR-файлы: {har_files}")
except NoValidHarFileError as ex:
    print(f"Ошибка: {ex}")
```

### `readHAR`

```python
def readHAR(request_config: RequestConfig) -> None:
    """
    Считывает данные из HAR-файлов и заполняет объект RequestConfig.

    Args:
        request_config (RequestConfig): Объект RequestConfig для заполнения данными из HAR-файлов.

    Returns:
        None

    Raises:
        NoValidHarFileError: Если proof_token не найден в HAR-файлах.
    """
```

**Назначение**: Функция читает HAR-файлы, извлекает из них данные (токены, заголовки, куки) и сохраняет их в объект `RequestConfig`.

**Как работает функция**:

1. Получает список HAR-файлов с помощью функции `get_har_files()`.
2. Перебирает каждый HAR-файл в списке.
3. Открывает HAR-файл и пытается загрузить его содержимое как JSON. Если возникают ошибки при чтении JSON, переходит к следующему файлу.
4. Перебирает записи в HAR-файле (`harFile['log']['entries']`).
5. Для каждой записи:
   - Извлекает заголовки с помощью функции `get_headers()`.
   - Если URL записи соответствует `arkose_url`, парсит запись с помощью `parseHAREntry()` и сохраняет результат в `request_config.arkose_request`.
   - Если URL записи начинается с `start_url`, пытается извлечь `access_token` из текста ответа, а также `proof_token` и `turnstile_token` из заголовков. Куки извлекаются из запроса.
6. Если после обработки всех HAR-файлов `request_config.proof_token` остается `None`, вызывает исключение `NoValidHarFileError`.

```
A: Получение списка HAR-файлов
|
B: Перебор HAR-файлов
|
C: Загрузка содержимого HAR-файла как JSON
|
D: Перебор записей в HAR-файле
|
E: Извлечение заголовков
|
F: Проверка URL записи на соответствие arkose_url или start_url
|
G: Извлечение данных (access_token, proof_token, turnstile_token, куки)
|
H: Проверка наличия proof_token после обработки всех файлов
```

**Примеры**:

```python
request_config = RequestConfig()
try:
    readHAR(request_config)
    print(f"Access Token: {request_config.access_token}")
    print(f"Proof Token: {request_config.proof_token}")
except NoValidHarFileError as ex:
    print(f"Ошибка: {ex}")
```

### `get_headers`

```python
def get_headers(entry: dict) -> dict:
    """
    Извлекает заголовки из записи HAR-файла.

    Args:
        entry (dict): Запись из HAR-файла.

    Returns:
        dict: Словарь с заголовками, приведенными к нижнему регистру.
    """
```

**Назначение**: Функция извлекает заголовки из записи HAR-файла и возвращает их в виде словаря, приводя имена заголовков к нижнему регистру.

**Как работает функция**:

1. Перебирает заголовки в записи HAR-файла (`entry['request']['headers']`).
2. Исключает заголовки `content-length`, `cookie` и заголовки, начинающиеся с `:`.
3. Приводит имя каждого заголовка к нижнему регистру.
4. Возвращает словарь, где ключи - имена заголовков (в нижнем регистре), а значения - значения заголовков.

```
A: Перебор заголовков в записи HAR-файла
|
B: Исключение нежелательных заголовков
|
C: Приведение имени заголовка к нижнему регистру
|
D: Возврат словаря с заголовками
```

**Примеры**:

```python
entry = {
    'request': {
        'headers': [
            {'name': 'Content-Type', 'value': 'application/json'},
            {'name': 'Cookie', 'value': 'test=123'},
            {'name': 'X-Custom-Header', 'value': 'custom_value'}
        ]
    }
}
headers = get_headers(entry)
print(headers)  # Вывод: {'content-type': 'application/json', 'x-custom-header': 'custom_value'}
```

### `parseHAREntry`

```python
def parseHAREntry(entry: dict) -> arkReq:
    """
    Парсит запись HAR-файла для извлечения данных Arkose Labs.

    Args:
        entry (dict): Запись из HAR-файла.

    Returns:
        arkReq: Объект класса arkReq с данными для запроса к Arkose Labs.
    """
```

**Назначение**: Функция парсит запись HAR-файла, содержащую информацию о запросе к Arkose Labs, и создает объект класса `arkReq` с извлеченными данными.

**Как работает функция**:

1. Создает временный объект `arkReq`.
2. Заполняет поля объекта `arkReq` данными из записи HAR-файла:
   - `arkURL` берется из `entry['request']['url']`.
   - `arkHeader` получается с помощью функции `get_headers(entry)`.
   - `arkBody` формируется из параметров POST-запроса (`entry['request']['postData']['params']`), исключая параметр `rnd`, и декодируя значения параметров с помощью `unquote()`.
   - `arkCookies` формируется из куки запроса (`entry['request']['cookies']`).
3. Извлекает `userAgent` из заголовков.
4. Извлекает значения `bda` и `bw` из тела запроса и заголовков соответственно.
5. Расшифровывает значение `bda` с использованием `userAgent` и `bw` с помощью функции `decrypt()`. Результат сохраняется в `tmpArk.arkBx`.
6. Возвращает объект `tmpArk`.

```
A: Создание временного объекта arkReq
|
B: Заполнение полей объекта arkReq данными из записи HAR-файла
|
C: Извлечение userAgent
|
D: Извлечение значений bda и bw
|
E: Расшифровка значения bda
|
F: Возврат объекта arkReq
```

**Примеры**:

```python
entry = {
    'request': {
        'url': 'https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147',
        'headers': [
            {'name': 'User-Agent', 'value': 'Mozilla/5.0'},
            {'name': 'X-Ark-Esync-Value', 'value': 'test_bw'}
        ],
        'postData': {
            'params': [
                {'name': 'bda', 'value': 'encrypted_data'},
                {'name': 'rnd', 'value': '0.123'}
            ]
        },
        'cookies': [
            {'name': 'test_cookie', 'value': 'cookie_value'}
        ]
    }
}
ark_req = parseHAREntry(entry)
print(ark_req.arkURL)
print(ark_req.arkBody)
```

### `genArkReq`

```python
def genArkReq(chatArk: arkReq) -> arkReq:
    """
    Генерирует новый запрос Arkose Labs на основе существующего.

    Args:
        chatArk (arkReq): Объект класса arkReq с данными для запроса к Arkose Labs.

    Returns:
        arkReq: Новый объект класса arkReq с обновленными данными для запроса к Arkose Labs.

    Raises:
        RuntimeError: Если предоставленный объект arkReq недействителен.
    """
```

**Назначение**: Функция генерирует новый запрос Arkose Labs на основе существующего, обновляя значения `bda` и `rnd` в теле запроса, а также `x-ark-esync-value` в заголовках.

**Как работает функция**:

1. Создает глубокую копию объекта `chatArk`.
2. Проверяет, что `tmpArk` не `None` и что у него есть `arkBody` и `arkHeader`. Если нет, вызывает исключение `RuntimeError`.
3. Получает новые значения `bda` и `bw` с помощью функции `getBDA()`.
4. Кодирует `bda` в base64 и обновляет значение `bda` в `tmpArk.arkBody`.
5. Генерирует случайное число и обновляет значение `rnd` в `tmpArk.arkBody`.
6. Обновляет значение `x-ark-esync-value` в `tmpArk.arkHeader` на новое значение `bw`.
7. Возвращает обновленный объект `tmpArk`.

```
A: Создание глубокой копии объекта chatArk
|
B: Проверка валидности объекта arkReq
|
C: Получение новых значений bda и bw
|
D: Кодирование bda в base64 и обновление значения в tmpArk.arkBody
|
E: Генерация случайного числа и обновление значения rnd в tmpArk.arkBody
|
F: Обновление значения x-ark-esync-value в tmpArk.arkHeader
|
G: Возврат обновленного объекта arkReq
```

**Примеры**:

```python
ark_req = arkReq(
    arkURL='https://example.com',
    arkBx='test_bx',
    arkHeader={'x-ark-esync-value': 'old_bw', 'User-Agent': 'Mozilla/5.0'},
    arkBody={'bda': 'old_bda'},
    arkCookies={},
    userAgent='Mozilla/5.0'
)

try:
    new_ark_req = genArkReq(ark_req)
    print(f"New bda: {new_ark_req.arkBody['bda']}")
    print(f"New x-ark-esync-value: {new_ark_req.arkHeader['x-ark-esync-value']}")
except RuntimeError as ex:
    print(f"Ошибка: {ex}")
```

### `sendRequest`

```python
async def sendRequest(tmpArk: arkReq, proxy: str = None) -> str:
    """
    Отправляет запрос к Arkose Labs и возвращает токен.

    Args:
        tmpArk (arkReq): Объект класса arkReq с данными для запроса к Arkose Labs.
        proxy (str, optional): Строка с прокси-сервером. По умолчанию None.

    Returns:
        str: Токен Arkose Labs.

    Raises:
        RuntimeError: Если не удалось получить токен Arkose Labs.
    """
```

**Назначение**: Функция отправляет асинхронный POST-запрос к Arkose Labs с использованием предоставленных данных и возвращает полученный токен.

**Как работает функция**:

1. Создает асинхронную сессию с использованием `StreamSession` с заголовками, куками и прокси (если указан).
2. Отправляет POST-запрос к `tmpArk.arkURL` с данными из `tmpArk.arkBody`.
3. Получает JSON-ответ из ответа.
4. Извлекает значение токена из JSON-ответа (`data.get("token")`).
5. Проверяет, содержит ли токен подстроку `sup=1|rid=`. Если нет, вызывает исключение `RuntimeError`.
6. Возвращает токен.

```
A: Создание асинхронной сессии
|
B: Отправка POST-запроса к Arkose Labs
|
C: Получение JSON-ответа
|
D: Извлечение значения токена
|
E: Проверка валидности токена
|
F: Возврат токена
```

**Примеры**:

```python
import asyncio
async def main():
    ark_req = arkReq(
        arkURL='https://example.com',
        arkBx='test_bx',
        arkHeader={'x-ark-esync-value': 'old_bw', 'User-Agent': 'Mozilla/5.0'},
        arkBody={'bda': 'old_bda'},
        arkCookies={},
        userAgent='Mozilla/5.0'
    )

    try:
        token = await sendRequest(ark_req)
        print(f"Arkose Token: {token}")
    except RuntimeError as ex:
        print(f"Ошибка: {ex}")

asyncio.run(main())
```

### `getBDA`

```python
def getBDA(arkReq: arkReq) -> tuple[str, str]:
    """
    Генерирует зашифрованное значение bda и bw для Arkose Labs.

    Args:
        arkReq (arkReq): Объект класса arkReq с данными для запроса к Arkose Labs.

    Returns:
        tuple[str, str]: Кортеж, содержащий зашифрованное значение bda и bw.
    """
```

**Назначение**: Функция генерирует зашифрованное значение `bda` и `bw` для запроса к Arkose Labs, используя предоставленные данные из объекта `arkReq`.

**Как работает функция**:

1. Получает значение `bx` из `arkReq.arkBx`.
2. Заменяет значение ключа `"key":"n"` в `bx` на новое значение, полученное с помощью функции `getN()`.
3. Ищет старый UUID в `bx` и заменяет его на новый UUID.
4. Генерирует новое значение `bw` с помощью функций `getBt()` и `getBw()`.
5. Шифрует `bx` с использованием `arkReq.userAgent` и `bw` с помощью функции `encrypt()`.
6. Возвращает кортеж, содержащий зашифрованное значение `bx` и `bw`.

```
A: Получение значения bx
|
B: Замена значения ключа "key":"n"
|
C: Замена старого UUID на новый
|
D: Генерация нового значения bw
|
E: Шифрование bx
|
F: Возврат зашифрованного значения bx и bw
```

**Примеры**:

```python
ark_req = arkReq(
    arkURL='https://example.com',
    arkBx='test_bx',
    arkHeader={'x-ark-esync-value': 'old_bw', 'User-Agent': 'Mozilla/5.0'},
    arkBody={'bda': 'old_bda'},
    arkCookies={},
    userAgent='Mozilla/5.0'
)

encrypted_bx, bw = getBDA(ark_req)
print(f"Encrypted bx: {encrypted_bx}")
print(f"Bw: {bw}")
```

### `getBt`

```python
def getBt() -> int:
    """
    Получает текущее время в формате Unix timestamp.

    Args:
        None

    Returns:
        int: Текущее время в формате Unix timestamp.
    """
```

**Назначение**: Функция возвращает текущее время в формате Unix timestamp (количество секунд, прошедших с начала эпохи Unix).

**Как работает функция**:

1. Получает текущее время с помощью `time.time()`.
2. Преобразует время в целое число.
3. Возвращает полученное значение.

```
A: Получение текущего времени
|
B: Преобразование времени в целое число
|
C: Возврат времени в формате Unix timestamp
```

**Примеры**:

```python
bt = getBt()
print(f"Bt: {bt}")
```

### `getBw`

```python
def getBw(bt: int) -> str:
    """
    Вычисляет значение bw на основе времени bt.

    Args:
        bt (int): Время в формате Unix timestamp.

    Returns:
        str: Вычисленное значение bw.
    """
```

**Назначение**: Функция вычисляет значение `bw` на основе предоставленного времени `bt` (Unix timestamp).

**Как работает функция**:

1. Вычисляет остаток от деления `bt` на 21600.
2. Вычитает остаток из `bt`.
3. Преобразует результат в строку.
4. Возвращает полученную строку.

```
A: Вычисление остатка от деления bt на 21600
|
B: Вычитание остатка из bt
|
C: Преобразование результата в строку
|
D: Возврат вычисленного значения bw
```

**Примеры**:

```python
bt = int(time.time())
bw = getBw(bt)
print(f"Bw: {bw}")
```

### `getN`

```python
def getN() -> str:
    """
    Генерирует значение n на основе текущего времени.

    Args:
        None

    Returns:
        str: Значение n, закодированное в base64.
    """
```

**Назначение**: Функция генерирует значение `n` на основе текущего времени и кодирует его в base64.

**Как работает функция**:

1. Получает текущее время в формате Unix timestamp и преобразует его в строку.
2. Кодирует строку с временем в base64.
3. Декодирует закодированное значение в строку.
4. Возвращает полученную строку.

```
A: Получение текущего времени в формате Unix timestamp
|
B: Кодирование строки с временем в base64
|
C: Декодирование закодированного значения в строку
|
D: Возврат значения n
```

**Примеры**:

```python
n = getN()
print(f"N: {n}")
```

### `get_request_config`

```python
async def get_request_config(request_config: RequestConfig, proxy: str) -> RequestConfig:
    """
    Обновляет конфигурацию запроса, получая данные из HAR-файлов и Arkose Labs.

    Args:
        request_config (RequestConfig): Объект RequestConfig для обновления.
        proxy (str): Прокси-сервер для использования.

    Returns:
        RequestConfig: Обновленный объект RequestConfig.
    """
```

**Назначение**: Функция обновляет конфигурацию запроса, получая данные из HAR-файлов и запрашивая токен у Arkose Labs, если необходимо.

**Как работает функция**:

1. Если `request_config.proof_token` равен `None`, читает данные из HAR-файлов с помощью функции `readHAR()`.
2. Если `request_config.arkose_request` не равен `None`, генерирует и отправляет запрос к Arkose Labs с помощью функций `genArkReq()` и `sendRequest()`, и сохраняет полученный токен в `request_config.arkose_token`.
3. Возвращает обновленный объект `request_config`.

```
A: Проверка наличия proof_token
|
B: Чтение данных из HAR-файлов
|
C: Проверка наличия arkose_request
|
D: Генерация и отправка запроса к Arkose Labs
|
E: Возврат обновленного объекта request_config
```

**Примеры**:

```python
import asyncio

async def main():
    request_config = RequestConfig()
    proxy = None  # Замените на свой прокси, если необходимо

    updated_config = await get_request_config(request_config, proxy)

    print(f"Access Token: {updated_config.access_token}")
    print(f"Arkose Token: {updated_config.arkose_token}")

asyncio.run(main())