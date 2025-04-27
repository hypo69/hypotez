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
This code defines a Telegram bot application. It handles various user interactions, including:
- **Start command**: Initializes the user's data and begins the bot's interaction.
- **Profile command**: Displays the user's current subscription status (Free, Basic, or Pro).
- **Stat command**: Shows statistics (for admins only) about the number of users and those with active promo codes.
- **Payment processing**: Handles payment confirmation and updates user data.
- **Text generation**: Processes text generation requests using `ToolBox_requests` module, checking user's token balance and free requests.
- **Image generation**: Handles image generation requests, requiring a Pro subscription.
- **Callbacks**: Responds to button clicks, navigating through different features.
- **Tariff selection**: Allows users to choose between Basic, Pro, and promo code options.
- **Free mode**: Provides limited functionality for free users with a daily limit on requests.

Execution Steps
-------------------------
1. **Initialize environment variables**: Loads configuration values from a `.env` file.
2. **Create objects**: Instantiates `ToolBox` and `DataBase` objects to handle bot communication and user data persistence.
3. **Database setup**: Creates a database table and loads existing user data from the database.
4. **Define bot handlers**: Uses decorators to specify functions responsible for handling different user interactions.
5. **Process payment confirmation**: Updates user subscription status and token balances upon successful payments.
6. **Process `start` command**: Initializes user data or updates existing data with subscription details and token balances.
7. **Display user profile**: Shows the user's current subscription level and available resources.
8. **Display bot statistics**: Provides admin access to user statistics.
9. **Generate promotional code**: Creates a unique promo code for referral purposes.
10. **Handle callback queries**: Responds to button clicks, updating user preferences and triggering relevant actions.
11. **Process text generation requests**: Manages text generation requests based on user's subscription and available tokens.
12. **Process image generation requests**: Handles image generation requests, ensuring a Pro subscription is active.
13. **Start bot polling**: Initiates a loop to listen for incoming user messages and respond accordingly.
14. **Periodically check subscription expiry**: Runs a background task to check for subscription expiry and update user data.

Usage Example
-------------------------

```python
# Example of using the `StartProcessing` function
message = types.Message(chat={'id': 123456789})  # Simulate a user message with chat ID
StartProcessing(message)

# Example of handling a text generation request
message = types.Message(chat={'id': 123456789}, text='Generate a funny story about a cat.')
TasksProcessing(message)

# Example of selecting a Basic tariff
call = types.CallbackQuery(data='basic', message={'chat': {'id': 123456789}})
CallsProcessing(call)

# Example of using the promotional code
message = types.Message(chat={'id': 123456789}, text='free24')
get_promo_code(message)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".