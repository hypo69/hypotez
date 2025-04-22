# Модуль `executor` для Playwright

## Обзор

Модуль `executor` предоставляет функциональность для взаимодействия с веб-элементами с использованием Playwright на основе предоставленных локаторов. Он обрабатывает разбор локаторов, взаимодействие с элементами и обработку ошибок.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для автоматизации взаимодействия с веб-страницами с использованием библиотеки Playwright. Он предоставляет класс `PlaywrightExecutor`, который позволяет выполнять различные действия с веб-элементами, такие как клики, ввод текста, получение атрибутов и т.д.

## Классы

### `PlaywrightExecutor`

**Описание**: Класс `PlaywrightExecutor` выполняет команды на основе локаторов в стиле executor, используя Playwright.

**Атрибуты**:
- `driver` (Optional[Playwright]): Драйвер Playwright.
- `browser_type` (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit'). По умолчанию 'chromium'.
- `page` (Optional[Page]): Страница Playwright.
- `config` (SimpleNamespace): Конфигурация Playwright, загруженная из файла `playwrid.json`.

**Методы**:
- `__init__(self, browser_type: str = 'chromium', **kwargs)`: Инициализирует экземпляр класса `PlaywrightExecutor`.
- `start(self) -> None`: Запускает Playwright и запускает экземпляр браузера.
- `stop(self) -> None`: Закрывает браузер Playwright и останавливает его экземпляр.
- `execute_locator(self, locator: Union[dict, SimpleNamespace], message: Optional[str] = None, typing_speed: float = 0, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = 'presence_of_element_located') -> Union[str, list, dict, Locator, bool, None]`: Выполняет действия с веб-элементом на основе предоставленного локатора.
- `evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]`: Вычисляет и обрабатывает атрибуты локатора.
- `get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]`: Получает указанный атрибут из веб-элемента.
- `get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]`: Получает веб-элемент, используя локатор.
- `get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]`: Делает скриншот найденного веб-элемента.
- `execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]`: Выполняет событие, связанное с локатором.
- `send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool`: Отправляет сообщение веб-элементу.
- `goto(self, url: str) -> None`: Переходит по указанному URL.

### `__init__`

```python
def __init__(self, browser_type: str = 'chromium', **kwargs):
    """
    Инициализирует Playwright executor.

    Args:
        browser_type (str): Тип браузера для запуска (например, 'chromium', 'firefox', 'webkit').
            По умолчанию 'chromium'.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `PlaywrightExecutor`.

**Параметры**:
- `browser_type` (str, optional): Тип браузера для запуска. По умолчанию 'chromium'.
- `**kwargs`: Дополнительные параметры.

**Как работает функция**:
- Устанавливает драйвер в `None`.
- Устанавливает тип браузера `browser_type`.
- Устанавливает страницу `page` в `None`.
- Загружает конфигурацию из файла `playwrid.json` в атрибут `config`.

### `start`

```python
async def start(self) -> None:
    """
    Инициализирует Playwright и запускает экземпляр браузера.
    """
    ...
```

**Назначение**: Инициализирует Playwright и запускает экземпляр браузера.

**Как работает функция**:
1.  Запускает Playwright.
2.  Запускает браузер указанного типа с настройками из `self.config.options`.
3.  Создает новую страницу в браузере.
4.  Обрабатывает исключения, логируя критическую ошибку, если запуск браузера не удался.

### `stop`

```python
async def stop(self) -> None:
    """
    Закрывает браузер Playwright и останавливает его экземпляр.
    """
    ...
```

**Назначение**: Закрывает браузер Playwright и останавливает его экземпляр.

**Как работает функция**:
1.  Закрывает текущую страницу, если она существует.
2.  Останавливает драйвер Playwright, если он существует.
3.  Устанавливает драйвер в `None`.
4.  Логирует информацию об успешной остановке Playwright.
5.  Обрабатывает исключения, логируя ошибку, если закрытие браузера не удалось.

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
        locator (Union[dict, SimpleNamespace]): Данные локатора.
        message (Optional[str]): Дополнительное сообщение для событий.
        typing_speed (float): Скорость печати для событий (в секундах).
        timeout (Optional[float]): Время ожидания для поиска элемента (в секундах).
        timeout_for_event (Optional[str]): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

    Returns:
        Union[str, list, dict, Locator, bool, None]: Результат операции.
    """
    ...
```

**Назначение**: Выполняет действия с веб-элементом на основе предоставленного локатора.

**Параметры**:
- `locator` (Union[dict, SimpleNamespace]): Данные локатора. Может быть словарем или экземпляром `SimpleNamespace`.
- `message` (Optional[str]): Дополнительное сообщение для событий.
- `typing_speed` (float): Скорость печати для событий (в секундах).
- `timeout` (Optional[float]): Время ожидания для поиска элемента (в секундах).
- `timeout_for_event` (Optional[str]): Условие ожидания ('presence_of_element_located', 'visibility_of_all_elements_located').

**Возвращает**:
- `Union[str, list, dict, Locator, bool, None]`: Результат операции, который может быть строкой, списком, словарем, экземпляром `Locator`, булевым значением или `None`.

**Внутренние функции**:

#### `_parse_locator`

```python
async def _parse_locator(
        locator: SimpleNamespace, message: Optional[str]
) -> Union[str, list, dict, Locator, bool, None]:
    """Выполняет разбор и исполнение инструкций локатора."""
    ...
```

**Назначение**: Выполняет разбор и исполнение инструкций локатора.

**Параметры**:
- `locator` (SimpleNamespace): Данные локатора.
- `message` (Optional[str]): Дополнительное сообщение для событий.

**Возвращает**:
- `Union[str, list, dict, Locator, bool, None]`: Результат операции.

**Как работает функция**:
1.  Проверяет наличие атрибутов `event` и `attribute` и отсутствие флага `mandatory`.
2.  Если `locator.attribute` и `locator.by` являются строками, пытается получить атрибут элемента.
3.  Если `locator.by` имеет значение "VALUE", возвращает значение атрибута.
4.  Если есть событие `locator.event`, выполняет событие.
5.  Если есть атрибут `locator.attribute`, получает атрибут элемента.
6.  Если `locator.selector` и `locator.by` являются списками, обрабатывает их как пары элементов.
7.  Если `locator.sorted` имеет значение "pairs", создает пары элементов и выполняет рекурсивно `_parse_locator` для каждой пары.
8.  Возвращает список пар элементов.
9.  В случае невыполнения условий возвращает `None`.

**Как работает функция `execute_locator`**:

1.  Преобразует `locator` в `SimpleNamespace`, если это словарь.
2.  Проверяет, что `locator` содержит атрибут `attribute` или `selector`. Если нет, возвращает `None`.
3.  Вызывает внутреннюю функцию `_parse_locator` для разбора и выполнения инструкций локатора.
4.  Возвращает результат выполнения `_parse_locator`.

### `evaluate_locator`

```python
async def evaluate_locator(self, attribute: str | List[str] | dict) -> Optional[str | List[str] | dict]:
    """
    Вычисляет и обрабатывает атрибуты локатора.

    Args:
        attribute (str | List[str] | dict): Атрибут для вычисления.

    Returns:
        Optional[str | List[str] | dict]: Вычисленный атрибут.
    """
    ...
```

**Назначение**: Вычисляет и обрабатывает атрибуты локатора.

**Параметры**:
- `attribute` (str | List[str] | dict): Атрибут для вычисления.

**Возвращает**:
- `Optional[str | List[str] | dict]`: Вычисленный атрибут.

**Внутренние функции**:

#### `_evaluate`

```python
async def _evaluate(attr: str) -> Optional[str]:
    return attr
```

**Назначение**: Просто возвращает переданный атрибут.

**Параметры**:
- `attr` (str): Атрибут для возврата.

**Возвращает**:
- `Optional[str]`: Переданный атрибут.

**Как работает функция `evaluate_locator`**:
1.  Если `attribute` является списком, применяет функцию `_evaluate` к каждому элементу списка и возвращает список результатов.
2.  Если `attribute` не является списком, преобразует его в строку и применяет функцию `_evaluate`.
3.  Возвращает результат выполнения `_evaluate`.

### `get_attribute_by_locator`

```python
async def get_attribute_by_locator(self, locator: dict | SimpleNamespace) -> Optional[str | List[str] | dict]:
    """
    Получает указанный атрибут из веб-элемента.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.

    Returns:
        Optional[str | List[str] | dict]: Атрибут или None.
    """
    ...
```

**Назначение**: Получает указанный атрибут из веб-элемента.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.

**Возвращает**:
- `Optional[str | List[str] | dict]`: Атрибут или `None`.

**Внутренние функции**:

#### `_parse_dict_string`

```python
def _parse_dict_string(attr_string: str) -> dict | None:
    """Разбирает строку типа '{attr1:attr2}' в словарь."""
    ...
```

**Назначение**: Разбирает строку типа '{attr1:attr2}' в словарь.

**Параметры**:
- `attr_string` (str): Строка для разбора.

**Возвращает**:
- `dict | None`: Словарь или `None`, если строка имеет неверный формат.

**Как работает функция**:
1.  Пытается преобразовать строку в словарь, разделяя ее на пары ключ-значение по символу `:`.
2.  Удаляет пробелы вокруг ключей и значений.
3.  Возвращает полученный словарь.
4.  В случае ошибки логирует отладочное сообщение и возвращает `None`.

#### `_get_attribute`

```python
async def _get_attribute(el: Locator, attr: str) -> Optional[str]:
    """Извлекает один атрибут из Locator."""
    ...
```

**Назначение**: Извлекает один атрибут из `Locator`.

**Параметры**:
- `el` (Locator): Элемент `Locator`.
- `attr` (str): Имя атрибута.

**Возвращает**:
- `Optional[str]`: Значение атрибута или `None` в случае ошибки.

**Как работает функция**:
1.  Пытается получить атрибут элемента с помощью метода `get_attribute`.
2.  В случае ошибки логирует отладочное сообщение и возвращает `None`.

#### `_get_attributes_from_dict`

```python
async def _get_attributes_from_dict(element: Locator, attr_dict: dict) -> dict:
    """Извлекает несколько атрибутов на основе словаря."""
    ...
```

**Назначение**: Извлекает несколько атрибутов на основе словаря.

**Параметры**:
- `element` (Locator): Элемент `Locator`.
- `attr_dict` (dict): Словарь атрибутов.

**Возвращает**:
- `dict`: Словарь атрибутов и их значений.

**Как работает функция**:
1.  Создает пустой словарь для результатов.
2.  Для каждой пары ключ-значение в `attr_dict` получает значение атрибута с помощью `_get_attribute` и сохраняет его в словаре результатов.
3.  Возвращает словарь результатов.

**Как работает функция `get_attribute_by_locator`**:

1.  Преобразует `locator` в `SimpleNamespace`, если это словарь.
2.  Получает веб-элемент с помощью `get_webelement_by_locator`.
3.  Если элемент не найден, возвращает `None`.
4.  Если `locator.attribute` является строкой и начинается с `{`, пытается разобрать строку в словарь с помощью `_parse_dict_string`.
5.  Если удалось разобрать строку в словарь, получает атрибуты из элемента с помощью `_get_attributes_from_dict`.
6.  Если элемент является списком, получает атрибуты для каждого элемента списка параллельно.
7.  Если `locator.attribute` не является строкой, получает атрибут из элемента с помощью `_get_attribute`.
8.  Возвращает полученный атрибут.

### `get_webelement_by_locator`

```python
async def get_webelement_by_locator(self, locator: dict | SimpleNamespace) -> Optional[Locator | List[Locator]]:
    """
    Получает веб-элемент, используя локатор.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.

    Returns:
        Optional[Locator | List[Locator]]: Playwright Locator
    """
    ...
```

**Назначение**: Получает веб-элемент, используя локатор.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.

**Возвращает**:
- `Optional[Locator | List[Locator]]`: `Locator` Playwright или `None`.

**Как работает функция**:

1.  Преобразует `locator` в `SimpleNamespace`, если это словарь.
2.  Если `locator` недействителен, регистрирует ошибку и возвращает `None`.
3.  В зависимости от значения `locator.by` (XPATH или другой) использует соответствующий метод для поиска элементов на странице.
4.  Если `locator.if_list` имеет значение 'all', возвращает все найденные элементы в виде списка.
5.  Если `locator.if_list` имеет значение 'first', возвращает первый найденный элемент.
6.  Если `locator.if_list` имеет значение 'last', возвращает последний найденный элемент.
7.  Если `locator.if_list` имеет значение 'even', возвращает список элементов с четными индексами.
8.  Если `locator.if_list` имеет значение 'odd', возвращает список элементов с нечетными индексами.
9.  Если `locator.if_list` является списком, возвращает список элементов с индексами, указанными в `locator.if_list`.
10. Если `locator.if_list` является целым числом, возвращает элемент с индексом `locator.if_list - 1`.
11. В противном случае возвращает `Locator`.
12. В случае возникновения исключения регистрирует ошибку и возвращает `None`.

### `get_webelement_as_screenshot`

```python
async def get_webelement_as_screenshot(self, locator: dict | SimpleNamespace, webelement: Optional[Locator] = None) -> Optional[bytes]:
    """
    Делает скриншот найденного веб-элемента.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.
        webelement (Optional[Locator]): Веб-элемент Locator.

    Returns:
        Optional[bytes]: Скриншот в байтах или None.
    """
    ...
```

**Назначение**: Делает скриншот найденного веб-элемента.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.
- `webelement` (Optional[Locator]): Веб-элемент `Locator`.

**Возвращает**:
- `Optional[bytes]`: Скриншот в байтах или `None`.

**Как работает функция**:

1.  Преобразует `locator` в `SimpleNamespace`, если это словарь.
2.  Если `webelement` не передан, получает веб-элемент с помощью `get_webelement_by_locator`.
3.  Если элемент не найден, регистрирует отладочное сообщение и возвращает `None`.
4.  Пытается сделать скриншот элемента с помощью метода `screenshot`.
5.  В случае возникновения исключения регистрирует ошибку и возвращает `None`.
6.  Возвращает скриншот в байтах.

### `execute_event`

```python
async def execute_event(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> Union[str, List[str], bytes, List[bytes], bool]:
    """
    Выполняет событие, связанное с локатором.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.
        message (Optional[str]): Дополнительное сообщение для событий.
        typing_speed (float): Скорость печати для событий (в секундах).

    Returns:
        Union[str, List[str], bytes, List[bytes], bool]: Статус выполнения.
    """
    ...
```

**Назначение**: Выполняет событие, связанное с локатором.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.
- `message` (Optional[str]): Дополнительное сообщение для событий.
- `typing_speed` (float): Скорость печати для событий (в секундах).

**Возвращает**:
- `Union[str, List[str], bytes, List[bytes], bool]`: Статус выполнения.

**Как работает функция**:

1.  Преобразует `locator` в `SimpleNamespace`, если это словарь.
2.  Разделяет строку `locator.event` на отдельные события по символу `;`.
3.  Получает веб-элемент с помощью `get_webelement_by_locator`.
4.  Если элемент не найден, регистрирует отладочное сообщение и возвращает `False`.
5.  Если элемент является списком, берет первый элемент списка.
6.  Для каждого события выполняет соответствующее действие:
    -   `click()`: Кликает на элемент.
    -   `pause(duration)`: Приостанавливает выполнение на указанное время в миллисекундах.
    -   `upload_media()`: Загружает медиафайл, указанный в `message`.
    -   `screenshot()`: Делает скриншот элемента.
    -   `clear()`: Очищает поле ввода.
    -   `send_keys(keys)`: Отправляет указанные клавиши элементу.
    -   `type(message)`: Вводит текст `message` в элемент.
7.  В случае возникновения исключения регистрирует ошибку и возвращает `False`.
8.  Возвращает `True`, если все события выполнены успешно.

### `send_message`

```python
async def send_message(self, locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0) -> bool:
    """Отправляет сообщение веб-элементу.

    Args:
         locator (dict | SimpleNamespace): Информация о местоположении элемента на странице.
         message (str): Сообщение для отправки веб-элементу.
         typing_speed (float): Скорость ввода сообщения в секундах.

    Returns:
        bool: Возвращает `True`, если сообщение было отправлено успешно, `False` в противном случае.
    """
    ...
```

**Назначение**: Отправляет сообщение веб-элементу.

**Параметры**:
- `locator` (dict | SimpleNamespace): Информация о местоположении элемента на странице.
- `message` (str): Сообщение для отправки веб-элементу.
- `typing_speed` (float): Скорость ввода сообщения в секундах.

**Возвращает**:
- `bool`: `True`, если сообщение отправлено успешно, `False` в противном случае.

**Как работает функция**:

1.  Преобразует `locator` в `SimpleNamespace`, если это словарь.
2.  Получает веб-элемент с помощью `get_webelement_by_locator`.
3.  Если элемент не найден, регистрирует отладочное сообщение и возвращает `False`.
4.  Если элемент является списком, берет первый элемент списка.
5.  Вводит текст `message` в элемент с указанной скоростью `typing_speed`.
6.  Возвращает `True`, если сообщение отправлено успешно.

### `goto`

```python
async def goto(self, url: str) -> None:
    """
    Переходит по указанному URL.

    Args:
        url (str): URL для перехода.
    """
    ...
```

**Назначение**: Переходит по указанному URL.

**Параметры**:
- `url` (str): URL для перехода.

**Как работает функция**:

1.  Переходит по указанному URL, используя метод `goto` страницы Playwright.
2.  В случае возникновения исключения регистрирует ошибку.