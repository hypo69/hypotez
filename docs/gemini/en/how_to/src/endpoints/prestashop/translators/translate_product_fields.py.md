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
This code block defines functions for retrieving and translating product field data from a PrestaShop database. It uses a `ProductTranslationsManager` to interact with the database and a translation engine to translate product fields.

Execution Steps
-------------------------
1. **Retrieving Translations**:
   - The `get_translations_from_presta_translations_table` function retrieves translations for a specific product from the PrestaShop database.
   - It takes the product reference, database credentials, and target language as input.
   - It queries the database using a filter based on the product reference and returns a list of translations.

2. **Inserting New Translations**:
   - The `insert_new_translation_to_presta_translations_table` function inserts a new translation record into the PrestaShop database.
   - It takes a translation record and database credentials as input.
   - It uses the `ProductTranslationsManager` to insert the new record.

3. **Translating Product Fields**:
   - The `translate_record` function translates individual product field values.
   - It takes the record to translate, the source language, and the target language as input.
   - It uses a translation engine (presumably an LLM) to translate the record and returns the translated record.

Usage Example
-------------------------

```python
from src.endpoints.PrestaShop import PrestaShop
from src.product.product_fields.product_fields import record
from src.db import ProductTranslationsManager
from src.llm import translate

# Example product reference and credentials
product_reference = '12345'
credentials = {'host': 'localhost', 'database': 'prestashop', 'user': 'user', 'password': 'password'}

# Retrieve translations for the product
translations = get_translations_from_presta_translations_table(product_reference, credentials, i18n='en_EN')

# Translate a specific field
record_to_translate = {'field_name': 'Product Name', 'value': 'Original Name'}
translated_record = translate_record(record_to_translate, from_locale='en_EN', to_locale='he_HE')

# Insert a new translation
new_translation = {'product_reference': product_reference, 'field_name': 'Product Name', 'value': 'Hebrew Name', 'locale': 'he_HE'}
insert_new_translation_to_presta_translations_table(new_translation, credentials)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".