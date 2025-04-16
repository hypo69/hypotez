### Анализ кода `hypotez/src/endpoints/prestashop/api_schemas/api_resourses_list.py.md`

## Обзор

Модуль содержит список всех доступных ресурсов для API вызовов PrestaShop.

## Подробнее

Этот модуль определяет переменную `resource`, которая представляет собой список строк. Каждая строка в списке соответствует названию ресурса, доступного через PrestaShop API. Модуль служит для определения валидных значений для параметра `resource` при взаимодействии с API PrestaShop.

## Функции

В данном коде отсутствуют функции.

## Переменные

### `resource`

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

**Назначение**:
Список всех доступных ресурсов для API вызовов PrestaShop.

## Примеры использования

```python
from src.endpoints.prestashop.api_schemas import api_resourses_list

# Пример использования
print(api_resourses_list.resource)
```

## Зависимости

Нет зависимостей

## Взаимосвязи с другими частями проекта

Модуль `api_resourses_list.py` предоставляет список доступных ресурсов PrestaShop API и может использоваться в других частях проекта `hypotez` для проверки корректности API-запросов и обеспечения доступа только к поддерживаемым ресурсам.  С этим модулем взаимодействуют модули для непосредственной работы с  PrestaShop API

Пример:

*   Модуль `src.endpoints.prestashop.api` использует эту константу для валидации входных данных функции `_exec`.