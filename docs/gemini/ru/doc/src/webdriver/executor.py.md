# Модуль для взаимодействия с веб-элементами с использованием Selenium
## Обзор

Модуль `src.webdriver.executor` предоставляет функциональность для взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов. Он обрабатывает парсинг локаторов, взаимодействие с элементами и обработку ошибок.

Этот модуль является ключевым компонентом для автоматизированного взаимодействия с веб-страницами. Он позволяет находить элементы на странице по различным локаторам (например, id, class, xpath), выполнять с ними различные действия (например, клик, ввод текста) и получать значения их атрибутов. Модуль также включает механизмы ожидания появления элементов и обработки возможных ошибок, таких как таймауты и перехваты кликов.

## Подробней

Модуль содержит класс `ExecuteLocator`, который используется для выполнения действий с веб-элементами на основе предоставленных локаторов. Локаторы могут быть представлены в виде словарей или объектов `SimpleNamespace`. Модуль поддерживает различные типы событий, такие как клики, ввод текста, загрузка медиа и снятие скриншотов.

## Классы

### `ExecuteLocator`

**Описание**: Класс `ExecuteLocator` предназначен для обработки взаимодействия с веб-элементами с использованием Selenium на основе предоставленных локаторов.

**Атрибуты**:
- `driver` (Optional[object]): Экземпляр веб-драйвера Selenium.
- `actions` (ActionChains): Объект ActionChains для выполнения последовательности действий.
- `mode` (str): Режим работы (по умолчанию "debug").

**Методы**:
- `__post_init__()`: Инициализирует объект `ActionChains` после создания экземпляра класса.
- `execute_locator()`: Выполняет действия над веб-элементом на основе предоставленного локатора.
- `_evaluate_locator()`: Выполняет оценку и обработку атрибутов локатора.
- `get_attribute_by_locator()`: Получает атрибуты веб-элемента или списка веб-элементов.
- `get_webelement_by_locator()`: Получает веб-элемент или список веб-элементов на основе предоставленного локатора.
- `get_webelement_as_screenshot()`: Делает скриншот найденного веб-элемента.
- `execute_event()`: Выполняет событие, связанное с локатором.
- `send_message()`: Отправляет сообщение веб-элементу.

**Принцип работы**:

Класс `ExecuteLocator` инициализируется с экземпляром веб-драйвера Selenium. Он предоставляет методы для поиска веб-элементов на странице, получения их атрибутов и выполнения различных действий, таких как клики, ввод текста и т.д. Локаторы используются для определения местоположения веб-элементов на странице. Класс также включает обработку ошибок, таких как таймауты и перехваты кликов.

## Методы класса

### `__post_init__`

```python
    def __post_init__(self):
        """Инициализирует объект ActionChains после создания экземпляра класса."""
        if self.driver:
            self.actions = ActionChains(self.driver)
```

**Назначение**: Инициализирует объект `ActionChains` после создания экземпляра класса `ExecuteLocator`.

**Как работает функция**:
- Если `self.driver` существует (то есть, если драйвер был передан при создании экземпляра `ExecuteLocator`), создается экземпляр `ActionChains`, связанный с этим драйвером, и присваивается атрибуту `self.actions`. `ActionChains` используется для выполнения сложных последовательностей действий, таких как перемещение мыши, нажатие клавиш и т.д.

**Примеры**:
```python
driver = Firefox()
executor = ExecuteLocator(driver = driver)
print(executor.actions) # <selenium.webdriver.common.action_chains.ActionChains object at 0x...>
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
- `locator` (dict | SimpleNamespace): Данные локатора.
- `timeout` (Optional[float]): Время ожидания для определения местоположения элемента (в секундах). По умолчанию `0`.
- `timeout_for_event` (Optional[str]): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
- `message` (Optional[str]): Необязательное сообщение для таких действий, как `send_keys` или `type`. По умолчанию `None`.
- `typing_speed` (Optional[float]): Скорость печати для событий `send_keys` (в секундах). По умолчанию `0`.

**Возвращает**:
- `Optional[str | list | dict | WebElement | bool]`: Результат операции, который может быть строкой, списком, словарем, веб-элементом, булевым значением или `None`.

**Внутренние функции**:
#### `_parse_locator`

```python
        async def _parse_locator(
            locator: SimpleNamespace,
            message: Optional[str] = None,
            timeout: Optional[float] = 0,
            timeout_for_event: Optional[str] = "presence_of_element_located",
            typing_speed: Optional[float] = 0,
        ) -> Optional[str | list | dict | WebElement | bool]:
            """Parses and executes locator instructions."""
            ...
```

**Назначение**: Разбирает и выполняет инструкции локатора.

**Как работает функция**:
1. **Проверка на пустой локатор**:
   - Если у локатора отсутствуют атрибуты `attribute` и `selector`, то функция логирует отладочное сообщение и возвращает `None`.
2. **Преобразование типов**:
   - Если `locator.by` является строкой, она преобразуется в нижний регистр.
   - Если присутствует атрибут `locator.attribute`, он оценивается с помощью метода `self._evaluate_locator`.
3. **Обработка атрибутов**:
   - Если `locator.by` равен `"value"`, функция возвращает `locator.attribute`.
   - Если `locator.by` равен `"url"`, функция извлекает параметр из URL текущей страницы и возвращает его значение.
4. **Выполнение событий и получение атрибутов**:
   - Если у локатора есть событие (`locator.event`), вызывается метод `self.execute_event`.
   - Если у локатора есть атрибут (`locator.attribute`), вызывается метод `self.get_attribute_by_locator`.
   - В противном случае вызывается метод `self.get_webelement_by_locator`.
5. **Обработка списков**:
   - Если `locator.selector` и `locator.by` являются списками, функция создает пары элементов и рекурсивно вызывает `_parse_locator` для каждой пары.
6. **Обработка некорректных локаторов**:
   - Если локатор не содержит списки `selector` и `by` или значение `sorted` невалидно, функция логирует предупреждение.

**Примеры**:
```python
locator = {
    "by": "id",
    "selector": "some_id",
    "attribute": "value"
}
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
        ...
```

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:
- `attribute` (str | List[str] | dict): Атрибут для вычисления (может быть строкой, списком строк или словарем).

**Возвращает**:
- `Optional[str | List[str] | dict]`: Вычисленный атрибут, который может быть строкой, списком строк или словарем.

**Внутренние функции**:
#### `_evaluate`

```python
        def _evaluate(attr: str) -> Optional[str]:
            """Evaluates single attribute string."""
            return getattr(Keys, re.findall(r"%(\\w+)%", attr)[0], None) if re.match(r"^%\\w+%", attr) else attr
```

**Назначение**: Вычисляет одну строку атрибута.

**Как работает функция**:
- Если строка `attr` соответствует шаблону `^%\w+%`, функция пытается получить соответствующий атрибут из класса `Keys` (например, `Keys.ENTER`). Если соответствие найдено, возвращается значение атрибута; в противном случае возвращается `None`.
- Если строка `attr` не соответствует указанному шаблону, функция возвращает `attr` без изменений.

**Примеры**:

```python
attribute = "%ENTER%"
result = _evaluate_locator(attribute) # Keys.ENTER

attribute = "some_attribute"
result = _evaluate_locator(attribute) # "some_attribute"
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
        ...
```

**Назначение**: Извлекает атрибуты из веб-элемента или списка веб-элементов.

**Параметры**:
- `locator` (SimpleNamespace | dict): Данные локатора.
- `timeout` (Optional[float]): Время ожидания для определения местоположения элемента (в секундах). По умолчанию `0`.
- `timeout_for_event` (str): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
- `message` (Optional[str]): Не используется в этой функции.
- `typing_speed` (float): Не используется в этой функции.

**Возвращает**:
- `Optional[WebElement | list[WebElement]]`: Значение(я) атрибута в виде WebElement, списка WebElements или None, если не найдено.

**Внутренние функции**:

#### `_parse_dict_string`

```python
        def _parse_dict_string(attr_string: str) -> dict | None:
            """Parses a string like \'{attr1:attr2}\' into a dictionary."""
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

**Как работает функция**:
1. **Разбор строки**:
   - Функция пытается разделить входную строку `attr_string` на пары ключ-значение, используя двоеточие `:` в качестве разделителя.
   - Затем пары разделяются запятыми `,`.
2. **Создание словаря**:
   - Для каждой пары создается элемент словаря, где ключ и значение очищаются от лишних пробелов с помощью `strip()`.
3. **Обработка ошибок**:
   - Если формат строки не соответствует ожидаемому, возникает исключение `ValueError`, которое перехватывается. В этом случае функция логирует отладочное сообщение и возвращает `None`.

**Примеры**:

```python
attr_string = "{attr1:attr2, attr3:attr4}"
result = _parse_dict_string(attr_string) # {'attr1': 'attr2', 'attr3': 'attr4'}

attr_string = "invalid_string"
result = _parse_dict_string(attr_string) # None
```

#### `_get_attributes_from_dict`

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
                    logger.debug(f"Error retrieving attributes \'{key}\' or \'{value}\' from element.", ex)
                    return {}
            return result
```

**Назначение**: Извлекает значения атрибутов из WebElement на основе словаря.

**Как работает функция**:
1. **Перебор элементов словаря**:
   - Функция перебирает все пары ключ-значение в словаре `attr_dict`.
2. **Извлечение атрибутов**:
   - Для каждого ключа и значения функция пытается получить соответствующие атрибуты из `web_element` с помощью метода `get_attribute()`.
3. **Формирование результата**:
   - Если атрибуты успешно извлечены, они добавляются в словарь `result`.
4. **Обработка ошибок**:
   - Если происходит ошибка при извлечении атрибутов, функция логирует отладочное сообщение и возвращает пустой словарь.

**Примеры**:

```python
attr_dict = {"attr1": "attr2", "attr3": "attr4"}
result = _get_attributes_from_dict(web_element, attr_dict) # {'value1': 'value2'}
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
        ...
```

**Назначение**: Получает веб-элемент или список элементов на основе предоставленного локатора.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.
- `timeout` (Optional[float]): Время ожидания для определения местоположения элемента (в секундах). По умолчанию `0`.
- `timeout_for_event` (Optional[str]): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.

**Возвращает**:
- `Optional[WebElement | List[WebElement]]`: WebElement, список WebElements или None, если не найдено.

**Внутренние функции**:

#### `_parse_elements_list`

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

**Как работает функция**:
1. **Проверка на список**:
   - Если `web_elements` не является списком, функция возвращает `web_elements` без изменений.
2. **Обработка атрибута `if_list`**:
   - В зависимости от значения `locator.if_list`, функция возвращает различные подмножества списка `web_elements`:
     - `"all"`: возвращает весь список.
     - `"first"`: возвращает первый элемент списка.
     - `"last"`: возвращает последний элемент списка.
     - `"even"`: возвращает элементы с четными индексами.
     - `"odd"`: возвращает элементы с нечетными индексами.
     - `list`: возвращает элементы с индексами, указанными в списке.
     - `int`: возвращает элемент с указанным индексом (индекс начинается с 1).

**Примеры**:
```python
web_elements = [element1, element2, element3, element4]
locator = SimpleNamespace(if_list="first")
result = _parse_elements_list(web_elements, locator) # element1

locator = SimpleNamespace(if_list="even")
result = _parse_elements_list(web_elements, locator) # [element1, element3]
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
        ...
```

**Назначение**: Делает скриншот найденного веб-элемента.

**Параметры**:
- `locator` (SimpleNamespace | dict): Данные локатора.
- `timeout` (float): Время ожидания для определения местоположения элемента (в секундах). По умолчанию `5`.
- `timeout_for_event` (str): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
- `message` (Optional[str]): Не используется в этой функции.
- `typing_speed` (float): Не используется в этой функции.
- `webelement` (Optional[WebElement]): Предварительно полученный веб-элемент.

**Возвращает**:
- `Optional[BinaryIO]`: BinaryIO stream скриншота или None, если не удалось.

**Как работает функция**:
1. **Определение веб-элемента**:
   - Если `webelement` не передан, функция пытается получить веб-элемент с помощью метода `self.get_webelement_by_locator`.
2. **Создание скриншота**:
   - Если веб-элемент найден, функция вызывает метод `screenshot_as_png` для создания скриншота в формате PNG.
3. **Обработка ошибок**:
   - Если происходит ошибка при создании скриншота, функция логирует ошибку и возвращает `None`.

**Примеры**:
```python
locator = {"by": "id", "selector": "element_id"}
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
- `locator` (SimpleNamespace | dict): Данные локатора.
- `timeout` (float): Время ожидания для определения местоположения элемента (в секундах). По умолчанию `5`.
- `timeout_for_event` (str): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
- `message` (str): Необязательное сообщение для отправки с событием.
- `typing_speed` (float): Скорость печати для событий `send_keys` (в секундах).

**Возвращает**:
- `Optional[str | list[str] | bytes | list[bytes] | bool]`: Результат выполнения события (str, list of str, bytes, list of bytes, или bool).

**Как работает функция**:
1. **Разбор событий**:
   - Функция разделяет строку `locator.event` на отдельные события, используя символ `;` в качестве разделителя.
2. **Определение веб-элемента**:
   - Функция пытается получить веб-элемент с помощью метода `self.get_webelement_by_locator`.
3. **Выполнение событий**:
   - Для каждого события функция выполняет соответствующее действие:
     - `"click()"`: вызывает метод `click()` для веб-элемента.
     - `"pause(duration)"`: приостанавливает выполнение на указанное время (в секундах).
     - `"upload_media()"`: отправляет сообщение (путь к файлу) в веб-элемент для загрузки медиа.
     - `"screenshot()"`: делает скриншот веб-элемента.
     - `"clear()"`: очищает содержимое веб-элемента.
     - `"send_keys(keys)"`: отправляет указанные клавиши в веб-элемент.
     - `"type(message)"`: отправляет сообщение в веб-элемент, печатая каждый символ с указанной скоростью.

**Примеры**:
```python
locator = {"by": "id", "selector": "element_id", "event": "click()"}
result = await execute_event(locator)

locator = {"by": "id", "selector": "element_id", "event": "type(hello)"}
result = await execute_event(locator, typing_speed=0.1)
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
- `locator` (SimpleNamespace | dict): Данные локатора.
- `timeout` (float): Время ожидания для определения местоположения элемента (в секундах). По умолчанию `5`.
- `timeout_for_event` (str): Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`). По умолчанию `'presence_of_element_located'`.
- `message` (str): Сообщение для отправки веб-элементу.
- `typing_speed` (float): Скорость печати для событий `send_keys` (в секундах).

**Возвращает**:
- `bool`: True, если сообщение было успешно отправлено, False в противном случае.

**Внутренние функции**:

#### `type_message`

```python
        def type_message(
            el: WebElement,
            message: str,
            replace_dict: dict = {";": "SHIFT+ENTER"},\
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

**Назначение**: Печатает сообщение в веб-элемент с указанной скоростью печати.

**Как работает функция**:
1. **Разделение сообщения на слова**:
   - Функция разделяет сообщение на отдельные слова, используя пробел в качестве разделителя.
2. **Перебор символов в слове**:
   - Для каждого символа в слове функция выполняет следующие действия:
     - Если символ находится в словаре `replace_dict`, функция отправляет соответствующую комбинацию клавиш (например, `SHIFT+ENTER`).
     - В противном случае функция отправляет символ в веб-элемент и приостанавливает выполнение на указанное время (`typing_speed`).

**Примеры**:
```python
message = "hello; world"
result = type_message(webelement, message, replace_dict={";": "SHIFT+ENTER"}, typing_speed=0.1)
```