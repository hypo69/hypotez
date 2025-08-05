# Модуль для хранения сценариев для Murano Glass

## Обзор

Данный файл содержит словарь `scenario`, который хранит в себе сценарий для Murano Glass. Сценарий содержит в себе:
- `url`: URL-адрес страницы Amazon, на которой находятся товары.
- `condition`: Состояние товара ("new" - новый, "used" - б/у, "refurbished" - восстановленный).
- `presta_categories`: Словарь категорий PrestaShop, к которым должен быть отнесен товар.
- `price_rule`: Правило определения цены.

##  `scenario`

### Описание:

Словарь `scenario` хранит в себе описание сценария для Murano Glass. 

### Структура:

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
```

###  `Murano Glass`

###  Описание:

Словарь `Murano Glass` содержит в себе информацию о сценарии для Murano Glass. 

### Структура:

```python
"Murano Glass": {
    "url": "https://www.amazon.com/s?k=Art+Deco+murano+glass&crid=24Q0ZZYVNOQMP&sprefix=art+deco+murano+glass%2Caps%2C230&ref=nb_sb_noss",
    "condition": "new",
    "presta_categories": {
        "default_category":{"11209":"MURANO GLASS"}
    },
    "price_rule": 1
}
```
### `url`

**Описание**: URL-адрес страницы Amazon, на которой находятся товары.

### `condition`

**Описание**: Состояние товара ("new" - новый, "used" - б/у, "refurbished" - восстановленный).

### `presta_categories`

**Описание**: Словарь категорий PrestaShop, к которым должен быть отнесен товар.

### `price_rule`

**Описание**: Правило определения цены.


##  `presta_categories`

### Описание:

Словарь `presta_categories` содержит в себе категорию PrestaShop, к которой будет отнесен товар, полученный из сценария.

### Структура:

```python
"presta_categories": {
    "default_category":{"11209":"MURANO GLASS"}
}
```

### `default_category`

**Описание**: По умолчанию использует категорию `MURANO GLASS`.

### `11209`

**Описание**: ID категории PrestaShop.

### `MURANO GLASS`

**Описание**: Название категории PrestaShop.

##  `price_rule`

**Описание**: Правило определения цены. 

##  `url`

**Описание**: URL-адрес страницы Amazon, на которой находятся товары.

##  `condition`

**Описание**: Состояние товара ("new" - новый, "used" - б/у, "refurbished" - восстановленный).

```markdown