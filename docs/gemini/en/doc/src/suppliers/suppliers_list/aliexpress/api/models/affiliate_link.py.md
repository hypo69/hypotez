# Affiliate Link Model

## Overview

This module defines the `AffiliateLink` class, which represents an affiliate link for AliExpress products. The class stores the promotion link and source value, providing a structured way to handle affiliate links within the `hypotez` project.

## Details

The `AffiliateLink` class is used to manage and process affiliate links retrieved from AliExpress. The class encapsulates the promotion link and source value, simplifying the handling of these essential affiliate link attributes.

## Classes

### `AffiliateLink`

**Description**:  Represents an affiliate link for AliExpress products.

**Attributes**:

- `promotion_link` (str): The actual affiliate link to the product.
- `source_value` (str): The source value associated with the affiliate link.

**Example**:

```python
from hypotez.src.suppliers.aliexpress.api.models.affiliate_link import AffiliateLink

# Creating an AffiliateLink instance
affiliate_link = AffiliateLink(promotion_link='https://www.aliexpress.com/item/1000000000000000.html', source_value='some_source_value')

# Accessing attributes
print(f"Promotion Link: {affiliate_link.promotion_link}")
print(f"Source Value: {affiliate_link.source_value}")
```

## Parameter Details

- `promotion_link` (str): The actual affiliate link to the product. This link redirects users to the product page on AliExpress and includes the affiliate ID.
- `source_value` (str): The source value associated with the affiliate link. This value allows tracking where the affiliate link originated from.

## Examples

```python
from hypotez.src.suppliers.aliexpress.api.models.affiliate_link import AffiliateLink

# Example 1: Creating an AffiliateLink instance
affiliate_link = AffiliateLink(promotion_link='https://www.aliexpress.com/item/1000000000000000.html', source_value='some_source_value')

# Example 2: Accessing attributes
print(f"Promotion Link: {affiliate_link.promotion_link}")
print(f"Source Value: {affiliate_link.source_value}")
```