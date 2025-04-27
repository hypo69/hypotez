**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `CodeAssistant` Class
=========================================================================================

Description
-------------------------
The `CodeAssistant` class is designed to work with AI models to generate code documentation, examples, and tests. It reads code files, processes them with an AI model, and saves the results in the `docs/gemini` directory. The specific location within `docs/gemini` depends on the role assigned to the class. 

Execution Steps
-------------------------
1. **Initialize `CodeAssistant`**: Create an instance of the `CodeAssistant` class, specifying the role, language, and model to be used.
2. **Process Files**: Call the `process_files()` method to initiate the process of reading code files, generating documentation, and saving the results.

Usage Example
-------------------------

```python
    assistant = CodeAssistant(role='code_checker', lang='ru', model=['gemini'])
    assistant.process_files()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".