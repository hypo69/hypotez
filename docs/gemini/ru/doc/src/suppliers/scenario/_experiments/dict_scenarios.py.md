# Модуль src.scenario._experiments.dict_scenarios

## Обзор

Модуль `dict_scenarios.py` содержит словарь `scenario`, который определяет параметры для различных сценариев, связанных с продуктами. Каждый сценарий содержит информацию о URL, состоянии товара, категориях PrestaShop и правилах ценообразования.

## Подробней

Этот модуль, вероятно, используется для конфигурации и управления различными сценариями поиска и обработки продуктов, например, "Apple Wathes" и "Murano Glass". Он позволяет задавать параметры для каждого продукта, такие как URL для поиска на Amazon, состояние товара (новое или нет), категории для PrestaShop и правила ценообразования.

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

**Описание**: Словарь `scenario` содержит конфигурации для различных продуктов или сценариев.

**Принцип работы**:
- Ключами словаря являются названия продуктов или сценариев (например, "Apple Wathes", "Murano Glass").
- Значением каждого ключа является словарь, содержащий параметры для данного продукта/сценария:
    - `"url"` (str): URL для поиска продукта на Amazon.
    - `"active"` (bool, optional): Указывает, активен ли сценарий (для "Apple Wathes"). По умолчанию `False`.
    - `"condition"` (str): Состояние продукта (например, "new").
    - `"presta_categories"` (dict): Категории для PrestaShop, где ключи - это типы категорий (например, `"template"`, `"default_category"`), а значения - словари, связывающие ID категорий с названиями.
    - `"checkbox"` (bool, optional): Флаг для чекбокса (только для "Apple Wathes"). По умолчанию `False`.
    - `"price_rule"` (int): Правило ценообразования.

**Примеры**:

```python
# Пример доступа к URL для Apple Wathes
apple_watches_url = scenario["Apple Wathes"]["url"]
print(apple_watches_url)
# Вывод: https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A2811119011%2Cn%3A2407755011%2Cn%3A7939902011%2Cp_n_is_free_shipping%3A10236242011%2Cp_89%3AApple&dc&ds=v1%3AyDxGiVC9lCk%2BzGvhkah6ZCjaellz7FcqKtRIfFA3o2A&qid=1671818889&rnid=2407755011&ref=sr_nr_n_2

# Пример доступа к категории PrestaShop для Murano Glass
murano_glass_category = scenario["Murano Glass"]["presta_categories"]["default_category"]["11209"]
print(murano_glass_category)
# Вывод: MURANO GLASS