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
This code snippet demonstrates how to use the `gpt4free` library to make asynchronous text completion requests using the GPT-4 model. It sets up an asynchronous client, creates a chat completion request with a system message and a user query, and then prints the generated response.

Execution Steps
-------------------------
1. **Import necessary modules**: Import `asyncio` for asynchronous programming and `AsyncClient` from the `g4f.client` module to establish an asynchronous client connection to the GPT-4Free API.
2. **Define an asynchronous function `main()`**: This function contains the main logic for sending the chat completion request and processing the response.
3. **Create an asynchronous client**: Instantiate an `AsyncClient` object to interact with the GPT-4Free API.
4. **Create a chat completion request**: Use the `client.chat.completions.create()` method to create a chat completion request. This method takes the following arguments:
    - `model`: Specifies the GPT model to use, in this case, "gpt-4o".
    - `messages`: A list of chat messages to be sent to the model. This example includes a system message defining the assistant's role and a user message containing the query.
5. **Send the request and get the response**: Use the `await` keyword to send the request asynchronously and wait for the response. 
6. **Print the generated response**: Access the generated response text from the `response.choices[0].message.content` attribute and print it to the console.
7. **Run the asynchronous function**: Call `asyncio.run(main())` to execute the `main()` function asynchronously.

Usage Example
-------------------------

```python
import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the meaning of life?"}
        ]
    )

    print(response.choices[0].message.content)

asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".