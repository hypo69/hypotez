## Как использовать Playwrid -  Playwright Crawler с дополнительной функциональностью

=========================================================================================

Описание
-------------------------
`Playwrid` - это подкласс `PlaywrightCrawler`, который расширяет функциональность Playwright для работы с веб-страницами. 
Он позволяет:

- Устанавливать  настройки браузера и профили;
- Задавать опции запуска браузера с помощью Playwright;
- Выполнять  заданные действия  с элементами  веб-страницы, используя  `executor`;
- Получать доступ к контенту элементов и  весь текст страницы;
- Осуществлять  переход по URL-адресам.

Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создайте экземпляр `Playwrid` с опциями запуска (например, `headless` или  `options`).
    - Задайте  `user_agent` (необязательно).
    - Запустите браузер и перейдите на  `url` с помощью `start()`.

2. **Работа с  элементами**:
    - Получите  HTML-контент всей страницы с помощью `get_page_content()`.
    - Получите  HTML-контент элемента по CSS-селектору с помощью `get_element_content()`.
    - Получите  текстовое значение элемента по XPath с помощью `get_element_value_by_xpath()`.
    - Щелкните  элемент по CSS-селектору с помощью `click_element()`.
    -  Выполните  действие  с элементом, используя  `execute_locator()`  и  передавая  свойства локатора в  `locator` .

3. **Дополнительные методы**:
    - Доступ  к  `crawling_context`  (контекст  работы  краулера)  через  `self.context`.
    - Получение  текущего  URL  с помощью  `current_url`.

Пример использования
-------------------------

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