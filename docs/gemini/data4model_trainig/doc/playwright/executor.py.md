### Анализ кода модуля `hypotez/src/webdriver/playwright/executor.py`

## Обзор

Этот модуль предоставляет функциональность для взаимодействия с веб-элементами, используя Playwright, на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

## Подробнее

Модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам, выполнять с ними различные действия (например, клик, ввод текста) и получать снимки экрана. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты.

## Классы

### `PlaywrightExecutor`

```python
class PlaywrightExecutor:
    """
    Executes commands based on executor-style locator commands using Playwright.
    """
```

**Описание**:
Класс `PlaywrightExecutor` предназначен для выполнения команд на основе команд локатора в стиле исполнителя с использованием Playwright.

**Атрибуты**:
- `driver` (Optional[object]): Экземпляр Playwright.
- `page` (Optional[Page]): Экземпляр Playwright Page.
- `config` (SimpleNamespace): Конфигурация, загруженная из `playwrid.json`.
- `browser_type` (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit').

**Методы**:

*   `__init__(self, browser_type: str = 'chromium', **kwargs)`: Инициализирует исполнитель Playwright.
*   `start(self) -> None`: Инициализирует Playwright и запускает экземпляр браузера.
*   `stop(self) -> None`: Закрывает браузер Playwright и останавливает его экземпляр.
*   `execute_locator(self, locator: Union[dict, SimpleNamespace], message: Optional[str] = None, typing_speed: float = 0, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = 'presence_of_element_located') -> Union[str, list, dict, Locator, bool, None]`: Выполняет действия над веб-элементом на основе предоставленного локатора.
*   `evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
*   `get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]`: Получает указанный атрибут из веб-элемента.
*   `get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]`: Получает веб-элемент с помощью локатора.
*   `get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]`: Делает скриншот найденного веб-элемента.
*   `execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]`: Выполняет событие, связанное с локатором.
*   `send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.
*   `goto(self, url: str) -> None`: Переходит по указанному URL-адресу.

## Методы класса

### `__init__`

```python
def __init__(self, browser_type: str = 'chromium', **kwargs):
    """
    Initializes the Playwright executor.

    Args:
        browser_type: Type of browser to launch (e.g., 'chromium', 'firefox', 'webkit').
    """
    ...
```

**Назначение**: Инициализирует исполнитель Playwright.

**Параметры**:
- `browser_type` (str, optional): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit'). По умолчанию 'chromium'.

**Как работает функция**:
Сохраняет переданный тип браузера в атрибуте `self.browser_type` и загружает конфигурацию из файла `playwrid.json`.

### `start`

```python
async def start(self) -> None:
    """
    Initializes Playwright and launches a browser instance.
    """
    ...
```

**Назначение**: Инициализирует Playwright и запускает экземпляр браузера.

**Как работает функция**:
1.  Запускает Playwright, используя `async_playwright().start()`.
2.  Запускает указанный тип браузера (headless mode) с опциями из конфигурации.
3.  Создает новую страницу в браузере.
4.  В случае ошибки логирует информацию об ошибке.

### `stop`

```python
async def stop(self) -> None:
    """
    Closes Playwright browser and stops its instance.
    """
    ...
```

**Назначение**: Закрывает браузер Playwright и останавливает его экземпляр.

**Как работает функция**:
1.  Закрывает страницу, если она существует.
2.  Останавливает Playwright, если он запущен.
3.  В случае ошибки логирует информацию об ошибке.

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
        Executes actions on a web element based on the provided locator.

        Args:
            locator: Locator data (dict or SimpleNamespace).
            message: Optional message for events.
            typing_speed: Optional typing speed for events.
            timeout: Timeout for locating the element (seconds).
            timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').

        Returns:
             The result of the operation, which can be a string, list, dict, Locator, bool, or None.
        """
    ...
```

**Назначение**: Выполняет действия над веб-элементом на основе предоставленного локатора.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `message`: Необязательное сообщение для событий.
- `typing_speed`: Необязательная скорость ввода для событий.
- `timeout`: Время ожидания для обнаружения элемента (в секундах).
- `timeout_for_event`: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

**Возвращает**:
- Результат операции, который может быть строкой, списком, словарем, Locator, bool или None.

**Как работает функция**:
1. Проверяет, является ли локатор словарем, и преобразует его в объект SimpleNamespace, если это так.
2. Проверяет, содержит ли локатор атрибуты selector и by.
3. Вызывает внутреннюю асинхронную функцию `_parse_locator` для дальнейшей обработки локатора и выполнения действий.
4. Внутренняя функция `_parse_locator`:
    *   Проверяет, содержит ли локатор атрибуты event и attribute, и если не содержит `mandatory` flag, пропускает его.
    *   Если атрибут `by` имеет значение "VALUE", извлекает атрибут из веб-элемента с помощью `get_attribute_by_locator`.
    *   В противном случае, выполняет событие, получает атрибут или извлекает веб-элемент, вызывая соответствующие функции.

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
    ...
```

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:
- `attribute`: Атрибут для вычисления (может быть строкой, списком строк или словарем).

**Возвращает**:
- Вычисленный атрибут, который может быть строкой, списком строк или словарем.

**Как работает функция**:

1.  Внутренняя асинхронная функция `_evaluate` возвращает входной атрибут без изменений.
2.  Если `attribute` - список, возвращает результаты вычисления каждого элемента списка с помощью `asyncio.gather`.
3.  Если `attribute` - строка, возвращает результат вычисления атрибута с помощью функции `_evaluate`.

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
    ...
```

**Назначение**: Получает указанный атрибут из веб-элемента.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).

**Возвращает**:
- Attribute или None.

**Как работает функция**:

1.  Получает веб-элемент(ы) с помощью `get_webelement_by_locator`.
2.  Если элемент не найден, возвращает `None`.
3.  Определяет внутренние асинхронные функции для обработки и извлечения атрибутов из элемента, в том числе для случаев, когда `locator.attribute` является строкой, представляющей собой словарь.
4.  Вызывает подходящую внутреннюю функцию для получения атрибута или словаря атрибутов.

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
    ...
```

**Назначение**: Получает веб-элемент с помощью локатора.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).

**Возвращает**:
- Playwright Locator

**Как работает функция**:

1.  Преобразует локатор в `SimpleNamespace`, если он является словарем.
2.  В зависимости от значения `locator.by.upper()` создает Locator с использованием `self.page.locator`.
3.  В зависимости от значения `locator.if_list` возвращает первый, последний, все, четные, нечетные элементы или элемент по индексу.

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
    ...
```

**Назначение**: Делает скриншот найденного веб-элемента.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `webelement`: Веб-элемент Locator.

**Возвращает**:
- Скриншот в байтах или None.

**Как работает функция**:

1.  Если веб-элемент не передан, получает веб-элемент(ы) с помощью `get_webelement_by_locator`.
2.  Если элемент не найден, возвращает `None`.
3.  Делает скриншот веб-элемента и возвращает его в виде байтов.

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
    ...
```

**Назначение**: Выполняет событие, связанное с локатором.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `message`: Необязательное сообщение для событий.
- `typing_speed`: Необязательная скорость ввода для событий.

**Возвращает**:
- Статус выполнения.

**Как работает функция**:

1.  Получает веб-элемент(ы) с помощью `get_webelement_by_locator`.
2.  Если элемент не найден, возвращает `False`.
3.  Перебирает события, указанные в `locator.event`.
4.  В зависимости от события выполняет различные действия, такие как клик, пауза, загрузка медиа, скриншот, очистка и ввод текста.

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
    ...
```

**Назначение**: Отправляет сообщение веб-элементу.

**Параметры**:
- `locator`: Данные локатора (словарь или SimpleNamespace).
- `message`: Сообщение для отправки веб-элементу.
- `typing_speed`: Скорость ввода сообщения в секундах.

**Возвращает**:
- `True`, если сообщение было отправлено успешно, `False` в противном случае.

**Как работает функция**:

1.  Получает веб-элемент(ы) с помощью `get_webelement_by_locator`.
2.  Если элемент не найден, возвращает `False`.
3.  В зависимости от указанной скорости ввода вводит сообщение в элемент.

### `goto`

```python
async def goto(self, url: str) -> None:
    """
    Navigates to a specified URL.

    Args:
        url: URL to navigate to.
    """
    if self.page:
        try:
             await self.page.goto(url)
        except Exception as ex:
               logger.error(f'Error during navigation to {url=}', ex)
```

**Назначение**: Переходит по указанному URL-адресу.

**Параметры**:
- `url`: URL для перехода.

**Как работает функция**:

1. Если объект страницы существует, выполняется переход по URL с помощью `self.page.goto(url)`.
2. При возникновении исключений при переходе по URL, информация об ошибке записывается в лог.

## Переменные

-   `self.driver` - экземпляр Playwright.
-   `self.page` - экземпляр страницы браузера Playwright.
-   `self.config`- объект содержащий конфигурацию Playwright

## Запуск

Для использования этого модуля необходимо установить библиотеки `playwright`, `asyncio` и `dataclasses`.

```bash
pip install playwright asyncio dataclasses
```

Пример использования:

```python
import asyncio
from src.webdriver import Playwright
from src.webdriver.executor import ExecuteLocator

async def main():
    driver = Playwright()
    await driver.start()
    locator = {
        "by": "ID",
        "selector": "my_element",
        "event": "type(Hello, world!)"
    }
    success = await executor.execute_locator(locator)
    print(f"Event executed successfully: {success}")
    await driver.stop()

asyncio.run(main())