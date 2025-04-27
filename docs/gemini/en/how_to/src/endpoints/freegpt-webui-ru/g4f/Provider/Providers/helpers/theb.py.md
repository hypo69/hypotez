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
This code block interacts with the TheB chatbot API to generate text responses based on a user's prompt. It fetches a prompt from a JSON configuration, builds a request with appropriate headers and data, and sends it to the TheB API. The response is processed in chunks to provide real-time feedback to the user.

Execution Steps
-------------------------
1. **Load Configuration**: The code begins by loading a JSON configuration from the command line arguments. This configuration contains the prompt and other relevant data for the chatbot interaction.

2. **Extract Prompt**:  The prompt is extracted from the configuration, specifically the last message in the 'messages' array.

3. **Prepare Request**: The code constructs a request to the TheB API by building headers with specific values for authentication and user-agent information. It also prepares JSON data containing the prompt and optional options.

4. **Send Request**: The code sends a POST request to the API endpoint 'https://chatbot.theb.ai/api/chat-process', including the constructed headers and JSON data. It uses the `content_callback` parameter to process the response in chunks.

5. **Process Response**: The response is received and processed in chunks. Each chunk is decoded and parsed to extract the generated text. The text is then printed to the console. If an error occurs during processing, a message is printed, and the process continues.

6. **Exit**: The code exits after successfully sending the request and receiving the response.

Usage Example
-------------------------

```python
    # Example configuration data
    config = {
        'messages': [
            {
                'content': 'What is the meaning of life?'
            }
        ]
    }

    # Convert configuration to a JSON string
    config_json = json.dumps(config)

    # Run the code with the configuration as an argument
    python theb.py '{"messages":[{"content":"What is the meaning of life?"}]}' 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".