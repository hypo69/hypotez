# Модуль `dict_scenarios.py`

## Обзор

Модуль содержит словарь `scenarios`, который определяет различные сценарии для категорий товаров на сайте Kualastyle. Каждый сценарий включает в себя URL категории, статус активности, условие (например, "новый"), соответствия категориям PrestaShop и правила ценообразования.

## Подробней

Этот модуль, вероятно, используется для настройки и управления процессом сбора и обработки данных о товарах с сайта Kualastyle. Информация в словаре `scenarios` позволяет указать, какие категории товаров следует обрабатывать, как они должны быть категоризированы в PrestaShop, и какие правила ценообразования к ним применять.

## Переменные

### `scenarios`

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

**Описание**: Словарь, содержащий конфигурации для различных категорий товаров.

-   **Ключи**: Названия категорий товаров (например, "Sofas and Sectionals").
-   **Значения**: Словари, содержащие параметры для каждой категории:
    -   `url` (str): URL страницы категории на сайте Kualastyle.
    -   `active` (bool): Указывает, активна ли категория для обработки.
    -   `condition` (str): Условие товаров в категории (например, "new").
    -   `presta_categories` (dict): Соответствие категорий PrestaShop.
        -   `default_category` (dict): Словарь, где ключ - ID категории в PrestaShop, значение - название категории.
    -   `checkbox` (bool):  логическое значение. Опрелеяет установлен ли чекбокс
    -   `price_rule` (int): Правило ценообразования для данной категории.

**Принцип работы**:

Словарь `scenarios` задает конфигурации для категорий товаров. Каждый ключ словаря соответствует названию категории товаров. Значение каждого ключа — это словарь с параметрами конфигурации для этой категории, включая URL страницы категории, статус активности, условие (например, "новый"), соответствия категориям PrestaShop и правила ценообразования.

**Примеры**:

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