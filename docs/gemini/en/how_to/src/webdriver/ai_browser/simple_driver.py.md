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
The `SimpleDriver` class is a driver for running tasks using a LangChain agent and a language model. It configures the models (Gemini, OpenAI), sets API keys, and executes the task using the specified tools (web search, browser). The driver also provides functionality for running the task to completion (`run_task`) and streaming the task execution (`stream_task`).

Execution Steps
-------------------------
1. **Initialize the Driver**: Create an instance of the `SimpleDriver` class, providing the necessary API keys and model names.
2. **Define the Task**: The task is a string that describes the action to be performed.
3. **Initialize the Agent**: Create an instance of the `Agent` class, passing in the task, the language model, and any additional parameters.
4. **Execute the Task**: Use the `run()` method of the agent to execute the task and receive the result.
5. **Process the Result**: Handle the returned result, potentially converting it to a dictionary or other data structure.

Usage Example
------------------------

```python
    # Initialize the driver with a Gemini model
    driver = SimpleDriver(gemini_model_name='gemini-2.5-flash-preview-04-17')

    # Load the task from a Markdown file
    task = Path(__root__ / 'src' / 'webdriver' / 'ai_browser' / 'instructions' / 'get_news_from_nocamel_site.md').read_text(encoding='utf-8')

    # Execute the task asynchronously
    result = asyncio.run(driver.simple_process_task_async(task))

    # Print the result
    print(f"Result of task execution: {result}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".