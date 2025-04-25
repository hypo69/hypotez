# Модуль `dict_scenarios`

## Обзор

Этот модуль содержит словарь `scenario`, который определяет сценарии для сбора информации о товарах на Amazon.  Каждый сценарий включает URL-адрес поиска на Amazon, условия поиска (например, новое состояние товара),  категории в PrestaShop для сопоставления товаров,  правила ценообразования и другие параметры.

## Подробности

Этот файл определяет конфигурацию для различных сценариев сбора данных с Amazon.  В нем представлен словарь `scenario`, который хранит  информацию о  каждом сценарии. 

## Словарь `scenario`

### `scenario`

**Описание**: 
Словарь `scenario` хранит информацию о каждом сценарии, определенном для сбора данных с Amazon.
Словарь включает URL-адрес поиска, условия поиска, категории в PrestaShop для сопоставления товаров, правила ценообразования и другие параметры. 

**Параметры**:

- `"Apple Wathes"`: 
    - `"url"` (str): URL-адрес поиска на Amazon для часов Apple.
    - `"active"` (bool): Флаг, указывающий, активен ли этот сценарий (True, если активен).
    - `"condition"` (str): Условие поиска (например, "new" для новых товаров).
    - `"presta_categories"` (dict): Категории в PrestaShop для сопоставления товаров из этого сценария.
    - `"checkbox"` (bool): Флаг, указывающий,  нужно ли использовать флажок при поиске.
    - `"price_rule"` (int):  Правило ценообразования для товаров из этого сценария.
- `"Murano Glass"`: 
    - `"url"` (str): URL-адрес поиска на Amazon для Murano Glass.
    - `"condition"` (str): Условие поиска (например, "new" для новых товаров).
    - `"presta_categories"` (dict): Категории в PrestaShop для сопоставления товаров из этого сценария.
    - `"price_rule"` (int):  Правило ценообразования для товаров из этого сценария.

**Примеры**:

```python
# Пример получения информации о сценарии для часов Apple
apple_watches_scenario = scenario["Apple Wathes"]
print(f"URL для часов Apple: {apple_watches_scenario['url']}") 

# Пример проверки активности сценария для Murano Glass
is_murano_glass_active = scenario["Murano Glass"]["active"]
print(f"Сценарий для Murano Glass активен: {is_murano_glass_active}") 
```

## Как работает словарь `scenario`

Словарь `scenario` предоставляет информацию о том, как  искать  товары на Amazon,  как сопоставить  товары с категориями в PrestaShop и  как  обрабатывать цены. 

Каждый ключ в словаре `scenario`  представляет  сценарий, который  используется  для  поиска товаров на Amazon.  

## Примеры использования

```python
# Импорт необходимого модуля для работы с Amazon
from src.suppliers.amazon.amazon_core import Amazon

# Создание экземпляра Amazon
amazon = Amazon()

# Получение сценария для часов Apple
apple_watches_scenario = scenario["Apple Wathes"]

# Запуск  сбора  данных  с использованием  сценария  для  часов Apple
products_apple_watches = amazon.run_search(apple_watches_scenario)

# Получение сценария для Murano Glass
murano_glass_scenario = scenario["Murano Glass"]

# Запуск  сбора  данных  с использованием  сценария  для  Murano Glass
products_murano_glass = amazon.run_search(murano_glass_scenario)
```

```python
# Сохранение  данных  о товарах в формате JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products_apple_watches, f, indent=4)

# Вывод на консоль данных  о  товарах  в  формате  JSON
print(json.dumps(products_apple_watches, indent=4))
```
```markdown