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
This code snippet provides instructions for a language model to generate multiple, more specific contexts for person descriptions based on a broader, more general context.  

Execution Steps
-------------------------
1. The model receives a broad context that includes details about the type of person to generate, such as demographics, physical characteristics, behaviors, beliefs, and other relevant information.
2. The model processes the broad context and creates multiple, more specific contexts. Each specific context is designed to be a base for generating a detailed person description.
3. The model formats its response as an array in JSON format, where each element represents a specific context that can be used to generate a person description.

Usage Example
-------------------------

```python
    # Example of how to use the code snippet in the project
    broad_context = "Please, generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"
    # Call the language model with the broad context
    generated_contexts = language_model.generate_person_contexts(broad_context)
    # The language model returns an array of specific contexts
    print(generated_contexts)
    # Output:
    # ["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".