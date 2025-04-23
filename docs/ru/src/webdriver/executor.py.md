# Модуль `executor`

## Обзор

Модуль `executor` предоставляет функциональные возможности для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

Этот модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами.
Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath),
выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов.
Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Подробнее

Модуль содержит класс `ExecuteLocator`, который используется для выполнения действий над веб-элементами на основе предоставленных локаторов. Локаторы могут быть представлены в виде словарей или объектов `SimpleNamespace`. Модуль поддерживает различные типы событий, такие как клики, ввод текста, загрузка медиа и т.д.

## Классы

### `ExecuteLocator`

Описание: Класс предназначен для обработки взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Атрибуты**:

- `driver` (Optional[object]): Экземпляр веб-драйвера Selenium.
- `actions` (ActionChains): Объект для выполнения цепочки действий.
- `mode` (str): Режим работы (по умолчанию "debug").

**Методы**:

- `__post_init__()`: Инициализирует объект `ActionChains` после создания экземпляра класса.
- `execute_locator()`: Выполняет действия над веб-элементом на основе предоставленного локатора.
- `_evaluate_locator()`: Выполняет обработку атрибутов локатора.
- `get_attribute_by_locator()`: Извлекает атрибуты из веб-элемента или списка веб-элементов.
- `get_webelement_by_locator()`: Извлекает веб-элемент или список элементов на основе предоставленного локатора.
- `get_webelement_as_screenshot()`: Создает скриншот найденного веб-элемента.
- `execute_event()`: Выполняет событие, связанное с локатором.
- `send_message()`: Отправляет сообщение веб-элементу.

#### `__post_init__`

```python
def __post_init__(self):
    """Инициализирует объект ActionChains после создания экземпляра класса."""
    ...
```

Функция инициализирует атрибут `actions` класса `ExecuteLocator` объектом `ActionChains`, который позволяет выполнять сложные последовательности действий в браузере.

#### `execute_locator`

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
    Выполняет действия над веб-элементом на основе предоставленного локатора.

    Args:
        locator: Данные локатора (словарь или SimpleNamespace).
        timeout: Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Необязательное сообщение для таких действий, как send_keys или type.
        typing_speed: Скорость набора текста для событий send_keys (в секундах).

    Returns:
        Результат операции, который может быть строкой, списком, словарем, WebElement, bool или None.
    """
    ...
```

Функция `execute_locator` выполняет действия над веб-элементом, основываясь на предоставленном локаторе. Она принимает локатор, таймаут, условие таймаута для события, сообщение и скорость набора текста в качестве аргументов. Функция возвращает результат операции, который может быть строкой, списком, словарем, веб-элементом, булевым значением или None.

Внутри этой функции определена асинхронная внутренняя функция `_parse_locator`, которая используется для разбора инструкций локатора и выполнения соответствующих действий.

##### `_parse_locator`

```python
async def _parse_locator(
    locator: SimpleNamespace,
    message: Optional[str] = None,
    timeout: Optional[float] = 0,
    timeout_for_event: Optional[str] = "presence_of_element_located",
    typing_speed: Optional[float] = 0,
) -> Optional[str | list | dict | WebElement | bool]:
    """Разбирает и выполняет инструкции локатора."""
    ...
```

Эта внутренняя функция `_parse_locator` занимается разбором инструкций, содержащихся в локаторе, и выполняет соответствующие действия над веб-элементом. Она проверяет наличие атрибутов и событий, извлекает значения атрибутов, выполняет события (например, клики или ввод текста) и возвращает результат.
Функция обрабатывает различные типы локаторов и соответствующие действия, такие как получение атрибута элемента, выполнение события (например, клик) или получение самого веб-элемента. В зависимости от типа локатора и указанных атрибутов, функция вызывает другие методы класса, такие как `execute_event`, `get_attribute_by_locator` и `get_webelement_by_locator`.

#### `_evaluate_locator`

```python
def _evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
    """
    Оценивает и обрабатывает атрибуты локатора.

    Args:
        attribute: Атрибут для оценки (может быть строкой, списком строк или словарем).

    Returns:
        Оцененный атрибут, который может быть строкой, списком строк или словарем.
    """
    ...
```

Функция `_evaluate_locator` оценивает и обрабатывает атрибуты локатора. Она принимает атрибут в виде строки, списка строк или словаря и возвращает обработанный атрибут в том же формате. Функция использует внутреннюю функцию `_evaluate` для обработки отдельных строковых атрибутов.

##### `_evaluate`

```python
def _evaluate(attr: str) -> Optional[str]:
    """Оценивает строку одного атрибута."""
    ...
```

Внутренняя функция `_evaluate` оценивает строковый атрибут. Если атрибут соответствует определенному шаблону (например, `%\\w+%`), функция пытается извлечь значение из атрибута `Keys` и вернуть его. В противном случае функция возвращает исходный атрибут.

#### `get_attribute_by_locator`

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
    Извлекает атрибуты из веб-элемента или списка веб-элементов.

    Args:
        locator: Данные локатора (словарь или SimpleNamespace).
        timeout: Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Не используется в этой функции.
        typing_speed: Не используется в этой функции.

    Returns:
        Значение(я) атрибута в виде WebElement, списка WebElements или None, если не найдено.
    """
    ...
```

Функция `get_attribute_by_locator` извлекает атрибуты из веб-элемента или списка веб-элементов. Она принимает локатор, таймаут и условие таймаута для события в качестве аргументов. Функция возвращает значение атрибута в виде веб-элемента, списка веб-элементов или None, если элемент не найден.

Функция использует внутренние функции `_parse_dict_string` и `_get_attributes_from_dict` для обработки атрибутов, представленных в виде строк или словарей.

##### `_parse_dict_string`

```python
def _parse_dict_string(attr_string: str) -> dict | None:
    """Разбирает строку типа '{attr1:attr2}' в словарь."""
    ...
```

Внутренняя функция `_parse_dict_string` разбирает строку, представленную в формате словаря (например, "{attr1:attr2}"), и преобразует ее в словарь Python.

##### `_get_attributes_from_dict`

```python
def _get_attributes_from_dict(web_element: WebElement, attr_dict: dict) -> dict:
    """Извлекает значения атрибутов из WebElement на основе словаря."""
    ...
```

Внутренняя функция `_get_attributes_from_dict` извлекает значения атрибутов из веб-элемента на основе предоставленного словаря.

#### `get_webelement_by_locator`

```python
async def get_webelement_by_locator(
    self,
    locator: dict | SimpleNamespace,
    timeout: Optional[float] = 0,
    timeout_for_event: Optional[str] = "presence_of_element_located",
) -> Optional[WebElement | List[WebElement]]:
    """
    Извлекает веб-элемент или список элементов на основе предоставленного локатора.

    Args:
        locator: Данные локатора (словарь или SimpleNamespace).
        timeout: Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

    Returns:
       WebElement, список WebElements или None, если не найдено.
    """
    ...
```

Функция `get_webelement_by_locator` извлекает веб-элемент или список элементов на основе предоставленного локатора. Она принимает локатор, таймаут и условие таймаута для события в качестве аргументов. Функция возвращает веб-элемент, список веб-элементов или None, если элемент не найден.

Функция использует внутреннюю функцию `_parse_elements_list` для фильтрации списка веб-элементов на основе атрибута `if_list` локатора.

##### `_parse_elements_list`

```python
async def _parse_elements_list(
    web_elements: WebElement | List[WebElement], locator: SimpleNamespace
) ->  Optional[WebElement | List[WebElement]]:
    """Фильтрует список веб-элементов на основе атрибута if_list."""
    ...
```

Внутренняя функция `_parse_elements_list` фильтрует список веб-элементов на основе атрибута `if_list` локатора. Она принимает список веб-элементов и локатор в качестве аргументов и возвращает отфильтрованный список веб-элементов.

#### `get_webelement_as_screenshot`

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
    Делает скриншот найденного веб-элемента.

    Args:
        locator: Данные локатора (словарь или SimpleNamespace).
        timeout: Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Не используется в этой функции.
        typing_speed: Не используется в этой функции.
        webelement: Необязательный предварительно полученный веб-элемент.

    Returns:
       BinaryIO поток скриншота или None, если не удалось.
    """
    ...
```

Функция `get_webelement_as_screenshot` делает скриншот найденного веб-элемента. Она принимает локатор, таймаут, условие таймаута для события и предварительно полученный веб-элемент в качестве аргументов. Функция возвращает поток BinaryIO скриншота или None, если не удалось сделать скриншот.

#### `execute_event`

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
    Выполняет событие, связанное с локатором.

    Args:
        locator: Данные локатора (словарь или SimpleNamespace).
        timeout: Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Необязательное сообщение для отправки с событием.
        typing_speed: Скорость набора текста для событий send_keys (в секундах).

    Returns:
        Результат выполнения события (str, список str, bytes, список bytes или bool).
    """
    ...
```

Функция `execute_event` выполняет событие, связанное с локатором. Она принимает локатор, таймаут, условие таймаута для события, сообщение и скорость набора текста в качестве аргументов. Функция возвращает результат выполнения события (строка, список строк, байты, список байтов или логическое значение).

Функция поддерживает различные типы событий, такие как клик, пауза, загрузка медиа, создание скриншота, очистка элемента, отправка клавиш и ввод текста.

#### `send_message`

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
    Отправляет сообщение веб-элементу.

    Args:
        locator: Данные локатора (словарь или SimpleNamespace).
        timeout: Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event: Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').
        message: Сообщение для отправки веб-элементу.
        typing_speed: Скорость набора текста для событий send_keys (в секундах).

    Returns:
        True, если сообщение было успешно отправлено, False в противном случае.
    """
    ...
```

Функция `send_message` отправляет сообщение веб-элементу. Она принимает локатор, таймаут, условие таймаута для события, сообщение и скорость набора текста в качестве аргументов. Функция возвращает True, если сообщение было успешно отправлено, и False в противном случае.

Функция использует внутреннюю функцию `type_message` для ввода сообщения в веб-элемент.

##### `type_message`

```python
def type_message(
    el: WebElement,
    message: str,
    replace_dict: dict = {";": "SHIFT+ENTER"},
    typing_speed: float = typing_speed,
) -> bool:
    """Печатает сообщение в веб-элемент с указанной скоростью набора текста."""
    ...
```

Внутренняя функция `type_message` печатает сообщение в веб-элемент с указанной скоростью набора текста. Она принимает веб-элемент, сообщение, словарь замен и скорость набора текста в качестве аргументов. Функция возвращает True, если сообщение было успешно напечатано.