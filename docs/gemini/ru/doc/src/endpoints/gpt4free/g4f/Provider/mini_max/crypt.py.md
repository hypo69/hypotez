# Модуль crypt.py
## Обзор

Модуль `crypt.py` предназначен для реализации криптографических функций, используемых в запросах к API mini_max. Он включает в себя функции для хеширования, генерации заголовков и подготовки тела запроса.
Модуль является частью подпроекта g4f (gpt4free), который, вероятно, предназначен для обхода ограничений GPT-4 и других языковых моделей.
В частности, этот модуль создает необходимые хедеры и параметры для обхода защиты mini_max.

## Подробнее

Модуль содержит функции для имитации криптографических операций, используемых mini_max API, включая генерацию хешей, заголовков и тел запросов. Он также включает асинхронную функцию для получения callback из браузера.

## Функции

### `hash_function`

```python
def hash_function(base_string: str) -> str:
    """
    Mimics the hashFunction using MD5.
    """
```

**Назначение**: Имитирует функцию хеширования с использованием алгоритма MD5.

**Параметры**:
- `base_string` (str): Строка, которую необходимо хешировать.

**Возвращает**:
- `str`: MD5 хеш строки в шестнадцатеричном формате.

**Как работает функция**:
- Кодирует входную строку в байты.
- Вычисляет MD5 хеш закодированной строки.
- Возвращает хеш в виде шестнадцатеричной строки.

**Примеры**:

```python
>>> hash_function("example")
'5eb63bbbe01eeed093cb22bb5dbdcfe3'
```

### `generate_yy_header`

```python
def generate_yy_header(has_search_params_path: str, body_to_yy: dict, time: int) -> str:
    """
    Python equivalent of the generateYYHeader function.
    """
```

**Назначение**: Генерирует заголовок `yy` на основе пути с параметрами поиска, тела запроса и временной метки.

**Параметры**:
- `has_search_params_path` (str): Путь с параметрами поиска.
- `body_to_yy` (dict): Тело запроса, преобразованное в строку.
- `time` (int): Временная метка.

**Возвращает**:
- `str`: Сгенерированный заголовок `yy`.

**Как работает функция**:
- Кодирует путь с параметрами поиска с помощью `urllib.parse.quote`.
- Вычисляет хеш временной метки.
- Объединяет закодированный путь, тело запроса и хеш временной метки в одну строку.
- Вычисляет хеш объединенной строки.
- Возвращает полученный хеш.

**Примеры**:

```python
>>> generate_yy_header("/api/chat", "body", 1678886400)
'e5a9254ca990271212ba8c594142539a'
```

### `get_body_to_yy`

```python
def get_body_to_yy(l: dict) -> str:
    L = l["msgContent"].replace("\\r\\n", "").replace("\\n", "").replace("\\r", "")
    M = hash_function(l["characterID"]) + hash_function(L) + hash_function(l["chatID"])
    M += hash_function("")  # Mimics hashFunction(undefined) in JS

    # print("bodyToYY:", M)
    return M
```

**Назначение**: Формирует тело запроса для `yy` на основе содержимого сообщения, идентификатора персонажа и идентификатора чата.

**Параметры**:
- `l` (dict): Словарь, содержащий ключи `msgContent`, `characterID` и `chatID`.

**Возвращает**:
- `str`: Сформированное тело запроса `yy`.

**Как работает функция**:
- Удаляет символы новой строки и возврата каретки из содержимого сообщения.
- Вычисляет хеши идентификатора персонажа, содержимого сообщения и идентификатора чата.
- Объединяет полученные хеши в одну строку.
- Добавляет хеш пустой строки (имитация `hashFunction(undefined)` в JavaScript).
- Возвращает объединенную строку.

**Примеры**:

```python
>>> get_body_to_yy({"msgContent": "Hello\\nWorld", "characterID": "123", "chatID": "456"})
'a9993e364706816aba3e25717850c26ca1e9f52ca1e9f52ca1e9f52cad41d8cd'
```

### `get_body_json`

```python
def get_body_json(s: dict) -> str:
    return json.dumps(s, ensure_ascii=True, sort_keys=True)
```

**Назначение**: Преобразует словарь в JSON-строку с сортировкой ключей и обеспечением ASCII-совместимости.

**Параметры**:
- `s` (dict): Словарь для преобразования.

**Возвращает**:
- `str`: JSON-строка, представляющая словарь.

**Как работает функция**:
- Использует `json.dumps` для преобразования словаря в JSON-строку.
- Устанавливает `ensure_ascii=True` для обеспечения ASCII-совместимости.
- Устанавливает `sort_keys=True` для сортировки ключей в JSON-строке.

**Примеры**:

```python
>>> get_body_json({"name": "Alice", "age": 30})
'{"age": 30, "name": "Alice"}'
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

**Назначение**: Получает callback из браузера, включая токен аутентификации, путь запроса и временную метку.

**Параметры**:
- `auth_result` (CallbackResults): Объект, в котором будут сохранены результаты аутентификации.

**Возвращает**:
- `callback` (function): Асинхронная функция callback, которая принимает объект `page: Tab` и выполняет извлечение данных из браузера.

**Как работает функция**:
- Определяет внутреннюю асинхронную функцию `callback`, которая будет выполнена в контексте браузера.
- В цикле ожидает, пока в локальном хранилище браузера не появится токен аутентификации (`_token`).
- Извлекает из локального хранилища браузера информацию об устройстве, UUID пользователя, информацию об операционной системе и браузере, количестве ядер CPU, языке браузера, платформе, разрешении экрана и текущую временную метку Unix.
- Формирует строку параметров запроса на основе извлеченных данных.
- Сохраняет путь запроса и временную метку в объекте `auth_result`.
- Возвращает функцию `callback`.

Внутренние функции:
### `callback`
``` python
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
```

**Назначение**: Асинхронная функция, предназначенная для выполнения в контексте браузера для извлечения данных, таких как токен аутентификации, параметры запроса и временная метка.

**Параметры**:

- `page`(`Tab`): Объект, представляющий вкладку браузера, используемый для выполнения JavaScript кода и взаимодействия с содержимым страницы.

**Как работает функция**:

1.  **Ожидание токена аутентификации**:
    *   Функция входит в цикл `while`, который продолжается до тех пор, пока не будет получен токен аутентификации (`auth_result.token`).
    *   Использует `await page.evaluate("localStorage.getItem('_token')")` для выполнения JavaScript кода в браузере, который пытается получить значение элемента `_token` из локального хранилища.
    *   Если токен не найден (`if not auth_result.token`), функция приостанавливает выполнение на 1 секунду с помощью `await asyncio.sleep(1)`.

2.  **Извлечение параметров запроса и временной метки**:

    *   После получения токена функция выполняет JavaScript код для извлечения различных параметров, необходимых для формирования запроса:
        *   `device_id`: Идентификатор устройства из `localStorage`.
        *   `uuid`: Уникальный идентификатор пользователя из `localStorage`.
        *   `os_name`: Название операционной системы.
        *   `browser_name`: Название браузера.
        *   `cpu_core_num`: Количество ядер CPU.
        *   `browser_language`: Язык браузера.
        *   `browser_platform`: Платформа браузера.
        *   `screen_width`: Ширина экрана.
        *   `screen_height`: Высота экрана.
        *   `unix`: Текущая временная метка Unix в миллисекундах.

    *   Формирует объект `params` со всеми извлеченными параметрами.

    *   Преобразует объект `params` в строку запроса с помощью `new URLSearchParams(params).toString()`.

    *   Возвращает массив, содержащий строку запроса и временную метку `unix`.

    *   Сохраняет полученные значения в объекте `auth_result`:

        *   `auth_result.path_and_query`: Строка запроса.
        *   `auth_result.timestamp`: Временная метка.

3.  **Формирование полного пути запроса**:

    *   Формирует полный путь запроса, объединяя `API_PATH` (константа, содержащая базовый путь к API) и строку запроса из `auth_result.path_and_query`.

    *   Сохраняет полный путь запроса в `auth_result.path_and_query`.
```

**Примеры**:

```python
# Пример использования функции get_browser_callback
auth_result = CallbackResults()
callback_function = get_browser_callback(auth_result)
# Далее callback_function передается в асинхронную функцию, которая выполняет его в браузере.
```

### `CallbackResults`

```python
class CallbackResults(JsonMixin):
    def __init__(self):
        self.token: str = None
        self.path_and_query: str = None
        self.timestamp: int = None
```

**Описание**: Класс для хранения результатов callback из браузера.

**Наследует**:

-   `JsonMixin` - добавляет функциональность преобразования объекта в JSON.

**Атрибуты**:

-   `token` (str): Токен аутентификации.
-   `path_and_query` (str): Путь запроса с параметрами.
-   `timestamp` (int): Временная метка.

**Примеры**:

```python
>>> auth_result = CallbackResults()
>>> auth_result.token = "example_token"
>>> auth_result.path_and_query = "/api/chat?param1=value1"
>>> auth_result.timestamp = 1678886400
```