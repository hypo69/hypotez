### **Как использовать класс `Playwrid`**

=========================================================================================

Описание
-------------------------
Класс `Playwrid` - это подкласс `PlaywrightCrawler`, который предоставляет расширенные возможности для управления браузером Playwright. Он позволяет настраивать параметры запуска браузера, такие как user-agent и другие опции, а также предоставляет методы для взаимодействия с элементами на странице.

Шаги выполнения
-------------------------
1. **Инициализация класса `Playwrid`**:
   - Создайте экземпляр класса `Playwrid`, передав необходимые параметры, такие как `user_agent` и `options`.
   - Параметр `options` позволяет передавать дополнительные аргументы командной строки в браузер Playwright.
   - Функция `_set_launch_options` отвечает за настройку параметров запуска браузера, таких как headless режим, аргументы и user-agent.

2. **Запуск краулера**:
   - Вызовите метод `start(url)`, чтобы запустить краулер и перейти по указанному URL.
   - Этот метод запускает экземпляр `PlaywrightExecutor`, переходит по указанному URL-адресу и запускает краулер.

3. **Взаимодействие с элементами на странице**:
   - Используйте методы `get_page_content()`, `get_element_content(selector)`, `get_element_value_by_xpath(xpath)` и `click_element(selector)` для взаимодействия с элементами на странице.
   - Метод `get_page_content()` возвращает HTML-контент текущей страницы.
   - Метод `get_element_content(selector)` возвращает внутренний HTML-контент элемента, найденного по CSS-селектору.
   - Метод `get_element_value_by_xpath(xpath)` возвращает текстовое значение элемента, найденного по XPath.
   - Метод `click_element(selector)` выполняет клик по элементу, найденному по CSS-селектору.
   - Метод `execute_locator(locator, message, typing_speed)` выполняет операции с элементами, используя локаторы, определённые в формате словаря или `SimpleNamespace`.

4. **Получение текущего URL**:
   - Используйте свойство `current_url`, чтобы получить текущий URL страницы.

Пример использования
-------------------------

```python
    import asyncio
    from src.webdriver.playwright.playwrid import Playwrid

    async def main():
        # Инициализация браузера с опциями
        browser = Playwrid(options=["--headless"])
        
        # Запуск браузера и переход по URL
        await browser.start("https://www.example.com")
        
        # Получение HTML всего документа
        html_content = browser.get_page_content()
        if html_content:
            print(html_content[:200])  # Вывод первых 200 символов для примера
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