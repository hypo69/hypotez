**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `save_pdf_pdfkit` Function
=========================================================================================

Description
-------------------------
The `save_pdf_pdfkit` function in the `PDFUtils` class uses the `pdfkit` library to convert HTML content or files to PDF format. It utilizes the `wkhtmltopdf` executable to perform the conversion.

Execution Steps
-------------------------
1. **Check for `wkhtmltopdf.exe`**: The function first checks if the `wkhtmltopdf.exe` executable is present in the specified path. If not found, an error is logged and a `FileNotFoundError` is raised.
2. **Configure `pdfkit`**: The function sets up `pdfkit` with the path to the `wkhtmltopdf.exe` executable.
3. **Handle Input**:  The function accepts either HTML content as a string (`data` argument) or a file path (`data` argument).
4. **Convert to PDF**:  The function uses `pdfkit.from_string` or `pdfkit.from_file` to convert the HTML to PDF, saving the output to the specified `pdf_file` path.
5. **Log Success**:  If the conversion is successful, a success message is logged.
6. **Handle Errors**: The function includes a `try...except` block to catch potential errors during the conversion process. If an error occurs, it is logged and the function returns `False`.

Usage Example
-------------------------

```python
from src.utils.pdf import PDFUtils

# Example 1: Convert HTML content to PDF
html_content = "<html><body><h1>Hello, world!</h1></body></html>"
pdf_file_path = "output.pdf"
result = PDFUtils.save_pdf_pdfkit(html_content, pdf_file_path)

# Example 2: Convert an HTML file to PDF
html_file_path = "index.html"
pdf_file_path = "output.pdf"
result = PDFUtils.save_pdf_pdfkit(html_file_path, pdf_file_path)

if result:
    print("PDF conversion successful!")
else:
    print("PDF conversion failed.")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".