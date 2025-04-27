**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `ResultsReducer` Class
=========================================================================================

Description
-------------------------
The `ResultsReducer` class processes and extracts relevant information from a `TinyPerson`'s episodic memory. It applies user-defined reduction rules based on the type of event (stimulus or action) in the memory. This allows for filtering and extracting key data points for analysis.

Execution Steps
-------------------------
1. **Initialization**: The `ResultsReducer` is initialized with an empty `results` dictionary and an empty `rules` dictionary.
2. **Adding Reduction Rules**: The `add_reduction_rule` method allows adding custom rules to the `rules` dictionary. These rules are functions that define how to extract specific information based on event types.
3. **Reducing Agent Memory**: The `reduce_agent` method iterates through the `TinyPerson`'s episodic memory. It identifies events categorized as "user" or "assistant" and processes them according to the defined rules. 
    - **User Role**: It extracts information about stimuli, including type, content, source, and timestamp.
    - **Assistant Role**: It extracts information about actions, including type, content, target, and timestamp.
4. **Converting to DataFrame**: The `reduce_agent_to_dataframe` method converts the extracted information into a Pandas DataFrame.

Usage Example
-------------------------

```python
from tinytroupe.extraction import ResultsReducer
from tinytroupe.agent import TinyPerson

# Initialize the ResultsReducer
reducer = ResultsReducer()

# Define a reduction rule for a specific stimulus type
def extract_stimulus_content(focus_agent: TinyPerson, source_agent: TinyPerson, target_agent: TinyPerson, kind: str, event: str, content: str, timestamp: float) -> dict:
    """Extracts stimulus content."""
    return {"stimulus_type": event, "content": content, "timestamp": timestamp}

# Add the rule to the reducer
reducer.add_reduction_rule("text_stimulus", extract_stimulus_content)

# Create a TinyPerson instance 
agent = TinyPerson("Alice")

# Reduce the agent's memory and convert to a DataFrame
df = reducer.reduce_agent_to_dataframe(agent, column_names=["stimulus_type", "content", "timestamp"])

# Print the DataFrame
print(df)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".