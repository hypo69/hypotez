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
This code defines a class `PrestaLanguageAync` that interacts with language settings in PrestaShop. It inherits from the `PrestaShopAsync` class and provides methods for getting language details, adding, deleting, and updating languages.

Execution Steps
-------------------------
1. **Initialize the class**: Create an instance of `PrestaLanguageAync` with necessary parameters.
2. **Access language details**: Call `get_lang_name_by_index` to retrieve the ISO name of a language based on its index in PrestaShop.
3. **Get language schema**: Use `get_languages_schema` to obtain the language schema for the store.
4. **Perform operations**: The class offers methods for adding, deleting, and updating languages in PrestaShop.

Usage Example
-------------------------

```python
from src.endpoints.prestashop.language_async import PrestaLanguageAync

async def main():
    lang_class = PrestaLanguageAync(API_DOMAIN='your_domain', API_KEY='your_api_key')
    language_name = await lang_class.get_lang_name_by_index(1)
    print(f'Language name: {language_name}')

    languages_schema = await lang_class.get_languages_schema()
    print(languages_schema)

if __name__ == '__main__':
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".