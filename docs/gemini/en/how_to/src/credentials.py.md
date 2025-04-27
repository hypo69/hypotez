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
The code block defines a `ProgramSettings` class that acts as a central repository for storing global project configuration and credentials. It implements the Singleton pattern to ensure only one instance of the settings is available throughout the application's lifecycle. 

Execution Steps
-------------------------
1. The code initializes the `ProgramSettings` class with default values for host name, configuration, and credentials.
2. It then loads the configuration from `config.json` and sets attributes like timestamp format, project name, host, git repository, and user.
3. The code defines paths to various directories and configures the system's path to include them.
4. It sets the `WEASYPRINT_DLL_DIRECTORIES` environment variable for the WeasyPrint library.
5. The code calls `_load_credentials()` to fetch credentials from a KeePass database.
6. It uses `PyKeePass` to access the KeePass database and extract credentials for different services like AliExpress, OpenAI, Discord, Telegram, PrestaShop, SMTP, Facebook, and Google API.
7. The `_load_credentials()` method iterates through entries in the KeePass database and stores the credentials in the corresponding properties of the `ProgramSettings` instance.
8. Finally, the code defines a `now` property that returns the current timestamp.

Usage Example
-------------------------

```python
    # Get the global ProgramSettings instance
    settings = ProgramSettings() 

    # Access configuration settings
    print(settings.config.project_name)  # Outputs the project name

    # Access credentials
    print(settings.credentials.aliexpress.api_key)  # Outputs the AliExpress API key

    # Get the current timestamp
    current_timestamp = settings.now
    print(current_timestamp) 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".