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
This code snippet implements unit tests for the integration of GPT-4 Free (g4f) with different providers like Bing (Copilot) and OpenAI (DDG). It covers both synchronous and asynchronous chat completion scenarios.

Execution Steps
-------------------------
1. **Import Necessary Libraries**: The code imports the required libraries like `unittest`, `json`, `g4f.client`, `g4f.Provider`.
2. **Define Default Messages**: A list of default messages is defined, which includes a system message and a user message.
3. **Create Test Classes**: Two test classes are defined: `TestProviderIntegration` and `TestChatCompletionAsync`.
4. **Define Test Methods**: Each test class contains methods that test the integration with specific providers.
    - `test_bing` and `test_openai` in `TestProviderIntegration` test the synchronous chat completion for Bing and OpenAI providers respectively.
    - `test_bing` and `test_openai` in `TestChatCompletionAsync` test the asynchronous chat completion for Bing and OpenAI providers respectively.
5. **Create Clients**: Within each test method, a `Client` or `AsyncClient` is created using the appropriate provider (`Copilot` for Bing, `DDG` for OpenAI).
6. **Generate Chat Completions**: The `create` method of the client's `chat.completions` object is used to generate chat completions, passing the default messages, an empty string for additional context, and a response format to get a JSON object.
7. **Verify Response Type**: The response is asserted to be an instance of `ChatCompletion`.
8. **Check for Success Key**: The content of the response message is parsed as JSON, and it is asserted that the JSON contains the key `"success"`.

Usage Example
-------------------------

```python
    from g4f.client import Client, AsyncClient, ChatCompletion
    from g4f.Provider import Copilot, DDG

    # Synchronous chat completion with Bing (Copilot)
    client = Client(provider=Copilot)
    response = client.chat.completions.create(
        [{"role": "system", "content": 'Response in json, Example: {"success": false}'},
         {"role": "user", "content": "Say success true in json"}],
        "",
        response_format={"type": "json_object"}
    )
    assert isinstance(response, ChatCompletion)
    assert "success" in json.loads(response.choices[0].message.content)

    # Asynchronous chat completion with OpenAI (DDG)
    async_client = AsyncClient(provider=DDG)
    response = await async_client.chat.completions.create(
        [{"role": "system", "content": 'Response in json, Example: {"success": false}'},
         {"role": "user", "content": "Say success true in json"}],
        "",
        response_format={"type": "json_object"}
    )
    assert isinstance(response, ChatCompletion)
    assert "success" in json.loads(response.choices[0].message.content)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".