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
This code block handles various tool calls within a conversational AI system. It defines classes for managing authentication, processing thinking chunks, and handling specific tools like web search and bucket access. The core function `iter_run_tools` orchestrates the tool execution, asynchronously or synchronously, and yields the results along with any relevant sources.

Execution Steps
-------------------------
1. **Web Search**:  If a `web_search` parameter is provided, the code initiates a web search based on the query and updates the messages with the search results.
2. **API Key**: If the provider requires authentication, the code attempts to load the API key from a configuration file.
3. **Tool Calls**: It processes each tool call defined in `tool_calls`, including functions for search, continuation, and bucket access. 
4. **Response Generation**: The code uses the provider's `get_async_create_function` to generate a response based on the provided model, messages, and additional parameters. 
5. **Thinking Chunk Processing**:  It iterates through the response chunks and processes thinking indicators like `<think>` and `</think>` to provide informative status updates.
6. **Yielding Results**: It yields the processed response chunks, source information, and any completion or reasoning status updates. 

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.tools.run_tools import iter_run_tools

# Example messages
messages = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"}
]

# Example tool calls
tool_calls = [
    {
        "type": "function",
        "function": {
            "name": "search_tool",
            "arguments": {
                "query": "What is the history of Paris?" 
            }
        }
    }
]

# Example provider
provider = "OpenaiAccount"

# Example model
model = "gpt-3.5-turbo"

# Example keyword arguments
kwargs = {"temperature": 0.7}

# Generate responses
for chunk in iter_run_tools(provider, model, messages, tool_calls, **kwargs):
    print(chunk)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".