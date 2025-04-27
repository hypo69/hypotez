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
The code block defines several functions for converting data between dictionaries and various formats, including SimpleNamespace objects, XML, CSV, JSON, XLS, HTML, and PDF. 

Execution Steps
-------------------------
1. **`replace_key_in_dict` function**: This function recursively replaces a specified key with a new key within a dictionary or list.
2. **`dict2ns` function**: This function recursively converts dictionaries to SimpleNamespace objects.
3. **`dict2xml` function**: This function generates an XML string from a dictionary.
4. **`dict2csv`, `dict2xls`, `dict2json` functions**: These functions save dictionary or SimpleNamespace data to the respective file formats (CSV, XLS, JSON).
5. **`dict2html` function**: This function generates an HTML table string from a dictionary or SimpleNamespace object.
6. **`dict2pdf` function**: This function saves dictionary data as a PDF file.

Usage Example
-------------------------

```python
    from src.utils.convertors.dict import dict2ns, dict2xml, dict2csv, dict2xls, dict2html, dict2pdf

    # Example data
    data = {
        "product": {
            "name": "Test Product",
            "price": "10.00",
            "id_tax_rules_group": "13",
            "id_category_default": "2"
        }
    }

    # Convert dictionary to SimpleNamespace
    ns_data = dict2ns(data)
    print(ns_data)  # Output: namespace(product=namespace(name='Test Product', price='10.00', id_tax_rules_group='13', id_category_default='2'))

    # Generate XML string
    xml_string = dict2xml(data)
    print(xml_string)  # Output: XML string representing the dictionary

    # Save to CSV file
    dict2csv(data, "product_data.csv")

    # Save to XLS file
    dict2xls(data, "product_data.xls")

    # Generate HTML table
    html_string = dict2html(data)
    print(html_string)  # Output: HTML table string

    # Save to PDF
    dict2pdf(data, "product_data.pdf")

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".