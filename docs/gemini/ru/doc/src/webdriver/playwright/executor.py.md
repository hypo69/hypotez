# Модуль: Исполнитель Playwright

## Обзор

Модуль `executor.py` предоставляет функциональность для взаимодействия с веб-элементами с использованием Playwright на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для автоматизации взаимодействия с веб-страницами с использованием Playwright. Он предоставляет класс `PlaywrightExecutor`, который позволяет выполнять различные действия с веб-элементами, такие как клики, ввод текста, получение атрибутов и создание скриншотов.

## Классы

### `PlaywrightExecutor`

**Описание**: Класс `PlaywrightExecutor` выполняет команды на основе команд локаторов в стиле исполнителя, используя Playwright.

**Методы**:

- `__init__(self, browser_type: str = 'chromium', **kwargs)`: Инициализирует экземпляр класса `PlaywrightExecutor`.
- `start(self) -> None`: Запускает Playwright и запускает экземпляр браузера.
- `stop(self) -> None`: Закрывает браузер Playwright и останавливает его экземпляр.
- `execute_locator(self, locator: Union[dict, SimpleNamespace], message: Optional[str] = None, typing_speed: float = 0, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = 'presence_of_element_located') -> Union[str, list, dict, Locator, bool, None]`: Выполняет действия с веб-элементом на основе предоставленного локатора.
- `evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Оценивает и обрабатывает атрибуты локатора.
- `get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]`: Получает указанный атрибут из веб-элемента.
- `get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]`: Получает веб-элемент, используя локатор.
- `get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]`: Делает скриншот расположенного веб-элемента.
- `execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]`: Выполняет событие, связанное с локатором.
- `send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.
- `goto(self, url: str) -> None`: Переходит по указанному URL.

## Методы класса

### `__init__`

```python
def __init__(self, browser_type: str = 'chromium', **kwargs) -> None:
    """
    Инициализирует исполнитель Playwright.

    Args:
        browser_type (str): Тип запускаемого браузера (например, 'chromium', 'firefox', 'webkit'). По умолчанию 'chromium'.
        **kwargs: Дополнительные параметры.
    """
```

### `start`

```python
async def start(self) -> None:
    """
    Инициализирует Playwright и запускает экземпляр браузера.
    """
```
**Как работает функция**:
- Функция запускает асинхронный экземпляр Playwright.
- Запускает браузер указанного типа (по умолчанию chromium) в headless режиме с заданными опциями конфигурации.
- Создает новую страницу в браузере.
- В случае ошибки при запуске браузера, функция регистрирует критическую ошибку с использованием `logger.critical`.

**Примеры**:
```python
executor = PlaywrightExecutor(browser_type='chromium')
await executor.start()
```

### `stop`

```python
async def stop(self) -> None:
    """
    Закрывает браузер Playwright и останавливает его экземпляр.
    """
```
**Как работает функция**:
- Функция пытается закрыть текущую страницу браузера, если она существует.
- Останавливает драйвер Playwright, если он существует, и устанавливает его в `None`.
- Регистрирует информационное сообщение об остановке Playwright с использованием `logger.info`.
- В случае ошибки при закрытии браузера, функция регистрирует ошибку с использованием `logger.error`.

**Примеры**:
```python
executor = PlaywrightExecutor(browser_type='chromium')
await executor.start()
await executor.stop()
```

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
    Выполняет действия с веб-элементом на основе предоставленного локатора.

    Args:
        locator (Union[dict, SimpleNamespace]): Данные локатора (словарь или SimpleNamespace).
        message (Optional[str]): Необязательное сообщение для событий.
        typing_speed (float): Необязательная скорость печати для событий.
        timeout (Optional[float]): Время ожидания для обнаружения элемента (в секундах).
        timeout_for_event (Optional[str]): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

    Returns:
        Union[str, list, dict, Locator, bool, None]: Результат операции, который может быть строкой, списком, словарем, локатором, булевым значением или None.
    """
```
**Как работает функция**:
- Функция принимает локатор веб-элемента и выполняет действия на основе его атрибутов и событий.
- Если локатор является словарем, он преобразуется в объект `SimpleNamespace`.
- Вызывает внутреннюю асинхронную функцию `_parse_locator` для обработки локатора и выполнения связанных действий.
- Если локатор пустой, возвращает `None`.

**Внутренние функции**:
- `_parse_locator(locator: SimpleNamespace, message: Optional[str]) -> Union[str, list, dict, Locator, bool, None]`:
  - **Назначение**: Разбирает инструкции локатора и выполняет их.
  - **Параметры**:
    - `locator` (SimpleNamespace): Данные локатора.
    - `message` (Optional[str]): Необязательное сообщение для событий.
  - **Возвращает**: Результат операции, который может быть строкой, списком, словарем, локатором, булевым значением или `None`.
  - **Как работает**:
    - Проверяет наличие обязательных атрибутов и флагов.
    - В зависимости от типа и атрибутов локатора, вызывает соответствующие методы для получения атрибутов, выполнения событий или получения веб-элементов.
    - Обрабатывает локаторы, содержащие списки селекторов и атрибутов.
  - **Примеры**:
    ```python
    locator = SimpleNamespace(attribute='value', by='VALUE', selector='//div', event=None, mandatory=True, timeout=0, timeout_for_event='presence_of_element_located', locator_description='Описание локатора')
    result = await self.execute_locator(locator)
    ```

**Примеры**:
```python
locator = {'attribute': 'value', 'by': 'VALUE', 'selector': '//div', 'event': None, 'mandatory': True, 'timeout': 0, 'timeout_for_event': 'presence_of_element_located', 'locator_description': 'Описание локатора'}
result = await executor.execute_locator(locator, message='Test message', typing_speed=0.1)
```

### `evaluate_locator`

```python
async def evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
    """
    Оценивает и обрабатывает атрибуты локатора.

    Args:
        attribute (str | List[str] | dict): Атрибут для оценки (может быть строкой, списком строк или словарем).

    Returns:
        Optional[str | List[str] | dict]: Оцененный атрибут, который может быть строкой, списком строк или словарем.
    """
```
**Как работает функция**:
- Функция оценивает атрибуты локатора.
- Если атрибут является списком, она асинхронно оценивает каждый элемент списка.
- Если атрибут является строкой, она оценивает строку.

**Внутренние функции**:
- `_evaluate(attr: str) -> Optional[str]`:
  - **Назначение**: Оценивает строковый атрибут.
  - **Параметры**:
    - `attr` (str): Атрибут для оценки.
  - **Возвращает**: Оцененный атрибут.
  - **Как работает**:
    - Просто возвращает атрибут без изменений.

**Примеры**:
```python
attribute = 'test'
result = await executor.evaluate_locator(attribute)
```

### `get_attribute_by_locator`

```python
async def get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]:
    """
    Получает указанный атрибут из веб-элемента.

    Args:
        locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).

    Returns:
        Optional[str | List[str] | dict]: Атрибут или None.
    """
```
**Как работает функция**:
- Функция получает атрибут веб-элемента, используя предоставленный локатор.
- Сначала извлекает веб-элемент с помощью `get_webelement_by_locator`.
- Затем, в зависимости от типа атрибута, получает его значение и возвращает.

**Внутренние функции**:
- `_parse_dict_string(attr_string: str) -> dict | None`:
  - **Назначение**: Преобразует строку вида '{attr1:attr2}' в словарь.
  - **Параметры**:
    - `attr_string` (str): Строка для преобразования.
  - **Возвращает**: Словарь или `None` в случае ошибки.
  - **Как работает**:
    - Разбирает строку на пары ключ-значение и создает словарь.
- `_get_attribute(el: Locator, attr: str) -> Optional[str]`:
  - **Назначение**: Получает один атрибут из локатора.
  - **Параметры**:
    - `el` (Locator): Локатор элемента.
    - `attr` (str): Имя атрибута.
  - **Возвращает**: Значение атрибута или `None` в случае ошибки.
  - **Как работает**:
    - Пытается получить значение атрибута из элемента.
- `_get_attributes_from_dict(element: Locator, attr_dict: dict) -> dict`:
  - **Назначение**: Получает несколько атрибутов на основе словаря.
  - **Параметры**:
    - `element` (Locator): Локатор элемента.
    - `attr_dict` (dict): Словарь атрибутов.
  - **Возвращает**: Словарь с полученными атрибутами.
  - **Как работает**:
    - Итерируется по словарю атрибутов и получает значение каждого атрибута.

**Примеры**:
```python
locator = {'attribute': 'id', 'by': 'XPATH', 'selector': '//div'}
attribute = await executor.get_attribute_by_locator(locator)
```

### `get_webelement_by_locator`

```python
async def get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]:
    """
    Получает веб-элемент, используя локатор.

    Args:
        locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).

    Returns:
        Optional[Locator | List[Locator]]: Playwright Locator
    """
```
**Как работает функция**:
- Функция получает веб-элемент, используя предоставленный локатор.
- В зависимости от значения `locator.by`, функция использует либо `xpath`, либо `css selector` для поиска элементов на странице.
- В зависимости от значения `locator.if_list`, функция возвращает один элемент или список элементов.

**Примеры**:
```python
locator = {'by': 'XPATH', 'selector': '//div', 'if_list': 'all'}
elements = await executor.get_webelement_by_locator(locator)
```

### `get_webelement_as_screenshot`

```python
async def get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]:
    """
    Делает скриншот расположенного веб-элемента.

    Args:
        locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).
        webelement (Optional[Locator]): Веб-элемент Locator.

    Returns:
        Optional[bytes]: Скриншот в байтах или None.
    """
```
**Как работает функция**:
- Функция делает скриншот веб-элемента, используя предоставленный локатор.
- Если `webelement` не предоставлен, функция сначала пытается получить веб-элемент с помощью `get_webelement_by_locator`.
- Если веб-элемент не найден, возвращает `None`.

**Примеры**:
```python
locator = {'by': 'XPATH', 'selector': '//div'}
screenshot = await executor.get_webelement_as_screenshot(locator)
```

### `execute_event`

```python
async def execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]:
    """
    Выполняет событие, связанное с локатором.

    Args:
        locator (dict | SimpleNamespace): Данные локатора (словарь или SimpleNamespace).
        message (Optional[str]): Необязательное сообщение для событий.
        typing_speed (float): Необязательная скорость печати для событий.

    Returns:
        Union[str, List[str], bytes, List[bytes], bool]: Статус выполнения.
    """
```
**Как работает функция**:
- Функция выполняет событие, связанное с локатором, такое как клик, ввод текста, загрузка файла или создание скриншота.
- Функция разбирает строку `locator.event`, разделяя события по символу `;`.
- Для каждого события выполняется соответствующее действие.

**Примеры**:
```python
locator = {'by': 'XPATH', 'selector': '//button', 'event': 'click()'}
result = await executor.execute_event(locator)
```

### `send_message`

```python
async def send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool:
    """
    Отправляет сообщение веб-элементу.

    Args:
        locator (dict | SimpleNamespace): Информация о местоположении элемента на странице.
        message (str): Сообщение для отправки веб-элементу.
        typing_speed (float): Скорость печати сообщения в секундах.

    Returns:
        bool: Возвращает `True`, если сообщение было успешно отправлено, `False` в противном случае.
    """
```
**Как работает функция**:
- Функция отправляет сообщение веб-элементу, используя предоставленный локатор.
- Если `typing_speed` задана, функция отправляет сообщение посимвольно с заданной задержкой.

**Примеры**:
```python
locator = {'by': 'XPATH', 'selector': '//input'}
result = await executor.send_message(locator, message='test message', typing_speed=0.1)
```

### `goto`

```python
async def goto(self, url: str) -> None:
    """
    Переходит по указанному URL.

    Args:
        url (str): URL для перехода.
    """
```
**Как работает функция**:
- Функция переходит по указанному URL, используя метод `goto` объекта `self.page`.
- В случае ошибки при переходе, функция регистрирует ошибку с использованием `logger.error`.

**Примеры**:
```python
url = 'https://www.example.com'
await executor.goto(url)