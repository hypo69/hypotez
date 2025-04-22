# Модуль: src.suppliers.kualastyle._experiments.dict_scenarios

## Обзор

Этот модуль содержит словарь `scenarios`, который определяет конфигурации для различных категорий товаров, таких как "Sofas and Sectionals" и "Bookcases and Display Cabinets". Каждая категория содержит информацию о URL, активности, состоянии товара ("new"), соответствии категориям PrestaShop и правилах ценообразования.
## Подробнее

Модуль предоставляет структуру данных для настройки процесса сбора и категоризации товаров с веб-сайта поставщика Kualastyle для интеграции с платформой PrestaShop. Этот файл служит конфигурационным файлом, определяющим параметры для различных категорий товаров, включая URL-адреса, соответствия категорий PrestaShop и правила ценообразования. Он предназначен для упрощения процесса добавления и обновления товаров в интернет-магазине PrestaShop на основе данных, полученных от Kualastyle.

## Переменные

### `scenarios`

```python
scenarios: dict
```

Словарь, содержащий конфигурации для различных категорий товаров.

**Описание**: Словарь `scenarios` определяет параметры для каждой категории товаров, которые будут использоваться при сборе и категоризации товаров с веб-сайта Kualastyle.

**Структура**:
```python
{
    "Имя категории (например, Sofas and Sectionals)": {
        "url": "URL страницы категории на сайте Kualastyle",
        "active": True/False (указывает, активна ли категория для обработки),
        "condition": "new" (состояние товара, в данном случае всегда "new"),
        "presta_categories": {
            "default_category": {"ID категории в PrestaShop": "Название категории в PrestaShop"}
        },
        "checkbox": False (логическое значение, указывающее, используется ли чекбокс),
        "price_rule": 1 (правило ценообразования)
    },
    ...
}
```
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
```
В этом примере `scenarios` содержит конфигурации для двух категорий: "Sofas and Sectionals" и "Bookcases and Display Cabinets". Для каждой категории указан URL, статус активности, состояние, соответствие категориям PrestaShop и правило ценообразования.