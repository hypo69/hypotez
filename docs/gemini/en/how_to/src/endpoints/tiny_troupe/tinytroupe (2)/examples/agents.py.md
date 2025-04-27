**Instructions for Generating Code Documentation**

How to Use These Code Blocks
=========================================================================================

Description
-------------------------
This code snippet demonstrates the creation of various TinyPerson agents using the `tinytroupe` library. It provides examples of defining different agent attributes like age, nationality, occupation, behaviors, personality, preferences, skills, and relationships. These examples can be used directly or modified to create your own unique agents. 

Execution Steps
-------------------------
1. **Import necessary modules**: Import the `TinyPerson` class and the `load_example_agent_specification` function from the `tinytroupe` and `loaders` modules respectively.
2. **Create an agent**: Define a function to create a specific agent.
3. **Define agent attributes**: Within the function, create a `TinyPerson` object. Use the `define` method to set the agent's attributes like `age`, `nationality`, `occupation`, `behaviors`, `personality`, `preferences`, `skills`, and `relationships`.
4. **Load agent specification**: Alternatively, use the `load_specification` method of the `TinyPerson` class to load an agent's attributes from a pre-defined specification file.

Usage Example
-------------------------

```python
# Example 1: Create Oscar, the architect using a pre-defined specification file
oscar = create_oscar_the_architect()

# Example 2: Create Lisa, the Data Scientist using a purely programmatic approach
lisa = create_lisa_the_data_scientist_2()
```