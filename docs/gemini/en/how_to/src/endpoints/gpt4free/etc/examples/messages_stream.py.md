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
This code snippet demonstrates how to use the `g4f.client.AsyncClient` to interact with the OpenAI GPT-4 API for chat completions in a streaming fashion. It uses an asynchronous context to receive and display the generated text in real-time as it is produced by the model.

Execution Steps
-------------------------
1. **Import Necessary Modules**: The code starts by importing the `asyncio` library for asynchronous programming and the `AsyncClient` class from the `g4f.client` module.
2. **Create an Asynchronous Client**: An instance of the `AsyncClient` class is created.
3. **Initiate a Chat Completion Request**: The `client.chat.completions.create()` method is called to initiate a chat completion request using the GPT-4 model (`model="gpt-4"`). The input message is provided as a list of dictionaries with the role and content (`messages=[{"role": "user", "content": "Say hello there!"}]`). The `stream=True` parameter enables streaming mode, which allows receiving the response text incrementally.
4. **Iterate Over Streaming Chunks**: The code enters a loop that iterates over each streaming chunk (`async for chunk in stream`). 
5. **Process Incoming Text**: For each chunk, it checks if there is a content delta (`chunk.choices and chunk.choices[0].delta.content`). If so, it retrieves the content (`content = chunk.choices[0].delta.content`), adds it to the accumulated text (`accumulated_text += content`), and prints it to the console (`print(content, end="", flush=True)`). This ensures that the text is printed as it arrives.
6. **Error Handling**: The code includes a `try...except` block to catch any potential errors during the streaming process. If an error occurs, it prints an error message.
7. **Final Output**: After the loop finishes or an error occurs, the final accumulated text is printed (`print("\n\nFinal accumulated text:", accumulated_text)`).

Usage Example
-------------------------

```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Tell me a joke."}],
        stream=True,
    )

    accumulated_text = ""
    try:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_text += content
                print(content, end="", flush=True)
    except Exception as e:
        print(f"\nError occurred: {e}")
    finally:
        print("\n\nFinal accumulated text:", accumulated_text)

asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".