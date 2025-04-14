# Модуль для работы с HAR-файлами для получения конфигураций запросов

## Обзор

Модуль `har_file.py` предназначен для чтения и обработки HAR-файлов (HTTP Archive) с целью извлечения необходимой информации для настройки запросов, таких как cookies, headers, access_token, proof_token, turnstile_token и arkose_token. Данный модуль используется для автоматической конфигурации запросов к API, требующим определенной аутентификации и защиты от ботов. Он также включает функции для расшифровки и шифрования данных, необходимых для работы с Arkose Labs.

## Подробней

Модуль предоставляет функциональность для чтения HAR-файлов, поиска в них необходимых токенов и параметров, а также для генерации запросов Arkose Labs. Это позволяет автоматизировать процесс получения необходимых данных для взаимодействия с API, что особенно полезно в случаях, когда требуется обходить защиту от ботов или проходить аутентификацию.

## Классы

### `RequestConfig`

**Описание**: Класс, представляющий конфигурацию запроса. Содержит атрибуты для хранения cookies, headers, access_token, proof_token, turnstile_token, arkose_request, arkose_token и data_build.

**Атрибуты**:
- `cookies` (dict): Словарь с cookies.
- `headers` (dict): Словарь с headers.
- `access_token` (str): Access token.
- `proof_token` (list): Список proof token.
- `turnstile_token` (str): Turnstile token.
- `arkose_request` (arkReq): Объект запроса Arkose Labs.
- `arkose_token` (str): Токен Arkose Labs.
- `data_build` (str): Версия сборки данных.

### `arkReq`

**Описание**: Класс, представляющий запрос Arkose Labs. Содержит информацию об URL, заголовках, теле запроса, cookies и userAgent.

**Атрибуты**:
- `arkURL` (str): URL запроса Arkose Labs.
- `arkBx` (str): Зашифрованные данные Arkose Labs.
- `arkHeader` (dict): Словарь с заголовками запроса Arkose Labs.
- `arkBody` (dict): Словарь с телом запроса Arkose Labs.
- `arkCookies` (dict): Словарь с cookies запроса Arkose Labs.
- `userAgent` (str): User-Agent.

## Функции

### `get_har_files`

```python
def get_har_files() -> list[str]:
    """
    Находит все HAR-файлы в директории cookies.

    Returns:
        list[str]: Список путей к HAR-файлам.

    Raises:
        NoValidHarFileError: Если директория cookies не читаема или в ней нет HAR-файлов.

    Как работает функция:
    - Проверяет доступность директории cookies для чтения.
    - Проходит по всем файлам в директории cookies и добавляет пути к HAR-файлам в список.
    - Сортирует список HAR-файлов по времени изменения.
    - Если список пуст, выбрасывает исключение NoValidHarFileError.
    """
```

### `readHAR`

```python
def readHAR(request_config: RequestConfig) -> None:
    """
    Читает HAR-файлы и извлекает из них cookies, headers, access_token, proof_token и turnstile_token.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.

    Raises:
        NoValidHarFileError: Если не найден proof_token в HAR-файлах.

    Как работает функция:
    - Проходит по всем HAR-файлам, полученным из `get_har_files()`.
    - Открывает каждый файл и пытается загрузить его содержимое как JSON.
    - Проходит по каждой записи в HAR-файле и извлекает URL, headers и cookies.
    - Если URL соответствует URL Arkose Labs, парсит запись с помощью `parseHAREntry()`.
    - Если URL начинается с `start_url`, извлекает access_token, proof_token, turnstile_token и cookies.
    - Если не найден `proof_token`, выбрасывает исключение `NoValidHarFileError`.
    """
```

### `get_headers`

```python
def get_headers(entry: dict) -> dict:
    """
    Извлекает заголовки из записи HAR-файла.

    Args:
        entry (dict): Запись HAR-файла.

    Returns:
        dict: Словарь с заголовками, приведенными к нижнему регистру.

    Как работает функция:
    - Проходит по списку заголовков в записи HAR-файла.
    - Приводит имя каждого заголовка к нижнему регистру.
    - Исключает заголовки `content-length`, `cookie` и заголовки, начинающиеся с `:`.
    - Возвращает словарь с заголовками.
    """
```

### `parseHAREntry`

```python
def parseHAREntry(entry: dict) -> arkReq:
    """
    Парсит запись HAR-файла для получения информации о запросе Arkose Labs.

    Args:
        entry (dict): Запись HAR-файла.

    Returns:
        arkReq: Объект запроса Arkose Labs.

    Как работает функция:
    - Извлекает URL, заголовки, тело запроса и cookies из записи HAR-файла.
    - Создает объект `arkReq` с извлеченными данными.
    - Дешифрует данные `bda` из тела запроса с использованием `decrypt()`.
    - Возвращает объект `arkReq`.
    """
```

### `genArkReq`

```python
def genArkReq(chatArk: arkReq) -> arkReq:
    """
    Генерирует запрос Arkose Labs с обновленными параметрами.

    Args:
        chatArk (arkReq): Объект запроса Arkose Labs.

    Returns:
        arkReq: Объект запроса Arkose Labs с обновленными параметрами.

    Raises:
        RuntimeError: Если .har файл не валидный

    Как работает функция:
    - Создает глубокую копию объекта `chatArk`.
    - Проверяет наличие тела и заголовков запроса.
    - Генерирует новые значения `bda` и `bw` с использованием `getBDA()`.
    - Кодирует `bda` в base64.
    - Добавляет случайное число `rnd` в тело запроса.
    - Обновляет заголовок `x-ark-esync-value` значением `bw`.
    - Возвращает обновленный объект `arkReq`.
    """
```

### `sendRequest`

```python
async def sendRequest(tmpArk: arkReq, proxy: str = None) -> str:
    """
    Отправляет запрос Arkose Labs и получает токен.

    Args:
        tmpArk (arkReq): Объект запроса Arkose Labs.
        proxy (str, optional): Прокси-сервер. По умолчанию `None`.

    Returns:
        str: Токен Arkose Labs.

    Raises:
        RuntimeError: Если не удалось сгенерировать валидный токен Arkose Labs.

    Как работает функция:
    - Отправляет POST-запрос к URL Arkose Labs с использованием `StreamSession`.
    - Получает JSON-ответ и извлекает токен из поля `token`.
    - Проверяет наличие подстроки `sup=1|rid=` в токене.
    - Возвращает токен Arkose Labs.
    """
```

### `getBDA`

```python
def getBDA(arkReq: arkReq) -> tuple[str, str]:
    """
    Генерирует данные `bda` и `bw` для запроса Arkose Labs.

    Args:
        arkReq (arkReq): Объект запроса Arkose Labs.

    Returns:
        tuple[str, str]: Кортеж, содержащий зашифрованные данные `bda` и значение `bw`.

    Как работает функция:
    - Получает значение `bx` из объекта `arkReq`.
    - Заменяет значение ключа `n` в `bx` на новое значение, полученное с помощью `getN()`.
    - Заменяет старый UUID в `bx` на новый UUID.
    - Генерирует значение `bw` с использованием `getBw()` и `getBt()`.
    - Шифрует `bx` с использованием `encrypt()`.
    - Возвращает зашифрованные данные `bda` и значение `bw`.
    """
```

### `getBt`

```python
def getBt() -> int:
    """
    Возвращает текущее время в секундах.

    Returns:
        int: Текущее время в секундах.

    Как работает функция:
    - Получает текущее время с помощью `time.time()`.
    - Возвращает текущее время в виде целого числа.
    """
```

### `getBw`

```python
def getBw(bt: int) -> str:
    """
    Вычисляет значение `bw` на основе времени `bt`.

    Args:
        bt (int): Время в секундах.

    Returns:
        str: Значение `bw`.

    Как работает функция:
    - Вычисляет значение `bw` как `bt - (bt % 21600)`.
    - Возвращает значение `bw` в виде строки.
    """
```

### `getN`

```python
def getN() -> str:
    """
    Генерирует значение `n` на основе текущего времени.

    Returns:
        str: Значение `n`, закодированное в base64.

    Как работает функция:
    - Получает текущее время с помощью `time.time()`.
    - Кодирует текущее время в base64.
    - Возвращает закодированное значение.
    """
```

### `get_request_config`

```python
async def get_request_config(request_config: RequestConfig, proxy: str) -> RequestConfig:
    """
    Получает конфигурацию запроса, читая HAR-файлы и получая токен Arkose Labs.

    Args:
        request_config (RequestConfig): Объект конфигурации запроса.
        proxy (str): Прокси-сервер.

    Returns:
        RequestConfig: Объект конфигурации запроса с обновленными данными.

    Как работает функция:
    - Если `proof_token` не установлен, читает HAR-файлы с помощью `readHAR()`.
    - Если `arkose_request` установлен, генерирует и отправляет запрос Arkose Labs с помощью `genArkReq()` и `sendRequest()`.
    - Возвращает обновленный объект `request_config`.
    """