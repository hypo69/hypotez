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
This code block demonstrates how to use the `g4f.ChatCompletion` class to interact with a GPT-like chatbot. It includes two examples: one for synchronous chat completion and another for asynchronous chat completion.

Execution Steps
-------------------------
1. **Import necessary libraries:** The code imports modules like `sys`, `pathlib`, `g4f`, and `asyncio`. 
2. **Initialize a chat completion object:** An instance of the `g4f.ChatCompletion` class is created.
3. **Synchronous chat completion:** 
    - The code calls the `create()` method with the `model`, `messages`, and `stream` parameters to get a response from the chatbot.
    - The `messages` parameter specifies the user's prompt, in this case, "write a poem about a tree."
    - The `stream` parameter enables streaming responses for interactive chat interactions.
4. **Asynchronous chat completion:** 
    - The `create_async()` method is used to perform chat completion asynchronously.
    - The `run_async()` function wraps the asynchronous call in an `asyncio.run()` block.
5. **Print responses:** The responses from the chatbot are printed to the console.

Usage Example
-------------------------

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f, asyncio

# Synchronous Chat Completion
print("create:", end=" ", flush=True)
for response in g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True
):
    print(response, end="", flush=True)
print()

# Asynchronous Chat Completion
async def run_async():
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        messages=[{"role": "user", "content": "hello!"}],
    )
    print("create_async:", response)

asyncio.run(run_async())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".