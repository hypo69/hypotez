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
The code defines a `AffiliateLink` class with two attributes: `promotion_link` and `source_value`.  It is likely used to represent an affiliate link from AliExpress.

Execution Steps
-------------------------
1. Defines a class named `AffiliateLink`.
2. Defines two attributes: `promotion_link` (a string representing the affiliate link) and `source_value` (a string representing the source of the link). 

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.models.affiliate_link import AffiliateLink

affiliate_link = AffiliateLink()
affiliate_link.promotion_link = "https://www.aliexpress.com/item/4000000000000.html?aff=xxxxxxxx"
affiliate_link.source_value = "aliexpress_api"

print(affiliate_link.promotion_link)
# Output: https://www.aliexpress.com/item/4000000000000.html?aff=xxxxxxxx
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".