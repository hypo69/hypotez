### Анализ кода модуля `src/webdriver/edge/edge.py`

## Обзор

Этот модуль предоставляет пользовательскую реализацию Edge WebDriver на основе Selenium, упрощая его настройку и использование.

## Подробней

Модуль `src/webdriver/edge/edge.py` предназначен для работы с Microsoft Edge WebDriver в проекте `hypotez`. Он предоставляет класс `Edge`, который наследует от `selenium.webdriver.Edge` и позволяет настраивать различные параметры браузера, такие как пользовательский агент, профиль пользователя и другие опции, с использованием файла конфигурации `edge.json`. Модуль также интегрирует функциональность для выполнения JavaScript-кода и поиска элементов на странице.

## Классы

### `Edge`

**Описание**: Пользовательская реализация Edge WebDriver на основе Selenium.

**Наследует**:

-   `selenium.webdriver.Edge`

**Атрибуты**:

-   `driver_name` (str): Имя драйвера ("edge").

**Методы**:

-   `__init__(self, profile_name: Optional[str] = None, user_agent: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует экземпляр класса `Edge` с указанными параметрами.
-   `__init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs)`: Автоматически вызывается при создании подкласса `Driver`.
-   `set_proxy(self, options: Options) -> None`: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.
-   `_payload(self) -> None`: Загружает исполнителей для локаторов и JavaScript сценариев.
-   `set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions`: Создает и настраивает опции запуска для Edge WebDriver.

#### `__init__`

**Назначение**: Инициализирует экземпляр класса `Edge`.

```python
def __init__(self,  profile_name: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 options: Optional[List[str]] = None,
                 window_mode: Optional[str] = None,
                 *args, **kwargs) -> None:
    """
    Initializes the Edge WebDriver with the specified user agent and options.

    :param user_agent: The user-agent string to be used. If `None`, a random user agent is generated.
    :type user_agent: Optional[str]
    :param options: A list of Edge options to be passed during initialization.
    :type options: Optional[List[str]]
    :param window_mode: Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.)
    :type window_mode: Optional[str]
    """
    ...
```

**Параметры**:

-   `profile_name` (Optional[str]): Имя пользовательского профиля Edge.
-   `user_agent` (Optional[str]): Пользовательский агент в формате строки.
-   `options` (Optional[List[str]]): Список опций для Edge.
-   `window_mode` (Optional[str]): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.)
-   `*args`: Произвольные позиционные аргументы, передаваемые в конструктор базового класса.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор базового класса.

**Как работает функция**:

1.  Загружает настройки Edge из файла `edge.json`.
2.  Инициализирует объект `EdgeOptions` для настройки Edge.
3.  Устанавливает пользовательский агент, используя `fake_useragent` для генерации случайного агента, если не указан.
4.  Добавляет опции из файла конфигурации и переданных аргументов.
5.  Устанавливает режим окна браузера (kiosk, windowless, full\_window).
6.  Настраивает директорию профиля пользователя.
7.  Создает экземпляр `Edge WebDriver` с указанными настройками.
8.  Вызывает функцию `_payload` для загрузки исполнителей для локаторов и JavaScript сценариев.
9.  Логирует информацию о процессе запуска и обрабатывает возможные исключения.

#### `set_proxy`

**Назначение**: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.

```python
def set_proxy(self, options: Options) -> None:
    """
    Настройка прокси из словаря, возвращаемого get_proxies_dict.

    :param options: Опции Chrome, в которые добавляются настройки прокси.
    :type options: Options
    """
    ...
```

**Параметры**:

-   `options` (Options): Опции Edge, в которые добавляются настройки прокси.

**Как работает функция**:

1.  Получает словарь прокси-серверов, используя функцию `get_proxies_dict`.
2.  Создает список всех прокси-серверов (SOCKS4 и SOCKS5).
3.  Перебирает прокси-серверы в случайном порядке, чтобы найти рабочий прокси.
4.  Если рабочий прокси найден, настраивает опции Edge для использования этого прокси.
5.  Логирует информацию о настройке прокси или отсутствии доступных прокси-серверов.

#### `_payload`

**Назначение**: Загружает исполнителей для локаторов и JavaScript сценариев.

```python
def _payload(self) -> None:
    """
    Load executors for locators and JavaScript scenarios.
    """
    ...
```

**Как работает функция**:

1.  Создает экземпляр класса `JavaScript`, передавая ему экземпляр веб-драйвера.
2.  Назначает методы из экземпляра `JavaScript` (например, `get_page_lang`, `ready_state`, `unhide_DOM_element`) атрибутам текущего объекта `Edge`.
3.  Создает экземпляр класса `ExecuteLocator`, передавая ему экземпляр веб-драйвера.
4.  Назначает методы из экземпляра `ExecuteLocator` (например, `execute_locator`, `get_webelement_as_screenshot`, `send_message`) атрибутам текущего объекта `Edge`.

#### `set_options`

**Назначение**: Создает и настраивает опции запуска для Edge WebDriver.

```python
def set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions:  
    """  
    Create and configure launch options for the Edge WebDriver.  

    :param opts: A list of options to add to the Edge WebDriver. Defaults to `None`.  
    :return: Configured `EdgeOptions` object.  
    """  
    ...
```

**Параметры**:

-   `opts` (Optional[List[str]]): Список опций для добавления в Edge WebDriver. По умолчанию `None`.

**Возвращает**:

-   `EdgeOptions`: Настроенный объект `EdgeOptions`.

**Как работает функция**:

1. Создает экземпляр `EdgeOptions`.
2. Если переданы какие-либо опции, добавляет их в `EdgeOptions`.
3. Возвращает настроенный объект `EdgeOptions`.

## Переменные модуля

-   `driver_name` (str): Имя драйвера ("edge").
-   `service` (Service): Экземпляр класса `selenium.webdriver.edge.service.Service`, который управляет процессом EdgeDriver.
-    `options_obj` (Options): экземпляр класса `selenium.webdriver.edge.options.Options`, который используется для настройки параметров запуска браузера Edge.
-   `user_agent` (str): Содержит строку User-Agent, которая будет установлена для браузера.
-   `profile_directory` (str): содержит путь к профилю пользователя Edge.

## Пример использования

**Создание экземпляра Edge WebDriver с настройками по умолчанию:**

```python
from src.webdriver.edge import Edge

driver = Edge()
driver.get("https://www.example.com")
driver.quit()
```

**Создание экземпляра Edge WebDriver с пользовательским профилем и User-Agent:**

```python
from src.webdriver.edge import Edge

driver = Edge(profile_name="my_profile", user_agent="My Custom Agent")
driver.get("https://www.example.com")
driver.quit()
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/webdriver/edge/edge.py` зависит от библиотеки `selenium` для управления браузером Edge, от модуля `src.webdriver.executor` для выполнения действий с веб-элементами, от модуля `src.webdriver.js` для выполнения JavaScript-кода, от модуля `fake_useragent` для генерации случайных User-Agent, от модуля `src.logger.logger` для логирования и от модуля `src.utils.jjson` для загрузки конфигурации.
-   Он предоставляет класс `Edge`, который используется в других модулях для создания и управления веб-драйвером Edge.