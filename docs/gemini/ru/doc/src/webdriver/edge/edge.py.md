# Модуль `edge.py`

## Обзор

Модуль `edge.py` предоставляет класс `Edge`, который является пользовательским классом WebDriver для браузера Edge. Он упрощает настройку Edge WebDriver с использованием `fake_useragent` для генерации случайных user-agent, а также предоставляет дополнительные методы для работы с элементами на веб-странице.

## Подробнее

Модуль содержит класс `Edge`, который наследуется от `selenium.webdriver.Edge`. Он инициализирует драйвер Edge с заданными параметрами, такими как user-agent, опции и режим окна. Также он загружает исполнители локаторов и JavaScript сценариев для выполнения различных действий на веб-странице.

## Классы

### `Edge`

**Описание**: Класс `Edge` представляет собой пользовательский WebDriver для браузера Edge. Он позволяет настраивать user-agent, опции и режим окна при инициализации драйвера.

**Наследует**: `selenium.webdriver.Edge`

**Атрибуты**:
- `driver_name` (str): Имя WebDriver, используемого по умолчанию, равно 'edge'.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Edge` с заданными параметрами.
- `_payload`: Загружает исполнители для локаторов и JavaScript сценариев.
- `set_options`: Создает и настраивает параметры запуска для Edge WebDriver.

#### `__init__`

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
    :type options: Optional[str]
    :param window_mode: Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.)
    :type window_mode: Optional[str]
    """
```

**Назначение**: Инициализирует экземпляр класса `Edge` с заданными параметрами, такими как user-agent, опции и режим окна.

**Параметры**:
- `profile_name` (Optional[str], optional): Имя профиля пользователя. По умолчанию `None`.
- `user_agent` (Optional[str], optional): User-agent, который будет использоваться. Если `None`, генерируется случайный user-agent.
- `options` (Optional[List[str]], optional): Список опций Edge, передаваемых при инициализации. По умолчанию `None`.
- `window_mode` (Optional[str], optional): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.). По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы.
- `**kwargs`: Произвольные именованные аргументы.

**Возвращает**: `None`

**Вызывает исключения**:
- `WebDriverException`: Если не удается запустить Edge WebDriver.
- `Exception`: При возникновении общей ошибки.

**Как работает функция**:
1. Инициализирует user-agent, используя предоставленное значение или генерирует случайный, если значение не предоставлено.
2. Загружает настройки из файла `edge.json`.
3. Инициализирует опции Edge, добавляет user-agent и другие опции, полученные из файла конфигурации и переданные в качестве аргументов.
4. Настраивает директорию профиля пользователя.
5. Пытается запустить Edge WebDriver с заданными опциями и сервисом.
6. Вызывает метод `_payload` для загрузки исполнителей локаторов и JavaScript.
7. Логирует информацию о запуске Edge WebDriver.
8. Обрабатывает исключения, если не удается запустить Edge WebDriver или происходит общая ошибка.

**Примеры**:
```python
driver = Edge(user_agent='Mozilla/5.0', options=['--headless'])
driver = Edge(window_mode='kiosk')
```

#### `_payload`

```python
def _payload(self) -> None:
    """
    Load executors for locators and JavaScript scenarios.
    """
```

**Назначение**: Загружает исполнители для локаторов и JavaScript сценариев.

**Параметры**:
- Нет

**Возвращает**: `None`

**Как работает функция**:
1. Инициализирует класс `JavaScript` с текущим экземпляром `Edge`.
2. Присваивает функции JavaScript из класса `JavaScript` текущему экземпляру `Edge`.
3. Инициализирует класс `ExecuteLocator` с текущим экземпляром `Edge`.
4. Присваивает функции из класса `ExecuteLocator` текущему экземпляру `Edge`.

**Примеры**:
```python
driver = Edge()
driver._payload()
```

#### `set_options`

```python
def set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions:  
    """  
    Create and configure launch options for the Edge WebDriver.  

    :param opts: A list of options to add to the Edge WebDriver. Defaults to `None`.  
    :return: Configured `EdgeOptions` object.  
    """
```

**Назначение**: Создает и настраивает параметры запуска для Edge WebDriver.

**Параметры**:
- `opts` (Optional[List[str]], optional): Список опций для добавления в Edge WebDriver. По умолчанию `None`.

**Возвращает**:
- `EdgeOptions`: Сконфигурированный объект `EdgeOptions`.

**Как работает функция**:
1. Создает экземпляр класса `EdgeOptions`.
2. Если передан список опций `opts`, добавляет каждую опцию в экземпляр `EdgeOptions`.
3. Возвращает сконфигурированный объект `EdgeOptions`.

**Примеры**:
```python
options = Edge().set_options(['--headless', '--disable-gpu'])
```

## Пример использования

```python
if __name__ == "__main__":
    driver = Edge(window_mode='full_window')
    driver.get("https://www.example.com")
```

В этом примере создается экземпляр класса `Edge` в полноэкранном режиме и открывается веб-страница "https://www.example.com".