### Анализ кода `hypotez/src/webdriver/executor.py.md`

## Обзор

Модуль предоставляет функциональность для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов. Он обрабатывает парсинг локаторов, взаимодействие с элементами и обработку ошибок.

## Подробнее

Этот модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath), выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Классы

### `ExecuteLocator`

```python
@dataclass
class ExecuteLocator:
    """
    Handles web element interaction using Selenium based on provided locators.
    """
    ...
```

**Описание**:
Класс для управления взаимодействием с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Атрибуты**:

*   `driver` (Optional[object]): Экземпляр Selenium WebDriver.
*   `actions` (ActionChains): Объект ActionChains для выполнения цепочки действий.
*   `mode` (str): Режим работы (по умолчанию "debug").

**Методы**:

*   `__post_init__(self)`: Инициализирует объект `ActionChains` после создания экземпляра класса.
*   `execute_locator(self, locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = "presence_of_element_located", message: Optional[str] = None, typing_speed: Optional[float] = 0) -> Optional[str | list | dict | WebElement | bool]`: Выполняет действия с веб-элементом на основе предоставленного локатора.
*   `_evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
*   `get_attribute_by_locator(self, locator: SimpleNamespace | dict, timeout: Optional[float] = 0, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0) -> Optional[WebElement | list[WebElement]]`: Извлекает атрибуты из веб-элемента или списка веб-элементов.
*   `get_webelement_by_locator(self, locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: str = "presence_of_element_located") -> Optional[WebElement | List[WebElement]]`: Извлекает веб-элемент или список элементов на основе предоставленного локатора.
*   `get_webelement_as_screenshot(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0, webelement: Optional[WebElement] = None) -> Optional[BinaryIO]`: Снимает скриншот найденного веб-элемента.
*   `execute_event(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> Optional[str | list[str] | bytes | list[bytes] | bool]`: Выполняет событие, связанное с локатором.
*   `send_message(self, locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.

## Методы класса

### `__post_init__`

```python
def __post_init__(self):
    if self.driver:
        self.actions = ActionChains(self.driver)
```

**Назначение**:
Инициализирует объект `ActionChains` после создания экземпляра класса.

**Как работает**:

*   Проверяет, установлен ли атрибут `driver`. Если да, создает объект `ActionChains` для выполнения цепочки действий с веб-элементами.

### `execute_locator`

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

**Назначение**:
Выполняет действия с веб-элементом на основе предоставленного локатора.

**Параметры**:

*   `locator`: Данные локатора (словарь или SimpleNamespace).
*   `timeout`: Время ожидания для поиска элемента (в секундах).
*   `timeout_for_event`: Условие ожидания ('presence\_of\_element\_located', 'visibility\_of\_all\_elements\_located').
*   `message`: Опциональное сообщение для действий, таких как `send_keys` или `type`.
*   `typing_speed`: Скорость ввода текста для событий `send_keys` (в секундах).

**Возвращает**:

*   Результат операции, который может быть строкой, списком, словарем, WebElement, булевым значением или None.

**Как работает**:

1.  Преобразует локатор в `SimpleNamespace`, если он передан в виде словаря.
2.  Проверяет, содержит ли локатор атрибуты `attribute` и `selector`. Если нет, возвращает `None`.
3.  Вызывает внутреннюю асинхронную функцию `_parse_locator` для выполнения действий на основе локатора.

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

**Назначение**:
Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:

*   `attribute`: Атрибут для вычисления (может быть строкой, списком строк или словарем).

**Возвращает**:

*   Вычисленный атрибут, который может быть строкой, списком строк или словарем.

**Как работает**:

1.  Определяет внутреннюю функцию `_evaluate`, которая выполняет подстановку значения атрибута `Keys` из selenium, если атрибут соответствует паттерну `%\\w+%`.
2.  Если атрибут является списком, применяет функцию `_evaluate` к каждому элементу списка.
3.  В противном случае применяет функцию `_evaluate` к атрибуту, преобразованному в строку.

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
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Not used in this function.
        typing_speed: Not used in this function.

    Returns:
        The attribute value(s) as a WebElement, list of WebElements, or None if not found.
    """
    ...
```

**Назначение**:
Извлекает атрибуты из веб-элемента или списка веб-элементов.

**Параметры**:

*   `locator`: Данные локатора (словарь или SimpleNamespace).
*   `timeout`: Время ожидания для поиска элемента (в секундах).
*   `timeout_for_event`: Условие ожидания ('presence\_of\_element\_located', 'visibility\_of\_all\_elements\_located').
*   `message`: Не используется в этой функции.
*   `typing_speed`: Не используется в этой функции.

**Возвращает**:

*   Значение атрибута(ов) в виде `WebElement`, списка `WebElement` или `None`, если элемент не найден.

**Как работает**:

1.  Преобразует локатор в `SimpleNamespace`, если он передан в виде словаря.
2.  Получает веб-элемент с помощью `self.get_webelement_by_locator`.
3.  Если элемент не найден и является обязательным, логирует отладочное сообщение и возвращает `None`.
4.  Если элемент найден, определяет внутреннюю функцию `_parse_dict_string` для обработки атрибута в виде строки, представляющей словарь.
5.  Определяет внутреннюю функцию `_get_attributes_from_dict` для получения значений атрибутов из `WebElement` на основе словаря.
6.  Если `locator.attribute` является строкой, начинающейся с `{`, преобразует её в словарь и получает значения атрибутов из `WebElement`.
7.  Если `web_element` является списком, получает значение атрибута для каждого элемента списка и возвращает список значений.
8.  В противном случае возвращает значение атрибута `locator.attribute` из `web_element`.

### `get_webelement_by_locator`

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

**Назначение**:
Извлекает веб-элемент или список элементов на основе предоставленного локатора.

**Параметры**:

*   `locator`: Данные локатора (словарь или SimpleNamespace).
*   `timeout`: Время ожидания для поиска элемента (в секундах).
*   `timeout_for_event`: Условие ожидания ('presence\_of\_element\_located', 'visibility\_of\_all\_elements\_located').

**Возвращает**:

*   `WebElement`, список `WebElement` или `None`, если элемент не найден.

**Как работает**:

1.  Извлекает значение таймаута из локатора или использует значение по умолчанию.
2.  Определяет внутреннюю асинхронную функцию `_parse_elements_list` для обработки списка веб-элементов в соответствии с атрибутом `if_list` локатора.
3.  Преобразует локатор в `SimpleNamespace`, если он передан в виде словаря.
4.  Использует `driver.find_elements` для поиска веб-элементов. Если указан `timeout`, использует `WebDriverWait` с заданным условием ожидания.
5.  Вызывает `_parse_elements_list` для фильтрации и обработки списка веб-элементов.
6.  Обрабатывает исключения `TimeoutException` и другие исключения, логируя ошибки и возвращая `None`.

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
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Not used in this function.
        typing_speed: Not used in this function.
        webelement: Optional pre-fetched web element.

    Returns:
       BinaryIO stream of the screenshot or None if failed.
    """
    ...
```

**Назначение**:
Делает скриншот найденного веб-элемента.

**Параметры**:

*   `locator`: Данные локатора (словарь или SimpleNamespace).
*   `timeout`: Время ожидания для поиска элемента (в секундах).
*   `timeout_for_event`: Условие ожидания ('presence\_of\_element\_located', 'visibility\_of\_all\_elements\_located').
*   `message`: Не используется в этой функции.
*   `typing_speed`: Не используется в этой функции.
*   `webelement`: Опциональный предварительно полученный веб-элемент.

**Возвращает**:

*   `BinaryIO`: Поток `BinaryIO` скриншота или `None`, если не удалось сделать скриншот.

**Как работает**:

1.  Преобразует локатор в `SimpleNamespace`, если он передан в виде словаря.
2.  Получает веб-элемент с помощью `self.get_webelement_by_locator`, если он не был передан в качестве аргумента.
3.  Если элемент не найден, возвращает `None`.
4.  Делает скриншот элемента с помощью `webelement.screenshot_as_png`.
5.  В случае ошибки логирует ее и возвращает `None`.

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
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Optional message to send with the event.
        typing_speed: Typing speed for send_keys events (seconds).

    Returns:
        The result of the event execution (str, list of str, bytes, list of bytes, or bool).
    """
    ...
```

**Назначение**:
Выполняет событие, связанное с локатором.

**Параметры**:

*   `locator`: Данные локатора (словарь или SimpleNamespace).
*   `timeout`: Время ожидания для поиска элемента (в секундах).
*   `timeout_for_event`: Условие ожидания ('presence\_of\_element\_located', 'visibility\_of\_all\_elements\_located').
*   `message`: Опциональное сообщение для отправки с событием.
*   `typing_speed`: Скорость ввода текста для событий `send_keys` (в секундах).

**Возвращает**:

*   Результат выполнения события (`str`, список `str`, `bytes`, список `bytes` или `bool`).

**Как работает**:

1.  Преобразует локатор в `SimpleNamespace`, если он передан в виде словаря.
2.  Разделяет строку `locator.event` на отдельные события.
3.  Получает веб-элемент с помощью `self.get_webelement_by_locator`.
4.  Для каждого события в списке выполняет действия:

    *   `click()`: Кликает по элементу.
    *   `pause(duration)`: Приостанавливает выполнение на указанное время.
    *   `upload_media()`: Загружает медиа-файл (требует наличия сообщения).
    *   `screenshot()`: Делает скриншот элемента.
    *   `clear()`: Очищает элемент.
    *   `send_keys(keys_to_send)`: Отправляет клавиши элементу.
    *   `type(message)`: Вводит текст в элемент с указанной скоростью.
5.  Возвращает результат выполнения событий.

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
        timeout_for_event: Wait condition ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Message to send to the web element.
        typing_speed: Typing speed for send_keys events (seconds).

    Returns:
        True if the message was sent successfully, False otherwise.
    """
    ...
```

**Назначение**:
Отправляет сообщение веб-элементу.

**Параметры**:

*   `locator`: Данные локатора (словарь или SimpleNamespace).
*   `timeout`: Время ожидания для поиска элемента (в секундах).
*   `timeout_for_event`: Условие ожидания ('presence\_of\_element\_located', 'visibility\_of\_all\_elements\_located').
*   `message`: Сообщение для отправки веб-элементу.
*   `typing_speed`: Скорость ввода текста для событий `send_keys` (в секундах).

**Возвращает**:

*   `True`, если сообщение было отправлено успешно, `False` в противном случае.

**Как работает**:

1.  Преобразует локатор в `SimpleNamespace`, если он передан в виде словаря.
2.  Определяет внутреннюю функцию `type_message` для ввода текста в веб-элемент.
3.  Получает веб-элемент с помощью `self.get_webelement_by_locator`.
4.  Перемещает курсор к веб-элементу.
5.  Вызывает функцию `type_message` для ввода текста.
6.  Возвращает `True`, если ввод успешен, `False` в противном случае.

## Переменные

Отсутствуют

## Примеры использования

```python
from src.webdriver.driver import Driver
from src.webdriver.executor import ExecuteLocator
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import asyncio
from types import SimpleNamespace

# Пример использования ExecuteLocator
async def main():
    driver = Driver(Chrome)
    executor = ExecuteLocator(driver)
    locator = SimpleNamespace(by=By.ID, selector='myElement', attribute='value')
    result = await executor.execute_locator(locator)
    print(f"Результат: {result}")
```

## Зависимости

*   `asyncio`: Для асинхронного программирования.
*   `re`: Для работы с регулярными выражениями.
*   `dataclasses`: Для использования декоратора `@dataclass`.
*   `typing.List, typing.Optional`: Для аннотаций типов.
*   `itertools.zip_longest`: для работы с итераторами разной длины
*   `types.SimpleNamespace`: Для создания объектов `SimpleNamespace`.
*   `selenium.webdriver.common.action_chains.ActionChains`: Для выполнения цепочки действий.
*   `selenium.webdriver.common.by.By`: Для определения стратегий поиска элементов.
*   `selenium.webdriver.common.keys.Keys`: Для отправки специальных клавиш.
*   `selenium.webdriver.remote.webelement.WebElement`: Для представления веб-элементов.
*   `selenium.webdriver.support.expected_conditions`: Для определения условий ожидания.
*   `selenium.webdriver.support.ui.WebDriverWait`: Для организации ожидания.
*   `header`: Модуль, определяющий корень проекта.
*   `src.logger.logger`: Для логирования.
*   `src.logger.exceptions`: для отлова кастомных исключений
*   `src.utils.printer.pprint`:Для форматированного вывода в консоль.

## Взаимосвязи с другими частями проекта

Модуль `executor.py` является ключевым компонентом для автоматизации взаимодействия с веб-страницами и используется в других частях проекта `hypotez`, где требуется выполнение автоматизированных действий в браузере.  Он зависит от:

*   `src.webdriver.driver`: Для получения экземпляра веб-драйвера.
*   `src.logger.logger`: Для логирования.
*   `src.logger.exceptions`: Для выброса кастомных исключений
*   `src.utils.printer.pprint`: Для форматированного вывода в консоль.

Рекомендации:
*    Использовать логгер из модуля `src.logger.logger` вместо  print команды
*    Удалить избыточное дублирование кода
*    Для повышения надежности  рекомендовано обрабатывать большее количество исключений
*   Привести документацию в соответствие с шаблоном проекта
*   Использовать аннотации типов