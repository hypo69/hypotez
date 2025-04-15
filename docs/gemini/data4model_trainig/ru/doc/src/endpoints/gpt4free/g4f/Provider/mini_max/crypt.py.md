# Модуль для криптографических функций mini_max

## Обзор

Модуль `crypt.py` содержит функции, используемые для криптографических операций и генерации заголовков, необходимых для взаимодействия с API mini_max. Он включает функции для хэширования строк, генерации специальных заголовков и подготовки данных для запросов.

## Подробней

Этот модуль предоставляет инструменты для обеспечения безопасности и правильной аутентификации при работе с API mini_max. Он используется для создания уникальных идентификаторов и заголовков, которые необходимы для подтверждения подлинности запросов.

## Классы

### `CallbackResults`

**Описание**: Класс для хранения результатов обратного вызова браузера, включая токен, путь запроса с параметрами и временную метку.

**Наследует**:
- `JsonMixin`: Добавляет функциональность для работы с JSON.

**Атрибуты**:
- `token` (str): Токен аутентификации.
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

**Назначение**: Функция `hash_function` генерирует MD5-хеш строки.

**Параметры**:
- `base_string` (str): Строка для хеширования.

**Возвращает**:
- `str`: MD5-хеш строки в шестнадцатеричном формате.

**Как работает функция**:
- Преобразует входную строку в байты, используя кодировку UTF-8.
- Вычисляет MD5-хеш полученных байтов.
- Возвращает хеш в виде строки шестнадцатеричных цифр.

**Примеры**:
```python
>>> hash_function("test_string")
'd8e8fca2dc0f896fd7cb4cb0031ba249'
```

### `generate_yy_header`

```python
def generate_yy_header(has_search_params_path: str, body_to_yy: dict, time: int) -> str:
    """
    Python equivalent of the generateYYHeader function.
    """
    ...
```

**Назначение**: Функция `generate_yy_header` генерирует специальный заголовок YY, используемый для аутентификации запросов.

**Параметры**:
- `has_search_params_path` (str): Путь запроса с параметрами поиска.
- `body_to_yy` (dict): Тело запроса, преобразованное функцией `get_body_to_yy`.
- `time` (int): Временная метка.

**Возвращает**:
- `str`: Сгенерированный заголовок YY.

**Как работает функция**:
- Кодирует путь запроса с параметрами поиска с использованием `urllib.parse.quote`.
- Вычисляет хеш временной метки с помощью `hash_function`.
- Объединяет закодированный путь, тело запроса и хеш временной метки в одну строку.
- Вычисляет хеш полученной строки и возвращает его.

**Примеры**:
```python
>>> generate_yy_header("/v4/api/chat/msg?param1=value1", "body_hash", 1678886400)
'd41d8cd98f00b204e9800998ecf8427e'
```

### `get_body_to_yy`

```python
def get_body_to_yy(l):
    ...
```

**Назначение**: Функция `get_body_to_yy` преобразует тело запроса в формат, необходимый для генерации заголовка YY.

**Параметры**:
- `l` (dict): Словарь, содержащий данные тела запроса, такие как `msgContent`, `characterID` и `chatID`.

**Возвращает**:
- `str`: Преобразованное тело запроса.

**Как работает функция**:
- Очищает содержимое сообщения (`msgContent`) от символов новой строки и возврата каретки.
- Вычисляет хеши `characterID`, очищенного `msgContent` и `chatID`.
- Объединяет полученные хеши в одну строку и возвращает её.

**Примеры**:
```python
>>> get_body_to_yy({"msgContent": "test message", "characterID": "char123", "chatID": "chat456"})
'...'
```

### `get_body_json`

```python
def get_body_json(s):
    return json.dumps(s, ensure_ascii=True, sort_keys=True)
```

**Назначение**: Функция `get_body_json` преобразует входной словарь в JSON-строку.

**Параметры**:
- `s` (dict): Словарь, который необходимо преобразовать в JSON.

**Возвращает**:
- `str`: JSON-представление входного словаря.

**Как работает функция**:
- Использует `json.dumps` для преобразования словаря в JSON-строку.
- Устанавливает `ensure_ascii=True`, чтобы гарантировать, что все символы будут представлены в виде ASCII-кодов.
- Устанавливает `sort_keys=True`, чтобы ключи в JSON-строке были отсортированы.

**Примеры**:
```python
>>> get_body_json({"key1": "value1", "key2": "value2"})
'{"key1": "value1", "key2": "value2"}'
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
            const params = {\n                device_platform: "web",\n                biz_id: 2,\n                app_id: 3001,\n                version_code: 22201,\n                lang: "en",\n                uuid,\n                device_id,\n                os_name,\n                browser_name,\n                cpu_core_num,\n                browser_language,\n                browser_platform,\n                screen_width,\n                screen_height,\n                unix\n            };\n            [new URLSearchParams(params).toString(), unix]\n        """)\n        auth_result.path_and_query = f"{API_PATH}?{auth_result.path_and_query}"\n    return callback
```

**Назначение**: Функция `get_browser_callback` создает обратный вызов для получения токена аутентификации и параметров запроса из браузера.

**Параметры**:
- `auth_result` (CallbackResults): Объект `CallbackResults` для хранения результатов аутентификации.

**Возвращает**:
- `callback` (Callable): Асинхронная функция обратного вызова, которая принимает объект `page` (вкладку браузера) и извлекает данные.

**Как работает функция**:
- Определяет внутреннюю асинхронную функцию `callback`, которая выполняет следующие действия:
  - Ожидает, пока в локальном хранилище браузера не появится токен (`_token`).
  - Извлекает значения `device_id`, `uuid`, `os_name`, `browser_name`, `cpu_core_num`, `browser_language`, `browser_platform`, `screen_width`, `screen_height` из браузера и формирует параметры запроса.
  - Получает текущую временную метку Unix в миллисекундах.
  - Формирует строку запроса с параметрами и сохраняет ее в `auth_result.path_and_query`.
  - Сохраняет временную метку в `auth_result.timestamp`.

**Внутренние функции**:

### `callback`

```python
async def callback(page: Tab):
    ...
```

**Назначение**: Асинхронная функция обратного вызова, извлекающая токен аутентификации и параметры запроса из браузера.

**Параметры**:
- `page` (Tab): Объект, представляющий вкладку браузера.

**Как работает функция**:
- Ожидает, пока в локальном хранилище браузера не появится токен (`_token`).
- Извлекает значения `device_id`, `uuid`, `os_name`, `browser_name`, `cpu_core_num`, `browser_language`, `browser_platform`, `screen_width`, `screen_height` из браузера и формирует параметры запроса.
- Получает текущую временную метку Unix в миллисекундах.
- Формирует строку запроса с параметрами и сохраняет ее в `auth_result.path_and_query`.
- Сохраняет временную метку в `auth_result.timestamp`.

**Примеры**:
```python
# Пример использования функции get_browser_callback
auth_result = CallbackResults()
callback_function = get_browser_callback(auth_result)

# Вызов callback_function с объектом page (пример):
# await callback_function(page)
# После выполнения:
# auth_result.token будет содержать токен
# auth_result.path_and_query будет содержать путь запроса с параметрами
# auth_result.timestamp будет содержать временную метку