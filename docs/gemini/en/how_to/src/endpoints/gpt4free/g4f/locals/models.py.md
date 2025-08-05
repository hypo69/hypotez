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
This code block defines functions to manage a collection of GPT4Free models. It handles loading models from a remote source, extracting model names from filenames, formatting model data, reading model data from a local JSON file, saving model data to a JSON file, and retrieving the models from a local directory.

Execution Steps
-------------------------
1. **`load_models()`**:
   - Fetches model data from a remote URL ("https://gpt4all.io/models/models3.json").
   - Checks the response status code for errors.
   - Calls `format_models()` to structure the model data.
   - Returns the formatted model data as a dictionary.
2. **`get_model_name()`**:
   - Extracts the model name from a filename.
   - Removes common suffixes (e.g., "-v1_5", "-v1", "-q4_0") from the filename.
   - Returns the extracted model name.
3. **`format_models()`**:
   - Iterates through a list of models.
   - Extracts model name, path, RAM requirement, prompt template, and system prompt for each model.
   - Organizes this information into a dictionary keyed by model name.
   - Returns the resulting model dictionary.
4. **`read_models()`**:
   - Reads model data from a local JSON file.
   - Returns the loaded model data.
5. **`save_models()`**:
   - Saves model data to a local JSON file.
   - Indents the output for better readability.
6. **`get_model_dir()`**:
   - Determines the path to the "models" directory within the project.
   - Creates the directory if it doesn't exist.
   - Returns the path to the "models" directory.
7. **`get_models()`**:
   - Checks if a "models.json" file exists in the "models" directory.
   - If it exists, loads the model data from the file.
   - If it doesn't exist, calls `load_models()` to fetch models, saves them to "models.json", and returns the fetched models.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.locals.models import get_models

models = get_models()

# Access a specific model
model_data = models["gpt4all-lora-13b"]

# Print the model path
print(model_data["path"]) 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".