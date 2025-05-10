
# Локаторы полей на `HTML`-странице

**Локатор** — это структурированное описание (в данном случае, в формате JSON), которое указывает веб-драйверу, как найти конкретный элемент (например, кнопку, поле ввода, изображение, текстовый блок) на HTML-странице. Он содержит информацию о **стратегии поиска** (например, XPath, CSS-селектор, ID) и **значении селектора** (конкретное выражение XPath, строка CSS-селектора и т.д.).

Кроме того, локатор может включать дополнительные инструкции:
*   Какой **атрибут** элемента получить (например, `href`, `src`, `innerText`).
*   Какое **действие** (`event`) выполнить с элементом (например, `click()`, `screenshot()`).
*   Как **обрабатывать** ситуацию, если найдено **несколько элементов** (`if_list`).
*   Нужно ли **ожидать** появления элемента (`timeout`).
*   Является ли нахождение элемента **обязательным** (`mandatory`).

Каждый именованный JSON-объект в файлах `.json` (расположенных в директории `locators/` каждого поставщика) представляет собой один такой локатор, предназначенный для поиска определённого поля или выполнения действия на странице.

### Пример локатора:

```json
"close_banner": {
    "attribute": null, // Атрибут не получаем
    "by": "XPATH",     // Стратегия поиска - XPath
    "selector": "//button[@id = 'closeXButton']", // Значение селектора (XPath-выражение)
    "if_list": "first", // Если найдено несколько, взять первый
    "use_mouse": false, // Не использовать эмуляцию мыши
    "mandatory": false, // Локатор НЕ обязателен (ошибки не будет, если не найден)
    "timeout": 0,       // Таймаут ожидания элемента (0 - не ждать)
    "timeout_for_event": "presence_of_element_located", // Условие ожидания перед событием
    "event": "click()", // Действие - кликнуть по элементу
    "locator_description": "Закрываю pop-up окно. Если оно не появилось — не страшно (`mandatory`: `false`)."
  },
  "additional_images_urls": {
    "attribute": "src", // Получить значение атрибута 'src'
    "by": "XPATH",
    "selector": "//ol[contains(@class, 'flex-control-thumbs')]//img",
    "if_list": "all",   // Взять все найденные элементы
    "use_mouse": false,
    "mandatory": false, // Необязательный
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": null,      // Действий нет, только получение атрибута
    "locator_description": "Получает список `url` дополнительных изображений."
  },
  "id_supplier": {
    "attribute": "innerText", // Получить текстовое содержимое
    "by": "XPATH",
    "selector": "//span[@class = 'ltr sku-copy']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": true,    // Обязательный локатор
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "locator_description": "SKU Morlevi."
  },
  "default_image_url": {
    "attribute": null, // Атрибут не получаем, т.к. есть событие screenshot()
    "by": "XPATH",
    "selector": "//a[@id = 'mainpic']//img",
    "if_list": "first",
    "use_mouse": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "screenshot()", // Действие - сделать скриншот элемента
    "mandatory": true,
    "locator_description": "Внимание! В Morlevi картинка получается через screenshot и возвращается как PNG (`bytes`)."
  }
```

### Детали:

Имя словаря (ключа верхнего уровня в JSON, например, `"name"`, `"price"`, `"close_banner"`) обычно соответствует имени поля класса `ProductFields` ([подробнее о `ProductFields`](../product/product_fields)) или описывает выполняемое действие.

Например, локатор `name` будет использоваться для получения имени товара, локатор `price` — для получения цены товара и т.д.

```python
# Внутри класса Graber или его наследника
f = self.fields # Экземпляр ProductFields
# Имя будет получено с использованием локатора "name" из product.json
await self.name() # self.fields.name = await self.driver.execute_locator(self.product_locator.name)
# Цена будет получена с использованием локатора "price"
await self.price() # self.fields.price = await self.driver.execute_locator(self.product_locator.price)
...
```
Кроме того, можно создать свои локаторы для выполнения вспомогательных действий на странице. Например, локатор `close_banner` используется для закрытия баннера.

Словарь локатора содержит следующие ключи:

*   **`attribute`** (`string | null`): Атрибут, который нужно получить от найденного веб-элемента (например: `innerText`, `textContent`, `src`, `id`, `href`, `value`). Если `null` или не указан *и* нет `event`, то WebDriver вернёт сам веб-элемент (`WebElement`). Если указан `event`, то `attribute` часто игнорируется (зависит от `event`, например, `screenshot()` сам определяет возвращаемый тип).

*   **`by`** (`string`): Стратегия для поиска элемента. Соответствует константам `selenium.webdriver.common.by.By`:
    *   `ID` -> `By.ID`
    *   `NAME` -> `By.NAME`
    *   `CLASS_NAME` -> `By.CLASS_NAME`
    *   `TAG_NAME` -> `By.TAG_NAME`
    *   `LINK_TEXT` -> `By.LINK_TEXT`
    *   `PARTIAL_LINK_TEXT` -> `By.PARTIAL_LINK_TEXT`
    *   `CSS_SELECTOR` -> `By.CSS_SELECTOR`
    *   `XPATH` -> `By.XPATH`
    *   `VALUE` (специальное значение): Не ищет элемент, а просто возвращает значение из поля `attribute`. Полезно для задания статических значений (например, ID поставщика).

*   **`selector`** (`string`): Строка селектора, соответствующая выбранной стратегии `by`. Примеры:
    *   Для `XPATH`: `(//li[@class = 'slide selected previous'])[1]//img`, `//a[@id = 'mainpic']//img`, `//span[@class = 'ltr sku-copy']`
    *   Для `CSS_SELECTOR`: `a#mainpic img`, `span.ltr.sku-copy`, `input[name='username']`
    *   Для `ID`: `mainpic`
    *   Для `VALUE`: Обычно `"none"` или любое другое значение, т.к. селектор не используется.

*   **`if_list`** (`string | list[int] | int`): Определяет, как обработать список найденных веб-элементов (`web_elements`), если стратегия поиска вернула больше одного элемента:
    *   `first` (или `1`): выбрать первый элемент (`web_elements[0]`).
    *   `last`: выбрать последний элемент (`web_elements[-1]`).
    *   `all`: вернуть весь список найденных элементов (`web_elements`).
    *   `even`: выбрать элементы с чётными индексами (`web_elements[0]`, `web_elements[2]`, ...).
    *   `odd`: выбрать элементы с нечётными индексами (`web_elements[1]`, `web_elements[3]`, ...).
    *   `[1, 3, 5]` (список int): выбрать элементы с указанными индексами (нумерация с 1). Вернет `[web_elements[0], web_elements[2], web_elements[4]]`.
    *   `3` (int): выбрать элемент с указанным номером (нумерация с 1). Вернет `web_elements[2]`.
    *   *Альтернатива:* Часто нужный элемент можно выбрать прямо в селекторе (особенно в XPath), например: `(//div[contains(@class, 'description')])[2]//p` выберет `<p>` из второго `div`.

*   **`use_mouse`** (`boolean`): `true` | `false`. В текущей реализации `ExecuteLocator` напрямую не используется, но может быть зарезервировано для будущих действий с `ActionChains`, требующих имитации мыши.

*   **`event`** (`string | null`): Действие, которое WebDriver должен выполнить с найденным(и) веб-элементом(ами).
    *   **Важно❗**: Если указан `event`, он обычно выполняется **до** попытки получения значения из `attribute` (если `attribute` вообще используется).
    *   Примеры:
        *   `click()`: Кликнуть по элементу.
        *   `screenshot()`: Сделать скриншот элемента. Возвращает `bytes`.
        *   `type(текст)`: Ввести указанный текст в элемент (например, поле ввода).
        *   `send_keys(KEYS_ENUM)`: Отправить специальные клавиши (например, `send_keys(ENTER)`). `KEYS_ENUM` должно соответствовать атрибуту `selenium.webdriver.common.keys.Keys`.
        *   `clear()`: Очистить поле ввода.
        *   `upload_media()`: Специальное событие для загрузки файла (ожидает путь к файлу в `message` при вызове `execute_locator`).
        *   `pause(секунды)`: Вставить паузу (например, `pause(2)`).
        *   Можно комбинировать через точку с запятой: `clear();type(текст);send_keys(ENTER)`
    *   Если `event` равен `null`, выполняется только поиск элемента и/или получение атрибута.

*   **`mandatory`** (`boolean`): Является ли нахождение и успешное взаимодействие с элементом обязательным.
    *   Если `true`: При ошибке (элемент не найден, не кликабелен, таймаут и т.д.) выполнение прерывается (или вызывает исключение, в зависимости от обработки).
    *   Если `false`: При ошибке элемент пропускается, ошибки не возникает, метод вернёт `None` или `False`.

*   **`timeout`** (`float | int`): Время ожидания (в секундах) появления элемента на странице перед тем, как считать его не найденным. Если `0`, ожидание не используется (используется `find_element(s)` вместо `WebDriverWait`).

*   **`timeout_for_event`** (`string`): Условие ожидания `WebDriverWait`, используемое если `timeout > 0`. Основные значения:
    *   `presence_of_element_located`: Ждать, пока элемент появится в DOM (может быть невидимым).
    *   `visibility_of_element_located` / `visibility_of_all_elements_located`: Ждать, пока элемент(ы) станет видимым.
    *   Другие условия из `selenium.webdriver.support.expected_conditions`.

*   **`locator_description`** (`string`): Произвольное текстовое описание локатора для удобства чтения и отладки (выводится в логах).

---

### Сложные локаторы (Использование списков):

В ключи `attribute`, `by`, `selector`, `event`, `use_mouse`, `mandatory`, `locator_description` можно передавать списки одинаковой длины. Это позволяет выполнить последовательность действий.

#### Пример локатора со списками:

```json
"description": {
    "attribute": [
      null,       // Для первого шага атрибут не нужен
      "innerText" // Для второго шага - получить текст
    ],
    "by": [
      "XPATH",    // Стратегия для первого шага
      "XPATH"     // Стратегия для второго шага
    ],
    "selector": [
      "//a[contains(@href, '#tab-description')]", // Селектор для клика по вкладке
      "//div[@id = 'tab-description']//p"         // Селектор для получения текста описания
    ],
    "timeout": 0, // Общий таймаут (можно тоже списком)
    "timeout_for_event": "presence_of_element_located", // Общее условие ожидания
    "event": [
      "click()",  // На первом шаге - кликнуть
      null        // На втором шаге - действия нет
    ],
    "if_list": "first", // Общее правило для списков (можно списком)
    "use_mouse": false,  // Общее (можно списком)
    "mandatory": [
      true,       // Первый шаг обязателен
      true        // Второй шаг обязателен
    ],
    "locator_description": [
      "Нажимаю на вкладку 'Описание'.", // Описание первого шага
      "Читаю текст из блока описания."  // Описание второго шага
    ]
  }
```
В этом примере:
1.  Найдется элемент `//a[contains(@href, '#tab-description')]` (вкладка "Описание").
2.  По нему будет выполнен `click()`.
3.  Затем найдется элемент `//div[@id = 'tab-description']//p` (параграф внутри блока описания).
4.  Будет получено его текстовое содержимое (`innerText`).
Именно этот текст и будет итоговым результатом выполнения данного локатора.

#### Пример локатора со словарём в `attribute`:

```json
"specification_pairs": {
  "attribute": {"dt": "dd"}, // Ключ словаря - селектор для ключа, Значение - селектор для значения
  "by": "XPATH",
  "selector": "//dl[@class='specifications-list']", // Родительский элемент для пар
  "if_list": "all", // Обработать все найденные пары
  "mandatory": false,
  "timeout": 2,
  "timeout_for_event": "presence_of_element_located",
  "event": null,
  "locator_description": "Получает пары ключ-значение из списка спецификаций <dl>"
}
```
Этот формат используется для извлечения связанных данных, например, пар "Характеристика: Значение". Метод `get_attribute_by_locator` в `ExecuteLocator` содержит логику для обработки такого словаря: он находит родительский элемент (`//dl`), затем внутри него ищет элементы по селекторам из ключа (`dt`) и значения (`dd`) словаря `attribute` и формирует словарь Python `{ключ: значение}`.

---

### Где расположены локаторы:

Файлы с локаторами (`product.json`, `category.json` и т.д.) хранятся в директории `locators` внутри папки каждого конкретного поставщика:

```text
src/
└── suppliers/
    ├── suppliers_list/
    │   ├── ksp/
    │   │   ├── __init__.py
    │   │   ├── graber.py  # <--- Класс Graber для ksp
    │   │   └── locators/  # <--- Папка с локаторами для ksp
    │   │       ├── product.json
    │   │       └── category.json
    │   ├── aliexpress/
    │   │   ├── __init__.py
    │   │   ├── graber.py
    │   │   └── locators/
    │   │       ├── product.json
    │   │       └── category.json
    │   └── ...
    ├── graber.py # Базовый класс Graber
    └── get_graber_by_supplier.py # Фабрика граберов
```

Разметка страницы может меняться (например, десктопная/мобильная версии). В таком случае рекомендуется создавать отдельные файлы локаторов для каждой версии (например, `product_desktop.json`, `product_mobile.json`). Выбор нужного файла локаторов можно реализовать в методе `grab_page_async` класса-наследника `Graber`, проверяя, например, текущий URL:

```python
# Внутри класса-наследника Graber (например, KspGraber)
class KspGraber(Graber):
    # ... __init__ ...

    async def grab_page_async(self, *args, **kwargs) -> ProductFields:
        # Проверяем URL перед загрузкой локаторов по умолчанию
        if 'ksp.co.il/mob' in self.driver.current_url:
            logger.info("Обнаружена мобильная версия сайта KSP, загружаю мобильные локаторы.")
            # Перезагружаем локаторы из мобильного файла
            self.product_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'product_mobile.json')
            self.category_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'category_mobile.json')
        else:
            # Убедимся, что используются десктопные (если не были загружены ранее или переключились с мобильной)
             self.product_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'product.json')
             self.category_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'category.json')


        # Дальнейшая логика сбора данных...
        try:
            await super().grab_page_async(*args, **kwargs) # Вызываем базовую логику с нужными локаторами
            return self.fields
        except Exception as ex:
            logger.error(f"Ошибка в функции `grab_page_async` KSP", ex)
            return None
