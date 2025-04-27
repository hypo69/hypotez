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
This code block handles the logic for successful payment in a Telegram bot.  It: 

    - Records the payment details to the database.
    - Retrieves the details of the purchased product.
    - Sends notifications to administrators about the purchase.
    - Sends confirmation and product information to the user.
    - Sends the purchased file, if any, to the user.
    - Handles refunding of "stars" if the payment type is "stars". 

Execution Steps
-------------------------
1. **Record the Purchase**: The code records the payment details to the database by creating a new purchase record.
2. **Retrieve Product Information**: The code retrieves the product information from the database based on the product ID. 
3. **Send Administrator Notifications**: The code sends notifications to all administrators about the successful purchase, including the product name, price, and user ID.
4. **Send User Confirmation**: The code sends a message to the user confirming the purchase and providing details about the product, such as the name, description, price, and whether or not it includes a file.
5. **Send Product File**: If the product includes a file, the code sends the file to the user.
6. **Refund Stars**: If the payment type is "stars," the code automatically refunds the stars to the user.


Usage Example
-------------------------

```python
    # Assuming you have a payment_data dictionary with payment details
    # and a session, bot object, currency, and user_tg_id
    await successful_payment_logic(session=session, payment_data=payment_data, currency=currency, user_tg_id=user_tg_id, bot=bot) 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".