# Модуль `executor.py`

## Обзор

Модуль `executor.py` предоставляет функциональность для взаимодействия с веб-элементами с использованием Playwright на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для автоматизации взаимодействия с веб-страницами с использованием Playwright. Он включает в себя класс `PlaywrightExecutor`, который предоставляет методы для запуска и остановки браузера, выполнения действий с веб-элементами на основе локаторов, получения атрибутов элементов, выполнения событий (например, кликов, ввода текста) и навигации по URL. Модуль использует библиотеку Playwright для управления браузером и выполнения действий на веб-странице.

## Классы

### `PlaywrightExecutor`

**Описание**: Класс `PlaywrightExecutor` выполняет команды на основе локаторов в стиле executor, используя Playwright.

**Принцип работы**:
1.  Инициализируется с указанием типа браузера (по умолчанию `chromium`) и дополнительными аргументами.
2.  Запускает браузер Playwright с помощью метода `start`, создавая новую страницу.
3.  Останавливает браузер Playwright с помощью метода `stop`, закрывая страницу и останавливая драйвер.
4.  Выполняет действия с веб-элементами с использованием метода `execute_locator`, который принимает локатор и выполняет соответствующие действия (например, получение атрибута, выполнение события).
5.  Предоставляет методы для получения атрибутов веб-элементов (`get_attribute_by_locator`), получения веб-элементов по локатору (`get_webelement_by_locator`), выполнения скриншотов веб-элементов (`get_webelement_as_screenshot`), выполнения событий (`execute_event`), отправки сообщений (`send_message`) и навигации по URL (`goto`).

**Методы**:

*   `__init__(self, browser_type: str = 'chromium', **kwargs)`: Инициализирует экземпляр класса `PlaywrightExecutor`.
*   `start(self) -> None`: Запускает браузер Playwright.
*   `stop(self) -> None`: Останавливает браузер Playwright.
*   `execute_locator(self, locator: Union[dict, SimpleNamespace], message: Optional[str] = None, typing_speed: float = 0, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = 'presence_of_element_located') -> Union[str, list, dict, Locator, bool, None]`: Выполняет действия с веб-элементом на основе предоставленного локатора.
*   `evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
*   `get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]`: Получает указанный атрибут из веб-элемента.
*   `get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]`: Получает веб-элемент с использованием локатора.
*   `get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]`: Делает скриншот найденного веб-элемента.
*   `execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]`: Выполняет событие, связанное с локатором.
*   `send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.
*   `goto(self, url: str) -> None`: Переходит по указанному URL.

## Функции

### `start`

```python
async def start(self) -> None:
    """
    Инициализирует Playwright и запускает экземпляр браузера.
    """
```

**Назначение**: Инициализирует Playwright и запускает браузер.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.

**Возвращает**:

*   `None`

**Как работает функция**:

1.  Инициализирует Playwright с помощью `async_playwright().start()`.
2.  Запускает браузер, используя тип браузера, указанный в `self.browser_type`.
3.  Создает новую страницу в браузере.

```
    Начало
    │
    ├─── Запуск Playwright
    │
    ├─── Запуск браузера
    │
    └─── Создание новой страницы
    │
    Конец
```

**Примеры**:

```python
executor = PlaywrightExecutor(browser_type='chromium')
await executor.start()
```

### `stop`

```python
async def stop(self) -> None:
    """
    Закрывает браузер Playwright и останавливает его экземпляр.
    """
```

**Назначение**: Закрывает браузер Playwright и останавливает его экземпляр.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.

**Возвращает**:

*   `None`

**Как работает функция**:

1.  Проверяет, существует ли страница, и закрывает ее, если она существует.
2.  Проверяет, существует ли драйвер, и останавливает его, если он существует.
3.  Устанавливает `self.driver` в `None`.

```
    Начало
    │
    ├─── Проверка наличия страницы
    │   └─── Закрытие страницы (если есть)
    │
    ├─── Проверка наличия драйвера
    │   └─── Остановка драйвера (если есть)
    │
    └─── Установка self.driver в None
    │
    Конец
```

**Примеры**:

```python
executor = PlaywrightExecutor(browser_type='chromium')
await executor.start()
await executor.stop()
```

### `execute_locator`

```python
async def execute_locator(
        self,
        locator: Union[dict, SimpleNamespace],
        message: Optional[str] = None,
        typing_speed: float = 0,
        timeout: Optional[float] = 0,
        timeout_for_event: Optional[str] = 'presence_of_element_located',
) -> Union[str, list, dict, Locator, bool, None]:
    """
    Выполняет действия с веб-элементом на основе предоставленного локатора.

    Args:
        locator: Данные локатора (dict или SimpleNamespace).
        message: Необязательное сообщение для событий.
        typing_speed: Необязательная скорость печати для событий.
        timeout: Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

    Returns:
         Результат операции, который может быть строкой, списком, словарем, Locator, bool или None.
    """
```

**Назначение**: Выполняет действия с веб-элементом на основе предоставленного локатора.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `locator` (Union[dict, SimpleNamespace]): Данные локатора.
*   `message` (Optional[str]): Необязательное сообщение для событий.
*   `typing_speed` (float): Необязательная скорость печати для событий.
*   `timeout` (Optional[float]): Время ожидания для обнаружения элемента (в секундах).
*   `timeout_for_event` (Optional[str]): Условие ожидания.

**Возвращает**:

*   `Union[str, list, dict, Locator, bool, None]`: Результат операции.

**Внутренние функции**:

#### `_parse_locator`

```python
async def _parse_locator(
        locator: SimpleNamespace, message: Optional[str]
) -> Union[str, list, dict, Locator, bool, None]:
    """Parses and executes locator instructions."""
```

**Назначение**: Разбирает и выполняет инструкции локатора.

**Параметры**:

*   `locator` (SimpleNamespace): Данные локатора.
*   `message` (Optional[str]): Необязательное сообщение для событий.

**Возвращает**:

*   `Union[str, list, dict, Locator, bool, None]`: Результат операции.

**Как работает функция**:

1.  Преобразует входной `locator` в `SimpleNamespace`, если он является словарем.
2.  Проверяет, что локатор содержит атрибут `selector` и `by`. Если нет, возвращает `None`.
3.  Определяет внутреннюю асинхронную функцию `_parse_locator`, которая рекурсивно обрабатывает локаторы.
4.  В зависимости от типа и содержимого локатора, выполняет различные действия, такие как получение атрибута, выполнение события или получение веб-элемента.
5.  Возвращает результат операции.

```
Начало
│
├─── Проверка типа локатора
│   └─── Преобразование в SimpleNamespace (если dict)
│
├─── Проверка наличия атрибутов selector и by
│   └─── Возврат None (если отсутствуют)
│
├─── Определение внутренней функции _parse_locator
│   │
│   └─── В зависимости от атрибутов локатора:
│       ├─── Получение атрибута
│       ├─── Выполнение события
│       └─── Получение веб-элемента
│
└─── Возврат результата
│
Конец
```

**Примеры**:

```python
locator_data = {"by": "XPATH", "selector": "//button", "event": "click()"}
result = await executor.execute_locator(locator_data)
```

### `evaluate_locator`

```python
async def evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
    """
    Evaluates and processes locator attributes.

    Args:
        attribute: Attribute to evaluate (can be a string, list of strings, or a dictionary).

    Returns:
        The evaluated attribute, which can be a string, list of strings, or dictionary.
    """
```

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `attribute` (str | List[str] | dict): Атрибут для вычисления.

**Возвращает**:

*   `Optional[str | List[str] | dict]`: Вычисленный атрибут.

**Внутренние функции**:

#### `_evaluate`

```python
async def _evaluate(attr: str) -> Optional[str]:
    return attr
```

**Назначение**: Возвращает переданный атрибут.

**Параметры**:

*   `attr` (str): Атрибут для возврата.

**Возвращает**:

*   `Optional[str]`: Возвращает переданный атрибут.

**Как работает функция**:

1.  Определяет внутреннюю асинхронную функцию `_evaluate`, которая просто возвращает переданный атрибут.
2.  Если атрибут является списком, вызывает `_evaluate` для каждого элемента списка и возвращает список результатов.
3.  В противном случае вызывает `_evaluate` для атрибута и возвращает результат.

```
Начало
│
├─── Определение внутренней функции _evaluate
│   │
│   └─── Возврат переданного атрибута
│
├─── Проверка типа атрибута
│   ├─── Если список:
│   │   └─── Вызов _evaluate для каждого элемента
│   └─── Иначе:
│       └─── Вызов _evaluate для атрибута
│
└─── Возврат результата
│
Конец
```

**Примеры**:

```python
attribute = "some_attribute"
evaluated_attribute = await executor.evaluate_locator(attribute)
```

### `get_attribute_by_locator`

```python
async def get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]:
    """
    Gets the specified attribute from the web element.

    Args:
        locator: Locator data (dict or SimpleNamespace).

    Returns:
        Attribute or None.
    """
```

**Назначение**: Получает указанный атрибут из веб-элемента.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `locator` (dict | SimpleNamespace): Данные локатора.

**Возвращает**:

*   `Optional[str | List[str] | dict]`: Атрибут или None.

**Внутренние функции**:

#### `_parse_dict_string`

```python
def _parse_dict_string(attr_string: str) -> dict | None:
    """Parses a string like '{attr1:attr2}' into a dictionary."""
```

**Назначение**: Преобразует строку типа '{attr1:attr2}' в словарь.

**Параметры**:

*   `attr_string` (str): Строка для преобразования.

**Возвращает**:

*   `dict | None`: Словарь или None.

**Как работает функция**:

1.  Пытается преобразовать строку в словарь, разделяя ее по символам ':' и ','.
2.  В случае ошибки логирует сообщение и возвращает None.

#### `_get_attribute`

```python
async def _get_attribute(el: Locator, attr: str) -> Optional[str]:
    """Retrieves a single attribute from a Locator."""
```

**Назначение**: Извлекает один атрибут из Locator.

**Параметры**:

*   `el` (Locator): Locator элемента.
*   `attr` (str): Название атрибута.

**Возвращает**:

*   `Optional[str]`: Значение атрибута или None.

**Как работает функция**:

1.  Пытается получить значение атрибута из элемента Locator.
2.  В случае ошибки логирует сообщение и возвращает None.

#### `_get_attributes_from_dict`

```python
async def _get_attributes_from_dict(element: Locator, attr_dict: dict) -> dict:
    """Retrieves multiple attributes based on a dictionary."""
```

**Назначение**: Извлекает несколько атрибутов на основе словаря.

**Параметры**:

*   `element` (Locator): Locator элемента.
*   `attr_dict` (dict): Словарь атрибутов.

**Возвращает**:

*   `dict`: Словарь значений атрибутов.

**Как работает функция**:

1.  Проходит по словарю атрибутов и получает значение каждого атрибута из элемента Locator.
2.  Возвращает словарь значений атрибутов.

**Как работает функция `get_attribute_by_locator`**:

1.  Преобразует входной `locator` в `SimpleNamespace`, если он является словарем.
2.  Получает веб-элемент с помощью `self.get_webelement_by_locator(locator)`.
3.  В зависимости от типа атрибута (строка или словарь), выполняет различные действия, такие как получение одного атрибута или получение нескольких атрибутов.
4.  Возвращает результат операции.

```
Начало
│
├─── Проверка типа локатора
│   └─── Преобразование в SimpleNamespace (если dict)
│
├─── Получение веб-элемента
│
├─── Проверка типа атрибута
│   ├─── Если строка:
│   │   └─── Получение атрибута
│   └─── Если словарь:
│       └─── Получение нескольких атрибутов
│
└─── Возврат результата
│
Конец
```

**Примеры**:

```python
locator_data = {"by": "XPATH", "selector": "//button", "attribute": "class"}
attribute_value = await executor.get_attribute_by_locator(locator_data)
```

### `get_webelement_by_locator`

```python
async def get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]:
    """
    Gets a web element using the locator.

    Args:
        locator: Locator data (dict or SimpleNamespace).

    Returns:
        Playwright Locator
    """
```

**Назначение**: Получает веб-элемент с использованием локатора.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `locator` (dict | SimpleNamespace): Данные локатора.

**Возвращает**:

*   `Optional[Locator | List[Locator]]`: Playwright Locator.

**Как работает функция**:

1.  Преобразует входной `locator` в `SimpleNamespace`, если он является словарем.
2.  В зависимости от значения `locator.by`, использует `self.page.locator` для поиска элемента.
3.  В зависимости от значения `locator.if_list`, возвращает один элемент или список элементов.

```
Начало
│
├─── Преобразование локатора в SimpleNamespace (если dict)
│
├─── Определение метода поиска элемента (XPATH или CSS)
│
├─── В зависимости от if_list:
│   ├─── 'all': Возвращает все элементы
│   ├─── 'first': Возвращает первый элемент
│   ├─── 'last': Возвращает последний элемент
│   ├─── 'even': Возвращает элементы с четными индексами
│   ├─── 'odd': Возвращает элементы с нечетными индексами
│   ├─── list: Возвращает элементы по индексам из списка
│   ├─── int: Возвращает элемент по указанному индексу
│   └─── Иначе: Возвращает Locator
│
└─── Возврат результата
│
Конец
```

**Примеры**:

```python
locator_data = {"by": "XPATH", "selector": "//button"}
element = await executor.get_webelement_by_locator(locator_data)
```

### `get_webelement_as_screenshot`

```python
async def get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]:
    """
    Takes a screenshot of the located web element.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        webelement: The web element Locator.

    Returns:
         Screenshot in bytes or None.
    """
```

**Назначение**: Делает скриншот найденного веб-элемента.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `locator` (dict | SimpleNamespace): Данные локатора.
*   `webelement` (Optional[Locator]): Веб-элемент Locator.

**Возвращает**:

*   `Optional[bytes]`: Скриншот в байтах или None.

**Как работает функция**:

1.  Преобразует входной `locator` в `SimpleNamespace`, если он является словарем.
2.  Если `webelement` не предоставлен, пытается получить его с помощью `self.get_webelement_by_locator(locator)`.
3.  Делает скриншот веб-элемента с помощью `webelement.screenshot()`.

```
Начало
│
├─── Преобразование локатора в SimpleNamespace (если dict)
│
├─── Получение веб-элемента (если не предоставлен)
│
├─── Создание скриншота элемента
│
└─── Возврат результата
│
Конец
```

**Примеры**:

```python
locator_data = {"by": "XPATH", "selector": "//button"}
screenshot = await executor.get_webelement_as_screenshot(locator_data)
```

### `execute_event`

```python
async def execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]:
    """
    Executes the event associated with the locator.

     Args:
        locator: Locator data (dict or SimpleNamespace).
        message: Optional message for events.
        typing_speed: Optional typing speed for events.

    Returns:
       Execution status.
    """
```

**Назначение**: Выполняет событие, связанное с локатором.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `locator` (dict | SimpleNamespace): Данные локатора.
*   `message` (Optional[str]): Необязательное сообщение для событий.
*   `typing_speed` (float): Необязательная скорость печати для событий.

**Возвращает**:

*   `Union[str, List[str], bytes, List[bytes], bool]`: Статус выполнения.

**Как работает функция**:

1.  Преобразует входной `locator` в `SimpleNamespace`, если он является словарем.
2.  Получает веб-элемент с помощью `self.get_webelement_by_locator(locator)`.
3.  Разделяет строку `locator.event` на отдельные события.
4.  Выполняет каждое событие в цикле.

```
Начало
│
├─── Преобразование локатора в SimpleNamespace (если dict)
│
├─── Получение веб-элемента
│
├─── Разделение строки events
│
├─── Цикл по events:
│   ├─── click()
│   ├─── pause()
│   ├─── upload_media()
│   ├─── screenshot()
│   ├─── clear()
│   ├─── send_keys()
│   └─── type()
│
└─── Возврат результата
│
Конец
```

**Примеры**:

```python
locator_data = {"by": "XPATH", "selector": "//button", "event": "click()"}
execution_status = await executor.execute_event(locator_data)
```

### `send_message`

```python
async def send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool:
    """Sends a message to a web element.

    Args:
         locator: Information about the element's location on the page.
         message: The message to be sent to the web element.
         typing_speed: Speed of typing the message in seconds.

    Returns:
        Returns `True` if the message was sent successfully, `False` otherwise.
    """
```

**Назначение**: Отправляет сообщение веб-элементу.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `locator` (dict | SimpleNamespace): Данные локатора.
*   `message` (str): Сообщение для отправки.
*   `typing_speed` (float): Скорость печати сообщения в секундах.

**Возвращает**:

*   `bool`: True, если сообщение отправлено успешно, False в противном случае.

**Как работает функция**:

1.  Преобразует входной `locator` в `SimpleNamespace`, если он является словарем.
2.  Получает веб-элемент с помощью `self.get_webelement_by_locator(locator)`.
3.  Отправляет сообщение веб-элементу с указанной скоростью печати.

```
Начало
│
├─── Преобразование локатора в SimpleNamespace (если dict)
│
├─── Получение веб-элемента
│
├─── Отправка сообщения с учетом typing_speed
│
└─── Возврат результата
│
Конец
```

**Примеры**:

```python
locator_data = {"by": "XPATH", "selector": "//input"}
message = "Hello, world!"
send_status = await executor.send_message(locator_data, message)
```

### `goto`

```python
async def goto(self, url: str) -> None:
    """
    Navigates to a specified URL.

    Args:
        url: URL to navigate to.
    """
```

**Назначение**: Переходит по указанному URL.

**Параметры**:

*   `self` (PlaywrightExecutor): Экземпляр класса `PlaywrightExecutor`.
*   `url` (str): URL для перехода.

**Возвращает**:

*   `None`

**Как работает функция**:

1.  Использует `self.page.goto(url)` для перехода по указанному URL.

```
Начало
│
├─── Переход по URL
│
└─── Конец
│
Конец
```

**Примеры**:

```python
url = "https://www.example.com"
await executor.goto(url)