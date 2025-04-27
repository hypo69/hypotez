**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the PrestaCustomer Class
=========================================================================================

Description
-------------------------
The `PrestaCustomer` class provides methods to interact with customer data in a PrestaShop store. It uses the PrestaShop API to perform actions like creating, updating, and deleting customer records.

Execution Steps
-------------------------
1. **Initialize the PrestaCustomer class**: The class requires either `credentials` (a dictionary or SimpleNamespace object containing `api_domain` and `api_key`) or `api_domain` and `api_key` as individual parameters.
2. **Use the class methods**: The class provides the following methods:
    - `add_customer_PrestaShop(customer_name: str, customer_email: str)`: Creates a new customer in PrestaShop.
    - `delete_customer_PrestaShop(customer_id: int)`: Deletes a customer from PrestaShop.
    - `update_customer_PrestaShop(customer_id: int, new_name: str)`: Updates a customer's name in PrestaShop.
    - `get_customer_details_PrestaShop(customer_id: int)`: Retrieves details of a customer from PrestaShop.

Usage Example
-------------------------

```python
    from src.endpoints.prestashop.customer import PrestaCustomer

    # Initialize PrestaCustomer with API credentials
    prestacustomer = PrestaCustomer(API_DOMAIN="your-api-domain.com", API_KEY="your-api-key")

    # Create a new customer
    prestacustomer.add_customer_PrestaShop(customer_name='John Doe', customer_email='johndoe@example.com')

    # Delete a customer
    prestacustomer.delete_customer_PrestaShop(3)

    # Update a customer's name
    prestacustomer.update_customer_PrestaShop(4, 'Updated Customer Name')

    # Get customer details
    customer_details = prestacustomer.get_customer_details_PrestaShop(5)
    print(customer_details)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".