# Модуль `executor.py`

## Обзор

Модуль `executor.py` предоставляет функциональность для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.
Этот модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath), выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Подробнее

Этот модуль определяет класс `ExecuteLocator`, который инкапсулирует логику для выполнения действий над веб-элементами. Он использует Selenium для поиска элементов на веб-странице на основе заданных локаторов и выполнения различных операций, таких как клики, ввод текста и получение атрибутов. Модуль также включает обработку исключений, связанных с взаимодействием с веб-элементами, и ведение журнала для отслеживания процесса выполнения.

## Классы

### `ExecuteLocator`

**Описание**: Класс `ExecuteLocator` предназначен для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Принцип работы**:
Класс инициализируется с драйвером веб-браузера Selenium. Он содержит методы для поиска веб-элементов на странице, выполнения различных действий над ними (например, клик, ввод текста) и получения значений их атрибутов. Класс также обрабатывает исключения, которые могут возникнуть при взаимодействии с веб-элементами, и ведет журнал для отслеживания процесса выполнения.

**Аттрибуты**:

- `driver` (Optional[object]): Драйвер веб-браузера Selenium. По умолчанию `None`.
- `actions` (ActionChains): Объект ActionChains для выполнения последовательности действий. Инициализируется в методе `__post_init__`.
- `mode` (str): Режим работы (например, "debug"). По умолчанию "debug".

**Методы**:

- `__post_init__()`: Инициализирует объект `ActionChains` после создания экземпляра класса, если передан драйвер.
- `execute_locator(locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = "presence_of_element_located", message: Optional[str] = None, typing_speed: Optional[float] = 0) -> Optional[str | list | dict | WebElement | bool]`: Выполняет действия над веб-элементом на основе предоставленного локатора.
- `_evaluate_locator(attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
- `get_attribute_by_locator(locator: SimpleNamespace | dict, timeout: Optional[float] = 0, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0) -> Optional[WebElement | list[WebElement]]`: Извлекает атрибуты из веб-элемента или списка веб-элементов.
- `get_webelement_by_locator(locator: dict | SimpleNamespace, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = "presence_of_element_located") -> Optional[WebElement | List[WebElement]]`: Извлекает веб-элемент или список элементов на основе предоставленного локатора.
- `get_webelement_as_screenshot(locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: Optional[str] = None, typing_speed: float = 0, webelement: Optional[WebElement] = None) -> Optional[BinaryIO]`: Делает скриншот найденного веб-элемента.
- `execute_event(locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> Optional[str | list[str] | bytes | list[bytes] | bool]`: Выполняет событие, связанное с локатором.
- `send_message(locator: SimpleNamespace | dict, timeout: float = 5, timeout_for_event: str = "presence_of_element_located", message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.

## Функции

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
        timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').
        message: Optional message for actions like send_keys or type.
        typing_speed: Typing speed for send_keys events (seconds).

    Returns:
        The result of the operation, which can be a string, list, dict, WebElement, bool, or None.
    """
```

**Назначение**: Выполняет действия над веб-элементом на основе предоставленного локатора.

**Параметры**:

- `locator` (dict | SimpleNamespace): Данные локатора.
- `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию `0`.
- `timeout_for_event` (Optional[str]): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
- `message` (Optional[str]): Необязательное сообщение для действий, таких как `send_keys` или `type`. По умолчанию `None`.
- `typing_speed` (Optional[float]): Скорость печати для событий `send_keys` (в секундах). По умолчанию `0`.

**Возвращает**:

- `Optional[str | list | dict | WebElement | bool]`: Результат операции, который может быть строкой, списком, словарем, веб-элементом, булевым значением или `None`.

**Как работает функция**:

1.  **Преобразование локатора**: Если локатор является словарем, он преобразуется в объект `SimpleNamespace` для удобства доступа к атрибутам.
2.  **Проверка локатора**: Проверяется, что локатор не пустой (содержит атрибут или селектор).
3.  **Внутренняя функция `_parse_locator`**: Определяется внутренняя асинхронная функция `_parse_locator`, которая выполняет разбор инструкций локатора.
4.  **Обработка атрибутов**: Внутри `_parse_locator` происходит обработка атрибутов локатора, таких как `by` (метод поиска), `attribute` (атрибут для извлечения) и `event` (событие для выполнения).
5.  **Выполнение действий**: В зависимости от атрибутов локатора вызываются соответствующие методы для выполнения действий над веб-элементом, такие как получение атрибута, выполнение события или получение веб-элемента.
6.  **Обработка списков**: Если локатор содержит списки селекторов и методов поиска, выполняется итерация по этим спискам и вызывается `_parse_locator` для каждой пары.
7.  **Возврат результата**: Функция возвращает результат выполнения действий над веб-элементом.

**Внутренние функции**:

### `_parse_locator`
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

**Назначение**: Разбирает и выполняет инструкции, полученные из локатора. Эта функция обрабатывает различные типы локаторов и соответствующие им действия, такие как получение атрибутов, выполнение событий (например, клик) или получение веб-элементов.

**Параметры**:
- `locator` (SimpleNamespace): Объект, содержащий данные локатора, такие как метод поиска, селектор, атрибут, событие и другие параметры.
- `message` (Optional[str]): Необязательное сообщение, которое может использоваться при выполнении определенных действий, таких как ввод текста.
- `timeout` (Optional[float]): Максимальное время ожидания (в секундах) при поиске элемента.
- `timeout_for_event` (Optional[str]): Условие ожидания для события (например, "presence_of_element_located").
- `typing_speed` (Optional[float]): Скорость печати (в секундах) при вводе текста.

**Возвращает**:
`Optional[str | list | dict | WebElement | bool]`: Результат выполнения инструкции локатора. Это может быть строкой, списком, словарем, веб-элементом, булевым значением или `None`, если выполнение не удалось.

**Как работает функция**:
1. **Проверка флагов и атрибутов**:
   - Проверяет наличие обязательного флага (`mandatory`) при наличии события и атрибута в локаторе. Если флаг отсутствует, локатор пропускается.
2. **Обработка типа локатора**:
   - Приводит метод поиска (`locator.by`) к нижнему регистру.
   - Если метод поиска равен "value", возвращает атрибут локатора после его оценки.
   - Если метод поиска равен "url", извлекает значение параметра из URL текущей страницы.
3. **Выполнение действий**:
   - Если указано событие (`locator.event`), вызывает метод `execute_event` для выполнения соответствующего действия (например, клик).
   - Если указан атрибут (`locator.attribute`), вызывает метод `get_attribute_by_locator` для получения значения атрибута элемента.
   - Если не указаны ни событие, ни атрибут, вызывает метод `get_webelement_by_locator` для получения веб-элемента.
4. **Обработка списков**:
   - Если `locator.by` и `locator.selector` являются списками, обрабатывает их как пары элементов. Создает новые локаторы для каждой пары и рекурсивно вызывает `_parse_locator` для их обработки.
5. **Обработка ошибок**:
   - Логирует предупреждения, если локатор не содержит списки селекторов и методов поиска, или если значение `sorted` недействительно.
6. **Возврат результата**:
   - Возвращает результат выполнения инструкции локатора.

**ASCII flowchart**:

```
    [Проверка наличия mandatory флага]
        |
        V
    [Проверка типа локатора (locator.by)]
        |
        V
    [Обработка 'value', 'url']
        |
    [Вызов соответствующего метода]
        |
        V
    [Вызов execute_event, get_attribute_by_locator, get_webelement_by_locator]
        |
        V
    [Обработка списков (locator.by и locator.selector)]
        |
        V
    [Создание новых локаторов и рекурсивный вызов _parse_locator]
        |
        V
    [Возврат результата]
```

**Примеры**:

```python
# Пример 1: Получение атрибута 'href' из элемента с id 'myLink'
locator = {'by': 'id', 'selector': 'myLink', 'attribute': 'href'}
result = await execute_locator(locator)

# Пример 2: Клик на элемент с xpath '//button[@id="submit"]'
locator = {'by': 'xpath', 'selector': '//button[@id="submit"]', 'event': 'click()'}
result = await execute_locator(locator)

# Пример 3: Получение значения параметра 'token' из URL текущей страницы
locator = {'by': 'url', 'attribute': 'token'}
result = await execute_locator(locator)
```

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
```

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:

- `attribute` (str | List[str] | dict): Атрибут для вычисления (может быть строкой, списком строк или словарем).

**Возвращает**:

- `Optional[str | List[str] | dict]`: Вычисленный атрибут, который может быть строкой, списком строк или словарем.

**Как работает функция**:

1.  **Внутренняя функция `_evaluate`**: Определяется внутренняя функция `_evaluate`, которая выполняет вычисление отдельной строки атрибута.
2.  **Вычисление атрибута**: Если атрибут соответствует шаблону `%\\w+%`, он извлекает имя атрибута из `Keys` и возвращает соответствующее значение. В противном случае возвращает атрибут без изменений.
3.  **Обработка списка**: Если атрибут является списком, функция применяет `_evaluate` к каждому элементу списка и возвращает список вычисленных атрибутов.
4.  **Возврат результата**: Функция возвращает вычисленный атрибут.

**Внутренние функции**:

### `_evaluate`
```python
def _evaluate(attr: str) -> Optional[str]:
    """Evaluates single attribute string."""
    return getattr(Keys, re.findall(r"%(\\w+)%", attr)[0], None) if re.match(r"^%\\w+%", attr) else attr
```

**Назначение**: Вычисляет строку атрибута, заменяя специальные маркеры, такие как `%ENTER%`, соответствующими значениями из класса `Keys` библиотеки Selenium.

**Параметры**:
- `attr` (str): Строка атрибута для вычисления.

**Возвращает**:
`Optional[str]`: Вычисленная строка атрибута. Если маркер найден и заменен, возвращается соответствующее значение из класса `Keys`. В противном случае возвращается исходная строка атрибута.

**Как работает функция**:
1. **Проверка на наличие маркера**:
   - Использует регулярное выражение для проверки, начинается ли строка с маркера `%\\w+%`.
2. **Извлечение значения из Keys**:
   - Если маркер найден, извлекает имя ключа из маркера с помощью регулярного выражения.
   - Пытается получить соответствующее значение из класса `Keys` с помощью `getattr`.
3. **Возврат результата**:
   - Если значение найдено в классе `Keys`, возвращает это значение.
   - Если значение не найдено или маркер отсутствует, возвращает исходную строку атрибута.

**Примеры**:
```python
# Пример 1: Вычисление атрибута "%ENTER%"
attribute = "%ENTER%"
result = _evaluate(attribute)  # Результат: Keys.ENTER

# Пример 2: Вычисление атрибута "some_text"
attribute = "some_text"
result = _evaluate(attribute)  # Результат: "some_text"
```

**ASCII flowchart**:
```
    [Проверка: начинается ли строка с маркера `%\\w+%`]
        |
        V
    [Извлечение имени ключа из маркера]
        |
        V
    [Попытка получения значения из класса Keys]
        |
        V
    [Возврат значения из Keys или исходной строки]
```

**Примеры**:

```python
# Пример 1: Вычисление атрибута "%ENTER%"
attribute = "%ENTER%"
result = _evaluate_locator(attribute)

# Пример 2: Вычисление списка атрибутов ["%ENTER%", "some_text"]
attribute = ["%ENTER%", "some_text"]
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
```

**Назначение**: Извлекает атрибуты из веб-элемента или списка веб-элементов.

**Параметры**:

- `locator` (SimpleNamespace | dict): Данные локатора.
- `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию `0`.
- `timeout_for_event` (str): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
- `message` (Optional[str]): Не используется в этой функции.
- `typing_speed` (float): Не используется в этой функции.

**Возвращает**:

- `Optional[WebElement | list[WebElement]]`: Значение(я) атрибута в виде `WebElement`, списка `WebElement` или `None`, если не найдено.

**Как работает функция**:

1.  **Преобразование локатора**: Если локатор является словарем, он преобразуется в объект `SimpleNamespace` для удобства доступа к атрибутам.
2.  **Получение веб-элемента**: Вызывается метод `get_webelement_by_locator` для получения веб-элемента на основе предоставленного локатора.
3.  **Проверка наличия элемента**: Если веб-элемент не найден и атрибут `mandatory` установлен в `True`, функция логирует отладочное сообщение и возвращает `None`.
4.  **Внутренняя функция `_parse_dict_string`**: Определяется внутренняя функция `_parse_dict_string`, которая преобразует строку типа `'{attr1:attr2}'` в словарь.
5.  **Внутренняя функция `_get_attributes_from_dict`**: Определяется внутренняя функция `_get_attributes_from_dict`, которая извлекает значения атрибутов из `WebElement` на основе словаря.
6.  **Обработка атрибутов**: Если атрибут является строкой и начинается с `{`, функция вызывает `_parse_dict_string` для преобразования строки в словарь и `_get_attributes_from_dict` для извлечения значений атрибутов.
7.  **Обработка списка элементов**: Если `web_element` является списком, функция извлекает атрибуты для каждого элемента в списке и возвращает список значений атрибутов.
8.  **Извлечение атрибута**: Если `web_element` не является списком, функция извлекает значение атрибута с помощью метода `get_attribute` и возвращает его.
9.  **Возврат результата**: Функция возвращает значение(я) атрибута или `None`, если атрибут не найден.

**Внутренние функции**:

### `_parse_dict_string`
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

**Назначение**: Преобразует строку вида `'{attr1:attr2}'` в словарь.

**Параметры**:
- `attr_string` (str): Строка для преобразования в словарь.

**Возвращает**:
`dict | None`: Словарь, полученный из строки, или `None`, если строка имеет неверный формат.

**Как работает функция**:
1. **Удаление скобок**:
   - Удаляет начальные и конечные фигурные скобки из строки.
2. **Разделение на пары**:
   - Разделяет строку на пары ключ-значение, используя запятую в качестве разделителя.
3. **Разделение пары на ключ и значение**:
   - Разделяет каждую пару на ключ и значение, используя двоеточие в качестве разделителя.
4. **Создание словаря**:
   - Создает словарь, где ключи и значения очищаются от лишних пробелов.
5. **Обработка ошибок**:
   - Если строка имеет неверный формат, функция перехватывает исключение `ValueError`, логирует отладочное сообщение и возвращает `None`.

**Примеры**:
```python
# Пример 1: Преобразование строки '{attr1:attr2}' в словарь
attr_string = "{attr1:attr2}"
result = _parse_dict_string(attr_string)  # Результат: {'attr1': 'attr2'}

# Пример 2: Преобразование строки с лишними пробелами '{ attr1 : attr2 }' в словарь
attr_string = "{ attr1 : attr2 }"
result = _parse_dict_string(attr_string)  # Результат: {'attr1': 'attr2'}

# Пример 3: Неверный формат строки
attr_string = "attr1:attr2"
result = _parse_dict_string(attr_string)  # Результат: None
```

### `_get_attributes_from_dict`
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

**Назначение**: Извлекает значения атрибутов из веб-элемента на основе словаря, где ключи и значения словаря соответствуют именам атрибутов веб-элемента.

**Параметры**:
- `web_element` (WebElement): Веб-элемент, из которого извлекаются атрибуты.
- `attr_dict` (dict): Словарь, содержащий имена атрибутов для извлечения.

**Возвращает**:
`dict`: Словарь, содержащий извлеченные значения атрибутов. Если при извлечении атрибутов возникает ошибка, возвращается пустой словарь.

**Как работает функция**:
1. **Инициализация результата**:
   - Создает пустой словарь `result` для хранения извлеченных значений атрибутов.
2. **Перебор атрибутов в словаре**:
   - Перебирает пары ключ-значение в словаре `attr_dict`.
3. **Извлечение атрибутов**:
   - Для каждой пары пытается извлечь значения атрибутов из `web_element` с помощью метода `get_attribute`.
   - Ключ и значение из словаря используются как имена атрибутов для извлечения.
4. **Сохранение результата**:
   - Сохраняет извлеченные значения атрибутов в словаре `result`, где значение атрибута `attr_key` становится ключом, а значение атрибута `attr_value` становится значением.
5. **Обработка ошибок**:
   - Если при извлечении атрибутов возникает ошибка, функция перехватывает исключение, логирует отладочное сообщение и возвращает пустой словарь.
6. **Возврат результата**:
   - Возвращает словарь `result`, содержащий извлеченные значения атрибутов.

**Примеры**:
```python
# Пример:
web_element = ... # Предположим, что это WebElement
attr_dict = {"width": "height"}
result = _get_attributes_from_dict(web_element, attr_dict) # вернет словарь
```

**ASCII flowchart**:
```
[Инициализация словаря result = {}]
|
V
[Перебор каждой пары key, value в словаре attr_dict]
|
V
[Попытка извлечения значений атрибутов web_element.get_attribute(key) и web_element.get_attribute(value)]
|
V
[Сохранение значений в словаре result[attr_key] = attr_value]
|
V
[Если возникла ошибка, логирование и возврат {}]
|
V
[Возврат словаря result]
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
    Retrieves a web element or list of elements based on the provided locator.

    Args:
        locator: Locator data (dict or SimpleNamespace).
        timeout: Timeout for locating the element (seconds).
        timeout_for_event: Wait condition (\'presence_of_element_located\', \'visibility_of_all_elements_located\').

    Returns:
       WebElement, list of WebElements, or None if not found.
    """
```

**Назначение**: Извлекает веб-элемент или список элементов на основе предоставленного локатора.

**Параметры**:

- `locator` (dict | SimpleNamespace): Данные локатора.
- `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах). По умолчанию `0`.
- `timeout_for_event` (Optional[str]): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.

**Возвращает**:

- `Optional[WebElement | List[WebElement]]`: `WebElement`, список `WebElement` или `None`, если не найдено.

**Как работает функция**:

1.  **Получение времени ожидания**: Если предоставленное время ожидания (`timeout`) больше 0, оно используется. В противном случае используется атрибут `timeout` из объекта `locator`.
2.  **Внутренняя функция `_parse_elements_list`**: Определяется внутренняя асинхронная функция `_parse_elements_list`, которая фильтрует список веб-элементов на основе атрибута `if_list`.
3.  **Преобразование локатора**: Если локатор является словарем, он преобразуется в объект `SimpleNamespace` для удобства доступа к атрибутам.
4.  **Проверка локатора**: Проверяется, что локатор не является недействительным.
5.  **Поиск элементов**: В зависимости от значения `timeout` вызывается метод `find_elements` драйвера Selenium для поиска элементов. Если `timeout` равен 0, элементы ищутся немедленно. В противном случае используется `WebDriverWait` для ожидания появления элементов в течение заданного времени.
6.  **Фильтрация элементов**: Если элементы найдены, вызывается `_parse_elements_list` для фильтрации списка элементов на основе атрибута `if_list`.
7.  **Обработка исключений**: Если во время поиска элементов происходит исключение `TimeoutException`, функция логирует сообщение об ошибке и возвращает `None`. Если происходит другое исключение, функция также логирует сообщение об ошибке и возвращает `None`.
8.  **Возврат результата**: Функция возвращает веб-элемент, список веб-элементов или `None`, если элементы не найдены.

**Внутренние функции**:

### `_parse_elements_list`
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

**Назначение**: Фильтрует список веб-элементов на основе атрибута `if_list`, указанного в локаторе.

**Параметры**:
- `web_elements` (WebElement | List[WebElement]): Список веб-элементов для фильтрации.
- `locator` (SimpleNamespace): Объект, содержащий данные локатора, включая атрибут `if_list`.

**Возвращает**:
`Optional[WebElement | List[WebElement]]`: Отфильтрованный веб-элемент или список веб-элементов. Если входной параметр `web_elements` не является списком, он возвращается без изменений.

**Как работает функция**:
1. **Проверка типа входных данных**:
   - Проверяет, является ли `web_elements` списком. Если нет, возвращает `web_elements` без изменений.
2. **Извлечение атрибута `if_list`**:
   - Извлекает значение атрибута `if_list` из объекта `locator`.
3. **Фильтрация списка**:
   - В зависимости от значения `if_list` выполняет фильтрацию списка `web_elements`:
     - Если `if_list == "all"`: возвращает весь список.
     - Если `if_list == "first"`: возвращает первый элемент списка.
     - Если `if_list == "last"`: возвращает последний элемент списка.
     - Если `if_list == "even"`: возвращает список элементов с четными индексами.
     - Если `if_list == "odd"`: возвращает список элементов с нечетными индексами.
     - Если `if_list` является списком: возвращает список элементов, индексы которых указаны в `if_list`.
     - Если `if_list` является целым числом: возвращает элемент с индексом `if_list - 1`.
4. **Возврат результата**:
   - Возвращает отфильтрованный веб-элемент или список веб-элементов.

**ASCII flowchart**:
```
[Проверка: web_elements является списком?]
|
V
[Извлечение значения if_list из локатора]
|
V
[if_list == "all"?] --Y--> [Возврат web_elements]
|
[if_list == "first"?] --Y--> [Возврат web_elements[0]]
|
[if_list == "last"?] --Y--> [Возврат web_elements[-1]]
|
[if_list == "even"?] --Y--> [Возврат элементов с четными индексами]
|
[if_list == "odd"?] --Y--> [Возврат элементов с нечетными индексами]
|
[if_list является списком?] --Y--> [Возврат элементов с указанными индексами]
|
[if_list является целым числом?] --Y--> [Возврат web_elements[if_list - 1]]
|
[Возврат web_elements]
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
```

**Назначение**: Делает скриншот найденного веб-элемента.

**Параметры**:

-   `locator` (SimpleNamespace | dict): Данные локатора.
-   `timeout` (float): Время ожидания для поиска элемента (в секундах). По умолчанию 5.
-   `timeout_for_event` (str): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
-   `message` (Optional[str]): Не используется в этой функции.
-   `typing_speed` (float): Не используется в этой функции.
-   `webelement` (Optional[WebElement]): Предварительно полученный веб-элемент. По умолчанию `None`.

**Возвращает**:

-   `Optional[BinaryIO]`: Двоичный поток скриншота или `None` в случае неудачи.

**Как работает функция**:

1.  **Преобразование локатора**: Если локатор является словарем, он преобразуется в объект `SimpleNamespace` для удобства доступа к атрибутам.
2.  **Получение веб-