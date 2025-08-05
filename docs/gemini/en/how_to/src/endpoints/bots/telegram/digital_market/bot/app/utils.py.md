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
This code block defines functions for handling payments through Robokassa, a popular payment gateway. The functions generate payment links, validate signatures, and process payment results.

Execution Steps
-------------------------
1. **`calculate_signature`:** Calculates a MD5 hash signature for the payment transaction using essential information like login, cost, invoice ID, and passwords. It includes additional parameters related to the user and product for verification.
2. **`generate_payment_link`:** Constructs a URL for the Robokassa payment page using parameters like cost, order number, description, user ID, user Telegram ID, product ID, and a test/live mode flag. 
3. **`parse_response`:** Parses the query string of a URL request into a dictionary of parameters.
4. **`check_signature_result`:** Verifies the signature received from Robokassa after a payment result is processed. It recalculates the signature using the provided parameters and compares it with the received signature.
5. **`result_payment`:** Handles the payment result received from Robokassa. It checks the signature, retrieves order details, and returns an "OK" confirmation if the payment is successful.
6. **`check_success_payment`:** Checks the successful payment result received from Robokassa. It verifies the signature and returns a success message if the payment is validated.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.app.utils import generate_payment_link, result_payment, check_success_payment

# Generate a payment link
payment_link = generate_payment_link(
    cost=10.00,
    number=12345,
    description="Digital Product",
    user_id=123,
    user_telegram_id=123456789,
    product_id=567
)

# Process a payment result (ResultURL)
result_data = result_payment(request="https://example.com/?OutSum=10.00&InvId=12345&SignatureValue=...") 
# result_data will be 'OK12345' if successful, 'bad sign' otherwise

# Process a successful payment (SuccessURL)
success_message = check_success_payment(request="https://example.com/?OutSum=10.00&InvId=12345&SignatureValue=...")
# success_message will be "Thank you for using our service" if successful, 'bad sign' otherwise
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".