# Модуль для управления куки

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/g4f/cookies.py` предназначен для управления куки, используемыми в проекте.

## Подробней

Модуль предоставляет функции для загрузки куки из различных браузеров и файлов HAR.

## Переменные

*   `browsers` (list): Список функций для получения куки из разных браузеров.
*   `DOMAINS` (list): Список доменов, для которых загружаются куки.

## Классы

### `CookiesConfig`

**Описание**: Класс для хранения конфигурации куки.

**Атрибуты**:

*   `cookies` (Dict[str, Cookies]): Словарь, содержащий куки для разных доменов.
*   `cookies_dir` (str): Путь к директории с файлами куки.

## Функции

### `get_cookies`

```python
def get_cookies(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False, cache_result: bool = True) -> Dict[str, str]:
```

**Назначение**: Загружает куки для указанного домена из различных браузеров и кэширует результаты.

**Параметры**:

*   `domain_name` (str): Домен, для которого нужно получить куки.
*   `raise_requirements_error` (bool, optional): Вызывать ли исключение при отсутствии `browser_cookie3`. Defaults to `True`.
*   `single_browser` (bool, optional): Получать ли куки только из одного браузера. Defaults to `False`.
*   `cache_result` (bool, optional): Кэшировать ли результаты. Defaults to `True`.

**Возвращает**:

*   `Dict[str, str]`: Словарь, содержащий куки.

**Как работает функция**:

1.  Проверяет, есть ли куки для указанного домена в кэше.
2.  Если куки есть в кэше и `cache_result` равен `True`, возвращает куки из кэша.
3.  Загружает куки из браузеров, используя функцию `load_cookies_from_browsers`.
4.  Кэширует куки (если `cache_result` равен `True`).
5.  Возвращает словарь с куками.

### `set_cookies`

```python
def set_cookies(domain_name: str, cookies: Cookies = None) -> None:
```

**Назначение**: Устанавливает куки для указанного домена.

**Параметры**:

*   `domain_name` (str): Домен, для которого нужно установить куки.
*   `cookies` (Cookies, optional): Словарь с куками. Defaults to `None`.

**Как работает функция**:

1.  Если `cookies` указаны, сохраняет их в кэше.
2.  Иначе удаляет куки для указанного домена из кэша.

### `load_cookies_from_browsers`

```python
def load_cookies_from_browsers(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False) -> Cookies:
```

**Назначение**: Загружает куки для указанного домена из различных браузеров.

**Параметры**:

*   `domain_name` (str): Домен, для которого нужно получить куки.
*   `raise_requirements_error` (bool, optional): Вызывать ли исключение при отсутствии `browser_cookie3`. Defaults to `True`.
*   `single_browser` (bool, optional): Получать ли куки только из одного браузера. Defaults to `False`.

**Возвращает**:

*   `Dict[str, str]`: Словарь, содержащий куки.

**Как работает функция**:

1.  Проверяет, установлен ли пакет `browser_cookie3`. Если нет, вызывает исключение (если `raise_requirements_error` равен `True`).
2.  Итерируется по списку браузеров `browsers`.
3.  Для каждого браузера:

    *   Пытается получить куки для указанного домена, используя функцию браузера.
    *   Добавляет куки в словарь `cookies`.
    *   Если `single_browser` равен `True`, останавливает итерацию после первого успешного получения куки.
4.  Возвращает словарь с куками.

### `set_cookies_dir`

```python
def set_cookies_dir(dir: str) -> None:
```

**Назначение**: Устанавливает директорию для файлов куки.

**Параметры**:

*   `dir` (str): Путь к директории.

**Как работает функция**:

1.  Устанавливает значение атрибута `cookies_dir` класса `CookiesConfig`.

### `get_cookies_dir`

```python
def get_cookies_dir() -> str:
```

**Назначение**: Возвращает директорию для файлов куки.

**Возвращает**:

*   `str`: Путь к директории.

**Как работает функция**:

1.  Возвращает значение атрибута `cookies_dir` класса `CookiesConfig`.

### `read_cookie_files`

```python
def read_cookie_files(dirPath: str = None):
```

**Назначение**: Читает файлы куки (HAR и JSON) из указанной директории.

**Параметры**:

*   `dirPath` (str, optional): Путь к директории с файлами куки. Defaults to `None`.

**Как работает функция**:

1.  Устанавливает путь к директории, используя `CookiesConfig.cookies_dir`, если `dirPath` не указан.
2.  Проверяет, доступна ли директория для чтения.
3.  Итерируется по файлам в директории и добавляет файлы с расширениями `.har` и `.json` в соответствующие списки.
4.  Загружает куки из файлов HAR и JSON и сохраняет их в `CookiesConfig.cookies`.