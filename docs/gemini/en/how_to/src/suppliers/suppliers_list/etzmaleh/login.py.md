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
This code snippet defines a `login` function that attempts to log in to the Etz Maleh supplier website using a WebDriver. 

Execution Steps
-------------------------
1. The function takes a `Supplier` object (denoted as `s`) as input.
2. The code logs an informational message indicating that the login process is starting.
3. The function returns `True` to indicate a successful login, without actually performing any login actions. 

Usage Example
-------------------------

```python
from src.suppliers.etzmaleh.login import login
from src.suppliers.etzmaleh import Supplier

# Create a Supplier object (replace with actual supplier details)
etz_maleh_supplier = Supplier(
    user='your_username',
    password='your_password',
    # ...other supplier details
)

# Attempt to log in
logged_in = login(etz_maleh_supplier)

if logged_in:
    print('Login successful!')
else:
    print('Login failed.')

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".