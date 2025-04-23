# Модуль `edge.py`

## Обзор

Модуль `edge.py` предоставляет кастомный класс `Edge`, который расширяет возможности стандартного Edge WebDriver из библиотеки Selenium. Класс предназначен для упрощения конфигурации WebDriver, включая управление user-agent, опциями запуска и профилями пользователей. Модуль использует библиотеку `fake_useragent` для генерации случайных user-agent строк, что помогает имитировать поведение реальных пользователей и избегать блокировок со стороны веб-сайтов.

## Подробнее

Модуль содержит класс `Edge`, который наследуется от `selenium.webdriver.Edge`. Он позволяет настраивать различные параметры запуска браузера Edge, такие как user-agent, опции командной строки и профиль пользователя. Класс также включает методы для выполнения JavaScript-кода и поиска элементов на странице с использованием локаторов.

## Классы

### `Edge`

**Описание**:
Кастомный класс Edge WebDriver для расширенной функциональности.

**Наследует**:
`selenium.webdriver.Edge`

**Атрибуты**:
- `driver_name` (str): Имя используемого драйвера WebDriver, по умолчанию 'edge'.
- `user_agent` (str): Строка user-agent, используемая для имитации браузера.

**Методы**:
- `__init__`: Инициализирует Edge WebDriver с указанным user-agent и опциями.
- `_payload`: Загружает исполнители для локаторов и JavaScript сценариев.
- `set_options`: Создает и конфигурирует параметры запуска для Edge WebDriver.

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
```

**Назначение**:
Инициализирует экземпляр класса `Edge`.

**Параметры**:
- `profile_name` (Optional[str], optional): Имя профиля пользователя. По умолчанию `None`.
- `user_agent` (Optional[str], optional): User-agent для имитации. Если не указан, генерируется случайный user-agent. По умолчанию `None`.
- `options` (Optional[List[str]], optional): Список опций Edge для передачи при инициализации. По умолчанию `None`.
- `window_mode` (Optional[str], optional): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.). По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, которые передаются в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, которые передаются в конструктор родительского класса.

**Как работает функция**:
- Инициализирует user-agent, используя предоставленный или генерируя случайный.
- Загружает настройки из файла `edge.json`.
- Устанавливает опции Edge, такие как user-agent, режим окна (kiosk, windowless, full_window) и другие параметры из конфигурации и переданных аргументов.
- Настраивает директорию профиля пользователя.
- Запускает Edge WebDriver с заданными опциями и сервисом.
- Вызывает метод `_payload` для загрузки исполнителей локаторов и JavaScript.

**Примеры**:

```python
# Инициализация Edge WebDriver с пользовательским user-agent
driver = Edge(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

# Инициализация Edge WebDriver с дополнительными опциями
driver = Edge(options=['--disable-gpu', '--disable-extensions'])

# Инициализация Edge WebDriver в режиме kiosk
driver = Edge(window_mode='kiosk')
```

### `_payload`

```python
def _payload(self) -> None:
    """
    Load executors for locators and JavaScript scenarios.
    """
```

**Назначение**:
Загружает исполнители для локаторов и JavaScript сценариев.

**Как работает функция**:
- Создает экземпляр класса `JavaScript` и присваивает его атрибуту `j`.
- Присваивает методы из экземпляра `JavaScript` текущему экземпляру `Edge`:
  - `get_page_lang` - получение языка страницы.
  - `ready_state` - получение состояния готовности страницы.
  - `get_referrer` - получение реферера страницы.
  - `unhide_DOM_element` - отображение DOM элемента.
  - `window_focus` - установка фокуса на окно.
- Создает экземпляр класса `ExecuteLocator` и присваивает его переменной `execute_locator`.
- Присваивает методы из экземпляра `ExecuteLocator` текущему экземпляру `Edge`:
  - `execute_locator` - выполнение локатора.
  - `get_webelement_as_screenshot` - получение скриншота веб-элемента.
  - `get_webelement_by_locator` - получение веб-элемента по локатору.
  - `get_attribute_by_locator` - получение атрибута по локатору.
  - `send_message` - отправка сообщения веб-элементу.
  - `send_key_to_webelement` - отправка ключа веб-элементу.

**Примеры**:

```python
# Загрузка исполнителей для локаторов и JavaScript сценариев
driver._payload()
```

### `set_options`

```python
def set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions:  
    """  
    Create and configure launch options for the Edge WebDriver.  

    :param opts: A list of options to add to the Edge WebDriver. Defaults to `None`.  
    :return: Configured `EdgeOptions` object.  
    """  
```

**Назначение**:
Создает и конфигурирует параметры запуска для Edge WebDriver.

**Параметры**:
- `opts` (Optional[List[str]], optional): Список опций для добавления в Edge WebDriver. По умолчанию `None`.

**Возвращает**:
- `EdgeOptions`: Сконфигурированный объект `EdgeOptions`.

**Как работает функция**:
- Создает экземпляр класса `EdgeOptions`.
- Если предоставлен список опций (`opts`), добавляет каждую опцию в объект `EdgeOptions`.
- Возвращает сконфигурированный объект `EdgeOptions`.

**Примеры**:

```python
# Создание и настройка опций запуска Edge WebDriver
options = driver.set_options(opts=['--disable-gpu', '--disable-extensions'])
```

## Параметры класса

- `driver_name` (str): Имя используемого драйвера WebDriver, по умолчанию 'edge'.
- `user_agent` (str): Строка user-agent, используемая для имитации браузера.

## Пример использования

```python
from src.webdriver.edge.edge import Edge

# Создание инстанса Edge WebDriver в режиме полного окна
driver = Edge(window_mode='full_window')

# Открытие веб-страницы
driver.get("https://www.example.com")
```