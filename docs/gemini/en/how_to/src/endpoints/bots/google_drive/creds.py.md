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
This code snippet defines a class called `Creds` to store credentials required for a Google Drive bot. It contains attributes for the Telegram bot token, Team Drive folder ID, and Team Drive ID.

Execution Steps
-------------------------
1. **Define the `Creds` Class**: The code defines a class named `Creds`.
2. **Declare Attributes**:  Inside the `Creds` class, three attributes are declared:
    - `TG_TOKEN`: Stores the Telegram bot token.
    - `TEAMDRIVE_FOLDER_ID`: Stores the ID of the Team Drive folder used for uploads.
    - `TEAMDRIVE_ID`: Stores the ID of the Team Drive.
3. **Provide Example Values**: Example values are provided as comments to demonstrate how to assign the credentials.

Usage Example
-------------------------

```python
    # Instantiate the Creds class
    creds = Creds()

    # Assign the credentials
    creds.TG_TOKEN = "your_telegram_bot_token"
    creds.TEAMDRIVE_FOLDER_ID = "your_team_drive_folder_id"
    creds.TEAMDRIVE_ID = "your_team_drive_id"

    # Use the credentials in your bot logic
    # ... 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".