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
This code block provides functions for converting XML data into dictionaries. It includes functions for parsing XML strings and converting XML element trees into dictionary representations.

Execution Steps
-------------------------
1. **Parsing XML Nodes (`_parse_node`)**: The `_parse_node` function takes an XML element (node) and creates a dictionary representation of it. It iterates through the node's attributes and children, creating a hierarchical dictionary structure. 
2. **Creating a Dictionary (`_make_dict`)**: The `_make_dict` function takes a tag name and a value and constructs a dictionary with the tag name as the key and the value as the dictionary value. It also handles namespaces in tag names, extracting them and storing them in the dictionary. 
3. **Converting XML String to Dictionary (`xml2dict`)**: The `xml2dict` function converts an XML string into a dictionary. It uses the `ET.fromstring` method to parse the XML string into an element tree, and then calls the `ET2dict` function to convert the element tree into a dictionary. 
4. **Converting Element Tree to Dictionary (`ET2dict`)**: The `ET2dict` function converts an XML element tree into a dictionary. It uses the `_make_dict` function to create the dictionary representation.

Usage Example
-------------------------

```python
from src.utils.convertors.xml2dict import xml2dict

xml_string = """
<data>
  <item id="1">
    <name>Alice</name>
    <age>30</age>
  </item>
</data>
"""

data_dict = xml2dict(xml_string)

print(data_dict)  # Output: {'data': {'item': {'attrs': {'id': '1'}, 'name': 'Alice', 'age': '30'}}} 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".