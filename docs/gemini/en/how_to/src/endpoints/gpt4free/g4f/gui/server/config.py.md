**Instructions for Generating Code Documentation**

1. **Analyze the Code**: This code snippet defines a dictionary called `special_instructions`. This dictionary stores instructions for different AI personas (e.g., "gpt-dude-1.0", "gpt-dan-1.0") that are used to alter the behavior and responses of a language model like ChatGPT.

2. **Create a Step-by-Step Guide**:

    - **Description**: This code snippet defines a dictionary called `special_instructions` which contains instructions for different AI personas. The instructions are in the form of a list of messages where each message has a role (either "user" or "assistant") and a content. The user messages define the instructions for the AI persona while the assistant messages confirm the understanding of these instructions.

    - **Execution Steps**: 
        1. The code creates a dictionary called `special_instructions`.
        2. It defines entries for different AI personas like "gpt-dude-1.0", "gpt-dan-1.0", "gpt-dan-2.0", "gpt-math-1.0", "gpt-dev-2.0", and "gpt-evil-1.0".
        3. For each persona, it creates a list of messages (user and assistant).
        4. The user messages provide detailed instructions to the AI persona, outlining its specific behavior, abilities, and restrictions.
        5. The assistant messages confirm that the persona understands the instructions.

    - **Usage Example**:

    ```python
    from hypotez.src.endpoints.gpt4free.g4f.gui.server.config import special_instructions

    # Accessing instructions for a specific persona
    dude_instructions = special_instructions['gpt-dude-1.0']

    # Printing the instructions for "gpt-dude-1.0"
    print(dude_instructions) 

    ```

3. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".