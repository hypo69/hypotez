# Module for working with tools
=================================================

The module contains the :class:`ToolSupportProvider` class, which is used for interacting with various AI models (e.g., Google Gemini and OpenAI) and performing code processing tasks.

## Details
The module defines the `ToolSupportProvider` class. It utilizes the `AsyncGeneratorProvider` to access the asynchronous data generation functionality of the `hypotez` framework.
The `ToolSupportProvider` is responsible for handling interactions with external tools, such as function calls.

## Classes

### `ToolSupportProvider`

**Description**: The `ToolSupportProvider` class provides the ability to use external tools within the conversational context of the `hypotez` project. It allows developers to invoke functions and receive results, integrating external functionality directly into the AI-powered dialogue.

**Inherits**:
 - `AsyncGeneratorProvider`

**Attributes**:

- `working`: `bool`, a flag that indicates whether the provider is actively working or not.

**Methods**:

- `create_async_generator()`: Asynchronously creates a generator for handling tool interactions and processing messages within the AI model.

## Functions

### `create_async_generator`

**Purpose**: The `create_async_generator` method is responsible for setting up the asynchronous generation process for handling tool interactions. It retrieves the necessary AI model and provider, sets up the request parameters, and prepares the asynchronous generator for streaming responses.

**Parameters**:

- `model (str)`: The name of the AI model to use for processing messages.
- `messages (Messages)`: A list of messages representing the conversation history, including user input and previous responses.
- `stream (bool)`: Indicates whether to stream the response in chunks or receive it as a whole. Defaults to `True`, which enables streaming.
- `media (MediaListType)`: A list of media objects, such as images or audio files, that can be used by the AI model during processing. Defaults to `None`.
- `tools (list[str])`: A list of tools available for the AI model to use. Currently, only one tool is supported at a time.
- `response_format (dict)`: The desired format for the response. Defaults to `{"type": "json"}`.
- `**kwargs`: Additional keyword arguments that can be passed to the AI model.

**Returns**:

- `AsyncResult`: An asynchronous generator that yields chunks of the response, usage information, and completion status.

**Raises Exceptions**:

- `ValueError`: If more than one tool is provided in the `tools` parameter.

**How the Function Works**:
 - The function starts by initializing the `provider` and `model` variables.
 - It then checks if multiple tools are provided. If so, it raises a `ValueError` as only one tool is currently supported.
 - The function then prepares a message for the AI model, informing it of the tool's capabilities and the desired response format.
 - An asynchronous generator is created using `provider.get_async_create_function()` and is utilized to process the messages, stream responses, and handle tool interactions.
 - The function yields chunks of the response, usage information, and completion status to the asynchronous generator.

**Examples**:
```python
# Example 1: Using a single tool with JSON response format
model = "gemini:1.0"
tools = ["translate"]
messages = [
    {"role": "user", "content": "Translate this text into Spanish: Hello world!"}
]
async_generator = await ToolSupportProvider.create_async_generator(model=model, messages=messages, tools=tools)
# Process the async_generator

# Example 2: Using no tools with default response format
model = "gemini:1.0"
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]
async_generator = await ToolSupportProvider.create_async_generator(model=model, messages=messages)
# Process the async_generator
```