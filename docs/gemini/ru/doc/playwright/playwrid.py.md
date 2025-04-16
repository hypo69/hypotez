### Анализ кода модуля `src/webdriver/playwright/playwrid.py`

## Обзор

Этот модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee, предназначенную для автоматизации взаимодействия с веб-страницами.

## Подробней

Модуль `src/webdriver/playwright/playwrid.py` определяет класс `Playwrid`, который является подклассом `PlaywrightCrawler` из библиотеки Crawlee. Этот класс расширяет возможности стандартного обходчика Playwright, предоставляя гибкую настройку запуска браузера, а также методы для упрощения выполнения типовых задач, таких как навигация по страницам, извлечение контента и взаимодействие с элементами.

## Классы

### `Playwrid`

**Описание**: Подкласс `PlaywrightCrawler`, предоставляющий дополнительную функциональность для автоматизации браузера.

**Наследует**:

-   `crawlee.crawlers.PlaywrightCrawler`

**Атрибуты**:

-   `driver_name` (str): Имя драйвера ("playwrid").
-   `base_path` (Path): Базовый путь к файлам драйвера и конфигурации.
-   `config` (SimpleNamespace): Объект `SimpleNamespace`, содержащий настройки из файла `playwrid.json`.
-   `context`: Контекст обхода страниц Crawlee.

**Методы**:

-   `__init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None`: Инициализирует экземпляр класса `Playwrid`.
-   `_set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]`: Настраивает параметры запуска для Playwright.
-   `start(self, url: str) -> None`: Запускает Playwrid Crawler и переходит по указанному URL.
-   `current_url(self) -> Optional[str]`: Возвращает текущий URL браузера.
-   `get_page_content(self) -> Optional[str]`: Возвращает HTML-контент текущей страницы.
-   `get_element_content(self, selector: str) -> Optional[str]`: Возвращает внутренний HTML-контент одного элемента на странице по CSS-селектору.
-   `get_element_value_by_xpath(self, xpath: str) -> Optional[str]`: Возвращает текстовое значение одного элемента на странице по XPath.
-   `click_element(self, selector: str) -> None`: Кликает на элемент на странице по CSS-селектору.
-   `execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool`: Выполняет локатор через исполнитель.

#### `__init__`

**Назначение**: Инициализирует класс Playwrid, настраивая параметры запуска и User-Agent.

```python
def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
    """
    Initializes the Playwrid Crawler with the specified launch options, settings, and user agent.
    """
    ...
```

**Параметры**:

-   `user_agent` (Optional[str]): User-Agent для браузера.
-   `options` (Optional[List[str]]): Дополнительные опции для запуска браузера.
-    `*args`: Произвольные позиционные аргументы, передаваемые в конструктор базового класса.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор базового класса.

**Как работает функция**:

1.  Вызывает метод `_set_launch_options` для настройки параметров запуска браузера, включая User-Agent и дополнительные опции.
2.  Инициализирует исполнитель `PlaywrightExecutor`.
3.  Инициализирует базовый класс `PlaywrightCrawler` с заданными параметрами.

#### `_set_launch_options`

**Назначение**: Настраивает параметры запуска для Playwright.

```python
def _set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Configures the launch options for the Playwright Crawler.

    :param settings: A SimpleNamespace object containing launch settings.
    :type settings: SimpleNamespace
    :param user_agent: The user-agent string to be used.
    :type user_agent: Optional[str]
    :param options: A list of Playwright options to be passed during initialization.
    :type options: Optional[List[str]]
    :returns: A dictionary with launch options for Playwright.
    :rtype: Dict[str, Any]
    """
    ...
```

**Параметры**:

-   `user_agent` (Optional[str]): User-Agent для браузера.
-   `options` (Optional[List[str]]): Дополнительные опции для запуска браузера.

**Возвращает**:

-   `Dict[str, Any]`: Словарь с опциями запуска для Playwright.

**Как работает функция**:

1.  Инициализирует словарь `launch_options` с параметрами по умолчанию, такими как `headless` и `args`, беря их из файла конфигурации.
2.  Добавляет пользовательский User-Agent, если он указан.
3.  Объединяет пользовательские опции с опциями по умолчанию.
4.  Возвращает словарь с настроенными опциями запуска.

#### `start`

**Назначение**: Запускает Playwrid Crawler и переходит по указанному URL.

```python
async def start(self, url: str) -> None:
    """
    Starts the Playwrid Crawler and navigates to the specified URL.

    :param url: The URL to navigate to.
    :type url: str
    """
    ...
```

**Параметры**:

-   `url` (str): URL для перехода.

**Как работает функция**:

1.  Логирует информацию о начале запуска обходчика для указанного URL.
2.  Запускает экземпляр Playwright, используя `self.executor.start()`.
3.  Переходит по указанному URL, используя `self.executor.goto(url)`.
4.  Запускает обход страниц, используя `super().run(url)`.
5.  Сохраняет контекст обхода страниц в атрибуте `self.context`.

#### `current_url`

**Назначение**: Возвращает текущий URL браузера.

```python
@property
def current_url(self) -> Optional[str]:
    """
    Returns the current URL of the browser.

    :returns: The current URL.
    :rtype: Optional[str]
    """
    ...
```

**Возвращает**:

-   `Optional[str]`: Текущий URL браузера.

**Как работает функция**:

1.  Проверяет, существует ли контекст обхода страниц (`self.context`) и страницу (`self.context.page`).
2.  Если контекст и страница существуют, возвращает текущий URL страницы.

#### `get_page_content`

**Назначение**: Возвращает HTML-контент текущей страницы.

```python
def get_page_content(self) -> Optional[str]:
    """
    Returns the HTML content of the current page.

    :returns: HTML content of the page.
    :rtype: Optional[str]
    """
    ...
```

**Возвращает**:

-   `Optional[str]`: HTML-контент страницы.

**Как работает функция**:

1.  Проверяет, существует ли контекст обхода страниц (`self.context`) и страницу (`self.context.page`).
2.  Если контекст и страница существуют, возвращает содержимое страницы.

#### `get_element_content`

**Назначение**: Возвращает внутренний HTML-контент одного элемента на странице по CSS-селектору.

```python
async def get_element_content(self, selector: str) -> Optional[str]:
    """
    Returns the inner HTML content of a single element on the page by CSS selector.

    :param selector: CSS selector for the element.
    :type selector: str
    :returns: Inner HTML content of the element, or None if not found.
    :rtype: Optional[str]
    """
    ...
```

**Параметры**:

-   `selector` (str): CSS-селектор элемента.

**Возвращает**:

-   `Optional[str]`: Внутренний HTML-контент элемента или `None`, если элемент не найден.

**Как работает функция**:

1.  Проверяет, существует ли контекст обхода страниц (`self.context`) и страницу (`self.context.page`).
2.  Если контекст и страница существуют, находит элемент на странице с помощью `self.context.page.locator(selector)`.
3.  Возвращает внутренний HTML-контент элемента, используя `await element.inner_html()`.
4.  Логирует информацию об ошибках, используя `logger.warning`.

#### `get_element_value_by_xpath`

**Назначение**: Возвращает текстовое значение одного элемента на странице по XPath.

```python
async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]:
    """
    Returns the text value of a single element on the page by XPath.

    :param xpath: XPath of the element.
    :type xpath: str
    :returns: The text value of the element, or None if not found.
    :rtype: Optional[str]
    """
    ...
```

**Параметры**:

-   `xpath` (str): XPath элемента.

**Возвращает**:

-   `Optional[str]`: Текстовое значение элемента или `None`, если элемент не найден.

**Как работает функция**:

1.  Проверяет, существует ли контекст обхода страниц (`self.context`) и страницу (`self.context.page`).
2.  Если контекст и страница существуют, находит элемент на странице с помощью `self.page.locator(f'xpath={xpath}')`.
3.  Возвращает текстовое значение элемента, используя `await element.text_content()`.
4.  Логирует информацию об ошибках, используя `logger.warning`.

#### `click_element`

**Назначение**: Кликает на элемент на странице по CSS-селектору.

```python
async def click_element(self, selector: str) -> None:
    """
    Clicks a single element on the page by CSS selector.

    :param selector: CSS selector of the element to click.
    :type selector: str
    """
    ...
```

**Параметры**:

-   `selector` (str): CSS-селектор элемента для клика.

**Как работает функция**:

1.  Проверяет, существует ли контекст обхода страниц (`self.context`) и страницу (`self.context.page`).
2.  Если контекст и страница существуют, находит элемент на странице с помощью `self.page.locator(selector)`.
3.  Кликает на найденный элемент, используя `await element.click()`.
4.  Логирует информацию об ошибках, используя `logger.warning`.

#### `execute_locator`

**Назначение**: Выполняет локатор через исполнитель.

```python
async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
    """
    Executes locator through executor

     Args:
        locator: Locator data (dict or SimpleNamespace).
        message: Optional message for events.
        typing_speed: Optional typing speed for events.

    Returns:
       Execution status.
    """
    ...
```

**Параметры**:

-   `locator` (dict | SimpleNamespace): Информация о локаторе.
-   `message` (Optional[str]): Опциональное сообщение для событий.
-   `typing_speed` (float): Опциональная скорость набора текста для событий.

**Возвращает**:

-   Результат выполнения.

**Как работает функция**:

1. Выполняет локатор через исполнитель.

## Переменные модуля

-   `driver_name` (str): Имя драйвера ("playwrid").
-   `base_path` (Path): Базовый путь к файлам драйвера и конфигурации.
-   `config` (SimpleNamespace): Объект `SimpleNamespace`, содержащий настройки из файла `playwrid.json`.
-   `context`: Контекст обхода страниц Crawlee.
*Утилиты*
+ `locator.by`
+`message`
+`typing_speed`
+`self.executor`

## Пример использования

**Использование PlaywrightCrawler для сбора данных с веб-страницы:**

```python
from src.webdriver import Driver
from src.webdriver.playwright import Playwrid
from src.webdriver.playwright.executor import PlaywrightExecutor
from types import SimpleNamespace
import asyncio

# Инициализация драйвера
driver = Driver(Playwright)
await driver.start()
executor = PlaywrightExecutor(driver.driver)

# Пример локатора
locator = SimpleNamespace(
    by="xpath",
    selector="//input[@name='q']",
    attribute=None,
    event="type(Привет, мир!)",
    mandatory=True
)

async def main():
    # Переход на страницу
    await driver.goto("https://www.google.com")

    # Выполнение события с использованием локатора
    result = await executor.execute_locator(locator, typing_speed=0.1)
    print(f"Результат выполнения: {result}")

if __name__ == "__main__":
    asyncio.run(main())
await driver.stop()
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/webdriver/playwright/playwrid.py` зависит от библиотеки `playwright` и `crawlee`.
-   Он также использует модуль `src.logger.logger` для логирования и модуль `src.utils.jjson` для загрузки конфигурации.
-   Модуль `src/webdriver/playwright/executor.py` служит для выполнения запросов.