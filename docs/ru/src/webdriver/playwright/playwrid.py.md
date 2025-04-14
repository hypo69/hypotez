# Модуль `src.webdriver.playwright.playwrid`

## Обзор

Модуль `src.webdriver.playwright.playwrid` предоставляет класс `Playwrid`, который является подклассом `PlaywrightCrawler` из библиотеки `crawlee`. Этот класс предназначен для веб-скрапинга с использованием Playwright и предоставляет дополнительные возможности, такие как настройка параметров запуска браузера, профилей и опций запуска.

## Подробней

Модуль `Playwrid` расширяет функциональность `PlaywrightCrawler`, позволяя более гибко настраивать параметры запуска браузера. Это может быть полезно для эмуляции различных пользовательских окружений, обхода блокировок и решения других задач, связанных с веб-скрапингом. Класс использует библиотеку `crawlee` для управления процессом обхода веб-страниц и Playwright для взаимодействия с браузером.

## Классы

### `Playwrid`

**Описание**: Подкласс `PlaywrightCrawler`, предоставляющий дополнительные функциональные возможности для управления браузером Playwright.

**Наследует**:
- `PlaywrightCrawler`

**Атрибуты**:
- `driver_name` (str): Имя драйвера, по умолчанию 'playwrid'.
- `base_path` (Path): Путь к базовой директории модуля.
- `config` (SimpleNamespace): Объект, содержащий конфигурацию из файла `playwrid.json`.
- `context`: Контекст выполнения Playwright.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Playwrid`.
- `_set_launch_options`: Настраивает параметры запуска браузера Playwright.
- `start`: Запускает обход веб-страницы по указанному URL.
- `current_url`: Возвращает текущий URL браузера.
- `get_page_content`: Возвращает HTML-контент текущей страницы.
- `get_element_content`: Возвращает внутренний HTML-контент элемента по CSS-селектору.
- `get_element_value_by_xpath`: Возвращает текстовое значение элемента по XPath.
- `click_element`: Кликает на элемент по CSS-селектору.
- `execute_locator`: Выполняет локатор через исполнитель.

### `__init__`

```python
def __init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None:
    """
    Initializes the Playwright Crawler with the specified launch options, settings, and user agent.
    """
```

**Назначение**: Инициализирует экземпляр класса `Playwrid`, настраивая параметры запуска браузера и другие необходимые компоненты.

**Параметры**:
- `user_agent` (Optional[str]): User-agent для установки в браузере. По умолчанию `None`.
- `options` (Optional[List[str]]): Список опций командной строки для передачи в Playwright. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса `PlaywrightCrawler`.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса `PlaywrightCrawler`.

**Как работает функция**:

1. **Настройка опций запуска**: Функция вызывает метод `_set_launch_options` для конфигурации опций запуска браузера, включая user-agent и другие параметры.
2. **Инициализация исполнителя**: Создается экземпляр класса `PlaywrightExecutor`, который отвечает за выполнение действий в браузере.
3. **Инициализация родительского класса**: Вызывается конструктор родительского класса `PlaywrightCrawler` с передачей необходимых параметров. Если `PlaywrightCrawler` не принимает `launch_options`, они обрабатываются отдельно.
4. **Установка опций запуска (если необходимо)**: Если у экземпляра класса есть метод `set_launch_options`, то опции запуска устанавливаются через него. В противном случае требуется иная обработка опций запуска.

```
A: Вызов _set_launch_options для конфигурации опций запуска
↓
B: Создание экземпляра PlaywrightExecutor
↓
C: Инициализация PlaywrightCrawler с необходимыми параметрами
↓
D: Проверка наличия метода set_launch_options
├──> E1: Если есть, вызов set_launch_options для установки опций запуска
└──> E2: Если нет, иная обработка опций запуска (pass)
```

**Примеры**:

```python
browser = Playwrid(user_agent="CustomUserAgent", options=["--disable-web-security"])
```

### `_set_launch_options`

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
```

**Назначение**: Конфигурирует опции запуска для Playwright Crawler, объединяя параметры из конфигурационного файла, пользовательского user-agent и дополнительных опций командной строки.

**Параметры**:
- `user_agent` (Optional[str]): User-agent для установки в браузере. По умолчанию `None`.
- `options` (Optional[List[str]]): Список опций командной строки для передачи в Playwright. По умолчанию `None`.

**Возвращает**:
- `Dict[str, Any]`: Словарь с опциями запуска для Playwright.

**Как работает функция**:

1. **Инициализация опций запуска**: Создается словарь `launch_options` с базовыми опциями, такими как `headless` (из конфигурации) и `args` (опции командной строки из конфигурации).
2. **Добавление user-agent**: Если передан параметр `user_agent`, он добавляется в словарь `launch_options`.
3. **Объединение опций**: Если переданы дополнительные опции в параметре `options`, они добавляются к списку `args` в словаре `launch_options`.
4. **Возврат опций**: Функция возвращает получившийся словарь `launch_options`.

```
A: Инициализация словаря launch_options с базовыми опциями (headless, args)
↓
B: Проверка и добавление user_agent в launch_options (если передан)
↓
C: Проверка и добавление дополнительных опций в launch_options['args'] (если переданы)
↓
D: Возврат словаря launch_options
```

**Примеры**:

```python
launch_options = self._set_launch_options(user_agent="CustomUserAgent", options=["--disable-web-security"])
```

### `start`

```python
async def start(self, url: str) -> None:
    """
    Starts the Playwrid Crawler and navigates to the specified URL.

    :param url: The URL to navigate to.
    :type url: str
    """
```

**Назначение**: Запускает Playwright Crawler и переходит по указанному URL.

**Параметры**:
- `url` (str): URL для перехода.

**Как работает функция**:

1. **Логирование**: Записывает информационное сообщение о начале работы Playwright Crawler для указанного URL.
2. **Запуск исполнителя**: Запускает исполнитель (`self.executor`), который отвечает за управление браузером.
3. **Переход по URL**: Использует исполнитель для перехода по указанному URL.
4. **Запуск обхода**: Запускает основной процесс обхода страниц с использованием метода `super().run(url)`.
5. **Получение контекста**: Получает текущий контекст обхода страниц (`self.crawling_context`) и сохраняет его в `self.context`.
6. **Обработка исключений**: В случае возникновения исключения записывает критическую ошибку в лог.

```
A: Логирование начала работы Playwright Crawler
↓
B: Запуск исполнителя (self.executor)
↓
C: Переход по URL с использованием исполнителя
↓
D: Запуск обхода страниц (super().run(url))
↓
E: Получение и сохранение контекста обхода страниц
↓
F: Обработка исключений (логирование критической ошибки)
```

**Примеры**:

```python
await browser.start("https://www.example.com")
```

### `current_url`

```python
@property
def current_url(self) -> Optional[str]:
    """
    Returns the current URL of the browser.

    :returns: The current URL.
    :rtype: Optional[str]
    """
```

**Назначение**: Возвращает текущий URL браузера.

**Возвращает**:
- `Optional[str]`: Текущий URL или `None`, если контекст или страница не определены.

**Как работает функция**:

1. **Проверка контекста и страницы**: Проверяет, что контекст (`self.context`) и страница (`self.context.page`) определены.
2. **Получение URL**: Если контекст и страница существуют, возвращает URL текущей страницы.
3. **Возврат None**: Если контекст или страница не определены, возвращает `None`.

```
A: Проверка наличия контекста и страницы
├──> B1: Если контекст и страница есть, получение URL текущей страницы
└──> B2: Если контекста или страницы нет, возврат None
```

**Примеры**:

```python
url = browser.current_url
if url:
    print(f"Текущий URL: {url}")
```

### `get_page_content`

```python
def get_page_content(self) -> Optional[str]:
    """
    Returns the HTML content of the current page.

    :returns: HTML content of the page.
    :rtype: Optional[str]
    """
```

**Назначение**: Возвращает HTML-контент текущей страницы.

**Возвращает**:
- `Optional[str]`: HTML-контент страницы или `None`, если контекст или страница не определены.

**Как работает функция**:

1. **Проверка контекста и страницы**: Проверяет, что контекст (`self.context`) и страница (`self.context.page`) определены.
2. **Получение контента**: Если контекст и страница существуют, возвращает HTML-контент текущей страницы.
3. **Возврат None**: Если контекст или страница не определены, возвращает `None`.

```
A: Проверка наличия контекста и страницы
├──> B1: Если контекст и страница есть, получение HTML-контента страницы
└──> B2: Если контекста или страницы нет, возврат None
```

**Примеры**:

```python
html_content = browser.get_page_content()
if html_content:
    print(html_content[:200])
```

### `get_element_content`

```python
async def get_element_content(self, selector: str) -> Optional[str]:
    """
    Returns the inner HTML content of a single element on the page by CSS selector.

    :param selector: CSS selector for the element.
    :type selector: str
    :returns: Inner HTML content of the element, or None if not found.
    :rtype: Optional[str]
    """
```

**Назначение**: Возвращает внутренний HTML-контент элемента, найденного по CSS-селектору.

**Параметры**:
- `selector` (str): CSS-селектор элемента.

**Возвращает**:
- `Optional[str]`: Внутренний HTML-контент элемента или `None`, если элемент не найден или произошла ошибка.

**Как работает функция**:

1. **Проверка контекста и страницы**: Проверяет, что контекст (`self.context`) и страница (`self.context.page`) определены.
2. **Поиск элемента**: Если контекст и страница существуют, пытается найти элемент с использованием CSS-селектора.
3. **Получение контента**: Если элемент найден, возвращает его внутренний HTML-контент.
4. **Обработка исключений**: В случае возникновения исключения (например, элемент не найден) записывает предупреждение в лог и возвращает `None`.
5. **Возврат None**: Если контекст или страница не определены, возвращает `None`.

```
A: Проверка наличия контекста и страницы
├──> B1: Если контекст и страница есть, поиск элемента по CSS-селектору
│   ├──> C1: Если элемент найден, получение внутреннего HTML-контента
│   └──> C2: Если элемент не найден, обработка исключения (логирование и возврат None)
└──> B2: Если контекста или страницы нет, возврат None
```

**Примеры**:

```python
element_content = await browser.get_element_content("h1")
if element_content:
    print(element_content)
```

### `get_element_value_by_xpath`

```python
async def get_element_value_by_xpath(self, xpath: str) -> Optional[str]:
    """
    Returns the text value of a single element on the page by XPath.

    :param xpath: XPath of the element.
    :type xpath: str
    :returns: The text value of the element, or None if not found.
    :rtype: Optional[str]
    """
```

**Назначение**: Возвращает текстовое значение элемента, найденного по XPath.

**Параметры**:
- `xpath` (str): XPath элемента.

**Возвращает**:
- `Optional[str]`: Текстовое значение элемента или `None`, если элемент не найден или произошла ошибка.

**Как работает функция**:

1. **Проверка контекста и страницы**: Проверяет, что контекст (`self.context`) и страница (`self.context.page`) определены.
2. **Поиск элемента**: Если контекст и страница существуют, пытается найти элемент с использованием XPath.
3. **Получение значения**: Если элемент найден, возвращает его текстовое значение.
4. **Обработка исключений**: В случае возникновения исключения (например, элемент не найден) записывает предупреждение в лог и возвращает `None`.
5. **Возврат None**: Если контекст или страница не определены, возвращает `None`.

```
A: Проверка наличия контекста и страницы
├──> B1: Если контекст и страница есть, поиск элемента по XPath
│   ├──> C1: Если элемент найден, получение текстового значения
│   └──> C2: Если элемент не найден, обработка исключения (логирование и возврат None)
└──> B2: Если контекста или страницы нет, возврат None
```

**Примеры**:

```python
xpath_value = await browser.get_element_value_by_xpath("//head/title")
if xpath_value:
    print(xpath_value)
```

### `click_element`

```python
async def click_element(self, selector: str) -> None:
    """
    Clicks a single element on the page by CSS selector.

    :param selector: CSS selector of the element to click.
    :type selector: str
    """
```

**Назначение**: Кликает на элемент, найденный по CSS-селектору.

**Параметры**:
- `selector` (str): CSS-селектор элемента для клика.

**Как работает функция**:

1. **Проверка контекста и страницы**: Проверяет, что контекст (`self.context`) и страница (`self.context.page`) определены.
2. **Поиск элемента**: Если контекст и страница существуют, пытается найти элемент с использованием CSS-селектора.
3. **Клик на элемент**: Если элемент найден, выполняет клик на него.
4. **Обработка исключений**: В случае возникновения исключения (например, элемент не найден) записывает предупреждение в лог.

```
A: Проверка наличия контекста и страницы
├──> B1: Если контекст и страница есть, поиск элемента по CSS-селектору
│   ├──> C1: Если элемент найден, выполнение клика на элемент
│   └──> C2: Если элемент не найден, обработка исключения (логирование)
└──> B2: Если контекста или страницы нет, функция завершается
```

**Примеры**:

```python
await browser.click_element("button")
```

### `execute_locator`

```python
async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
    """
    Executes locator through executor

    :param locator: Locator data (dict or SimpleNamespace).
    :type locator: dict | SimpleNamespace
    :param message: Optional message for events.
    :type message: Optional[str]
    :param typing_speed: Optional typing speed for events.
    :type typing_speed: float
    :returns: Execution status.
    :rtype: str | List[str] | bytes | List[bytes] | bool
    """
```

**Назначение**: Выполняет локатор через исполнитель.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора.
- `message` (Optional[str]): Опциональное сообщение для событий.
- `typing_speed` (float): Опциональная скорость печати для событий.

**Возвращает**:
- `str | List[str] | bytes | List[bytes] | bool`: Статус выполнения.

**Как работает функция**:

1. **Вызов исполнителя**: Вызывает метод `execute_locator` у объекта `self.executor`, передавая параметры `locator`, `message` и `typing_speed`.
2. **Возврат результата**: Возвращает результат выполнения локатора, полученный от исполнителя.

```
A: Вызов execute_locator у self.executor с передачей параметров
↓
B: Возврат результата выполнения локатора
```

**Примеры**:

```python
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
```

## Примеры

В секции `if __name__ == "__main__":` представлен пример использования класса `Playwrid`. В этом примере создается экземпляр класса, запускается браузер, выполняются различные действия на странице (получение контента, клик на элемент) и выводятся результаты.
```