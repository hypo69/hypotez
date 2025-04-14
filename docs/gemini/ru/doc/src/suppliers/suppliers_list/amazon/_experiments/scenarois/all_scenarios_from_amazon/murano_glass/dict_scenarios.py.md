# Модуль `dict_scenarios.py`

## Обзор

Модуль `dict_scenarios.py` содержит словарь `scenario`, который определяет параметры для сценария сбора данных о "Murano Glass" (муранском стекле) с сайта Amazon. Этот словарь включает URL для поиска, условие ("new"), категории PrestaShop и правило ценообразования.

## Подробнее

Этот файл является частью экспериментов по сбору данных с Amazon для товаров "murano glass". Он определяет конфигурацию для одного конкретного сценария. Словарь `scenario` содержит всю необходимую информацию для запуска процесса сбора данных и последующей загрузки этих данных в PrestaShop.

## Переменные

### `scenario`

```python
scenario: dict
```

Словарь, содержащий конфигурацию сценария для сбора данных о "Murano Glass" с Amazon.

**Структура словаря `scenario`**:

- `"Murano Glass"` (str): Ключ, идентифицирующий сценарий.
    - `"url"` (str): URL для поиска товаров "Art Deco murano glass" на Amazon.
    - `"condition"` (str): Условие для отбора товаров (в данном случае, "new").
    - `"presta_categories"` (dict): Категории PrestaShop, к которым следует отнести товары.
        - `"default_category"` (dict): Словарь, сопоставляющий идентификатор категории PrestaShop (11209) с названием категории ("MURANO GLASS").
    - `"price_rule"` (int): Правило ценообразования, которое следует применять к товарам (в данном случае, 1).

**Примеры**:

Пример структуры словаря `scenario`:

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