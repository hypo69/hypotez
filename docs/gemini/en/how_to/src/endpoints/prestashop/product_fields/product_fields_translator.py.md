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
This code block implements a function called `translate_presta_fields_dict` that translates product field values from a PrestaShop website to the format used by the client's database. The function takes a dictionary of product fields from PrestaShop, a schema of the client's languages, and the language of the product page (optional). It translates the field values based on the language mapping and updates the `id` attribute of the field values to match the client's database structure.

Execution Steps
-------------------------
1. **Rearrange Language Keys**: The function first calls the `rearrange_language_keys` function to update the language IDs in the PrestaShop field dictionary based on the client's language schema. This step ensures that the language IDs in the PrestaShop data are consistent with the client's database.

2. **Fetch Translations from Database**: The code then fetches existing product translations from the database using the `get_translations_from_presta_translations_table` function. It checks if any translations exist for the given product reference.

3. **Insert New Translations**: If no translations are found in the database, the function creates a new translation record and inserts it into the database using the `insert_new_translation_to_presta_translations_table` function.

4. **Translate Field Values**: The function iterates through the client's language schema and compares the language codes with the translated product data from the database. For each matching language, it retrieves the corresponding translated field values from the database and updates the field values in the PrestaShop dictionary.

5. **Return Translated Data**: The function returns the updated dictionary of product fields containing the translated values.

Usage Example
-------------------------

```python
    # Example usage
    from src.product.product_fields.product_fields_translator import translate_presta_fields_dict

    presta_fields_dict = {
        "reference": "12345",
        "name": {
            "language": [
                {"attrs": {"id": "1"}, "value": "Product Name (English)"},
                {"attrs": {"id": "2"}, "value": "Название продукта (Русский)"},
            ]
        }
    }
    client_langs_schema = [
        {"id": 1, "iso_code": "en", "locale": "en-US", "language_code": "en-us"},
        {"id": 2, "iso_code": "ru", "locale": "ru-RU", "language_code": "ru-ru"},
    ]
    page_lang = "en-US"

    translated_fields = translate_presta_fields_dict(presta_fields_dict, client_langs_schema, page_lang)
    print(translated_fields)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".