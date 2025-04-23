# Модуль `dict_scenarios.py`

## Обзор

Модуль содержит словарь `scenario`, определяющий сценарии для поиска и обработки товаров "Murano Glass" на Amazon.  Сценарий включает URL для поиска, условие товара, категории PrestaShop и правило цены.

## Подробней

Этот модуль используется для настройки параметров поиска и категорий товаров Murano Glass на Amazon.  В коде определен словарь `scenario`, который содержит конфигурацию для определенного типа товара.  Этот сценарий включает URL для поиска на Amazon, условие товара, категории PrestaShop, к которым товар будет отнесен, и правило цены.

## Переменные

### `scenario`

```python
scenario: dict
```

Словарь, содержащий конфигурацию сценария для поиска и обработки товаров Murano Glass на Amazon.

**Содержимое словаря `scenario`**:

-   `"Murano Glass"`: Ключ, представляющий сценарий для товаров Murano Glass.
    -   `"url"`: URL для поиска товаров Art Deco murano glass на Amazon.
    -   `"condition"`: Условие товара, в данном случае `"new"`.
    -   `"presta_categories"`: Словарь, содержащий категории PrestaShop, к которым будет отнесен товар.
        -   `"default_category"`: Подкатегория PrestaShop.
            -   `"11209"`: ID категории `"MURANO GLASS"`.
    -   `"price_rule"`: Правило цены, в данном случае `1`.

**Примеры**:

```python
scenario: dict = {
    "Murano Glass": {
        "url": "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss",
        "condition": "new",
        "presta_categories": {
            "default_category":{"11209":"MURANO GLASS"}
        },
        "price_rule": 1
    }
}