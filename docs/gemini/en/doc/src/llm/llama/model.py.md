# Module src.ai.llama.model

## Overview

This module implements a simple example of loading and using the `Meta-Llama-3.1-8B-Instruct-GGUF` model using the `llama-cpp-python` library. 

## Details

The code demonstrates loading the `Meta-Llama-3.1-8B-Instruct-GGUF` model from Hugging Face and generating text based on a given prompt.  

## Classes

### `Llama`

**Description:** This class represents the `llama-cpp` model instance, providing methods to generate text, interact with the model, and manage its configuration.  

**Methods:**

- **`from_pretrained(repo_id: str, filename: str)`**: This method loads the pre-trained `llama-cpp` model from Hugging Face.
- **`__call__(prompt: str, max_tokens: int = 512, echo: bool = True)`**: This method takes a prompt as input and generates text using the model, with options to specify the maximum number of tokens to generate and whether to echo the prompt in the output.

**Parameters:**
- `repo_id` (str): The Hugging Face repository ID for the model.
- `filename` (str): The filename of the model file.
- `prompt` (str): The input prompt for the model to generate text from.
- `max_tokens` (int, optional): The maximum number of tokens to generate. Defaults to 512.
- `echo` (bool, optional): Whether to echo the prompt in the output. Defaults to True.

**Example:**

```python
from llama_cpp import Llama

# Load the Llama model
llm = Llama.from_pretrained(
    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    filename="Meta-Llama-3.1-8B-Instruct-IQ4_XS.gguf",
)

# Generate text
output = llm(
    "Once upon a time,",
    max_tokens=512,
    echo=True
)
print(output)
```

**Inner Functions:**
- There are no inner functions in this example.

**How the Function Works:**
- The `Llama` class relies on the `llama-cpp` library to load and interact with the Llama model.
- The `from_pretrained` method retrieves the model from the Hugging Face repository and loads it into memory. 
- The `__call__` method takes a prompt, passes it to the Llama model, and returns the generated text.

**Examples:**
- The example code demonstrates how to load the Llama model, generate text, and print the result.