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
This code block is a Python script that parses data from the `ksp.co.il` website and writes it to a Google Spreadsheet. The script utilizes the `gs`, `ksp`, `GSpreadsheet`, and `GWorksheet` modules to achieve this.

Execution Steps
-------------------------
1. **Initialization**:
    - The script imports the necessary modules.
    - It defines a function `run()` that acts as the main entry point.
    - It sets the spreadsheet ID (`sh_id`) and the root URL (`root`) for the website.

2. **Website Navigation**:
    - The script uses the `Driver` object to navigate to the root URL (`root`).
    - It calls `ksp.get_worlds()` to extract a dictionary of worlds and their corresponding URLs.

3. **Spreadsheet Interaction**:
    - The script creates a `GSpreadsheet` object using the spreadsheet ID (`sh_id`).
    - It iterates through each world in the dictionary:
        - Creates a `GWorksheet` object for the current world using its title.
        - Sets the header row in the worksheet.
        - Fetches the URL for the world's category.
        - Navigates to the category URL using the `Driver` object.
        - Retrieves a list of subcategories and their URLs.
        - Iterates through each subcategory:
            - Navigates to the subcategory URL.
            - Appends a row with the category title to the worksheet.
            - Retrieves a list of brands and their quantities.
            - Iterates through each brand:
                - Appends a row with the brand name and quantity to the worksheet.

4. **Data Extraction**:
    - The script utilizes functions from the `ksp` module to extract data from the website, including worlds, subcategories, and brands.
    - It uses the `pprint` function to print output to the console.

5. **Spreadsheet Management**:
    - The script uses the `GSpreadsheet` and `GWorksheet` objects to interact with the Google Spreadsheet, including creating worksheets, setting headers, and appending rows.


Usage Example
-------------------------

```python
    from src import gs
    from src.logger.logger import logger, WebDriverException,  pprint

    # ... (Rest of the code)

    sh_id = '1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM'
    root: str = 'https://ksp.co.il' 
    d.get(root)
    worlds_dic: dict = ksp.get_worlds()

    sh = GSpreadsheet(sh_id)
    for url, ws_title in worlds_dic.items():
        ws: GWorksheet = GWorksheet(sh, ws_title)
        # ... (Rest of the code)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".