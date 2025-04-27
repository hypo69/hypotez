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
This code snippet sets up an asynchronous workflow to test different GPT-4Free providers. It creates a separate task for each working provider, executing the `create_async` function to send a message and log the execution time. Finally, it gathers the results from all tasks and prints the total execution time.

Execution Steps
-------------------------
1. **Import Necessary Modules**: Import required modules for asynchronous programming, path handling, and the GPT-4Free library.
2. **Configure System Path**: Add project directories to the system path for importing modules from different locations.
3. **Define `create_async` Function**: This function sends a test message to a specified GPT-4Free provider using `log_time_async` to measure the execution time.
4. **Define `run_async` Function**: This function creates a list of asynchronous tasks, each calling the `create_async` function for a working provider, and executes them using `asyncio.gather`.
5. **Execute `run_async` and Log Time**: Run the asynchronous task using `asyncio.run` and log the total execution time with `log_time_async`.


Usage Example
-------------------------

```python
import sys
from pathlib import Path
import asyncio

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f
from testing._providers import get_providers
from testing.log_time import log_time_async

async def create_async(provider):
    try:
        response = await log_time_async(
            provider.create_async,
            model=g4f.models.default.name,
            messages=[{"role": "user", "content": "Hello, are you GPT 3.5?"}]
        )
        print(f"{provider.__name__}:", response)
    except Exception as e:
        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")

async def run_async():
  responses: list = [
      create_async(provider)
      for provider in get_providers()
      if provider.working
  ]
  await asyncio.gather(*responses)

print("Total:", asyncio.run(log_time_async(run_async)))
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".