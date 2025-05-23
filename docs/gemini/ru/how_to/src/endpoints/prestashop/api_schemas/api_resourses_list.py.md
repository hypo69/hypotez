## Как использовать список ресурсов API PrestaShop
=========================================================================================

### Описание
-------------------------
Этот блок кода определяет список всех доступных ресурсов для API вызовов в PrestaShop. 

### Шаги выполнения
-------------------------
1. **Инициализация списка:** Создается список `resource`, в котором хранятся имена всех доступных ресурсов API.
2. **Добавление ресурсов:**  В список последовательно добавляются имена всех ресурсов:
    - `products`
    - `categories`
    - `attachments`
    - ...
    - `zones`

### Пример использования
-------------------------

```python
from src.endpoints.prestashop.api_schemas.api_resourses_list import resource

# Получение списка всех ресурсов API
available_resources = resource

# Вывод списка ресурсов
print(available_resources) 
```

**Результат:**
```
['products', 'categories', 'attachments', 'addresses', 'carriers', 'cart_rules', 'carts', 'countries', 'content_management_system', 'currencies', 'customer_messages', 'customer_threads', 'customers', 'customizations', 'deliveries', 'employees', 'groups', 'guests', 'image_types', 'customizations', 'images', 'languages', 'manufacturers', 'messages', 'order_carriers', 'order_cart_rules', 'order_details', 'order_histories', 'order_invoices', 'order_payments', 'order_slip', 'order_states', 'orders', 'price_ranges', 'product_customization_fields', 'product_feature_values', 'product_features', 'product_option_values', 'product_options', 'product_suppliers', 'products', 'search', 'shop_groups', 'shop_urls', 'shops', 'specific_price_rules', 'specific_prices', 'states', 'stock_availables', 'stock_movement_reasons', 'stock_movements', 'stocks', 'stores', 'suppliers', 'supply_order_details', 'supply_order_receipt_histories', 'supply_order_states', 'supply_orders', 'tags', 'tax_rule_groups', 'tax_rules', 'taxes', 'translated_configurations', 'warehouse_product_locations', 'warehouses', 'weight_ranges', 'zones']
```

### Заметки
- Этот список используется для валидации запросов API, чтобы убедиться, что запрашиваемый ресурс существует. 
- С помощью этого списка разработчики могут проверить доступность ресурсов и выбрать подходящий для своих задач.