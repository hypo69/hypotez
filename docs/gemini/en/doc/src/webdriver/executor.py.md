# Модуль `src.webdriver.executor`

## Обзор

Модуль `src.webdriver.executor` предоставляет функциональность для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

Этот модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath), выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Детали

Модуль содержит класс `ExecuteLocator`, который инкапсулирует всю логику взаимодействия с веб-элементами. Класс использует драйвер Selenium для выполнения различных действий, таких как поиск элементов, выполнение кликов, ввод текста и получение атрибутов. Модуль также включает обработку ошибок, таких как `TimeoutException` и `ElementClickInterceptedException`.

## Классы

### `ExecuteLocator`

**Описание**: Класс `ExecuteLocator` предназначен для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Атрибуты**:
- `driver` (Optional[object]): Драйвер Selenium, используемый для взаимодействия с веб-страницей.
- `actions` (ActionChains): Объект `ActionChains` для выполнения сложных последовательностей действий.
- `mode` (str): Режим работы (по умолчанию "debug").

**Методы**:
- `__post_init__()`: Инициализирует объект `ActionChains` после создания экземпляра класса.
- `execute_locator()`: Выполняет действия над веб-элементом на основе предоставленного локатора.
- `_evaluate_locator()`: Вычисляет и обрабатывает атрибуты локатора.
- `get_attribute_by_locator()`: Извлекает атрибуты из веб-элемента или списка веб-элементов.
- `get_webelement_by_locator()`: Извлекает веб-элемент или список элементов на основе предоставленного локатора.
- `get_webelement_as_screenshot()`: Делает скриншот найденного веб-элемента.
- `execute_event()`: Выполняет событие, связанное с локатором.
- `send_message()`: Отправляет сообщение веб-элементу.

## Методы класса `ExecuteLocator`

### `__post_init__`

```python
def __post_init__(self):
    """Инициализирует объект ActionChains после создания экземпляра класса."""
```

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
    """Выполняет действия над веб-элементом на основе предоставленного локатора.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.
        timeout (Optional[float], optional): Время ожидания для поиска элемента в секундах. По умолчанию 0.
        timeout_for_event (Optional[str], optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".
        message (Optional[str], optional): Сообщение для действий, таких как send_keys или type. По умолчанию None.
        typing_speed (Optional[float], optional): Скорость ввода текста для событий send_keys в секундах. По умолчанию 0.

    Returns:
        Optional[str | list | dict | WebElement | bool]: Результат операции (строка, список, словарь, WebElement, bool или None).
    """
```

Внутренняя функция: `_parse_locator`
```python
async def _parse_locator(
    locator: SimpleNamespace,
    message: Optional[str] = None,
    timeout: Optional[float] = 0,
    timeout_for_event: Optional[str] = "presence_of_element_located",
    typing_speed: Optional[float] = 0,
) -> Optional[str | list | dict | WebElement | bool]:
    """Разбирает и выполняет инструкции локатора.
    Args:
        locator (SimpleNamespace): Данные локатора.
        message (Optional[str], optional): Сообщение для действий, таких как send_keys или type. По умолчанию None.
        timeout (Optional[float], optional): Время ожидания для поиска элемента в секундах. По умолчанию 0.
        timeout_for_event (Optional[str], optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".
        typing_speed (Optional[float], optional): Скорость ввода текста для событий send_keys в секундах. По умолчанию 0.

    Returns:
        Optional[str | list | dict | WebElement | bool]: Результат операции (строка, список, словарь, WebElement, bool или None).
    """
```
**Принцип работы**:
- Функция `execute_locator` выполняет действия над веб-элементом на основе предоставленного локатора.
- Сначала проверяется, является ли локатор словарем, и, если да, преобразует его в `SimpleNamespace` для удобства доступа к атрибутам.
- Затем проверяется наличие атрибутов `attribute` и `selector` в локаторе. Если они отсутствуют, функция завершается, возвращая `None`.
- Далее вызывается асинхронная функция `_parse_locator`, которая разбирает инструкции локатора и выполняет соответствующие действия, такие как получение атрибута, выполнение события или получение веб-элемента.

**Примеры**:
```python
# Пример вызова функции execute_locator с различными параметрами
result1 = await executor.execute_locator(locator={'by': 'id', 'selector': 'element_id'})
result2 = await executor.execute_locator(locator=SimpleNamespace(by='xpath', selector='//button'), timeout=10)
result3 = await executor.execute_locator(locator={'by': 'class', 'selector': 'my_class', 'attribute': 'text'}, message='Hello')
```

### `_evaluate_locator`

```python
def _evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
    """Вычисляет и обрабатывает атрибуты локатора.

    Args:
        attribute (str | List[str] | dict): Атрибут для вычисления (строка, список строк или словарь).

    Returns:
        Optional[str | List[str] | dict]: Вычисленный атрибут (строка, список строк или словарь).
    """
```

Внутренняя функция: `_evaluate`
```python
def _evaluate(attr: str) -> Optional[str]:
    """Вычисляет строковый атрибут.

    Args:
        attr (str): Атрибут для вычисления (строка).

    Returns:
        Optional[str]: Вычисленный атрибут (строка).
    """
```
**Принцип работы**:
- Функция `_evaluate_locator` вычисляет и обрабатывает атрибуты локатора.
- Она проверяет, является ли атрибут списком, и если да, то применяет функцию `_evaluate` к каждому элементу списка.
- Если атрибут является строкой, то применяется функция `_evaluate` непосредственно к строке.
- Функция `_evaluate` проверяет, соответствует ли атрибут шаблону `%\\w+%`, и если да, пытается получить соответствующий атрибут из класса `Keys`.

**Примеры**:
```python
# Пример вызова функции _evaluate_locator с различными атрибутами
result1 = executor._evaluate_locator(attribute='%ENTER%')
result2 = executor._evaluate_locator(attribute=['%SHIFT%', '%CONTROL%'])
result3 = executor._evaluate_locator(attribute={'key1': '%ALT%', 'key2': '%TAB%'})
```

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
    """Извлекает атрибуты из веб-элемента или списка веб-элементов.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (Optional[float], optional): Время ожидания для поиска элемента в секундах. По умолчанию 0.
        timeout_for_event (str, optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".
        message (Optional[str], optional): Не используется в этой функции. По умолчанию None.
        typing_speed (float, optional): Не используется в этой функции. По умолчанию 0.

    Returns:
        Optional[WebElement | list[WebElement]]: Значение атрибута или список значений атрибутов.
    """
```

Внутренняя функция: `_parse_dict_string`
```python
def _parse_dict_string(attr_string: str) -> dict | None:
    """Разбирает строку типа '{attr1:attr2}' в словарь."""
```

Внутренняя функция: `_get_attributes_from_dict`
```python
def _get_attributes_from_dict(web_element: WebElement, attr_dict: dict) -> dict:
    """Извлекает значения атрибутов из WebElement на основе словаря."""
```
**Принцип работы**:
- Функция `get_attribute_by_locator` извлекает атрибуты из веб-элемента или списка веб-элементов на основе предоставленного локатора.
- Сначала она получает веб-элемент с помощью функции `get_webelement_by_locator`.
- Затем, в зависимости от типа атрибута (строка или словарь), она извлекает соответствующие значения атрибутов.

**Примеры**:
```python
# Пример вызова функции get_attribute_by_locator с различными параметрами
result1 = await executor.get_attribute_by_locator(locator={'by': 'id', 'selector': 'element_id', 'attribute': 'value'})
result2 = await executor.get_attribute_by_locator(locator=SimpleNamespace(by='xpath', selector='//button', attribute='text'), timeout=10)
result3 = await executor.get_attribute_by_locator(locator={'by': 'class', 'selector': 'my_class', 'attribute': '{attr1:attr2}'})
```

### `get_webelement_by_locator`

```python
async def get_webelement_by_locator(
    self,
    locator: dict | SimpleNamespace,
    timeout: Optional[float] = 0,
    timeout_for_event: Optional[str] = "presence_of_element_located",
) -> Optional[WebElement | List[WebElement]]:
    """Извлекает веб-элемент или список элементов на основе предоставленного локатора.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.
        timeout (Optional[float], optional): Время ожидания для поиска элемента в секундах. По умолчанию 0.
        timeout_for_event (Optional[str], optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".

    Returns:
        Optional[WebElement | List[WebElement]]: Веб-элемент или список веб-элементов.
    """
```

Внутренняя функция: `_parse_elements_list`
```python
async def _parse_elements_list(
    web_elements: WebElement | List[WebElement], locator: SimpleNamespace
) ->  Optional[WebElement | List[WebElement]]:
    """Фильтрует список веб-элементов на основе атрибута if_list."""
```
**Принцип работы**:
- Функция `get_webelement_by_locator` извлекает веб-элемент или список элементов на основе предоставленного локатора.
- Она использует драйвер Selenium для поиска элементов на странице.
- В зависимости от значения параметра `timeout`, она может ожидать появления элемента в течение определенного времени.
- После получения элементов, она фильтрует их на основе атрибута `if_list`.

**Примеры**:
```python
# Пример вызова функции get_webelement_by_locator с различными параметрами
element1 = await executor.get_webelement_by_locator(locator={'by': 'id', 'selector': 'element_id'})
element2 = await executor.get_webelement_by_locator(locator=SimpleNamespace(by='xpath', selector='//button'), timeout=10)
element3 = await executor.get_webelement_by_locator(locator={'by': 'class', 'selector': 'my_class'}, timeout_for_event='visibility_of_all_elements_located')
```

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
    """Делает скриншот найденного веб-элемента.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (float, optional): Время ожидания для поиска элемента в секундах. По умолчанию 5.
        timeout_for_event (str, optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".
        message (Optional[str], optional): Не используется в этой функции. По умолчанию None.
        typing_speed (float, optional): Не используется в этой функции. По умолчанию 0.
        webelement (Optional[WebElement], optional): Предварительно полученный веб-элемент. По умолчанию None.

    Returns:
        Optional[BinaryIO]: BinaryIO поток скриншота или None, если не удалось.
    """
```

**Принцип работы**:
- Функция `get_webelement_as_screenshot` делает скриншот найденного веб-элемента.
- Сначала она получает веб-элемент с помощью функции `get_webelement_by_locator`, если `webelement` не был передан.
- Затем она пытается сделать скриншот элемента и возвращает его в виде `BinaryIO` потока.

**Примеры**:
```python
# Пример вызова функции get_webelement_as_screenshot с различными параметрами
screenshot1 = await executor.get_webelement_as_screenshot(locator={'by': 'id', 'selector': 'element_id'})
screenshot2 = await executor.get_webelement_as_screenshot(locator=SimpleNamespace(by='xpath', selector='//button'), timeout=10)
```

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
    """Выполняет событие, связанное с локатором.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (float, optional): Время ожидания для поиска элемента в секундах. По умолчанию 5.
        timeout_for_event (str, optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".
        message (str, optional): Сообщение для отправки с событием. По умолчанию None.
        typing_speed (float, optional): Скорость ввода текста для событий send_keys в секундах. По умолчанию 0.

    Returns:
        Optional[str | list[str] | bytes | list[bytes] | bool]: Результат выполнения события.
    """
```

**Принцип работы**:
- Функция `execute_event` выполняет событие, связанное с локатором.
- Она получает веб-элемент с помощью функции `get_webelement_by_locator`.
- Затем она разбирает строку события и выполняет соответствующие действия, такие как клик, ввод текста или загрузка медиа.

**Примеры**:
```python
# Пример вызова функции execute_event с различными параметрами
result1 = await executor.execute_event(locator={'by': 'id', 'selector': 'element_id', 'event': 'click()'})
result2 = await executor.execute_event(locator=SimpleNamespace(by='xpath', selector='//button', event='pause(5)'), timeout=10)
result3 = await executor.execute_event(locator={'by': 'class', 'selector': 'my_class', 'event': 'upload_media()', 'message': 'path/to/file'})
```

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
    """Отправляет сообщение веб-элементу.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (float, optional): Время ожидания для поиска элемента в секундах. По умолчанию 5.
        timeout_for_event (str, optional): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию "presence_of_element_located".
        message (str, optional): Сообщение для отправки веб-элементу. По умолчанию None.
        typing_speed (float, optional): Скорость ввода текста для событий send_keys в секундах. По умолчанию 0.

    Returns:
        bool: True, если сообщение было отправлено успешно, False в противном случае.
    """
```

Внутренняя функция: `type_message`
```python
def type_message(
    el: WebElement,
    message: str,
    replace_dict: dict = {";": "SHIFT+ENTER"},
    typing_speed: float = typing_speed,
) -> bool:
    """Вводит сообщение в веб-элемент с заданной скоростью ввода."""
```
**Принцип работы**:
- Функция `send_message` отправляет сообщение веб-элементу.
- Она получает веб-элемент с помощью функции `get_webelement_by_locator`.
- Затем она использует функцию `type_message` для ввода текста в элемент с заданной скоростью.

**Примеры**:
```python
# Пример вызова функции send_message с различными параметрами
result1 = await executor.send_message(locator={'by': 'id', 'selector': 'element_id'}, message='Hello, world!')
result2 = await executor.send_message(locator=SimpleNamespace(by='xpath', selector='//input'), message='Some text', timeout=10)
```