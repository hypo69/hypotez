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
This code defines a custom event handler class (`EventHandler`) that overrides the default behavior of the OpenAI Assistant to provide customized output formatting. This class handles various events triggered during the OpenAI Assistant's response stream and prints them to the console in a more readable format.

Execution Steps
-------------------------
1. **Create `EventHandler` class**:
   - The `EventHandler` class inherits from `AssistantEventHandler`, which provides the base class for handling events.
2. **Override Event Handlers**:
   - The class overrides several methods like `on_text_created`, `on_text_delta`, `on_tool_call_created`, and `on_tool_call_delta` to customize the output formatting for different events.
3. **Implement Event Handling**:
   - Each overridden method defines the specific actions to be taken when the corresponding event is triggered. For example, the `on_text_created` method prints the prefix "assistant >" before the assistant's response. 
4. **Handle Text Events**:
   - The `on_text_created` and `on_text_delta` methods handle text responses from the assistant.
5. **Handle Tool Call Events**:
   - The `on_tool_call_created` and `on_tool_call_delta` methods handle events related to tool calls, like code interpreter execution. They print relevant information about the tool calls and their outputs.

Usage Example
-------------------------

```python
from openai import OpenAI
from src.ai.openai.model.event_handler import EventHandler

# Initialize OpenAI client
openai = OpenAI()

# Create a new assistant
assistant = openai.beta.assistants.create(
    name="My Assistant",
    model="gpt-4-1106-preview",
    instructions="You are a helpful and informative AI assistant.",
)

# Define the thread where the assistant will be used
thread = openai.beta.threads.create()

# Run the assistant in the thread with the custom event handler
run = openai.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Hello, world!",
    tools=[
        {
            "type": "code_interpreter",
        },
    ],
    event_handler=EventHandler(),  # Use the custom EventHandler
)

# Stream the response
run.stream() 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".