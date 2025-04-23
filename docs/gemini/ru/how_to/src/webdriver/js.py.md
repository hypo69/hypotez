### **Инструкции по использованию кода модуля `JavaScript`**

=========================================================================================

#### **Описание модуля**
Модуль `JavaScript` предназначен для расширения возможностей Selenium WebDriver путем добавления JavaScript-функций для взаимодействия с веб-страницами. Он включает функции для управления видимостью DOM-элементов, получения метаданных страницы и управления фокусом браузера.

#### **Класс `JavaScript`**

##### **Описание**
Класс `JavaScript` предоставляет набор утилитных функций, которые позволяют взаимодействовать с веб-страницей через выполнение JavaScript-кода.

##### **Инициализация**
```python
    def __init__(self, driver: WebDriver):
        """Initializes the JavaScript helper with a Selenium WebDriver instance.

        Args:
            driver (WebDriver): Selenium WebDriver instance to execute JavaScript.
        """
        self.driver = driver
```

**Шаги выполнения**
1.  Класс инициализируется экземпляром `WebDriver` из Selenium.
2.  Этот драйвер используется для выполнения JavaScript-кода на странице.

**Пример использования**
```python
from selenium import webdriver
from src.webdriver.js import JavaScript

driver = webdriver.Chrome()  # или любой другой поддерживаемый драйвер
js_utils = JavaScript(driver)
```

##### **Метод `unhide_DOM_element`**
```python
    def unhide_DOM_element(self, element: WebElement) -> bool:
        """Makes an invisible DOM element visible by modifying its style properties.

        Args:
            element (WebElement): The WebElement object to make visible.

        Returns:
            bool: True if the script executes successfully, False otherwise.
        """
        script = """
        arguments[0].style.opacity = 1;
        arguments[0].style.transform = 'translate(0px, 0px) scale(1)';
        arguments[0].style.MozTransform = 'translate(0px, 0px) scale(1)';
        arguments[0].style.WebkitTransform = 'translate(0px, 0px) scale(1)';
        arguments[0].style.msTransform = 'translate(0px, 0px) scale(1)';
        arguments[0].style.OTransform = 'translate(0px, 0px) scale(1)';
        arguments[0].scrollIntoView(true);
        return true;
        """
        try:
            self.driver.execute_script(script, element)
            return True
        except Exception as ex:
            logger.error('Error in unhide_DOM_element: %s', ex)
            return False
```

**Описание**
Функция изменяет CSS-свойства элемента, чтобы сделать его видимым.

**Шаги выполнения**
1.  Принимает `WebElement` в качестве аргумента.
2.  Выполняет JavaScript-код, который изменяет стили элемента, делая его видимым (opacity = 1, transform = scale(1)).
3.  Прокручивает элемент в область видимости.
4.  Возвращает `True`, если выполнение успешно, и `False` в случае ошибки.

**Пример использования**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.webdriver.js import JavaScript

driver = webdriver.Chrome()
driver.get("https://example.com")

element = driver.find_element(By.ID, "hiddenElement")
js_utils = JavaScript(driver)
js_utils.unhide_DOM_element(element)
```

##### **Свойство `ready_state`**
```python
    @property
    def ready_state(self) -> str:
        """Retrieves the document loading status.

        Returns:
            str: 'loading' if the document is still loading, 'complete' if loading is finished.
        """
        try:
            return self.driver.execute_script('return document.readyState;')
        except Exception as ex:
            logger.error('Error retrieving document.readyState: %s', ex)
            return ''
```

**Описание**
Свойство возвращает текущий статус загрузки документа.

**Шаги выполнения**
1.  Выполняет JavaScript-код, который возвращает значение `document.readyState`.
2.  Возвращает строку `'loading'`, если документ еще загружается, и `'complete'`, если загрузка завершена.
3.  В случае ошибки возвращает пустую строку.

**Пример использования**
```python
from selenium import webdriver
from src.webdriver.js import JavaScript

driver = webdriver.Chrome()
driver.get("https://example.com")

js_utils = JavaScript(driver)
print(js_utils.ready_state)
```

##### **Метод `window_focus`**
```python
    def window_focus(self) -> None:
        """Sets focus to the browser window using JavaScript.

        Attempts to bring the browser window to the foreground.
        """
        try:
            self.driver.execute_script('window.focus();')
        except Exception as ex:
            logger.error('Error executing window.focus(): %s', ex)
```

**Описание**
Функция устанавливает фокус на окно браузера.

**Шаги выполнения**
1.  Выполняет JavaScript-код `window.focus()`.
2.  Пытается перевести окно браузера на передний план.

**Пример использования**
```python
from selenium import webdriver
from src.webdriver.js import JavaScript

driver = webdriver.Chrome()
driver.get("https://example.com")

js_utils = JavaScript(driver)
js_utils.window_focus()
```

##### **Метод `get_referrer`**
```python
    def get_referrer(self) -> str:
        """Retrieves the referrer URL of the current document.

        Returns:
            str: The referrer URL, or an empty string if unavailable.
        """
        try:
            return self.driver.execute_script('return document.referrer;') or ''
        except Exception as ex:
            logger.error('Error retrieving document.referrer: %s', ex)
            return ''
```

**Описание**
Функция возвращает URL-адрес реферера текущего документа.

**Шаги выполнения**
1.  Выполняет JavaScript-код, который возвращает значение `document.referrer`.
2.  Возвращает URL-адрес реферера или пустую строку, если он недоступен.

**Пример использования**
```python
from selenium import webdriver
from src.webdriver.js import JavaScript

driver = webdriver.Chrome()
driver.get("https://example.com")

js_utils = JavaScript(driver)
print(js_utils.get_referrer())
```

##### **Метод `get_page_lang`**
```python
    def get_page_lang(self) -> str:
        """Retrieves the language of the current page.

        Returns:
            str: The language code of the page, or an empty string if unavailable.
        """
        try:
            return self.driver.execute_script('return document.documentElement.lang;') or ''
        except Exception as ex:
            logger.error('Error retrieving document.documentElement.lang: %s', ex)
            return ''
```

**Описание**
Функция возвращает язык текущей страницы.

**Шаги выполнения**
1.  Выполняет JavaScript-код, который возвращает значение `document.documentElement.lang`.
2.  Возвращает код языка страницы или пустую строку, если он недоступен.

**Пример использования**
```python
from selenium import webdriver
from src.webdriver.js import JavaScript

driver = webdriver.Chrome()
driver.get("https://example.com")

js_utils = JavaScript(driver)
print(js_utils.get_page_lang())