# Модуль для определения списка ресурсов API

## Обзор

Данный модуль предоставляет список всех доступных ресурсов для вызова API PrestaShop. 

## Детали

`api_resourses_list.py` - это файл, который содержит список всех ресурсов, доступных через API PrestaShop. Каждый элемент списка представляет собой строку, 
которая соответствует имени ресурса.

## Список ресурсов

```python
resource:list = [
    'products', 
    'categories', 
    'attachments', 
    'addresses',  
    'carriers', 
    'cart_rules', 
    'carts',
    'countries',
    'content_management_system',
    'currencies', 
    'customer_messages', 
    'customer_threads',
    'customers',
    'customizations',
    'deliveries',
    'employees', 
    'groups', 
    'guests',
    'image_types',
    'customizations',
    'images',
    'languages', 
    'manufacturers', 
    'messages',
    'order_carriers',
    'order_cart_rules',
    'order_details',
    'order_histories', 
    'order_invoices', 
    'order_payments',
    'order_slip',
    'order_states',
    'orders',
    'price_ranges',
    'product_customization_fields',
    'product_feature_values',
    'product_features', 
    'product_option_values', 
    'product_options',
    'product_suppliers',
    'products',
    'search',
    'shop_groups',
    'shop_urls',
    'shops', 
    'specific_price_rules', 
    'specific_prices',
    'states',
    'stock_availables',
    'stock_movement_reasons',
    'stock_movements',
    'stocks',
    'stores',
    'suppliers', 
    'supply_order_details', 
    'supply_order_receipt_histories',
    'supply_order_states',
    'supply_orders',
    'tags',
    'tax_rule_groups',
    'tax_rules',
    'taxes',
    'translated_configurations',
    'warehouse_product_locations', 
    'warehouses', 
    'weight_ranges',
    'zones',
]
```

## Примеры

```python
# Получение списка всех ресурсов
resources = api_resourses_list.resource

# Вывод списка ресурсов
print(resources)
```

## Взаимодействие с кодом

Данный модуль используется для определения доступных ресурсов API PrestaShop, 
что позволяет другим модулям проекта `hypotez` взаимодействовать с API и 
выполнять запросы к различным ресурсам.