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
This code snippet interacts with the Phind API to get responses for user prompts using the `gpt-4` or `gpt-3.5` models. It constructs a JSON request body with user's prompt and model-specific parameters and sends it to Phind's API. It handles the response in chunks and prints the final response.

Execution Steps
-------------------------
1. **Import necessary modules**: Imports `sys`, `json`, `datetime`, `urllib.parse`, and `requests` from `curl_cffi`.
2. **Load configuration**: Loads configuration from the command-line argument `sys.argv[1]`, which is a JSON string.
3. **Extract prompt and skill**: Extracts the user prompt from the configuration and sets the `skill` based on the model (`gpt-4` or `gpt-3.5`).
4. **Construct JSON data**: Constructs a JSON data structure with the `question` (user prompt) and `options` (skill, date, language, detailed, creative, customLinks).
5. **Set headers**: Defines headers for the HTTP request to Phind's API, including Content-Type, Pragma, Accept, User-Agent, Referer, Connection, Host, etc.
6. **Define output function**: Defines a function to process the response in chunks, filtering out metadata and printing the output to the console.
7. **Send the request and process the response**: Sends a POST request to Phind's API with the constructed JSON data and headers. The `content_callback` parameter uses the `output` function to process the response in chunks.
8. **Handle errors**: Catches any exceptions during the request process and retries the request.

Usage Example
-------------------------

```python
    # Example configuration JSON
    config = {
        'messages': [
            {'role': 'user', 'content': 'What is the meaning of life?'}
        ],
        'model': 'gpt-4'
    }

    # Convert the config to JSON string
    config_json = json.dumps(config)

    # Run the script with the JSON configuration as an argument
    import subprocess
    subprocess.run(['python', 'path/to/phind.py', config_json])
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".