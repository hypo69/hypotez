# Модуль crypt.py

## Обзор

Модуль `crypt.py` предназначен для обеспечения криптографических функций, необходимых для взаимодействия с API mini_max. Он включает в себя функции для генерации хешей, формирования заголовков и подготовки данных для запросов.

## Подробнее

Этот модуль содержит функции, которые эмулируют криптографические операции, используемые в JavaScript, для обеспечения совместимости с API mini_max. Он включает функции хеширования, создания заголовков и формирования JSON-структур для запросов. Он также включает асинхронную функцию для получения callback из браузера для авторизации.

## Классы

### `CallbackResults`

**Описание**: Класс для хранения результатов обратного вызова, содержащий токен авторизации, путь запроса и временную метку.

**Принцип работы**:
Класс `CallbackResults` используется для хранения данных, полученных в результате выполнения JavaScript-кода в браузере. Он содержит токен авторизации, путь запроса и временную метку, необходимые для последующих запросов к API.

**Атрибуты**:
- `token` (str): Токен авторизации.
- `path_and_query` (str): Путь запроса с параметрами.
- `timestamp` (int): Временная метка.

## Функции

### `hash_function`

```python
def hash_function(base_string: str) -> str:
    """
    Mimics the hashFunction using MD5.
    """
    ...
```

**Назначение**: Функция эмулирует функцию хеширования MD5.

**Параметры**:
- `base_string` (str): Строка для хеширования.

**Возвращает**:
- `str`: MD5 хеш строки в шестнадцатеричном формате.

**Как работает функция**:
1. Кодирует входную строку `base_string` в байты, используя кодировку UTF-8.
2. Вычисляет MD5 хеш закодированной строки.
3. Возвращает хеш в шестнадцатеричном формате.

```
Строка для хеширования
     ↓
Кодирование строки в байты (UTF-8)
     ↓
Вычисление MD5 хеша
     ↓
Преобразование хеша в шестнадцатеричный формат
     ↓
Возврат хеша
```

**Примеры**:
```python
hash_function("test")
```

### `generate_yy_header`

```python
def generate_yy_header(has_search_params_path: str, body_to_yy: dict, time: int) -> str:
    """
    Python equivalent of the generateYYHeader function.
    """
    ...
```

**Назначение**: Функция генерирует заголовок YY, необходимый для запросов к API.

**Параметры**:
- `has_search_params_path` (str): Путь с параметрами поиска.
- `body_to_yy` (dict): Тело запроса, преобразованное в строку.
- `time` (int): Временная метка.

**Возвращает**:
- `str`: Сгенерированный заголовок YY.

**Как работает функция**:
1. Кодирует `has_search_params_path` с помощью `urllib.parse.quote`.
2. Вычисляет хеш от временной метки `time`.
3. Объединяет закодированный путь, тело запроса и хеш временной метки в одну строку.
4. Вычисляет MD5 хеш объединенной строки.
5. Возвращает полученный хеш.

```
Путь с параметрами поиска, Тело запроса, Временная метка
     ↓
Кодирование пути
     ↓
Вычисление хеша временной метки
     ↓
Объединение закодированного пути, тела запроса и хеша времени в одну строку
     ↓
Вычисление MD5 хеша объединенной строки
     ↓
Возврат хеша
```

**Примеры**:
```python
generate_yy_header("/api/chat", {"msg": "hello"}, 1678886400)
```

### `get_body_to_yy`

```python
def get_body_to_yy(l):
    L = l["msgContent"].replace("\\r\\n", "").replace("\\n", "").replace("\\r", "")
    M = hash_function(l["characterID"]) + hash_function(L) + hash_function(l["chatID"])\
        + hash_function("")  # Mimics hashFunction(undefined) in JS

    # print("bodyToYY:", M)
    return M
```

**Назначение**: Функция генерирует строку для тела запроса.

**Параметры**:
- `l` (dict): Словарь, содержащий данные для формирования тела запроса.

**Возвращает**:
- `str`: Сгенерированная строка для тела запроса.

**Как работает функция**:
1. Извлекает `msgContent` из словаря `l` и удаляет символы переноса строки.
2. Вычисляет хеши для `characterID`, `msgContent` и `chatID`.
3. Объединяет полученные хеши в одну строку.
4. Добавляет хеш пустой строки (эмуляция `hashFunction(undefined)` в JavaScript).
5. Возвращает объединенную строку.

```
Словарь с данными
     ↓
Извлечение и очистка msgContent
     ↓
Вычисление хешей characterID, msgContent и chatID
     ↓
Объединение хешей
     ↓
Добавление хеша пустой строки
     ↓
Возврат объединенной строки
```

**Примеры**:
```python
get_body_to_yy({"msgContent": "test message", "characterID": "123", "chatID": "456"})
```

### `get_body_json`

```python
def get_body_json(s):
    return json.dumps(s, ensure_ascii=True, sort_keys=True)
```

**Назначение**: Функция преобразует объект Python в JSON-строку с сортировкой ключей и поддержкой ASCII.

**Параметры**:
- `s`: Объект Python для преобразования в JSON.

**Возвращает**:
- `str`: JSON-строка.

**Как работает функция**:
1. Использует `json.dumps` для преобразования объекта `s` в JSON-строку.
2. Устанавливает `ensure_ascii=True` для поддержки ASCII.
3. Устанавливает `sort_keys=True` для сортировки ключей в JSON-строке.
4. Возвращает полученную JSON-строку.

```
Объект Python
     ↓
Преобразование в JSON-строку
     ↓
Поддержка ASCII
     ↓
Сортировка ключей
     ↓
Возврат JSON-строки
```

**Примеры**:
```python
get_body_json({"message": "hello", "id": 1})
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
            const browser_platform = `${navigator.platform || "unknown"}`;
            const screen_width = window.screen.width || "unknown";
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
            };
            [new URLSearchParams(params).toString(), unix]
        """)
        auth_result.path_and_query = f"{API_PATH}?{auth_result.path_and_query}"
    return callback
```

**Назначение**: Асинхронная функция для получения callback из браузера.

**Параметры**:
- `auth_result` (CallbackResults): Объект `CallbackResults` для хранения результатов.

**Возвращает**:
- `callback`: Асинхронная функция обратного вызова, которая принимает объект `page` (вкладку браузера) в качестве аргумента.

**Как работает функция**:
1. Определяет внутреннюю асинхронную функцию `callback`, которая принимает объект `page` (вкладку браузера) в качестве аргумента.
2. В цикле ожидает, пока не будет получен токен авторизации из `localStorage` браузера.
3. После получения токена извлекает параметры устройства и браузера из `localStorage` и `navigator` объекта браузера.
4. Формирует строку запроса с параметрами.
5. Обновляет `path_and_query` в объекте `auth_result`.
6. Возвращает функцию `callback`.

**Внутренние функции**:

### `callback`

```python
async def callback(page: Tab):
    """
    Асинхронная функция обратного вызова, выполняемая в браузере для получения токена и параметров запроса.
    """
    ...
```

**Назначение**: Асинхронная функция обратного вызова, выполняемая в браузере для получения токена и параметров запроса.

**Параметры**:
- `page` (Tab): Объект, представляющий вкладку браузера.

**Как работает функция**:
1. В цикле ожидает, пока не будет получен токен авторизации из `localStorage` браузера.
2. После получения токена извлекает параметры устройства и браузера из `localStorage` и `navigator` объекта браузера.
3. Формирует строку запроса с параметрами.
4. Обновляет `path_and_query` в объекте `auth_result`.

```
Объект page (вкладка браузера)
     ↓
Ожидание получения токена из localStorage
     ↓
Извлечение параметров устройства и браузера
     ↓
Формирование строки запроса с параметрами
     ↓
Обновление path_and_query в объекте auth_result
```

**Примеры**:
```python
auth_result = CallbackResults()
callback_func = await get_browser_callback(auth_result)
# callback_func(page)  # Вызов функции callback с объектом page