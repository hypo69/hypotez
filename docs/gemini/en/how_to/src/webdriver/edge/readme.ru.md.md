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
This code block imports the `Edge` class from the `src.webdriver.edge` module and creates an instance of the Edge WebDriver.

Execution Steps
-------------------------
1. Imports the `Edge` class from the `src.webdriver.edge` module.
2. Creates an instance of the `Edge` class, setting the `user_agent` and `options` parameters.
3. Opens the specified website using the `get` method.
4. Closes the browser using the `quit` method.

Usage Example
-------------------------

```python
from src.webdriver.edge import Edge

# Initialize Edge WebDriver with user-agent and custom options
browser = Edge(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", options=["--headless", "--disable-gpu"])

# Open a website
browser.get("https://www.example.com")

# Close the browser
browser.quit()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".