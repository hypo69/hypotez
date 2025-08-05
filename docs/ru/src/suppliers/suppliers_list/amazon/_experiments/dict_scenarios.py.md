# Модуль для определения сценариев Amazon в формате словаря

## Обзор

Модуль `dict_scenarios.py` содержит словарь `scenario`, который определяет различные сценарии для работы с Amazon. Каждый сценарий включает в себя URL, условия, категории PrestaShop и другие параметры, необходимые для обработки товаров.

## Подробней

Этот модуль предоставляет структуру данных для настройки и управления различными сценариями сбора данных о товарах на Amazon. Он определяет, какие товары следует искать, какие условия должны быть соблюдены и как эти товары должны быть категоризированы в PrestaShop. Модуль используется для автоматизации процесса извлечения и категоризации товаров с Amazon.

## Переменные

### `scenario`

```python
scenario: dict
```

**Описание**: Словарь, содержащий различные сценарии для работы с Amazon.

**Структура**:
Словарь имеет следующую структуру:

```
{
    "Название сценария": {
        "url": "URL страницы Amazon",
        "active": True/False,
        "condition": "Состояние товара",
        "presta_categories": {
            "template": {"ключ": "Значение"},
            "default_category":{"ключ":"Значение"}
        },
        "checkbox": True/False,
        "price_rule": Номер правила цены
    }
}
```

- `"Название сценария"`: Ключ, идентифицирующий сценарий (например, `"Apple Wathes"`).
- `"url"`: URL страницы Amazon для данного сценария.
- `"active"`: Определяет, активен ли сценарий (значение `True`) или нет (значение `False`).
- `"condition"`: Условие товара (например, `"new"`).
- `"presta_categories"`: Словарь, определяющий категории PrestaShop для данного сценария. Он может содержать шаблоны категорий (`"template"`) или категории по умолчанию (`"default_category"`).
- `"checkbox"`: Логическое значение, указывающее, нужно ли использовать чекбокс (значение `True`) или нет (значение `False`).
- `"price_rule"`: Номер правила цены, которое следует применить к товарам из этого сценария.

**Примеры**:

```python
scenario: dict = {
    "Apple Wathes": {
        "url": "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A2811119011%2Cn%3A2407755011%2Cn%3A7939902011%2Cp_n_is_free_shipping%3A10236242011%2Cp_89%3AApple&dc&ds=v1%3AyDxGiVC9lCk%2BzGvhkah6ZCjaellz7FcqKtRIfFA3o2A&qid=1671818889&rnid=2407755011&ref=sr_nr_n_2",
        "active": True,
        "condition": "new",
        "presta_categories": {
            "template": {"apple": "WATCHES"}
        },
        "checkbox": False,
        "price_rule": 1
    },
    "Murano Glass": {
        "url": "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss",
        "condition": "new",
        "presta_categories": {
            "default_category":{"11209":"MURANO GLASS"}
        },
        "price_rule": 1
    }
}
```

В этом примере определены два сценария: `"Apple Wathes"` и `"Murano Glass"`. Каждый сценарий имеет свой URL, условие, категории PrestaShop и правило цены. Сценарий `"Apple Wathes"` активен, использует шаблон категории `"apple"` и правило цены `1`. Сценарий `"Murano Glass"` использует категорию по умолчанию `"MURANO GLASS"` с идентификатором `11209` и правило цены `1`.