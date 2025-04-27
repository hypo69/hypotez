## Как использовать словарь сценариев

=========================================================================================

Описание
-------------------------
Словарь `scenario` содержит набор сценариев для работы с поставщиком Amazon. Каждый сценарий описывает набор параметров для поиска товаров, их условия (новые, б/у) и правила сопоставления с категориями магазина PrestaShop.

Шаги выполнения
-------------------------
1. **Создание сценария**: 
   - Добавьте новый элемент в словарь `scenario` с уникальным ключом, например, `'New Product'`.
2. **Определение параметров**:
   - Укажите `url` для поиска на Amazon, `condition` (новое или б/у), `presta_categories` - словарь с категориями PrestaShop, которым соответствует товар, и `price_rule` - правило расчета цены.
3. **Сопоставление категорий**: 
   -  В `presta_categories` укажите ключ `default_category`, который будет сопоставляться с категориями товара в PrestaShop.
   - Значения `default_category` - это словарь, где ключи - это идентификаторы категорий в PrestaShop, а значения - это название категории. 

Пример использования
-------------------------

```python
from src.suppliers.amazon._experiments.scenarois.dict_scenarios import scenario

# Получение сценария по ключу
new_product_scenario = scenario['Murano Glass']

# Доступ к параметрам сценария
print(f'URL for search: {new_product_scenario["url"]}')
print(f'Condition: {new_product_scenario["condition"]}')
print(f'PrestaShop categories: {new_product_scenario["presta_categories"]}')
print(f'Price rule: {new_product_scenario["price_rule"]}')

# Использование сценария для поиска товаров
# ...
```