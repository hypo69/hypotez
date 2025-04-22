# Модуль для работы с веб-драйверами Selenium

## Обзор

Основное назначение модуля - предоставить класс `Driver`, который обеспечивает унифицированный интерфейс для работы с веб-драйверами Selenium. Он упрощает задачи инициализации драйвера, навигации по URL, управления куками и обработки исключений. Код вебдрайверов находится в подмодулях `chrome`, `firefox`, `edge`, `playwright`, а файлы настроек для веб-браузеров - в соответствующих JSON-файлах.

## Подробнее

Модуль предназначен для абстрагирования работы с различными веб-браузерами через Selenium WebDriver. Он включает в себя класс `Driver`, который позволяет инициализировать и управлять веб-драйверами, такими как Chrome, Firefox и Edge.  Этот модуль также обрабатывает распространенные исключения, которые могут возникнуть при работе с веб-драйверами, и предоставляет удобные методы для выполнения таких задач, как прокрутка страниц, получение URL и сохранение куки.

## Классы

### `Driver`

**Описание**: Класс обеспечивает удобный интерфейс для работы с различными драйверами, такими как Chrome, Firefox и Edge.

**Атрибуты**:
    - `driver` (selenium.webdriver): Экземпляр Selenium WebDriver.
    - `current_url` (str): Текущий URL, с которым работает драйвер.

**Методы**:
    - `__init__(self, webdriver_cls, *args, **kwargs)`: Инициализирует экземпляр класса `Driver`.
    - `__init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs)`: Автоматически вызывается при создании подкласса `Driver`.
    - `__getattr__(self, item: str)`: Прокси для доступа к атрибутам драйвера.
    - `scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3)`: Прокручивает страницу в указанном направлении.
    - `locale`: Определяет язык страницы на основе мета-тегов или JavaScript.
    - `get_url(self, url: str)`: Переходит по указанному URL и сохраняет текущий URL, предыдущий URL и куки.
    - `window_open(self, url: Optional[str] = None)`: Открывает новую вкладку в текущем окне браузера и переключается на нее.
    - `wait(self, delay: float = .3)`: Ожидает указанное количество времени.
    - `_save_cookies_localy(self)`: Сохраняет текущие куки веб-драйвера в локальный файл.
    - `fetch_html(self, url: Optional[str] = '')`: Извлекает HTML-контент из локального файла или веб-URL и сохраняет его.

**Принцип работы**:
Класс `Driver` предоставляет унифицированный интерфейс для работы с веб-драйверами Selenium. При инициализации класса передается класс веб-драйвера (например, `Chrome` или `Firefox`), который затем используется для создания экземпляра веб-драйвера. Класс также предоставляет методы для выполнения общих задач, таких как прокрутка страниц, получение URL, сохранение куки и извлечение HTML-контента.

## Методы класса

### `__init__(self, webdriver_cls, *args, **kwargs)`

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

**Назначение**: Инициализация экземпляра класса `Driver`.

**Параметры**:
    - `webdriver_cls`: Класс WebDriver, который будет использоваться (например, `Chrome` или `Firefox`).
    - `*args`: Позиционные аргументы, передаваемые конструктору `webdriver_cls`.
    - `**kwargs`: Ключевые аргументы, передаваемые конструктору `webdriver_cls`.

**Вызывает исключения**:
    - `TypeError`: Если `webdriver_cls` не является допустимым классом WebDriver (не имеет атрибута `get`).

**Как работает функция**:
Функция проверяет, является ли переданный класс `webdriver_cls` допустимым классом WebDriver, убедившись, что у него есть атрибут `get`. Если проверка проходит, создается экземпляр класса `webdriver_cls` с переданными аргументами `*args` и `**kwargs`, и этот экземпляр присваивается атрибуту `driver` класса `Driver`.

**Примеры**:
```python
from selenium.webdriver import Chrome
driver = Driver(Chrome, executable_path='/path/to/chromedriver')
```

### `__init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs)`

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

**Назначение**: Инициализация подклассов `Driver`.

**Параметры**:
    - `browser_name` (Optional[str]): Имя браузера.
    - `kwargs`: Дополнительные аргументы.

**Вызывает исключения**:
    - `ValueError`: Если `browser_name` не указан.

**Как работает функция**:
Функция `__init_subclass__` автоматически вызывается при создании подкласса `Driver`. Она проверяет, указано ли имя браузера (`browser_name`). Если имя браузера не указано, вызывается исключение `ValueError`. В противном случае имя браузера сохраняется как атрибут класса (`cls.browser_name`).

**Примеры**:
```python
class MyDriver(Driver, browser_name='Chrome'):
    pass
```

### `__getattr__(self, item: str)`

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

**Назначение**: Обеспечивает доступ к атрибутам драйвера Selenium.

**Параметры**:
    - `item` (str): Имя атрибута, к которому необходимо получить доступ.

**Как работает функция**:
Функция пытается получить атрибут с именем `item` из экземпляра драйвера Selenium (`self.driver`) и возвращает его. Это позволяет обращаться к атрибутам и методам драйвера Selenium напрямую через экземпляр класса `Driver`.

**Примеры**:
```python
driver = Driver(Chrome)
url = driver.current_url
```

### `scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3)`

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
    ...
```

**Назначение**: Прокрутка страницы в заданном направлении.

**Параметры**:
    - `scrolls` (int): Количество прокруток. По умолчанию 1.
    - `frame_size` (int): Размер прокрутки в пикселях. По умолчанию 600.
    - `direction` (str): Направление прокрутки (`'both'`, `'down'`, `'up'`). По умолчанию `'both'`.
    - `delay` (float): Задержка между прокрутками в секундах. По умолчанию 0.3.

**Возвращает**:
    - `bool`: `True`, если прокрутка выполнена успешно, `False` в противном случае.

**Внутренние функции**:
    - `carousel(direction: str = '', scrolls: int = 1, frame_size: int = 600, delay: float = .3) -> bool`: Локальный метод для прокрутки экрана.

**Как работает функция**:
Функция `scroll` прокручивает страницу в указанном направлении (`direction`). Если `direction` равно `'forward'` или `'down'`, страница прокручивается вниз. Если `direction` равно `'backward'` или `'up'`, страница прокручивается вверх. Если `direction` равно `'both'`, страница прокручивается и вниз, и вверх.  Функция использует JavaScript для выполнения прокрутки.

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

**Назначение**: Определение языка страницы на основе мета-тегов или JavaScript.

**Возвращает**:
    - `Optional[str]`: Код языка, если найден, иначе `None`.

**Как работает функция**:
Функция `locale` пытается определить язык страницы, сначала ища мета-тег `Content-Language`. Если мета-тег не найден, функция пытается определить язык с помощью JavaScript. Если ни один из этих методов не срабатывает, функция возвращает `None`.

**Примеры**:
```python
lang = driver.locale
print(lang)  # 'en' или None
```

### `get_url(self, url: str)`

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

**Назначение**: Переход по указанному URL.

**Параметры**:
    - `url` (str): URL для перехода.

**Возвращает**:
    - `bool`: `True`, если переход успешен, `False` в противном случае.

**Вызывает исключения**:
    - `WebDriverException`: Если возникает ошибка с WebDriver.
    - `InvalidArgumentException`: Если URL некорректен.
    - `Exception`: Для любых других ошибок при переходе.

**Как работает функция**:
Функция `get_url` переходит по указанному URL, используя метод `get` драйвера Selenium.  Она также сохраняет текущий URL, предыдущий URL и куки. В случае возникновения исключений, таких как `WebDriverException` или `InvalidArgumentException`, они перехватываются и логируются, а функция возвращает `False`.

**Примеры**:
```python
driver.get_url('https://www.example.com')
```

### `window_open(self, url: Optional[str] = None)`

```python
def window_open(self, url: Optional[str] = None) -> None:
    """Open a new tab in the current browser window and switch to it.

    Args:
        url: URL to open in the new tab. Defaults to `None`.
    """
    ...
```

**Назначение**: Открывает новую вкладку в текущем окне браузера и переключается на нее.

**Параметры**:
    - `url` (Optional[str]): URL для открытия в новой вкладке. По умолчанию `None`.

**Как работает функция**:
Функция `window_open` использует JavaScript для открытия новой вкладки в текущем окне браузера. Затем она переключается на новую вкладку и, если указан URL, переходит по этому URL.

**Примеры**:
```python
driver.window_open('https://www.example.com')
```

### `wait(self, delay: float = .3)`

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

**Назначение**: Ожидание в течение заданного времени.

**Параметры**:
    - `delay` (float): Время задержки в секундах. По умолчанию 0.3.

**Как работает функция**:
Функция `wait` приостанавливает выполнение программы на указанное количество секунд, используя функцию `time.sleep`.

**Примеры**:
```python
driver.wait(1)  # Ожидание в течение 1 секунды
```

### `_save_cookies_localy(self)`

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

**Назначение**: Сохранение куки веб-драйвера в локальный файл.

**Вызывает исключения**:
    - `Exception`: Если возникает ошибка при сохранении куки.

**Как работает функция**:
Функция `_save_cookies_localy` сохраняет текущие куки веб-драйвера в локальный файл, используя модуль `pickle` для сериализации данных. В случае возникновения ошибки при сохранении куки, она логируется.  В текущей реализации функция всегда возвращает `True` и не сохраняет куки (закомментировано для отладки).

### `fetch_html(self, url: Optional[str] = '')`

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
        >>> file_uri = Path(tmp_file_path).as_uri() # e.g., file:///tmp/xyz.html or file:///C:/Users/...
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
        ...        drive = Path(tmp_file_path).drive # e.g., 'C:\\'
        ...        if drive:
        ...             test_uri = f"file://{drive}/{cleaned_path_str.split(':', 1)[1]}"
        ...        else: # If no drive, likely network path, won't match regex
        ...             test_uri = Path(tmp_file_path).as_uri() # Fallback
        ...    else: # Unix
        ...        test_uri = Path(tmp_file_path).as_uri() # e.g., file:///path/to/file
        ...
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

**Назначение**: Извлечение HTML-контента из локального файла или веб-URL и сохранение его.

**Параметры**:
    - `url` (Optional[str]): URL или путь к локальному файлу (с префиксом `'file://'`), из которого нужно извлечь HTML-контент. Поддерживаются протоколы `'file://'`, `'http://'` и `'https://'`. Если не указан, используется значение `self.current_url`. По умолчанию `''`.

**Возвращает**:
    - `bool`: `True`, если HTML-контент успешно извлечен и сохранен в `self.html_content`. `False`, если произошла ошибка во время извлечения или чтения.

**Как работает функция**:
Функция `fetch_html` пытается извлечь HTML-код на основе указанного `url`. Если `url` начинается с `'file://'`, функция пытается прочитать HTML из локального файла. Если `url` начинается с `'http://'` или `'https://'`, функция использует метод `get_url` для получения HTML-кода из сети. Полученный HTML-код сохраняется в `self.html_content`.

Если `url` не указан, используется значение `self.current_url`.

Если возникает какая-либо ошибка (например, неверный формат пути к файлу, файл не найден, ошибка чтения файла, сетевая ошибка), она логируется, и функция возвращает `False`.

**Примеры**:
```python
instance = YourClassName()
instance.current_url = 'http://default.example.com'

# 1. Извлечение с веб-URL
success_web = instance.fetch_html('https://example.com/page')
# Предполагается, что get_url успешно устанавливает self.page_source
print(success_web)
True
print(instance.html_content) # doctest: +ELLIPSIS
<html><body>Mock content for https://example.com/page</body></html>

# 2. Извлечение из локального файла (требуется создание фиктивного файла)
import tempfile
import os
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_file:
    _ = tmp_file.write("<html><body>Local Test Content</body></html>")
    tmp_file_path = tmp_file.name
# Конструкция file URI (скорректируйте формат для OS, если необходимо, Path.as_uri() является надежным)
file_uri = Path(tmp_file_path).as_uri() # e.g., file:///tmp/xyz.html or file:///C:/Users/...
# Нам нужно немного адаптировать URI, если regex ожидает букву диска явно
if os.name == 'nt':
    # Восстановите URI, чтобы соответствовать regex C:/... при необходимости для детали реализации
    # Текущий regex '[a-zA-Z]:[\\\\/].*' требует этого в Windows
    # Пример: 'file://C:/Users/...'
    match = re.match(r"file:///(?P<drive>[a-zA-Z]):/(?P<rest>.*)", file_uri)
    if match:
        file_uri_for_func = f"file://{match.group('drive')}:/{match.group('rest')}"
    else: # Fallback, если разбор не удался, может не работать с функцией
        file_uri_for_func = file_uri
else: # В Unix-подобных системах Path.as_uri() обычно работает, если regex игнорируется
    file_uri_for_func = file_uri