# Модуль `dict_scenarios`

## Обзор

Модуль `dict_scenarios` содержит словарь со сценариями для сбора данных о товарах с веб-сайта Amazon.

## Подробней

Модуль определяет структуру данных, содержащую информацию о различных сценариях сбора данных, включая URL, условия поиска и настройки для интеграции с PrestaShop.

## Переменные

### `scenario`

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

**Описание**: Словарь, содержащий сценарии для сбора данных о товарах.

**Ключи словаря**: Название сценария (например, `"Apple Wathes"`, `"Murano Glass"`).

**Значения словаря**: Словари, содержащие параметры сценария:

*   `url` (str): URL страницы для сбора данных.
*   `active` (bool): Флаг активности сценария.
*   `condition` (str): Состояние товара.
*   `presta_categories` (dict): Информация о категориях PrestaShop.
    *   `default_category` (dict): Словарь, содержащий ID категории PrestaShop по умолчанию.
*   `price_rule` (int): Правило для определения цены.

## Примечания

Модуль предназначен для экспериментов, поэтому структура словаря и значения полей могут быть изменены.
Отсутствует обработка ошибок.

Использование "магических" строк (таких как `'Murano Glass'` и `'Apple Wathes'`) и числовых идентификаторов (таких как `11209`) следует избегать, чтобы сделать код более понятным и поддерживаемым.