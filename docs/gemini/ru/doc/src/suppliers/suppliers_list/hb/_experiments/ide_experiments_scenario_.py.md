# Модуль `ide_experiments_scenario_`

## Обзор

Модуль `ide_experiments_scenario_`  предназначен для проверки наполнения полей продукта в системе HB. В нем определены сценарии тестирования, которые используются для проверки корректности данных продукта на веб-сайте HB.

## Подробности

Модуль использует библиотеку `selenium` для взаимодействия с веб-браузером. Он взаимодействует с веб-сайтом HB с помощью `Driver` из `src.webdriver.driver`. В модуле определен сценарий тестирования `s.current_scenario` для проверки наполнения полей продукта.  Сценарий задает URL, название, состояние продукта и его категории в PrestaShop.

## Функции

### `run_scenarios`

**Назначение**: Запускает сценарии тестирования для проверки наполнения полей продукта в системе HB.

**Параметры**:

- `s`: Объект `Supplier`  -  хранит информацию о поставщике.
- `current_scenario`: Словарь, описывающий текущий сценарий тестирования, включающий URL продукта, его название, состояние и категории в PrestaShop.

**Возвращает**:

- `ret`: Результат выполнения сценария тестирования.

**Как работает**:
 - `run_scenarios` запускает процесс тестирования для заданного сценария тестирования, используя объект `Supplier`.
 - Функция проверяет соответствие данных продукта на веб-сайте HB заданным параметрам в `current_scenario`.

**Примеры**:

```python
s: Supplier = Supplier(supplier_prefix = 'hb')
p: Product = Product(s)
l: dict = s.locators['product']
d: Driver = s.driver
f: ProductFields = ProductFields(s)

s.current_scenario: dict =  {
      "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
      "name": "טיפוח כפות ידיים ורגליים",
      "condition": "new",
      "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
      }
    }

ret = run_scenarios(s, s.current_scenario)
```

## Параметры класса `Supplier`

- `supplier_prefix`: Префикс поставщика.
- `locators`: Словарь с локаторами элементов на странице продукта.
- `driver`: Драйвер веб-браузера.
- `product_fields`:  Объект `ProductFields` -  предоставляет доступ к полям продукта. 
- `current_scenario`: Текущий сценарий тестирования.

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

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