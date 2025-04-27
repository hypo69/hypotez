# Модуль `src.suppliers.amazon._experiments.scenarois.dict_scenarios`

## Обзор

Модуль `src.suppliers.amazon._experiments.scenarois.dict_scenarios` содержит словарь `scenario` с предопределенными сценариями для работы с Amazon. Каждый сценарий представляет собой набор настроек для сбора данных о товарах с Amazon, включая URL-адрес, условия (например, "new" или "used"), категории в PrestaShop и правило ценообразования.

## Детали

Модуль используется в экспериментах с Amazon, чтобы проверить различные сценарии сбора данных о товарах.  

## Словарь `scenario`

### `scenario`

**Описание**:  Словарь, который содержит информацию о различных сценариях сбора данных.

**Принцип работы**:  Словарь `scenario` содержит ключи, каждый из которых представляет собой название сценария.  Внутри каждого сценария есть следующие ключи:

- **`url`**: URL-адрес страницы Amazon, с которой нужно собирать информацию.
- **`condition`**:  Состояние товара (например, "new" или "used").
- **`presta_categories`**: Словарь, который содержит сопоставление категорий Amazon с категориями PrestaShop.
- **`price_rule`**: Правило, используемое для определения цены. 

**Примеры**:

```python
scenario = {
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

## Примеры использования

```python
from src.suppliers.amazon._experiments.scenarois.dict_scenarios import scenario

# Доступ к сценарию "Murano Glass"
murano_glass_scenario = scenario["Murano Glass"]

# Получение URL-адреса сценария
murano_glass_url = murano_glass_scenario["url"]

# Получение категории PrestaShop для сценария
presta_category = murano_glass_scenario["presta_categories"]["default_category"]["11209"]

# Вывод значений
print(f"URL: {murano_glass_url}")
print(f"Category: {presta_category}")
```