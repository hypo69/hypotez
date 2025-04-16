### Анализ кода модуля `hypotez/src/webdriver/executor.py`

## Обзор

Этот модуль предоставляет функциональность для взаимодействия с веб-элементами, используя Selenium, на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

Этот модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath), выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Классы

### `ExecuteLocator`

```python
@dataclass
class ExecuteLocator:
    """
    Handles web element interaction using Selenium based on provided locators.
    """

    driver: Optional[object] = None
    actions: ActionChains = field(init=False)
    mode: str = "debug"
```

**Описание**:
Класс `ExecuteLocator` предназначен для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Атрибуты**:
- `driver` (Optional[object]): Экземпляр Selenium WebDriver.
- `actions` (ActionChains): Объект для выполнения цепочки действий.
- `mode` (str): Режим работы (например, "debug").

**Методы**:

*   `__post_init__(self)`: Инициализирует атрибут `actions` после создания экземпляра класса.
*   `execute_locator(self, locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = "presence_of_element_located", message: Optional[str] = None, typing_speed: Optional[float] = 0) -> Optional[str | list | dict | WebElement | bool]`: Выполняет действия с веб-элементом на основе предоставленного локатора.
*   `_evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
*   `get_attribute_by_locator(self, locator: SimpleNamespace | dict, timeout: Optional[float] = 0, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0) -> Optional[WebElement | list[WebElement]]`: Извлекает атрибуты из веб-элемента или списка веб-элементов.
*   `get_webelement_by_locator(self, locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: str = "presence_of_element_located") -> Optional[WebElement | List[WebElement]]`: Извлекает веб-элемент или список элементов на основе предоставленного локатора.
*   `get_webelement_as_screenshot(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0, webelement: Optional[WebElement] = None) -> Optional[BinaryIO]`: Делает скриншот найденного веб-элемента.
*   `execute_event(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> Optional[str | list[str] | bytes | list[bytes] | bool]`: Выполняет событие, связанное с локатором.
*   `send_message(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.

## Методы класса

### `__post_init__`

```python
def __post_init__(self):
    if self.driver:
        self.actions = ActionChains(self.driver)
```

**Назначение**: Инициализирует атрибут `actions` после создания экземпляра класса.

**Как работает функция**:
Если атрибут `driver` не None, создает инстанс `ActionChains`

### `execute_locator`

```python
async def execute_locator(
        self,
        locator:  dict | SimpleNamespace,\n        timeout: Optional[float] = 0,\n        timeout_for_event: Optional[str] = "presence_of_element_located",\n        message: Optional[str] = None,\n        typing_speed: Optional[float] = 0,\n    ) ->  Optional[str | list | dict | WebElement | bool]:
        """
        Executes actions on a web element based on the provided locator.

        Args:
            locator: Locator data (dict or SimpleNamespace).
            timeout: Timeout for locating the element (seconds).
            timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').
            message: Optional message for actions like send_keys or type.
            typing_speed: Typing speed for send_keys events (seconds).

        Returns:
            The result of the operation, which can be a string, list, dict, WebElement, bool, or None.
        """
    ...
```

**Назначение**: Выполняет действия над веб-элементом на основе предоставленного локатора.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `timeout`: Время ожидания для обнаружения элемента (в секундах).
- `timeout_for_event`: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
- `message`: Необязательное сообщение для таких действий, как `send_keys` или `type`.
- `typing_speed`: Скорость ввода для событий `send_keys` (в секундах).

**Возвращает**:
- Результат операции, который может быть строкой, списком, словарем, WebElement, bool или None.

**Как работает функция**:
1. Функция проверяет, является ли локатор словарем, и преобразует его в объект SimpleNamespace, если это так.
2. Проверяет, содержит ли локатор атрибуты selector и by.
3. Вызывает внутреннюю асинхронную функцию `_parse_locator` для дальнейшей обработки локатора и выполнения действий.
4. Внутренняя функция `_parse_locator`:
    *   Проверяет, содержит ли локатор атрибуты event и attribute, и если не содержит `mandatory` flag, пропускает его.
    *   Преобразует атрибут `by` к нижнему регистру.
    *   Если атрибут `by` имеет значение "value", извлекает атрибут из веб-элемента с помощью `get_attribute_by_locator`.
    *   Если атрибут `by` имеет значение "url", извлекает параметр из URL страницы.
    *   В противном случае, выполняет событие, получает атрибут или извлекает веб-элемент, вызывая соответствующие функции.

### `_evaluate_locator`

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

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:
- `attribute`: Атрибут для вычисления (может быть строкой, списком строк или словарем).

**Возвращает**:
- Вычисленный атрибут, который может быть строкой, списком строк или словарем.

**Как работает функция**:

1.  Внутренняя функция `_evaluate` заменяет подстроки, соответствующие регулярному выражению `r"%(\w+)%"` на атрибуты из `Keys`, если они найдены.
2.  Если `attribute` - список, применяет внутреннюю функцию `_evaluate` к каждому элементу списка и возвращает новый список.
3.  Если `attribute` - строка, вычисляет ее с помощью функции `_evaluate`.

### `get_attribute_by_locator`

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
            timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').
            message: Not used in this function.
            typing_speed: Not used in this function.

        Returns:
            The attribute value(s) as a WebElement, list of WebElements, or None if not found.
        """
    ...
```

**Назначение**: Извлекает атрибуты из веб-элемента или списка веб-элементов.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `timeout`: Время ожидания для обнаружения элемента (в секундах).
- `timeout_for_event`: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
- `message`: Не используется в этой функции.
- `typing_speed`: Не используется в этой функции.

**Возвращает**:
- Значения атрибутов в виде WebElement, списка WebElements или None, если не найдено.

**Как работает функция**:

1.  Получает веб-элемент(ы) с помощью `get_webelement_by_locator`.
2.  Если элемент не найден, возвращает `None`.
3.  Если `locator.attribute` - строка, начинающаяся с "{", пытается преобразовать строку в словарь.
4.  Если веб-элемент является списком, возвращает список значений атрибутов для каждого элемента списка.
5.  В противном случае возвращает значение атрибута для одного веб-элемента.

### `get_webelement_by_locator`

```python
async def get_webelement_by_locator(
        self,
        locator: dict | SimpleNamespace,
        timeout: Optional[float] = 0,
        timeout_for_event: Optional[str] = "presence_of_element_located",
    ) -> Optional[WebElement | List[WebElement]]:
        """
        Retrieves a web element or list of elements based on the provided locator.

        Args:
            locator: Locator data (dict or SimpleNamespace).
            timeout: Timeout for locating the element (seconds).
            timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').

        Returns:
           WebElement, list of WebElements, or None if not found.
        """
    ...
```

**Назначение**: Извлекает веб-элемент или список элементов на основе предоставленного локатора.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `timeout`: Время ожидания для обнаружения элемента (в секундах).
- `timeout_for_event`: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

**Возвращает**:
- WebElement, список WebElements или None, если не найдено.

**Как работает функция**:

1.  Преобразует локатор в `SimpleNamespace`, если он является словарем.
2.  В зависимости от значения `timeout` и `timeout_for_event` использует `driver.find_elements` или `WebDriverWait` для поиска веб-элементов.
3.  Вызывает внутреннюю асинхронную функцию `_parse_elements_list` для фильтрации полученного списка элементов.
4.  Возвращает отфильтрованный список элементов или `None`, если элементы не найдены.

### `get_webelement_as_screenshot`

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
            timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').
            message: Not used in this function.
            typing_speed: Not used in this function.
            webelement: Optional pre-fetched web element.

        Returns:
           BinaryIO stream of the screenshot or None if failed.
        """
    ...
```

**Назначение**: Сделать скриншот найденного веб-элемента.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `timeout`: Время ожидания для обнаружения элемента (в секундах).
- `timeout_for_event`: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
- `message`: Не используется в этой функции.
- `typing_speed`: Не используется в этой функции.
- `webelement`: Optional pre-fetched web element.

**Возвращает**:
- Двоичный поток BinaryIO скриншота или None, если не удалось.

**Как работает функция**:
1. Если веб-элемент не передан, получает веб-элемент(ы) с помощью `get_webelement_by_locator`.
2. Если элемент не найден, возвращает `None`.
3. Пытается сделать скриншот веб-элемента и вернуть его в виде бинарного потока.

### `execute_event`

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
            timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').
            message: Optional message to send with the event.
            typing_speed: Typing speed for send_keys events (seconds).

        Returns:
            The result of the event execution (str, list of str, bytes, list of bytes, or bool).
        """
    ...
```

**Назначение**: Выполняет событие, связанное с локатором.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `timeout`: Время ожидания для обнаружения элемента (в секундах).
- `timeout_for_event`: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
- `message`: Необязательное сообщение для отправки с событием.
- `typing_speed`: Скорость ввода для событий `send_keys` (в секундах).

**Возвращает**:
- Результат выполнения события (str, список str, bytes, список bytes или bool).

**Как работает функция**:

1.  Получает веб-элемент(ы) с помощью `get_webelement_by_locator`.
2.  Если элемент не найден, возвращает `False`.
3.  Перебирает события, указанные в `locator.event`.
4.  В зависимости от события выполняет различные действия:
    *   `click()`: Кликает на веб-элемент.
    *   `pause(duration)`: Приостанавливает выполнение на указанное время.
    *   `upload_media()`: Загружает медиа-файл.
    *   `screenshot()`: Делает скриншот веб-элемента.
    *   `clear()`: Очищает веб-элемент.
    *   `send_keys()`: Отправляет клавиши веб-элементу.
    *   `type()`: Вводит текст в веб-элемент с указанной скоростью.

### `send_message`

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
            timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').
            message: Message to send to the web element.
            typing_speed: Typing speed for send_keys events (seconds).

        Returns:
            True if the message was sent successfully, False otherwise.
        """
    ...
```

**Назначение**: Отправляет сообщение веб-элементу.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `timeout`: Время ожидания для обнаружения элемента (в секундах).
- `timeout_for_event`: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
- `message`: Сообщение для отправки веб-элементу.
- `typing_speed`: Скорость ввода для событий `send_keys` (в секундах).

**Возвращает**:
- `True`, если сообщение было отправлено успешно, `False` в противном случае.

**Как работает функция**:

1.  Определяет внутреннюю функцию `type_message`, которая выполняет ввод текста в веб-элемент с указанной скоростью.
2.  Получает веб-элемент с помощью `get_webelement_by_locator`.
3.  Если элемент не найден, возвращает `False`.
4.  Вызывает функцию `type_message` для ввода текста в веб-элемент.

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеку `selenium`, `asyncio` и `dataclasses`.

```bash
pip install selenium asyncio dataclasses
```

Пример использования:

```python
import asyncio
from src.webdriver import Driver, Chrome
from src.webdriver.executor import ExecuteLocator

async def main():
    driver = Driver(Chrome)
    executor = ExecuteLocator(driver=driver.driver)
    locator = {
        "by": "ID",
        "selector": "my_element",
        "event": "type(Hello, world!)"
    }
    success = await executor.execute_locator(locator)
    print(f"Event executed successfully: {success}")

asyncio.run(main())