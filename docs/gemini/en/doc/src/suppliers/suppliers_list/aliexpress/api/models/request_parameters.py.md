# Module Name

## Overview

The module `src.suppliers.suppliers_list.aliexpress.api.models.request_parameters.py` contains the definition of classes for different parameters used in AliExpress API requests. These parameters are crucial for specifying product types, sorting criteria, and link types, facilitating efficient and targeted data retrieval from the AliExpress platform.

## Details

This module defines a set of classes that serve as containers for various parameters used in API requests to AliExpress. The classes are specifically designed to ensure type safety and consistency in the parameters passed to the API. This approach helps in reducing errors and enhancing the reliability of the data retrieval process.

## Classes

### `ProductType`

**Description**: This class represents the available product types for filtering data from AliExpress.

**Attributes**:

- `ALL` (`str`): Represents the option to retrieve all product types.
- `PLAZA` (`str`): Represents the option to retrieve products from Plaza platform.
- `TMALL` (`str`): Represents the option to retrieve products from TMall platform.

### `SortBy`

**Description**: This class defines various sorting criteria for AliExpress products.

**Attributes**:

- `SALE_PRICE_ASC` (`str`): Represents sorting by sale price in ascending order.
- `SALE_PRICE_DESC` (`str`): Represents sorting by sale price in descending order.
- `LAST_VOLUME_ASC` (`str`): Represents sorting by last volume in ascending order.
- `LAST_VOLUME_DESC` (`str`): Represents sorting by last volume in descending order.

### `LinkType`

**Description**: This class defines the different types of links used in AliExpress API requests.

**Attributes**:

- `NORMAL` (`int`): Represents a normal link type.
- `HOTLINK` (`int`): Represents a hotlink type.