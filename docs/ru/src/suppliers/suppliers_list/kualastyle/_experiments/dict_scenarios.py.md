# Модуль: src.suppliers.kualastyle._experiments.dict_scenarios

## Обзор

Модуль `dict_scenarios.py` содержит словарь `scenarios`, определяющий сценарии для парсинга и категоризации товаров с сайта Kualastyle. Каждый сценарий включает URL коллекции, параметры активности, состояния товара, правила для категорий PrestaShop и ценообразования.

## Подробнее

Этот модуль предоставляет структуру данных для настройки процессов сбора и категоризации товаров. Информация, содержащаяся в `scenarios`, используется для автоматизации задач, связанных с товарами.

## Переменные

### `scenarios`

```python
scenarios: dict
```

Словарь, содержащий конфигурации для различных сценариев обработки товаров. Каждый сценарий представляет собой ключ (например, "Sofas and Sectionals") и соответствующий словарь с параметрами.

#### **Параметры сценария**

-   `url` (str): URL коллекции товаров на сайте Kualastyle.
-   `active` (bool): Указывает, активен ли данный сценарий. Если `True`, сценарий используется; если `False` - игнорируется.
-   `condition` (str): Состояние товара (например, "new").
-   `presta_categories` (dict): Словарь, определяющий категории PrestaShop, к которым следует отнести товары. Содержит подсловарь `default_category`, где ключи - идентификаторы категорий, а значения - их названия.
-   `checkbox` (bool): Флаг, указывающий на необходимость использования чекбоксов при выборе категории.
-   `price_rule` (int): Правило ценообразования для товаров в данной категории.

**Примеры**

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
        "url": "https://kualastyle.com/collections/%D7%9E%D7%96%D7%A0%D7%95%D7%A0%D7%99%D7%9D-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA-%D7%98%D7%9C%D7%95%D7%95%D7%99%D7%96%D7%99%D7%94",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "default_category": {"11061": "ספריות ומזנונים"}
        },
        "price_rule": 1
    }
}
```