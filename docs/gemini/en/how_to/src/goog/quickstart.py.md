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
This code snippet demonstrates basic usage of the Apps Script API to create a new script project, upload a file to the project, and log the script's URL to the console. The code utilizes Google's authentication libraries for user authorization and the `googleapiclient` library to interact with the Apps Script API.

Execution Steps
-------------------------
1. **Authentication and Authorization**: The code first checks if a token file exists (`token.json`). If not, it initiates an authorization flow using `InstalledAppFlow` to obtain user credentials. The credentials are then saved to the `token.json` file for future use.
2. **Build API Service**: The code builds a Google Apps Script API service using `build` function. The service is configured with the user credentials obtained in the previous step.
3. **Create Project**: The code creates a new Apps Script project using the `service.projects().create` method. It sets the project title to `My Script`.
4. **Upload Files**: The code uploads two files to the newly created project using the `service.projects().updateContent` method. The files are `hello.js` containing sample JavaScript code and `appsscript.json` containing project manifest data.
5. **Print URL**: Finally, the code prints the URL of the newly created script project for the user to access and modify.

Usage Example
-------------------------

```python
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

# ... (Rest of the imports and code)

if __name__ == '__main__':
    main()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".