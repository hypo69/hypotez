# Модуль api_resourses_list

## Обзор

Модуль `api_resourses_list.py` содержит список всех доступных ресурсов для API-вызовов PrestaShop. Этот список используется для определения того, какие ресурсы могут быть запрошены через API.

## Подробней

Данный модуль предоставляет константу `resource`, представляющую собой список строк. Каждая строка в этом списке соответствует названию ресурса, доступного через API PrestaShop. Этот список используется для валидации запросов и определения доступных операций.

## Переменные

### `resource`

```python
resource: list = [
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

**Описание**: Список доступных ресурсов API PrestaShop.

**Назначение**: Этот список определяет, какие ресурсы могут быть запрошены через API. Он используется для валидации входящих запросов и маршрутизации их к соответствующим обработчикам.

**Как работает переменная**:

1.  Инициализация: Переменная `resource` инициализируется как список строк.
2.  Использование: Список используется для проверки допустимости API-запросов.

```
resource (list)
│
└───"products"
│   └───"categories"
│   └───"attachments"
│   └─── ... (и другие ресурсы)
```

**Примеры**:

```python
# Пример использования списка resource для проверки, является ли запрошенный ресурс допустимым
def is_valid_resource(resource_name: str) -> bool:
    """
    Проверяет, является ли указанный ресурс допустимым ресурсом API.

    Args:
        resource_name (str): Название ресурса для проверки.

    Returns:
        bool: True, если ресурс допустимый, иначе False.
    """
    return resource_name in resource


print(is_valid_resource('products'))  # Вывод: True
print(is_valid_resource('nonexistent'))  # Вывод: False