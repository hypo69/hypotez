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
This code snippet generates a table of contents for a documentation file in Markdown format. The code identifies headings and creates links to those headings within the document.

Execution Steps
-------------------------
1. The code iterates through lines in the input string (which is likely the contents of the documentation file).
2. It identifies heading lines using the `re.findall` function to match lines starting with `##` (level 2 heading) or `###` (level 3 heading).
3. For each identified heading, the code extracts the heading text, cleans it up by removing leading and trailing spaces, and converts it to lowercase.
4. It creates a link to the heading using Markdown syntax.
5. The generated links are appended to a list.
6. Finally, the code joins the links into a single string, separated by newlines.

Usage Example
-------------------------

```python
from src.utils.string.readme import generate_toc

# Example documentation content
content = """
## Overview

This is a brief overview of the project.

### Features

The project includes several features:

- Feature 1
- Feature 2

## Usage

Here's how to use the project...
"""

# Generate the table of contents
toc = generate_toc(content)
print(toc)
```

Output:

```
## Overview
### Features
## Usage
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".