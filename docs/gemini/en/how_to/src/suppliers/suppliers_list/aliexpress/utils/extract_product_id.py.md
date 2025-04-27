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
The `extract_prod_ids` function extracts product IDs from a list of URLs or directly returns IDs if given. It accepts a string (single URL) or a list of strings (multiple URLs) as input. 

Execution Steps
-------------------------
1. **Initialization**: The function checks if the input `urls` is a list or a single string.
2. **ID Extraction**: If `urls` is a list, it iterates through each URL and attempts to extract the product ID using a regular expression (`pattern`) and the `extract_id` helper function.
3. **Helper Function**: The `extract_id` function checks if the input is a valid product ID (consisting only of digits). If it is, it directly returns the ID. Otherwise, it uses a regular expression to extract the ID from the URL. 
4. **Output**: If the input was a list, the function returns a list of extracted IDs. If it was a single URL or valid ID, it returns the extracted or input ID respectively. If no valid ID is found, it returns `None`.

Usage Example
-------------------------

```python
    # Example 1: Single URL
    url = "https://www.aliexpress.com/item/123456.html"
    product_id = extract_prod_ids(url)
    print(product_id)  # Output: '123456'

    # Example 2: List of URLs
    urls = ["https://www.aliexpress.com/item/123456.html", "7891011.html"]
    product_ids = extract_prod_ids(urls)
    print(product_ids)  # Output: ['123456', '7891011']

    # Example 3: Invalid URL
    url = "https://www.example.com/item/abcdef.html"
    product_id = extract_prod_ids(url)
    print(product_id)  # Output: None
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".