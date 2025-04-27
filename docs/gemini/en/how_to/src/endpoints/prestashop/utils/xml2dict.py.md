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
The `xml2dict` module provides functions to convert XML data into a Python dictionary. This module is particularly useful for working with PrestaShop API responses, which are in XML format. The `xml2dict` module handles namespaces, attributes, and nested elements effectively, allowing you to access and manipulate XML data as a Python dictionary.

Execution Steps
-------------------------
1. **Import necessary modules**: The code starts by importing the `re` module for regular expressions and the `xml.etree.ElementTree` module for XML parsing.
2. **Define `_parse_node(node)`**: This function recursively parses a single XML node, converting it to a dictionary. 
    - **Iterate over attributes**: It extracts attributes from the node, handling namespaces and creating a nested `'attrs'` dictionary.
    - **Extract node text**: The function extracts the node's text value.
    - **Process child nodes**: It iterates over child nodes, recursively calling itself to parse them, and then combines the resulting dictionaries into a single nested dictionary.
    - **Create a list for multiple elements**: If the same tag appears multiple times, the function creates a list to store multiple values.
3. **Define `_make_dict(tag, value)`**: This function creates a dictionary entry from a tag and its value, handling namespaces and storing them as the `'xmlns'` key.
4. **Define `xml2dict(xml)`**: This function takes an XML string as input and converts it to a dictionary using the `ET.fromstring()` function to parse the XML and `ET2dict()` to process the resulting element tree.
5. **Define `ET2dict(element_tree)`**: This function takes an `ElementTree` object as input and converts it to a dictionary using `_make_dict()` to create the root dictionary and `_parse_node()` to parse the element tree.
6. **Main execution**: The `if __name__ == '__main__'` block includes example XML strings and demonstrates how to use `xml2dict()` and `ET2dict()` functions to convert XML to dictionaries.

Usage Example
-------------------------

```python
from src.endpoints.prestashop.utils.xml2dict import xml2dict

xml_string = """
<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
<addresses>
<address id="1" xlink:href="http://localhost:8080/api/addresses/1"/>
<address id="2" xlink:href="http://localhost:8080/api/addresses/2"/>
<address id="3" xlink:href="http://localhost:8080/api/addresses/3"/>
<address id="4" xlink:href="http://localhost:8080/api/addresses/4"/>
<address id="5" xlink:href="http://localhost:8080/api/addresses/5"/>
<address id="6" xlink:href="http://localhost:8080/api/addresses/6"/>
<address id="7" xlink:href="http://localhost:8080/api/addresses/7"/>
<address id="8" xlink:href="http://localhost:8080/api/addresses/8"/>
</addresses>
</prestashop>
"""

# Convert XML to dictionary
data = xml2dict(xml_string)

# Access data from the dictionary
print(data['prestashop']['addresses']['address'][0]['id'])
# Output: 1
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".