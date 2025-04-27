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
This code snippet defines functions for converting HTML content. It provides functions to escape HTML tags, unescape them, convert HTML to a dictionary, and convert it to a SimpleNamespace object. Additionally, it includes a function for converting HTML content to a PDF document using WeasyPrint.

Execution Steps
-------------------------
1. The code snippet imports necessary libraries like `re`, `typing`, `Path`, `logger`, `SimpleNamespace`, `HTMLParser`, `pisa`, `subprocess`, `Path`, and `os`. 
2. The code defines a function `html2escape` which escapes HTML tags to escape sequences. 
3. It defines a function `escape2html` which unescapes HTML tags from escape sequences to original HTML.
4. It defines a function `html2dict` which converts HTML to a dictionary where tags are keys and content are values.
5. It defines a function `html2ns` which converts HTML to a SimpleNamespace object where tags are attributes and content are values. 
6. It defines a function `html2pdf` which converts HTML content to a PDF file using WeasyPrint.
7. It defines a function `html_to_docx` which converts HTML file to a DOCX file using LibreOffice.

Usage Example
-------------------------

```python
from src.utils.convertors.html import html2escape, escape2html, html2dict, html2ns, html2pdf

# Escape HTML tags
escaped_html = html2escape("<p>Hello, world!</p>")
print(escaped_html)  # Output: &lt;p&gt;Hello, world!&lt;/p&gt;

# Unescape HTML tags
unescaped_html = escape2html("&lt;p&gt;Hello, world!&lt;/p&gt;")
print(unescaped_html)  # Output: <p>Hello, world!</p>

# Convert HTML to dictionary
html_dict = html2dict("<p>Hello</p><a href='link'>World</a>")
print(html_dict)  # Output: {'p': 'Hello', 'a': 'World'}

# Convert HTML to SimpleNamespace
html_ns = html2ns("<p>Hello</p><a href='link'>World</a>")
print(html_ns.p)  # Output: Hello
print(html_ns.a)  # Output: World

# Convert HTML to PDF
html2pdf("<p>Hello, world!</p>", "output.pdf")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".