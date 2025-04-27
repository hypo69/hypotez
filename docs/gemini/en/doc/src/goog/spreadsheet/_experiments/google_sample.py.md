# Module: Google Spreadsheets API Sample

## Overview

This module provides a basic example of how to interact with Google Spreadsheets using the Google Sheets API and OAuth2 authentication. It demonstrates reading data from a spreadsheet and printing selected columns.

## Details

The code showcases the following steps:

1. **Authentication:**
    - It uses OAuth2 authentication to obtain credentials for accessing the user's Google account.
    - It retrieves credentials from a local file (`token.json`) or initiates an authentication flow if they are not present or expired.

2. **API Call:**
    - It builds a Google Sheets API service object using the obtained credentials.
    - It makes an API request to retrieve values from a specified spreadsheet and range (`SAMPLE_SPREADSHEET_ID` and `SAMPLE_RANGE_NAME`).

3. **Data Processing:**
    - It extracts values from the API response and prints specific columns (Name and Major) to the console.

## Classes

### `Credentials`

**Description:** A class that represents credentials for authenticating with Google APIs.

**Inherits:**  `google.oauth2.credentials.Credentials`

**Attributes:**

- `token`: An access token for accessing Google APIs.
- `refresh_token`: A refresh token for renewing expired access tokens.

**Methods:**

- `refresh(Request())`: Refreshes the access token using the refresh token.

### `InstalledAppFlow`

**Description:** A class that manages the OAuth2 authentication flow for a desktop application.

**Inherits:**  `google_auth_oauthlib.flow.InstalledAppFlow`

**Attributes:**

- `client_secrets_file`: The path to the file containing the client secrets for the application.
- `scopes`: A list of scopes (permissions) required for the application.

**Methods:**

- `run_local_server(port=0)`: Starts a local server for the OAuth2 flow, allowing the user to authenticate and grant access.

### `build`

**Description:** A function that creates a Google API service object using the provided credentials.

**Parameters:**

- `service`: The name of the Google API service to connect to (e.g., `'sheets'`).
- `version`: The API version to use (e.g., `'v4'`).
- `credentials`: The credentials object obtained through OAuth2 authentication.

**Returns:**
- A Google API service object representing the specified API service.

## Functions

### `main`

**Purpose:**
- This function serves as the entry point for the script.
- It handles OAuth2 authentication, builds the Google Sheets API service, makes API calls, and processes the retrieved data.

**Parameters:**
- None

**Returns:**
- None

**Raises Exceptions:**
- `HttpError`: An error occurred while interacting with the Google Sheets API.

**Example:**

```python
if __name__ == '__main__':
    main()
```

**How the Function Works:**

1. **Authentication:**
    - It retrieves credentials from the `token.json` file.
    - If credentials are not present or expired, it initiates an OAuth2 flow using `InstalledAppFlow` to obtain new credentials.

2. **API Service Creation:**
    - It constructs a Google Sheets API service object using `build` with the obtained credentials.

3. **API Call:**
    - It uses the Sheets API service to make a `values().get()` request, retrieving values from the specified spreadsheet and range.

4. **Data Processing:**
    - It extracts values from the API response and prints specific columns.

5. **Error Handling:**
    - It catches `HttpError` exceptions that might occur during API interactions and prints the error message.

## Inner Functions

### `None`

This function does not have any inner functions.


## Parameter Details

- `SAMPLE_SPREADSHEET_ID`:  The ID of the Google Spreadsheet to be accessed.

- `SAMPLE_RANGE_NAME`:  The range of cells to retrieve data from within the specified spreadsheet.

- `SCOPES`:  A list of API scopes (permissions) required for the application to read data from Google Spreadsheets.

- `path`: The path to the file containing the client secrets for the application, used for OAuth2 authentication.

- `token.json`: A file that stores the user's access and refresh tokens, allowing the script to quickly authenticate in subsequent runs.

## Examples

```python
# Example 1: Running the script with existing credentials
if __name__ == '__main__':
    main()

# Example 2: Initiating the authentication flow
if __name__ == '__main__':
    main()
```