### Анализ кода модуля `src/endpoints/prestashop/api_schemas/api_resourses_list.py`

## Обзор

Этот модуль содержит список всех доступных ресурсов для API-вызовов PrestaShop.

## Подробней

Модуль `src/endpoints/prestashop/api_schemas/api_resourses_list.py` предоставляет переменную `resource`, которая представляет собой список строк, содержащих имена всех доступных ресурсов для взаимодействия через API PrestaShop.

## Функции

В данном модуле отсутствуют функции.

## Переменные модуля

-   `resource` (list): Список всех доступных ресурсов для API вызовов PrestaShop.

### Список ресурсов

Следующие ресурсы доступны для API вызовов PrestaShop:

-   `'products'`
-   `'categories'`
-   `'attachments'`
-   `'addresses'`
-   `'carriers'`
-   `'cart_rules'`
-   `'carts'`
-   `'countries'`
-   `'content_management_system'`
-   `'currencies'`
-   `'customer_messages'`
-   `'customer_threads'`
-   `'customers'`
-   `'customizations'`
-   `'deliveries'`
-   `'employees'`
-   `'groups'`
-   `'guests'`
-   `'image_types'`
-   `'customizations'`
-   `'images'`
-   `'languages'`
-   `'manufacturers'`
-   `'messages'`
-   `'order_carriers'`
-   `'order_cart_rules'`
-   `'order_details'`
-   `'order_histories'`
-   `'order_invoices'`
-   `'order_payments'`
-   `'order_slip'`
-   `'order_states'`
-   `'orders'`
-   `'price_ranges'`
-   `'product_customization_fields'`
-   `'product_feature_values'`
-   `'product_features'`
-   `'product_option_values'`
-   `'product_options'`
-   `'product_suppliers'`
-   `'products'`
-   `'search'`
-   `'shop_groups'`
-   `'shop_urls'`
-   `'shops'`
-   `'specific_price_rules'`
-   `'specific_prices'`
-   `'states'`
-   `'stock_availables'`
-   `'stock_movement_reasons'`
-   `'stock_movements'`
-   `'stocks'`
-   `'stores'`
-   `'suppliers'`
-   `'supply_order_details'`
-   `'supply_order_receipt_histories'`
-   `'supply_order_states'`
-   `'supply_orders'`
-   `'tags'`
-   `'tax_rule_groups'`
-   `'tax_rules'`
-   `'taxes'`
-   `'translated_configurations'`
-   `'warehouse_product_locations'`
-   `'warehouses'`
-   `'weight_ranges'`
-   `'zones'`

## Пример использования

```python
from src.endpoints.prestashop.api_schemas import api_resourses_list

# Получение списка ресурсов
available_resources = api_resourses_list.resource
print(available_resources)
```

## Взаимосвязь с другими частями проекта

Этот модуль используется другими модулями проекта `hypotez` для определения списка доступных ресурсов при взаимодействии с PrestaShop API. Он не имеет зависимостей от других модулей, кроме стандартных.