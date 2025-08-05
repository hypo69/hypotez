# Модуль `dict_scenarios`

## Обзор

Модуль `dict_scenarios` определяет словарь `scenarios`, который хранит информацию о категориях товаров на сайте `kualastyle.com`.

## Детали

Словарь `scenarios` содержит информацию о каждой категории товаров, включающую URL-адрес страницы категории на сайте, активность категории, условие отображения товаров (например, "new"), соответствие категориям в PrestaShop, использование чекбокса и правило ценообразования. 

## Словарь `scenarios`

### Структура

Словарь `scenarios` имеет следующую структуру:

```python
scenarios: dict = {
    "Название категории": {
        "url": "URL-адрес страницы категории",
        "active": True,  # Флаг активности категории
        "condition": "Условие отображения товаров",
        "presta_categories": {  # Соответствие категориям в PrestaShop
            "default_category": {
                "ID категории в PrestaShop": "Название категории в PrestaShop"
            }
        },
        "checkbox": False,  # Флаг использования чекбокса
        "price_rule": 1  # Правило ценообразования
    }
}
```

### Примеры

#### Категория "Sofas and Sectionals"

```python
"Sofas and Sectionals": {
    "url": "https://kualastyle.com/collections/%D7%A1%D7%A4%D7%95%D7%AA-%D7%9E%D7%A2%D7%95%D7%A6%D7%91%D7%95%D7%AA",
    "active": True,
    "condition": "new",
    "presta_categories": {
        "default_category": {"11055": "Sofas and Sectionals"}
    },
    "checkbox": False,
    "price_rule": 1
}
```

#### Категория "Bookcases and Display Cabinets"

```python
"Bookcases and Display Cabinets": {
    "url": "https://kualastyle.com/collections/%D7%9E%D7%96%D7%A0%D7%95%D7%A0%D7%99%D7%9D-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA-%D7%98%D7%9C%D7%95%D7%95%D7%99%D7%96%D7%99%D7%94",
    "active": True,
    "condition": "new",
    "presta_categories": {
        "default_category": {"11061": "ספריות ומזנונים"}
    },
    "price_rule": 1
}
```

## Как работает модуль

Модуль `dict_scenarios` используется для хранения информации о категориях товаров на сайте `kualastyle.com`. Эта информация необходима для автоматизации задач, таких как:

- Создание новых товаров в PrestaShop
- Обновление существующих товаров
- Фильтрация товаров по категориям
- Анализ данных о продажах

## Примеры использования

```python
# Получение информации о категории "Sofas and Sectionals"
sofa_category = scenarios["Sofas and Sectionals"]

# Получение URL-адреса страницы категории
sofa_url = sofa_category["url"]

# Проверка активности категории
is_sofa_category_active = sofa_category["active"]

# Получение соответствия категории в PrestaShop
presta_category_id = sofa_category["presta_categories"]["default_category"]["11055"]
```

## Дополнительные замечания

- Модуль `dict_scenarios` является частью проекта `hypotez`.
- Словарь `scenarios` может быть изменен в соответствии с требованиями к обработке данных.
- Документация модуля `dict_scenarios` предоставляет информацию для разработчиков, которые работают с данным модулем.