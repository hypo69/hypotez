**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Contribute to the gpt4free Project
=========================================================================================

Description
-------------------------
This code block provides instructions on how to contribute to the gpt4free project by adding support for new websites.

Execution Steps
-------------------------
1. **Select a Website:** Choose a website from the list provided in the [sites-to-reverse](https://github.com/xtekky/gpt4free/issues/40) issue.
2. **Create Unit Tests:** Implement unit tests for the chosen website and place them in the [./etc/unittest/](https://github.com/xtekky/gpt4free/tree/main/etc/unittest/) directory.
3. **Refactor and Integrate:** Refactor the code and integrate it into the [./g4f](https://github.com/xtekky/gpt4free/tree/main/g4f) directory.

Usage Example
-------------------------

```python
    # 1. Select a website from the list: https://github.com/xtekky/gpt4free/issues/40
    website_url = "https://www.example.com"

    # 2. Create unit tests for the website and place them in ./etc/unittest/
    # ...

    # 3. Refactor the code and integrate it into ./g4f
    # ...
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".