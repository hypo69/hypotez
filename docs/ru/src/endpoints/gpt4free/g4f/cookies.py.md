# Модуль для работы с cookies

## Обзор

Модуль `cookies.py` предназначен для загрузки и управления cookies для различных доменов из поддерживаемых браузеров и HAR/JSON файлов. Он предоставляет функциональность для получения, установки и хранения cookies, а также для работы с cookies, сохраненными в файлах.

## Подробнее

Этот модуль используется для автоматического получения cookies из различных источников (браузеры, файлы) для использования в последующих запросах к веб-сайтам. Это позволяет имитировать поведение пользователя и получать доступ к контенту, требующему аутентификации или сохранения состояния сессии.

## Классы

### `CookiesConfig`

**Описание**: Класс конфигурации для хранения cookies и директории с файлами cookies.

**Атрибуты**:
- `cookies` (Dict[str, Cookies]): Словарь, содержащий cookies для каждого домена.
- `cookies_dir` (str): Путь к директории, где хранятся HAR и JSON файлы с cookies. По умолчанию "./har_and_cookies".

**Принцип работы**:
Класс `CookiesConfig` используется для хранения глобальных настроек, связанных с cookies. Он содержит словарь `cookies`, где ключами являются доменные имена, а значениями - словари с именами и значениями cookies. Также класс хранит путь к директории, в которой могут находиться файлы с cookies в формате HAR или JSON.

## Функции

### `g4f(domain_name: str) -> list`

**Назначение**: Загружает cookies из браузера "g4f" (если он существует).

**Параметры**:
- `domain_name` (str): Домен, для которого загружаются cookies.

**Возвращает**:
- `list`: Список cookies.

**Как работает функция**:
Функция проверяет наличие установленной библиотеки `platformdirs`. Если она установлена, функция пытается найти файл с cookies браузера "g4f" в директории конфигурации пользователя и загрузить cookies для указанного домена. Если файл не существует или библиотека `platformdirs` не установлена, возвращается пустой список.

### `get_cookies(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False, cache_result: bool = True) -> Dict[str, str]`

**Назначение**: Загружает cookies для заданного домена из всех поддерживаемых браузеров и кэширует результаты.

**Параметры**:
- `domain_name` (str): Домен, для которого загружаются cookies.
- `raise_requirements_error` (bool, optional): Если `True`, вызывает исключение `MissingRequirementsError`, если не установлен пакет `browser_cookie3`. По умолчанию `True`.
- `single_browser` (bool, optional): Если `True`, загружает cookies только из первого найденного браузера. По умолчанию `False`.
- `cache_result` (bool, optional): Если `True`, кэширует результаты загрузки cookies. По умолчанию `True`.

**Возвращает**:
- `Dict[str, str]`: Словарь, содержащий имена и значения cookies.

**Как работает функция**:
Функция сначала проверяет, есть ли cookies для данного домена в кэше (`CookiesConfig.cookies`). Если есть и `cache_result` равен `True`, функция возвращает cookies из кэша. В противном случае функция вызывает `load_cookies_from_browsers` для загрузки cookies из браузеров, кэширует результат (если `cache_result` равен `True`) и возвращает загруженные cookies.

### `set_cookies(domain_name: str, cookies: Cookies = None) -> None`

**Назначение**: Устанавливает cookies для заданного домена.

**Параметры**:
- `domain_name` (str): Домен, для которого устанавливаются cookies.
- `cookies` (Cookies, optional): Словарь с cookies для установки. Если `None`, cookies для данного домена удаляются из кэша. По умолчанию `None`.

**Как работает функция**:
Если передан словарь `cookies`, функция сохраняет его в кэше (`CookiesConfig.cookies`) для указанного домена. Если `cookies` равен `None`, функция удаляет cookies для данного домена из кэша, если они там есть.

### `load_cookies_from_browsers(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False) -> Cookies`

**Назначение**: Загружает cookies из различных браузеров.

**Параметры**:
- `domain_name` (str): Домен, для которого загружаются cookies.
- `raise_requirements_error` (bool, optional): Если `True`, вызывает исключение `MissingRequirementsError`, если не установлен пакет `browser_cookie3`. По умолчанию `True`.
- `single_browser` (bool, optional): Если `True`, загружает cookies только из первого найденного браузера. По умолчанию `False`.

**Возвращает**:
- `Dict[str, str]`: Словарь, содержащий имена и значения cookies.

**Как работает функция**:
Функция проверяет, установлен ли пакет `browser_cookie3`. Если нет и `raise_requirements_error` равен `True`, вызывается исключение `MissingRequirementsError`. Затем функция перебирает список поддерживаемых браузеров (`browsers`) и пытается загрузить cookies для указанного домена из каждого браузера. Если загрузка cookies прошла успешно, функция добавляет их в общий словарь `cookies`. Если `single_browser` равен `True`, функция прекращает перебор браузеров после первого успешного получения cookies.

Внутренняя логика:
- Проверка наличия библиотеки `browser_cookie3`.
- Итерация по списку браузеров.
- Для каждого браузера:
    - Попытка получить cookie jar.
    - Если cookie jar получен, итерация по всем cookies в cookie jar.
    - Добавление cookie в результирующий словарь `cookies`, если его там еще нет и срок его действия не истек.
    - Если `single_browser` равен `True`, выход из цикла после первого успешного получения cookies.
- Возврат словаря `cookies`.

### `set_cookies_dir(dir: str) -> None`

**Назначение**: Устанавливает директорию для хранения файлов cookies.

**Параметры**:
- `dir` (str): Путь к директории.

**Как работает функция**:
Функция устанавливает значение атрибута `cookies_dir` класса `CookiesConfig` равным переданному значению `dir`.

### `get_cookies_dir() -> str`

**Назначение**: Возвращает директорию для хранения файлов cookies.

**Возвращает**:
- `str`: Путь к директории.

**Как работает функция**:
Функция возвращает значение атрибута `cookies_dir` класса `CookiesConfig`.

### `read_cookie_files(dirPath: str = None)`

**Назначение**: Читает файлы cookies из указанной директории.

**Параметры**:
- `dirPath` (str, optional): Путь к директории с файлами cookies. Если не указан, используется значение из `CookiesConfig.cookies_dir`.

**Как работает функция**:
Функция читает HAR и JSON файлы из указанной директории и загружает cookies в `CookiesConfig.cookies`. Сначала проверяется доступность директории для чтения. Затем функция ищет файлы с расширениями ".har" и ".json". HAR файлы обрабатываются путем извлечения домена и cookies из записей лога. JSON файлы обрабатываются как списки объектов cookie, где каждый объект содержит информацию о домене и значениях cookie.

Внутренние функции:

    get_domain(v: dict) -> str:
        """
        Извлекает домен из записи HAR файла.

        Args:
            v (dict): Запись из HAR файла.

        Returns:
            str: Доменное имя или None, если домен не найден.
        """
        # Функция извлекает значение host из заголовков запроса в записи HAR файла.
        # Она ищет заголовки с именами "host" или ":authority" (для HTTP/2).
        # Если заголовок найден, функция извлекает его значение.
        # Затем, функция проверяет, содержит ли значение заголовка один из известных доменов (DOMAINS).
        # Если домен найден, функция возвращает его.
        # Если заголовок не найден или домен не найден, функция возвращает None.

## Параметры класса

- `cookies` (Dict[str, Cookies]): Более подробное описание словаря, содержащего cookies для каждого домена.
- `cookies_dir` (str): Более подробное описание пути к директории, где хранятся HAR и JSON файлы с cookies. По умолчанию "./har_and_cookies".

## Примеры

```python
# Пример использования get_cookies
cookies = get_cookies(".google.com")
print(cookies)

# Пример использования set_cookies
set_cookies(".google.com", {"test_cookie": "test_value"})

# Пример использования get_cookies_dir и set_cookies_dir
set_cookies_dir("./custom_cookies")
print(get_cookies_dir())  # Выведет: ./custom_cookies

# Пример использования read_cookie_files
read_cookie_files("./har_and_cookies")
```