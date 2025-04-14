Хорошо, вот более развернутое руководство по использованию класса `ExecuteLocator` для взаимодействия с веб-элементами, с подробным описанием каждого метода, его назначения и сценариев использования.

---

## Полное Руководство: Эффективное Взаимодействие с Веб-Элементами с помощью `ExecuteLocator`

Класс `ExecuteLocator` представляет собой мощный инструмент в вашем фреймворке автоматизации, разработанный для упрощения и стандартизации процесса поиска веб-элементов и выполнения действий над ними с использованием Selenium WebDriver. Его основная цель — предоставить единый, асинхронный интерфейс, который абстрагирует сложности ожидания элементов, обработки различных исключений Selenium и выполнения стандартных взаимодействий, таких как клики, ввод текста, получение атрибутов и многое другое.

**Ключевые преимущества:**

*   **Асинхронность:** Все операции ввода-вывода (ожидание элементов, взаимодействие с драйвером) выполняются асинхронно (`async`/`await`), что позволяет вашему приложению оставаться отзывчивым во время ожидания загрузки страницы или появления элементов.
*   **Абстракция:** Скрывает детали реализации Selenium (например, `WebDriverWait`, `expected_conditions`), предоставляя более высокоуровневые методы.
*   **Унификация:** Работает с локаторами, определенными в стандартизированном формате (словари или `SimpleNamespace`), что упрощает управление ими.
*   **Обработка ошибок:** Включает базовую обработку таймаутов и других распространенных исключений, с возможностью логирования и контроля обязательности элемента (`mandatory`).
*   **Гибкость:** Поддерживает различные стратегии поиска (ID, XPath, CSS, Class Name и т.д.) и разнообразные действия над элементами.

### 1. Подготовка к Работе

Прежде чем использовать `ExecuteLocator`, убедитесь, что выполнены следующие условия:

1.  **Инициализированный WebDriver:** У вас должен быть активный экземпляр вашего кастомного `Driver` (например, `Firefox` из `src/webdriver/firefox/firefox.py`), который, в свою очередь, управляет экземпляром Selenium WebDriver.
2.  **Экземпляр `ExecuteLocator`:** Создайте объект `ExecuteLocator`, передав ему ваш активный `driver`.
3.  **Асинхронная Среда:** Поскольку все методы `ExecuteLocator` являются корутинами (`async def`), их необходимо вызывать с использованием ключевого слова `await` внутри другой асинхронной функции.
4.  **Формат Локатора:** Вы должны определить локаторы для элементов, с которыми хотите взаимодействовать. Локатор — это словарь Python или объект `types.SimpleNamespace`, описывающий, как найти элемент и что с ним делать.

```python
import asyncio
from types import SimpleNamespace
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Для send_keys

# --- Заглушки для демонстрации ---
class MockWebElement:
    def get_attribute(self, attr): print(f"  [Mock] Getting attribute: {attr}"); return f"value_of_{attr}" if attr != 'textContent' else "Mock Text Content"
    def click(self): print("  [Mock] Clicked element")
    def send_keys(self, keys): print(f"  [Mock] Sent keys: {keys}")
    def clear(self): print("  [Mock] Cleared element")
    @property
    def screenshot_as_png(self): print("  [Mock] Took screenshot"); return b"PNG_MOCK_DATA"
    def __repr__(self): return "<MockWebElement>"

class MockDriver:
    _elements_found = [MockWebElement(), MockWebElement()] # Имитируем нахождение нескольких элементов
    def find_elements(self, by, selector): print(f"  [Mock] Searching MULTIPLE by {by} for '{selector}'"); return self._elements_found
    def find_element(self, by, selector): print(f"  [Mock] Searching SINGLE by {by} for '{selector}'"); return self._elements_found[0]
    def execute_script(self, script, *args): print(f"  [Mock] Executing script: {script[:50]}..."); return True
    def current_url(self): return "https://example.com/page?query=test&id=123&lang=en"
    # Добавьте другие методы Selenium по мере необходимости для тестов
    class MockActionChains:
        def move_to_element(self, el): print(f"  [Mock] Moved to {el}"); return self
        def send_keys(self, keys): print(f"  [Mock AC] Sent keys: {keys}"); return self
        def pause(self, duration): print(f"  [Mock AC] Paused for {duration}s"); return self
        def key_down(self, key): print(f"  [Mock AC] Key down: {key}"); return self
        def key_up(self, key): print(f"  [Mock AC] Key up: {key}"); return self
        def perform(self): print("  [Mock AC] Performed actions")
    def ActionChains(self, driver_instance): return self.MockActionChains()

# --- Инициализация ---
driver = MockDriver() # Используем заглушку для примера
# executor = ExecuteLocator(driver) # В реальном коде используйте ваш драйвер

# --- Структура Локатора (Детально) ---
# locator_example = {
#     "locator_description": "Кнопка 'Войти' на главной странице", # Опциональное описание для логирования
#     "by": By.XPATH,                  # Обязательно: Метод поиска (из selenium.webdriver.common.by.By) или строка "url", "value"
#     "selector": "//button[@id='login']", # Обязательно (кроме by='value'/'url'): Селектор для поиска
#     "attribute": None,               # Опционально: Имя атрибута для извлечения ('href', 'value', 'src', 'textContent', 'data-id', "{'key_attr':'value_attr'}")
#     "event": None,                   # Опционально: Действие для выполнения ('click()', 'clear();type(text)', 'send_keys(ENTER)', 'screenshot()', 'pause(2)', 'upload_media()')
#     "if_list": "first",              # Опционально ('all'|'first'|'last'|'even'|'odd'|int|list[int]): Как обработать, если найдено несколько элементов. По умолчанию 'all'.
#     "mandatory": True,               # Опционально (True|False): Считать ли ошибкой, если элемент не найден в течение таймаута? По умолчанию None (зависит от контекста).
#     "timeout": 10,                   # Опционально (float): Максимальное время ожидания элемента (в секундах). 0 - без ожидания.
#     "timeout_for_event": "presence_of_element_located", # Опционально: Условие ожидания Selenium ('presence...', 'visibility...')
# }
# Можно использовать SimpleNamespace для удобства доступа через точку:
# locator_ns = SimpleNamespace(**locator_example)
```

### 2. Получение Веб-Элемента (`get_webelement_by_locator`)

**Назначение:** Этот метод используется, когда вам нужен сам объект `WebElement` (или список объектов `WebElement`), возвращаемый Selenium. Это может быть полезно, если вам нужно выполнить над элементом нестандартные действия, не предусмотренные `execute_event`, или передать элемент в другую функцию/метод.

**Как работает:**
1. Принимает локатор (dict или SimpleNamespace).
2. Использует `by` и `selector` для поиска элемента(ов).
3. Учитывает `timeout` и `timeout_for_event` для ожидания.
4. Применяет правило `if_list` для фильтрации списка найденных элементов, если их несколько.
5. Возвращает `WebElement`, список `[WebElement]` или `None`, если элемент не найден (и `mandatory=False` или не указан явно как `True` в контексте, где это критично).

**Пример 1: Найти уникальное поле ввода по ID**

```python
async def example_get_single_element():
    print("\n--- Пример: get_webelement_by_locator (один элемент) ---")
    locator = SimpleNamespace(
        locator_description="Поле ввода имени пользователя",
        by=By.ID,
        selector="user-login-field",
        timeout=5,
        mandatory=True
    )
    try:
        element = await executor.get_webelement_by_locator(locator)
        if element:
            # element - это объект MockWebElement
            print(f"Найден элемент: {element}. Можно выполнить действия Selenium, например: element.is_displayed()")
        else:
            print(f"Элемент '{locator.selector}' не найден.")
    except Exception as e:
        print(f"Ошибка при поиске элемента: {e}")

# asyncio.run(example_get_single_element())
```

**Пример 2: Найти все ссылки в меню и взять последнюю**

```python
async def example_get_last_element_from_list():
    print("\n--- Пример: get_webelement_by_locator (последний из списка) ---")
    locator = SimpleNamespace(
        locator_description="Последний пункт меню навигации",
        by=By.CSS_SELECTOR,
        selector="nav.main-menu > ul > li > a",
        if_list="last", # Явно указываем взять последний
        timeout=10,
        mandatory=False
    )
    try:
        last_menu_item = await executor.get_webelement_by_locator(locator)
        if last_menu_item:
             # last_menu_item - один MockWebElement
            print(f"Найден последний пункт меню: {last_menu_item}")
        else:
            print("Пункты меню не найдены или список пуст.")
    except Exception as e:
        print(f"Ошибка при поиске пунктов меню: {e}")

# asyncio.run(example_get_last_element_from_list())
```

### 3. Получение Атрибута Элемента (`get_attribute_by_locator`)

**Назначение:** Используется для извлечения значения конкретного HTML-атрибута (например, `href`, `src`, `value`, `class`, `id`, `style`, `data-*`) или текстового содержимого элемента.

**Как работает:**
1. Находит элемент(ы) с помощью `get_webelement_by_locator`, используя `by`, `selector`, `timeout`, `if_list`.
2. Если элемент(ы) найден(ы), извлекает значение атрибута, указанного в поле `attribute`.
3. Поддерживает получение текстового содержимого через `attribute="textContent"` или `attribute="innerText"`.
4. Поддерживает специальный формат `attribute="{key_attr:value_attr}"` для извлечения пар ключ-значение, где ключи и значения сами являются атрибутами элемента (полезно для таблиц или списков `data-*`).
5. Возвращает строку со значением атрибута, список строк (если найдено несколько элементов и `if_list='all'` или подобное), словарь (для формата `{key:value}`), список словарей, или `None`, если элемент/атрибут не найден.

**Пример 1: Получить URL изображения из атрибута `src`**

```python
async def example_get_src_attribute():
    print("\n--- Пример: get_attribute_by_locator (атрибут 'src') ---")
    locator = SimpleNamespace(
        locator_description="Логотип сайта",
        by=By.CSS_SELECTOR,
        selector="img#logo",
        attribute="src", # Указываем, что нужен 'src'
        timeout=5,
        mandatory=True
    )
    try:
        image_url = await executor.get_attribute_by_locator(locator)
        if image_url is not None:
            print(f"URL логотипа: {image_url}") # Ожидаем "value_of_src"
        else:
            print("Атрибут 'src' или сам логотип не найден.")
    except Exception as e:
        print(f"Ошибка при получении атрибута 'src': {e}")

# asyncio.run(example_get_src_attribute())
```

**Пример 2: Получить текст первого параграфа**

```python
async def example_get_text_content():
    print("\n--- Пример: get_attribute_by_locator (текст элемента) ---")
    locator = SimpleNamespace(
        locator_description="Первый параграф статьи",
        by=By.TAG_NAME,
        selector="p",
        attribute="textContent", # Получаем видимый текст
        if_list="first",
        timeout=5
    )
    try:
        paragraph_text = await executor.get_attribute_by_locator(locator)
        print(f"Текст параграфа: '{paragraph_text}'") # Ожидаем "Mock Text Content"
    except Exception as e:
        print(f"Ошибка при получении текста параграфа: {e}")

# asyncio.run(example_get_text_content())
```

**Пример 3: Получить `data-id` и `data-name` для всех продуктов**

```python
async def example_get_dict_attributes():
    print("\n--- Пример: get_attribute_by_locator (словарный атрибут) ---")
    locator = SimpleNamespace(
        locator_description="ID и имена продуктов",
        by=By.CLASS_NAME,
        selector="product-card",
        attribute="{data-id:data-product-name}", # Извлекаем пары
        if_list="all", # Для всех найденных карточек
        timeout=10
    )
    try:
        # В реальном коде get_attribute вернет реальные значения
        # Заглушка вернет [{'value_of_data-id': 'value_of_data-product-name'}, ...]
        product_data = await executor.get_attribute_by_locator(locator)
        if product_data:
            print(f"Данные продуктов (ID: Имя): {product_data}")
        else:
            print("Карточки продуктов не найдены.")
    except Exception as e:
        print(f"Ошибка при получении словарных атрибутов: {e}")

# asyncio.run(example_get_dict_attributes()) # Заглушка вернет не совсем то, что в реальном сценарии
```

### 4. Выполнение События (`execute_event`)

**Назначение:** Этот метод выполняет предопределенные действия (события) над найденным веб-элементом. Это основной способ взаимодействия со страницей.

**Как работает:**
1. Находит элемент(ы) с помощью `get_webelement_by_locator`.
2. Парсит строку `event`. События разделяются точкой с запятой (`;`), что позволяет выполнять цепочки действий.
3. Выполняет каждое событие последовательно:
    *   `click()`: Выполняет клик по элементу. Обрабатывает `ElementClickInterceptedException`.
    *   `clear()`: Очищает поле ввода (`<input>`, `<textarea>`).
    *   `type(текст)`: Вводит указанный `текст` в поле ввода. Использует `send_keys` Selenium. Может использоваться с `typing_speed`.
    *   `send_keys(КЛАВИША)`: Отправляет специальные клавиши (например, `ENTER`, `TAB`, `CONTROL+A`). Названия клавиш берутся из `selenium.webdriver.common.keys.Keys`. Комбинации задаются через `+`, например `send_keys(CONTROL+A)`.
    *   `screenshot()`: Делает скриншот *только этого элемента* и возвращает бинарные PNG-данные.
    *   `pause(секунды)`: Приостанавливает выполнение на указанное количество секунд (`asyncio.sleep`).
    *   `upload_media()`: Предназначен для полей `<input type="file">`. Использует `send_keys` для указания пути к файлу, который передается через параметр `message` метода `execute_locator`.
4. Возвращает `True`, если все события в цепочке выполнены успешно, `False` в случае ошибки (например, элемент не найден и `mandatory=True`, клик перехвачен, ошибка при выполнении JS-клика). Если событие `screenshot()`, возвращает бинарные данные скриншота (или список данных, если несколько элементов/скриншотов).

**Пример 1: Кликнуть на чекбокс**

```python
async def example_event_click():
    print("\n--- Пример: execute_event (клик) ---")
    locator = SimpleNamespace(
        locator_description="Чекбокс 'Согласен с условиями'",
        by=By.CSS_SELECTOR,
        selector="input[type='checkbox']#terms",
        event="click()",
        timeout=5,
        mandatory=True
    )
    try:
        success = await executor.execute_event(locator)
        print(f"Результат клика: {success}") # Ожидаем True
    except Exception as e:
        print(f"Ошибка при клике на чекбокс: {e}")

# asyncio.run(example_event_click())
```

**Пример 2: Очистить поле поиска, ввести запрос и нажать Enter**

```python
async def example_event_clear_type_enter():
    print("\n--- Пример: execute_event (цепочка: очистить, ввести, Enter) ---")
    locator = SimpleNamespace(
        locator_description="Поле поиска",
        by=By.NAME,
        selector="q",
        event="clear();type(Selenium WebDriver);send_keys(ENTER)", # Цепочка событий
        timeout=10,
        mandatory=True
    )
    try:
        # message здесь не используется, текст в 'event'
        # typing_speed можно передать для 'type()'
        success = await executor.execute_event(locator, typing_speed=0.02)
        print(f"Результат выполнения цепочки поиска: {success}") # Ожидаем True
    except Exception as e:
        print(f"Ошибка в цепочке поиска: {e}")

# asyncio.run(example_event_clear_type_enter())
```

**Пример 3: Сделать скриншот капчи**

```python
async def example_event_screenshot():
    print("\n--- Пример: execute_event (скриншот элемента) ---")
    locator = SimpleNamespace(
        locator_description="Изображение капчи",
        by=By.ID,
        selector="captcha-image",
        event="screenshot()",
        timeout=15 # Даем время на загрузку
    )
    try:
        png_data = await executor.execute_event(locator)
        if isinstance(png_data, bytes):
            print(f"Получены данные скриншота капчи: {len(png_data)} байт") # Ожидаем b"PNG_MOCK_DATA"
            # Здесь можно сохранить png_data в файл или передать на распознавание
        elif png_data is False:
             print("Не удалось сделать скриншот (элемент не найден?).")
        else:
            print(f"Неожиданный результат скриншота: {type(png_data)}")
    except Exception as e:
        print(f"Ошибка при получении скриншота капчи: {e}")

# asyncio.run(example_event_screenshot())
```

### 5. Получение Скриншота Элемента (`get_webelement_as_screenshot`)

**Назначение:** Это специализированный метод, эквивалентный вызову `execute_event` с `event="screenshot()"`. Он предназначен исключительно для получения бинарных PNG-данных скриншота конкретного элемента.

**Как работает:**
1. Находит элемент с помощью `get_webelement_by_locator`.
2. Вызывает метод `.screenshot_as_png` у найденного `WebElement`.
3. Возвращает бинарные данные (`bytes`) или `None`, если элемент не найден или произошла ошибка при снятии скриншота.

**Пример: Сделать скриншот баннера**

```python
async def example_direct_screenshot():
    print("\n--- Пример: get_webelement_as_screenshot ---")
    locator = SimpleNamespace(
        locator_description="Рекламный баннер",
        by=By.CSS_SELECTOR,
        selector="div.ad-banner > img",
        if_list="first",
        timeout=8
    )
    try:
        banner_png = await executor.get_webelement_as_screenshot(locator)
        if banner_png:
            print(f"Получены данные скриншота баннера: {len(banner_png)} байт")
        else:
            print("Не удалось сделать скриншот баннера.")
    except Exception as e:
        print(f"Ошибка при получении скриншота баннера: {e}")

# asyncio.run(example_direct_screenshot())
```

### 6. Отправка Сообщения (Имитация Печати) (`send_message`)

**Назначение:** Этот метод специально разработан для имитации *пользовательского набора текста* в поля ввода (`<input>`, `<textarea>`). Он позволяет контролировать скорость печати и обрабатывает специальные символы (например, перенос строки).

**Как работает:**
1. Находит целевой элемент с помощью `get_webelement_by_locator`.
2. Перемещает курсор к элементу с помощью `ActionChains`.
3. Итерирует по словам и символам в переданной строке `message`.
4. Для каждого символа использует `ActionChains.send_keys(символ)`.
5. Если задан `typing_speed` (задержка в секундах), добавляет паузу (`ActionChains.pause`) после каждого символа.
6. Обрабатывает символ `;` как команду для нажатия `Shift+Enter` (перенос строки без отправки формы).
7. Выполняет накопленные действия `ActionChains.perform()`.
8. Возвращает `True` в случае успеха, `False` если элемент не найден.

**Пример: Напечатать отзыв с переносами строк**

```python
async def example_typing_message():
    print("\n--- Пример: send_message (имитация печати) ---")
    locator = SimpleNamespace(
        locator_description="Поле для ввода отзыва",
        by=By.ID,
        selector="review-text",
        timeout=5,
        mandatory=True
    )
    review = "Отличный продукт! Очень доволен покупкой.;Рекомендую всем."
    try:
        # Имитируем печать со скоростью 15 символов в секунду (примерно)
        success = await executor.send_message(
            locator,
            message=review,
            typing_speed=1/15
        )
        if success:
            # Mock ActionChains покажет симуляцию нажатий
            print("Отзыв успешно напечатан.")
        else:
            print("Не удалось напечатать отзыв.")
    except Exception as e:
        print(f"Ошибка при печати отзыва: {e}")

# asyncio.run(example_typing_message())
```

### 7. Универсальный Метод (`execute_locator`)

**Назначение:** Это главный, универсальный метод класса. Он анализирует предоставленный локатор и сам решает, какое действие выполнить: получить элемент, извлечь атрибут или выполнить событие. Используйте его, когда вам не нужно явно указывать тип операции.

**Как работает:**
1. Принимает локатор (dict или SimpleNamespace), `timeout`, `timeout_for_event`, `message`, `typing_speed`.
2. **Проверяет `by`:**
   *   Если `by == 'value'`, просто возвращает значение из поля `attribute` локатора (интерпретируется как константа).
   *   Если `by == 'url'`, извлекает значение параметра из `driver.current_url`, имя параметра берется из `attribute`.
3. **Проверяет `event`:** Если поле `event` заполнено, вызывает `execute_event` для выполнения указанного события(ий).
4. **Проверяет `attribute`:** Если `event` пусто, но `attribute` заполнено, вызывает `get_attribute_by_locator` для извлечения атрибута.
5. **По умолчанию:** Если `event` и `attribute` пусты (и `by` не 'value'/'url'), вызывает `get_webelement_by_locator` для получения самого веб-элемента.
6. Возвращает результат соответствующего вызванного метода (`WebElement`, `list[WebElement]`, `str`, `list[str]`, `dict`, `list[dict]`, `bool`, `bytes`, `list[bytes]` или `None`).

**Примеры использования `execute_locator`:**

```python
async def example_universal_executor():
    print("\n--- Пример: execute_locator (универсальный) ---")

    # Случай 1: Получить элемент (event и attribute пустые)
    locator_element = SimpleNamespace(by=By.ID, selector="footer", timeout=3)
    result1 = await executor.execute_locator(locator_element)
    print(f"Результат 1 (ожидаем WebElement): {result1}")

    # Случай 2: Получить атрибут (attribute задан)
    locator_attr = SimpleNamespace(by=By.TAG_NAME, selector="html", attribute="lang", timeout=1)
    result2 = await executor.execute_locator(locator_attr)
    print(f"Результат 2 (ожидаем значение 'lang'): {result2}") # value_of_lang

    # Случай 3: Выполнить событие (event задан)
    locator_event = SimpleNamespace(by=By.LINK_TEXT, selector="Privacy Policy", event="click()", timeout=5)
    result3 = await executor.execute_locator(locator_event)
    print(f"Результат 3 (ожидаем True/False): {result3}") # True

    # Случай 4: Получить параметр URL (by='url')
    locator_url = SimpleNamespace(by="url", attribute="id") # Получить 'id' из URL
    result4 = await executor.execute_locator(locator_url)
    print(f"Результат 4 (ожидаем значение 'id' из URL): {result4}") # 123

    # Случай 5: Получить константу (by='value')
    locator_value = SimpleNamespace(by="value", attribute="Постоянное значение")
    result5 = await executor.execute_locator(locator_value)
    print(f"Результат 5 (ожидаем константу): {result5}") # Постоянное значение

# asyncio.run(example_universal_executor())
```

### 8. Лучшие Практики и Советы

*   **Выбирайте Надежные Селекторы:** Отдавайте предпочтение ID (если они уникальны и статичны), затем CSS-селекторам и только в крайнем случае XPath (старайтесь избегать абсолютных XPath). Используйте атрибуты `data-*`, если они доступны.
*   **Используйте `locator_description`:** Добавляйте описания к локаторам для улучшения читаемости логов и облегчения отладки.
*   **Настраивайте Таймауты:** Подбирайте адекватные значения `timeout` в зависимости от ожидаемой скорости загрузки элемента. Не ставьте слишком большие таймауты без необходимости.
*   **Управляйте `mandatory`:** Устанавливайте `mandatory=True` только для тех элементов, отсутствие которых является критической ошибкой для вашего сценария. Для опциональных элементов оставляйте `False` или `None`.
*   **Понимайте `if_list`:** Используйте `if_list`, чтобы точно указать, какой элемент вам нужен, если селектор может вернуть несколько.
*   **Асинхронность:** Помните, что все вызовы должны использовать `await`. Используйте `asyncio.gather` для параллельного выполнения независимых операций с локаторами, если это необходимо.
*   **Логирование:** Изучайте логи, генерируемые вашим `logger`, для диагностики проблем с поиском элементов или выполнением событий.

---

Это руководство предоставляет исчерпывающий обзор возможностей класса `ExecuteLocator`. Используя его методы правильно, вы можете значительно повысить надежность, читаемость и эффективность вашего кода для автоматизации веб-взаимодействий.