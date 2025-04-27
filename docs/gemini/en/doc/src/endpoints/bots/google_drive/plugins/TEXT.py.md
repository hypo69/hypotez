# Module for Google Drive Uploader Bot
## Overview
This module defines constants and strings used in the Google Drive Uploader Bot. It provides messages and configurations for user interaction, file handling, and authentication. 

## Details
This module is crucial for managing the interaction and functionality of the Google Drive Uploader Bot. It provides the following functionalities:
- User interaction: Provides messages to guide users on how to authorize the bot, use commands, and understand supported features.
- File handling: Specifies download paths and formats messages for reporting download progress and completion.
- Authentication: Defines URLs and messages related to the Google Drive authentication process, including success and error messages.
- Update messages: Contains information about the bot's updates and features.


## Constants
### `drive_folder_name`
**Description**: The name of the folder on Google Drive where uploaded files are stored. 
**Type**: `str`
**Value**: `"GDriveUploaderBot"` (default) - Replace with your desired folder name.
### `MEGA_EMAIL`
**Description**: The email address associated with the Mega account. 
**Type**: `str`
**Value**: `"bearyan8@yandex.com"` (default) - Replace with your actual Mega email address.
### `MEGA_PASSWORD`
**Description**: The password associated with the Mega account. 
**Type**: `str`
**Value**: `"bearyan8@yandex.com"` (default) - Replace with your actual Mega password.
### `START`
**Description**: The initial welcome message displayed to the user when they start the bot. 
**Type**: `str`
**Value**: `" Hi {}  \\nI am Drive Uploader Bot . Please Authorise To use me .By using /auth \\n\\n For more info /help \\n\\n Third-Party Website \\n Support Added /update \\n\\n For Bot Updates  \\n <a href =\'https://t.me/aryan_bots\'>Join Channel</a>\\nPlease Report Bugs  @aryanvikash"` 
### `HELP`
**Description**: The help message displayed to the user when they use the `/help` command. 
**Type**: `str`
**Value**: `"   <b>AUTHORISE BOT</b> \n       Use  /auth Command Generate\n       Your Google Drive Token And \n       Send It To Bot  \n<b> You Wanna Change Your Login \n        Account ?</b> \\n\\n        You Can Use /revoke \n        command            \n<b>What I Can Do With This Bot? </b>\n            You Can Upload Any Internet\n            Files On Your google\n            Drive Account.\n<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links\n            \n            + More On Its way:)\n                \nBug Report @aryanvikash\n        "` 
### `DP_DOWNLOAD`
**Description**: Message displayed when the bot starts downloading from a Dropbox link. 
**Type**: `str`
**Value**: `"Dropbox Link !! Downloading Started ..."`
### `OL_DOWNLOAD`
**Description**: Message displayed when the bot starts downloading from an Openload link. 
**Type**: `str`
**Value**: `"Openload Link !! Downloading Started ... \\n Openload Links Are Extremely Slow"`
### `PROCESSING`
**Description**: Message displayed when the bot is processing the user's request.
**Type**: `str`
**Value**: `"Processing Your Request ...!!"`
### `DOWN_TWO`
**Description**: Flag indicating whether the download process is active.
**Type**: `bool`
**Value**: `True` 
### `DOWNLOAD`
**Description**: Message displayed when the bot starts downloading a file.
**Type**: `str`
**Value**: `"Downloading Started ..."`
### `DOWN_MEGA`
**Description**: Message displayed when the bot starts downloading a file from a Mega link.
**Type**: `str`
**Value**: `"Downloading Started... \\n  Mega Links are \\n Extremely Slow :("`
### `DOWN_COMPLETE`
**Description**: Message displayed when the bot completes downloading a file. 
**Type**: `str`
**Value**: `"Downloading complete !!"`
### `NOT_AUTH`
**Description**: Message displayed to the user when they are not authorized to use the bot.
**Type**: `str`
**Value**: `"You Are Not Authorised To Using this Bot \\n\\n Please Authorise Me Using /auth  \\n\\n @aryanvikash"`
### `REVOKE_FAIL`
**Description**: Message displayed to the user when they try to revoke access while already unauthorized.
**Type**: `str`
**Value**: `"You Are Already UnAuthorised \\n. Please Use /auth To Authorise \\n\\n report At @aryanvikash "`
### `AUTH_SUCC`
**Description**: Message displayed to the user when they successfully authorize the bot.
**Type**: `str`
**Value**: `"Authorised Successfully  !! \\n\\n Now Send me A direct Link :)"`
### `ALREADY_AUTH`
**Description**: Message displayed to the user when they are already authorized. 
**Type**: `str`
**Value**: `"You Are Already Authorised ! \\n\\n Wanna Change Drive Account? \\n\\n Use /revoke \\n\\n report At @aryanvikash "`
### `AUTH_URL`
**Description**: The URL to generate the Google Drive authorization token. 
**Type**: `str`
**Value**: `'<a href ="{}">Vist This Url</a> \\n Generate And Copy Your Google Drive Token And Send It To Me'` - Replace `{}` with the actual authorization URL.
### `UPLOADING`
**Description**: Message displayed when the bot is uploading the downloaded file to Google Drive. 
**Type**: `str`
**Value**: `"Download Complete !! \\n Uploading Your file"`
### `REVOKE_TOK`
**Description**: Message displayed to the user when their Google Drive token is successfully revoked. 
**Type**: `str`
**Value**: `" Your Token is Revoked Successfully !! \\n\\n Use /auth To Re-Authorise Your Drive Acc. "`
### `DOWN_PATH`
**Description**: The download path for files. 
**Type**: `str`
**Value**: `"Downloads/"` (Linux) - Set the appropriate path for your operating system.
### `DOWNLOAD_URL`
**Description**: Format for the download URL of the uploaded file.
**Type**: `str`
**Value**: `"Your File Uploaded Successfully \\n\\n <b>Filename</b> : {} \\n\\n <b> Size</b> : {} MB \\n\\n <b>Download</b> {}"`
### `AUTH_ERROR`
**Description**: Error message displayed when the bot encounters an authentication error. 
**Type**: `str`
**Value**: `"AUTH Error !! Please  Send Me a  valid Token or Re - Authorise Me  \\n\\n report At @aryanvikash"`
### `OPENLOAD`
**Description**: Flag indicating whether Openload links are supported.
**Type**: `bool`
**Value**: `True` 
### `DROPBOX`
**Description**: Flag indicating whether Dropbox links are supported. 
**Type**: `bool`
**Value**: `True`
### `MEGA`
**Description**: Flag indicating whether Mega links are supported.
**Type**: `bool`
**Value**: `True`
### `UPDATE`
**Description**: Message containing information about the bot's updates and features. 
**Type**: `str`
**Value**: `" <b> Update  on  27.07.2019</b>\n            * MEGA LINK added\n            * Error Handling Improved\n\n<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links (only files)\n            \n            + More are in way:) "`