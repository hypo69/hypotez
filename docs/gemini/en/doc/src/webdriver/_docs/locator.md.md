# Locators: Interaction with `executor`

## Overview

This documentation explains the concept of locators in the `hypotez` project and their role in interacting with the `executor`. Locators are configuration objects that define how to find and interact with web elements on a page. They are used by the `executor` to perform various actions such as clicks, sending messages, extracting attributes, etc.

## Details

Locators are JSON objects containing a set of keys that specify the target web element and the actions to be performed on it. Each key has a specific purpose, contributing to the overall functionality of the locator. 

The following sections break down the structure of locators and provide examples of their usage.

## Locators

### `close_banner`

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
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}
```

**Purpose of the Locator**: Закрыть баннер (всплывающее окно), если он появляется на странице.

**Keys**:

- `attribute`: Не используется в этом случае.
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//button[@id = 'closeXButton']`).
- `if_list`: Если найдено несколько элементов, используйте первый (`first`).
- `use_mouse`: Не используйте мышь (`false`).
- `mandatory`: Необязательное действие (`false`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Событие для выполнения (`click()`).
- `locator_description`: Описание локатора.

**Interaction with `executor`**:

- `executor` найдет элемент по XPATH и выполнит на нем клик.
- Если элемент не найден, `executor` продолжит выполнение, поскольку действие не является обязательным (`mandatory: false`).

### `id_manufacturer`

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

**Purpose of the Locator**: Вернуть значение, установленное в `attribute`.

**Keys**:

- `attribute`: Значение атрибута (`11290`).
- `by`: Тип локатора (`VALUE`).
- `selector`: Не используется в этом случае.
- `if_list`: Если найдено несколько элементов, используйте первый (`first`).
- `use_mouse`: Не используйте мышь (`false`).
- `mandatory`: Обязательное действие (`true`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).
- `locator_description`: Описание локатора.

**Interaction with `executor`**:

- `executor` вернет значение, установленное в `attribute` (`11290`).
- Поскольку `by` установлено в `VALUE`, `executor` не будет искать элемент на странице.

### `additional_images_urls`

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

**Purpose of the Locator**: Извлечь URL-адреса дополнительных изображений.

**Keys**:

- `attribute`: Атрибут для извлечения (`src`).
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элементов (`//ol[contains(@class, 'flex-control-thumbs')]//img`).
- `if_list`: Если найдено несколько элементов, используйте первый (`first`).
- `use_mouse`: Не используйте мышь (`false`).
- `mandatory`: Необязательное действие (`false`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).

**Interaction with `executor`**:

- `executor` найдет элементы по XPATH и извлечет значение атрибута `src` для каждого элемента.
- Если элементы не найдены, `executor` продолжит выполнение, поскольку действие не является обязательным (`mandatory: false`).

### `default_image_url`

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
  "locator_description": "Внимание! В Morlevi изображение получаем через скриншоты и возвращаем как png (`bytes`)"
}
```

**Purpose of the Locator**: Сделать снимок экрана основного изображения.

**Keys**:

- `attribute`: Не используется в этом случае.
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//a[@id = 'mainpic']//img`).
- `if_list`: Если найдено несколько элементов, используйте первый (`first`).
- `use_mouse`: Не используйте мышь (`false`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Событие для выполнения (`screenshot()`).
- `mandatory`: Обязательное действие (`true`).
- `locator_description`: Описание локатора.

**Interaction with `executor`**:

- `executor` найдет элемент по XPATH и сделает снимок экрана элемента.
- Если элемент не найден, `executor` выдаст ошибку, поскольку действие является обязательным (`mandatory: true`).

### `id_supplier`

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

**Purpose of the Locator**: Извлечь текст внутри элемента, содержащего SKU.

**Keys**:

- `attribute`: Атрибут для извлечения (`innerText`).
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//span[@class = 'ltr sku-copy']`).
- `if_list`: Если найдено несколько элементов, используйте первый (`first`).
- `use_mouse`: Не используйте мышь (`false`).
- `mandatory`: Обязательное действие (`true`).
- `timeout`: Время ожидания поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).
- `locator_description`: Описание локатора.

**Interaction with `executor`**:

- `executor` найдет элемент по XPATH и извлечет текст внутри элемента (`innerText`).
- Если элемент не найден, `executor` выдаст ошибку, поскольку действие является обязательным (`mandatory: true`).

## Interaction with `executor`

`executor` использует локаторы для выполнения различных действий на веб-странице. Основные шаги взаимодействия:

1. **Разбор локатора**: Преобразует локатор в объект `SimpleNamespace`, если это необходимо.
2. **Поиск элемента**: Использует тип локатора (`by`) и селектор (`selector`) для поиска элемента на странице.
3. **Выполнение события**: Если указан ключ `event`, выполняет соответствующее действие (например, клик, снимок экрана).
4. **Извлечение атрибута**: Если указан ключ `attribute`, извлекает значение атрибута из найденного элемента.
5. **Обработка ошибок**: Если элемент не найден, а действие не является обязательным (`mandatory: false`), продолжает выполнение. Если действие является обязательным, выдает ошибку.

Таким образом, локаторы предоставляют гибкий и мощный инструмент для автоматизации взаимодействия с веб-элементами, а `executor` гарантирует их выполнение с учетом всех параметров и условий.