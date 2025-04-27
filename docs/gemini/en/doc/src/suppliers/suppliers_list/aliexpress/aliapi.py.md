# AliExpress API Module

## Overview

This module provides a custom API class (`AliApi`) for interacting with the AliExpress API. This class extends the `AliexpressApi` class and allows you to retrieve product details, generate affiliate links, and perform other AliExpress-related operations.

## Details

The `AliApi` class is designed to simplify interactions with the AliExpress API. It handles the necessary authentication, API requests, and response parsing. This module is used for fetching product details, generating affiliate links, and potentially other tasks related to AliExpress data retrieval.

## Classes

### `AliApi`

**Description**: This class extends the `AliexpressApi` class and provides customized methods for interacting with the AliExpress API.

**Inherits**: `AliexpressApi` 

**Attributes**:

- `language` (str): The language to use for API requests. Defaults to 'en'.
- `currency` (str): The currency to use for API requests. Defaults to 'usd'.

**Methods**:

- `__init__(self, language: str = 'en', currency: str = 'usd', *args, **kwargs)`: Initializes an instance of the `AliApi` class, setting the language and currency for API requests and handling authentication.

- `retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None`: Retrieves product details for a given list of product IDs. It calls the `retrieve_product_details` method of the parent class and then converts the returned list of `SimpleNamespace` objects to a list of dictionaries.

- `get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]`: Retrieves affiliate links for the specified products. It calls the `get_affiliate_links` method of the parent class and returns a list of `SimpleNamespace` objects containing affiliate links.

## Class Methods

### `retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None`

```python
    def retrieve_product_details_as_dict(self, product_ids: list) -> dict | dict | None:
        """ 
        Отправляет список ID товаров на AliExpress и получает список объектов SimpleNamespace с описанием товаров.
        
        Args:
            product_ids (list): Список ID товаров.
        
        Returns:
            dict | None: Список данных о товарах в виде словарей.
        
        Example:
            # Преобразование из формата SimpleNamespace в dict
            namespace_list = [
                SimpleNamespace(a=1, b=2, c=3),
                SimpleNamespace(d=4, e=5, f=6),
                SimpleNamespace(g=7, h=8, i=9)
            ]
            
            # Преобразование каждого объекта SimpleNamespace в словарь
            dict_list = [vars(ns) for ns in namespace_list]
            
            # Альтернативно, используйте метод __dict__:
            dict_list = [ns.__dict__ for ns in namespace_list]
            
            # Вывод списка словарей
            print(dict_list)
        """
        prod_details_ns = self.retrieve_product_details(product_ids)
        prod_details_dict = [vars(ns) for ns in prod_details_ns]
        return prod_details_dict
```

**Purpose**: This method retrieves product details from AliExpress for a given list of product IDs. It calls the `retrieve_product_details` method of the parent class, which sends a request to the AliExpress API, and then converts the response data from `SimpleNamespace` objects to dictionaries.

**Parameters**:

- `product_ids` (list): A list of product IDs to retrieve details for.

**Returns**:

- `dict | None`: A list of dictionaries containing product details, or `None` if an error occurs.

**How the Function Works**:

1. The method calls the `retrieve_product_details` method of the parent class, passing the `product_ids` list. This method sends a request to the AliExpress API to retrieve product details for the specified IDs.
2. The `retrieve_product_details` method returns a list of `SimpleNamespace` objects, where each object represents a product with its attributes.
3. The `retrieve_product_details_as_dict` method then iterates through the list of `SimpleNamespace` objects and converts each object to a dictionary using the `vars` function. 
4. The function finally returns the list of dictionaries containing product details.

**Examples**:

```python
# Example 1: Retrieving details for a single product
product_id = 123456789
product_details = aliapi.retrieve_product_details_as_dict([product_id])
pprint(product_details)

# Example 2: Retrieving details for multiple products
product_ids = [123456789, 987654321, 1011121314]
product_details = aliapi.retrieve_product_details_as_dict(product_ids)
pprint(product_details)
```

### `get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]`

```python
    def get_affiliate_links(self, links: str | list, link_type: int = 0, **kwargs) -> List[SimpleNamespace]:
        """ 
        Извлекает партнерские ссылки для указанных товаров.
        
        Args:
            links (str | list): Ссылки на товары, которые необходимо обработать.
            link_type (int, optional): Тип партнерской ссылки, которую нужно сгенерировать. По умолчанию 0.
        
        Returns:
            List[SimpleNamespace]: Список объектов SimpleNamespace, содержащих партнерские ссылки.
        """
        return super().get_affiliate_links(links, link_type, **kwargs)
```

**Purpose**: This method retrieves affiliate links for the specified products. It calls the `get_affiliate_links` method of the parent class, passing the product links and the desired affiliate link type.

**Parameters**:

- `links` (str | list): A single product link or a list of product links to generate affiliate links for.
- `link_type` (int, optional): The type of affiliate link to generate. Defaults to 0.

**Returns**:

- `List[SimpleNamespace]`: A list of `SimpleNamespace` objects containing affiliate links for the specified products.

**How the Function Works**:

1. The method calls the `get_affiliate_links` method of the parent class, passing the `links` and `link_type` arguments.
2. The `get_affiliate_links` method of the parent class sends a request to the AliExpress API to generate affiliate links for the provided product links and the specified link type.
3. The API response is parsed and returned as a list of `SimpleNamespace` objects, each containing the affiliate link for a corresponding product.

**Examples**:

```python
# Example 1: Generating affiliate links for a single product
product_link = 'https://www.aliexpress.com/item/10000000000000000.html'
affiliate_links = aliapi.get_affiliate_links(product_link)
pprint(affiliate_links)

# Example 2: Generating affiliate links for multiple products
product_links = [
    'https://www.aliexpress.com/item/10000000000000000.html',
    'https://www.aliexpress.com/item/20000000000000000.html',
    'https://www.aliexpress.com/item/30000000000000000.html'
]
affiliate_links = aliapi.get_affiliate_links(product_links)
pprint(affiliate_links)
```

## Parameter Details

- `product_ids` (list): A list of product IDs to retrieve details for.
- `links` (str | list): A single product link or a list of product links to generate affiliate links for.
- `link_type` (int, optional): The type of affiliate link to generate. Defaults to 0.

## Examples

```python
# Create an instance of the AliApi class
aliapi = AliApi(language='en', currency='usd')

# Retrieve product details for a single product
product_id = 123456789
product_details = aliapi.retrieve_product_details_as_dict([product_id])
pprint(product_details)

# Retrieve affiliate links for a single product
product_link = 'https://www.aliexpress.com/item/10000000000000000.html'
affiliate_links = aliapi.get_affiliate_links(product_link)
pprint(affiliate_links)
```