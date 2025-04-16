### Анализ кода модуля `hypotez/src/webdriver/edge/edge.py`

## Обзор

Этот модуль предоставляет кастомную реализацию Edge WebDriver для Selenium.

## Подробнее

Этот модуль расширяет базовый класс `webdriver.Edge` из Selenium, добавляя поддержку пользовательских профилей, `user-agent`, режимов работы окна и интеграцию с файлами конфигурации.

## Классы

### `Edge`

```python
class Edge(WebDriver):
    """
    Custom Edge WebDriver class for enhanced functionality.

    Attributes:
        driver_name (str): Name of the WebDriver used, defaults to 'edge'.
    """
```

**Описание**:
Класс `Edge` является расширением для `webdriver.Edge` и предоставляет дополнительные возможности для управления браузером Edge.

**Наследует**:
- `WebDriver` (из `selenium.webdriver`)

**Атрибуты**:
- `driver_name` (str): Имя драйвера (`'edge'`).

**Методы**:

*   `__init__(self, profile_name: Optional[str] = None, user_agent: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует экземпляр класса `Edge`.
*   `set_proxy(self, options: Options) -> None`: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.
*   `_payload(self) -> None`: Загружает исполнителей для локаторов и JavaScript сценариев.
*   `set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions`: Создает и настраивает параметры запуска для Edge WebDriver.

## Методы класса

### `__init__`

```python
def __init__(self, profile_name: Optional[str] = None,
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

*   `profile_name` (Optional[str]): Имя профиля.
*   `user_agent` (Optional[str]): Строка User-Agent.
*   `options` (Optional[List[str]]): Дополнительные опции для Edge.
*   `window_mode` (Optional[str]): Режим отображения окна (например, "kiosk", "windowless", "full_window").
*   `*args`: Дополнительные позиционные аргументы, передаваемые в конструктор базового класса.
*   `**kwargs`: Дополнительные именованные аргументы, передаваемые в конструктор базового класса.

**Как работает функция**:

1.  Загружает конфигурацию из файла `edge.json`.
2.  Инициализирует объект `EdgeOptions`.
3.  Добавляет пользовательский user-agent и другие параметры.
4.  Создает сервис Edge с указанным путем к драйверу.
5.  Вызывает конструктор базового класса `WebDriver` с настроенными опциями и сервисом.

### `set_proxy`

```python
def set_proxy(self, options: Options) -> None:
    """
    Настройка прокси из словаря, возвращаемого get_proxies_dict.

    :param options: Опции Chrome, в которые добавляются настройки прокси.
    :type options: Options
    """
    ...
```

**Назначение**:
Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.

**Параметры**:
-   `options` (Options): Объект `Options`, к которому применяются настройки прокси.

**Как работает функция**:
1.  Получает словарь прокси-серверов, используя `get_proxies_dict()`.
2.  Проверяет, есть ли рабочие прокси и настраивает их, если они найдены.
3. Логирует параметры установленного прокси

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

1.  Создает экземпляр класса `JavaScript` и назначает его методы для управления веб-страницей.
2.  Создает экземпляр класса `ExecuteLocator` и назначает его методы для выполнения локаторов.

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
-   `opts` (Optional[List[str]]): Список опций для добавления в Edge WebDriver. По умолчанию None.

**Возвращает**:
-   `EdgeOptions`: Настроенный объект `EdgeOptions`.

**Как работает функция**:
1.  Создает объект `EdgeOptions`.
2.  Если передан список опций, добавляет их к объекту `EdgeOptions`.
3.  Возвращает настроенный объект `EdgeOptions`.

## Переменные

-   `driver_name: str = 'edge'` - имя драйвера

## Запуск

Для использования этого модуля необходимо установить библиотеку `selenium` и `fake_useragent`.
Также необходимо скачать и указать путь к EdgeDriver.

```bash
pip install selenium fake_useragent
```

Пример использования:

```python
from src.webdriver.edge import Edge

driver = Edge(window_mode='full_window')
driver.get("https://google.com")