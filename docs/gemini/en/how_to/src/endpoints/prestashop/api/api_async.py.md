**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `PrestaShopAsync` Class
=========================================================================================

Description
-------------------------
The `PrestaShopAsync` class provides asynchronous methods to interact with the PrestaShop API, allowing for CRUD operations, searching, and uploading images. It handles error responses and parses data in JSON or XML format. 

Execution Steps
-------------------------
1. **Initialization**:
   - Create an instance of the `PrestaShopAsync` class, providing the API domain, API key, and optional configuration parameters like `data_format`, `debug`, and `default_lang`.
   - The `__init__` method creates a client session using `aiohttp` for making asynchronous requests.

2. **CRUD Operations**:
   - Utilize methods like `create()`, `read()`, `write()`, and `unlink()` to perform create, read, update, and delete operations on PrestaShop resources (e.g., products, categories).
   - These methods use the `_exec()` method to execute the HTTP requests asynchronously.

3. **Search**:
   - Use the `search()` method to retrieve resources based on a search filter.

4. **Image Upload**:
   - Use the `create_binary()` method to upload binary files (e.g., images) to the API.
   - Use the `upload_image()` and `upload_image_async()` methods to upload images by URL.

5. **Data Fetching**:
   - Use the `get_data()` method to fetch data from the API and save it to a JSON file.

6. **API Discovery**:
   - Use the `get_apis()` method to retrieve a list of available APIs.

7. **Language Schema**:
   - Use the `get_languages_schema()` method to retrieve the schema for languages.

Usage Example
-------------------------

```python
import asyncio

async def main():
    api = PrestaShopAsync(
        API_DOMAIN='https://your-prestashop-domain.com',
        API_KEY='your_api_key',
        data_format='JSON',
        debug=True,
    )

    # Ping the API
    await api.ping()

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
    rec = await api.create('taxes', data)

    # Update the same tax record
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
    update_rec = await api.write('taxes', update_data)

    # Remove this tax
    await api.unlink('taxes', str(rec['id']))

    # Search for the first 3 taxes with '5' in the name
    recs = await api.search('taxes', filter='[name]=%[5]%', limit='3')
    for rec in recs:
        print(rec)

    # Upload a product image
    await api.create_binary('images/products/22', 'img.jpeg', 'image')

    # Upload an image from a URL
    await api.upload_image('images/products/22', 22, 'https://example.com/image.png')

    # Get product images
    images = await api.get_product_images(22)
    print(images)

if __name__ == "__main__":
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".