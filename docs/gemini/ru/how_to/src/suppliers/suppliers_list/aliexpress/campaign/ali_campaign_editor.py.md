## Как использовать класс AliCampaignEditor
=========================================================================================

### Описание
-------------------------
Класс `AliCampaignEditor` предоставляет функционал для редактирования рекламных кампаний на AliExpress. 
Он наследует от `AliPromoCampaign` и расширяет его возможности. 

### Шаги выполнения
-------------------------
1. **Инициализация:**
   - Создайте экземпляр класса `AliCampaignEditor` с помощью конструктора `__init__`, передав в него имя кампании, язык и валюту.
   - Конструктор инициализирует все необходимые атрибуты класса, например, пути к файлам, список продуктов, категорию и т.д.
2. **Редактирование товаров:**
   - Используйте методы `delete_product` и `update_product` для управления списком товаров в кампании.
     - Метод `delete_product` удаляет товар по его ID, если он не имеет аффилированной ссылки.
     - Метод `update_product` обновляет информацию о товаре в заданной категории.
3. **Обновление кампании:**
   - Метод `update_campaign` позволяет обновлять параметры кампании, например, описание, теги и т.д.
4. **Работа с категориями:**
   - Методы `update_category`, `get_category` и `list_categories` позволяют редактировать, получать информацию о категории и получать список всех категорий в кампании.
   - Метод `update_category` обновляет информацию о категории в файле.
   - Метод `get_category` возвращает объект `SimpleNamespace` с информацией о категории по ее имени.
   - Метод `list_categories` возвращает список названий категорий в кампании.
5. **Получение товаров для категории:**
   - Метод `get_category_products` позволяет получить список объектов `SimpleNamespace`, представляющих товары в заданной категории.
   - Метод выполняет чтение данных о товарах из JSON-файлов для заданной категории.

### Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign.ali_campaign_editor import AliCampaignEditor

# Создание экземпляра класса AliCampaignEditor
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")

# Удаление товара по ID
editor.delete_product("12345")

# Обновление товара в категории "Electronics"
editor.update_product("Electronics", "EN", {"product_id": "12345", "title": "Smartphone"})

# Получение списка категорий
categories = editor.list_categories
print(categories)  # ['Electronics', 'Fashion', 'Home']

# Получение товаров для категории "Electronics"
products = editor.get_category_products("Electronics")
print(len(products))  # 15

# Обновление категории "Electronics"
category = SimpleNamespace(name="Electronics", description="Updated description")
editor.update_category(Path("category.json"), category)
```

### Дополнительные замечания

- Класс `AliCampaignEditor` использует различные вспомогательные функции для работы с файлами, данными и API AliExpress.
- Методы `delete_product`, `update_product` и `update_campaign` предоставляют функционал для редактирования содержимого кампании.
- Методы `update_category`, `get_category` и `list_categories` позволяют работать с категориями в кампании.
- Метод `get_category_products` позволяет получить список товаров для заданной категории.
- Класс `AliCampaignEditor` предоставляет мощные инструменты для управления и редактирования рекламных кампаний на AliExpress.