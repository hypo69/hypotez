### Анализ кода модуля `src/webdriver/executor.py`

## Обзор

Этот модуль предоставляет функциональность для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

## Подробней

Модуль `src/webdriver/executor.py` является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath), выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Классы

### `ExecuteLocator`

**Описание**: Класс, который обрабатывает взаимодействие с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Атрибуты**:

-   `driver` (Optional[object]): Экземпляр Selenium WebDriver.
-   `actions` (ActionChains): Объект `ActionChains` для выполнения последовательности действий.
-   `mode` (str): Режим работы (по умолчанию `"debug"`).

**Методы**:

-   `__init__(self, webdriver_cls, *args, **kwargs)`: Инициализирует экземпляр класса `ExecuteLocator`.
-   `execute_locator(self, locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = "presence_of_element_located", message: Optional[str] = None, typing_speed: Optional[float] = 0) -> Optional[str | list | dict | WebElement | bool]`: Выполняет действия над веб-элементом на основе предоставленного локатора.
-   `_evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
-   `get_attribute_by_locator(self, locator: SimpleNamespace | dict, timeout: Optional[float] = 0, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0) -> Optional[WebElement | list[WebElement]]`: Извлекает атрибуты из веб-элемента или списка веб-элементов.
-   `get_webelement_by_locator(self, locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: str = "presence_of_element_located") -> Optional[WebElement | List[WebElement]]`: Получает веб-элемент или список элементов на основе предоставленного локатора.
-   `get_webelement_as_screenshot(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0, webelement: Optional[WebElement] = None) -> Optional[BinaryIO]`: Создает снимок экрана найденного веб-элемента.
-   `execute_event(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> Optional[str | list[str] | bytes | list[bytes] | bool]`: Выполняет событие, связанное с локатором.
-   `send_message(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.

#### `__init__`

**Назначение**: Инициализирует экземпляр класса `ExecuteLocator`.

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
    if not hasattr(webdriver_cls, 'get'):
        raise TypeError('`webdriver_cls` должен быть допустимым классом WebDriver.')
    self.driver = webdriver_cls(*args, **kwargs)
```

**Параметры**:

-   `driver` (Optional[object]): Экземпляр Selenium WebDriver.
-   `actions` (ActionChains): Объект `ActionChains` для выполнения последовательности действий.
-   `mode` (str): Режим работы (по умолчанию `"debug"`).

**Как работает функция**:

1.  Инициализирует атрибут `actions` объектом `ActionChains`, связанным с переданным экземпляром драйвера.

#### `execute_locator`

**Назначение**: Выполняет действия над веб-элементом на основе предоставленного локатора.

```python
async def execute_locator(
    self,
    locator:  dict | SimpleNamespace,
    timeout: Optional[float] = 0,
    timeout_for_event: Optional[str] = "presence_of_element_located",
    message: Optional[str] = None,
    typing_speed: Optional[float] = 0,
) ->  Optional[str | list | dict | WebElement | bool]:
    """
    Executes actions on a web element based on the provided locator.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Optional message for actions like send_keys or type.
        typing_speed: Typing speed for send_keys events (seconds).

    Returns:
        The result of the operation, which can be a string, list, dict, WebElement, bool, or None.
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `timeout`: Время ожидания для поиска элемента (в секундах).
-   `timeout_for_event`: Условие ожидания ("presence\_of\_element\_located", "visibility\_of\_all\_elements\_located").
-   `message`: Опциональное сообщение для действий, таких как send\_keys или type.
-   `typing_speed`: Скорость набора текста для событий send\_keys (в секундах).

**Возвращает**:

-   Результат операции, который может быть строкой, списком, словарем, WebElement, bool или None.

**Как работает функция**:

1.  Преобразует локатор в объект `SimpleNamespace`, если он представлен в виде словаря.
2.  Проверяет наличие атрибутов `attribute` и `selector` в локаторе. Если они отсутствуют, возвращает `None`.
3.  Определяет внутреннюю функцию `_parse_locator` для разбора и выполнения инструкций локатора.
4.  В зависимости от типа локатора выполняет различные действия:
    -   Если `locator.by` является строкой, пытается получить атрибут элемента по указанному локатору или выполнить событие.
    -   Если `locator.by` и `locator.selector` являются списками, обрабатывает локаторы как пары элементов.
5.  Возвращает результат выполнения операции.

#### `_evaluate_locator`

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

```python
def _evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
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

**Назначение**: Извлекает атрибуты из веб-элемента или списка веб-элементов.

```python
async def get_attribute_by_locator(
    self,
    locator: SimpleNamespace | dict,
    timeout: Optional[float] = 0,
    timeout_for_event: str = "presence_of_element_located",
    message: Optional[str] = None,
    typing_speed: float = 0,
) -> Optional[WebElement | list[WebElement]]:
    """
    Retrieves attributes from a web element or a list of web elements.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Not used in this function.
        typing_speed: Not used in this function.

    Returns:
        The attribute value(s) as a WebElement, list of WebElements, or None if not found.
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `timeout`: Время ожидания для поиска элемента (в секундах).
-   `timeout_for_event`: Условие ожидания ("presence\_of\_element\_located", "visibility\_of\_all\_elements\_located").
-   `message`: Не используется в этой функции.
-   `typing_speed`: Не используется в этой функции.

**Возвращает**:

-   Значение атрибута(ов) как WebElement, список WebElements или None, если не найдено.

**Как работает функция**:

1.  Получает веб-элемент или список элементов, используя функцию `get_webelement_by_locator`.
2.  Если элемент не найден и локатор является обязательным, логирует отладочное сообщение и возвращает `None`.
3.  Определяет внутреннюю функцию `_parse_dict_string` для преобразования строки типа `'{attr1:attr2}'` в словарь.
4.  Определяет внутреннюю функцию `_get_attributes_from_dict` для извлечения значений атрибутов из `WebElement` на основе словаря.
5.  Если `locator.attribute` является строкой, начинающейся с "{", преобразует ее в словарь и извлекает значения атрибутов на основе этого словаря.
6.  В противном случае извлекает значение атрибута непосредственно из `WebElement`.

#### `get_webelement_by_locator`

**Назначение**: Получает веб-элемент или список элементов на основе предоставленного локатора.

```python
async def get_webelement_by_locator(
    self,
    locator: dict | SimpleNamespace,
    timeout: Optional[float] = 0,
    timeout_for_event: str = "presence_of_element_located",
) -> Optional[WebElement | List[WebElement]]:
    """
    Retrieves a web element or list of elements based on the provided locator.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').

    Returns:
       WebElement, list of WebElements, or None if not found.
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `timeout`: Время ожидания для поиска элемента (в секундах).
-   `timeout_for_event`: Условие ожидания ("presence\_of\_element\_located", "visibility\_of\_all\_elements\_located").

**Возвращает**:

-   `WebElement`, список `WebElements` или `None`, если не найдено.

**Как работает функция**:

1.  Принимает данные локатора и параметры таймаута.
2.  В зависимости от наличия таймаута использует либо `driver.find_elements` для немедленного поиска элементов, либо `WebDriverWait` с условием ожидания для поиска элементов в течение заданного времени.
3.  Вызывает внутреннюю функцию `_parse_elements_list` для фильтрации списка элементов на основе атрибута `if_list` в локаторе.
4.  Логирует информацию об ошибках, используя `logger.error`.

#### `get_webelement_as_screenshot`

**Назначение**: Создает снимок экрана найденного веб-элемента.

```python
async def get_webelement_as_screenshot(
    self,
    locator: SimpleNamespace | dict,
    timeout: float = 5,
    timeout_for_event: str = "presence_of_element_located",
    message: Optional[str] = None,
    typing_speed: float = 0,
    webelement: Optional[WebElement] = None,
) -> Optional[BinaryIO]:
    """
    Takes a screenshot of the located web element.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Not used in this function.
        typing_speed: Not used in this function.
        webelement: Optional pre-fetched web element.

    Returns:
       BinaryIO stream of the screenshot or None if failed.
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `timeout`: Время ожидания для поиска элемента (в секундах).
-   `timeout_for_event`: Условие ожидания ("presence\_of\_element\_located", "visibility\_of\_all\_elements\_located").
-   `message`: Не используется в этой функции.
-   `typing_speed`: Не используется в этой функции.
-   `webelement`: Опциональный предварительно полученный веб-элемент.

**Возвращает**:

-   Бинарный поток `BinaryIO` снимка экрана или `None`, если не удалось.

**Как работает функция**:

1.  Получает веб-элемент, используя функцию `get_webelement_by_locator`.
2.  Если элемент не найден, возвращает `None`.
3.  Делает снимок экрана веб-элемента, используя `webelement.screenshot_as_png`.
4.  Логирует информацию об ошибках, используя `logger.error`.

#### `execute_event`

**Назначение**: Выполняет событие, связанное с локатором.

```python
async def execute_event(
    self,
    locator: SimpleNamespace | dict,
    timeout: float = 5,
    timeout_for_event: str = "presence_of_element_located",
    message: str = None,
    typing_speed: float = 0,
) -> Optional[str | list[str] | bytes | list[bytes] | bool]:
    """
    Executes an event associated with a locator.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Optional message to send with the event.
        typing_speed: Typing speed for send_keys events (seconds).

    Returns:
        The result of the event execution (str, list of str, bytes, list of bytes, or bool).
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `timeout`: Время ожидания для поиска элемента (в секундах).
-   `timeout_for_event`: Условие ожидания ("presence\_of\_element\_located", "visibility\_of\_all\_elements\_located").
-   `message`: Опциональное сообщение для отправки с событием.
-   `typing_speed`: Скорость набора текста для событий `send_keys` (в секундах).

**Возвращает**:

-   Результат выполнения события (str, список str, bytes, список bytes или bool).

**Как работает функция**:

1.  Преобразует локатор в объект `SimpleNamespace`, если он представлен в виде словаря.
2.  Разделяет строку события на отдельные события, используя разделитель ";".
3.  Получает веб-элемент, используя функцию `get_webelement_by_locator`.
4.  Выполняет цикл по каждому событию:
    -   Если событие `click()`, пытается кликнуть на элемент.
    -   Если событие `pause()`, приостанавливает выполнение на указанное время.
    -   Если событие `upload_media()`, отправляет медиафайл, используя `send_keys`.
    -   Если событие `screenshot()`, делает скриншот элемента.
    -   Если событие `clear()`, очищает элемент.
    -   Если событие `send_keys()`, отправляет указанные клавиши.
    -   Если событие `type()`, отправляет сообщение, печатая каждый символ с указанной скоростью.
5.  Логирует информацию об ошибках, используя `logger.error`.

#### `send_message`

**Назначение**: Отправляет сообщение веб-элементу.

```python
async def send_message(
    self,
    locator: SimpleNamespace | dict,
    timeout: float = 5,
    timeout_for_event: str = "presence_of_element_located",
    message: str = None,
    typing_speed: float = 0,
) -> bool:
    """
    Sends a message to a web element.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Message to send to the web element.
        typing_speed: Typing speed for send_keys events (seconds).

    Returns:
        True if the message was sent successfully, False otherwise.
    """
    ...
```

**Параметры**:

-   `locator`: Данные локатора (словарь или SimpleNamespace).
-   `timeout`: Время ожидания для поиска элемента (в секундах).
-   `timeout_for_event`: Условие ожидания ("presence\_of\_element\_located", "visibility\_of\_all\_elements\_located").
-   `message`: Сообщение для отправки веб-элементу.
-   `typing_speed`: Скорость набора текста (в секундах).

**Возвращает**:

-   `bool`: `True`, если сообщение было отправлено успешно, `False` - в противном случае.

**Как работает функция**:

1.  Определяет внутреннюю функцию `type_message` для набора сообщения в веб-элементе.
2.  Получает веб-элемент, используя функцию `get_webelement_by_locator`.
3.  Использует объект `ActionChains` для перемещения к элементу и вызова функции `type_message` для набора текста.
4.  Логирует информацию об ошибках, используя `logger.error`.

## Переменные модуля

-   Отсутствуют.

## Пример использования

```python
from src.webdriver import Driver
from selenium.webdriver import Chrome
from src.webdriver.executor import ExecuteLocator
from types import SimpleNamespace
from selenium.webdriver.common.by import By
import asyncio

# Инициализация драйвера
driver = Driver(Chrome)
executor = ExecuteLocator(driver)

# Пример локатора
locator = SimpleNamespace(
    by=By.ID,
    selector="myTextField",
    attribute=None,
    event="type(Hello, world!)",
    mandatory=True
)

async def main():
    # Переход на страницу
    driver.get("https://example.com")

    # Выполнение события с использованием локатора
    result = await executor.execute_locator(locator, typing_speed=0.1)
    print(f"Результат выполнения: {result}")

asyncio.run(main())
driver.quit()
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/webdriver/executor.py` зависит от библиотеки `selenium` для взаимодействия с веб-элементами, от модуля `header` для получения пути к файлу настроек (хотя header не используется напрямую) и от модуля `src.logger.logger` для логирования.
- Он также зависит от других модулей в рамках `src.webdriver`, таких как `driver.py`.