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
This code snippet defines a class called `ChatGpt` and implements a method called `yeld_conversations_htmls` that iterates through HTML files in a specific directory and returns their content.

Execution Steps
-------------------------
1. **Initialize a `ChatGpt` instance**: Create an object of the `ChatGpt` class.
2. **Call the `yeld_conversations_htmls` method**: This method will:
    - Define a directory path for conversation HTML files.
    - Use `glob` to find all HTML files within the specified directory.
    - Iterate through each HTML file and yield its content.

Usage Example
-------------------------

```python
from src.suppliers.chat_gpt.chat_gpt import ChatGpt

chat_gpt_instance = ChatGpt()

for html_content in chat_gpt_instance.yeld_conversations_htmls():
    # Process the HTML content as needed
    print(html_content)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".