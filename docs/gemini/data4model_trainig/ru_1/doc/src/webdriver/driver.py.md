# Модуль для работы с веб-драйверами Selenium `driver.py`

## Обзор

Модуль предоставляет класс `Driver`, обеспечивающий унифицированный интерфейс для работы с веб-драйверами Selenium. Он упрощает инициализацию драйвера, навигацию по URL, управление куками и обработку исключений. В модуле определен класс `Driver`, который служит базовым классом для управления веб-драйверами, такими как Chrome, Firefox и Edge. Код вебдрайверов находится в подмодулях `chrome`, `firefox`, `edge`, `playwright`. Файлы настроек для веб-браузеров находятся в: `chrome\\chrome.json`, `firefox\\firefox.json`, `edge\\edge.json`, `playwright\\playwright.json`.

## Подробней

Этот модуль предназначен для упрощения взаимодействия с веб-драйверами, предоставляя абстракцию над сложными деталями настройки и управления драйверами. Он позволяет легко переключаться между различными браузерами и обеспечивает централизованное управление куками и обработку ошибок.

## Классы

### `Driver`

**Описание**:
Класс `Driver` предоставляет удобный интерфейс для работы с различными веб-драйверами, такими как Chrome, Firefox и Edge. Он упрощает процесс инициализации драйвера, навигации по URL, управления куками и обработки исключений.

**Атрибуты**:
- `driver` (selenium.webdriver): Экземпляр Selenium WebDriver.

**Методы**:
- `__init__(self, webdriver_cls, *args, **kwargs)`: Инициализирует экземпляр класса `Driver`.
- `__init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs)`: Автоматически вызывается при создании подкласса `Driver`.
- `__getattr__(self, item: str)`: Прокси для доступа к атрибутам драйвера.
- `scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3) -> bool`: Прокручивает страницу в указанном направлении.
- `locale(self) -> Optional[str]`: Определяет язык страницы на основе мета-тегов или JavaScript.
- `get_url(self, url: str) -> bool`: Переходит по указанному URL и сохраняет текущий URL, предыдущий URL и куки.
- `window_open(self, url: Optional[str] = None) -> None`: Открывает новую вкладку в текущем окне браузера и переключается на нее.
- `wait(self, delay: float = .3) -> None`: Ожидает указанное количество времени.
- `_save_cookies_localy(self) -> None`: Сохраняет текущие куки веб-драйвера в локальный файл.
- `fetch_html(self, url: str) -> Optional[bool]`: Извлекает HTML-контент из файла или веб-страницы.

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

**Назначение**:
Инициализирует экземпляр класса `Driver`, принимая класс веб-драйвера и аргументы для его инициализации.

**Параметры**:
- `webdriver_cls`: Класс WebDriver, например, `Chrome` или `Firefox`.
- `*args`: Позиционные аргументы, передаваемые конструктору `webdriver_cls`.
- `**kwargs`: Ключевые аргументы, передаваемые конструктору `webdriver_cls`.

**Вызывает исключения**:
- `TypeError`: Если `webdriver_cls` не является допустимым классом WebDriver (не имеет атрибута `get`).

**Как работает функция**:
1. Проверяет, является ли переданный класс `webdriver_cls` допустимым классом WebDriver (имеет ли атрибут `get`).
2. Если проверка проходит, создает экземпляр этого класса, передавая ему все дополнительные аргументы `*args` и `**kwargs`.
3. Сохраняет созданный экземпляр веб-драйвера в атрибуте `self.driver`.

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

**Назначение**:
Автоматически вызывается при создании подкласса `Driver`. Используется для задания имени браузера для подкласса.

**Параметры**:
- `browser_name`: Имя браузера (например, "Chrome", "Firefox").
- `**kwargs`: Дополнительные аргументы, передаваемые в `super().__init_subclass__()`.

**Вызывает исключения**:
- `ValueError`: Если `browser_name` не указан.

**Как работает функция**:
1. Вызывает метод `__init_subclass__` родительского класса (`super().__init_subclass__(**kwargs)`).
2. Проверяет, передан ли аргумент `browser_name`. Если нет, вызывает исключение `ValueError`.
3. Сохраняет значение `browser_name` в атрибуте класса `cls.browser_name`.

**Примеры**:

```python
class MyDriver(Driver, browser_name='Chrome'):
    pass
```

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

**Назначение**:
Обеспечивает доступ к атрибутам и методам экземпляра веб-драйвера, хранящегося в `self.driver`.

**Параметры**:
- `item`: Имя запрашиваемого атрибута.

**Возвращает**:
- Значение атрибута или метода из `self.driver`.

**Как работает функция**:
1. Пытается получить атрибут с именем `item` из экземпляра веб-драйвера `self.driver` с помощью функции `getattr()`.
2. Возвращает полученное значение. Если атрибут не найден, `getattr()` вызовет исключение `AttributeError`, которое будет перехвачено вызывающей стороной.

**Примеры**:

```python
driver = Driver(Chrome)
url = driver.current_url  # Получение текущего URL страницы
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

    try:
        if direction == 'forward' or direction == 'down':
            return carousel('', scrolls, frame_size, delay)
        elif direction == 'backward' or direction == 'up':
            return carousel('-', scrolls, frame_size, delay)
        elif direction == 'both':
            return carousel('', scrolls, frame_size, delay) and carousel('-', scrolls, frame_size, delay)
    except Exception as ex:
        logger.error('Ошибка в функции прокрутки', ex)
        return False
```

**Назначение**:
Прокручивает веб-страницу в заданном направлении на указанное количество "шагов" с заданной задержкой между ними.

**Параметры**:
- `scrolls` (int): Количество прокруток (шагов). По умолчанию 1.
- `frame_size` (int): Размер каждого "шага" прокрутки в пикселях. По умолчанию 600.
- `direction` (str): Направление прокрутки:
  - `'forward'` или `'down'`: Вниз.
  - `'backward'` или `'up'`: Вверх.
  - `'both'`: Вниз и вверх.
  По умолчанию `'both'`.
- `delay` (float): Задержка в секундах между каждым "шагом" прокрутки. По умолчанию 0.3.

**Возвращает**:
- `True`, если прокрутка выполнена успешно.
- `False`, если возникла ошибка.

**Внутренние функции**:
- `carousel(direction: str = '', scrolls: int = 1, frame_size: int = 600, delay: float = .3) -> bool`: Локальный метод для прокрутки экрана.
    - Параметры:
        - `direction` (str): Направление ('down', 'up').
        - `scrolls` (int): Количество прокруток.
        - `frame_size` (int): Размер прокрутки.
        - `delay` (float): Задержка между прокрутками.
    - Возвращает: `True`, если успешно, иначе `False`.

**Как работает функция**:
1. Определяет направление прокрутки на основе параметра `direction`.
2. Вызывает внутреннюю функцию `carousel` для выполнения фактической прокрутки в заданном направлении.
3. Если `direction` равен `'both'`, выполняет прокрутку вниз, а затем вверх.
4. Перехватывает любые исключения, возникшие в процессе прокрутки, логирует их и возвращает `False`.

**Примеры**:

```python
# Прокрутка страницы вниз на 3 шага с размером шага 800 пикселей и задержкой 0.5 секунды
driver.scroll(scrolls=3, frame_size=800, direction='down', delay=0.5)

# Прокрутка страницы вверх на 2 шага с размером шага по умолчанию и задержкой по умолчанию
driver.scroll(scrolls=2, direction='up')

# Прокрутка страницы вниз и вверх на 1 шаг с параметрами по умолчанию
driver.scroll()
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

**Назначение**:
Определяет язык текущей страницы, анализируя мета-теги и выполняя JavaScript-код.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Код языка страницы (например, `'en'`, `'ru'`), если он найден.
- `None`, если язык определить не удалось.

**Как работает функция**:
1. Пытается найти мета-тег `Content-Language` и извлечь из него значение атрибута `content`.
2. Если мета-тег не найден или произошла ошибка, пытается определить язык с помощью JavaScript-функции `self.get_page_lang()`.
3. Если ни один из способов не дал результата, возвращает `None`.
4. Все возникающие исключения логируются с уровнем `DEBUG`.

**Примеры**:

```python
lang = driver.locale
if lang:
    print(f"Язык страницы: {lang}")
else:
    print("Не удалось определить язык страницы")
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

**Назначение**:
Загружает указанный URL в текущий веб-драйвер и выполняет проверки для обеспечения успешной загрузки страницы.

**Параметры**:
- `url` (str): URL, который нужно загрузить.

**Возвращает**:
- `True`, если URL успешно загружен и состояние страницы соответствует ожидаемому.
- `False` в случае ошибки или несоответствия состояния страницы.

**Как работает функция**:
1. Копирует текущий URL (`self.current_url`) во временную переменную `_previous_url`.
2. Пытается загрузить новый URL (`self.driver.get(url)`).
3. Ожидает завершения загрузки страницы, проверяя свойство `self.ready_state`. Если страница не загружается в течение 5 попыток, прерывает цикл и логирует ошибку.
4. Если новый URL отличается от предыдущего, сохраняет предыдущий URL в `self.previous_url`.
5. Сохраняет куки (`self._save_cookies_localy()`).
6. Возвращает `True`, если все шаги выполнены успешно.
7. В случае возникновения исключений `WebDriverException`, `InvalidArgumentException` или других исключений, логирует ошибки и возвращает `False`.

**Примеры**:

```python
driver = Driver(Chrome)
success = driver.get_url("https://www.example.com")
if success:
    print("Страница успешно загружена")
else:
    print("Ошибка при загрузке страницы")
```

### `window_open`

```python
def window_open(self, url: Optional[str] = None) -> None:
    """Open a new tab in the current browser window and switch to it.

    Args:
        url: URL to open in the new tab. Defaults to `None`.
    """
    ...
```

**Назначение**:
Открывает новую вкладку в текущем окне браузера и переключается на нее.

**Параметры**:
- `url` (Optional[str]): URL, который нужно открыть в новой вкладке. Если не указан, открывается пустая вкладка. По умолчанию `None`.

**Возвращает**:
- `None`

**Как работает функция**:
1. Использует JavaScript для открытия новой вкладки (`self.execute_script('window.open();')`).
2. Переключается на новую вкладку, используя `self.switch_to.window(self.window_handles[-1])`.
3. Если указан `url`, загружает его в новой вкладке с помощью `self.get(url)`.

**Примеры**:

```python
driver = Driver(Chrome)
driver.window_open("https://www.example.com")  # Открывает новую вкладку с example.com
driver.window_open()  # Открывает пустую новую вкладку
```

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

**Назначение**:
Приостанавливает выполнение программы на заданное количество секунд.

**Параметры**:
- `delay` (float): Время задержки в секундах. По умолчанию 0.3 секунды.

**Возвращает**:
- `None`

**Как работает функция**:
1. Использует функцию `time.sleep(delay)` для приостановки выполнения программы на указанное количество секунд.

**Примеры**:

```python
driver = Driver(Chrome)
print("Начинаем ожидание...")
driver.wait(2)  # Ожидание в течение 2 секунд
print("Ожидание завершено!")
```

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

**Назначение**:
Сохраняет куки текущего сеанса веб-драйвера в локальный файл.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Exception`: Если происходит ошибка при сохранении куки в файл.

**Как работает функция**:
1. Определяет путь к файлу, в котором будут сохранены куки (`gs.cookies_filepath`).
2. Открывает файл в бинарном режиме для записи (`'wb'`).
3. Использует модуль `pickle` для сериализации куки, полученных из `self.driver.get_cookies()`, и записывает их в файл.
4. Перехватывает любые исключения, возникающие в процессе сохранения куки, логирует их с помощью `logger.error` и печатает сообщение об ошибке.

**Примеры**:

```python
driver = Driver(Chrome)
driver.get_url('https://www.example.com')
driver._save_cookies_localy()  # Сохраняет куки для сайта example.com
```

### `fetch_html`

```python
def fetch_html(self, url: str) -> Optional[bool]:
    """
    Извлекает HTML-контент из файла или веб-страницы.

    Args:
        url: Путь к файлу или URL для извлечения HTML-контента.

    Returns:
        Возвращает `True`, если контент успешно получен, иначе `None`.

    Raises:
        Exception: Если возникает ошибка при извлечении контента.
    """
    ...
```

**Назначение**:
Извлекает HTML-контент из указанного URL, который может быть как локальным файлом, так и веб-страницей.

**Параметры**:
- `url` (str): URL или путь к файлу, из которого нужно извлечь HTML-контент.

**Возвращает**:
- `True`, если HTML-контент успешно извлечен и сохранен в `self.html_content`.
- `False`, если произошла ошибка при извлечении контента.
- `None`, если не удалось определить протокол.

**Как работает функция**:
1. Проверяет, начинается ли URL с `file://`. Если да, то пытается прочитать HTML-контент из локального файла:
   - Извлекает путь к файлу из URL.
   - Проверяет, существует ли файл.
   - Если файл существует, открывает его в режиме чтения, с кодировкой UTF-8, и читает контент в `self.html_content`.
   - В случае ошибки логирует ее и возвращает `False`.
2. Если URL начинается с `http://` или `https://`, то пытается получить HTML-контент с веб-страницы:
   - Использует метод `self.get_url(url)` для загрузки страницы.
   - Если загрузка успешна, сохраняет `self.page_source` (HTML-код страницы) в `self.html_content`.
   - В случае ошибки логирует ее и возвращает `False`.
3. Если URL не начинается ни с `file://`, ни с `http://` или `https://`, то логирует ошибку о неподдерживаемом протоколе и возвращает `False`.

**Примеры**:

```python
driver = Driver(Chrome)

# Извлечение HTML-контента из локального файла
file_url = "file:///C:/path/to/your/local/file.html"
if driver.fetch_html(file_url):
    print("HTML-контент успешно извлечен из файла")
else:
    print("Не удалось извлечь HTML-контент из файла")

# Извлечение HTML-контента с веб-страницы
web_url = "https://www.example.com"
if driver.fetch_html(web_url):
    print("HTML-контент успешно извлечен с веб-страницы")
else:
    print("Не удалось извлечь HTML-контент с веб-страницы")