**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `ResultsExtractor` Class
=========================================================================================

Description
-------------------------
The `ResultsExtractor` class is designed to extract insights from TinyTroupe simulations. It utilizes OpenAI's language model to analyze interaction histories of agents and worlds, distilling key points into structured data.

Execution Steps
-------------------------
1. **Initialize the Extractor**: Create an instance of the `ResultsExtractor` class.
2. **Define Extraction Objective**: Specify the desired outcome of the extraction process using the `extraction_objective` parameter.
3. **Specify the Situation**: Provide context for the extraction by setting the `situation` parameter. 
4. **Choose Fields**: Optionally define specific fields you want to extract using the `fields` parameter.
5. **Trigger Extraction**: Call `extract_results_from_agent` or `extract_results_from_world` depending on whether you want to analyze an agent or a world.
6. **Save Results (Optional)**: Use the `save_as_json` method to save the extracted results in a JSON file.

Usage Example
-------------------------

```python
from tinytroupe.extraction import ResultsExtractor

# Initialize the ResultsExtractor
extractor = ResultsExtractor()

# Define extraction objective and situation
extraction_objective = "Summarize the key events in the agent's interaction history."
situation = "The agent is interacting with a chatbot to learn about the history of art."

# Extract results from an agent
agent = TinyPersonFactory.create_new_tiny_person("Alice") 
# Simulate interactions for the agent 
# ...
results = extractor.extract_results_from_agent(agent, extraction_objective, situation)

# Print the extracted results
print(results)

# Save the results to a JSON file
extractor.save_as_json("extraction_results.json")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".