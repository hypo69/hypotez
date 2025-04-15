# Модуль: src.endpoints.prestashop.api_schemas.api_resourses_list

## Обзор

Модуль содержит список всех доступных ресурсов для API вызовов PrestaShop. Этот список используется для определения того, какие ресурсы могут быть запрошены через API.

## Подробней

Этот модуль предоставляет переменную `resource`, которая представляет собой список строк. Каждая строка в списке соответствует имени ресурса, доступного через API PrestaShop. Этот список используется для валидации запросов к API и для динамического формирования URL-ов для различных ресурсов. Список ресурсов включает в себя такие элементы, как продукты, категории, заказы, клиенты и другие сущности, которыми можно управлять через API PrestaShop.

## Переменные

### `resource`

**Описание**: Список всех доступных ресурсов для API вызовов PrestaShop.

**Тип**: `list`

**Элементы списка**: `str`

**Принцип работы**:
Список содержит строки, представляющие имена ресурсов API PrestaShop. Этот список используется для проверки допустимости запросов к API и для динамического создания URL-адресов для различных ресурсов.

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