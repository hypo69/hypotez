# Module for Keyboard Buttons for Telegram Bot
## Overview

This module provides functions for generating keyboard buttons for a Telegram bot. These buttons are used for various actions within the bot, such as navigating through the catalog, purchasing products, and accessing user profiles.

## Details

The module utilizes the `aiogram.types` and `aiogram.utils.keyboard` libraries for constructing and customizing keyboard buttons. The functions defined here generate various keyboard layouts, including inline keyboards and reply keyboards, each tailored for different functionalities. The buttons are used to guide users through the bot's features and allow for seamless interaction.

## Classes
**No Classes**

## Functions

### `main_user_kb`

**Purpose**: Generates the main keyboard for the user interface.

**Parameters**:
- `user_id` (int): The ID of the user interacting with the bot.

**Returns**:
- `InlineKeyboardMarkup`: An inline keyboard markup with buttons for user actions, including profile access, catalog navigation, information about the store, and support for the author.

**Example**:

```python
from src.endpoints.bots.telegram.digital_market.bot.user.kbs import main_user_kb

# Example usage:
user_id = 1234567890
keyboard = main_user_kb(user_id)
# keyboard will be an InlineKeyboardMarkup object
```

### `catalog_kb`

**Purpose**: Generates a keyboard for navigating the catalog.

**Parameters**:
- `catalog_data` (List[Category]): A list of `Category` objects representing different product categories.

**Returns**:
- `InlineKeyboardMarkup`: An inline keyboard markup with buttons for each category in the catalog, allowing users to browse products based on category.

**Example**:

```python
from src.endpoints.bots.telegram.digital_market.bot.user.kbs import catalog_kb
from bot.dao.models import Category

# Example usage:
catalog_data = [Category(id=1, category_name="Category 1"), Category(id=2, category_name="Category 2")]
keyboard = catalog_kb(catalog_data)
# keyboard will be an InlineKeyboardMarkup object
```

### `purchases_kb`

**Purpose**: Generates a keyboard for accessing user purchases.

**Parameters**:
- None

**Returns**:
- `InlineKeyboardMarkup`: An inline keyboard markup with buttons for viewing purchase history and returning to the main menu.

**Example**:

```python
from src.endpoints.bots.telegram.digital_market.bot.user.kbs import purchases_kb

# Example usage:
keyboard = purchases_kb()
# keyboard will be an InlineKeyboardMarkup object
```

### `product_kb`

**Purpose**: Generates a keyboard for interacting with a specific product.

**Parameters**:
- `product_id` (int): The ID of the product.
- `price` (int): The price of the product in rubles.
- `stars_price` (int): The price of the product in stars.

**Returns**:
- `InlineKeyboardMarkup`: An inline keyboard markup with buttons for purchasing the product using different payment methods (ЮКасса, Robocassa, stars) and navigation buttons.

**Example**:

```python
from src.endpoints.bots.telegram.digital_market.bot.user.kbs import product_kb

# Example usage:
product_id = 1001
price = 1500
stars_price = 1000
keyboard = product_kb(product_id, price, stars_price)
# keyboard will be an InlineKeyboardMarkup object
```

### `get_product_buy_youkassa`

**Purpose**: Generates a keyboard for purchasing a product using ЮКасса.

**Parameters**:
- `price` (int): The price of the product.

**Returns**:
- `InlineKeyboardMarkup`: An inline keyboard markup with a button for payment through ЮКасса and a button for canceling the purchase.

**Example**:

```python
from src.endpoints.bots.telegram.digital_market.bot.user.kbs import get_product_buy_youkassa

# Example usage:
price = 1500
keyboard = get_product_buy_youkassa(price)
# keyboard will be an InlineKeyboardMarkup object
```

### `get_product_buy_robocassa`

**Purpose**: Generates a keyboard for purchasing a product using Robocassa.

**Parameters**:
- `price` (int): The price of the product.
- `payment_link` (str): The payment link provided by Robocassa.

**Returns**:
- `InlineKeyboardMarkup`: An inline keyboard markup with a button for payment through Robocassa (using a web app) and a button for canceling the purchase.

**Example**:

```python
from src.endpoints.bots.telegram.digital_market.bot.user.kbs import get_product_buy_robocassa

# Example usage:
price = 1500
payment_link = "https://example.com/payment"
keyboard = get_product_buy_robocassa(price, payment_link)
# keyboard will be an InlineKeyboardMarkup object
```

### `get_product_buy_stars`

**Purpose**: Generates a keyboard for purchasing a product using stars.

**Parameters**:
- `price` (int): The price of the product in stars.

**Returns**:
- `InlineKeyboardMarkup`: An inline keyboard markup with a button for payment using stars and a button for canceling the purchase.

**Example**:

```python
from src.endpoints.bots.telegram.digital_market.bot.user.kbs import get_product_buy_stars

# Example usage:
price = 1000
keyboard = get_product_buy_stars(price)
# keyboard will be an InlineKeyboardMarkup object
```