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
The `QuotationBuilder` class is designed to extract, parse, and save product data from various suppliers. It leverages AI processing and integrates with Facebook for product posting.

Execution Steps
-------------------------
1. **Initialization:** The `__init__` method sets up the Mexiron process by initializing the WebDriver, loading the AI model with instructions, and defining essential fields.
2. **Product Field Conversion:** The `convert_product_fields` function transforms product data from the `ProductFields` object into a dictionary suitable for the AI model.
3. **AI Processing:** The `process_llm` and `process_llm_async` methods interact with the AI model (Gemini) to generate product descriptions in different languages (currently `ru` and `he`).
4. **Data Saving:** The `save_product_data` method asynchronously stores individual product data to JSON files.
5. **Facebook Posting:** The `post_facebook_async` function handles the Facebook posting process, including sending the title, media, and publishing the post.

Usage Example
-------------------------

```python
# Initialize the QuotationBuilder class
quotation = QuotationBuilder(mexiron_name='250203025325520', driver='firefox')

# Process product data
product_data = quotation.convert_product_fields(f)

# Get AI-generated descriptions
ru_description, he_description = quotation.process_llm(product_data, lang='he')

# Save the processed product data to a JSON file
quotation.save_product_data(product_data)

# Post the product to Facebook
quotation.post_facebook_async(mexiron)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".