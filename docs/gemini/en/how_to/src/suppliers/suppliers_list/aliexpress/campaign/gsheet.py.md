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
This code block defines a class `AliCampaignGoogleSheet` that interacts with a Google Sheet spreadsheet used for managing AliExpress campaign data. The class inherits from `SpreadSheet` and provides additional methods for:

- Clearing the spreadsheet.
- Deleting product worksheets.
- Writing campaign data to a worksheet.
- Writing product data to a worksheet.
- Writing category data to a worksheet.
- Formatting the various worksheets.

Execution Steps
-------------------------
1. **Initialize `AliCampaignGoogleSheet`**: Create an instance of the class with the campaign name, language, and currency.
2. **Clear Spreadsheet (Optional)**: Call the `clear()` method to delete product worksheets and clear data from categories and other specified sheets.
3. **Set Campaign Worksheet**: Call `set_campaign_worksheet()` to write campaign data to the 'campaign' worksheet.
4. **Set Products Worksheet**: Call `set_products_worksheet()` for each category to write product data to the respective worksheet.
5. **Set Categories Worksheet**: Call `set_categories_worksheet()` to write category data to the 'categories' worksheet.
6. **Get Categories**: Call `get_categories()` to retrieve category data from the spreadsheet.
7. **Set Category Products**: Call `set_category_products()` to write product data for a specific category to a new worksheet.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.campaign.gsheet import AliCampaignGoogleSheet

# Initialize the spreadsheet
spreadsheet = AliCampaignGoogleSheet(campaign_name='Summer Sale', language='en', currency='USD')

# Clear all product worksheets (optional)
spreadsheet.clear()

# Set campaign data
spreadsheet.set_campaign_worksheet(campaign)

# Set products for a specific category
spreadsheet.set_products_worksheet('Electronics')

# Get categories data
categories_data = spreadsheet.get_categories()

# Set products for a specific category
spreadsheet.set_category_products('Electronics', products)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".