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
This code block implements a translation function using the OpenAI API. It takes source text, the source language, and the target language as input and returns the translated text.

Execution Steps
-------------------------
1. **Initialize OpenAI API Key**: Sets the `openai.api_key` using the credentials from the `gs` module.
2. **Define `translate` Function**:
    - **Input Parameters**: Accepts `text` (the text to be translated), `source_language` (the language of the input text), and `target_language` (the language to translate into).
    - **Formulate Prompt**: Constructs a prompt for the OpenAI API, indicating the translation task and including the source text.
    - **Send Request**: Sends a request to the OpenAI API using the `openai.Completion.create` method, specifying the model (`text-davinci-003`), prompt, and other parameters like `max_tokens`, `n`, `stop`, and `temperature`.
    - **Extract Translation**: Extracts the translated text from the API response and returns it.
    - **Handle Errors**: Logs any exceptions during the translation process using the `logger` module.

Usage Example
-------------------------

```python
    # Example usage
    source_text = "Привет, как дела?"
    source_language = "Russian"
    target_language = "English"

    # Translate the text
    translation = translate(source_text, source_language, target_language)

    # Print the translated text
    print(f"Translated text: {translation}") 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".