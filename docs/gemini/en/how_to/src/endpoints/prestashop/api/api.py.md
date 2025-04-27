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
This code block defines the `PrestaShop` class which provides methods to interact with the PrestaShop API, allowing for CRUD operations, searching, and uploading images. It also provides error handling for responses and methods to handle the API's data.

Execution Steps
-------------------------
1. **Initialize PrestaShop Object**:
    - Creates an instance of the `PrestaShop` class, passing in the necessary parameters like API key, domain, data format, default language, and debug mode.
    - The constructor sets up the API domain, API key, debug mode, language, and data format.
    - It performs a HEAD request to the API domain to check the connection and retrieve the PrestaShop version.

2. **Perform API Requests**:
    - Provides methods to execute different API operations:
        - `ping()`: Tests the API connection.
        - `create()`: Creates a new resource.
        - `read()`: Reads a resource.
        - `write()`: Updates a resource.
        - `unlink()`: Deletes a resource.
        - `search()`: Searches for resources.
        - `create_binary()`: Uploads a binary file (image).
        - `get_schema()`: Retrieves the schema of a resource.
        - `get_data()`: Fetches data from an API resource.
        - `get_apis()`: Gets a list of available APIs.
        - `upload_image_async()`: Uploads an image asynchronously.
        - `upload_image_from_url()`: Uploads an image from a URL.
        - `get_product_images()`: Gets images for a product.

3. **Handle Responses**:
    - Parses the responses from the API, handling both successful and error responses.
    - Logs errors using the `logger` module and returns appropriate data structures or error codes.

Usage Example
-------------------------

```python
from src.endpoints.prestashop.api import PrestaShop

api = PrestaShop(
    api_domain='https://your-prestashop-domain.com',
    api_key='your_api_key',
    default_lang=1,
    debug=True,
    data_format='JSON',
)

# Test API connection
api.ping()

# Create a new tax record
data = {
    'tax': {
        'rate': 3.000,
        'active': '1',
        'name': {
            'language': {
                'attrs': {'id': '1'},
                'value': '3% tax'
            }
        }
    }
}
rec = api.create('taxes', data)

# Update the tax record
update_data = {
    'tax': {
        'id': str(rec['id']),
        'rate': 3.000,
        'active': '1',
        'name': {
            'language': {
                'attrs': {'id': '1'},
                'value': '3% tax'
            }
        }
    }
}
update_rec = api.write('taxes', update_data)

# Delete the tax record
api.unlink('taxes', str(rec['id']))

# Search for taxes with '5' in the name
import pprint
recs = api.search('taxes', filter='[name]=%[5]%', limit='3')
for rec in recs:
    pprint(rec)

# Upload a product image
api.create_binary('images/products/22', 'img.jpeg', 'image')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".