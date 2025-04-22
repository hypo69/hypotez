# Документация для модуля `dict_scenarios.py`

## Обзор

Модуль `dict_scenarios.py` содержит словарь `scenario`, который определяет параметры для различных сценариев, связанных с товарами, такими как "Apple Wathes" и "Murano Glass". Эти сценарии включают URL-адреса для поиска товаров на Amazon, условия (например, состояние товара), правила ценообразования и категории PrestaShop, к которым товары должны быть отнесены.

## Подробней

Этот модуль, вероятно, используется для автоматизации процесса поиска и категоризации товаров, а также для определения правил ценообразования для этих товаров в PrestaShop. Словарь `scenario` служит конфигурационным файлом, который содержит всю необходимую информацию для каждого сценария. Он позволяет легко настраивать и изменять параметры сценариев без необходимости изменения кода.

## Переменные

### `scenario`

```python
scenario: dict
```

**Назначение**: Содержит конфигурации для различных сценариев, таких как "Apple Wathes" и "Murano Glass".

**Описание**:
Словарь `scenario` содержит конфигурации для различных сценариев, каждый из которых представлен ключом (например, "Apple Wathes"). Каждый сценарий включает следующие параметры:

- `"url"` (str): URL-адрес для поиска товаров на Amazon.
- `"active"` (bool): Указывает, активен ли сценарий.
- `"condition"` (str): Состояние товара (например, "new").
- `"presta_categories"` (dict): Категории PrestaShop, к которым товары должны быть отнесены.
  - `"template"` (dict): Шаблон категорий для "Apple Wathes", где "apple" соответствует "WATCHES".
  - `"default_category"` (dict): Категория по умолчанию для "Murano Glass", где "11209" соответствует "MURANO GLASS".
- `"checkbox"` (bool): Флаг для использования чекбоксов.
- `"price_rule"` (int): Правило ценообразования.

**Примеры**

```python
scenario = {
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
            "default_category": {"11209": "MURANO GLASS"}
        },
        "price_rule": 1
    }
}
```
В этом примере показаны конфигурации для двух сценариев: "Apple Wathes" и "Murano Glass". Для "Apple Wathes" указан URL для поиска на Amazon, состояние "new", активный статус, шаблон категорий PrestaShop и правило ценообразования. Для "Murano Glass" также указан URL, состояние "new", и категория PrestaShop по умолчанию.