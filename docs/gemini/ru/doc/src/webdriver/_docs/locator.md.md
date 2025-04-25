# Локаторы в `hypotez`

## Обзор

Этот файл содержит документацию по работе с локаторами в проекте `hypotez`. Локаторы - это конфигурационные объекты, которые описывают, как найти и взаимодействовать с веб-элементами на странице. Они передаются в класс `Executor` для выполнения различных действий, таких как клики, отправка сообщений, извлечение атрибутов и т.д.

## Подробнее

Локаторы представляют собой объекты JSON, которые содержат описание способа поиска веб-элемента и действий, которые необходимо выполнить с ним. 

**Пример:**

```json
{
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

**Ключи**:

- **attribute**:  Атрибут, который необходимо извлечь из найденного элемента.
- **by**: Тип локатора (например, XPATH, CSS, ID).
- **selector**: Селектор, который используется для поиска элемента (например, `//span[@class = 'ltr sku-copy']`).
- **if_list**: Если найдено несколько элементов, то укажите, какой из них использовать (например, `first`, `last`, `all`).
- **use_mouse**: Флаг, указывающий, следует ли использовать мышь при взаимодействии с элементом.
- **mandatory**: Флаг, указывающий, является ли действие обязательным.
- **timeout**: Таймаут для поиска элемента (в секундах).
- **timeout_for_event**:  Ожидание события (например, `presence_of_element_located`).
- **event**: Событие, которое необходимо выполнить (например, клик, получение скриншота).
- **locator_description**: Описание локатора.

## Примеры локаторов

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
  "locator_description": "Закрыть всплывающее окно, если оно не появится - не страшно (`mandatory`:`false`)"
}
```

**Назначение**: Закрыть баннер (всплывающее окно) на странице, если он отображается.

**Описание работы**:

- **executor** найдет элемент по XPATH (`//button[@id = 'closeXButton']`) и выполнит на нем клик (`event`: `click()`).
- Если элемент не найден, **executor** продолжит выполнение, поскольку действие не является обязательным (`mandatory: false`).

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

**Назначение**: Вернуть значение, установленное в `attribute`.

**Описание работы**:

- **executor** вернет значение, установленное в `attribute` (`11290`).
- Поскольку `by` установлен как `VALUE`, **executor** не будет искать элемент на странице.


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

**Назначение**: Извлечь URL-адреса дополнительных изображений.

**Описание работы**:

- **executor** найдет элементы по XPATH (`//ol[contains(@class, 'flex-control-thumbs')]//img`) и извлечет значение атрибута `src` для каждого элемента.
- Если элементы не найдены, **executor** продолжит выполнение, поскольку действие не является обязательным (`mandatory: false`).

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
  "locator_description": "Attention! In Morlevi, the image is obtained via screenshot and returned as png (`bytes`)"
}
```

**Назначение**: Сделать снимок экрана основного изображения.

**Описание работы**:

- **executor** найдет элемент по XPATH (`//a[@id = 'mainpic']//img`) и сделает снимок экрана элемента (`event`: `screenshot()`).
- Если элемент не найден, **executor** вызовет ошибку, поскольку действие является обязательным (`mandatory: true`).

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

**Назначение**: Извлечь текст из элемента, содержащего SKU.

**Описание работы**:

- **executor** найдет элемент по XPATH (`//span[@class = 'ltr sku-copy']`) и извлечет текст из элемента (`innerText`).
- Если элемент не найден, **executor** вызовет ошибку, поскольку действие является обязательным (`mandatory: true`).

## Взаимодействие с `executor`

`executor` использует локаторы для выполнения различных действий на веб-странице. Основные этапы взаимодействия:

1. **Разбор локатора**: Преобразует локатор в объект `SimpleNamespace`, если необходимо.
2. **Поиск элемента**: Использует тип локатора (`by`) и селектор (`selector`) для поиска элемента на странице.
3. **Выполнение события**: Если указан ключ `event`, выполняет соответствующее действие (например, клик, снимок экрана).
4. **Извлечение атрибута**: Если указан ключ `attribute`, извлекает значение атрибута из найденного элемента.
5. **Обработка ошибок**: Если элемент не найден, и действие не является обязательным (`mandatory: false`),  продолжает выполнение. Если действие является обязательным, то вызывает ошибку.

Таким образом, локаторы предоставляют гибкий и мощный инструмент для автоматизации взаимодействия с веб-элементами, а `executor` гарантирует их выполнение с учетом всех параметров и условий.