# Модуль PlaywrightExecutor

## Обзор

Модуль `src.webdriver.playwright.executor` предоставляет функциональность для взаимодействия с веб-элементами с использованием Playwright на основе предоставленных локаторов. Он обрабатывает парсинг локаторов, взаимодействие с элементами и обработку ошибок.

## Подробнее

Модуль `src.webdriver.playwright.executor` использует библиотеку Playwright для автоматизации взаимодействия с веб-браузерами. Он предоставляет класс `PlaywrightExecutor`, который позволяет выполнять действия на веб-страницах, такие как:

- получение атрибутов элементов
- выполнение событий (например, клики, отправка ключей, загрузка файлов)
- получение скриншотов элементов
- навигация по URL

Класс `PlaywrightExecutor` использует локаторы для определения местоположения элементов на веб-странице. Локатор может быть представлен в виде словаря или объекта `SimpleNamespace`. 

## Классы

### `PlaywrightExecutor`

**Описание**: Класс для взаимодействия с веб-элементами с использованием Playwright. 

**Наследует**: 

**Атрибуты**:

- `driver`: Объект Playwright Driver.
- `browser_type`: Тип браузера (например, `'chromium'`, `'firefox'`, `'webkit'`).
- `page`: Объект Playwright Page.
- `config`: Объект `SimpleNamespace`, содержащий конфигурационные параметры Playwright.

**Методы**:

- `start()`: Инициализирует Playwright и запускает браузер.
- `stop()`: Закрывает Playwright браузер и останавливает его экземпляр.
- `execute_locator(locator: Union[dict, SimpleNamespace], message: Optional[str] = None, typing_speed: float = 0, timeout: Optional[float] = 0, timeout_for_event: Optional[str] = 'presence_of_element_located')`: Выполняет действия на веб-элементе на основе предоставленного локатора.
- `evaluate_locator(attribute: str | List[str] | dict)`: Оценивает и обрабатывает атрибуты локатора.
- `get_attribute_by_locator(locator: dict | SimpleNamespace)`: Получает указанный атрибут из веб-элемента.
- `get_webelement_by_locator(locator: dict | SimpleNamespace)`: Получает веб-элемент с использованием локатора.
- `get_webelement_as_screenshot(locator: dict | SimpleNamespace, webelement: Optional[Locator] = None)`: Делает снимок экрана расположенного веб-элемента.
- `execute_event(locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0)`: Выполняет событие, связанное с локатором.
- `send_message(locator: dict | SimpleNamespace, message: str = None, typing_speed: float = 0)`: Отправляет сообщение веб-элементу.
- `goto(url: str)`: Переходит на указанный URL.

## Методы класса

### `start()`

**Назначение**: Инициализирует Playwright и запускает браузер.

**Параметры**:

-  

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
```

### `stop()`

**Назначение**: Закрывает Playwright браузер и останавливает его экземпляр.

**Параметры**:

-  

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    await executor.stop()
```


### `execute_locator()`

**Назначение**: Выполняет действия на веб-элементе на основе предоставленного локатора.

**Параметры**:

- `locator`: Локатор данных (словарь или `SimpleNamespace`).
- `message`: Необязательное сообщение для событий.
- `typing_speed`: Необязательная скорость ввода для событий.
- `timeout`: Время ожидания для поиска элемента (секунды).
- `timeout_for_event`: Условие ожидания (`'presence_of_element_located'`, `'visibility_of_all_elements_located'`).

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    locator = {"by": "XPATH", "selector": "//button[@id='submit']", "event": "click()"}
    await executor.execute_locator(locator)
```

### `evaluate_locator()`

**Назначение**: Оценивает и обрабатывает атрибуты локатора.

**Параметры**:

- `attribute`: Атрибут для оценки (может быть строкой, списком строк или словарем).

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    attribute = "{'key1': 'value1', 'key2': 'value2'}"
    evaluated_attribute = await executor.evaluate_locator(attribute)
    print(evaluated_attribute)
```


### `get_attribute_by_locator()`

**Назначение**: Получает указанный атрибут из веб-элемента.

**Параметры**:

- `locator`: Локатор данных (словарь или `SimpleNamespace`).

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    locator = {"by": "XPATH", "selector": "//input[@id='username']", "attribute": "value"}
    attribute_value = await executor.get_attribute_by_locator(locator)
    print(attribute_value)
```


### `get_webelement_by_locator()`

**Назначение**: Получает веб-элемент с использованием локатора.

**Параметры**:

- `locator`: Локатор данных (словарь или `SimpleNamespace`).

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    locator = {"by": "XPATH", "selector": "//input[@id='username']"}
    element = await executor.get_webelement_by_locator(locator)
    print(element)
```

### `get_webelement_as_screenshot()`

**Назначение**: Делает снимок экрана расположенного веб-элемента.

**Параметры**:

- `locator`: Локатор данных (словарь или `SimpleNamespace`).
- `webelement`: Локатор веб-элемента.

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    locator = {"by": "XPATH", "selector": "//input[@id='username']"}
    screenshot = await executor.get_webelement_as_screenshot(locator)
    print(screenshot)
```

### `execute_event()`

**Назначение**: Выполняет событие, связанное с локатором.

**Параметры**:

- `locator`: Локатор данных (словарь или `SimpleNamespace`).
- `message`: Необязательное сообщение для событий.
- `typing_speed`: Необязательная скорость ввода для событий.

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    locator = {"by": "XPATH", "selector": "//button[@id='submit']", "event": "click()"}
    await executor.execute_event(locator)
```

### `send_message()`

**Назначение**: Отправляет сообщение веб-элементу.

**Параметры**:

- `locator`: Информация о местоположении элемента на странице.
- `message`: Сообщение, которое будет отправлено веб-элементу.
- `typing_speed`: Скорость ввода сообщения в секундах.

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    locator = {"by": "XPATH", "selector": "//input[@id='search']"}
    await executor.send_message(locator, message="Hello, world!")
```

### `goto()`

**Назначение**: Переходит на указанный URL.

**Параметры**:

- `url`: URL, на который нужно перейти.

**Возвращает**:

-  

**Вызывает исключения**:

-  

**Пример**:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor
async def main():
    executor = PlaywrightExecutor()
    await executor.start()
    await executor.goto("https://www.google.com/")
```


## Параметры класса

- `browser_type`: Тип браузера, который будет запущен (например, `'chromium'`, `'firefox'`, `'webkit'`).

## Примеры

### Пример использования:

```python
from src.webdriver.playwright.executor import PlaywrightExecutor

async def main():
    executor = PlaywrightExecutor()
    await executor.start()

    # Найти кнопку "Поиск" на странице Google
    search_button_locator = {
        "by": "XPATH", 
        "selector": "//input[@name='q']", 
        "event": "click()"
    }

    # Нажать на кнопку "Поиск"
    await executor.execute_locator(search_button_locator)

    # Ввести текст в поле поиска
    search_field_locator = {
        "by": "XPATH",
        "selector": "//input[@name='q']",
        "event": "type('Python')"
    }

    await executor.execute_locator(search_field_locator)

    # Сделать снимок экрана поля поиска
    screenshot = await executor.get_webelement_as_screenshot(search_field_locator)
    print(screenshot)

    await executor.stop()

asyncio.run(main())