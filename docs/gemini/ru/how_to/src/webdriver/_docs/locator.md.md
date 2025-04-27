## Как использовать локаторы

=========================================================================================

Описание
-------------------------

Локаторы - это объекты конфигурации, описывающие, как найти и взаимодействовать с веб-элементами на странице. Они передаются в класс `ExecuteLocator` для выполнения различных действий, таких как клики, отправка сообщений, извлечение атрибутов и т. д. Давайте разберем примеры локаторов и их ключей, а также их взаимодействие с `executor`.

Шаги выполнения
-------------------------

1. **Создание локатора**: Локатор создается в виде объекта JSON, где каждый ключ определяет конкретный параметр.
2. **Передача локатора в `executor`**: Локатор передается в класс `ExecuteLocator`, который использует его для выполнения определенного действия.
3. **Обработка локатора**: `executor` анализирует локатор, понимая его тип и заданные параметры.
4. **Поиск элемента**: `executor` ищет элемент на странице, используя заданные в локаторе тип и селектор.
5. **Выполнение действия**: `executor` выполняет определенное действие, заданное в локаторе, например, клик, скриншот, извлечение атрибута.
6. **Обработка ошибок**: Если элемент не найден, `executor` обрабатывает ошибку в зависимости от параметра `mandatory`:
    - Если `mandatory` - `false`, `executor` продолжает выполнение.
    - Если `mandatory` - `true`, `executor` выдает ошибку.


Пример использования
-------------------------

```python
from src.webdriver import Driver, Chrome, Firefox, Playwright, ...

driver = Driver(Firefox)

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)

```

В данном примере локатор `close_banner` используется для закрытия всплывающего окна на странице. `executor` найдет кнопку по XPATH и выполнит клик по ней. Если кнопка не будет найдена, `executor` продолжит выполнение, так как `mandatory` - `false`.

## Локатор `close_banner`

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
  "locator_description": "Close the pop-up window, if it does not appear - it's okay (`mandatory`:`false`)"
}
```

**Описание**: Локатор `close_banner` используется для закрытия всплывающего окна на странице. 

**Ключи**:

- `attribute`: Не используется в этом случае.
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//button[@id = 'closeXButton']`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Необязательное действие (`false`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Событие для выполнения (`click()`).
- `locator_description`: Описание локатора.


**Взаимодействие с `executor`**:

- `executor` найдет элемент по XPATH и выполнит клик по нему.
- Если элемент не найден, `executor` продолжит выполнение, так как действие не является обязательным (`mandatory: false`).

## Локатор `id_manufacturer`

```json
"id_manufacturer": {
  "attribute": 11290,
  "by": "VALUE",
  "selector": null,
  "if_list": "first",
  "use_mouse": false,
  "mandatory": true,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": null,
  "locator_description": "id_manufacturer"
}
```

**Описание**: Локатор `id_manufacturer` используется для возврата значения, установленного в `attribute`.

**Ключи**:

- `attribute`: Значение атрибута (`11290`).
- `by`: Тип локатора (`VALUE`).
- `selector`: Не используется в этом случае.
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Обязательное действие (`true`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).
- `locator_description`: Описание локатора.

**Взаимодействие с `executor`**:

- `executor` вернет значение, установленное в `attribute` (`11290`).
- Так как `by` установлено в `VALUE`, `executor` не будет искать элемент на странице.

## Локатор `additional_images_urls`

```json
"additional_images_urls": {
  "attribute": "src",
  "by": "XPATH",
  "selector": "//ol[contains(@class, 'flex-control-thumbs')]//img",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": null
}
```

**Описание**: Локатор `additional_images_urls` используется для извлечения URL-адресов дополнительных изображений.

**Ключи**:

- `attribute`: Атрибут для извлечения (`src`).
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элементов (`//ol[contains(@class, 'flex-control-thumbs')]//img`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Необязательное действие (`false`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).

**Взаимодействие с `executor`**:

- `executor` найдет элементы по XPATH и извлечет значение атрибута `src` для каждого элемента.
- Если элементы не найдены, `executor` продолжит выполнение, так как действие не является обязательным (`mandatory: false`).

## Локатор `default_image_url`

```json
"default_image_url": {
  "attribute": null,
  "by": "XPATH",
  "selector": "//a[@id = 'mainpic']//img",
  "if_list": "first",
  "use_mouse": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "screenshot()",
  "mandatory": true,
  "locator_description": "Attention! In Morlevi, the image is obtained via screenshot and returned as png (`bytes`)"
}
```

**Описание**: Локатор `default_image_url` используется для создания скриншота основного изображения.

**Ключи**:

- `attribute`: Не используется в этом случае.
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//a[@id = 'mainpic']//img`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Событие для выполнения (`screenshot()`).
- `mandatory`: Обязательное действие (`true`).
- `locator_description`: Описание локатора.

**Взаимодействие с `executor`**:

- `executor` найдет элемент по XPATH и создаст скриншот элемента.
- Если элемент не найден, `executor` выдаст ошибку, так как действие является обязательным (`mandatory: true`).

## Локатор `id_supplier`

```json
"id_supplier": {
  "attribute": "innerText",
  "by": "XPATH",
  "selector": "//span[@class = 'ltr sku-copy']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": true,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": null,
  "locator_description": "SKU morlevi"
}
```

**Описание**: Локатор `id_supplier` используется для извлечения текста внутри элемента, содержащего SKU.

**Ключи**:

- `attribute`: Атрибут для извлечения (`innerText`).
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//span[@class = 'ltr sku-copy']`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Обязательное действие (`true`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).
- `locator_description`: Описание локатора.

**Взаимодействие с `executor`**:

- `executor` найдет элемент по XPATH и извлечет текст внутри элемента (`innerText`).
- Если элемент не найден, `executor` выдаст ошибку, так как действие является обязательным (`mandatory: true`).


## Взаимодействие с `executor`

`executor` использует локаторы для выполнения различных действий на веб-странице. Основные шаги взаимодействия:

1. **Парсинг локатора**: Преобразует локатор в объект `SimpleNamespace`, если это необходимо.
2. **Поиск элемента**: Использует тип локатора (`by`) и селектор (`selector`) для поиска элемента на странице.
3. **Выполнение события**: Если указан ключ `event`, выполняет соответствующее действие (например, клик, скриншот).
4. **Извлечение атрибута**: Если указан ключ `attribute`, извлекает значение атрибута из найденного элемента.
5. **Обработка ошибок**: Если элемент не найден, и действие не является обязательным (`mandatory: false`), продолжает выполнение. Если действие является обязательным, выдает ошибку.

Таким образом, локаторы предоставляют гибкий и мощный инструмент для автоматизации взаимодействия с веб-элементами, а `executor` обеспечивает их выполнение с учетом всех параметров и условий.