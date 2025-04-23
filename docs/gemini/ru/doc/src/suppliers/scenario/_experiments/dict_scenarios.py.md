# Документация модуля `dict_scenarios.py`

## Обзор

Модуль `dict_scenarios.py` содержит словарь `scenario`, который определяет параметры для различных сценариев, связанных с товарами, такими как "Apple Wathes" и "Murano Glass". Каждый сценарий включает в себя информацию о URL, статусе активности, состоянии товара, категориях PrestaShop и правилах ценообразования.

## Подробней

Этот модуль предназначен для хранения конфигурационных данных в виде словаря `scenario`. Этот словарь используется для определения различных параметров для каждого сценария, таких как URL, состояние товара, категории PrestaShop и правила ценообразования.
Этот модуль является частью экспериментов.

## Переменные

### `scenario`

```python
scenario: dict
```

**Назначение**: Словарь, содержащий параметры для различных сценариев товаров.

**Описание**:
Словарь `scenario` содержит конфигурации для различных сценариев, таких как "Apple Wathes" и "Murano Glass". Каждый сценарий включает в себя следующую информацию:

- `"url"` (str): URL-адрес товара на Amazon.
- `"active"` (bool): Указывает, активен ли сценарий.
- `"condition"` (str): Состояние товара (например, "new").
- `"presta_categories"` (dict): Категории товара в PrestaShop.
- `"checkbox"` (bool): Указывает, используется ли чекбокс.
- `"price_rule"` (int): Правило ценообразования для товара.

#### Пример структуры словаря `scenario`:

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

**Элементы словаря**:

- `"Apple Wathes"`:
  - `"url"`: URL для поиска Apple Watches на Amazon.
  - `"active"`: `True`, указывает, что сценарий активен.
  - `"condition"`: `"new"`, указывает, что товары должны быть новыми.
  - `"presta_categories"`: Словарь категорий для PrestaShop.
    - `"template"`:
      - `"apple"`: `"WATCHES"`, категория для Apple Watches.
  - `"checkbox"`: `False`, указывает, что чекбокс не используется.
  - `"price_rule"`: `1`, правило ценообразования.

- `"Murano Glass"`:
  - `"url"`: URL для поиска Murano Glass на Amazon.
  - `"condition"`: `"new"`, указывает, что товары должны быть новыми.
  - `"presta_categories"`: Словарь категорий для PrestaShop.
    - `"default_category"`:
      - `"11209"`: `"MURANO GLASS"`, категория для Murano Glass.
  - `"price_rule"`: `1`, правило ценообразования.