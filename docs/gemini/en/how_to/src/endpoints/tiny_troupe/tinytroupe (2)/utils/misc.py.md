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
This code block defines various utility functions for working with TinyPerson and TinyWorld objects. The functions include:

- **`name_or_empty(named_entity: AgentOrWorld)`:** Retrieves the name of the specified agent or environment, returning an empty string if the agent is None.
- **`custom_hash(obj)`:** Generates a deterministic hash for the provided object. It first converts the object to a string before hashing.
- **`fresh_id()`:** Generates a unique ID for a new object by incrementing a global counter.
- **`reset_fresh_id()`:** Resets the unique ID counter, primarily used for testing purposes.

Execution Steps
-------------------------
1. **`name_or_empty`:**
   - Checks if the `named_entity` is None.
   - If it is, returns an empty string.
   - Otherwise, returns the `name` attribute of the `named_entity`.

2. **`custom_hash`:**
   - Converts the `obj` to a string using `str(obj)`.
   - Encodes the string using `encode()`.
   - Calculates the SHA256 hash of the encoded string using `hashlib.sha256()`.
   - Returns the hash in hexadecimal format using `hexdigest()`.

3. **`fresh_id`:**
   - Increments the global counter `_fresh_id_counter`.
   - Returns the incremented counter value.

4. **`reset_fresh_id`:**
   - Sets the global counter `_fresh_id_counter` back to 0.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.tiny_troupe.tinytroupe (2).utils.misc import name_or_empty, custom_hash, fresh_id, reset_fresh_id

# Example usage:
tiny_person = TinyPerson(name="Alice")
tiny_world = TinyWorld(name="Wonderland")

# Get the name of the TinyPerson
name = name_or_empty(tiny_person)
print(f"The TinyPerson's name is: {name}")

# Generate a unique hash for the TinyWorld
hash_value = custom_hash(tiny_world)
print(f"The TinyWorld's hash is: {hash_value}")

# Generate a fresh ID for a new object
new_id = fresh_id()
print(f"New object ID: {new_id}")

# Reset the ID counter
reset_fresh_id()
new_id = fresh_id()
print(f"New object ID after reset: {new_id}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".