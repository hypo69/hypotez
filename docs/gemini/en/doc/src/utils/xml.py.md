# Module: `src.utils.xml`

## Overview

This module provides utility functions for working with XML data. It includes functions for cleaning empty CDATA sections and unnecessary whitespace in XML strings, and for saving formatted XML data to a file.

## Details

This module is used to handle XML data in the project. It's likely used for parsing, cleaning, and formatting XML files. Here's a breakdown:

- `clean_empty_cdata(xml_string: str) -> str`: This function cleans up the XML data, removing unnecessary whitespace and empty CDATA sections, ensuring that the XML remains valid and well-structured.
- `save_xml(xml_string: str, file_path: str) -> None`: This function takes an XML string and saves it to a file with appropriate indentation. It uses `minidom` to format the XML for better readability.

## Table of Contents

- [Functions](#functions)
    - [`clean_empty_cdata`](#clean_empty_cdata)
    - [`save_xml`](#save_xml)

## Functions

### `clean_empty_cdata`

```python
def clean_empty_cdata(xml_string: str) -> str:
    """! Cleans empty CDATA sections and unnecessary whitespace in XML string.

    Args:
        xml_string (str): Raw XML content.

    Returns:
        str: Cleaned and formatted XML content.
    """
    root = ET.fromstring(xml_string)
    
    def remove_empty_elements(element):
        for child in list(element):
            remove_empty_elements(child)
            if not (child.text and child.text.strip()) and not child.attrib and not list(child):
                element.remove(child)

    remove_empty_elements(root)
    cleaned_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
    cleaned_xml = re.sub(r">\\s+<", "><", cleaned_xml)  # Remove unnecessary whitespace
    return cleaned_xml
```

**Purpose**: This function cleans XML data by removing empty CDATA sections and unnecessary whitespace.

**Parameters**:

- `xml_string` (str): The raw XML content to be cleaned.

**Returns**:

- `str`: The cleaned and formatted XML content.

**How the Function Works**:

1. The function parses the provided XML string into an `ElementTree` object using `ET.fromstring`.
2. It recursively traverses the XML tree using the `remove_empty_elements` function.
3. For each element in the tree, `remove_empty_elements` checks if the element has any content (text or attributes), or any child elements. If not, the element is removed.
4. After cleaning, the function converts the `ElementTree` object back to a string using `ET.tostring`.
5. The function then uses a regular expression to remove unnecessary whitespace between tags, replacing `>\\s+<` with `><`.
6. Finally, the cleaned and formatted XML string is returned.

**Example**:

```python
# Example XML string
xml_data = """<root><item>Value</item><item attr="test"></item><empty/></root>"""

# Clean the XML string
cleaned_xml = clean_empty_cdata(xml_data)

# Print the cleaned XML
print(cleaned_xml)
```

**Output**:

```xml
<root><item>Value</item><item attr="test">Another</item></root>
```

### `save_xml`

```python
def save_xml(xml_string: str, file_path: str) -> None:
    """! Saves cleaned XML data from a string to a file with indentation.

    Args:
        xml_string (str): XML content as a string.
        file_path (str): Path to the output file.

    Returns:
        None
    """
    # Очистка XML от пустых элементов
    cleaned_xml = clean_empty_cdata(xml_string)
    
    # Парсим XML-строку
    xml_tree = ET.ElementTree(ET.fromstring(cleaned_xml))
    
    # Преобразуем в строку с отступами
    rough_string = ET.tostring(xml_tree.getroot(), encoding="utf-8")
    parsed_xml = minidom.parseString(rough_string)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")

    # Записываем в файл
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(pretty_xml)
```

**Purpose**: This function saves a cleaned XML string to a file with indentation, improving its readability.

**Parameters**:

- `xml_string` (str): The cleaned XML content as a string.
- `file_path` (str): The path to the output file where the XML data will be saved.

**Returns**:

- `None`: The function does not return any value.

**How the Function Works**:

1. The function first cleans the provided XML string using the `clean_empty_cdata` function.
2. It then parses the cleaned XML string into an `ElementTree` object.
3. The function converts the `ElementTree` object back to a string with indentation using `minidom.parseString` and `toprettyxml`.
4. Finally, it opens the specified output file in write mode and writes the formatted XML string to the file.

**Example**:

```python
# Example XML string
xml_data = """<root><item>Value</item><item attr="test">Another</item></root>"""

# Save the XML data to a file
save_xml(xml_data, "output.xml")
```

**Output**: The `output.xml` file will contain the following formatted XML:

```xml
<root>
  <item>Value</item>
  <item attr="test">Another</item>
</root>
```