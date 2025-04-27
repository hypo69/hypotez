# Catalog Router for Telegram Bot

## Overview

This module defines the `catalog_router` for the Telegram bot, handling interactions related to product catalogs and purchase processes. It provides functionalities for displaying categories, listing products within each category, handling user purchase requests, and processing successful payments.

## Details

This code is responsible for managing the product catalog and purchase flow within the Telegram bot. Users can browse through categories, view product details, and initiate purchases. 

The module interacts with several other components of the bot, including:

- `UserDAO`: for managing user data.
- `CategoryDao`: for retrieving category information.
- `ProductDao`: for retrieving product information.
- `PurchaseDao`: for managing purchase records.
- `generate_payment_link`: for creating payment links (likely for external payment gateways).
- `successful_payment_logic`: for processing successful payments and updating relevant data.

## Classes

### `catalog_router`

**Description**: This router is responsible for handling interactions with the Telegram bot related to product catalogs and purchases.

**Attributes**: None

**Methods**:

- `page_catalog(call: CallbackQuery, session_without_commit: AsyncSession)`: This method handles the display of the main catalog, showing available categories.
- `page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession)`: This method displays products within a specific category, based on the selected category ID.
- `process_about(call: CallbackQuery, session_without_commit: AsyncSession)`: This method handles the user's selection of a product to purchase and initiates the payment process based on the chosen payment method.
- `send_yukassa_invoice(call, user_info, product_id, price)`: Sends an invoice to the user for payment using Youkassa.
- `send_robocassa_invoice(call, user_info, product_id, price, session: AsyncSession)`: Sends a payment request to the user using Robocassa.
- `send_stars_invoice(call, user_info, product_id, stars_price)`: Sends an invoice to the user for payment using Stars.
- `pre_checkout_query(pre_checkout_q: PreCheckoutQuery)`: Confirms the payment request before proceeding with the checkout process.
- `successful_payment(message: Message, session_with_commit: AsyncSession)`: Processes a successful payment, updates the user's purchase history, and provides appropriate feedback to the user.

## Functions

### `page_catalog(call: CallbackQuery, session_without_commit: AsyncSession)`

**Purpose**: Displays the main product catalog with available categories to the user.

**Parameters**:
- `call (CallbackQuery)`: The Telegram callback query object containing user interaction details.
- `session_without_commit (AsyncSession)`: An asynchronous database session used for interacting with the database.

**Returns**: None

**Raises Exceptions**:
- `Exception`: If an error occurs during the deletion of the user's previous message.

**How the Function Works**:

1. The function first responds to the user with a message indicating that the catalog is loading.
2. It attempts to delete the user's previous message if it exists. 
3. It retrieves all available categories from the database using the `CategoryDao`.
4. It displays a message to the user with a list of categories, allowing the user to select one. The list of categories is displayed using the `catalog_kb` keyboard.

### `page_catalog_products(call: CallbackQuery, session_without_commit: AsyncSession)`

**Purpose**: Displays the products within a specific category selected by the user.

**Parameters**:
- `call (CallbackQuery)`: The Telegram callback query object containing user interaction details.
- `session_without_commit (AsyncSession)`: An asynchronous database session used for interacting with the database.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. The function extracts the category ID from the callback data.
2. It retrieves all products belonging to the specified category from the database using the `ProductDao`.
3. If products are found, it displays a message for each product with its details (name, price, and description) using a formatted text string. The `product_kb` keyboard is used for further interaction with each product.
4. If no products are found in the category, it sends a message to the user indicating that the category is empty.

### `process_about(call: CallbackQuery, session_without_commit: AsyncSession)`

**Purpose**: Handles the user's selection of a product to purchase and initiates the payment process based on the chosen payment method.

**Parameters**:
- `call (CallbackQuery)`: The Telegram callback query object containing user interaction details.
- `session_without_commit (AsyncSession)`: An asynchronous database session used for interacting with the database.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. The function retrieves user information from the database using the `UserDAO`.
2. It extracts information about the selected product (product ID, price, and payment type) from the callback data.
3. Based on the `payment_type`, it calls one of the following functions to initiate the payment process:
    - `send_yukassa_invoice`: for Youkassa payments.
    - `send_stars_invoice`: for Stars payments.
    - `send_robocassa_invoice`: for Robocassa payments.
4. It deletes the previous message.

### `send_yukassa_invoice(call, user_info, product_id, price)`

**Purpose**: Sends an invoice to the user for payment using Youkassa.

**Parameters**:
- `call (CallbackQuery)`: The Telegram callback query object containing user interaction details.
- `user_info`: User information retrieved from the database.
- `product_id`: The ID of the selected product.
- `price`: The price of the selected product.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. This function sends a payment invoice to the user through the Telegram bot.
2. It sets the invoice's title, description, payload (containing user ID, product ID, and payment type), provider token, currency, and price.
3. The `get_product_buy_youkassa` function constructs a keyboard for interacting with the payment request.

### `send_robocassa_invoice(call, user_info, product_id, price, session: AsyncSession)`

**Purpose**: Sends a payment request to the user using Robocassa.

**Parameters**:
- `call (CallbackQuery)`: The Telegram callback query object containing user interaction details.
- `user_info`: User information retrieved from the database.
- `product_id`: The ID of the selected product.
- `price`: The price of the selected product.
- `session (AsyncSession)`: An asynchronous database session used for interacting with the database.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. This function generates a payment link using `generate_payment_link` and sends it to the user for payment.
2. It retrieves the next available purchase ID from the database using `PurchaseDao.get_next_id`.
3. It sets the payment link parameters, including the cost, number, description, user ID, Telegram ID, and product ID.
4. It constructs a keyboard for the payment link using `get_product_buy_robocassa`.

### `send_stars_invoice(call, user_info, product_id, stars_price)`

**Purpose**: Sends an invoice to the user for payment using Stars.

**Parameters**:
- `call (CallbackQuery)`: The Telegram callback query object containing user interaction details.
- `user_info`: User information retrieved from the database.
- `product_id`: The ID of the selected product.
- `stars_price`: The price of the selected product in Stars.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. This function sends an invoice to the user using Stars.
2. It sets the invoice's title, description, payload, provider token, currency (XTR), and price in Stars.
3. It constructs a keyboard for interacting with the payment request using `get_product_buy_stars`.

### `pre_checkout_query(pre_checkout_q: PreCheckoutQuery)`

**Purpose**: Confirms the payment request before proceeding with the checkout process.

**Parameters**:
- `pre_checkout_q (PreCheckoutQuery)`: The Telegram pre-checkout query object containing details about the pending payment.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. This function confirms the payment request by sending a positive response to the `pre_checkout_q` object.

### `successful_payment(message: Message, session_with_commit: AsyncSession)`

**Purpose**: Processes a successful payment, updates the user's purchase history, and provides appropriate feedback to the user.

**Parameters**:
- `message (Message)`: The Telegram message object containing the successful payment information.
- `session_with_commit (AsyncSession)`: An asynchronous database session used for interacting with the database.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

1. This function extracts information about the successful payment from the `message` object.
2. It determines the payment type and price, converting the price from the Telegram format (in cents) to the appropriate currency.
3. It prepares a dictionary (`payment_data`) containing the payment details.
4. It calls `successful_payment_logic` to handle the payment logic, including database updates and user feedback.

## Inner Functions

None.

## Parameter Details

- `call (CallbackQuery)`:  The callback query object represents user interaction with the bot, including button presses and selection of options.
- `session_without_commit (AsyncSession)`: This parameter refers to an asynchronous database session that allows for interacting with the database without committing changes immediately. This is used for read-only operations or scenarios where changes are not immediately necessary.
- `session_with_commit (AsyncSession)`: Similar to the previous parameter, this is an asynchronous database session used for interacting with the database. However, it does commit changes immediately after executing operations. This is used for updating data persistently.
- `pre_checkout_q (PreCheckoutQuery)`: This object represents a pre-checkout query sent by the user before confirming a payment. It contains details about the payment that is about to be made.
- `message (Message)`: This object represents a message sent by the user, which may contain details about a successful payment.
- `user_info`: This parameter represents user information retrieved from the database. It is used to identify and retrieve user data.
- `product_id`: This parameter represents the unique identifier of the selected product.
- `price`: This parameter represents the price of the product.
- `stars_price`: This parameter represents the price of the product in Stars currency.
- `payment_type`: This parameter represents the payment method chosen by the user.

## Examples

```python
# Example 1: User selects a product and initiates payment
# Callback data: 'buy_yukassa_123_500' (payment type, product ID, price)
async def process_about(call: CallbackQuery, session_without_commit: AsyncSession):
    user_info = await UserDAO.find_one_or_none(session=session_without_commit, filters=TelegramIDModel(telegram_id=call.from_user.id))
    _, payment_type, product_id, price = call.data.split('_')

    if payment_type == 'yukassa':
        await send_yukassa_invoice(call, user_info, product_id, price)

# Example 2: User confirms a payment request
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# Example 3: User makes a successful payment
async def successful_payment(message: Message, session_with_commit: AsyncSession):
    payment_info = message.successful_payment
    payment_type, user_id, product_id = payment_info.invoice_payload.split('_')

    if payment_type == 'stars':
        price = payment_info.total_amount
        currency = '⭐'
    else:
        price = payment_info.total_amount / 100
        currency = '₽'

    payment_data = {
        'user_id': int(user_id),
        'payment_id': payment_info.telegram_payment_charge_id,
        'price': price,
        'product_id': int(product_id),
        'payment_type': payment_type
    }

    await successful_payment_logic(session=session_with_commit, payment_data=payment_data, currency=currency, user_tg_id=message.from_user.id, bot=bot)
```