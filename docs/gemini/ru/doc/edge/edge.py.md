### Анализ кода `hypotez/src/webdriver/edge/edge.py.md`

## Обзор

Модуль предоставляет кастомную реализацию Edge WebDriver для Selenium.

## Подробнее

Этот модуль расширяет возможности стандартного класса `webdriver.Edge` из библиотеки Selenium, предоставляя более удобный и гибкий интерфейс для работы с браузером Edge. Он включает поддержку пользовательских профилей, управление пользовательским агентом, прокси-серверами и различные режимы отображения окна браузера. Класс предназначен для упрощения автоматизации веб-браузеров в проекте `hypotez`.

## Классы

### `Edge`

```python
class Edge(WebDriver):
    """
    Custom Edge WebDriver class for enhanced functionality.

    Attributes:
        driver_name (str): Name of the WebDriver used, defaults to 'edge'.
    """
    ...
```

**Описание**:
Кастомный класс Edge WebDriver для расширенной функциональности.

**Наследует**:

*   `selenium.webdriver.Edge`

**Атрибуты**:

*   `driver_name` (str): Имя драйвера (`'edge'`).

**Методы**:

*   `__init__(self, profile_name: Optional[str] = None, user_agent: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует экземпляр класса `Edge`.
*   `set_proxy(self, options: Options) -> None`: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.
*   `_payload(self) -> None`: Загружает исполнителей для локаторов и JavaScript сценариев.
*   `set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions`: Создает и настраивает параметры запуска для Edge WebDriver.

## Методы класса

### `__init__`

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

**Назначение**:
Инициализирует экземпляр класса `Edge`.

**Параметры**:

*   `profile_name` (str, optional): Имя пользовательского профиля Edge.
*   `user_agent` (str, optional): Пользовательский агент в формате строки. Если `None`, генерируется случайный user-agent.
*   `options` (List[str], optional): Список опций Edge для передачи при инициализации.
*   `window_mode` (str, optional): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).
*   `*args`: Произвольные позиционные аргументы для конструктора `WebDriver`.
*   `**kwargs`: Произвольные именованные аргументы для конструктора `WebDriver`.

**Как работает функция**:

1.  Загружает настройки Edge из файла `edge.json`.
2.  Определяет путь к драйверу Edge (edgedriver).
3.  Инициализирует объект `EdgeOptions` для настройки Edge.
4.  Добавляет опции из файла конфигурации и переданные при инициализации.
5.  Устанавливает режим окна (kiosk, windowless, full\_window).
6.  Устанавливает пользовательский агент.
7.  Настраивает директорию профиля пользователя.
8.  Инициализирует экземпляр `Edge` с настроенными опциями и сервисом.
9.  Вызывает метод `_payload` для загрузки исполнителей для локаторов и JavaScript сценариев.
10. Обрабатывает исключения `WebDriverException` и другие исключения, логируя ошибки.

### `set_options`

```python
def set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions:  
    """  
    Create and configure launch options for the Edge WebDriver.  

    :param opts: A list of options to add to the Edge WebDriver. Defaults to `None`.  
    :return: Configured `EdgeOptions` object.  
    """
    ...
```

**Назначение**:
Создает и настраивает параметры запуска для Edge WebDriver.

**Параметры**:

*   `opts` (List[str], optional): Список опций для добавления в Edge WebDriver. По умолчанию `None`.

**Возвращает**:

*   `EdgeOptions`: Настроенный объект `EdgeOptions`.

**Как работает функция**:
1.  Создает экземпляр `EdgeOptions`.
2.  Если передан список опций, добавляет каждую опцию в объект `EdgeOptions`.
3.  Возвращает настроенный объект `EdgeOptions`.

### `_payload`

```python
def _payload(self) -> None:
    """
    Load executors for locators and JavaScript scenarios.
    """
    ...
```

**Назначение**:
Загружает исполнителей для локаторов и JavaScript сценариев.

**Как работает функция**:

1.  Создает экземпляр класса `JavaScript` и `ExecuteLocator`.
2.  Присваивает методы этих экземпляров атрибутам текущего объекта `self` для удобного доступа к ним.

## Переменные

*   `driver_name` (str): Имя драйвера (`'edge'`).

## Примеры использования

```python
from selenium.webdriver import Edge
from src.webdriver.edge import Edge

# Создание экземпляра драйвера Edge с настройками по умолчанию
driver = Edge()

# Создание экземпляра драйвера Edge с указанием режима окна
driver = Edge(window_mode='full_window')
```

## Зависимости

*   `os`: Для работы с операционной системой.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Optional, typing.List`: Для аннотаций типов.
*   `selenium.webdriver.edge.options.Options`: Для настройки опций Edge.
*   `selenium.webdriver.edge.service.Service`: Для управления EdgeDriver.
*   `selenium.common.exceptions.WebDriverException`: Для обработки исключений WebDriver.
*   `src.webdriver.executor.ExecuteLocator`: Для выполнения локаторов.
*   `src.webdriver.js.JavaScript`: Для выполнения JavaScript-кода.
*    `fake_useragent`: Для получения случайного user-agent
*   `src.utils.jjson.j_loads_ns`: Для загрузки конфигурации из JSON.
*   `src.logger.logger`: Для логирования.

## Взаимосвязи с другими частями проекта

Модуль `edge.py` расширяет функциональность Selenium WebDriver для браузера Edge и используется в других частях проекта `hypotez`, где требуется автоматизированное взаимодействие с веб-страницами через Edge.

*   Он зависит от `src.webdriver.executor.ExecuteLocator` и `src.webdriver.js.JavaScript` для выполнения действий на веб-страницах.
*   Использует `src.logger.logger` для логирования.
*   Для получения глобальных настроек используются модули `header`, `src.gs`.