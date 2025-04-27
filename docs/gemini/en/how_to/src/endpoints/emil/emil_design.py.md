**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `EmilDesign` Class
=========================================================================================

Description
-------------------------
The `EmilDesign` class is responsible for managing and processing images, as well as promoting them on Facebook and PrestaShop. It specifically targets the `emil-design.com` store. 

Key Features:
- Uses Gemini AI for image description generation.
- Uploads product descriptions to PrestaShop.
- Promotes images and descriptions to Facebook.

Execution Steps
-------------------------
1. **Initialization**: Create an instance of the `EmilDesign` class. This will load the necessary configurations and initialize connections to external services.
2. **Supplier Processing**: Use the `process_suppliers()` method to process images and descriptions for specific suppliers. This method allows you to specify a prefix or a list of prefixes for the desired suppliers.
3. **Image Description**: Utilize the `describe_images()` method to generate descriptions for images. It supports both Gemini and OpenAI models and provides control over the language and model configurations.
4. **Facebook Promotion**: The `promote_to_facebook()` method handles promoting images and descriptions to a designated Facebook group.
5. **PrestaShop Upload**: Leverage the `upload_described_products_to_prestashop()` method to upload product information, including descriptions, to PrestaShop. This method allows you to specify the language for the upload.

Usage Example
-------------------------

```python
from src.endpoints.emil.emil_design import EmilDesign

# Create an instance of the EmilDesign class
emil = EmilDesign()

# Process suppliers based on a specific prefix
asyncio.run(emil.process_suppliers(supplier_prefix='prefix_name'))

# Describe images in Hebrew
emil.describe_images(lang='he')

# Upload described products to PrestaShop in Hebrew
emil.upload_described_products_to_prestashop(id_lang='he')

# Promote images to Facebook
asyncio.run(emil.promote_to_facebook())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".