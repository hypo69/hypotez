**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code defines three classes: `ProductType`, `SortBy`, and `LinkType`. These classes provide constants representing different product types, sorting options, and link types used in AliExpress API requests.

Execution Steps
-------------------------
1. **Defines the `ProductType` class**:
   - Contains constants `ALL`, `PLAZA`, and `TMALL`, representing all product types, plaza products, and TMALL products respectively.
2. **Defines the `SortBy` class**:
   - Contains constants `SALE_PRICE_ASC`, `SALE_PRICE_DESC`, `LAST_VOLUME_ASC`, and `LAST_VOLUME_DESC`, representing sorting options for sale price ascending, sale price descending, last volume ascending, and last volume descending respectively.
3. **Defines the `LinkType` class**:
   - Contains constants `NORMAL` and `HOTLINK`, representing normal links and hotlinks.

Usage Example
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models.request_parameters import ProductType, SortBy, LinkType

# Get all products sorted by sale price descending
product_type = ProductType.ALL
sort_by = SortBy.SALE_PRICE_DESC

# Use the constants in an API request
api_request_data = {
    "product_type": product_type,
    "sort_by": sort_by
}
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".