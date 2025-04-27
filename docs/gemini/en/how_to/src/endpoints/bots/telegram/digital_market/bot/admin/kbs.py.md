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
This code block defines functions to generate inline keyboards for different actions within an admin panel of a Telegram bot. Each function creates a keyboard with specific buttons that trigger different actions based on the callback data.

Execution Steps
-------------------------
1. Each function initializes an `InlineKeyboardBuilder` object.
2. It adds buttons to the keyboard using `kb.button(text=..., callback_data=...)`.
3. The callback data is used to identify the specific action triggered by the button.
4. The `kb.adjust(...)` method adjusts the layout of the buttons on the keyboard.
5. Finally, the `kb.as_markup()` method converts the keyboard builder into an `InlineKeyboardMarkup` object.

Usage Example
-------------------------

```python
from bot.endpoints.bots.telegram.digital_market.bot.admin.kbs import catalog_admin_kb, admin_kb

# Get a list of categories from the database
catalog_data = [
    Category(id=1, category_name='Electronics'),
    Category(id=2, category_name='Clothing')
]

# Create an inline keyboard for the catalog admin panel
catalog_kb = catalog_admin_kb(catalog_data)

# Send the keyboard to the user
await bot.send_message(chat_id=user_id, text="Select a category:", reply_markup=catalog_kb)

# Example of using the admin keyboard
admin_kb = admin_kb()
await bot.send_message(chat_id=user_id, text="Admin Panel", reply_markup=admin_kb)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".