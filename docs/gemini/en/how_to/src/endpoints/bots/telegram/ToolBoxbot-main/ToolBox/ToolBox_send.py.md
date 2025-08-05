**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Send a Promotional Message to Telegram Users
=========================================================================================

Description
-------------------------
This code snippet sends a promotional message to Telegram users who have not yet redeemed a promocode. It utilizes the `telebot` and `sqlite3` libraries to interact with the Telegram API and a local database, respectively. 

Execution Steps
-------------------------
1. **Import Libraries**: Imports the `telebot`, `sqlite3`, and `os` libraries.
2. **Load Environment Variables**: Loads environment variables from a `.env` file using the `dotenv` library. This is assumed to contain the Telegram bot token.
3. **Initialize Telegram Bot**: Creates a `TeleBot` object from the imported `telebot` library using the loaded Telegram bot token.
4. **Connect to Database**: Establishes a connection to a SQLite database named "UsersData.db" and creates a cursor object.
5. **Fetch Users**: Executes an SQL query to select user IDs from the "users_data_table" where the `promocode` column is not equal to 1. This is likely used to filter users who haven't used a promocode.
6. **Send Message**: Iterates through the fetched user IDs and attempts to send a promotional message to each user's Telegram chat ID. The message is formatted with HTML tags for better readability.
7. **Handle Exceptions**: Includes a try-except block to catch potential exceptions during message sending. The `print` statements provide basic logging to indicate success or failure for each user.

Usage Example
-------------------------

```python
    import telebot, sqlite3, os
    from dotenv import load_dotenv
    load_dotenv()
    bot = telebot.TeleBot(token=os.environ['TOKEN'])
    conn = sqlite3.connect('UsersData.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM users_data_table WHERE promocode != 1")
    users = cursor.fetchall()
    for us in users:
        try:
            bot.send_message(chat_id=us[0], text="Успейте воспользоваться промокодом FREE24 до 21 декабря!\\n\\nПо нему вы получите бесплатный месяц тарифа PRO — это безлимит на генерацию текста и изображений 💥 \\n\\nЧтобы ввести промокод, перейдите на вкладку Тарифы и нажмите кнопку «Промокод».", parse_mode='html')
        except:
            print(us[0], "no")
        else:
            print(us[0], "yes")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".