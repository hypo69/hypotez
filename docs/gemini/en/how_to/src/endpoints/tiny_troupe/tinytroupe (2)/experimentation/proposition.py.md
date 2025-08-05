**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `Proposition` Class
=========================================================================================

Description
-------------------------
The `Proposition` class represents a textual claim about a target, which can be a `TinyWorld`, a `TinyPerson` or a list of either. It uses an LLM to evaluate the truth value of the claim based on a provided context.

Execution Steps
-------------------------
1. **Initialize the `Proposition` Object**: The constructor takes the target object(s), the claim, and optionally the number of interactions to consider (first and last) as arguments. 
2. **Retrieve the Context**: The `check` method gathers the simulation trajectory for the specified target(s), considering the specified interaction range. 
3. **Formulate the LLM Request**: The code constructs an `LLMRequest` object with the system prompt, user prompt (which includes the proposition, context, and additional context), and output type (boolean). 
4. **Evaluate the Proposition**: The `LLMRequest` object is called, which sends the prompt to the LLM and receives the response. The response is analyzed for its truth value, justification, and confidence score. 
5. **Store the Results**: The evaluated truth value, justification, confidence score, and raw LLM response are stored as attributes of the `Proposition` object. 

Usage Example
-------------------------
```python
    from tinytroupe.agent import TinyPerson
    from tinytroupe.environment import TinyWorld
    from tinytroupe.experimentation.proposition import Proposition

    # Create a TinyWorld and a TinyPerson
    world = TinyWorld(name="MyWorld")
    person = TinyPerson(name="Alice", world=world)

    # Define a proposition
    claim = "Alice is happy."
    proposition = Proposition(person, claim)

    # Evaluate the proposition
    result = proposition.check()

    # Print the results
    print(f"Proposition: {proposition.claim}")
    print(f"Value: {proposition.value}")
    print(f"Justification: {proposition.justification}")
    print(f"Confidence: {proposition.confidence}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".