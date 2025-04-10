# Модуль crypt

## Обзор

Модуль `crypt.py` предназначен для обеспечения криптографических функций, необходимых для взаимодействия с API MiniMax. Он включает в себя функции для генерации хешей, формирования заголовков и обработки данных, используемых при обмене данными с сервером. Модуль содержит функции для имитации работы JavaScript-функций хеширования и формирования запросов.

## Подробней

Этот модуль играет важную роль в процессе аутентификации и формирования запросов к API MiniMax. Он обеспечивает совместимость с требованиями API, генерируя необходимые заголовки и параметры запросов.

## Классы

### `CallbackResults`

**Описание**: Класс `CallbackResults` используется для хранения результатов обратного вызова, содержащих токен аутентификации, путь запроса и временную метку.

**Атрибуты**:

- `token` (str): Токен аутентификации. По умолчанию `None`.
- `path_and_query` (str): Путь запроса с параметрами. По умолчанию `None`.
- `timestamp` (int): Временная метка. По умолчанию `None`.

## Функции

### `hash_function`

```python
def hash_function(base_string: str) -> str:
    """
    Mimics the hashFunction using MD5.
    """
    ...
```

**Назначение**: Функция `hash_function` имитирует хеш-функцию, использующую алгоритм MD5 для генерации хеша из входной строки.

**Параметры**:

- `base_string` (str): Строка, которую необходимо хешировать.

**Возвращает**:

- `str`: MD5-хеш входной строки в шестнадцатеричном формате.

**Как работает функция**:

1. Кодирует входную строку `base_string` в байты, используя кодировку UTF-8.
2. Вычисляет MD5-хеш полученных байтов.
3. Преобразует хеш в шестнадцатеричную строку.

```ascii
base_string --> encode(UTF-8) --> MD5-hash --> hexdigest
```

**Примеры**:

```python
result = hash_function("example")
print(result)  # Вывод: 9cf95a712995e719366d6c1c640d75ba
```

### `generate_yy_header`

```python
def generate_yy_header(has_search_params_path: str, body_to_yy: dict, time: int) -> str:
    """
    Python equivalent of the generateYYHeader function.
    """
    ...
```

**Назначение**: Функция `generate_yy_header` генерирует заголовок YY, необходимый для аутентификации и выполнения запросов к API MiniMax.

**Параметры**:

- `has_search_params_path` (str): Путь с параметрами поиска.
- `body_to_yy` (dict): Тело запроса, преобразованное функцией `get_body_to_yy`.
- `time` (int): Временная метка.

**Возвращает**:

- `str`: Сгенерированный хеш заголовка YY.

**Как работает функция**:

1. Кодирует `has_search_params_path` с использованием `urllib.parse.quote`.
2. Вычисляет хеш от `time`.
3. Объединяет закодированный путь, тело запроса и хеш времени в одну строку.
4. Вычисляет хеш от объединенной строки.

```ascii
has_search_params_path --> quote --> encoded_path
time --> hash_function --> time_hash
encoded_path + body_to_yy + time_hash --> combined_string
combined_string --> hash_function --> yy_header
```

**Примеры**:

```python
path = "/v4/api/chat/msg"
body = {"msgContent": "test", "characterID": "123", "chatID": "456"}
time = 1678886400
body_to_yy = get_body_to_yy(body)
header = generate_yy_header(path, body_to_yy, time)
print(header)  # Пример вывода: some_hash_value
```

### `get_body_to_yy`

```python
def get_body_to_yy(l):
    ...
```

**Назначение**: Функция `get_body_to_yy` преобразует тело запроса в строку, пригодную для хеширования и включения в заголовок YY.

**Параметры**:

- `l` (dict): Словарь, содержащий параметры запроса, такие как `msgContent`, `characterID` и `chatID`.

**Возвращает**:

- `str`: Строка, сгенерированная на основе хешей параметров запроса.

**Как работает функция**:

1. Извлекает значения `msgContent`, `characterID` и `chatID` из входного словаря `l`.
2. Удаляет символы переноса строки из `msgContent`.
3. Вычисляет хеши от `characterID`, `msgContent` и `chatID`.
4. Объединяет хеши в одну строку.
5. Добавляет хеш от пустой строки (имитирует `hashFunction(undefined)` в JS).

```ascii
l --> extract msgContent, characterID, chatID
msgContent --> replace newlines
characterID --> hash_function --> hash1
msgContent --> hash_function --> hash2
chatID --> hash_function --> hash3
"" --> hash_function --> hash4
hash1 + hash2 + hash3 + hash4 --> body_to_yy
```

**Примеры**:

```python
body = {"msgContent": "test", "characterID": "123", "chatID": "456"}
result = get_body_to_yy(body)
print(result)  # Пример вывода: some_hash_value
```

### `get_body_json`

```python
def get_body_json(s):
    return json.dumps(s, ensure_ascii=True, sort_keys=True)
```

**Назначение**: Функция `get_body_json` преобразует входной объект в JSON-строку, обеспечивая кодировку ASCII и сортировку ключей.

**Параметры**:

- `s`: Объект, который необходимо преобразовать в JSON.

**Возвращает**:

- `str`: JSON-представление входного объекта.

**Как работает функция**:

1. Использует `json.dumps` для преобразования объекта `s` в JSON-строку.
2. Устанавливает `ensure_ascii=True` для кодирования не-ASCII символов.
3. Устанавливает `sort_keys=True` для сортировки ключей в алфавитном порядке.

```ascii
s --> json.dumps(ensure_ascii=True, sort_keys=True) --> json_string
```

**Примеры**:

```python
data = {"key1": "value1", "key2": "value2"}
result = get_body_json(data)
print(result)  # Вывод: {"key1": "value1", "key2": "value2"}
```

### `get_browser_callback`

```python
async def get_browser_callback(auth_result: CallbackResults):
    async def callback(page: Tab):
        while not auth_result.token:
            auth_result.token = await page.evaluate("localStorage.getItem(\'_token\')")
            if not auth_result.token:
                await asyncio.sleep(1)
        (auth_result.path_and_query, auth_result.timestamp) = await page.evaluate("""
            const device_id = localStorage.getItem("USER_HARD_WARE_INFO");
            const uuid = localStorage.getItem("UNIQUE_USER_ID");
            const os_name = navigator.userAgentData?.platform || navigator.platform || "Unknown";
            const browser_name = (() => {
                const userAgent = navigator.userAgent.toLowerCase();
                if (userAgent.includes("chrome") && !userAgent.includes("edg")) return "chrome";
                if (userAgent.includes("edg")) return "edge";
                if (userAgent.includes("firefox")) return "firefox";
                if (userAgent.includes("safari") && !userAgent.includes("chrome")) return "safari";
                return "unknown";
            })();
            const cpu_core_num = navigator.hardwareConcurrency || 8;
            const browser_language = navigator.language || "unknown";
            const browser_platform = `${navigator.platform || "unknown"}`;\n            const screen_width = window.screen.width || "unknown";
            const screen_height = window.screen.height || "unknown";
            const unix = Date.now(); // Current Unix timestamp in milliseconds
            const params = {
                device_platform: "web",
                biz_id: 2,
                app_id: 3001,
                version_code: 22201,
                lang: "en",
                uuid,
                device_id,
                os_name,
                browser_name,
                cpu_core_num,
                browser_language,
                browser_platform,
                screen_width,
                screen_height,
                unix
            };\n            [new URLSearchParams(params).toString(), unix]\n        """)
        auth_result.path_and_query = f"{API_PATH}?{auth_result.path_and_query}"
    return callback
```

**Назначение**: Функция `get_browser_callback` создает асинхронную функцию обратного вызова, которая извлекает токен аутентификации и параметры запроса из браузера.

**Параметры**:

- `auth_result` (CallbackResults): Объект `CallbackResults` для хранения полученных данных.

**Возвращает**:

- `callback` (async function): Асинхронная функция обратного вызова, которая принимает объект `page` (представляющий вкладку браузера) в качестве аргумента.

**Как работает функция**:

1. Определяет внутреннюю асинхронную функцию `callback`, которая будет выполняться в контексте браузера.
2. В цикле ожидает, пока не будет получен токен аутентификации из `localStorage` браузера.
3. Извлекает параметры запроса и временную метку из браузера, выполняя JavaScript-код.
4. Формирует полный путь запроса, объединяя `API_PATH` с полученными параметрами.
5. Сохраняет полученные данные в объекте `auth_result`.

**Внутренние функции**:

#### `callback`

```python
async def callback(page: Tab):
    ...
```

**Назначение**: Асинхронная функция обратного вызова, извлекающая токен аутентификации и параметры запроса из браузера.

**Параметры**:

- `page` (Tab): Объект, представляющий вкладку браузера.

**Как работает функция**:

1. В цикле ожидает, пока не будет получен токен аутентификации из `localStorage` браузера.
2. Извлекает параметры запроса и временную метку из браузера, выполняя JavaScript-код. JavaScript код собирает информацию об устройстве и браузере пользователя, такую как ID устройства, UUID, название операционной системы, название браузера, количество ядер CPU, язык браузера, платформа браузера, ширина и высота экрана. Эти данные используются для формирования параметров запроса.
3. Формирует полный путь запроса, объединяя `API_PATH` с полученными параметрами.
4. Сохраняет полученные данные в объекте `auth_result`.

```ascii
auth_result --> wait for token in localStorage --> token
page --> evaluate JavaScript --> path_and_query, timestamp
auth_result.path_and_query = API_PATH + path_and_query
```

**Примеры**:

```python
auth_result = CallbackResults()
callback = get_browser_callback(auth_result)
# Предполагается, что `page` - это объект, представляющий вкладку браузера
# await callback(page)
# Теперь `auth_result` содержит токен, путь запроса и временную метку