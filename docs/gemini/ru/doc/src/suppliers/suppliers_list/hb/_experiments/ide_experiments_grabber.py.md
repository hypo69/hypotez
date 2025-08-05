# Модуль `ide_experiments_grabber.py`

## Обзор

Модуль `ide_experiments_grabber.py` предназначен для проверки исполнения сценариев HB. 
Он содержит код для получения заполненного словаря `product_fields` и отправки его на сервер.

## Подробней

Модуль `ide_experiments_grabber.py` является частью проекта `hypotez`. 
Его основная задача - автоматизировать проверку работы сценариев HB (Harbinger) для сбора данных о товарах. 
Сценарии HB реализованы в модуле `src.scenario` и позволяют автоматизировать процесс извлечения информации с веб-сайтов. 
Модуль `ide_experiments_grabber.py` использует объект `ProductFields` для сбора данных о товарах, 
а затем отправляет эти данные на сервер для дальнейшей обработки.

## Классы

### `class Supplier`

**Описание**: Класс `Supplier` представляет поставщика товаров (в данном случае, HB).

**Атрибуты**:

- `supplier_prefix`: Префикс для идентификации поставщика (в данном случае, `hb`).
- `locators`: Словарь с локаторами веб-элементов для сайта поставщика.
- `driver`: Объект вебдрайвера для взаимодействия с сайтом.
- `current_scenario`: Словарь с текущим сценарием работы с сайтом.
- `related_modules`: Объект с зависимыми модулями для сбора данных о товарах.

**Методы**:

- `grab_product_page()`: Метод для сбора данных о товарах с текущей страницы.

### `class Product`

**Описание**: Класс `Product` представляет товар на сайте.

**Атрибуты**:

- `supplier`: Объект `Supplier` для получения данных о поставщике.
- `product_fields`: Объект `ProductFields` для сбора данных о товарах.
- `product_urls`: Список ссылок на товары, найденных на сайте.
- `product_details`: Список словарей с подробной информацией о каждом товаре.

**Методы**:

- `get_product_details(url: str) -> Dict | None`: Метод для получения подробной информации о товаре по заданной ссылке.
- `get_product_urls()`: Метод для поиска ссылок на товары на сайте.

### `class ProductFields`

**Описание**: Класс `ProductFields` представляет словарь с данными о товаре.

**Атрибуты**:

- `supplier`: Объект `Supplier` для получения данных о поставщике.
- `product_details`: Словарь с данными о товаре.

**Методы**:

- `get_product_fields_from_product_page(page: Union[WebElement, None]) -> Dict`: Метод для извлечения данных о товаре с текущей страницы.

### `class StringNormalizer`

**Описание**: Класс `StringNormalizer`  используется для нормализации строк текста.

**Атрибуты**:

- `text`: Строка текста, которую нужно нормализовать.

**Методы**:

- `strip`:  метод для удаления пробелов в начале и конце строки
- `normalize_string`: Метод для нормализации строки текста.

## Функции

### `run_scenarios`

**Назначение**: Запуск сценариев HB для сбора данных о товарах.

**Параметры**:

- `supplier`: Объект `Supplier` для получения данных о поставщике.
- `scenario`: Словарь с текущим сценарием работы с сайтом.

**Возвращает**:

- `List`: Список словарей с результатами выполнения сценариев.

**Как работает функция**:

- Функция `run_scenarios` использует объект `supplier` для получения данных о поставщике, 
- таких как вебдрайвер и локаторы.
- Затем функция `run_scenarios` запускает сценарии HB, указанные в параметре `scenario`.
- Для каждого сценария функция собирает данные о товарах с помощью объекта `ProductFields` 
- и возвращает список словарей с результатами выполнения сценариев.

**Примеры**:

```python
# Пример вызова функции:
result = run_scenarios(s, s.current_scenario)

# Пример результата:
result = [
  {
    "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
    "name": "טיפוח כפות ידיים ורגליים",
    "condition": "new",
    "presta_categories": {
      "default_category": 11259,
      "additional_categories": []
    },
    "product_fields": {
      "product_name": "מערכת טיפוח כפות ידיים ורגליים",
      "product_description": "מערכת טיפוח כפות ידיים ורגליים...",
      "product_price": "120.00",
      "product_currency": "ILS",
      "product_image_urls": ["https://hbdeadsea.co.il/wp-content/uploads/2023/06/image1.jpg", "https://hbdeadsea.co.il/wp-content/uploads/2023/06/image2.jpg"],
      "product_categories": [11259, 11260],
      "product_attributes": {
        "size": "M",
        "color": "Red"
      }
    }
  },
  # ... другие результаты сценариев
]
```

## Параметры класса
- `supplier_prefix`: Префикс для идентификации поставщика (в данном случае, `hb`).
- `locators`: Словарь с локаторами веб-элементов для сайта поставщика.
- `driver`: Объект вебдрайвера для взаимодействия с сайтом.
- `current_scenario`: Словарь с текущим сценарием работы с сайтом.
- `related_modules`: Объект с зависимыми модулями для сбора данных о товарах.


## Примеры

```python
# Пример определения класса и работы с классом
s = Supplier(supplier_prefix='hb')
p = Product(s)

# Пример работы с вебдрайвером
driver = Driver(Chrome)  # Создание инстанса драйвера (пример с Chrome)

# Выполнение локатора
result = driver.execute_locator(l) 

# Пример сбора данных о товарах
product_details = p.get_product_details("https://hbdeadsea.co.il/product/body-scrub/")
```

## Внутренние функции

### `inner_function`

**Описание**:  Внутренняя функция для сбора данных о товарах с текущей страницы.

**Параметры**:

- `page`: Объект `WebElement`, представляющий текущую страницу.

**Возвращает**:

- `Dict`: Словарь с данными о товаре.

**Как работает функция**:

-  Внутренняя функция получает объект `WebElement`, представляющий текущую страницу. 
-  Извлекает данные о товаре с этой страницы с помощью локаторов веб-элементов.
-  Возвращает словарь с данными о товаре.

**Примеры**:

```python
# Пример вызова внутренней функции:
product_fields = inner_function(page)

# Пример результата:
product_fields = {
  "product_name": "Мягкий скраб для тела",
  "product_description": "Мягкий скраб для тела...",
  "product_price": "120.00",
  "product_currency": "ILS",
  "product_image_urls": ["https://hbdeadsea.co.il/wp-content/uploads/2023/06/image1.jpg", "https://hbdeadsea.co.il/wp-content/uploads/2023/06/image2.jpg"],
  "product_categories": [11259, 11260],
  "product_attributes": {
    "size": "M",
    "color": "Red"
  }
}