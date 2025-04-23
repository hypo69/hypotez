# Модуль для обработки HAR-файлов (openai.har_file)

## Обзор

Модуль `har_file.py` предназначен для чтения, парсинга и обработки HAR (HTTP Archive) файлов, содержащих данные HTTP-запросов и ответов. Он используется для извлечения необходимой информации, такой как токены доступа, proof-токены, turnstile-токены и данные для запросов Arkose Labs.

## Подробнее

Этот модуль предоставляет функциональность для работы с HAR-файлами, которые могут содержать важные данные для аутентификации и авторизации при взаимодействии с API. Он включает в себя функции для извлечения заголовков, парсинга записей HAR, генерации запросов Arkose Labs и получения конфигурации запроса.

## Функции

### `get_har_files`

```python
def get_har_files() -> list[str]:
    """Функция выполняет поиск HAR-файлов в директории с куками.

    Returns:
        list[str]: Список путей к найденным HAR-файлам.

    Raises:
        NoValidHarFileError: Если директория с HAR-файлами не читаема или не найдено ни одного HAR-файла.

    """
```

**Назначение**: Функция выполняет поиск файлов с расширением `.har` в директории, предназначенной для хранения куки и HAR-файлов. Она проверяет доступность директории и наличие в ней хотя бы одного HAR-файла.

**Возвращает**:
- `list[str]`: Список полных путей к найденным HAR-файлам. Если файлы не найдены, вызывает исключение `NoValidHarFileError`.

**Вызывает исключения**:
- `NoValidHarFileError`: Если директория `get_cookies_dir()` не доступна для чтения или если в ней не найдено ни одного файла с расширением `.har`.

**Как работает функция**:
1. Проверяет, доступна ли директория, возвращаемая функцией `get_cookies_dir()`, для чтения. Если нет, вызывает исключение `NoValidHarFileError`.
2. Обходит директорию `get_cookies_dir()` и все её поддиректории в поисках файлов с расширением `.har`.
3. Сохраняет полные пути к найденным файлам в список `harPath`.
4. Если список `harPath` пуст (т.е. HAR-файлы не найдены), вызывает исключение `NoValidHarFileError`.
5. Сортирует список `harPath` по времени модификации файлов (от старых к новым).
6. Возвращает отсортированный список путей к HAR-файлам.

**Примеры**:

Пример 1:

```python
try:
    har_files = get_har_files()
    print(f"Найдены HAR-файлы: {har_files}")
except NoValidHarFileError as ex:
    print(f"Ошибка: {ex}")
```

### `readHAR`

```python
def readHAR(request_config: RequestConfig) -> None:
    """Функция выполняет чтение и парсинг HAR-файлов для извлечения конфигурационных данных.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса, в который будут записаны извлеченные данные.

    Raises:
        NoValidHarFileError: Если не найден proof_token в .har файлах.

    """
```

**Назначение**: Функция читает HAR-файлы и извлекает из них различные параметры конфигурации, такие как access_token, proof_token, turnstile_token, cookies и заголовки. Эти данные используются для настройки последующих HTTP-запросов.

**Параметры**:
- `request_config` (RequestConfig): Объект класса `RequestConfig`, в который будут записываться извлеченные из HAR-файла данные.

**Возвращает**:
- None. Функция изменяет переданный объект `request_config`.

**Вызывает исключения**:
- `NoValidHarFileError`: Если в HAR-файлах не найден `proof_token`.

**Как работает функция**:
1. Получает список путей к HAR-файлам с помощью функции `get_har_files()`.
2. Итерируется по списку HAR-файлов и пытается прочитать каждый файл как JSON. Если файл не является корректным JSON, переходит к следующему файлу.
3. Для каждого файла проходит по записям (entries) в разделе `log` и ищет определенные URL и заголовки:
   - Если URL совпадает с `arkose_url`, парсит запись HAR с помощью функции `parseHAREntry` и сохраняет результат в `request_config.arkose_request`.
   - Если URL начинается с `start_url`, пытается извлечь `access_token` из текста ответа, а также `proof_token` и `turnstile_token` из заголовков. Куки также извлекаются из записи запроса.
4. В случае возникновения ошибок при чтении заголовков, логирует ошибки с помощью `debug.log`.
5. После обработки всех HAR-файлов, проверяет, был ли найден `proof_token`. Если нет, вызывает исключение `NoValidHarFileError`.

**Примеры**:

```python
from src.logger import logger
request_config = RequestConfig()
try:
    readHAR(request_config)
    logger.info("Данные успешно прочитаны из HAR-файлов.")
    print(f"Access Token: {request_config.access_token}")
    print(f"Proof Token: {request_config.proof_token}")
    print(f"Turnstile Token: {request_config.turnstile_token}")
    print(f"Cookies: {request_config.cookies}")
except NoValidHarFileError as ex:
    logger.error(f"Ошибка при чтении HAR-файлов: {ex}", exc_info=True)
except Exception as ex:
    logger.error(f"Произошла ошибка: {ex}", exc_info=True)
```

### `get_headers`

```python
def get_headers(entry: dict) -> dict:
    """Функция извлекает заголовки из записи HAR.

    Args:
        entry (dict): Запись HAR, содержащая информацию о запросе.

    Returns:
        dict: Словарь, содержащий заголовки запроса в нижнем регистре.

    """
```

**Назначение**: Функция извлекает HTTP-заголовки из записи HAR (HTTP Archive) и возвращает их в виде словаря, приводя имена заголовков к нижнему регистру.

**Параметры**:
- `entry` (dict): Словарь, представляющий запись HAR, содержащую информацию о HTTP-запросе и ответе.

**Возвращает**:
- `dict`: Словарь, где ключи - это имена заголовков в нижнем регистре, а значения - соответствующие значения заголовков. Исключаются заголовки `content-length` и `cookie`, а также заголовки, начинающиеся с `:`

**Как работает функция**:
1. Проходит по списку заголовков в записи `entry['request']['headers']`.
2. Для каждого заголовка проверяет, не является ли его имя `content-length` или `cookie`, а также не начинается ли оно с символа `:`.
3. Если заголовок не исключен, добавляет его в словарь, приводя имя заголовка к нижнему регистру.
4. Возвращает полученный словарь.

**Примеры**:

Пример использования:
```python
har_entry = {
    'request': {
        'headers': [
            {'name': 'Content-Type', 'value': 'application/json'},
            {'name': 'content-length', 'value': '123'},
            {'name': 'Cookie', 'value': 'sessionid=12345'},
            {'name': ':method', 'value': 'GET'},
            {'name': 'Accept', 'value': 'text/html'}
        ]
    }
}

headers = get_headers(har_entry)
print(headers)
# Expected output: {'content-type': 'application/json', 'accept': 'text/html'}
```

### `parseHAREntry`

```python
def parseHAREntry(entry: dict) -> arkReq:
    """Функция парсит запись HAR и создает объект arkReq.

    Args:
        entry (dict): Запись HAR, содержащая информацию о запросе.

    Returns:
        arkReq: Объект arkReq, содержащий извлеченные данные.

    """
```

**Назначение**: Функция преобразует запись HAR (HTTP Archive) в объект `arkReq`, содержащий информацию, необходимую для выполнения запросов Arkose Labs.

**Параметры**:
- `entry` (dict): Словарь, представляющий запись HAR, содержащую информацию о HTTP-запросе.

**Возвращает**:
- `arkReq`: Объект класса `arkReq`, содержащий извлеченные из записи HAR данные, такие как URL, заголовки, параметры POST-запроса и куки.

**Как работает функция**:
1. Создает экземпляр класса `arkReq` и заполняет его данными из записи HAR:
   - `arkURL` берется из `entry['request']['url']`.
   - `arkHeader` заполняется заголовками, извлеченными с помощью функции `get_headers(entry)`.
   - `arkBody` заполняется параметрами POST-запроса, извлеченными из `entry['request']['postData']['params']`. Параметры с именем `rnd` исключаются. Значения параметров декодируются с помощью `unquote`.
   - `arkCookies` заполняется куками, извлеченными из `entry['request']['cookies']`.
   - `userAgent` извлекается из заголовка `User-Agent`.
2. Извлекает зашифрованные данные `bda` из тела запроса и расшифровывает их с использованием `userAgent` и значения заголовка `x-ark-esync-value` (bw). Результат сохраняется в `tmpArk.arkBx`.
3. Возвращает объект `tmpArk`.

**Примеры**:

```python
from src.logger import logger
# Пример записи HAR (упрощенный)
har_entry = {
    'request': {
        'url': 'https://tcr9i.chat.openai.com/fc/gt2/public_key/35536E1E-65B4-4D96-9D97-6ADB7EFF8147',
        'headers': [
            {'name': 'User-Agent', 'value': 'Mozilla/5.0'},
            {'name': 'X-Ark-Esync-Value', 'value': 'some_value'}
        ],
        'postData': {
            'params': [
                {'name': 'bda', 'value': 'encrypted_data'},
                {'name': 'rnd', 'value': '0.123'}
            ]
        },
        'cookies': [
            {'name': 'cookie1', 'value': 'value1'}
        ]
    }
}

try:
    ark_request = parseHAREntry(har_entry)
    logger.info("Объект arkReq успешно создан.")
    print(f"URL: {ark_request.arkURL}")
    print(f"User-Agent: {ark_request.userAgent}")
    print(f"Cookies: {ark_request.arkCookies}")
except Exception as ex:
    logger.error(f"Ошибка при парсинге HAR entry: {ex}", exc_info=True)
```

### `genArkReq`

```python
def genArkReq(chatArk: arkReq) -> arkReq:
    """Функция генерирует новый запрос Arkose Labs на основе предоставленного шаблона.

    Args:
        chatArk (arkReq): Объект arkReq, содержащий базовую конфигурацию запроса Arkose Labs.

    Returns:
        arkReq: Новый объект arkReq с обновленными данными для запроса Arkose Labs.

    Raises:
        RuntimeError: Если предоставленный объект arkReq недействителен.

    """
```

**Назначение**: Функция генерирует новый запрос Arkose Labs на основе предоставленного шаблона, заменяя устаревшие или случайные значения на новые.

**Параметры**:
- `chatArk` (arkReq): Объект `arkReq`, содержащий базовую конфигурацию запроса Arkose Labs.

**Возвращает**:
- `arkReq`: Новый объект `arkReq` с обновленными данными для запроса Arkose Labs.

**Вызывает исключения**:
- `RuntimeError`: Если предоставленный объект `arkReq` недействителен (например, отсутствует тело или заголовки).

**Как работает функция**:
1. Создает глубокую копию объекта `chatArk`, чтобы не изменять исходный объект.
2. Проверяет, что скопированный объект `tmpArk` содержит необходимые данные (тело и заголовки). Если нет, вызывает исключение `RuntimeError`.
3. Генерирует новые значения для параметров `bda` и `rnd` в теле запроса, а также для заголовка `x-ark-esync-value`.
4. Возвращает обновленный объект `tmpArk`.

**Примеры**:

```python
from src.logger import logger
# Пример использования функции genArkReq
try:
    # Предположим, что chatArk уже определен и содержит валидные данные
    new_ark_req = genArkReq(chatArk)
    logger.info("Новый запрос Arkose Labs успешно сгенерирован.")
    print(f"Новый bda: {new_ark_req.arkBody.get('bda')}")
    print(f"Новый rnd: {new_ark_req.arkBody.get('rnd')}")
    print(f"Новый x-ark-esync-value: {new_ark_req.arkHeader.get('x-ark-esync-value')}")
except RuntimeError as ex:
    logger.error(f"Ошибка при генерации запроса Arkose Labs: {ex}", exc_info=True)
except Exception as ex:
    logger.error(f"Произошла ошибка: {ex}", exc_info=True)
```

### `sendRequest`

```python
async def sendRequest(tmpArk: arkReq, proxy: str = None) -> str:
    """Асинхронная функция отправляет запрос Arkose Labs и возвращает токен.

    Args:
        tmpArk (arkReq): Объект arkReq, содержащий данные для запроса Arkose Labs.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.

    Returns:
        str: Токен Arkose Labs, полученный в результате запроса.

    Raises:
        RuntimeError: Если не удалось сгенерировать валидный токен Arkose Labs.

    """
```

**Назначение**: Функция отправляет асинхронный POST-запрос к Arkose Labs с использованием предоставленных данных и возвращает полученный токен.

**Параметры**:
- `tmpArk` (arkReq): Объект `arkReq`, содержащий все необходимые данные для запроса, включая URL, заголовки, куки и тело запроса.
- `proxy` (str, optional): Строка, представляющая адрес прокси-сервера, который будет использоваться для отправки запроса. По умолчанию `None`, что означает отсутствие прокси.

**Возвращает**:
- `str`: Токен Arkose Labs, извлеченный из ответа сервера.

**Вызывает исключения**:
- `RuntimeError`: Если в ответе от Arkose Labs не содержится валидный токен (т.е. строка `sup=1|rid=` отсутствует в токене).

**Как работает функция**:
1. Использует асинхронный HTTP-клиент `StreamSession` для отправки POST-запроса по URL, указанному в `tmpArk.arkURL`.
2. Передает заголовки (`tmpArk.arkHeader`), куки (`tmpArk.arkCookies`) и тело запроса (`tmpArk.arkBody`) в POST-запрос.
3. Если указан прокси-сервер (`proxy`), настраивает прокси для сессии.
4. Получает JSON-ответ от сервера и извлекает значение ключа `token`, которое представляет собой токен Arkose Labs.
5. Проверяет, содержит ли полученный токен подстроку `sup=1|rid=`, что указывает на валидность токена. Если подстрока отсутствует, вызывает исключение `RuntimeError`.
6. Возвращает полученный токен.

**Примеры**:

```python
from src.logger import logger
# Пример использования функции sendRequest (асинхронный)
async def main():
    try:
        # Предположим, что tmpArk уже определен и содержит валидные данные
        arkose_token = await sendRequest(tmpArk, proxy='http://your_proxy:8080')
        logger.info("Токен Arkose Labs успешно получен.")
        print(f"Токен Arkose Labs: {arkose_token}")
    except RuntimeError as ex:
        logger.error(f"Ошибка при получении токена Arkose Labs: {ex}", exc_info=True)
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}", exc_info=True)

# Запуск асинхронной функции
# asyncio.run(main())
```

### `getBDA`

```python
def getBDA(arkReq: arkReq) -> tuple[str, str]:
    """Функция генерирует зашифрованные данные BDA и ключ BW для Arkose Labs.

    Args:
        arkReq (arkReq): Объект arkReq, содержащий данные для генерации BDA.

    Returns:
        tuple[str, str]: Кортеж, содержащий зашифрованные данные BDA и ключ BW.

    """
```

**Назначение**: Функция генерирует зашифрованные данные `bda` и ключ `bw`, необходимые для запросов Arkose Labs.

**Параметры**:
- `arkReq` (arkReq): Объект `arkReq`, содержащий данные, необходимые для генерации `bda` и `bw`.

**Возвращает**:
- `tuple[str, str]`: Кортеж, содержащий зашифрованные данные `bda` (в виде строки) и ключ `bw` (в виде строки).

**Как работает функция**:
1. Извлекает значение `bx` из объекта `arkReq`.
2. Заменяет в `bx` значение ключа `"n"` на новое значение, полученное с помощью функции `getN()`.
3. Ищет в `bx` старый UUID и заменяет его на новый, сгенерированный с помощью `uuid.uuid4()`.
4. Генерирует ключ `bw` с помощью функции `getBw(getBt())`.
5. Шифрует `bx` с использованием ключа, состоящего из `arkReq.userAgent` и `bw`.
6. Кодирует зашифрованные данные `bx` в base64 и возвращает их вместе с ключом `bw`.

**Примеры**:

```python
from src.logger import logger
# Пример использования функции getBDA
try:
    # Предположим, что ark_req уже определен и содержит валидные данные
    bda, bw = getBDA(ark_req)
    logger.info("Данные BDA и BW успешно сгенерированы.")
    print(f"BDA: {bda}")
    print(f"BW: {bw}")
except Exception as ex:
    logger.error(f"Ошибка при генерации данных BDA и BW: {ex}", exc_info=True)
```

### `getBt`

```python
def getBt() -> int:
    """Функция возвращает текущее время в формате Unix timestamp.

    Returns:
        int: Текущее время в формате Unix timestamp.

    """
```

**Назначение**: Функция возвращает текущее время в формате Unix timestamp (количество секунд, прошедших с начала эпохи Unix).

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `int`: Текущее время в формате Unix timestamp.

**Как работает функция**:
1. Использует функцию `time.time()` для получения текущего времени в секундах.
2. Преобразует полученное значение в целое число с помощью `int()`.
3. Возвращает полученное целое число.

**Примеры**:

```python
from src.logger import logger
# Пример использования функции getBt
try:
    current_time = getBt()
    logger.info("Текущее время успешно получено.")
    print(f"Текущее время (Unix timestamp): {current_time}")
except Exception as ex:
    logger.error(f"Ошибка при получении текущего времени: {ex}", exc_info=True)
```

### `getBw`

```python
def getBw(bt: int) -> str:
    """Функция вычисляет значение BW на основе предоставленного времени BT.

    Args:
        bt (int): Время в формате Unix timestamp.

    Returns:
        str: Значение BW, вычисленное на основе BT.

    """
```

**Назначение**: Функция вычисляет значение `bw` (bandwidth) на основе предоставленного времени `bt` (в формате Unix timestamp).

**Параметры**:
- `bt` (int): Время в формате Unix timestamp.

**Возвращает**:
- `str`: Значение `bw`, вычисленное на основе `bt`.

**Как работает функция**:
1. Вычисляет остаток от деления `bt` на 21600.
2. Вычитает полученный остаток из `bt`.
3. Преобразует результат в строку и возвращает его.

**Примеры**:

```python
from src.logger import logger
# Пример использования функции getBw
try:
    bt = getBt()  # Получаем текущее время в формате Unix timestamp
    bw = getBw(bt)
    logger.info("Значение BW успешно вычислено.")
    print(f"BT: {bt}")
    print(f"BW: {bw}")
except Exception as ex:
    logger.error(f"Ошибка при вычислении значения BW: {ex}", exc_info=True)
```

### `getN`

```python
def getN() -> str:
    """Функция генерирует строку N на основе текущего времени.

    Returns:
        str: Строка N, закодированная в Base64.

    """
```

**Назначение**: Функция генерирует строку `N` на основе текущего времени и кодирует ее в Base64.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строка `N`, закодированная в Base64.

**Как работает функция**:
1. Получает текущее время в формате Unix timestamp (количество секунд с начала эпохи Unix) и преобразует его в строку.
2. Кодирует полученную строку в Base64.
3. Декодирует закодированную строку из байтов в строку UTF-8.
4. Возвращает полученную строку.

**Примеры**:

```python
from src.logger import logger
# Пример использования функции getN
try:
    n = getN()
    logger.info("Строка N успешно сгенерирована.")
    print(f"N: {n}")
except Exception as ex:
    logger.error(f"Ошибка при генерации строки N: {ex}", exc_info=True)
```

### `get_request_config`

```python
async def get_request_config(request_config: RequestConfig, proxy: str) -> RequestConfig:
    """Асинхронная функция получает конфигурацию запроса, включая токены Arkose Labs.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.
        proxy (str): Адрес прокси-сервера.

    Returns:
        RequestConfig: Обновленный объект конфигурации запроса.

    """
```

**Назначение**: Функция асинхронно получает и обновляет конфигурацию запроса, включая чтение данных из HAR-файлов и получение токена Arkose Labs.

**Параметры**:
- `request_config` (RequestConfig): Объект конфигурации запроса, который необходимо обновить.
- `proxy` (str): Строка, представляющая адрес прокси-сервера, который будет использоваться для отправки запросов.

**Возвращает**:
- `RequestConfig`: Обновленный объект `RequestConfig` с полученными данными.

**Как работает функция**:
1. Проверяет, установлен ли `proof_token` в объекте `request_config`. Если нет, вызывает функцию `readHAR(request_config)` для чтения данных из HAR-файлов.
2. Проверяет, установлен ли `arkose_request` в объекте `request_config`. Если да, то генерирует и отправляет запрос Arkose Labs для получения токена, используя функции `genArkReq(request_config.arkose_request)` и `sendRequest(..., proxy)`. Полученный токен сохраняется в `request_config.arkose_token`.
3. Возвращает обновленный объект `request_config`.

**Примеры**:

```python
from src.logger import logger
# Пример использования функции get_request_config (асинхронный)
async def main():
    request_config = RequestConfig()
    proxy = 'http://your_proxy:8080'
    try:
        updated_config = await get_request_config(request_config, proxy)
        logger.info("Конфигурация запроса успешно получена.")
        print(f"Access Token: {updated_config.access_token}")
        print(f"Arkose Token: {updated_config.arkose_token}")
    except Exception as ex:
        logger.error(f"Ошибка при получении конфигурации запроса: {ex}", exc_info=True)
```

## Классы

### `RequestConfig`

```python
class RequestConfig:
    """Конфигурация запроса.
    
    Attributes:
        cookies (dict, optional): Куки для запроса. По умолчанию None.
        headers (dict, optional): Заголовки для запроса. По умолчанию None.
        access_token (str, optional): Токен доступа. По умолчанию None.
        proof_token (list, optional): Proof-токен. По умолчанию None.
        turnstile_token (str, optional): Turnstile-токен. По умолчанию None.
        arkose_request (arkReq, optional): Объект arkReq для запроса Arkose Labs. По умолчанию None.
        arkose_token (str, optional): Токен Arkose Labs. По умолчанию None.
        data_build (str, optional): Версия сборки данных. По умолчанию "prod-db8e51e8414e068257091cf5003a62d3d4ee6ed0".
    """
```

**Описание**: Класс `RequestConfig` предназначен для хранения конфигурационных данных, необходимых для выполнения HTTP-запросов. Он содержит атрибуты для хранения куки, заголовков, токенов доступа и другой информации.

**Атрибуты**:
- `cookies` (dict, optional): Куки для запроса. По умолчанию `None`.
- `headers` (dict, optional): Заголовки для запроса. По умолчанию `None`.
- `access_token` (str, optional): Токен доступа. По умолчанию `None`.
- `proof_token` (list, optional): Proof-токен. По умолчанию `None`.
- `turnstile_token` (str, optional): Turnstile-токен. По умолчанию `None`.
- `arkose_request` (arkReq, optional): Объект `arkReq` для запроса Arkose Labs. По умолчанию `None`.
- `arkose_token` (str, optional): Токен Arkose Labs. По умолчанию `None`.
- `data_build` (str, optional): Версия сборки данных. По умолчанию `"prod-db8e51e8414e068257091cf5003a62d3d4ee6ed0"`.

### `arkReq`

```python
class arkReq:
    """Класс для представления запроса Arkose Labs.
    
    Attributes:
        arkURL (str): URL для запроса Arkose Labs.
        arkBx (str): Зашифрованные данные для запроса Arkose Labs.
        arkHeader (dict): Заголовки для запроса Arkose Labs.
        arkBody (dict): Тело запроса Arkose Labs.
        arkCookies (dict): Куки для запроса Arkose Labs.
        userAgent (str): User-Agent для запроса Arkose Labs.
    """
```

**Описание**: Класс `arkReq` используется для хранения данных, необходимых для выполнения запросов к Arkose Labs. Он содержит атрибуты для хранения URL, зашифрованных данных, заголовков, тела запроса и куки.

**Атрибуты**:
- `arkURL` (str): URL для запроса Arkose Labs.
- `arkBx` (str): Зашифрованные данные для запроса Arkose Labs.
- `arkHeader` (dict): Заголовки для запроса Arkose Labs.
- `arkBody` (dict): Тело запроса Arkose Labs.
- `arkCookies` (dict): Куки для запроса Arkose Labs.
- `userAgent` (str): User-Agent для запроса Arkose Labs.