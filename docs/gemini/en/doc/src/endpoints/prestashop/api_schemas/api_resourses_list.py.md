# Список доступных ресурсов для API вызовов

## Overview

Модуль `src.endpoints.prestashop.api_schemas.api_resourses_list` содержит список всех доступных ресурсов для API вызовов в PrestaShop.

## Details

Этот модуль используется для определения списка всех доступных ресурсов для API вызовов. Он представляет собой список строк, где каждая строка - это имя ресурса. 

## Table of Contents

- [Список ресурсов](#Список-ресурсов)

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

**Описание:**

- Переменная `resource` - список строк, содержащий все доступные ресурсы PrestaShop API. 
- Каждый элемент списка - это строка, представляющая имя ресурса.
- Например, `'products'` представляет ресурс для работы с товарами.

**Использование:**

Этот модуль используется в других модулях, которые работают с PrestaShop API. Например, в модулях, которые обрабатывают запросы API для получения данных о товарах, категориях или других ресурсах, используется этот список для определения доступных ресурсов.