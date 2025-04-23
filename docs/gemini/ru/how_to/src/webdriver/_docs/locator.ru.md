## Объяснение локаторов и их взаимодействие с `executor`

Локаторы — это конфигурационные объекты, которые описывают, как найти и взаимодействовать с веб-элементами на странице. Они передаются в класс `ExecuteLocator` для выполнения различных действий, таких как клики, отправка сообщений, извлечение атрибутов и т.д. Давайте разберем примеры локаторов и их ключи, а также их взаимодействие с `executor`.

Локаторы предоставляют гибкий инструмент для автоматизации взаимодействия с веб-элементами, а `executor` обеспечивает их выполнение с учетом всех параметров и условий.

### Примеры локаторов

#### 1. `close_banner`

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

**Суть локатора**: Закрыть баннер (pop-up окно), если он появился на странице.

**Ключи**:
- `attribute`: Не используется в данном случае.
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//button[@id = 'closeXButton']`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Необязательное действие (`false`).
- `timeout`: Таймаут для поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Событие для выполнения (`click()`).
- `locator_description`: Описание локатора.

**Взаимодействие с `executor`**:
- `executor` найдет элемент по XPATH и выполнит клик на нем.
- Если элемент не найден, `executor` продолжит выполнение, так как действие не обязательно (`mandatory: false`).

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет локатор `close_banner`, который используется для закрытия pop-up окна на веб-странице. Если окно появляется, локатор находит кнопку закрытия по XPATH и кликает по ней. Если окно не появляется, действие пропускается.

Шаги выполнения
-------------------------
1. Определяется JSON-объект `close_banner`, содержащий конфигурацию локатора.
2. Ключ `by` определяет, что поиск элемента будет осуществляться по XPATH.
3. Ключ `selector` содержит XPATH-выражение для кнопки закрытия (`//button[@id = 'closeXButton']`).
4. Ключ `event` указывает, что при нахождении элемента необходимо выполнить событие `click()`.
5. Ключ `mandatory` установлен в `false`, что означает, что отсутствие элемента не вызовет ошибку и выполнение продолжится.

Пример использования
-------------------------

```python
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

#### 2. `id_manufacturer`

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

**Суть локатора**: Возвращает значение, установленное в `attribute`.

**Ключи**:
- `attribute`: Значение атрибута (`11290`).
- `by`: Тип локатора (`VALUE`).
- `selector`: Не используется в данном случае.
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Обязательное действие (`true`).
- `timeout`: Таймаут для поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).
- `locator_description`: Описание локатора.

**Взаимодействие с `executor`**:
- `executor` вернет значение, установленное в `attribute` (`11290`).
- Так как `by` установлен в `VALUE`, `executor` не будет искать элемент на странице.

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет локатор `id_manufacturer`, который возвращает предопределенное значение атрибута (`11290`). Локатор не взаимодействует с элементами на странице, а просто возвращает значение, указанное в ключе `attribute`.

Шаги выполнения
-------------------------
1. Определяется JSON-объект `id_manufacturer`, содержащий конфигурацию локатора.
2. Ключ `by` установлен в `VALUE`, что указывает на то, что значение берется непосредственно из атрибута, а не из элемента на странице.
3. Ключ `attribute` содержит значение (`11290`), которое будет возвращено.
4. Ключ `selector` не используется, так как поиск элемента не требуется.
5. Ключ `mandatory` установлен в `true`, но это не влияет на выполнение, так как элемент не ищется.

Пример использования
-------------------------

```python
id_manufacturer = {
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

result = driver.execute_locator(id_manufacturer)
# result будет равен 11290
```

#### 3. `additional_images_urls`

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

**Суть локатора**: Извлечь URL дополнительных изображений.

**Ключи**:
- `attribute`: Атрибут для извлечения (`src`).
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элементов (`//ol[contains(@class, 'flex-control-thumbs')]//img`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Необязательное действие (`false`).
- `timeout`: Таймаут для поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).

**Взаимодействие с `executor`**:
- `executor` найдет элементы по XPATH и извлечет значение атрибута `src` для каждого элемента.
- Если элементы не найдены, `executor` продолжит выполнение, так как действие не обязательно (`mandatory: false`).

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет локатор `additional_images_urls`, который извлекает URL-адреса дополнительных изображений на веб-странице. Локатор находит все элементы `img`, находящиеся внутри элемента `ol` с классом, содержащим `flex-control-thumbs`, и извлекает значение атрибута `src` каждого найденного элемента.

Шаги выполнения
-------------------------
1. Определяется JSON-объект `additional_images_urls`, содержащий конфигурацию локатора.
2. Ключ `by` определяет, что поиск элементов будет осуществляться по XPATH.
3. Ключ `selector` содержит XPATH-выражение для поиска изображений (`//ol[contains(@class, 'flex-control-thumbs')]//img`).
4. Ключ `attribute` указывает, что необходимо извлечь значение атрибута `src` для каждого найденного элемента.
5. Ключ `mandatory` установлен в `false`, что означает, что если элементы не найдены, выполнение продолжится без ошибок.

Пример использования
-------------------------

```python
additional_images_urls = {
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

result = driver.execute_locator(additional_images_urls)
# result будет списком URL-адресов изображений
```

#### 4. `default_image_url`

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
  "locator_description": "Внимание! в морлеви картинка получается через screenshot и возвращается как png (`bytes`)"
}
```

**Суть локатора**: Сделать скриншот изображения по умолчанию.

**Ключи**:
- `attribute`: Не используется в данном случае.
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//a[@id = 'mainpic']//img`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `timeout`: Таймаут для поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Событие для выполнения (`screenshot()`).
- `mandatory`: Обязательное действие (`true`).
- `locator_description`: Описание локатора.

**Взаимодействие с `executor`**:
- `executor` найдет элемент по XPATH и сделает скриншот элемента.
- Если элемент не найден, `executor` выдаст ошибку, так как действие обязательно (`mandatory: true`).

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет локатор `default_image_url`, который делает скриншот изображения по умолчанию на веб-странице. Локатор находит элемент `img`, находящийся внутри элемента `a` с id `mainpic`, и выполняет функцию скриншота этого элемента.

Шаги выполнения
-------------------------
1. Определяется JSON-объект `default_image_url`, содержащий конфигурацию локатора.
2. Ключ `by` определяет, что поиск элемента будет осуществляться по XPATH.
3. Ключ `selector` содержит XPATH-выражение для поиска изображения (`//a[@id = 'mainpic']//img`).
4. Ключ `event` указывает, что при нахождении элемента необходимо выполнить событие `screenshot()`.
5. Ключ `mandatory` установлен в `true`, что означает, что если элемент не найден, будет выдана ошибка.

Пример использования
-------------------------

```python
default_image_url = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//a[@id = 'mainpic']//img",
  "if_list": "first",
  "use_mouse": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "screenshot()",
  "mandatory": true,
  "locator_description": "Внимание! в морлеви картинка получается через screenshot и возвращается как png (`bytes`)"
}

result = driver.execute_locator(default_image_url)
# result будет скриншотом изображения в формате png (`bytes`)
```

#### 5. `id_supplier`

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

**Суть локатора**: Извлечь текст внутри элемента, содержащего SKU.

**Ключи**:
- `attribute`: Атрибут для извлечения (`innerText`).
- `by`: Тип локатора (`XPATH`).
- `selector`: Выражение для поиска элемента (`//span[@class = 'ltr sku-copy']`).
- `if_list`: Если найдено несколько элементов, использовать первый (`first`).
- `use_mouse`: Не использовать мышь (`false`).
- `mandatory`: Обязательное действие (`true`).
- `timeout`: Таймаут для поиска элемента (`0`).
- `timeout_for_event`: Условие ожидания (`presence_of_element_located`).
- `event`: Нет события (`null`).
- `locator_description`: Описание локатора.

**Взаимодействие с `executor`**:
- `executor` найдет элемент по XPATH и извлечет текст внутри элемента (`innerText`).
- Если элемент не найден, `executor` выдаст ошибку, так как действие обязательно (`mandatory: true`).

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет локатор `id_supplier`, который извлекает текст (innerText) из элемента `span` с классом `ltr sku-copy` на веб-странице. Локатор используется для получения SKU товара.

Шаги выполнения
-------------------------
1. Определяется JSON-объект `id_supplier`, содержащий конфигурацию локатора.
2. Ключ `by` определяет, что поиск элемента будет осуществляться по XPATH.
3. Ключ `selector` содержит XPATH-выражение для поиска элемента (`//span[@class = 'ltr sku-copy']`).
4. Ключ `attribute` указывает, что необходимо извлечь значение атрибута `innerText` (текст внутри элемента).
5. Ключ `mandatory` установлен в `true`, что означает, что если элемент не найден, будет выдана ошибка.

Пример использования
-------------------------

```python
id_supplier = {
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

result = driver.execute_locator(id_supplier)
# result будет текстом внутри элемента (SKU товара)
```

### Взаимодействие с `executor`

`executor` использует локаторы для выполнения различных действий на веб-странице. Основные шаги взаимодействия:

1. **Парсинг локатора**: Преобразует локатор в объект `SimpleNamespace`, если это необходимо.
2. **Поиск элемента**: Использует тип локатора (`by`) и селектор (`selector`) для поиска элемента на странице.
3. **Выполнение события**: Если указан ключ `event`, выполняет соответствующее действие (например, клик, скриншот).
4. **Извлечение атрибута**: Если указан ключ `attribute`, извлекает значение атрибута из найденного элемента.
5. **Обработка ошибок**: Если элемент не найден и действие не обязательно (`mandatory: false`), продолжает выполнение. Если действие обязательно, выдает ошибку.