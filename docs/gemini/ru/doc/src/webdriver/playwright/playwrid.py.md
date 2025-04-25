# Модуль Playwrid - Playwright Crawler

## Обзор

Модуль `Playwrid` - это подкласс `PlaywrightCrawler`, который предоставляет дополнительную функциональность для работы с браузером Playwright. 

## Подробнее

`Playwrid` позволяет использовать Playwright для автоматизации задач веб-скрапинга и взаимодействия с веб-сайтами. 

- Модуль предоставляет возможность настройки параметров запуска Playwright (headless режим, опции браузера, user-agent), а также использует собственный класс `PlaywrightExecutor` для выполнения действий с веб-элементами. 
- В `Playwrid` определены методы для получения HTML-контента страницы, текста элементов по селектору, кликов по элементам, и другие. 
- Он использует локаторы (dictionaries or SimpleNamespace) для удобного управления взаимодействием с веб-элементами.
- Модуль использует `logger` из `src.logger.logger` для записи событий и ошибок в журнал.

## Классы

### `Playwrid`

**Описание**: Подкласс `PlaywrightCrawler` с дополнительной функциональностью для запуска браузера Playwright.

**Наследует**: `PlaywrightCrawler`

**Атрибуты**:
- `driver_name` (str): Имя драйвера, по умолчанию `'playwrid'`.
- `base_path` (Path): Путь к директории модуля Playwrid.
- `config` (SimpleNamespace): Настройки Playwrid, загруженные из `playwrid.json`.
- `context` (PlaywrightCrawlingContext): Контекст текущей сессии браузера.

**Методы**:

- `__init__(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None, *args, **kwargs) -> None`: Инициализирует Playwrid Crawler с заданными опциями запуска, настройками и user-agent.
- `_set_launch_options(self, user_agent: Optional[str] = None, options: Optional[List[str]] = None) -> Dict[str, Any]`: Конфигурирует опции запуска Playwright Crawler.
- `start(self, url: str) -> None`: Запускает Playwrid Crawler и переходит на указанный URL.
- `current_url(self) -> Optional[str]`: Возвращает текущий URL браузера.
- `get_page_content(self) -> Optional[str]`: Возвращает HTML-контент текущей страницы.
- `get_element_content(self, selector: str) -> Optional[str]`: Возвращает внутренний HTML-контент одного элемента на странице по CSS-селектору.
- `get_element_value_by_xpath(self, xpath: str) -> Optional[str]`: Возвращает текстовое значение одного элемента на странице по XPath.
- `click_element(self, selector: str) -> None`: Кликает по одному элементу на странице по CSS-селектору.
- `execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool`: Выполняет действие с веб-элементом по локатору.

## Параметры класса

- `user_agent` (Optional[str]): Строка User-Agent, которая будет использоваться для отправки запросов.
- `options` (Optional[List[str]]): Список опций Playwright, которые будут переданы во время инициализации.

## Примеры

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

## Методы класса

### `execute_locator`

```python
    async def execute_locator(self, locator: dict | SimpleNamespace, message: Optional[str] = None, typing_speed: float = 0) -> str | List[str] | bytes | List[bytes] | bool:
        """
        Выполняет действие с веб-элементом по локатору.

        :param locator: Данные локатора (dict или SimpleNamespace).
        :type locator: dict | SimpleNamespace
        :param message: Дополнительное сообщение для события.
        :type message: Optional[str]
        :param typing_speed: Скорость ввода для событий (в секундах).
        :type typing_speed: float
        :returns: Статус выполнения.
        :rtype: str | List[str] | bytes | List[bytes] | bool
        """
        return await self.executor.execute_locator(locator, message, typing_speed)
```

**Назначение**:  Выполняет действие с веб-элементом, используя локатор.

**Параметры**:
- `locator` (dict | SimpleNamespace): Данные локатора, определяющие тип поиска, селектор, и действие.
- `message` (Optional[str]): Дополнительное сообщение для события.
- `typing_speed` (float): Скорость ввода для событий (в секундах).

**Возвращает**:
- `str | List[str] | bytes | List[bytes] | bool`: Статус выполнения, который зависит от действия, выполняемого локатором.

**Примеры**:

```python
# Получение текста заголовка по XPATH
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

# Клик по кнопке по CSS селектору
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