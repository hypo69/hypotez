# # \file /src/utils/xml.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. module:: src.utils.xml 
	:platform: Windows, Unix
	:synopsis:"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

def clean_empty_cdata(xml_string: str) -> str:
    """! Cleans empty CDATA sections and unnecessary whitespace in XML string.

    Args:
        xml_string (str): Raw XML content.

    Returns:
        str: Cleaned and formatted XML content."""
    root = ET.fromstring(xml_string)
    
    def remove_empty_elements(element):
        for child in list(element):
            remove_empty_elements(child)
            if not (child.text and child.text.strip()) and not child.attrib and not list(child):
                element.remove(child)

    remove_empty_elements(root)
    cleaned_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
    cleaned_xml = re.sub(r">\s+<", "><", cleaned_xml)  # Remove unnecessary whitespace
    return cleaned_xml

def save_xml(xml_string: str, file_path: str) -> None:
    """! Saves cleaned XML data from a string to a file with indentation.

    Args:
        xml_string (str): XML content as a string.
        file_path (str): Path to the output file.

    Returns:
        None"""
    # Cleaning XML from empty elements
    cleaned_xml = clean_empty_cdata(xml_string)
    
    # Error 500 (Server Error)!!1500.That’s an error.There was an error. Please try again later.That’s all we know.
    xml_tree = ET.ElementTree(ET.fromstring(cleaned_xml))
    
    # We convert into a line with retreats
    rough_string = ET.tostring(xml_tree.getroot(), encoding="utf-8")
    parsed_xml = minidom.parseString(rough_string)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")

    # Record to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(pretty_xml)




if __name__ == '__main__':
    ...
    # An example of use
    # xml_data = """<root><item>Value</item><item attr="test">Another</item></root>"""
    # save_xml(xml_data, "output.xml")
