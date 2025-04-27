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
This code block provides two functions:
    - `clean_empty_cdata(xml_string: str) -> str`: Removes empty CDATA sections and unnecessary whitespace from an XML string.
    - `save_xml(xml_string: str, file_path: str) -> None`: Saves cleaned XML data from a string to a file with indentation.

Execution Steps
-------------------------
1. **`clean_empty_cdata(xml_string: str) -> str`**
    - Parses the input XML string using `ET.fromstring`.
    - Iterates through each element in the parsed XML tree using a recursive function `remove_empty_elements`.
    - Removes empty elements (elements without text, attributes, or child elements).
    - Removes unnecessary whitespace using a regular expression.
    - Returns the cleaned XML string.

2. **`save_xml(xml_string: str, file_path: str) -> None`**
    - Cleans the input XML string using `clean_empty_cdata`.
    - Parses the cleaned XML string using `ET.fromstring` and creates an `ElementTree` object.
    - Converts the `ElementTree` object into a string with indentation using `minidom.parseString` and `toprettyxml`.
    - Saves the formatted XML content to the specified file path.

Usage Example
-------------------------

```python
    # Example XML data
    xml_data = """<root><item>Value</item><item attr="test">Another</item></root>"""

    # Clean and save the XML data to a file
    save_xml(xml_data, "output.xml")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".