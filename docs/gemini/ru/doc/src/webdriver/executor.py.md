# Модуль `executor.py`

## Обзор

Модуль `executor.py` предназначен для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов. Он обрабатывает парсинг локаторов, взаимодействие с элементами и обработку ошибок.

Этот модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath), выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Подробнее

Модуль содержит класс `ExecuteLocator`, который предоставляет методы для выполнения различных действий с веб-элементами, таких как клик, ввод текста, получение атрибутов и т.д. Он использует Selenium WebDriver для взаимодействия с веб-страницами.

## Классы

### `ExecuteLocator`

**Описание**: Класс `ExecuteLocator` предназначен для обработки взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Атрибуты**:

- `driver` (Optional[object]): Экземпляр драйвера Selenium WebDriver.
- `actions` (ActionChains): Объект ActionChains для выполнения сложных последовательностей действий.
- `mode` (str): Режим работы, по умолчанию "debug".

**Принцип работы**:
Класс инициализируется с экземпляром драйвера Selenium WebDriver, который используется для выполнения действий с веб-элементами. ActionChains используется для выполнения сложных последовательностей действий, таких как перемещение мыши и ввод текста.

**Методы**:

- `__post_init__()`: Метод, вызываемый после инициализации экземпляра класса.
- `execute_locator()`: Выполняет действия с веб-элементом на основе предоставленного локатора.
- `_evaluate_locator()`: Вычисляет и обрабатывает атрибуты локатора.
- `get_attribute_by_locator()`: Получает атрибуты веб-элемента или списка веб-элементов.
- `get_webelement_by_locator()`: Получает веб-элемент или список элементов на основе предоставленного локатора.
- `get_webelement_as_screenshot()`: Делает скриншот найденного веб-элемента.
- `execute_event()`: Выполняет событие, связанное с локатором.
- `send_message()`: Отправляет сообщение веб-элементу.

## Методы класса

### `__post_init__`

```python
def __post_init__(self):
    """
    Инициализирует объект ActionChains, если предоставлен драйвер.
    """
```

**Назначение**: Инициализирует объект `ActionChains`, если предоставлен драйвер.

**Как работает функция**:
Функция проверяет, был ли предоставлен драйвер при инициализации класса. Если драйвер предоставлен, то создается объект `ActionChains`, который будет использоваться для выполнения сложных действий с веб-элементами.

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
    Выполняет действия с веб-элементом на основе предоставленного локатора.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.
        timeout (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию 0.
        timeout_for_event (Optional[str]): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
        message (Optional[str]): Сообщение для действий, таких как send_keys или type. По умолчанию None.
        typing_speed (Optional[float]): Скорость ввода текста для событий send_keys (в секундах). По умолчанию 0.

    Returns:
        Optional[str | list | dict | WebElement | bool]: Результат операции, который может быть строкой, списком, словарем, WebElement, булевым значением или None.

    """
```

**Назначение**: Выполняет действия с веб-элементом на основе предоставленного локатора.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.
- `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию 0.
- `timeout_for_event` (Optional[str]): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
- `message` (Optional[str]): Сообщение для действий, таких как send_keys или type. По умолчанию None.
- `typing_speed` (Optional[float]): Скорость ввода текста для событий send_keys (в секундах). По умолчанию 0.

**Возвращает**:
- `Optional[str | list | dict | WebElement | bool]`: Результат операции, который может быть строкой, списком, словарем, WebElement, булевым значением или None.

**Внутренние функции**:

- `_parse_locator`:
    ```python
    async def _parse_locator(
        locator: SimpleNamespace,
        message: Optional[str] = None,
        timeout: Optional[float] = 0,
        timeout_for_event: Optional[str] = "presence_of_element_located",
        typing_speed: Optional[float] = 0,
    ) -> Optional[str | list | dict | WebElement | bool]:
        """Parses and executes locator instructions."""
    ```
        **Назначение**:  Разбирает и выполняет инструкции локатора.

        **Параметры**:
        - `locator` (SimpleNamespace):  Данные локатора.
        - `message` (Optional[str]): Сообщение для действий, таких как `send_keys` или `type`. По умолчанию `None`.
        - `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию `0`.
        - `timeout_for_event` (Optional[str]): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
        - `typing_speed` (Optional[float]): Скорость ввода текста для событий `send_keys` (в секундах). По умолчанию `0`.

        **Возвращает**:
        - `Optional[str | list | dict | WebElement | bool]`:  Результат операции, который может быть строкой, списком, словарем, `WebElement`, булевым значением или `None`.

        **Как работает функция**:
        - Функция преобразует входной `locator` в объект `SimpleNamespace`, если он представлен в виде словаря.
        - Выполняет проверку на наличие атрибутов `attribute` и `selector` в локаторе. Если хотя бы один из них отсутствует, функция логирует отладочное сообщение и возвращает `None`.
        - Если `locator.by` является строкой, она преобразуется в нижний регистр. Далее, если `locator.attribute` существует, вызывается `self._evaluate_locator()` для его обработки. Если `locator.by` равно `'value'`, возвращается значение `locator.attribute`. Если `locator.by` равно `'url'`, извлекается параметр из URL.
        - Если `locator.event` определен, вызывается `self.execute_event()` для выполнения связанного события.
        - Если `locator.attribute` определен, вызывается `self.get_attribute_by_locator()` для получения значения атрибута элемента.
        - Если `locator.selector` и `locator.by` являются списками, и `locator.sorted` равно `'pairs'`, создаются пары элементов на основе предоставленных списков и рекурсивно вызывается `_parse_locator` для каждой пары.
        - Если ни одно из вышеперечисленных условий не выполнено, функция логирует предупреждение и возвращает `None`.
        - В конце функция возвращает результат вызова `_parse_locator`.

**Как работает функция**:

1.  Функция принимает данные локатора в виде словаря или объекта `SimpleNamespace`. Если передан словарь, он преобразуется в `SimpleNamespace`.
2.  Выполняется проверка на наличие атрибутов `attribute` и `selector` в локаторе. Если они отсутствуют, функция завершается и возвращает `None`.
3.  Вызывается внутренняя функция `_parse_locator` для обработки локатора и выполнения действий.
4.  Результат выполнения `_parse_locator` возвращается как результат `execute_locator`.

**Примеры**:

Пример использования с данными локатора в виде словаря:

```python
locator_data = {
    "by": "id",
    "selector": "myElement",
    "attribute": "value",
    "mandatory": True,
}
result = await execute_locator(locator_data)
```

Пример использования с данными локатора в виде `SimpleNamespace`:

```python
locator_data = SimpleNamespace(by="id", selector="myElement", attribute="value", mandatory=True)
result = await execute_locator(locator_data)
```

### `_evaluate_locator`

```python
def _evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
    """
    Вычисляет и обрабатывает атрибуты локатора.

    Args:
        attribute (str | List[str] | dict): Атрибут для вычисления (может быть строкой, списком строк или словарем).

    Returns:
        Optional[str | List[str] | dict]: Вычисленный атрибут, который может быть строкой, списком строк или словарем.
    """
```

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:

-   `attribute` (str | List[str] | dict): Атрибут для вычисления (может быть строкой, списком строк или словарем).

**Возвращает**:

-   `Optional[str | List[str] | dict]`: Вычисленный атрибут, который может быть строкой, списком строк или словарем.

**Внутренние функции**:

-   `_evaluate`:

    ```python
    def _evaluate(attr: str) -> Optional[str]:
        """Evaluates single attribute string."""
        return getattr(Keys, re.findall(r"%(\\w+)%", attr)[0], None) if re.match(r"^%\\w+%", attr) else attr
    ```

    **Назначение**: Вычисляет одиночный строковый атрибут.

    **Параметры**:

    -   `attr` (str): Атрибут для вычисления.

    **Возвращает**:

    -   `Optional[str]`: Вычисленный атрибут.

    **Как работает функция**:
    Функция проверяет, соответствует ли атрибут паттерну `%\\w+%`. Если соответствует, то извлекается имя атрибута из паттерна и возвращается соответствующий атрибут из класса `Keys`. Если не соответствует, то возвращается исходный атрибут.

**Как работает функция**:
Функция принимает атрибут, который может быть строкой, списком строк или словарем. Если атрибут является списком, то функция применяет функцию `_evaluate` к каждому элементу списка. Если атрибут является строкой, то функция применяет функцию `_evaluate` к строке. Результат вычисления возвращается.

**Примеры**:

Пример использования со строковым атрибутом:

```python
attribute = "%TAB%"
result = _evaluate_locator(attribute)
```

Пример использования со списком атрибутов:

```python
attribute = ["%TAB%", "value"]
result = _evaluate_locator(attribute)
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
    """
    Извлекает атрибуты из веб-элемента или списка веб-элементов.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию 0.
        timeout_for_event (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
        message (Optional[str]): Не используется в этой функции.
        typing_speed (float): Не используется в этой функции.

    Returns:
        Optional[WebElement | list[WebElement]]: Значение(я) атрибута в виде WebElement, списка WebElements или None, если не найдено.
    """
```

**Назначение**: Извлекает атрибуты из веб-элемента или списка веб-элементов.

**Параметры**:

-   `locator` (SimpleNamespace | dict): Данные локатора.
-   `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию 0.
-   `timeout_for_event` (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
-   `message` (Optional[str]): Не используется в этой функции.
-   `typing_speed` (float): Не используется в этой функции.

**Возвращает**:

-   `Optional[WebElement | list[WebElement]]`: Значение(я) атрибута в виде WebElement, списка WebElements или None, если не найдено.

**Внутренние функции**:

-   `_parse_dict_string`:

    ```python
    def _parse_dict_string(attr_string: str) -> dict | None:
        """Parses a string like '{attr1:attr2}' into a dictionary."""
        try:
            return {
                k.strip(): v.strip()
                for k, v in (pair.split(":") for pair in attr_string.strip("{}").split(","))
            }
        except ValueError as ex:
            logger.debug(f"Invalid attribute string format: {attr_string!r}", ex)
            return None
    ```

    **Назначение**: Преобразует строку вида '{attr1:attr2}' в словарь.

    **Параметры**:

    -   `attr_string` (str): Строка для преобразования.

    **Возвращает**:

    -   `dict | None`: Словарь, полученный из строки, или None в случае ошибки.

    **Как работает функция**:
    Функция пытается преобразовать строку вида '{attr1:attr2}' в словарь. Если преобразование удается, то возвращается словарь. Если преобразование не удается, то логируется отладочное сообщение и возвращается None.

-   `_get_attributes_from_dict`:

    ```python
    def _get_attributes_from_dict(web_element: WebElement, attr_dict: dict) -> dict:
        """Retrieves attribute values from a WebElement based on a dictionary."""
        result = {}
        for key, value in attr_dict.items():
            try:
                attr_key = web_element.get_attribute(key)
                attr_value = web_element.get_attribute(value)
                result[attr_key] = attr_value
            except Exception as ex:
                logger.debug(f"Error retrieving attributes '{key}' or '{value}' from element.", ex)
                return {}
        return result
    ```

    **Назначение**: Извлекает значения атрибутов из WebElement на основе словаря.

    **Параметры**:

    -   `web_element` (WebElement): Веб-элемент, из которого нужно извлечь атрибуты.
    -   `attr_dict` (dict): Словарь, определяющий, какие атрибуты нужно извлечь.

    **Возвращает**:

    -   `dict`: Словарь, содержащий извлеченные значения атрибутов.

    **Как работает функция**:
    Функция перебирает элементы словаря `attr_dict` и пытается извлечь значения атрибутов из `web_element` с использованием методов `get_attribute`. Если при извлечении атрибута происходит ошибка, то логируется отладочное сообщение и возвращается пустой словарь.

**Как работает функция**:

1.  Функция получает веб-элемент с помощью `self.get_webelement_by_locator`.
2.  Если атрибут локатора является строкой, начинающейся с '{', то строка преобразуется в словарь с помощью `_parse_dict_string`, и из веб-элемента извлекаются значения атрибутов на основе этого словаря с помощью `_get_attributes_from_dict`.
3.  Если атрибут локатора не является строкой, начинающейся с '{', то из веб-элемента извлекается значение атрибута с помощью `web_element.get_attribute`.

**Примеры**:

Пример использования с атрибутом в виде строки:

```python
locator = SimpleNamespace(by="id", selector="myElement", attribute="value")
result = await get_attribute_by_locator(locator)
```

Пример использования с атрибутом в виде словаря:

```python
locator = SimpleNamespace(by="id", selector="myElement", attribute="{attr1:attr2}")
result = await get_attribute_by_locator(locator)
```

### `get_webelement_by_locator`

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
        locator (dict | SimpleNamespace): Данные локатора.
        timeout (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию 0.
        timeout_for_event (Optional[str]): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.

    Returns:
       WebElement, list of WebElements, or None if not found.
    """
```

**Назначение**: Извлекает веб-элемент или список элементов на основе предоставленного локатора.

**Параметры**:

-   `locator` (dict | SimpleNamespace): Данные локатора.
-   `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию 0.
-   `timeout_for_event` (Optional[str]): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.

**Возвращает**:

-   `WebElement | List[WebElement] | None`: Веб-элемент, список веб-элементов или None, если не найдено.

**Внутренние функции**:

-   `_parse_elements_list`:

    ```python
    async def _parse_elements_list(
        web_elements: WebElement | List[WebElement], locator: SimpleNamespace
    ) ->  Optional[WebElement | List[WebElement]]:
        """Filters a list of web elements based on the if_list attribute."""
        if not isinstance(web_elements, list):
            return web_elements

        if_list = locator.if_list

        if if_list == "all":
            return web_elements
        elif if_list == "first":
            return web_elements[0]
        elif if_list == "last":
            return web_elements[-1]
        elif if_list == "even":
            return [web_elements[i] for i in range(0, len(web_elements), 2)]
        elif if_list == "odd":
            return [web_elements[i] for i in range(1, len(web_elements), 2)]
        elif isinstance(if_list, list):
            return [web_elements[i] for i in if_list]
        elif isinstance(if_list, int):
            return web_elements[if_list - 1]

        return web_elements
    ```

    **Назначение**: Фильтрует список веб-элементов на основе атрибута `if_list`.

    **Параметры**:

    -   `web_elements` (WebElement | List[WebElement]): Веб-элемент или список веб-элементов.
    -   `locator` (SimpleNamespace): Данные локатора.

    **Возвращает**:

    -   `Optional[WebElement | List[WebElement]]`: Отфильтрованный веб-элемент или список веб-элементов.

    **Как работает функция**:
    Функция принимает веб-элемент или список веб-элементов и данные локатора. Если веб-элемент не является списком, то он возвращается без изменений. Если веб-элемент является списком, то он фильтруется на основе атрибута `if_list` локатора. Атрибут `if_list` может иметь значения "all", "first", "last", "even", "odd", список индексов или целое число. В зависимости от значения атрибута `if_list` возвращается соответствующий отфильтрованный список веб-элементов.

**Как работает функция**:

1.  Функция преобразует данные локатора в объект `SimpleNamespace`, если это необходимо.
2.  Функция определяет, нужно ли использовать таймаут для поиска элемента, и если да, то использует `WebDriverWait` для ожидания появления элемента.
3.  Функция использует `driver.find_elements` для поиска элемента на странице.
4.  Если элемент найден, функция вызывает `_parse_elements_list` для фильтрации списка элементов на основе атрибута `if_list` локатора.

**Примеры**:

Пример использования без таймаута:

```python
locator = SimpleNamespace(by="id", selector="myElement")
element = await get_webelement_by_locator(locator)
```

Пример использования с таймаутом:

```python
locator = SimpleNamespace(by="id", selector="myElement", timeout=10)
element = await get_webelement_by_locator(locator)
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
    """
    Делает скриншот найденного веб-элемента.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (float): Время ожидания для поиска элемента (в секундах). По умолчанию 5.
        timeout_for_event (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
        message (Optional[str]): Не используется в этой функции.
        typing_speed (float): Не используется в этой функции.
        webelement (Optional[WebElement]): Предварительно полученный веб-элемент (опционально).

    Returns:
       BinaryIO stream of the screenshot or None if failed.
    """
```

**Назначение**: Делает скриншот найденного веб-элемента.

**Параметры**:

-   `locator` (SimpleNamespace | dict): Данные локатора.
-   `timeout` (float): Время ожидания для поиска элемента (в секундах). По умолчанию 5.
-   `timeout_for_event` (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
-   `message` (Optional[str]): Не используется в этой функции.
-   `typing_speed` (float): Не используется в этой функции.
-   `webelement` (Optional[WebElement]): Предварительно полученный веб-элемент (опционально).

**Возвращает**:

-   `Optional[BinaryIO]`: BinaryIO stream скриншота или None, если не удалось.

**Как работает функция**:

1.  Если `webelement` не передан, функция пытается получить веб-элемент с помощью `self.get_webelement_by_locator`.
2.  Если веб-элемент не найден, функция возвращает None.
3.  Функция пытается сделать скриншот веб-элемента с помощью `webelement.screenshot_as_png`.
4.  Если скриншот сделан успешно, функция возвращает BinaryIO stream скриншота.
5.  Если при создании скриншота произошла ошибка, функция логирует ошибку и возвращает None.

**Примеры**:

Пример использования с предварительно полученным веб-элементом:

```python
locator = SimpleNamespace(by="id", selector="myElement")
webelement = await get_webelement_by_locator(locator)
screenshot = await get_webelement_as_screenshot(locator, webelement=webelement)
```

Пример использования без предварительно полученного веб-элемента:

```python
locator = SimpleNamespace(by="id", selector="myElement")
screenshot = await get_webelement_as_screenshot(locator)
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
    """
    Выполняет событие, связанное с локатором.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (float): Время ожидания для поиска элемента (в секундах). По умолчанию 5.
        timeout_for_event (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
        message (str): Дополнительное сообщение для отправки с событием.
        typing_speed (float): Скорость ввода текста для событий send_keys (в секундах).

    Returns:
        Optional[str | list[str] | bytes | list[bytes] | bool]: Результат выполнения события (str, list of str, bytes, list of bytes, или bool).
    """
```

**Назначение**: Выполняет событие, связанное с локатором.

**Параметры**:

-   `locator` (SimpleNamespace | dict): Данные локатора.
-   `timeout` (float): Время ожидания для поиска элемента (в секундах). По умолчанию 5.
-   `timeout_for_event` (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
-   `message` (str): Дополнительное сообщение для отправки с событием.
-   `typing_speed` (float): Скорость ввода текста для событий send_keys (в секундах).

**Возвращает**:

-   `Optional[str | list[str] | bytes | list[bytes] | bool]`: Результат выполнения события (str, list of str, bytes, list of bytes, или bool).

**Как работает функция**:

1.  Функция получает веб-элемент с помощью `self.get_webelement_by_locator`.
2.  Функция разбивает строку `locator.event` на список событий, разделенных символом ';'.
3.  Функция перебирает список событий и выполняет каждое событие.
4.  Если событие равно "click()", функция пытается кликнуть на веб-элемент.
5.  Если событие начинается с "pause(", функция пытается извлечь длительность паузы из события и приостановить выполнение на указанное время.
6.  Если событие равно "upload_media()", функция пытается отправить сообщение веб-элементу с помощью `webelement.send_keys`.
7.  Если событие равно "screenshot()", функция пытается сделать скриншот веб-элемента с помощью `self.get_webelement_as_screenshot`.
8.  Если событие равно "clear()", функция пытается очистить веб-элемент с помощью `webelement.clear`.
9.  Если событие начинается с "send_keys(", функция пытается отправить клавиши веб-элементу с помощью `ActionChains`.
10. Если событие начинается с "type(", функция пытается ввести текст в веб-элемент с помощью `webelement.send_keys`.

**Примеры**:

Пример использования с событием "click()":

```python
locator = SimpleNamespace(by="id", selector="myElement", event="click()")
result = await execute_event(locator)
```

Пример использования с событием "pause(5)":

```python
locator = SimpleNamespace(by="id", selector="myElement", event="pause(5)")
result = await execute_event(locator)
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
    """
    Отправляет сообщение веб-элементу.

    Args:
        locator (SimpleNamespace | dict): Данные локатора.
        timeout (float): Время ожидания для поиска элемента (в секундах). По умолчанию 5.
        timeout_for_event (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
        message (str): Сообщение для отправки веб-элементу.
        typing_speed (float): Скорость ввода текста для событий send_keys (в секундах).

    Returns:
        bool: True, если сообщение было отправлено успешно, False в противном случае.
    """
```

**Назначение**: Отправляет сообщение веб-элементу.

**Параметры**:

-   `locator` (SimpleNamespace | dict): Данные локатора.
-   `timeout` (float): Время ожидания для поиска элемента (в секундах). По умолчанию 5.
-   `timeout_for_event` (str): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located'). По умолчанию 'presence_of_element_located'.
-   `message` (str): Сообщение для отправки веб-элементу.
-   `typing_speed` (float): Скорость ввода текста для событий send_keys (в секундах).

**Возвращает**:

-   `bool`: True, если сообщение было отправлено успешно, False в противном случае.

**Внутренние функции**:

-   `type_message`:

    ```python
    def type_message(
        el: WebElement,
        message: str,
        replace_dict: dict = {";": "SHIFT+ENTER"},
        typing_speed: float = typing_speed,
    ) -> bool:
        """Types a message into a web element with a specified typing speed."""
        message = message.split(" ")
        for word in message:
            word += " "
            try:
                for letter in word:
                    if letter in replace_dict.keys():
                        self.actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                    else:
                        self.actions.send_keys(letter)
                        self.actions.pause(typing_speed)
                        self.actions.perform()
            except Exception as ex:
                logger.error(f"Error typing message:/n message={print(message)},/n word={print(letter)},/n letter={print(letter)}/n", ex, False)
                continue
        return True
    ```

    **Назначение**: Вводит сообщение в веб-элемент с указанной скоростью ввода.

    **Параметры**:

    -   `el` (WebElement): Веб-элемент, в который нужно ввести сообщение.
    -   `message` (str): Сообщение для ввода.
    -   `replace_dict` (dict): Словарь для замены символов. По умолчанию {";": "SHIFT+ENTER"}.
    -   `typing_speed` (float): Скорость ввода текста (в секундах).

    **Возвращает**:

    -   `bool`: True, если сообщение было введено успешно, False в противном случае.

    **Как работает функция**:
    Функция разбивает сообщение на слова и перебирает каждое слово. Затем функция перебирает каждую букву в слове и, если буква есть в словаре `replace_dict`, заменяет ее на соответствующую комбинацию клавиш. В противном случае функция просто вводит букву в веб-элемент. После каждой буквы функция приостанавливает выполнение на указанное время.

**Как работает функция**:

1.  Функция получает веб-элемент с помощью `self.get_webelement_by_locator`.
2.  Функция перемещает фокус на веб-элемент с помощью `self.actions.move_to_element`.
3.  Функция вызывает `type_message` для ввода сообщения в веб-элемент.

**Примеры**:

Пример использования с сообщением:

```python
locator = SimpleNamespace(by="id", selector="myElement")
message = "Hello, world!"
result = await send_message(locator, message=message)
```