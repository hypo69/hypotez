# Модуль `playwrid.py`

## Обзор

Модуль `playwrid.py` предоставляет класс `Playwrid`, который является подклассом `PlaywrightCrawler` из библиотеки `crawlee`. Этот класс расширяет функциональность `PlaywrightCrawler`, добавляя возможность настройки параметров запуска браузера, таких как пользовательский агент и опции командной строки. Модуль предназначен для использования в задачах веб-скрапинга и автоматизации, где требуется более гибкая настройка браузера Playwright.

## Подробнее

Модуль определяет класс `Playwrid`, который наследуется от `PlaywrightCrawler`. Класс `Playwrid` позволяет настраивать параметры запуска браузера, такие как `user_agent` и опции командной строки (`options`). Это позволяет более точно контролировать поведение браузера при выполнении задач скрапинга и автоматизации.

Класс использует библиотеку `crawlee` для управления браузером и выполнения запросов. Он также использует модуль `src.webdriver.playwright.executor` для выполнения JavaScript-кода в браузере.

В основной части модуля (`if __name__ == "__main__":`) представлен пример использования класса `Playwrid`. В этом примере создается экземпляр класса `Playwrid`, запускается браузер, выполняется навигация по URL, извлекается HTML-контент страницы и элемента, выполняется клик по элементу, а также выполняется локатор для получения имени товара.

## Классы

### `Playwrid`

**Описание**: Класс `Playwrid` является подклассом `PlaywrightCrawler` и предоставляет расширенные возможности для настройки и управления браузером Playwright.

**Наследует**: `PlaywrightCrawler`

**Атрибуты**:
- `driver_name` (str): Имя драйвера, по умолчанию `'playwrid'`.
- `base_path` (Path): Путь к базовой директории модуля.
- `config` (SimpleNamespace): Объект, содержащий конфигурационные параметры из файла `playwrid.json`.
- `context`: Контекст выполнения Playwright.

**Методы**:
- `__init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None`: Инициализирует класс `Playwrid` с заданными параметрами запуска, настройками и пользовательским агентом.
- `_set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]`: Конфигурирует параметры запуска для Playwright Crawler.
- `start(self, url: str) -> None`: Запускает Playwrid Crawler и переходит по указанному URL.
- `current_url(self) -> Optional[str]`: Возвращает текущий URL браузера.
- `get_page_content(self) -> Optional[str]`: Возвращает HTML-контент текущей страницы.
- `get_element_content(self, selector: str) -> Optional[str]`: Возвращает внутренний HTML-контент элемента на странице по CSS-селектору.
- `get_element_value_by_xpath(self, xpath: str) -> Optional[str]`: Возвращает текстовое значение элемента на странице по XPath.
- `click_element(self, selector: str) -> None`: Кликает на элемент на странице по CSS-селектору.
- `execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool`: Выполняет локатор через executor.

**Принцип работы**:
Класс `Playwrid` расширяет возможности `PlaywrightCrawler`, предоставляя более гибкие настройки запуска браузера. Он позволяет указывать пользовательский агент, опции командной строки и другие параметры, которые влияют на поведение браузера. Класс также предоставляет методы для извлечения контента страницы, взаимодействия с элементами и выполнения JavaScript-кода.

## Методы класса

### `__init__`

```python
def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None
```

**Назначение**: Инициализирует экземпляр класса `Playwrid`, настраивая параметры запуска браузера и передавая их в конструктор родительского класса `PlaywrightCrawler`.

**Параметры**:
- `user_agent` (Optional[str], optional): Пользовательский агент для браузера. По умолчанию `None`.
- `options` (Optional[List[str]], optional): Список опций командной строки для запуска браузера. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор `PlaywrightCrawler`.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор `PlaywrightCrawler`.

**Возвращает**: `None`

**Как работает функция**:
1. Вызывает метод `_set_launch_options` для настройки параметров запуска браузера на основе переданных аргументов `user_agent` и `options`.
2. Создает экземпляр класса `PlaywrightExecutor` для выполнения JavaScript-кода в браузере.
3. Вызывает конструктор родительского класса `PlaywrightCrawler`, передавая ему настроенные параметры запуска.
4. Если у класса `PlaywrightCrawler` есть метод `set_launch_options`, вызывает его для установки параметров запуска.

### `_set_launch_options`

```python
def _set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]
```

**Назначение**: Конфигурирует параметры запуска браузера Playwright.

**Параметры**:
- `user_agent` (Optional[str], optional): Пользовательский агент для браузера. По умолчанию `None`.
- `options` (Optional[List[str]], optional): Список опций командной строки для запуска браузера. По умолчанию `None`.

**Возвращает**: `Dict[str, Any]`: Словарь с параметрами запуска браузера.

**Как работает функция**:
1. Инициализирует словарь `launch_options` с параметрами по умолчанию, такими как `headless` (определяется из конфигурации) и `args` (опции командной строки, также из конфигурации).
2. Если передан аргумент `user_agent`, добавляет его в словарь `launch_options`.
3. Если переданы аргументы `options`, добавляет их в список опций командной строки `launch_options['args']`.
4. Возвращает словарь `launch_options` с настроенными параметрами запуска браузера.

### `start`

```python
async def start(self, url: str) -> None
```

**Назначение**: Запускает Playwrid Crawler и выполняет навигацию по указанному URL.

**Параметры**:
- `url` (str): URL для навигации.

**Возвращает**: `None`

**Как работает функция**:
1. Логирует информацию о начале запуска Playwright Crawler для указанного URL.
2. Запускает executor для выполнения JavaScript-кода.
3. Выполняет навигацию по указанному URL с помощью executor.
4. Вызывает метод `run` родительского класса `PlaywrightCrawler` для запуска процесса скрапинга.
5. Сохраняет контекст выполнения в атрибуте `context`.
6. Обрабатывает возможные исключения и логирует критическую ошибку.

### `current_url`

```python
@property
def current_url(self) -> Optional[str]
```

**Назначение**: Возвращает текущий URL браузера.

**Параметры**: Нет

**Возвращает**: `Optional[str]`: Текущий URL браузера или `None`, если URL не удалось получить.

**Как работает функция**:
1. Проверяет, существует ли контекст выполнения (`self.context`) и страницу (`self.context.page`).
2. Если контекст и страница существуют, возвращает текущий URL страницы.
3. В противном случае возвращает `None`.

### `get_page_content`

```python
def get_page_content(self) -> Optional[str]
```

**Назначение**: Возвращает HTML-контент текущей страницы.

**Параметры**: Нет

**Возвращает**: `Optional[str]`: HTML-контент текущей страницы или `None`, если контент не удалось получить.

**Как работает функция**:
1. Проверяет, существует ли контекст выполнения (`self.context`) и страницу (`self.context.page`).
2. Если контекст и страница существуют, возвращает HTML-контент страницы.
3. В противном случае возвращает `None`.

### `get_element_content`

```python
async def get_element_content(self, selector: str) -> Optional[str]
```

**Назначение**: Возвращает внутренний HTML-контент элемента на странице по CSS-селектору.

**Параметры**:
- `selector` (str): CSS-селектор элемента.

**Возвращает**: `Optional[str]`: Внутренний HTML-контент элемента или `None`, если элемент не найден или произошла ошибка.

**Как работает функция**:
1. Проверяет, существует ли контекст выполнения (`self.context`) и страницу (`self.context.page`).
2. Если контекст и страница существуют, пытается найти элемент на странице по CSS-селектору.
3. Если элемент найден, возвращает его внутренний HTML-контент.
4. Если элемент не найден или произошла ошибка, логирует предупреждение и возвращает `None`.

### `get_element_value_by_xpath`

```python
async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]
```

**Назначение**: Возвращает текстовое значение элемента на странице по XPath.

**Параметры**:
- `xpath` (str): XPath элемента.

**Возвращает**: `Optional[str]`: Текстовое значение элемента или `None`, если элемент не найден или произошла ошибка.

**Как работает функция**:
1. Проверяет, существует ли контекст выполнения (`self.context`) и страницу (`self.context.page`).
2. Если контекст и страница существуют, пытается найти элемент на странице по XPath.
3. Если элемент найден, возвращает его текстовое значение.
4. Если элемент не найден или произошла ошибка, логирует предупреждение и возвращает `None`.

### `click_element`

```python
async def click_element(self, selector: str) -> None
```

**Назначение**: Кликает на элемент на странице по CSS-селектору.

**Параметры**:
- `selector` (str): CSS-селектор элемента для клика.

**Возвращает**: `None`

**Как работает функция**:
1. Проверяет, существует ли контекст выполнения (`self.context`) и страницу (`self.context.page`).
2. Если контекст и страница существуют, пытается найти элемент на странице по CSS-селектору.
3. Если элемент найден, выполняет клик на элементе.
4. Если элемент не найден или произошла ошибка, логирует предупреждение.

### `execute_locator`

```python
async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool
```

**Назначение**: Выполняет локатор через executor.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.
- `message` (Optional[str], optional): Опциональное сообщение для событий. По умолчанию `None`.
- `typing_speed` (float): Скорость печати для событий.

**Возвращает**: `str | List[str] | bytes | List[bytes] | bool`: Статус выполнения.

**Как работает функция**:
1. Вызывает метод `execute_locator` объекта `self.executor`, передавая ему параметры `locator`, `message` и `typing_speed`.
2. Возвращает результат выполнения локатора.

## Параметры класса

- `driver_name` (str): Имя драйвера, по умолчанию `'playwrid'`.
- `base_path` (Path): Путь к базовой директории модуля.
- `config` (SimpleNamespace): Объект, содержащий конфигурационные параметры из файла `playwrid.json`.
- `context`: Контекст выполнения Playwright.

## Примеры

### Инициализация и запуск Playwrid Crawler

```python
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
        print("\\nСодержимое элемента h1:")
        print(element_content)
    else:
        print("\\nЭлемент h1 не найден.")

    # Получение значения элемента по xpath
    xpath_value = await browser.get_element_value_by_xpath("//head/title")
    if xpath_value:
        print(f"\\nЗначение элемента по XPATH //head/title: {xpath_value}")
    else:
        print("\\nЭлемент по XPATH //head/title не найден")

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