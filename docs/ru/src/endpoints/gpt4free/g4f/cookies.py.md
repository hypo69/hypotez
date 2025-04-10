# Модуль для работы с cookies
============================

Модуль предоставляет функциональность для загрузки, хранения и управления cookies из различных источников, включая браузеры и файлы (HAR и JSON).

## Обзор

Модуль предназначен для автоматической загрузки и управления cookies, что может быть полезно для автоматизации задач, требующих аутентификации в веб-приложениях. Он поддерживает загрузку cookies из различных браузеров и файлов, а также предоставляет функции для установки и получения директории, где хранятся файлы cookie.

## Подробнее

Модуль состоит из нескольких функций и класса `CookiesConfig`, который содержит конфигурацию для работы с cookies. Основная функциональность включает в себя загрузку cookies из браузеров, чтение файлов cookie и управление директорией, где хранятся файлы cookie.

## Классы

### `CookiesConfig`

**Описание**: Класс, содержащий конфигурацию для работы с cookies.

**Атрибуты**:
- `cookies` (Dict[str, Cookies]): Словарь, где ключи - это доменные имена, а значения - словари cookie для этих доменов.
- `cookies_dir` (str): Путь к директории, где хранятся файлы cookie. По умолчанию "./har_and_cookies".

### Функции

### `g4f`

```python
def g4f(domain_name: str) -> list:
    """
    Загружает cookies из браузера 'g4f' (если он существует).

    Args:
        domain_name (str): Домен, для которого загружаются cookies.

    Returns:
        list: Список cookies.
    """
    ...
```

**Назначение**: Загружает cookies из специального браузера `g4f`, если он установлен и настроен.

**Параметры**:
- `domain_name` (str): Доменное имя, для которого требуется получить cookies.

**Возвращает**:
- `list`: Список найденных cookies.

**Как работает функция**:
1. Проверяет наличие установленной библиотеки `platformdirs`. Если библиотека отсутствует, возвращается пустой список.
2. Определяет директорию пользовательской конфигурации для `g4f` с использованием `platformdirs.user_config_dir`.
3. Формирует путь к файлу cookies (`Cookies`) внутри директории `Default`.
4. Если файл cookies существует, загружает cookies с помощью функции `chrome` из библиотеки `browser_cookie3` и возвращает их.
5. Если файл cookies не существует или библиотека `platformdirs` не установлена, возвращается пустой список.

**Примеры**:

```python
cookies = g4f(".google.com")
if cookies:
    print(f"Cookies найдены: {cookies}")
else:
    print("Cookies не найдены.")
```

### `get_cookies`

```python
def get_cookies(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False, cache_result: bool = True) -> Dict[str, str]:
    """
    Загружает cookies для заданного домена из всех поддерживаемых браузеров и кэширует результаты.

    Args:
        domain_name (str): Домен, для которого загружаются cookies.
        raise_requirements_error (bool, optional): Если `True`, вызывает исключение `MissingRequirementsError`, если не установлен `browser_cookie3`. По умолчанию `True`.
        single_browser (bool, optional): Если `True`, останавливает поиск cookies после первого успешного обнаружения. По умолчанию `False`.
        cache_result (bool, optional): Если `True`, кэширует результаты загрузки cookies для данного домена. По умолчанию `True`.

    Returns:
        Dict[str, str]: Словарь cookie, где ключи - имена cookie, а значения - их значения.
    """
    ...
```

**Назначение**: Загружает cookies для указанного домена из поддерживаемых браузеров, кэширует результаты для последующего использования.

**Параметры**:
- `domain_name` (str): Доменное имя, для которого требуется получить cookies.
- `raise_requirements_error` (bool): Флаг, указывающий, следует ли вызывать исключение, если не установлены необходимые библиотеки.
- `single_browser` (bool): Флаг, указывающий, следует ли останавливать поиск cookies после первого успешного обнаружения.
- `cache_result` (bool): Флаг, указывающий, следует ли кэшировать результат.

**Возвращает**:
- `Dict[str, str]`: Словарь, содержащий имена и значения cookies.

**Как работает функция**:

1.  **Проверка кэша**: Сначала проверяет, есть ли cookies для данного домена в кэше (`CookiesConfig.cookies`). Если есть и `cache_result` установлен в `True`, функция возвращает кэшированные cookies.
2.  **Загрузка cookies из браузеров**: Если в кэше cookies нет, функция вызывает `load_cookies_from_browsers` для загрузки cookies из различных браузеров.
3.  **Кэширование результата**: Если `cache_result` установлен в `True`, загруженные cookies сохраняются в кэше (`CookiesConfig.cookies`) для последующего использования.
4.  **Возврат cookies**: Функция возвращает словарь с именами и значениями cookies.

**Примеры**:

```python
cookies = get_cookies(".google.com")
if cookies:
    print(f"Cookies найдены: {cookies}")
else:
    print("Cookies не найдены.")
```

### `set_cookies`

```python
def set_cookies(domain_name: str, cookies: Cookies = None) -> None:
    """
    Устанавливает cookies для заданного домена.

    Args:
        domain_name (str): Домен, для которого устанавливаются cookies.
        cookies (Cookies, optional): Словарь cookies, который необходимо установить. Если `None`, удаляет cookies для данного домена. По умолчанию `None`.
    """
    ...
```

**Назначение**: Устанавливает или удаляет cookies для указанного домена в кэше.

**Параметры**:
- `domain_name` (str): Доменное имя, для которого устанавливаются cookies.
- `cookies` (Cookies): Словарь с cookies, которые нужно установить для домена.

**Как работает функция**:

1.  **Установка cookies**: Если передан словарь `cookies`, он сохраняется в `CookiesConfig.cookies` для указанного домена.
2.  **Удаление cookies**: Если `cookies` равен `None`, функция пытается удалить cookies для указанного домена из `CookiesConfig.cookies`.

**Примеры**:

```python
# Установка cookies
cookies = {"cookie1": "value1", "cookie2": "value2"}
set_cookies(".example.com", cookies)

# Удаление cookies
set_cookies(".example.com", None)
```

### `load_cookies_from_browsers`

```python
def load_cookies_from_browsers(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False) -> Cookies:
    """
    Вспомогательная функция для загрузки cookies из различных браузеров.

    Args:
        domain_name (str): Домен, для которого загружаются cookies.
        raise_requirements_error (bool, optional): Если `True`, вызывает исключение `MissingRequirementsError`, если не установлен `browser_cookie3`. По умолчанию `True`.
        single_browser (bool, optional): Если `True`, останавливает поиск cookies после первого успешного обнаружения. По умолчанию `False`.

    Returns:
        Dict[str, str]: Словарь cookie, где ключи - имена cookie, а значения - их значения.
    """
    ...
```

**Назначение**: Загружает cookies из различных установленных браузеров для указанного домена.

**Параметры**:
- `domain_name` (str): Доменное имя, для которого требуется получить cookies.
- `raise_requirements_error` (bool): Флаг, указывающий, следует ли вызывать исключение, если не установлены необходимые библиотеки.
- `single_browser` (bool): Флаг, указывающий, следует ли останавливать поиск cookies после первого успешного обнаружения.

**Возвращает**:
- `Dict[str, str]`: Словарь, содержащий имена и значения cookies.

**Как работает функция**:

1.  **Проверка наличия `browser_cookie3`**: Проверяет, установлена ли библиотека `browser_cookie3`. Если нет и `raise_requirements_error` установлен в `True`, вызывает исключение `MissingRequirementsError`.
2.  **Перебор браузеров**: Перебирает список браузеров (`browsers`) и пытается загрузить cookies для каждого браузера.
3.  **Загрузка cookies из браузера**: Для каждого браузера вызывается соответствующая функция (например, `chrome`, `firefox`).
4.  **Обработка ошибок**: Обрабатывает исключения `BrowserCookieError` и другие исключения, которые могут возникнуть при чтении cookies из браузера.
5.  **Сохранение cookies**: Сохраняет cookies в словарь `cookies`, исключая cookies с истекшим сроком действия.
6.  **Остановка после первого браузера**: Если `single_browser` установлен в `True` и cookies были успешно загружены, останавливает перебор браузеров.

**Примеры**:

```python
cookies = load_cookies_from_browsers(".google.com")
if cookies:
    print(f"Cookies найдены: {cookies}")
else:
    print("Cookies не найдены.")
```

### `set_cookies_dir`

```python
def set_cookies_dir(dir: str) -> None:
    """
    Устанавливает директорию для хранения файлов cookie.

    Args:
        dir (str): Путь к директории, где будут храниться файлы cookie.
    """
    ...
```

**Назначение**: Устанавливает директорию, в которой будут храниться файлы cookie.

**Параметры**:
- `dir` (str): Путь к директории.

**Как работает функция**:
Просто устанавливает значение атрибута `cookies_dir` класса `CookiesConfig` на переданное значение `dir`.

**Примеры**:

```python
set_cookies_dir("./my_cookies")
```

### `get_cookies_dir`

```python
def get_cookies_dir() -> str:
    """
    Возвращает директорию для хранения файлов cookie.

    Returns:
        str: Путь к директории, где хранятся файлы cookie.
    """
    ...
```

**Назначение**: Возвращает путь к директории, в которой хранятся файлы cookie.

**Возвращает**:
- `str`: Путь к директории.

**Как работает функция**:
Функция возвращает значение атрибута `CookiesConfig.cookies_dir`.

**Примеры**:

```python
cookies_dir = get_cookies_dir()
print(f"Директория для cookies: {cookies_dir}")
```

### `read_cookie_files`

```python
def read_cookie_files(dirPath: str = None):
    """
    Читает файлы cookie из указанной директории (HAR и JSON).

    Args:
        dirPath (str, optional): Путь к директории, из которой нужно читать файлы cookie. Если `None`, используется `CookiesConfig.cookies_dir`. По умолчанию `None`.
    """
    ...
```

**Назначение**: Читает файлы cookie из указанной директории, поддерживая форматы HAR и JSON.

**Параметры**:
- `dirPath` (str, optional): Путь к директории с файлами cookie. Если не указан, используется значение по умолчанию из `CookiesConfig.cookies_dir`.

**Как работает функция**:

1.  **Определение директории**: Если `dirPath` не указан, используется значение `CookiesConfig.cookies_dir`.
2.  **Проверка доступа к директории**: Проверяет, доступна ли директория для чтения. Если нет, выводит сообщение в лог и завершает работу.
3.  **Поиск файлов**: Выполняет обход директории и ищет файлы с расширениями ".har" и ".json".
4.  **Чтение HAR-файлов**: Для каждого HAR-файла пытается прочитать его содержимое как JSON. Извлекает cookies из записей HAR-файла и сохраняет их в `CookiesConfig.cookies`.
5.  **Чтение JSON-файлов**: Для каждого JSON-файла пытается прочитать его содержимое как JSON. Извлекает cookies из JSON-файла и сохраняет их в `CookiesConfig.cookies`.

**Примеры**:

```python
read_cookie_files("./my_cookies")
```

ASCII Flowchart для `read_cookie_files`:

```
    Определение директории → Проверка доступа к директории
        ↓                      ↓
    Поиск файлов             Директория недоступна?
        ↓                      ↓
    Обход файлов             (Вывод в лог) → Конец
        ↓
    Файл .har? → Чтение HAR-файла → Извлечение cookies
        ↓                                   ↓
        Нет                             Сохранение cookies
        ↓                                   ↓
    Файл .json? → Чтение JSON-файла → Извлечение cookies
        ↓                                   ↓
        Нет                             Сохранение cookies
        ↓
    Конец
```

## Константы

### `DOMAINS`

Список доменных имен, используемых для поиска cookies.

```python
DOMAINS = [
    ".bing.com",
    ".meta.ai",
    ".google.com",
    "www.whiterabbitneo.com",
    "huggingface.co",
    "chat.reka.ai",
    "chatgpt.com",
    ".cerebras.ai",
    "github.com",
    "huggingface.co",
    ".huggingface.co"
]