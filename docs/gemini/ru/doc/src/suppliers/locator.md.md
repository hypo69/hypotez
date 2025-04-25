# Локаторы веб-элементов

## Обзор

Данный файл содержит документацию для разработчика по использованию локаторов веб-элементов в проекте `hypotez`. Локаторы используются для нахождения и взаимодействия с элементами на веб-страницах поставщиков. Файл `locators.json` хранит информацию о структуре веб-страницы и содержит определения для каждого элемента.

## Как работает файл `locators.json`

Файл `locators.json` представляет собой словарь, содержащий определения локаторов для каждого элемента на веб-странице. Каждый локатор является словарем со следующими ключами:

- **`attribute`**: Атрибут, который нужно получить от веб-элемента. Например: `innerText`, `src`, `id`, `href` и т.д. Если установить значение `attribute` в `none/false`, то WebDriver вернёт весь веб-элемент (`WebElement`).
- **`by`**: Стратегия для поиска элемента:
    - `ID` соответствует `By.ID`
    - `NAME` соответствует `By.NAME`
    - `CLASS_NAME` соответствует `By.CLASS_NAME`
    - `TAG_NAME` соответствует `By.TAG_NAME`
    - `LINK_TEXT` соответствует `By.LINK_TEXT`
    - `PARTIAL_LINK_TEXT` соответствует `By.PARTIAL_LINK_TEXT`
    - `CSS_SELECTOR` соответствует `By.CSS_SELECTOR`
    - `XPATH` соответствует `By.XPATH`
- **`selector`**: Селектор, определяющий способ нахождения веб-элемента. Примеры:
    - `(//li[@class = 'slide selected previous'])[1]//img`
    - `//a[@id = 'mainpic']//img`
    - `//span[@class = 'ltr sku-copy']`
- **`if_list`**: Определяет, что делать со списком найденных веб-элементов (`web_element`). Возможные значения:
    - `first`: выбрать первый элемент из списка.
    - `all`: выбрать все элементы.
    - `last`: выбрать последний элемент.
    - `even`, `odd`: выбрать чётные/нечётные элементы.
    - Указание конкретных номеров, например, `1,2,...` или `[1,3,5]`: выбрать элементы с указанными номерами.
    
    Альтернативный способ — указать номер элемента прямо в селекторе, например:
    - `(//div[contains(@class, 'description')])[2]//p`
- **`use_mouse`**: `true` | `false`
    Используется для выполнения действий с помощью мыши.
- **`event`**: WebDriver может выполнить действие с веб-элементом, например, `click()`, `screenshot()`, `scroll()` и т.д. **Важно❗**: Если указан `event`, он будет выполнен **до** получения значения из `attribute`. Например:
    ```json
    {
        ...
        "attribute": "href",
        ...
        "timeout": 0,
        "timeout_for_event": "presence_of_element_located",
        "event": "click()",
        ...
    }
    ```
    В этом случае сначала драйвер выполнит `click()` на веб-элементе, а затем получит его атрибут `href`. Принцип работы: **действие -> атрибут**.
    
    Еще примеры эвентов:
    - `screenshot()` возвращает вебэлемент как снимок экрана. Удобно, когда `CDN` сервер не возвращает изображение через `URL`.
    - `send_message()` - отправляет сообщение вебэлементу. Я рекомендую отправлять сообщение через переменную `%EXTERNAL_MESSAGE%`, как показано ниже:
      ```json
      {"timeout": 0, 
      "timeout_for_event": "presence_of_element_located", 
      "event": "click();backspace(10);%EXTERNAL_MESSAGE%"\n
      }
      ```
      
      
      ```
      исполняет последовательность:  
      <ol type="1">
        <li><code>click()</code> - нажимает на вебэлемент (переводит фокус в поле ввода) <code>&lt;textbox&gt;</code>.</li>
        <li><code>backspace(10)</code> - сдвигает каретку на 10 символов влево (очищает текст в поле ввода).</li>
        <li><code>%EXTERNAL_MESSAGE%</code> - отправляет сообщение в поле ввода.</li>
      </ol>
      ```
      
- **`mandatory`**: Является ли локатор обязательным.  Если `{mandatory: true}` и взаимодействие с веб-элементом невозможно, код выбросит ошибку. Если `mandatory: false`, элемент будет пропущен.
- **`locator_description`**: Описание локатора.

## Пример локатора

```json
"close_banner": {
    "attribute": null, 
    "by": "XPATH",
    "selector": "//button[@id = 'closeXButton']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "click()",
    "locator_description": "Закрываю pop-up окно. Если оно не появилось — не страшно (`mandatory`: `false`)."\
  }
```

## Использование локаторов

Локаторы используются в коде грабера страниц поставщиков. Например, в файле `graber.py` для получения информации о продукте:

```python
from src.suppliers.locator import j_loads_ns
from src.suppliers.locator import j_loads
from src.product.product_fields import ProductFields
from src.webdirver import Driver, Chrome

class Grabber:
    def __init__(self):
        self.locator = j_loads_ns('product.json') # <- загружаем локаторы из файла 'product.json'

    async def grab_page(self) -> ProductFields:
        d = Driver(Chrome) # <- Создание инстанса драйвера (пример с Chrome)
        product_fields = ProductFields(
            name = d.execute_locator('name'), # <- Получение имени товара
            price = d.execute_locator('price'), # <- Получение цены товара
            ...
        )
        return product_fields
```

### Детали

- Имя словаря соответствует имени поля класса `ProductFields` ([подробнее о `ProductFields`](../product/product_fields)).
- Например, локатор `name {}` будет использоваться для получения имени продукта, локатор `price {}` — для получения цены продукта и т.д.

```python
f = ProductFields(
    name = d.execute_locator('name'),
    price = d.execute_locator('price'),
    ...
)
```
- Кроме того, можно создать свои локаторы для дополнительных действий на странице. Например, `close_banner {}` будет использоваться для закрытия баннера на странице.

## Сложные локаторы

В ключи локатора можно передавать списки, кортежи или словари.

### Пример локатора со списками

```json
"sample_locator": {
    "attribute": [
      null,
      "href"
    ],
    "by": [
      "XPATH",
      "XPATH"
    ],
    "selector": [
      "//a[contains(@href, '#tab-description')]",
      "//div[@id = 'tab-description']//p"
    ],
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": [
      "click()",
      null
    ],
    "if_list": "first",
    "use_mouse": [
      false,
      false
    ],
    "mandatory": [
      true,
      true
    ],
    "locator_description": [
      "Нажимаю на вкладку для открытия поля description.",
      "Читаю данные из div."
    ]
  }
```
В этом примере сначала будет найден элемент `//a[contains(@href, '#tab-description')]`. Драйвер выполнит команду `click()`, затем получит значение атрибута `href` элемента `//a[contains(@href, '#tab-description')]`.

### Пример локатора со словарём

```json
"sample_locator": {
  "attribute": {"href": "name"},
  ...
}
```

## Где расположены локаторы

```text
src/
├── suppliers/
│   ├── suppliers_list/
│   │   ├── supplier_a/
│   │   │   ├── __init__.py
│   │   │   ├── graber.py  # <--- Модуль для supplier_a
│   │   │   └── locators/
│   │   │       └── category.json # <--- Локаторы для supplier_a
│   │   ├── supplier_b/
│   │   │   ├── __init__.py
│   │   │   ├── graber.py  # <--- Модуль для supplier_b
│   │   │   └── locators/
│   │   │       └── category.json
│   │   └── ...
│   └── ...
└── ...
```

##  Дополнительные замечания

- Разметка страницы может меняться. Например, десктопная/мобильная версии. В таком случае я рекомендую держать несколько файлов локторов для каждой из версий. Например: `product.json`,`product_mobile_site.json`.
- По умолчанию локаторы читаются из файла `product.json`. Вот как можно это изменить:
  - В файле грабера страницы поставщика делается проверка на `url`
    ```python
        async def grab_page(self) -> ProductFields:
            ...
             = driver  
            if 'ksp.co.il/mob' in d.current_url: # <- бывает, что подключается к мобильной версии сайта
                self.locator = j_loads_ns(gs.path.src / 'suppliers' / 'ksp' / 'locators' / 'product_mobile_site.json')
            ...
    ```
- Подробней о локаторах можно почитать в `lovator.ru.md` в модуле `webdrivaer`