# Модуль: Список ресурсов API PrestaShop

## Обзор

Модуль содержит список всех доступных ресурсов для API вызовов PrestaShop. Этот список используется для определения того, с какими данными можно взаимодействовать через API.

## Подробней

Этот файл содержит переменную `resource`, которая представляет собой список строк. Каждая строка в списке соответствует названию ресурса, доступного через API PrestaShop. Этот список может использоваться для автоматической генерации документации API, проверки доступности ресурсов или для других целей, связанных с взаимодействием с API PrestaShop.

## Переменные

### `resource`

**Описание**: Список доступных ресурсов API PrestaShop.

**Тип**: `list`

**Элементы списка**: `str`

**Принцип работы**:
Переменная `resource` представляет собой список строк, каждая из которых является названием ресурса API PrestaShop. Этот список включает в себя такие ресурсы, как товары (`products`), категории (`categories`), вложения (`attachments`) и многие другие. Этот список используется для определения доступных ресурсов для API-взаимодействия с PrestaShop.

**Примеры**:

```python
resource = [
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
Этот список содержит все ресурсы, доступные для взаимодействия через API PrestaShop.