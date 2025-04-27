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
The code defines custom exceptions specific to AliExpress API operations. These exceptions provide structured error handling mechanisms, allowing the application to gracefully handle various API-related issues.

Execution Steps
-------------------------
1. **Define a Base Exception Class (`AliexpressException`)**: This class serves as the base for all AliExpress API exceptions. It initializes the `reason` attribute, which stores a descriptive message about the error.
2. **Define Specific Exception Classes**:
    - **`InvalidArgumentException`**: Raised when the provided arguments are not valid.
    - **`ProductIdNotFoundException`**: Raised when the requested product ID is not found.
    - **`ApiRequestException`**: Raised when a request to the AliExpress API fails.
    - **`ApiRequestResponseException`**: Raised when the response received from the AliExpress API is invalid.
    - **`ProductsNotFoudException`**: Raised when no products are found based on the search criteria.
    - **`CategoriesNotFoudException`**: Raised when no categories are found based on the search criteria.
    - **`InvalidTrackingIdException`**: Raised when the provided tracking ID is not present or invalid.

Usage Example
-------------------------

```python
from src.suppliers.aliexpress.api.errors.exceptions import InvalidArgumentException

try:
    # Example API call with invalid arguments
    result = api_client.get_products(invalid_argument='value')
except InvalidArgumentException as e:
    print(f"Error: {e}")
    # Handle the error, e.g., log it or display an error message to the user
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".