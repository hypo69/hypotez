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
This code block defines constants used by the Google Drive Uploader Bot. These constants contain messages for the bot's interactions with users, file download and upload status updates, authorization messages, and other relevant information. It also defines configuration variables related to supported file sharing services like Dropbox, Openload, and Mega.

Execution Steps
-------------------------
1. **Define Drive Folder Name**: Sets the default name for the folder where files will be uploaded.
2. **Define Mega Credentials**: Assigns the email and password for the Mega account used by the bot.
3. **Define Bot Messages**: Establishes text messages for different bot functionalities including initial greeting, help information, download and upload status, authorization messages, error handling, and update notifications.
4. **Configure Supported Services**: Sets flags to indicate the availability of support for specific file sharing services (Dropbox, Openload, Mega).
5. **Define Download Path**: Defines the default directory where files will be downloaded.
6. **Define Download URL Message**: Prepares a formatted message to display the download link after successful file upload.
7. **Define Authentication Error Message**: Specifies the message displayed when an authentication error occurs.
8. **Define Update Message**: Contains information about the bot updates and supported services. 

Usage Example
-------------------------
```python
# Example usage of the constants in the bot's logic:
if user_input == '/help':
    bot.send_message(user_id, HELP)  # Send the help message
elif user_input == '/auth':
    # Generate authentication URL and send to user
elif user_input.startswith('https://www.dropbox.com/'):
    bot.send_message(user_id, DP_DOWNLOAD)  # Indicate Dropbox download started
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".