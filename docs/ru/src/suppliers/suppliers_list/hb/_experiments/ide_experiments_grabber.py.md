# src.suppliers.hb._experiments.ide_experiments_grabber

## Обзор

Модуль `ide_experiments_grabber.py` предназначен для проведения экспериментов и проверок при работе с поставщиком HB (hbdeadsea.co.il). В частности, он используется для получения заполненного словаря `product_fields` и отправки его на сервер. Этот модуль помогает автоматизировать процесс сбора данных о товарах и их загрузки на платформу PrestaShop.

## Подробней

Модуль выполняет следующие основные задачи:

1.  Инициализация необходимых объектов и параметров для работы с поставщиком HB.
2.  Запуск сценариев для сбора данных о товарах с веб-страницы поставщика.
3.  Извлечение и подготовка данных о товарах в формате, необходимом для загрузки на сервер.
4.  Логирование процесса выполнения и обработка возможных ошибок.

Этот модуль является частью процесса интеграции данных с поставщиком HB и автоматизирует рутинные задачи, связанные с обновлением информации о товарах.

## Классы

В данном модуле нет явно определенных классов, но используются экземпляры классов `Supplier`, `Product`, `ProductFields` и `Driver`.

## Переменные модуля

-   `dir_root` (Path): Корневая директория проекта `hypotez`.
-   `sys.path` (List[str]): Список путей, используемых Python для поиска модулей.
-   `dir_src` (Path): Путь к директории `src` внутри проекта.
-   `s` (Supplier): Экземпляр класса `Supplier` с префиксом `hb`.
-   `p` (Product): Экземпляр класса `Product`, связанный с поставщиком `s`.
-   `l` (Dict): Словарь локаторов для продукта, полученный из `s.locators["product"]`.
-   `d` (Driver): Экземпляр класса `Driver`, связанный с поставщиком `s`.
-   `f` (ProductFields): Экземпляр класса `ProductFields`, связанный с поставщиком `s`.
-   `s.current_scenario` (Dict): Словарь, содержащий информацию о текущем сценарии, включая URL, название и категории PrestaShop.

## Функции

В модуле используются функции из других модулей, таких как `run_scenarios` из `src.scenario` и `grab_product_page` из `s.related_modules`.

## Методы

В модуле используются методы классов `Driver` (например, `get_url`) и `Supplier` (например, `grab_product_page`).

## Пример

В модуле происходит инициализация объектов и запуск сценария для сбора данных о товарах с определенной страницы поставщика:

```python
s: Supplier = Supplier(supplier_prefix = 'hb')
p: Product = Product(s)
l: Dict = s.locators["product"]
d: Driver = s.driver
f: ProductFields = ProductFields(s)

s.current_scenario: Dict =  {
      "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
      "name": "טיפוח כפות ידיים ורגליים",
      "condition": "new",
      "presta_categories": {
        "default_category": 11259,
        "additional_categories": []
      }
    }

d.get_url(s.current_scenario['url'])
ret = run_scenarios(s, s.current_scenario)
s.related_modules.grab_product_page(s)
```

В данном примере создаются экземпляры классов `Supplier`, `Product`, `Driver` и `ProductFields`, а также задается текущий сценарий с URL и категориями. Затем происходит переход по URL и запуск сценария для сбора данных.