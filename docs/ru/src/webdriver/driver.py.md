# Модуль `driver`

## Обзор

Модуль `driver` предназначен для работы с веб-драйверами Selenium, предоставляя унифицированный интерфейс для взаимодействия с различными веб-браузерами, такими как Chrome, Firefox и Edge. Он упрощает задачи инициализации драйвера, навигации по URL, управления куками и обработки исключений.

## Подробней

Этот модуль обеспечивает абстракцию над Selenium WebDriver, что позволяет упростить взаимодействие с веб-браузерами. Он содержит класс `Driver`, который можно использовать для управления веб-драйвером, навигации по страницам, выполнения JavaScript-кода и взаимодействия с элементами на странице.

Файлы настроек для веб-браузеров находятся в директориях `chrome`, `firefox`, `edge` и `playwright`, а соответствующие файлы конфигурации имеют расширение `.json`.

## Классы

### `Driver`

**Описание**: Класс обеспечивает удобный интерфейс для работы с различными драйверами, такими как Chrome, Firefox и Edge.

**Принцип работы**:
Класс `Driver` является оболочкой для Selenium WebDriver, предоставляя методы для упрощения взаимодействия с веб-браузерами. Он позволяет инициализировать драйвер с различными параметрами, переходить по URL, управлять куками и выполнять другие операции.

**Аттрибуты**:
- `driver` (selenium.webdriver): Экземпляр Selenium WebDriver.
- `browser_name` (str): Имя браузера, используемое в подклассах.
- `previous_url` (str): Предыдущий URL, на котором находился драйвер.
- `html_content` (str): HTML-контент страницы, извлеченный функцией `fetch_html`.

**Методы**:
- `__init__(webdriver_cls, *args, **kwargs)`: Инициализирует экземпляр класса `Driver`.
- `__init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs)`: Автоматически вызывается при создании подкласса `Driver`.
- `__getattr__(self, item: str)`: Прокси для доступа к атрибутам драйвера.
- `scroll(scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3)`: Прокручивает страницу в указанном направлении.
- `locale`: Определяет язык страницы на основе мета-тегов или JavaScript.
- `get_url(url: str)`: Переходит по указанному URL и сохраняет текущий URL, предыдущий URL и куки.
- `window_open(url: Optional[str] = None)`: Открывает новую вкладку в текущем окне браузера и переключается на нее.
- `wait(delay: float = .3)`: Ожидает указанное количество времени.
- `_save_cookies_localy()`: Сохраняет текущие куки веб-драйвера в локальный файл.
- `fetch_html(url: str)`: Извлекает HTML-контент из файла или веб-страницы.

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

**Назначение**: Инициализирует экземпляр класса `Driver`, принимая класс веб-драйвера (например, `Chrome` или `Firefox`) и аргументы для его инициализации.

**Параметры**:
- `webdriver_cls`: Класс WebDriver, который будет использоваться (например, `Chrome`, `Firefox`).
- `*args`: Позиционные аргументы, передаваемые в конструктор `webdriver_cls`.
- `**kwargs`: Ключевые аргументы, передаваемые в конструктор `webdriver_cls`.

**Возвращает**:
- None

**Вызывает исключения**:
- `TypeError`: Если `webdriver_cls` не является допустимым классом WebDriver (т.е. не имеет метода `get`).

**Как работает функция**:
1. Проверяет, является ли `webdriver_cls` допустимым классом WebDriver (имеет ли он атрибут `get`).
2. Если проверка проходит, создает экземпляр `webdriver_cls` с переданными аргументами `*args` и `**kwargs`.
3. Сохраняет созданный экземпляр в атрибуте `self.driver`.

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

**Назначение**: Автоматически вызывается при создании подкласса `Driver`. Используется для установки имени браузера для подкласса.

**Параметры**:
- `cls`: Класс, для которого вызывается метод.
- `browser_name` (Optional[str]): Имя браузера. Должно быть указано при создании подкласса.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- None

**Вызывает исключения**:
- `ValueError`: Если `browser_name` не указан при создании подкласса.

**Как работает функция**:
1. Вызывает метод `__init_subclass__` родительского класса.
2. Проверяет, указано ли имя браузера (`browser_name`).
3. Если имя браузера не указано, вызывает исключение `ValueError`.
4. Сохраняет имя браузера в атрибуте `browser_name` класса.

**Примеры**:

```python
class MyDriver(Driver, browser_name='Chrome'):
    ...
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

**Назначение**: Обеспечивает доступ к атрибутам и методам базового драйвера `self.driver` через экземпляр класса `Driver`.

**Параметры**:
- `item` (str): Имя атрибута, к которому необходимо получить доступ.

**Возвращает**:
- Значение атрибута или метода из `self.driver`.

**Как работает функция**:
1. Пытается получить атрибут `item` из `self.driver` с помощью функции `getattr`.
2. Возвращает полученное значение. Если атрибут не существует, будет вызвано исключение `AttributeError`.

**Примеры**:

```python
driver = Driver(Chrome)
url = driver.current_url  # Получение текущего URL через прокси
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

**Назначение**: Прокручивает страницу в указанном направлении на заданное количество пикселей с заданной задержкой.

**Параметры**:
- `scrolls` (int): Количество прокруток. По умолчанию 1.
- `frame_size` (int): Размер прокрутки в пикселях. По умолчанию 600.
- `direction` (str): Направление прокрутки ('both', 'down', 'up', 'forward', 'backward'). По умолчанию 'both'.
- `delay` (float): Задержка между прокрутками в секундах. По умолчанию 0.3.

**Возвращает**:
- `True`, если прокрутка выполнена успешно, `False` в случае ошибки.

**Внутренние функции**:

- `carousel(direction: str = '', scrolls: int = 1, frame_size: int = 600, delay: float = .3) -> bool`:
  - **Назначение**: Выполняет фактическую прокрутку страницы на заданное количество пикселей в указанном направлении.
  - **Параметры**:
    - `direction` (str): Направление прокрутки ('', '-').
    - `scrolls` (int): Количество прокруток.
    - `frame_size` (int): Размер прокрутки в пикселях.
    - `delay` (float): Задержка между прокрутками в секундах.
  - **Возвращает**:
    - `True`, если прокрутка выполнена успешно, `False` в случае ошибки.

**Как работает функция**:

Основная функция `scroll` вызывает внутреннюю функцию `carousel` в зависимости от переданного параметра `direction`:
1. Если `direction` равно `'forward'` или `'down'`, вызывает `carousel` с пустым направлением (`''`) для прокрутки вниз.
2. Если `direction` равно `'backward'` или `'up'`, вызывает `carousel` с направлением `'-'` для прокрутки вверх.
3. Если `direction` равно `'both'`, вызывает `carousel` дважды: один раз для прокрутки вниз, другой раз для прокрутки вверх.

Внутренняя функция `carousel` выполняет прокрутку страницы с помощью JavaScript-кода `window.scrollBy`. Она прокручивает страницу на `frame_size` пикселей в указанном направлении (`direction`) заданное количество раз (`scrolls`) с задержкой `delay` между прокрутками.

**Примеры**:

```python
driver.scroll(scrolls=3, direction='down')  # Прокрутка вниз на 3 раза
driver.scroll(scrolls=2, frame_size=800, direction='up', delay=0.5)  # Прокрутка вверх на 2 раза с другими параметрами
driver.scroll(direction='both')  # Прокрутка вверх и вниз по одному разу
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
    try:
        meta_language = self.find_element(By.CSS_SELECTOR, "meta[http-equiv='Content-Language']")
        return meta_language.get_attribute('content')
    except Exception as ex:
        logger.debug('Не удалось определить язык сайта из META', ex)
        try:
            return self.get_page_lang()
        except Exception as ex:
            logger.debug('Не удалось определить язык сайта из JavaScript', ex)
            return
```

**Назначение**: Определяет язык страницы, анализируя мета-теги или выполняя JavaScript-код.

**Параметры**:
- None

**Возвращает**:
- Код языка страницы (например, 'en', 'ru') в виде строки, если язык удалось определить.
- `None`, если язык не удалось определить ни через мета-теги, ни через JavaScript.

**Как работает функция**:
1. **Пытается извлечь язык из мета-тега**:
   - Использует `find_element` для поиска элемента `<meta>` с атрибутом `http-equiv="Content-Language"`.
   - Если элемент найден, извлекает значение атрибута `content`, которое должно содержать код языка.
   - Если происходит исключение (например, элемент не найден), логирует отладочное сообщение и переходит к следующему шагу.
2. **Пытается извлечь язык с помощью JavaScript**:
   - Вызывает метод `get_page_lang()`.
   - Если вызов успешен, возвращает полученный код языка.
   - Если происходит исключение, логирует отладочное сообщение и возвращает `None`.

ASCII flowchart:

```
A[Поиск мета-тега Content-Language]
|
B[Удалось найти?]
|
C[Извлечение атрибута content]
|
D[Возврат кода языка]
|
E[Вызов get_page_lang()]
|
F[Успешно?]
|
G[Возврат кода языка]
|
H[Возврат None]

A --> B
B -- Да --> C
C --> D
B -- Нет --> E
E --> F
F -- Да --> G
G --> Конец
F -- Нет --> H
H --> Конец
```

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
    _previous_url: str = copy.copy(self.current_url)

    try:
        self.driver.get(url)
       
        attempts = 5
        while self.ready_state not in ('complete','interactive'):
            """ Ожидание завершения загрузки страницы """
            attempts -= 5
            if attempts < 0: # Если страница не загрузилась за 5 попыток, то цикл прерывается с выводом сообщения об ошибке
                logger.error(f'Страница не загрузилась за 5 попыток: {url=}')
                ...
                break
            time.sleep(1)

        if url != _previous_url:
            self.previous_url = _previous_url

        self._save_cookies_localy()
        return True
        
    except WebDriverException as ex:
        logger.error('WebDriverException', ex)
        return False

    except InvalidArgumentException as ex:
        logger.error(f"InvalidArgumentException {url}", ex)
        return False
    except Exception as ex:
        logger.error(f'Ошибка при переходе по URL: {url}\n', ex)
        return False
```

**Назначение**: Переходит по указанному URL, сохраняет текущий URL, предыдущий URL и куки.

**Параметры**:
- `url` (str): URL для перехода.

**Возвращает**:
- `True`, если переход успешен и текущий URL совпадает с ожидаемым.
- `False`, в противном случае.

**Вызывает исключения**:
- `WebDriverException`: Если возникает ошибка, связанная с WebDriver.
- `InvalidArgumentException`: Если URL некорректен.
- `Exception`: Для любых других ошибок при переходе.

**Как работает функция**:
1. Сохраняет текущий URL в переменную `_previous_url`.
2. Пытается перейти по указанному URL с помощью `self.driver.get(url)`.
3. Ожидает завершения загрузки страницы, проверяя `self.ready_state`.
4. Если URL отличается от предыдущего, сохраняет предыдущий URL в `self.previous_url`.
5. Сохраняет куки в локальный файл с помощью `self._save_cookies_localy()`.
6. Возвращает `True`, если все шаги выполнены успешно.
7. В случае возникновения исключений `WebDriverException`, `InvalidArgumentException` или `Exception`, логирует ошибку и возвращает `False`.

ASCII flowchart:

```
A[Сохранение текущего URL]
|
B[Переход по URL]
|
C[Ожидание загрузки страницы]
|
D[URL изменился?]
|
E[Сохранение предыдущего URL]
|
F[Сохранение куки]
|
G[Возврат True]
|
H[Обработка WebDriverException]
|
I[Обработка InvalidArgumentException]
|
J[Обработка Exception]
|
K[Логирование ошибки]
|
L[Возврат False]

A --> B
B --> C
C --> D
D -- Да --> E
E --> F
D -- Нет --> F
F --> G
B -- Исключение --> H
H --> K
K --> L
C -- Превышено время ожидания --> K
K --> L
```

**Примеры**:

```python
url = "https://www.example.com"
if driver.get_url(url):
    print(f"Успешно перешли на {url}")
else:
    print(f"Не удалось перейти на {url}")
```

### `window_open`

```python
def window_open(self, url: Optional[str] = None) -> None:
    """Open a new tab in the current browser window and switch to it.

    Args:
        url: URL to open in the new tab. Defaults to `None`.
    """
    self.execute_script('window.open();')
    self.switch_to.window(self.window_handles[-1])
    if url:
        self.get(url)
```

**Назначение**: Открывает новую вкладку в текущем окне браузера и переключается на нее.

**Параметры**:
- `url` (Optional[str]): URL для открытия в новой вкладке. Если не указан, открывается пустая вкладка.

**Возвращает**:
- None

**Как работает функция**:
1. Открывает новую вкладку с помощью JavaScript-кода `window.open()`.
2. Переключается на новую вкладку, используя `self.switch_to.window(self.window_handles[-1])`.
3. Если указан URL, открывает его в новой вкладке с помощью `self.get(url)`.

**Примеры**:

```python
driver.window_open("https://www.example.com")  # Открывает новую вкладку с указанным URL
driver.window_open()  # Открывает новую пустую вкладку
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
    time.sleep(delay)
```

**Назначение**: Приостанавливает выполнение кода на указанное количество секунд.

**Параметры**:
- `delay` (float): Время задержки в секундах. По умолчанию 0.3.

**Возвращает**:
- None

**Как работает функция**:
1. Использует функцию `time.sleep(delay)` для приостановки выполнения кода на `delay` секунд.

**Примеры**:

```python
driver.wait(1)  # Ожидание в течение 1 секунды
driver.wait()  # Ожидание в течение 0.3 секунды
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
    return True # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ debug
    try:
        with open(gs.cookies_filepath, 'wb') as cookiesfile:
            pickle.dump(self.driver.get_cookies(), cookiesfile)
    except Exception as ex:
        logger.error('Ошибка при сохранении куки:', ex)
```

**Назначение**: Сохраняет текущие куки веб-драйвера в локальный файл.

**Параметры**:
- None

**Возвращает**:
- None

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при сохранении куки.

**Как работает функция**:
1. Открывает файл, указанный в `gs.cookies_filepath`, в режиме записи байтов (`'wb'`).
2. Использует `pickle.dump()` для сериализации и сохранения куки, полученных с помощью `self.driver.get_cookies()`, в открытый файл.
3. Обрабатывает возможное исключение, логирует ошибку с помощью `logger.error()` и передает информацию об исключении.

**Примеры**:

```python
driver._save_cookies_localy()
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
    if url.startswith('file://'):
        cleaned_url = url.replace('file://', '')
        match = re.search(r'[a-zA-Z]:[\\/].*', cleaned_url)
        if match:
            file_path = Path(match.group(0))
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.html_content = file.read()
                    return True
                except Exception as ex:
                    logger.error('Ошибка при чтении файла:', ex)
                    return False
            else:
                logger.error('Локальный файл не найден:', file_path)
                return False
        else:
            logger.error('Некорректный путь к файлу:', cleaned_url)
            return False
    elif url.startswith('http://') or url.startswith('https://'):
        try:
            if self.get_url(url):
                self.html_content = self.page_source
                return True
        except Exception as ex:
            logger.error(f"Ошибка при получении {url}:", ex)
            return False
    else:
        logger.error("Ошибка: Неподдерживаемый протокол для URL:", url)
        return False
```

**Назначение**: Извлекает HTML-контент из файла или веб-страницы.

**Параметры**:
- `url` (str): Путь к файлу или URL для извлечения HTML-контента.

**Возвращает**:
- `True`, если контент успешно получен.
- `False`, если произошла ошибка при чтении файла или получении веб-страницы.
- `None` в случае неподдерживаемого протокола.

**Как работает функция**:
1. **Проверяет протокол URL**:
   - Если URL начинается с `file://`, пытается прочитать HTML-контент из локального файла.
   - Если URL начинается с `http://` или `https://`, пытается получить HTML-контент с веб-страницы.
   - Если URL не соответствует ни одному из поддерживаемых протоколов, логирует ошибку и возвращает `False`.

2. **Чтение из локального файла**:
   - Удаляет префикс `file://` из URL.
   - Извлекает путь к файлу с помощью регулярного выражения.
   - Проверяет существование файла с помощью `Path(file_path).exists()`.
   - Если файл существует, открывает его в режиме чтения, читает контент и сохраняет в `self.html_content`.
   - В случае ошибки логирует её и возвращает `False`.

3. **Получение с веб-страницы**:
   - Вызывает `self.get_url(url)` для перехода на указанный URL.
   - Если переход успешен, сохраняет `self.page_source` (HTML-контент страницы) в `self.html_content`.
   - В случае ошибки логирует её и возвращает `False`.

ASCII flowchart:

```
A[Проверка протокола URL]
|
B[file://]   C[http(s)://]   D[Другой]
|
E[Чтение из файла]  F[Получение с веб-страницы]  G[Ошибка: Неподдерживаемый протокол]
|
H[Удаление префикса]  I[Вызов self.get_url(url)]  J[Логирование ошибки]
|
K[Извлечение пути к файлу]  L[Переход успешен?]
|
M[Файл существует?]  N[Сохранение self.page_source в self.html_content]
|
O[Чтение контента файла]  P[Возврат True]
|
Q[Сохранение в self.html_content]
|
R[Возврат True]
|
S[Логирование ошибки]
|
T[Возврат False]

A --> B, C, D
B --> E
C --> F
D --> G
G --> J --> T
E --> H
F --> I
I --> L
L -- Да --> N
N --> P
L -- Нет --> S --> T
H --> K
K --> M
M -- Да --> O
O --> Q
Q --> R
M -- Нет --> S --> T
```

**Примеры**:

```python
# Чтение из локального файла
driver.fetch_html('file:///C:/path/to/file.html')

# Получение с веб-страницы
driver.fetch_html('https://www.example.com')