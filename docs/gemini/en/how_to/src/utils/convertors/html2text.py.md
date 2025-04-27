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
This code block defines the `html2text` module, which converts HTML code into Markdown format. It includes functions for handling entities, unescaping, wrapping, and parsing CSS styles. It also defines a class called `_html2text` which is a subclass of `HTMLParser.HTMLParser` and uses a series of functions to process the HTML content and generate Markdown output.

Execution Steps
-------------------------
1. The code defines various utility functions for handling entities, unescaping, wrapping, and parsing CSS styles.
2. The `_html2text` class is defined, which inherits from `HTMLParser.HTMLParser`. This class overrides methods like `handle_starttag`, `handle_endtag`, and `handle_data` to process the HTML content and convert it to Markdown.
3. The class utilizes various functions to handle different HTML elements like headings, paragraphs, lists, tables, and images.
4. The `html2text_file` function takes an HTML string and an optional output function (defaulting to `wrapwrite`) and a base URL as input, feeds the HTML content to the `_html2text` parser, and returns the parsed Markdown output.
5. The `html2text` function is used to convert the given HTML string into Markdown, optionally providing a base URL.
6. The code also includes a `Storage` class, which is used to store the options passed to the parser.
7. The `__main__` block demonstrates how to use the `html2text` module from the command line, including options for converting Google Docs, specifying unordered list styles, controlling body width, and adjusting Google list indentation.


Usage Example
-------------------------

```python
from src.utils.convertors.html2text import html2text

html_content = """
<!DOCTYPE html>
<html>
<head>
  <title>Example HTML</title>
</head>
<body>
  <h1>Heading 1</h1>
  <p>This is a paragraph of text.</p>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</body>
</html>
"""

markdown_output = html2text(html_content)

print(markdown_output)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".