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
This code block implements the catalog routing logic for a Telegram bot, allowing users to browse product categories, view product details, and initiate payments for selected items.

Execution Steps
-------------------------
1. **Router Initialization**: The `catalog_router` is initialized using the `Router` class from the `aiogram` library. This router will handle all interactions related to the bot's catalog functionality.
2. **Catalog Page Handler**: The `page_catalog` function is triggered when the user selects the "catalog" option in the bot's menu. It retrieves the list of product categories from the database using the `CategoryDao` and displays them to the user.
3. **Category Products Handler**: The `page_catalog_products` function is triggered when the user selects a specific category. It retrieves the products within that category using the `ProductDao` and presents them to the user.
4. **Buy Button Handler**: The `process_about` function is triggered when the user selects the "buy" button for a product. Based on the chosen payment method (Yukassa, Stars, or Robocassa), it redirects the user to the appropriate payment process.
5. **Yukassa Invoice Handler**: The `send_yukassa_invoice` function sends an invoice using the Yukassa payment gateway, allowing the user to complete the purchase via the Telegram bot.
6. **Robocassa Invoice Handler**: The `send_robocassa_invoice` function generates a payment link using the Robocassa gateway and displays it to the user for completing the purchase.
7. **Stars Invoice Handler**: The `send_stars_invoice` function handles payments using an internal "Stars" currency within the bot, allowing the user to purchase with accumulated Stars.
8. **Pre-Checkout Query Handler**: The `pre_checkout_query` function is triggered when the user confirms the payment details. It sends a response to the Telegram platform to proceed with the payment process.
9. **Successful Payment Handler**: The `successful_payment` function is triggered when the user successfully completes the payment. It extracts payment details, records the purchase in the database using the `PurchaseDao`, and sends a confirmation message to the user.

Usage Example
-------------------------

```python
# Example of how to use the `catalog_router` in a Telegram bot application
from aiogram import Dispatcher

# ...other imports...

dp = Dispatcher(bot)

# Register the catalog router with the Dispatcher
dp.include_router(catalog_router)

# Start the bot
bot.run_polling()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".