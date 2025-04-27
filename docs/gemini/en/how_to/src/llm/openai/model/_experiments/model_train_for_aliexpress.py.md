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
The code snippet reads a list of product titles from a specified directory, processes them using OpenAI and Gemini models, and generates responses for each set of titles.

Execution Steps
-------------------------
1. It retrieves filenames of "product_titles.txt" files from a directory named "campaigns" located within the "aliexpress" folder.
2. It reads the system instruction from a specified file path.
3. It initializes OpenAI and Gemini models with the system instruction.
4. It iterates through each product title file:
    - Reads the product titles from the file.
    - Sends the product titles to the OpenAI model and retrieves the response.
    - Sends the product titles to the Gemini model and retrieves the response.
5. The code continues with further processing (denoted by "...") after obtaining responses from both models. 

Usage Example
-------------------------

```python
from src import gs
from src.llm import OpenAIModel, GoogleGenerativeAi
from src.utils.file import recursively_get_filenames, read_text_file
from src.utils.printer import pprint

# Define file paths
product_titles_files = recursively_get_filenames(gs.path.google_drive / 'aliexpress' / 'campaigns', 'product_titles.txt')
system_instruction_path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'

# Read system instruction
system_instruction = read_text_file(system_instruction_path)

# Initialize OpenAI and Gemini models
openai = OpenAIModel(system_instruction=system_instruction)
gemini = GoogleGenerativeAi(system_instruction=system_instruction)

# Iterate through product title files
for file in product_titles_files:
    product_titles = read_text_file(file)
    response_openai = openai.ask(product_titles)
    response_gemini = gemini.ask(product_titles)
    # Process responses (denoted by "...") 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".