### Анализ кода модуля `src/webdriver/playwright/executor.py`

## Обзор

Этот модуль предоставляет класс `PlaywrightExecutor` для выполнения команд с использованием Playwright.

## Подробней

Модуль `src/webdriver/playwright/executor.py` предоставляет класс `PlaywrightExecutor`, который служит для выполнения действий с веб-элементами с использованием библиотеки Playwright. Он обрабатывает локаторы, события и обеспечивает гибкое взаимодействие с веб-страницами.

## Классы

### `PlaywrightExecutor`

**Описание**: Класс, который выполняет команды на основе предоставленных локаторов с использованием Playwright.

**Атрибуты**:

-   `driver` (Optional[object]): Экземпляр Playwright.
-   `browser_type` (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit').
-   `page` (Optional[Page]): Экземпляр страницы Playwright.
-   `config` (SimpleNamespace): Объект `SimpleNamespace`, содержащий настройки из файла конфигурации.

**Методы**:

-   `__init__(self, browser_type: str = 'chromium', **kwargs)`: Инициализирует `PlaywrightExecutor`.
-   `start(self) -> None`: Инициализирует Playwright и запускает экземпляр браузера.
-   `stop(self) -> None`: Закрывает браузер Playwright и останавливает его экземпляр.
-   `execute_locator(self, locator: Union[dict, SimpleNamespace], message: Optional[str] = None, typing_speed: float = 0, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = 'presence_of_element_located') -> Union[str, list, dict, Locator, bool, None]`: Выполняет действия с веб-элементом на основе предоставленного локатора.
-   `evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
-   `get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]`: Получает указанный атрибут из веб-элемента.
-   `get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]`: Получает веб-элемент, используя локатор.
-   `get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]`: Создает скриншот найденного веб-элемента.
-   `execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]`: Выполняет событие, связанное с локатором.
-   `send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.
-   `goto(self, url: str) -> None`: Переходит по указанному URL.

#### `__init__`

**Назначение**: Инициализирует экземпляр `PlaywrightExecutor`.

```python
def __init__(self, browser_type: str = 'chromium', **kwargs):
    """
    Initializes the Playwright executor.

    Args:
        browser_type: Type of browser to launch (e.g., 'chromium', 'firefox', 'webkit').
    """
    ...
```

**Параметры**:

-   `browser_type` (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit'). По умолчанию 'chromium'.
-   `**kwargs`: Дополнительные аргументы, передаваемые в конструктор.

**Как работает функция**:

1.  Устанавливает тип браузера, который будет использоваться.
2.  Загружает конфигурацию из файла `playwrid.json`, используя функцию `j_loads_ns`.

#### `start`

**Назначение**: Инициализирует Playwright и запускает экземпляр браузера.

```python
async def start(self) -> None:
    """
    Initializes Playwright and launches a browser instance.
    """
    ...
```

**Как работает функция**:

1.  Запускает Playwright, используя `async_playwright().start()`.
2.  Запускает браузер указанного типа (chromium, firefox, webkit) в безголовом режиме, передавая опции из конфигурации.
3.  Создает новую страницу в браузере.
4.  Логирует информацию об ошибках, используя `logger.critical`.

#### `stop`

**Назначение**: Закрывает браузер Playwright и останавливает его экземпляр.

```python
async def stop(self) -> None:
    """
    Closes Playwright browser and stops its instance.
    """
    ...
```

**Как работает функция**:

1.  Закрывает текущую страницу, если она существует.
2.  Останавливает экземпляр Playwright, если он существует.
3.  Логирует информацию об остановке Playwright, используя `logger.info`.
4.  Обрабатывает возможные исключения, логируя ошибки с использованием `logger.error`.

#### `execute_locator`

**Назначение**: Выполняет действия с веб-элементом на основе предоставленного локатора.

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
    Executes actions on a web element based on the provided locator.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        message: Optional message for events.
        typing_speed: Optional typing speed for events.
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').

    Returns:
         The result of the operation, which can be a string, list, dict, Locator, bool, or None.
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `message`: Опциональное сообщение для событий.
-   `typing_speed`: Опциональная скорость набора текста для событий.
-   `timeout`: Время ожидания для поиска элемента (в секундах).
-   `timeout_for_event`: Условие ожидания ("presence\_of\_element\_located", "visibility\_of\_all\_elements\_located").

**Возвращает**:

-   Результат операции, который может быть строкой, списком, словарем, `Locator`, булевым значением или `None`.

**Как работает функция**:

1.  Преобразует локатор в объект `SimpleNamespace`, если он представлен в виде словаря.
2.  Проверяет наличие атрибутов `attribute` и `selector` в локаторе. Если они отсутствуют, возвращает `None`.
3.  Определяет внутреннюю функцию `_parse_locator` для разбора и выполнения инструкций локатора.
4.  В зависимости от типа локатора выполняет различные действия:
    -   Если `locator.attribute` и `locator.by` являются строками, пытается получить атрибут элемента или выполнить событие.
    -   Если `locator.selector` и `locator.by` являются списками, обрабатывает локаторы как пары элементов.
5.  Возвращает результат выполнения операции.

#### `evaluate_locator`

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

```python
async def evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
    """
    Evaluates and processes locator attributes.

    Args:
        attribute: Attribute to evaluate (can be a string, list of strings, or a dictionary).

    Returns:
        The evaluated attribute, which can be a string, list of strings, or dictionary.
    """
    ...
```

**Параметры**:

-   `attribute`: Атрибут для вычисления (может быть строкой, списком строк или словарем).

**Возвращает**:

-   Вычисленный атрибут, который может быть строкой, списком строк или словарем.

**Как работает функция**:

1.  Определяет внутреннюю функцию `_evaluate` для вычисления одного атрибута, представленного строкой.
2.  Если атрибут является списком, применяет функцию `_evaluate` к каждому элементу списка.
3.  Если атрибут является строкой, применяет функцию `_evaluate` к строке.
4.  Возвращает вычисленный атрибут.

#### `get_attribute_by_locator`

**Назначение**: Получает указанный атрибут из веб-элемента.

```python
async def get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]:
    """
    Gets the specified attribute from the web element.

    Args:
        locator: Locator data (dict or SimpleNamespace).

    Returns:
        Attribute or None.
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).

**Возвращает**:

-   Значение атрибута или `None`.

**Как работает функция**:

1.  Преобразует локатор в объект `SimpleNamespace`, если он представлен в виде словаря.
2.  Получает веб-элемент, используя функцию `get_webelement_by_locator`.
3.  Определяет внутреннюю функцию `_parse_dict_string` для преобразования строки типа `'{attr1:attr2}'` в словарь.
4.  Определяет внутреннюю функцию `_get_attribute` для получения атрибута из `Locator`.
5.  Определяет внутреннюю функцию `_get_attributes_from_dict` для получения нескольких атрибутов на основе словаря.
6.  В зависимости от типа атрибута извлекает его значение из `WebElement`.

#### `get_webelement_by_locator`

**Назначение**: Получает веб-элемент, используя локатор.

```python
async def get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]:
    """
    Gets a web element using the locator.

    Args:
        locator: Locator data (dict or SimpleNamespace).

    Returns:
        Playwright Locator
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).

**Возвращает**:

-   `Locator`: Playwright Locator или список Locator.

**Как работает функция**:

1.  Преобразует локатор в объект `SimpleNamespace`, если он представлен в виде словаря.
2.  В зависимости от значения `locator.by.upper()` выполняет поиск элемента с использованием соответствующих методов Playwright:
    -   Если `locator.by.upper()` равен "XPATH", использует `self.page.locator(f'xpath={locator.selector}')`.
    -   В противном случае использует `self.page.locator(locator.selector)`.
3.  В зависимости от значения `locator.if_list` возвращает один элемент, список элементов или их часть.

#### `get_webelement_as_screenshot`

**Назначение**: Создает снимок экрана найденного веб-элемента.

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
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `webelement`: Веб-элемент Locator.

**Возвращает**:

-   Снимок экрана в байтах или `None`.

**Как работает функция**:

1.  Преобразует локатор в объект `SimpleNamespace`, если он представлен в виде словаря.
2.  Получает веб-элемент, используя функцию `get_webelement_by_locator`, если `webelement` не был передан.
3.  Если элемент не найден, возвращает `None`.
4.  Делает снимок экрана веб-элемента, используя `webelement.screenshot()`.

#### `execute_event`

**Назначение**: Выполняет событие, связанное с локатором.

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
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `message`: Опциональное сообщение для событий.
-   `typing_speed`: Опциональная скорость набора текста для событий.

**Возвращает**:

-   Статус выполнения.

**Как работает функция**:

1.  Преобразует локатор в объект `SimpleNamespace`, если он представлен в виде словаря.
2.  Разделяет строку события на отдельные события, используя разделитель ";".
3.  Получает веб-элемент, используя функцию `get_webelement_by_locator`.
4.  Выполняет цикл по каждому событию:
    -   Если событие `click()`, пытается кликнуть на элемент.
    -   Если событие `pause()`, приостанавливает выполнение на указанное время.
    -   Если событие `upload_media()`, загружает медиафайл, используя `element.set_input_files()`.
    -   Если событие `screenshot()`, делает скриншот элемента.
    -   Если событие `clear()`, очищает элемент.
    -   Если событие `send_keys()`, отправляет указанные клавиши, используя `element.type()`.
    -   Если событие `type()`, отправляет сообщение, печатая каждый символ с указанной скоростью.

#### `send_message`

**Назначение**: Отправляет сообщение веб-элементу.

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
    ...
```

**Параметры**:

-   `locator`: Информация о расположении элемента на странице.
-   `message`: Сообщение, которое нужно отправить веб-элементу.
-   `typing_speed`: Скорость набора текста в секундах.

**Возвращает**:

-   `bool`: `True`, если сообщение было отправлено успешно, `False` - в противном случае.

**Как работает функция**:

1.  Определяет внутреннюю функцию `type_message` для набора сообщения в веб-элементе.
2.  Получает веб-элемент, используя функцию `get_webelement_by_locator`.
3.  Использует метод `element.type()` для отправки текста.
    - Если указана скорость набора текста (typing_speed), то используется цикл, чтобы отправлять символы по одному с указанной задержкой между каждым символом.

#### `goto`

**Назначение**: Переходит по указанному URL.

```python
async def goto(self, url: str) -> None:
    """
    Navigates to a specified URL.

    Args:
        url: URL to navigate to.
    """
    ...
```

**Параметры**:

-   `url` (str): URL для перехода.

**Как работает функция**:

1.  Использует метод `self.page.goto(url)` для перехода по указанному URL.
2.  Обрабатывает исключения, логируя ошибки с использованием `logger.error`.

## Переменные модуля

-   В данном модуле отсутствуют глобальные переменные, за исключением импортированных модулей.

## Пример использования

```python
from src.webdriver import Driver
from src.webdriver.playwright import Playwright
from src.webdriver.playwright.executor import PlaywrightExecutor
from types import SimpleNamespace
import asyncio

# Инициализация драйвера
driver = Driver(Playwright)
await driver.start()
executor = PlaywrightExecutor(driver.driver)

# Пример локатора
locator = SimpleNamespace(
    by="xpath",
    selector="//input[@name='q']",
    attribute=None,
    event="type(Привет, мир!)",
    mandatory=True
)

async def main():
    # Переход на страницу
    await driver.goto("https://www.google.com")

    # Выполнение события с использованием локатора
    result = await executor.execute_locator(locator, typing_speed=0.1)
    print(f"Результат выполнения: {result}")

if __name__ == "__main__":
    asyncio.run(main())
await driver.stop()
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/webdriver/playwright/executor.py` зависит от библиотеки `playwright` для управления браузером, от модуля `src.logger.logger` для логирования и от модуля `src.utils.jjson` для загрузки конфигурации.
-   Он также зависит от других модулей в рамках `src.webdriver`, таких как `driver.py`.