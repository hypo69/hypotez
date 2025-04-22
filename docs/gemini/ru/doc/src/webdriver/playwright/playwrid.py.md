# Модуль `playwrid.py`

## Обзор

Модуль `playwrid.py` является частью проекта `hypotez` и предназначен для работы с веб-страницами с использованием Playwright. Он определяет класс `Playwrid`, который расширяет функциональность `PlaywrightCrawler` из библиотеки `crawlee`. Класс `Playwrid` предоставляет возможность настройки параметров запуска браузера, профилей и опций запуска с использованием Playwright.

## Подробнее

Модуль содержит класс `Playwrid`, который является подклассом `PlaywrightCrawler`. Он добавляет функциональность, такую как возможность установки пользовательских настроек браузера, профилей и параметров запуска с использованием Playwright.

## Классы

### `Playwrid`

**Описание**:
Класс `Playwrid` является подклассом `PlaywrightCrawler` и предоставляет расширенные возможности для управления браузером Playwright.

**Наследует**:
`PlaywrightCrawler`

**Атрибуты**:
- `driver_name` (str): Имя драйвера, по умолчанию 'playwrid'.
- `base_path` (Path): Путь к базовой директории модуля.
- `config` (SimpleNamespace): Конфигурация, загруженная из файла `playwrid.json`.
- `context`: Контекст выполнения Playwright.

**Методы**:
- `__init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None`: Инициализирует класс `Playwrid`.
- `_set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]`: Конфигурирует параметры запуска Playwright.
- `start(self, url: str) -> None`: Запускает Playwright и переходит по указанному URL.
- `current_url(self) -> Optional[str]`: Возвращает текущий URL браузера.
- `get_page_content(self) -> Optional[str]`: Возвращает HTML-контент текущей страницы.
- `get_element_content(self, selector: str) -> Optional[str]`: Возвращает внутренний HTML-контент элемента по CSS-селектору.
- `get_element_value_by_xpath(self, xpath: str) -> Optional[str]`: Возвращает текстовое значение элемента по XPath.
- `click_element(self, selector: str) -> None`: Кликает на элемент на странице по CSS-селектору.
- `execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool`: Выполняет локатор через executor.

## Методы класса

### `__init__`

```python
def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
    """
    Инициализирует Playwright Crawler с указанными параметрами запуска, настройками и user agent.

    Args:
        user_agent (Optional[str], optional): User-agent, который будет использоваться. По умолчанию `None`.
        options (Optional[List[str]], optional): Список опций Playwright, передаваемых при инициализации. По умолчанию `None`.
        *args: Произвольные позиционные аргументы.
        **kwargs: Произвольные именованные аргументы.

    Raises:
        Exception: Если PlaywrightCrawler не принимает launch_options.

    Как работает функция:
        1. Вызывает метод `_set_launch_options` для конфигурации параметров запуска.
        2. Создает экземпляр класса `PlaywrightExecutor`.
        3. Инициализирует родительский класс `PlaywrightCrawler` с параметрами, включая browser_type и другие аргументы.
        4. Если `PlaywrightCrawler` не принимает `launch_options` при инициализации, устанавливает их отдельно, используя метод `set_launch_options`, если он доступен.
    """
```

### `_set_launch_options`

```python
def _set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Конфигурирует параметры запуска для Playwright Crawler.

    Args:
        user_agent (Optional[str], optional): User-agent, который будет использоваться. По умолчанию `None`.
        options (Optional[List[str]], optional): Список опций Playwright, передаваемых при инициализации. По умолчанию `None`.

    Returns:
        Dict[str, Any]: Словарь с параметрами запуска для Playwright.

    Как работает функция:
        1. Инициализирует словарь `launch_options` значениями из конфигурации (`self.config`), если они доступны.
        2. Добавляет пользовательский user-agent, если он предоставлен.
        3. Объединяет пользовательские опции с опциями по умолчанию.
    """
```

### `start`

```python
async def start(self, url: str) -> None:
    """
    Запускает Playwrid Crawler и переходит по указанному URL.

    Args:
        url (str): URL для перехода.

    Raises:
        Exception: Если Playwrid Crawler завершается с ошибкой.

    Как работает функция:
        1. Логирует информацию о запуске Playwright Crawler.
        2. Запускает `PlaywrightExecutor`.
        3. Переходит по указанному URL, используя `executor.goto(url)`.
        4. Запускает стандартный процесс обхода, используя `super().run(url)`.
        5. Получает контекст обхода (`crawling_context`).
    """
```

### `current_url`

```python
@property
def current_url(self) -> Optional[str]:
    """
    Возвращает текущий URL браузера.

    Returns:
        Optional[str]: Текущий URL или None, если URL недоступен.

    Как работает функция:
        1. Проверяет, существует ли контекст обхода (`self.context`) и страница (`self.context.page`).
        2. Возвращает текущий URL страницы, если она доступна.
    """
```

### `get_page_content`

```python
def get_page_content(self) -> Optional[str]:
    """
    Возвращает HTML-контент текущей страницы.

    Returns:
        Optional[str]: HTML-контент страницы или None, если контент недоступен.

    Как работает функция:
        1. Проверяет, существует ли контекст обхода (`self.context`) и страница (`self.context.page`).
        2. Возвращает HTML-контент страницы, если она доступна.
    """
```

### `get_element_content`

```python
async def get_element_content(self, selector: str) -> Optional[str]:
    """
    Возвращает внутренний HTML-контент элемента по CSS-селектору.

    Args:
        selector (str): CSS-селектор элемента.

    Returns:
        Optional[str]: Внутренний HTML-контент элемента или None, если элемент не найден или произошла ошибка.

    Как работает функция:
        1. Проверяет, существует ли контекст обхода (`self.context`) и страница (`self.context.page`).
        2. Пытается найти элемент на странице по CSS-селектору.
        3. Возвращает внутренний HTML-контент элемента, если он найден.
        4. Логирует предупреждение, если элемент не найден или произошла ошибка при извлечении контента.
    """
```

### `get_element_value_by_xpath`

```python
async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]:
    """
    Возвращает текстовое значение элемента по XPath.

    Args:
        xpath (str): XPath элемента.

    Returns:
        Optional[str]: Текстовое значение элемента или None, если элемент не найден или произошла ошибка.

    Как работает функция:
        1. Проверяет, существует ли контекст обхода (`self.context`) и страница (`self.context.page`).
        2. Пытается найти элемент на странице по XPath.
        3. Возвращает текстовое значение элемента, если он найден.
        4. Логирует предупреждение, если элемент не найден или произошла ошибка при извлечении значения.
    """
```

### `click_element`

```python
async def click_element(self, selector: str) -> None:
    """
    Кликает на элемент на странице по CSS-селектору.

    Args:
        selector (str): CSS-селектор элемента для клика.

    Как работает функция:
        1. Проверяет, существует ли контекст обхода (`self.context`) и страница (`self.context.page`).
        2. Пытается найти элемент на странице по CSS-селектору.
        3. Кликает на элемент, если он найден.
        4. Логирует предупреждение, если элемент не найден или произошла ошибка при клике.
    """
```

### `execute_locator`

```python
async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
    """
    Выполняет локатор через executor.

    Args:
        locator (dict | SimpleNamespace): Данные локатора.
        message (Optional[str], optional): Сообщение для событий. По умолчанию `None`.
        typing_speed (float, optional): Скорость печати для событий. По умолчанию 0.

    Returns:
        str | List[str] | bytes | List[bytes] | bool: Статус выполнения.

    Как работает функция:
        1. Вызывает метод `execute_locator` класса `PlaywrightExecutor` для выполнения локатора.
        2. Возвращает статус выполнения.
    """
```

## Примеры

### Пример использования класса `Playwrid`

```python
if __name__ == "__main__":
    async def main():
        browser = Playwrid(options=["--headless"])
        await browser.start("https://www.example.com")
        
        # Получение HTML всего документа
        html_content = browser.get_page_content()
        if html_content:
            print(html_content[:200])  # Выведем первые 200 символов для примера
        else:
            print("Не удалось получить HTML-контент.")
        
        # Получение HTML элемента по селектору
        element_content = await browser.get_element_content("h1")
        if element_content:
            print("\nСодержимое элемента h1:")
            print(element_content)
        else:
            print("\nЭлемент h1 не найден.")
        
        # Получение значения элемента по xpath
        xpath_value = await browser.get_element_value_by_xpath("//head/title")
        if xpath_value:
             print(f"\nЗначение элемента по XPATH //head/title: {xpath_value}")
        else:
             print("\nЭлемент по XPATH //head/title не найден")

        # Нажатие на кнопку (при наличии)
        await browser.click_element("button")

        locator_name = {
        "attribute": "innerText",
        "by": "XPATH",
        "selector": "//h1",
        "if_list": "first",
        "use_mouse": False,
        "timeout": 0,
        "timeout_for_event": "presence_of_element_located",
        "event": None,
        "mandatory": True,
        "locator_description": "Название товара"
        }

        name = await browser.execute_locator(locator_name)
        print("Name:", name)

        locator_click = {
        "attribute": None,
        "by": "CSS",
        "selector": "button",
        "if_list": "first",
        "use_mouse": False,
        "timeout": 0,
        "timeout_for_event": "presence_of_element_located",
        "event": "click()",
        "mandatory": True,
        "locator_description": "название товара"
        }
        await browser.execute_locator(locator_click)
        await asyncio.sleep(3)
    asyncio.run(main())
```