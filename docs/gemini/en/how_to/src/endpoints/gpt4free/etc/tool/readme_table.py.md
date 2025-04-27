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
This code block generates a Markdown table containing a list of GPT-4 Free providers, their models, and relevant details. It includes a check for active providers, authentication requirements, and supported features like message history and streaming. 

Execution Steps
-------------------------
1. **Get Active Providers**: The code retrieves a list of active providers from the `__providers__` global list.
2. **Group Providers**: Providers are categorized into "Free" and "Auth" based on their authentication requirements.
3. **Create Table Lines**: For each provider, the code builds Markdown lines for the table, including provider name, website, status, authentication, models, and supported features.
4. **Print Table**: The code prints the generated Markdown lines to the console or a file.

Usage Example
-------------------------

```python
    from g4f import Provider

    # Print provider table to the console
    print_providers()

    # Print provider table to a file
    with open("docs/providers.md", "w") as f:
        f.write("\n".join(print_providers()))
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".