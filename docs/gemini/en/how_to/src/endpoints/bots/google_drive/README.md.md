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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

```markdown
# Google Drive Uploader Bot

This is a Telegram bot written in Python that can upload direct and supported links to Google Drive. It's inspired by the Google Drive Uploader bot by Sumanjay.

### Inspired By Sumanjay Bot:D [Google Drive Uploader](https://telegram.dog/driveuploadbot)

Here is the live version of the bot [Gdriveupme_bot](http://telegram.dog/gdriveupme_bot)

## How to Use the Bot

1. **Authorize the Bot:** Use the `/auth` command to generate a key and send it to the bot.
2. **Send Links:** Send supported links to the bot.

## Supported Links:

- Direct links
- Mega.nz links
- Openload links (not available anymore)
- Dropbox links

## Requirements:

- [Google Drive API Credential](https://console.cloud.google.com/apis/credentials) (Other types) *Required*
- Telegram Bot Token (Using BotFather) *Required*
- Openload FTP login and Key *Optional*
- Mega Email and Password *Optional*

## Setup Your Own Bot

1. Create your [Google Drive API Credential](https://console.cloud.google.com/apis/credentials) (other type) and download its JSON.
2. Paste it in the bot root directory and rename it "client_secrets.json".
3. Replace your bot token in the [creds.py file](./creds.py).
4. Your bot is ready to host.

### Hosting with Heroku

Make sure you have changed your bot token and Google client API before hosting it.

## TODO:

- Rename files while uploading
- Add Telegram File Support [slow download :( ]
- Add YouTube-dl
- Fix openload support
- Add zippyshare, Mediafire, cloud mail, Yandex disk, Sourceforge {these are already written in PPE plugin, you can use these from there}
- Google Drive Direct Link Generator

## License

- GPLv3

## Credits

- [CyberBoySumanjay](https://github.com/cyberboysumanjay)
- [SpEcHiDe](https://github.com/SpEcHiDe)
- [Atulkadian](https://github.com/atulkadian)