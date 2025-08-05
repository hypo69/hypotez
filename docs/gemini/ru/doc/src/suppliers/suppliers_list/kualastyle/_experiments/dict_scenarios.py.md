# Модуль для работы с каталогом товаров Kualastyle

## Обзор

Этот модуль предоставляет словарь `scenarios`, содержащий информацию о различных категориях товаров на сайте Kualastyle. Каждая категория описывается своим набором параметров:

- `url`: URL страницы категории на сайте Kualastyle.
- `active`: Флаг, указывающий на активность категории.
- `condition`: Условие, которое применяется к товарам в категории.
- `presta_categories`: Словарь, сопоставляющий идентификаторы категорий в PrestaShop с соответствующими категориями на Kualastyle.
- `checkbox`: Флаг, указывающий на наличие чекбокса фильтрации в категории.
- `price_rule`: Правило, определяющее ценообразование для товаров в категории.


## Подробней

Этот модуль используется для обработки данных о категориях товаров с сайта Kualastyle. Данные из словаря `scenarios` используются для:

- Получения информации о категориях товаров.
- Сопоставления категорий на Kualastyle с категориями в PrestaShop.
- Фильтрации товаров в соответствии с заданными условиями.


##  Словари

### `scenarios`

**Описание**: Словарь, содержащий описание различных категорий товаров на Kualastyle.

**Структура**:

```python
scenarios: dict = {
    "Название категории": {
        "url": "URL страницы категории",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "default_category": {"Идентификатор категории в PrestaShop": "Название категории в Kualastyle"}
        },
        "checkbox": False,
        "price_rule": 1
    },
    "Название категории": {
        "url": "URL страницы категории",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "default_category": {"Идентификатор категории в PrestaShop": "Название категории в Kualastyle"}
        },
        "checkbox": False,
        "price_rule": 1
    }
}
```

**Пример**:

```python
scenarios: dict = {
    "Sofas and Sectionals": {
        "url": "https://kualastyle.com/collections/%D7%A1%D7%A4%D7%95%D7%AA-%D7%9E%D7%A2%D7%95%D7%A6%D7%91%D7%95%D7%AA",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "default_category": {"11055": "Sofas and Sectionals"}
        },
        "checkbox": False,
        "price_rule": 1
    },
    "Bookcases and Display Cabinets": {
        "url": "https://kualastyle.com/collections/%D7%9E%D7%96%D7%A0%D7%95%D7%A0%D7%99%D7%9D-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%95%D7%AA-%D7%98%D7%9C%D7%95%D7%95%D7%99%D7%96%D7%99%D7%94",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "default_category": {"11061": "ספריות ומזנונים"}
        },
        "price_rule": 1
    }
}
```

**Пример использования**:

```python
from src.suppliers.kualastyle._experiments.dict_scenarios import scenarios

print(scenarios["Sofas and Sectionals"]["url"])