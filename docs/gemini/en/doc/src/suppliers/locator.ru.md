# Локаторы для парсинга HTML-страниц в Hypotez

## Обзор

В этом документе описывается структура и использование локаторов для извлечения данных с HTML-страниц в проекте `hypotez`. Локаторы определяют, как находить и извлекать нужные элементы (например, название товара, цену) с веб-страниц поставщиков.

## Подробнее

Локаторы хранятся в файлах JSON и используются для описания полей класса `ProductFields`.  Кроме того, локаторы могут быть использованы для выполнения дополнительных действий на странице, таких как закрытие баннеров.

## Структура и примеры локаторов

### Пример структуры локатора

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
    "locator_description": "Закрываю pop-up окно. Если оно не появилось — не страшно (`mandatory`: `false`)."
  }
```

### Ключи локатора

#### `attribute`
Атрибут веб-элемента, значение которого необходимо получить. Если указано `null` или `false`, возвращается весь `WebElement`.
- Тип: строка или `null`

#### `by`
Стратегия поиска веб-элемента:
- `ID`: соответствует `By.ID`
- `NAME`: соответствует `By.NAME`
- `CLASS_NAME`: соответствует `By.CLASS_NAME`
- `TAG_NAME`: соответствует `By.TAG_NAME`
- `LINK_TEXT`: соответствует `By.LINK_TEXT`
- `PARTIAL_LINK_TEXT`: соответствует `By.PARTIAL_LINK_TEXT`
- `CSS_SELECTOR`: соответствует `By.CSS_SELECTOR`
- `XPATH`: соответствует `By.XPATH`

#### `selector`
Строка, определяющая способ нахождения веб-элемента (например, XPath).

#### `if_list`
Определяет, что делать со списком найденных элементов:
- `first`: выбрать первый элемент.
- `all`: выбрать все элементы.
- `last`: выбрать последний элемент.
- `even`, `odd`: выбрать четные/нечетные элементы.
- Указание конкретных номеров, например, `1,2,...` или `[1,3,5]`: выбрать элементы с указанными номерами.

#### `use_mouse`
Указывает, использовать ли мышь для взаимодействия с элементом (`true` или `false`).

#### `event`
Действие, которое необходимо выполнить с веб-элементом (`click()`, `screenshot()`, `scroll()` и т.д.). Выполняется **до** получения значения атрибута.

#### `mandatory`
Указывает, является ли локатор обязательным. Если `true` и элемент не найден, выбрасывается исключение. Если `false`, элемент пропускается.

#### `locator_description`
Описание локатора.

### Пример использования локаторов
```python
f = ProductFields(
    name = d.execute_locator('name'),
    price = d.execute_locator('price'),
    ...
)
```

### Сложные локаторы

В ключи локатора можно передавать списки, кортежи или словари.

#### Пример локатора со списками:

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
В этом примере сначала будет найден элемент `//a[contains(@href, '#tab-description')]`.
Драйвер выполнит команду `click()`, затем получит значение атрибута `href` элемента `//a[contains(@href, '#tab-description')]`.

#### Пример локатора со словарём:

```json
"sample_locator": {
  "attribute": {"href": "name"},
  ...
}
```

## Изменение локаторов в зависимости от версии сайта

Поскольку разметка страниц может меняться (например, для десктопной и мобильной версий), рекомендуется хранить несколько файлов локаторов для каждой из версий.

По умолчанию локаторы считываются из файла `product.json`.  Изменить это можно, проверяя URL в файле грабера страницы поставщика:

```python
async def grab_page(self) -> ProductFields:
    ...
    d = driver
    if 'ksp.co.il/mob' in d.current_url: # <- бывет, что подключается к мобильной версии сайта
        self.locator = j_loads_ns(gs.path.src / 'suppliers' / 'ksp' / 'locators' / 'product_mobile_site.json')
    ...
```

## Расположение файлов с локаторами

Файлы локаторов расположены в директориях поставщиков:

```text
src/
├── suppliers/
│   ├── suppliers_list/
│   │   ├── supplier_a/
│   │   │   ├── __init__.py
│   │   │   ├── handler.py  # <--- Модуль для supplier_a
│   │   │   └── locators/
│   │   │       └── category.json
│   │   ├── supplier_b/
│   │   │   ├── __init__.py
│   │   │   ├── handler.py  # <--- Модуль для supplier_b
│   │   │   └── locators/
│   │   │       └── category.json
│   │   └── ...
│   └── ...
└── ...
```