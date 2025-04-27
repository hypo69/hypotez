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
The `TinyTool` class represents a tool that can be used by agents within a simulation. It provides a framework for defining and executing tool actions, with features for managing ownership, real-world side effects, and enriching/exporting results.

Execution Steps
-------------------------
1. **Initialization**: A `TinyTool` object is created with a name, description, optional owner, and flags indicating whether it has real-world side effects and if it uses an exporter or enricher.
2. **Action Processing**: The `_process_action` method, which must be implemented by subclasses, defines the specific logic for handling actions.
3. **Safety Checks**: Before executing an action, the `process_action` method performs safety checks:
    - **Real-World Side Effects**: If the tool has real-world side effects, a warning is logged.
    - **Ownership**: If the tool has an owner, it ensures that the agent attempting to use the tool is the owner.
4. **Action Execution**: The `_process_action` method is called to handle the action, and the result is returned.

Usage Example
-------------------------

```python
from tinytroupe.tools import TinyTool
from tinytroupe.agents import Agent

class MyTool(TinyTool):
    def __init__(self, name, description):
        super().__init__(name, description, real_world_side_effects=True)

    def _process_action(self, agent, action: dict) -> bool:
        # Perform tool-specific action based on 'action'
        print(f"Tool '{self.name}' executing action: {action}")
        return True

# Create an agent and a tool
my_agent = Agent("Agent1")
my_tool = MyTool("My Tool", "A tool for demonstration purposes")

# Execute an action using the tool
action = {"task": "print_message", "message": "Hello from the tool!"}
result = my_tool.process_action(my_agent, action)
print(f"Action result: {result}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".