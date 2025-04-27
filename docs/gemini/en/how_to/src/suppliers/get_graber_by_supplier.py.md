**How to Use the `get_graber_by_supplier_url` Function**
=========================================================================================

**Description**
-------------------------
The `get_graber_by_supplier_url` function identifies and returns the appropriate `Graber` object for a given supplier URL. Each supplier has a dedicated `Graber` that extracts field values from the target HTML page.

**Execution Steps**
-------------------------
1. **URL Validation**: The function checks the provided URL against a list of known supplier prefixes (e.g., `aliexpress.com`, `amazon.com`).
2. **Graber Instantiation**: If a match is found, the function instantiates the corresponding `Graber` class (e.g., `AliexpressGraber`, `AmazonGraber`).
3. **Graber Return**: The function returns the instantiated `Graber` object. If no match is found, it returns `None`.

**Usage Example**
-------------------------

```python
    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
    from src.webdriver import Driver # Assumed Driver import

    # Driver Initialization (Example)
    driver = Driver() 
    url = 'https://www.example.com'
    graber = get_graber_by_supplier_url(driver, url, 2) # Example with lang_index = 2

    if graber:
        # Using the graber to extract data
        product_data = graber.get_product_data()
        print(f'Data extracted: {product_data}')
    else:
        # Handling the case when no graber is found
        print(f'No grabber found for URL: {url}')

```

**How to Use the `get_graber_by_supplier_prefix` Function**
=========================================================================================

**Description**
-------------------------
The `get_graber_by_supplier_prefix` function identifies and returns the appropriate `Graber` object based on a supplier prefix.

**Execution Steps**
-------------------------
1. **Prefix Conversion**: The function converts the provided supplier prefix to lowercase.
2. **Graber Matching**: The function compares the lowercase prefix with a list of known supplier prefixes.
3. **Graber Instantiation**: If a match is found, the function instantiates the corresponding `Graber` class.
4. **Graber Return**: The function returns the instantiated `Graber` object. If no match is found, it returns `None`.

**Usage Example**
-------------------------

```python
    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix
    from src.webdriver import Driver # Assumed Driver import

    # Driver Initialization (Example)
    driver = Driver()
    prefix = 'ksp'
    graber = get_graber_by_supplier_prefix(driver, prefix, 2) # Example with lang_index = 2

    if graber:
        # Using the graber to extract data
        product_data = graber.get_product_data()
        print(f'Data extracted: {product_data}')
    else:
        # Handling the case when no graber is found
        print(f'No grabber found for prefix: {prefix}')

```