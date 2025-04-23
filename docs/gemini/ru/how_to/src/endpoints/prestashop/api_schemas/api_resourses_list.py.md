### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода определяет список `resource`, содержащий перечень всех доступных ресурсов для API вызовов в PrestaShop. Этот список используется для определения того, к каким данным можно получить доступ через API.

Шаги выполнения
-------------------------
1.  Инициализация списка `resource`: Создается список с именем `resource`, который будет содержать строки, представляющие названия ресурсов API.
2.  Добавление элементов в список: В список добавляются строки, каждая из которых соответствует названию ресурса (например, `'products'`, `'categories'`, `'customers'` и т.д.).
3.  Использование списка: Список `resource` может быть использован для проверки доступности определенного ресурса через API, для динамического формирования URL API запросов или для отображения списка доступных ресурсов в интерфейсе.

Пример использования
-------------------------

```python
## \file /src/endpoints/prestashop/api_schemas/api_resourses_list.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.prestashop.api_schemas 
	:platform: Windows, Unix
	:synopsis: Список всех доступных ресурсов для API вызовов

"""


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

def is_resource_available(resource_name: str) -> bool:
    """
    Функция проверяет, доступен ли указанный ресурс в API.

    Args:
        resource_name (str): Название ресурса для проверки.

    Returns:
        bool: True, если ресурс доступен, иначе False.
    """
    return resource_name in resource

# Пример использования функции
resource_to_check = 'customers'
if is_resource_available(resource_to_check):
    print(f"Ресурс '{resource_to_check}' доступен через API.")
else:
    print(f"Ресурс '{resource_to_check}' не доступен через API.")