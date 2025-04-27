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
This code snippet defines a function to interact with a chatbot API called `theb.ai`. It sends a user prompt to the API and retrieves the chatbot's response.

Execution Steps
-------------------------
1. **Load Configuration**: Loads a JSON configuration from the first command line argument. This configuration includes user messages and other settings.
2. **Extract Prompt**: Extracts the user's prompt from the last message in the configuration.
3. **Set Headers**: Defines headers for the HTTP request to the API, including authorization, language preferences, and user agent information.
4. **Prepare JSON Data**: Creates a JSON object with the extracted user prompt and optional options.
5. **Define Format Function**: Creates a function to handle the response from the API in chunks. It extracts the relevant content from each chunk and prints it to the console.
6. **Send API Request**: Sends a POST request to the chatbot API endpoint with the prepared JSON data and headers. It uses the `format` function to process the response in chunks.
7. **Exit on Success**: Exits the program after successfully receiving and processing the response.
8. **Handle Errors**: Includes a try-except block to handle errors during the API request. If an error occurs, the program prints an error message and continues retrying.

Usage Example
-------------------------

```python
    # Example usage with a configuration file:
    # Assuming config.json is a file containing the user prompt and other settings
    python theb.py config.json
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".