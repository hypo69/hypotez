**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `md2dict` Function
=========================================================================================

Description
-------------------------
The `md2dict` function converts a Markdown string into a structured dictionary, extracting JSON content if present.

Execution Steps
-------------------------
1. **Convert Markdown to HTML**: The function first converts the Markdown string into HTML using the `md2html` function.
2. **Parse HTML for Sections**: The function iterates through each line of the HTML, identifying heading tags (h1, h2, etc.) and their content. 
3. **Organize Sections**: The function creates a dictionary with keys representing section titles and values representing lists of text content within each section.
4. **Extract JSON**: If JSON content is detected within the Markdown string, it is extracted and processed. 
5. **Return Dictionary**: The function returns the structured dictionary containing the parsed Markdown content. 

Usage Example
-------------------------

```python
from src.utils.convertors.md2dict import md2dict

md_string = """
# My Markdown Document

This is some text.

## Section 1

This is the first section.

## Section 2

This is the second section.

```json
{
  "key1": "value1",
  "key2": "value2"
}
```
"""

sections = md2dict(md_string)
print(sections)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".