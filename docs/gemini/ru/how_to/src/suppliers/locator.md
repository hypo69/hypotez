### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот документ описывает структуру и параметры, Используетсяые для определения локаторов элементов на `HTML`-странице. Локаторы используются для автоматического поиска и взаимодействия с элементами веб-страницы, что необходимо для автоматизации тестирования и сбора данных.

Шаги выполнения
-------------------------
1.  **Определение локатора**: Создайте `JSON`-объект, который описывает, как найти элемент на странице. Этот объект должен включать следующие ключи:
    *   `attribute`: Атрибут элемента, который нужно получить.
    *   `by`: Метод поиска элемента (`XPATH`, `ID`, `CLASS_NAME` и т. д.).
    *   `selector`: Строка селектора, Используетсяая для поиска элемента.
    *   `if_list`: Указывает, что делать, если найдено несколько элементов.
    *   `use_mouse`: Указывает, использовать ли мышь для взаимодействия с элементом.
    *   `event`: Действие, которое нужно выполнить с элементом (например, `click()`).
    *   `mandatory`: Указывает, является ли локатор обязательным.
    *   `timeout`: Время ожидания (в секундах) для поиска элемента.
    *   `timeout_for_event`: Время ожидания (в секундах) для события.
    *   `locator_description`: Описание локатора.

2.  **Использование локатора**: Передайте `JSON`-объект в функцию, которая использует `WebDriver` для поиска элемента на странице и выполнения необходимых действий.

3.  **Обработка результатов**: В зависимости от значений `attribute` и `event`, функция вернет либо значение атрибута элемента, либо сам элемент (`WebElement`), либо выполнит запрошенное действие.

Пример использования
-------------------------

```python
"close_banner": {
    "attribute": null, 
    "by": "XPATH",
    "strategy_for_multiple_selectors": "find_first_match","selector": "//button[@id = 'closeXButton']",
    "if_list": "first",

    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "click()",
    "text_to_be_present_in_element":"","locator_description": "Закрыть всплывающее окно. Если оно не появляется — не страшно (`mandatory`: `false`)."
  },
  "additional_images_urls": {
    "attribute": "src",
    "by": "XPATH",
    "strategy_for_multiple_selectors": "find_first_match","selector": "//ol[contains(@class, 'flex-control-thumbs')]//img",
    "if_list": "all",

    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "text_to_be_present_in_element":"","locator_description": "Извлечь список `urls` для дополнительных изображений."
  },
  "id_supplier": {
    "attribute": "innerText",
    "by": "XPATH",
    "strategy_for_multiple_selectors": "find_first_match","selector": "//span[@class = 'ltr sku-copy']",
    "if_list": "first",

    "mandatory": true,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "text_to_be_present_in_element":"","locator_description": "SKU Morlevi."
  },
  "default_image_url": {
    "attribute": null,
    "by": "XPATH",
    "strategy_for_multiple_selectors": "find_first_match","selector": "//a[@id = 'mainpic']//img",
    "if_list": "first",

    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "screenshot()",
    "mandatory": true,
    "text_to_be_present_in_element":"","locator_description": "Внимание! В Morlevi изображение получается через скриншот и возвращается как PNG (`bytes`)."
  }
```

В этом примере, каждый `JSON`-объект определяет локатор для конкретного элемента на странице. Например, `close_banner` используется для поиска и закрытия всплывающего окна, `additional_images_urls` — для извлечения `URL` дополнительных изображений, `id_supplier` — для получения `SKU`, и `default_image_url` — для получения основного изображения через скриншот.