**Instructions for Generating Code Documentation**

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code defines a `ResultsExtractor` class designed to extract results from interactions between agents (represented by `TinyPerson` objects) and the environment (represented by `TinyWorld` objects) in a game-like setting. The class leverages OpenAI's language model to analyze interaction histories and generate structured results based on provided objectives, situations, and optional field hints. 

Execution Steps
-------------------------
1. **Initialization:**
   - Creates a `ResultsExtractor` object, optionally accepting parameters for default settings, including the extraction objective, the situation, desired fields, and field hints.
   - Stores default values and initializes empty dictionaries to cache extracted results for agents and worlds.

2. **Extraction from Agents:**
   - The `extract_results_from_agents` method iterates through a list of `TinyPerson` objects, calling `extract_results_from_agent` for each.
   - `extract_results_from_agent` utilizes an extraction prompt template, interaction history, and provided parameters to formulate a prompt for OpenAI.
   - The prompt includes the extraction objective, situation, agent's name, and the formatted interaction history of the agent.
   - It sends the prompt to OpenAI and extracts JSON-formatted results from the response, caching the results for the agent.

3. **Extraction from World:**
   - The `extract_results_from_world` method performs similar extraction as `extract_results_from_agent`, but with a focus on the entire `TinyWorld`'s interaction history.
   - The prompt for OpenAI considers all agents in the environment and their interaction histories.
   - It then retrieves and caches the JSON results.

4. **Saving Results:**
   - The `save_as_json` method writes the cached extraction results for agents and worlds to a specified JSON file.

Usage Example
-------------------------

```python
from tinytroupe.extraction.results_extractor import ResultsExtractor

# Create an instance of ResultsExtractor
extractor = ResultsExtractor(
    extraction_objective="Summarize the main points of the interaction between the agents.",
    fields=["Action", "Outcome"]  # Define fields to extract
)

# Sample agents and world
agents = [TinyPerson(name="Agent A"), TinyPerson(name="Agent B")]
world = TinyWorld(name="My World")

# Extract results from agents
results = extractor.extract_results_from_agents(agents, situation="They are playing a game.")
print(f"Agent results: {results}")  # Output results for each agent

# Extract results from the world
world_result = extractor.extract_results_from_world(world, extraction_objective="Describe the overall progress of the world.")
print(f"World result: {world_result}")

# Save results to JSON
extractor.save_as_json("extraction_results.json")
```