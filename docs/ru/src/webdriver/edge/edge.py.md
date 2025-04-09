# Модуль `src.webdriver.edge.edge`

## Обзор

Модуль предоставляет пользовательский класс `Edge` для управления веб-драйвером Edge с упрощенной конфигурацией, использующей `fake_useragent`. Он позволяет настраивать user-agent, параметры запуска и профили пользователей.

## Подробнее

Этот модуль предоставляет класс `Edge`, который наследует от `selenium.webdriver.Edge`. Он предназначен для упрощения настройки и запуска драйвера Edge с использованием `fake_useragent` для генерации случайных user-agent'ов. Модуль также позволяет указывать различные параметры запуска, такие как режим окна (kiosk, windowless, full_window) и путь к профилю пользователя.

## Классы

### `Edge`

**Описание**: Пользовательский класс WebDriver для Edge, расширяющий функциональность стандартного `selenium.webdriver.Edge`.

**Наследует**:
- `selenium.webdriver.Edge`

**Аттрибуты**:
- `driver_name` (str): Имя используемого веб-драйвера, по умолчанию `'edge'`.

**Методы**:
- `__init__`: Инициализирует драйвер Edge с указанными параметрами user-agent, опциями и режимом окна.
- `_payload`: Загружает исполнители для локаторов и JavaScript-сценариев.
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
    :type options: Optional[List[str]]
    :param window_mode: Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.)
    :type window_mode: Optional[str]
    """
```

**Назначение**: Инициализирует драйвер Edge WebDriver с заданными параметрами, такими как user-agent, опции и режим окна.

**Параметры**:
- `profile_name` (Optional[str]): Имя профиля пользователя. По умолчанию `None`.
- `user_agent` (Optional[str]): User-agent, который будет использоваться. Если `None`, генерируется случайный user-agent.
- `options` (Optional[List[str]]): Список опций Edge для передачи во время инициализации.
- `window_mode` (Optional[str]): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).
- `*args`: Произвольные позиционные аргументы.
- `**kwargs`: Произвольные именованные аргументы.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `WebDriverException`: Если не удается запустить Edge WebDriver.
- `Exception`: При возникновении общей ошибки во время запуска WebDriver.

**Как работает функция**:

1. **Инициализация User-Agent**: Если `user_agent` не предоставлен, генерируется случайный user-agent с использованием `fake_useragent`.
2. **Загрузка настроек**: Загружает настройки из файла `edge.json`, расположенного в каталоге `src/webdriver/edge`.
3. **Настройка опций Edge**:
   - Создается объект `EdgeOptions`.
   - Устанавливается user-agent.
   - Настраивается режим окна (kiosk, windowless, full_window) из параметров или конфигурации.
   - Добавляются пользовательские опции, переданные во время инициализации.
   - Добавляются опции из конфигурационного файла.
   - Добавляются заголовки из конфигурационного файла.
   - Настраивается директория профиля.
4. **Запуск WebDriver**:
   - Пытается запустить Edge WebDriver с заданными опциями и сервисом.
   - Вызывает метод `_payload` для загрузки исполнителей локаторов и JavaScript-сценариев.
5. **Обработка исключений**:
   - Ловит исключение `WebDriverException`, если не удается запустить WebDriver.
   - Ловит общее исключение `Exception` для обработки других ошибок.

```
Начало
  ↓
Загрузка настроек из edge.json
  ↓
Создание и настройка EdgeOptions
  ↓
Установка user-agent
  ↓
Установка режима окна (kiosk, windowless, full_window)
  ↓
Добавление пользовательских опций
  ↓
Добавление опций и заголовков из конфигурации
  ↓
Настройка директории профиля
  ↓
Запуск Edge WebDriver с заданными опциями
  ↓
Загрузка исполнителей через _payload()
  ↓
Конец
```

**Примеры**:

```python
from src.webdriver.edge.edge import Edge

# Пример с пользовательским user-agent
driver = Edge(user_agent='My Custom User Agent')

# Пример с дополнительными опциями
options = ['--disable-gpu', '--mute-audio']
driver = Edge(options=options)

# Пример с режимом окна kiosk
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
- `None`

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Нет`

**Как работает функция**:

1. **Инициализация JavaScript**: Создает экземпляр класса `JavaScript`, передавая ему текущий экземпляр драйвера `self`.
2. **Назначение JavaScript функций**: Присваивает атрибутам экземпляра драйвера функции из экземпляра `JavaScript`:
   - `self.get_page_lang = j.get_page_lang`
   - `self.ready_state = j.ready_state`
   - `self.get_referrer = j.ready_state`
   - `self.unhide_DOM_element = j.unhide_DOM_element`
   - `self.window_focus = j.window_focus`
3. **Инициализация ExecuteLocator**: Создает экземпляр класса `ExecuteLocator`, передавая ему текущий экземпляр драйвера `self`.
4. **Назначение функций ExecuteLocator**: Присваивает атрибутам экземпляра драйвера функции из экземпляра `ExecuteLocator`:
   - `self.execute_locator = execute_locator.execute_locator`
   - `self.get_webelement_as_screenshot = execute_locator.get_webelement_as_screenshot`
   - `self.get_webelement_by_locator = execute_locator.get_webelement_by_locator`
   - `self.get_attribute_by_locator = execute_locator.get_attribute_by_locator`
   - `self.send_message = self.send_key_to_webelement = execute_locator.send_message`

```
Начало
  ↓
Создание экземпляра JavaScript
  ↓
Присвоение функций JavaScript драйверу
  ↓
Создание экземпляра ExecuteLocator
  ↓
Присвоение функций ExecuteLocator драйверу
  ↓
Конец
```

**Примеры**:

```python
from src.webdriver.edge.edge import Edge

driver = Edge()
driver._payload()
# Теперь можно использовать методы, такие как driver.execute_locator
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
- `opts` (Optional[List[str]]): Список опций для добавления в Edge WebDriver. По умолчанию `None`.

**Возвращает**:
- `EdgeOptions`: Настроенный объект `EdgeOptions`.

**Вызывает исключения**:
- `Нет`

**Как работает функция**:

1. **Создание экземпляра EdgeOptions**: Создает новый экземпляр класса `EdgeOptions`.
2. **Добавление опций**: Если передан список опций `opts`, добавляет каждую опцию из списка в экземпляр `EdgeOptions`.
3. **Возврат EdgeOptions**: Возвращает настроенный объект `EdgeOptions`.

```
Начало
  ↓
Создание экземпляра EdgeOptions
  ↓
Если есть опции для добавления:
  → Добавление каждой опции в EdgeOptions
  ↓
Возврат EdgeOptions
  ↓
Конец
```

**Примеры**:

```python
from src.webdriver.edge.edge import Edge
from selenium.webdriver.edge.options import Options as EdgeOptions

driver = Edge()
options = ['--disable-gpu', '--mute-audio']
edge_options = driver.set_options(options)

# Теперь edge_options можно использовать при создании драйвера, например:
# driver = Edge(options=edge_options)
```

## Функции

Нет функций, определенных вне класса `Edge`.

## Примеры

Пример использования класса `Edge` в `if __name__ == "__main__":` показывает, как создать экземпляр драйвера Edge и открыть веб-страницу.

```python
if __name__ == "__main__":
    driver = Edge(window_mode='full_window')
    driver.get("https://www.example.com")