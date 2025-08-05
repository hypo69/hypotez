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
The code defines several functions that generate various inline keyboard markups for a Telegram bot. These markups are used to provide interactive menus for the bot's users.

Execution Steps
-------------------------
1. **`main_user_kb(user_id: int) -> InlineKeyboardMarkup`**: This function generates a keyboard for the main user menu. It includes buttons for user profile, catalog, about the store, and support. If the user is an admin, an admin panel button is also included.
2. **`catalog_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup`**: This function generates a keyboard for the product catalog, displaying buttons for each category based on the provided `catalog_data`.
3. **`purchases_kb() -> InlineKeyboardMarkup`**: This function generates a keyboard for the user's purchase history, allowing them to view their previous purchases.
4. **`product_kb(product_id, price, stars_price) -> InlineKeyboardMarkup`**: This function generates a keyboard for a specific product, providing options to buy using different payment methods (Yukassa, Robocassa, or Stars).
5. **`get_product_buy_youkassa(price) -> InlineKeyboardMarkup`**: This function generates a keyboard for buying a product using Yukassa, showing the price and offering an option to cancel.
6. **`get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup`**: This function generates a keyboard for buying a product using Robocassa, showing the price and providing a web app link for payment.
7. **`get_product_buy_stars(price) -> InlineKeyboardMarkup`**: This function generates a keyboard for buying a product using Stars, showing the price and offering an option to cancel.

Usage Example
-------------------------

```python
from bot.endpoints.bots.telegram.digital_market.bot.user.kbs import main_user_kb, catalog_kb, product_kb

# Generate the main user keyboard
main_kb = main_user_kb(user_id=12345)

# Generate a catalog keyboard with sample category data
categories = [Category(id=1, category_name="Electronics"), Category(id=2, category_name="Clothes")]
catalog_kb = catalog_kb(catalog_data=categories)

# Generate a product keyboard with sample data
product_kb = product_kb(product_id=10, price=100, stars_price=50)

# Send the keyboards to the user using the Telegram bot API
# ...
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".