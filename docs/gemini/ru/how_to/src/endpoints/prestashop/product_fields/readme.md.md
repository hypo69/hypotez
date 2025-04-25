## Как использовать `ProductFields` 
=========================================================================================

### Описание
-------------------------
`ProductFields` - это класс, который представляет собой **контейнер данных для товара** в PrestaShop. Он хранит информацию о товаре, включая его характеристики, связи, описание, цены и т.д., в **формате, совместимом с API PrestaShop**.

### Шаги выполнения
-------------------------
1. **Создание экземпляра:** 
    - Создайте экземпляр класса `ProductFields`. Вы можете передать необязательный аргумент `id_lang` для указания языка по умолчанию. Если язык не задан, используется английский (ID 1).
    ```python
    # По умолчанию используется английский язык (ID 1)
    product = ProductFields()
    
    # Использовать язык с ID 2 (например, Иврит)
    product_he = ProductFields(id_lang=2)
    ```
2. **Заполнение полей:**
    - Используйте свойства (геттеры и сеттеры) для установки значений полей товара.
    - При установке значения для мультиязычных полей (например, `name`, `description`) можно указать язык в качестве аргумента сеттера.
    ```python
    product.id_supplier = 15
    product.reference = "ART-123"
    product.price = 99.90
    product.name = "Пример товара" # Установит имя для языка id_lang=1 (по умолчанию)
    product.description = "<p>Это описание товара.</p>" # Установит описание для языка id_lang=1
    ```
3. **Добавление связей:**
    - Используйте специальные методы для добавления связей товара с категориями, изображениями, характеристиками, тегами и т.д.
    ```python
    product.id_category_default = 5 # Обязательно установить главную категорию
    product.additional_category_append(5) # Добавляем главную в список связей
    product.additional_category_append(10)
    product.additional_category_append(12)

    # Добавление характеристики (Feature)
    # Предположим, ID характеристики "Цвет" = 2, ID значения "Красный" = 8
    product.product_features_append(feature_id=2, feature_value_id=8)

    # Добавление тега
    # Предположим, ID тега "Новинка" = 1
    product.product_tag_append(tag_id=1)
    ```
4. **Получение словаря для API:**
    - Используйте метод `to_dict()` для получения словаря Python, содержащего все данные товара в формате, совместимом с API PrestaShop.
    ```python
    api_dict = product.to_dict()
    ```
5. **Использование словаря в API:**
    - Используйте полученный словарь `api_dict` для создания нового товара или редактирования существующего товара в PrestaShop через API. 

### Пример использования
-------------------------

```python
from hypotez.src.endpoints.prestashop.product_fields import ProductFields

# Создаем объект для товара на английском языке
product = ProductFields() 

# Заполняем поля
product.id_supplier = 15
product.reference = "SKU-001"
product.name = "My Product" 
product.price = 120.50
product.active = 1

# Добавляем категории
product.id_category_default = 2 # Обязательно установить главную категорию
product.additional_category_append(2) # Добавляем главную в список связей
product.additional_category_append(9) 

# Получаем словарь для API
api_dict = product.to_dict()

# Вывод части словаря для примера
print({
    "id_supplier": api_dict.get("id_supplier"),
    "reference": api_dict.get("reference"),
    "price": api_dict.get("price"),
    "active": api_dict.get("active"),
    "name": api_dict.get("name"),
    "associations": api_dict.get("associations")
})

# Возможный вывод (структура name и associations важна):
# {
#     'id_supplier': '15',
#     'reference': 'SKU-001',
#     'price': '120.500000', # Цена будет отформатирована как строка с 6 знаками после запятой
#     'active': '1',
#     'name': {'language': [{'attrs': {'id': 1}, 'value': 'My Product'}]}, # Формат мультиязычного поля
#     'associations': {
#         'categories': [{'id': '2'}, {'id': '9'}] # Связи с категориями
#         # ... другие связи, если были добавлены
#     }
# }

```