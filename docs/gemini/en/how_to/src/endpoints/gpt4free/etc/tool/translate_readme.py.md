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
This code block translates a markdown document to a specified language using the GPT4Free API. It reads the document, splits it into sections based on `##` headers, translates each section individually, and then writes the translated document to a new file. 

Execution Steps
-------------------------
1. **Import necessary libraries**: This includes modules for interacting with the file system, asyncio for asynchronous operations, and the GPT4Free API.
2. **Configure GPT4Free**: Set the provider to OpenaiChat, define the target language, and construct a translation prompt.
3. **Define helper functions**:
    - `read_text`: Extracts the content between ````` markers in a given text, representing code blocks.
    - `translate`: Translates a text snippet using the GPT4Free API, preserving code blocks and `[!Note]` markers.
    - `translate_part`: Translates a section of the document, handling blocklisted sections and applying translations to allowed headlines.
4. **Translate the entire README**:
    - Split the README into sections using `##` headers.
    - Translate each section asynchronously using `translate_part`.
    - Combine the translated sections and write them to a new file named `README-{iso}.md`.

Usage Example
-------------------------

```python
import sys
from pathlib import Path
import asyncio

sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f
g4f.debug.logging = True
from g4f.debug import access_token
provider = g4f.Provider.OpenaiChat

iso = "GE"
language = "german"
translate_prompt = f"""
Translate this markdown document to {language}.
Don't translate or change inline code examples.
```md
"""
keep_note = "Keep this: [!Note] as [!Note].\\n"
blocklist = [
    '## ©️ Copyright',
    '## 🚀 Providers and Models',
    '## 🔗 Related GPT4Free Projects'
]
allowlist = [
    "### Other",
    "### Models"
]

# ... rest of the code ... 

with open("README.md", "r") as fp:
    readme = fp.read()

print("Translate readme...")
readme = asyncio.run(translate_readme(readme))

file = f"README-{iso}.md"
with open(file, "w") as fp:
    fp.write(readme)
print(f'"{file}" saved')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".