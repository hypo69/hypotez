# Модуль для работы с веб-драйверами Selenium

## Обзор

Модуль предоставляет класс `Driver` для унифицированного взаимодействия с веб-драйверами Selenium, такими как Chrome, Firefox и Edge. Он упрощает задачи инициализации драйвера, навигации по URL, управления куками и обработки исключений.

## Подробнее

Основное назначение класса `Driver` — обеспечение унифицированного интерфейса для работы с веб-драйверами Selenium. Он предоставляет интерфейс для взаимодействия с веб-браузерами, такими как Chrome, Firefox и Edge. Код вебдрайверов находится в подмодулях `chrome`, `firefox`, `edge`, `playwright` . Файлы настроек для веб-браузеров находятся в: `chrome\\chrome.json`, `firefox\\firefox.json`, `edge\\edge.json`, `playwright\\playwright.json`.

## Классы

### `Driver`

**Описание**: Класс обеспечивает удобный интерфейс для работы с различными драйверами, такими как Chrome, Firefox и Edge.

**Атрибуты**:

- `driver` (selenium.webdriver): Экземпляр Selenium WebDriver.
- `current_url` (str): Текущий URL.

**Принцип работы**:

Класс `Driver` инициализируется с указанием класса веб-драйвера (например, `Chrome` или `Firefox`). Он предоставляет методы для навигации по URL, управления куками и выполнения JavaScript-кода.

**Методы**:
- `__init__(self, webdriver_cls, *args, **kwargs)`: Инициализирует экземпляр класса Driver.
- `__init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs)`: Автоматически вызывается при создании подкласса `Driver`.
- `__getattr__(self, item: str)`: Прокси для доступа к атрибутам драйвера.
- `scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3) -> bool`: Прокручивает страницу в указанном направлении.
- `locale(self) -> Optional[str]`: Определяет язык страницы на основе мета-тегов или JavaScript.
- `get_url(self, url: str) -> bool`: Переходит по указанному URL и сохраняет текущий URL, предыдущий URL и куки.
- `window_open(self, url: Optional[str] = None) -> None`: Открывает новую вкладку в текущем окне браузера и переключается на неё.
- `wait(self, delay: float = .3) -> None`: Ожидает указанное количество времени.
- `_save_cookies_localy(self) -> None`: Сохраняет текущие куки веб-драйвера в локальный файл.
- `fetch_html(self, url: Optional[str] = '') -> bool`: Извлекает HTML-контент из локального файла или веб-URL и сохраняет его.

## Методы класса

### `__init__`

```python
def __init__(self, webdriver_cls, *args, **kwargs):
    """
    Инициализирует экземпляр класса Driver.

    Args:
        webdriver_cls: Класс WebDriver, например Chrome или Firefox.
        args: Позиционные аргументы для драйвера.
        kwargs: Ключевые аргументы для драйвера.

    Raises:
        TypeError: Если `webdriver_cls` не является допустимым классом WebDriver.

    Example:
        >>> from selenium.webdriver import Chrome
        >>> driver = Driver(Chrome, executable_path='/path/to/chromedriver')
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `Driver` с указанным классом веб-драйвера и аргументами.

**Параметры**:

- `webdriver_cls`: Класс WebDriver, например `Chrome` или `Firefox`.
- `*args`: Позиционные аргументы для драйвера.
- `**kwargs`: Ключевые аргументы для драйвера.

**Вызывает исключения**:

- `TypeError`: Если `webdriver_cls` не является допустимым классом WebDriver.

**Примеры**:

```python
from selenium.webdriver import Chrome
driver = Driver(Chrome, executable_path='/path/to/chromedriver')
```

### `__init_subclass__`

```python
def __init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs):
    """
    Автоматически вызывается при создании подкласса `Driver`.

    Args:
        browser_name: Имя браузера.
        kwargs: Дополнительные аргументы.

    Raises:
        ValueError: Если browser_name не указан.
    """
    ...
```

**Назначение**: Автоматически вызывается при создании подкласса `Driver`.

**Параметры**:

- `browser_name`: Имя браузера.
- `kwargs`: Дополнительные аргументы.

**Вызывает исключения**:

- `ValueError`: Если `browser_name` не указан.

### `__getattr__`

```python
def __getattr__(self, item: str):
    """
    Прокси для доступа к атрибутам драйвера.

    Args:
        item: Имя атрибута.

    Example:
        >>> driver.current_url
    """
    ...
```

**Назначение**: Предоставляет прокси-доступ к атрибутам драйвера Selenium.

**Параметры**:

- `item`: Имя атрибута.

**Примеры**:

```python
driver.current_url
```

### `scroll`

```python
def scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3) -> bool:
    """
    Прокручивает страницу в указанном направлении.

    Args:
        scrolls: Количество прокруток, по умолчанию 1.
        frame_size: Размер прокрутки в пикселях, по умолчанию 600.
        direction: Направление ('both', 'down', 'up'), по умолчанию 'both'.
        delay: Задержка между прокрутками, по умолчанию 0.3.

    Returns:
        True, если успешно, иначе False.

    Example:
        >>> driver.scroll(scrolls=3, direction='down')
    """
    def carousel(direction: str = '', scrolls: int = 1, frame_size: int = 600, delay: float = .3) -> bool:
        """
        Локальный метод для прокрутки экрана.

        Args:
            direction: Направление ('down', 'up').
            scrolls: Количество прокруток.
            frame_size: Размер прокрутки.
            delay: Задержка между прокрутками.

        Returns:
            True, если успешно, иначе False.
        """
        try:
            for _ in range(scrolls):
                self.execute_script(f'window.scrollBy(0,{direction}{frame_size})')
                self.wait(delay)
            return True
        except Exception as ex:
            logger.error('Ошибка при прокрутке', exc_info=ex)
            return False
    ...
```

**Назначение**: Прокручивает страницу в указанном направлении на заданное количество пикселей с заданной задержкой.

**Параметры**:

- `scrolls` (int): Количество прокруток, по умолчанию 1.
- `frame_size` (int): Размер прокрутки в пикселях, по умолчанию 600.
- `direction` (str): Направление прокрутки ('both', 'down', 'up'), по умолчанию 'both'.
- `delay` (float): Задержка между прокрутками в секундах, по умолчанию 0.3.

**Возвращает**:

- `bool`: `True`, если прокрутка выполнена успешно, `False` в противном случае.

**Внутренние функции**:
- `carousel(direction: str = '', scrolls: int = 1, frame_size: int = 600, delay: float = .3) -> bool`: Локальный метод для фактической прокрутки экрана.
    - **Параметры**:
        - `direction` (str): Направление прокрутки ('down', 'up').
        - `scrolls` (int): Количество прокруток.
        - `frame_size` (int): Размер прокрутки.
        - `delay` (float): Задержка между прокрутками.
    - **Возвращает**:
        - `bool`: `True`, если прокрутка выполнена успешно, `False` в противном случае.
    - Функция выполняет JavaScript-код для прокрутки окна на заданное количество пикселей в указанном направлении.

**Как работает функция**:
- Функция `scroll` принимает параметры для управления процессом прокрутки веб-страницы. Она использует внутреннюю функцию `carousel` для выполнения фактической прокрутки. Функция `carousel` выполняет JavaScript-код для прокрутки окна на заданное количество пикселей в указанном направлении. Если указано направление 'both', функция `carousel` вызывается дважды: один раз для прокрутки вниз и один раз для прокрутки вверх.
- Функция обрабатывает возможные исключения, возникающие во время прокрутки, и регистрирует их с использованием `logger.error`.
- Функция возвращает `True`, если прокрутка выполнена успешно, и `False` в случае ошибки.

**Примеры**:

```python
driver.scroll(scrolls=3, direction='down')
```

### `locale`

```python
@property
def locale(self) -> Optional[str]:
    """
    Определяет язык страницы на основе мета-тегов или JavaScript.

    Returns:
        Код языка, если найден, иначе None.

    Example:
        >>> lang = driver.locale
        >>> print(lang)  # 'en' или None
    """
    ...
```

**Назначение**: Определяет язык страницы на основе мета-тегов или JavaScript.

**Возвращает**:

- `str | None`: Код языка, если найден, иначе `None`.

**Как работает функция**:
- Сначала пытается найти элемент `<meta>` с атрибутом `http-equiv="Content-Language"` и извлечь значение атрибута `content`.
- Если это не удается, вызывает метод `get_page_lang()` для определения языка с использованием JavaScript.
- Если ни один из этих методов не дает результата, возвращает `None`.

**Примеры**:

```python
lang = driver.locale
print(lang)  # 'en' или None
```

### `get_url`

```python
def get_url(self, url: str) -> bool:
    """
    Переходит по указанному URL и сохраняет текущий URL, предыдущий URL и куки.

    Args:
        url: URL для перехода.

    Returns:
        `True`, если переход успешен и текущий URL совпадает с ожидаемым, `False` в противном случае.

    Raises:
        WebDriverException: Если возникает ошибка с WebDriver.
        InvalidArgumentException: Если URL некорректен.
        Exception: Для любых других ошибок при переходе.
    """
    ...
```

**Назначение**: Переходит по указанному URL, сохраняет текущий URL, предыдущий URL и куки.

**Параметры**:

- `url` (str): URL для перехода.

**Возвращает**:

- `bool`: `True`, если переход успешен и текущий URL совпадает с ожидаемым, `False` в противном случае.

**Вызывает исключения**:

- `WebDriverException`: Если возникает ошибка с WebDriver.
- `InvalidArgumentException`: Если URL некорректен.
- `Exception`: Для любых других ошибок при переходе.

**Как работает функция**:
- Функция `get_url` выполняет переход по указанному URL, используя метод `self.driver.get(url)`.
- Перед переходом функция сохраняет текущий URL в переменную `_previous_url`.
- После перехода функция сохраняет куки и обновляет значения `self.current_url` и `self.previous_url`.
- Если во время перехода возникают исключения, они перехватываются, логируются с использованием `logger.error`, и функция возвращает `False`.
- В случае успешного перехода функция возвращает `True`.

### `window_open`

```python
def window_open(self, url: Optional[str] = None) -> None:
    """Open a new tab in the current browser window and switch to it.

    Args:
        url: URL to open in the new tab. Defaults to `None`.
    """
    ...
```

**Назначение**: Открывает новую вкладку в текущем окне браузера и переключается на неё.

**Параметры**:

- `url` (Optional[str]): URL для открытия в новой вкладке. По умолчанию `None`.

**Как работает функция**:
- Выполняет JavaScript-код `window.open()` для открытия новой вкладки.
- Переключается на новую вкладку, используя `self.switch_to.window(self.window_handles[-1])`.
- Если указан URL, переходит по нему, используя метод `self.get(url)`.

### `wait`

```python
def wait(self, delay: float = .3) -> None:
    """
    Ожидает указанное количество времени.

    Args:
        delay: Время задержки в секундах. По умолчанию 0.3.

    Returns:
        None
    """
    ...
```

**Назначение**: Ожидает указанное количество времени.

**Параметры**:

- `delay` (float): Время задержки в секундах. По умолчанию 0.3.

**Как работает функция**:
- Использует функцию `time.sleep(delay)` для приостановки выполнения кода на указанное количество секунд.

### `_save_cookies_localy`

```python
def _save_cookies_localy(self) -> None:
    """
    Сохраняет текущие куки веб-драйвера в локальный файл.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при сохранении куки.
    """
    ...
```

**Назначение**: Сохраняет текущие куки веб-драйвера в локальный файл.

**Как работает функция**:
- Пытается сохранить куки в файл, используя `pickle.dump`.
- Если возникает исключение, оно перехватывается и логируется.

### `fetch_html`

```python
def fetch_html(self, url: Optional[str] = '') -> bool:
    """
    Fetches HTML content from a local file or web URL and stores it.

    This method attempts to retrieve the HTML source code based on the provided
    `url`. It supports fetching from local files using the 'file://'
    protocol and from web pages using 'http://' or 'https://' protocols
    by calling the instance's `get_url` method.

    If the `url` argument is not provided, is None, or is an empty string,
    the method will attempt to use the value stored in `self.current_url`.

    Upon successful retrieval, the HTML content is stored in the instance
    variable `self.html_content`. If any error occurs during the process
    (e.g., invalid path format for files, file not found, file read error,
    network error during web fetch, unsupported URL protocol), the error
    is logged, and the method returns `False`.

    Note on File Paths:
        - The method expects file paths to be prefixed with `file://`.
        - After removing `file://`, it currently uses a regular expression
          (`[a-zA-Z]:[\\/].*`) designed to match Windows-style absolute paths
          (e.g., `C:/...` or `C:\\...`). It may not correctly handle other
          path formats (like relative paths or standard Unix paths without
          this specific check) unless they coincidentally match the regex
          after the prefix removal. Consider this limitation for cross-platform
          compatibility.

    Args:
        url (Optional[str]): The URL or local file path (prefixed with 'file://')
            from which to fetch HTML content. Supports 'file://', 'http://',
            and 'https://' protocols. If omitted, empty, or None, the value
            of `self.current_url` will be used instead. Defaults to ''.

    Returns:
        bool: `True` if the HTML content was successfully fetched from the
              specified source and stored in `self.html_content`.
              `False` if any error occurred during the fetching or reading
              process, or if the URL protocol is unsupported.

    Side Effects:
        - Sets `self.html_content` to the fetched HTML string on success.
        - May modify `self.page_source` via the `self.get_url` method call.
        - Logs errors using the configured `logger` upon failure.

    Examples:
        >>> instance = YourClassName()
        >>> instance.current_url = 'http://default.example.com'

        >>> # 1. Fetching from a web URL
        >>> success_web = instance.fetch_html('https://example.com/page')
        # Assuming get_url succeeds and sets self.page_source
        >>> print(success_web)
        True
        >>> print(instance.html_content) # doctest: +ELLIPSIS
        <html><body>Mock content for https://example.com/page</body></html>

        >>> # 2. Fetching from a local file (requires creating a dummy file)
        >>> import tempfile
        >>> import os
        >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_file:
        ...     _ = tmp_file.write("<html><body>Local Test Content</body></html>")
        ...     tmp_file_path = tmp_file.name
        >>> # Construct file URI (adjust format for OS if needed, Path.as_uri() is robust)
        >>> file_uri = Path(tmp_file_path).as_uri() # e.g., file:///tmp/xyz.html or file:///C:/Users/...\
        >>> # We need to adapt the URI slightly if the regex expects a drive letter explicitly
        >>> if os.name == 'nt':
        ...     # Reconstruct URI to match the regex C:/... if needed by implementation detail
        ...     # The current regex '[a-zA-Z]:[\\\\/].*' requires this on Windows
        ...     # Example: 'file://C:/Users/...'
        ...     match = re.match(r"file:///(?P<drive>[a-zA-Z]):/(?P<rest>.*)", file_uri)
        ...     if match:
        ...         file_uri_for_func = f"file://{match.group('drive')}:/{match.group('rest')}"
        ...     else: # Fallback if parsing fails, might not work with the function
        ...         file_uri_for_func = file_uri
        ... else: # On Unix-like systems, Path.as_uri() usually works if regex is ignored
        ...     file_uri_for_func = file_uri
        ...
        >>> # Mocking Path.exists() and open() for the example to work without the function's specific regex check
        >>> original_exists = Path.exists
        >>> original_open = open
        >>> def mock_exists(path_obj):
        ...     return str(path_obj) == tmp_file_path
        >>> def mock_open(path_obj, mode='r', encoding=None):
        ...     if str(path_obj) == tmp_file_path:
        ...         # Return a real file handle to the temp file
        ...         return original_open(tmp_file_path, mode, encoding=encoding)
        ...     else:
        ...         raise FileNotFoundError
        >>> Path.exists = mock_exists
        >>> builtins_open = __builtins__.open # Store original built-in open
        >>> __builtins__.open = mock_open # Temporarily override built-in open

        >>> # This part depends heavily on the regex implementation detail:
        >>> # Let's assume file_uri_for_func is now correctly formatted for the regex on Windows
        >>> # or that the regex check is bypassed/modified for Unix.
        >>> # Forcing a simple path string that *might* work with the regex if C: drive exists
        >>> test_uri = 'file://C:/path/to/mock/file.html' # Generic placeholder
        >>> if os.path.exists(Path(tmp_file_path)): # Ensure temp file still exists
        ...    if os.name == 'nt': # Construct path expected by regex
        ...        cleaned_path_str = tmp_file_path.replace('\\\\', '/') # Ensure forward slashes
        ...        drive = Path(tmp_file_path).drive # e.g., 'C:'
        ...        if drive:
        ...             test_uri = f"file://{drive}/{cleaned_path_str.split(':', 1)[1]}"
        ...        else: # If no drive, likely network path, won't match regex
        ...             test_uri = Path(tmp_file_path).as_uri() # Fallback
        ...    else: # Unix
        ...        test_uri = Path(tmp_file_path).as_uri() # e.g., file:///path/to/file

        >>> # Now, let's simulate the call with the constructed URI or a generic one
        >>> # NOTE: This example is complex due to mocking file system and the regex dependency
        >>> # A simplified test might just check the logic branches
        >>> print(f"Attempting to fetch: {test_uri}") # Show what URI is being used
        Attempting to fetch: ...
        >>> # success_file = instance.fetch_html(test_uri) # Actual call (mocked)
        >>> # print(success_file) # Expected: True
        >>> # print(instance.html_content) # Expected: "<html><body>Local Test Content</body></html>"
        >>> # Clean up mocks and temp file
        >>> Path.exists = original_exists
        >>> __builtins__.open = builtins_open
        >>> os.remove(tmp_file_path)
        >>> print("Skipping actual file test execution in docstring due to complexity") # Placeholder acknowledgment
        Skipping actual file test execution in docstring due to complexity

        >>> # 3. Using default URL (self.current_url)
        >>> success_default = instance.fetch_html() # url is '', use self.current_url
        >>> print(success_default)
        True
        >>> print(instance.html_content) # doctest: +ELLIPSIS
        <html><body>Mock content for http://default.example.com</body></html>

        >>> # 4. Handling a non-existent local file path
        >>> success_no_file = instance.fetch_html('file://C:/non/existent/file.html')
        >>> print(success_no_file)
        False

        >>> # 5. Handling file path with incorrect format (not matching regex)
        >>> success_bad_format = instance.fetch_html('file:///unix/style/path/without/drive/letter') # Might fail regex check
        >>> print(success_bad_format)
        False

        >>> # 6. Handling failure from get_url (e.g., 404 Not Found simulated)
        >>> success_fail_fetch = instance.fetch_html('http://example.com/notfound')
        >>> print(success_fail_fetch)
        False

        >>> # 7. Handling network error exception from get_url
        >>> success_network_error = instance.fetch_html('http://error.example.com')
        >>> print(success_network_error)
        False

        >>> # 8. Handling unsupported protocol
        >>> success_bad_protocol = instance.fetch_html('ftp://example.com/resource')
        >>> print(success_bad_protocol)
        False
    """
    ...
```

**Назначение**: Извлекает HTML-контент из локального файла или веб-URL и сохраняет его.

**Параметры**:

- `url` (Optional[str]): URL или путь к локальному файлу (с префиксом 'file://'), из которого нужно извлечь HTML-контент. Поддерживает протоколы 'file://', 'http://' и 'https://'. Если опущен, пуст или `None`, будет использовано значение `self.current_url`. По умолчанию ''.

**Возвращает**:

- `bool`: `True`, если HTML-контент был успешно извлечен из указанного источника и сохранен в `self.html_content`. `False`, если произошла какая-либо ошибка во время извлечения или чтения, или если протокол URL не поддерживается.

**Как работает функция**:

1. **Определение эффективного URL**:
   - Функция сначала определяет, какой URL использовать для извлечения HTML-контента. Если аргумент `url` передан и является строкой, то используется он. В противном случае используется значение `self.current_url`. Если ни один из них не указан, функция регистрирует ошибку и возвращает `False`.

2. **Обработка на основе протокола**:
   - **Локальные файлы (file://)**:
     - Если URL начинается с 'file://', функция удаляет этот префикс и пытается обработать оставшуюся часть как путь к файлу.
     - Используется регулярное выражение `[a-zA-Z]:[\\/].*` для проверки, является ли путь Windows-подобным (например, `C:/...` или `C:\\...`). Если путь соответствует этому шаблону, функция пытается открыть и прочитать файл.
     - Если файл успешно прочитан, его содержимое сохраняется в `self.html_content`, и функция возвращает `True`.
     - Если файл не найден или произошла ошибка при чтении, функция регистрирует ошибку и возвращает `False`.
   - **Веб-URL (http:// или https://)**:
     - Если URL начинается с 'http://' или 'https://', функция вызывает метод `self.get_url(url)` для извлечения контента.
     - Если `self.get_url(url)` возвращает `False` (например, из-за сетевой ошибки), функция регистрирует ошибку и возвращает `False`.
     - В случае успеха, предполагает, что `self.get_url(url)` сохраняет HTML-контент в `self.page_source` и возвращает `self.page_source`.
   - **Неподдерживаемые протоколы**:
     - Если URL не начинается ни с одного из поддерживаемых протоколов, функция регистрирует ошибку и возвращает `False`.

**Примеры**:

```python
instance = YourClassName()
instance.current_url = 'http://default.example.com'

# 1. Извлечение с веб-URL
success_web = instance.fetch_html('https://example.com/page')
# Предполагается, что get_url успешно получает данные и устанавливает self.page_source
print(success_web)
True
print(instance.html_content) # doctest: +ELLIPSIS
<html><body>Mock content for https://example.com/page</body></html>

# 2. Извлечение из локального файла (требует создания фиктивного файла)
import tempfile
import os
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_file:
    _ = tmp_file.write("<html><body>Local Test Content</body></html>")
    tmp_file_path = tmp_file.name
# Создание URI файла (скорректируйте формат для ОС, Path.as_uri() надежен)
file_uri = Path(tmp_file_path).as_uri() # например, file:///tmp/xyz.html или file:///C:/Users/...\
# Нам нужно немного адаптировать URI, если регулярное выражение явно ожидает букву диска
if os.name == 'nt':
    # Реконструируем URI, чтобы соответствовать регулярному выражению C:/..., если это необходимо для реализации
    # Текущее регулярное выражение '[a-zA-Z]:[\\\\/].*' требует этого в Windows
    # Пример: 'file://C:/Users/...'
    match = re.match(r"file:///(?P<drive>[a-zA-Z]):/(?P<rest>.*)", file_uri)
    if match:
        file_uri_for_func = f"file://{match.group('drive')}:/{match.group('rest')}"
    else: # Откат, если разбор не удался, может не работать с функцией
        file_uri_for_func = file_uri
else: # В Unix-подобных системах Path.as_uri() обычно работает, если регулярное выражение игнорируется
    file_uri_for_func = file_uri
...
# Mocking Path.exists() and open() for the example to work without the function's specific regex check
original_exists = Path.exists
original_open = open
def mock_exists(path_obj):
    return str(path_obj) == tmp_file_path
def mock_open(path_obj, mode='r', encoding=None):
    if str(path_obj) == tmp_file_path:
        # Вернуть реальный дескриптор файла для временного файла
        return original_open(tmp_file_path, mode, encoding=encoding)
    else:
        raise FileNotFoundError
Path.exists = mock_exists
builtins_open = __builtins__.open # Store original built-in open
__builtins__.open = mock_open # Temporarily override built-in open

# Эта часть сильно зависит от детали реализации регулярного выражения:
# Давайте предположим, что file_uri_for_func теперь правильно отформатирован для регулярного выражения в Windows
# или что проверка регулярного выражения обходится/изменяется для Unix.
# Принудительно используем простую строку пути, которая *может* работать с регулярным выражением, если диск C: существует
test_uri = 'file://C:/path/to/mock/file.html' # Общий заполнитель
if os.path.exists(Path(tmp_file_path)): # Убедитесь, что временный файл все еще существует
   if os.name == 'nt': # Создаем путь, ожидаемый регулярным выражением
       cleaned_path_str = tmp_file_path.replace('\\\\', '/') # Обеспечиваем прямые слэши
       drive = Path(tmp_file_path).drive # например, 'C:'
       if drive:
            test_uri = f"file://{drive}/{cleaned_path_str.split(':', 1)[1]}"
       else: # Если нет диска, вероятно, сетевой путь, не будет соответствовать регулярному выражению
            test_uri = Path(tmp_file_path).as_uri() # Откат
   else: # Unix
       test_uri = Path(tmp_file_path).as_uri() # например, file:///path/to/file
...
# Теперь давайте смоделируем вызов с созданным URI или общим
# ПРИМЕЧАНИЕ: Этот пример сложен из-за моделирования файловой системы и зависимости от регулярного выражения
# Упрощенный тест может просто проверить логические ветви
print(f"Attempting to fetch: {test_uri}") # Show what URI is being used
Attempting to fetch: ...
# success_file = instance.fetch_html(test_uri) # Actual call (mocked)
# print(success_file) # Expected: True
# print(instance.html_content) # Expected: "<html><body>Local Test Content</body></html>"
# Clean up mocks and temp file
Path.exists = original_exists
__builtins__.open = builtins_open
os.remove(tmp_file_path)
print("Skipping actual file test execution in docstring due to complexity") # Placeholder acknowledgment
Skipping actual file test execution in docstring due to complexity

# 3. Использование URL по умолчанию (self.current_url)
success_default = instance.fetch_html() # url is '', use self.current_url
print(success_default)
True
print(instance.html_content) # doctest: +ELLIPSIS
<html><body>Mock content for http://default.example.com</body></html>

# 4. Обработка несуществующего пути к локальному файлу
success_no_file = instance.fetch_html('file://C:/non/existent/file.html')
print(success_no_file)
False

# 5. Обработка пути к файлу с неправильным форматом (не соответствующим регулярному выражению)
success_bad_format = instance.fetch_html('file:///unix/style/path/without/drive/letter') # Might fail regex check
print(success_bad_format)
False

# 6. Обработка сбоя из get_url (например, 404 Not Found simulated)
success_fail_fetch = instance.fetch_html('http://example.com/notfound')
print(success_fail_fetch)
False

# 7. Обработка исключения сетевой ошибки из get_url
success_network_error = instance.fetch_html('http://error.example.com')
print(success_network_error)
False

# 8. Обработка неподдерживаемого протокола
success_bad_protocol = instance.fetch_html('ftp://example.com/resource')
print(success_bad_protocol)
False
```

## Параметры класса

- `webdriver_cls`: Класс WebDriver, например Chrome или Firefox.
- `*args`: Позиционные аргументы для драйвера.
- `**kwargs`: Ключевые аргументы для драйвера.
- `item` (str): Имя атрибута.
- `scrolls` (int): Количество прокруток, по умолчанию 1.
- `frame_size` (int): Размер прокрутки в пикселях, по умолчанию 600.
- `direction` (str): Направление ('both', 'down', 'up'), по умолчанию 'both'.
- `delay` (float): Время задержки между прокрутками, по умолчанию 0.3.
- `url` (str): URL для перехода.
- `url` (Optional[str]): URL для открытия в новой вкладке. По умолчанию `None`.
- `delay` (float): Время задержки в секундах. По умолчанию 0.3.
- `url` (Optional[str]): URL или путь к локальному файлу (с префиксом 'file://'), из которого нужно извлечь HTML-контент. Поддерживает протоколы 'file://', 'http://' и 'https://'. Если опущен, пуст или `None`, будет использовано значение `self.current_url`. По умолчанию ''.

```markdown
## Оглавление

1. [Классы](#Классы)
    - [`Driver`](#Driver)
2. [Методы класса](#Методы-класса)
    - [`__init__`](#__init__)
    - [`__init_subclass__`](#__init_subclass__)
    - [`__getattr__`](#__getattr__)
    - [`scroll`](#scroll)
        -