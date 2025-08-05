**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `ReportGenerator` Class
=========================================================================================

Description
-------------------------
The `ReportGenerator` class handles the generation of HTML and PDF reports based on data loaded from a JSON file. It utilizes Jinja2 templating for HTML generation and PDFkit for PDF conversion. The class includes methods for loading data, generating HTML, saving HTML, generating PDF, and creating a complete report workflow.

Execution Steps
-------------------------
1. **Initialization**: The `__init__` method initializes the class instance with optional arguments for specifying whether to generate PDF and DOCX reports.
2. **Asynchronous Report Creation**: The `create_reports_async` method is the main entry point for creating all types of reports asynchronously. It takes data, language, and other parameters, and performs the following steps:
    - Loads data from a JSON file.
    - Generates HTML using Jinja2 based on the provided data and language.
    - Saves HTML to a file.
    - Generates PDF from the HTML content if `if_need_pdf` is True.
    - Generates DOCX from the HTML content if `if_need_docx` is True.
3. **HTML Report Generation**: The `create_html_report_async` method generates HTML content using Jinja2, rendering a template with the provided data and language.
4. **PDF Report Generation**: The `create_pdf_report_async` method converts the HTML content into a PDF using PDFkit and saves the PDF file.
5. **DOCX Report Generation**: The `create_docx_report_async` method converts the HTML content into a DOCX file.


Usage Example
-------------------------

```python
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator

# Initialize the ReportGenerator
report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=True)

# Load data from a JSON file
data = {"name": "Alice", "age": 30}

# Generate HTML and PDF reports
asyncio.run(report_generator.create_reports_async(data, lang="ru", mexiron_name="250127221657987"))
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".