# Mega Class Documentation

## Overview

This module provides the `Mega` class for interacting with the Mega cloud storage service. It allows you to:

- Login using email and password or as an ephemeral user.
- Download and upload files.
- Get public URLs for files.
- Retrieve file information (attributes).

## Details

The `Mega` class uses the Mega API to interact with the service. It performs requests using `requests` and handles decryption and encryption using the `Crypto` library. 

## Classes

### `Mega`

**Description:** 
This class represents a Mega client that interacts with the Mega cloud storage service.

**Attributes:**

- `seqno (int):`  Sequential number used for API requests. 
- `sid (str):`  Session ID for authenticated users.
- `master_key (list):` The user's decrypted master key.
- `rsa_priv_key (list):` The user's RSA private key (only for users with a `csid`).
- `root_id (str):`  The ID of the user's root folder (Cloud Drive).
- `inbox_id (str):`  The ID of the user's inbox folder.
- `trashbin_id (str):` The ID of the user's trashbin folder.

**Methods:**

- `api_req(data: dict) -> dict:` Sends an API request to Mega.
- `login_user(email: str, password: str) -> None:` Logs in a user with the provided email and password.
- `login_ephemeral() -> None:` Logs in as an ephemeral user.
- `_login_common(res: dict, password: list) -> None:` Performs common login operations after obtaining initial data from the API.
- `get_files() -> dict:` Retrieves a list of files and folders in the user's Mega account.
- `download_from_url(url: str) -> str:` Downloads a file from a public Mega URL.
- `download_file(file_id: str, file_key: str, public: bool = False, store_path: str = None) -> str:` Downloads a file from Mega.
- `get_public_url(file_id: str, file_key: list) -> str:` Generates a public URL for a file.
- `uploadfile(filename: str, dst: str = None) -> dict:` Uploads a file to Mega.

## Functions

### `api_req(data: dict) -> dict:` 

**Purpose:**  Sends an API request to Mega and returns the response data.

**Parameters:**

- `data (dict):`  A dictionary containing the request data.

**Returns:**

- `dict:`  The response data from the Mega API as a dictionary.

**Raises Exceptions:**

- `MegaRequestException: ` If the Mega API returns an error code.

**How the Function Works:**

1.  The function constructs a request to the Mega API endpoint `https://g.api.mega.co.nz/cs`.
2.  It includes the current sequence number (`seqno`) and the session ID (`sid`) if available.
3.  The request data is encoded as JSON and sent to the API.
4.  The function handles the response:
    - If the response is an integer, it is considered an error code and raises a `MegaRequestException`.
    - Otherwise, the function returns the first element of the response array, which should be the API response data.

### `login_user(email: str, password: str) -> None:`

**Purpose:** Logs in a user with the provided email and password.

**Parameters:**

- `email (str):` The user's email address.
- `password (str):` The user's password.

**Raises Exceptions:**

- `MegaIncorrectPasswordExcetion:` If the provided email and/or password are incorrect.

**How the Function Works:**

1.  The function prepares the password using `prepare_key` and `str_to_a32`.
2.  It calculates the user hash (`uh`) using `stringhash`.
3.  It sends a `us` (user sign-in) request to the API with the email and user hash.
4.  It calls `_login_common` to complete the login process using the response and prepared password.

### `login_ephemeral() -> None:`

**Purpose:** Logs in as an ephemeral user.

**How the Function Works:**

1.  The function generates random master key, password key, and session self-challenge.
2.  It encrypts the master key using `encrypt_key` and encodes it to base64.
3.  It creates a `ts` (timestamp) value by combining the session self-challenge with the encrypted self-challenge using the master key.
4.  It sends a `up` (user password) request to the API with the encoded keys and timestamp.
5.  It receives a user handle from the API response.
6.  It sends a `us` (user sign-in) request with the user handle.
7.  It calls `_login_common` to complete the login process using the response and the randomly generated password key.

### `_login_common(res: dict, password: list) -> None:` 

**Purpose:** Performs common login operations after obtaining initial data from the API.

**Parameters:**

- `res (dict):`  The API response data.
- `password (list):`  The password key (either the user's password or the ephemeral password key).

**How the Function Works:**

1.  It checks for error codes (-2 or -9) in the response and raises `MegaIncorrectPasswordExcetion` if necessary.
2.  It decrypts the master key (`k`) from the response using the provided password and stores it in `self.master_key`.
3.  If the response includes a `tsid`, the function extracts the timestamp, encrypts it with the master key, and verifies the encrypted timestamp against the provided one to ensure the session is valid.
4.  If the response includes a `csid`, the function decrypts the RSA private key using the master key, constructs an RSA object, and decrypts the `csid` to obtain the session ID (`sid`).

### `get_files() -> dict:`

**Purpose:** Retrieves a list of files and folders in the user's Mega account.

**Returns:**

- `dict:`  A dictionary containing information about the user's files and folders, including:
    - `f (list):` A list of files and folders.
    - `h (str):` The user's root folder ID.
    - `i (str):` The user's inbox folder ID.
    - `t (str):` The user's trashbin folder ID.

**How the Function Works:**

1.  The function sends an `f` (files) request to the API to retrieve the user's file list.
2.  For each file or folder in the response:
    - It decrypts the key (`k`) using the master key.
    - It decrypts the attributes (`a`) using the key and stores the decrypted values in the file data.
3.  It extracts the root folder ID (`h`), inbox folder ID (`i`), and trashbin folder ID (`t`) if present in the response.
4.  It returns the entire file list data.

### `download_from_url(url: str) -> str:`

**Purpose:** Downloads a file from a public Mega URL.

**Parameters:**

- `url (str):`  The public Mega URL for the file.

**Returns:**

- `str:` The path to the downloaded file.

**How the Function Works:**

1.  The function parses the URL to extract the file ID and file key.
2.  It calls `download_file` with the file ID and file key, setting `public` to `True`.

### `download_file(file_id: str, file_key: str, public: bool = False, store_path: str = None) -> str:`

**Purpose:** Downloads a file from Mega.

**Parameters:**

- `file_id (str):`  The file ID.
- `file_key (str):`  The file key.
- `public (bool):`  Whether the file is publicly accessible. Default: `False`.
- `store_path (str):`  The path to the directory where the file should be saved. Default: `None`.

**Returns:**

- `str:` The path to the downloaded file.

**Raises Exceptions:**

- `ValueError:` If the file MAC doesn't match.

**How the Function Works:**

1.  The function sends a `g` (get) request to the API to retrieve the file data.
2.  It decrypts the file key and extracts the initialization vector (IV), meta-MAC, file URL, file size, and attributes.
3.  It downloads the file in chunks using `requests` and streams the data to a local file.
4.  It decrypts each chunk using a counter-mode AES decryptor with the extracted key and IV.
5.  It calculates a MAC for each chunk and accumulates the MAC values to create the file MAC.
6.  It compares the calculated file MAC with the meta-MAC and raises a `ValueError` if they don't match.
7.  It closes the input and output streams and returns the path to the downloaded file.

### `get_public_url(file_id: str, file_key: list) -> str:`

**Purpose:** Generates a public URL for a file.

**Parameters:**

- `file_id (str):`  The file ID.
- `file_key (list):`  The file key.

**Returns:**

- `str:` The public Mega URL for the file.

**How the Function Works:**

1.  The function sends an `l` (link) request to the API to retrieve the public handle for the file.
2.  It encodes the file key to base64.
3.  It constructs the public URL using the public handle and encoded file key.

### `uploadfile(filename: str, dst: str = None) -> dict:`

**Purpose:** Uploads a file to Mega.

**Parameters:**

- `filename (str):` The path to the file to upload.
- `dst (str):`  The destination folder ID (optional). Default: `None` (uploads to root folder).

**Returns:**

- `dict:` The response data from the API.

**How the Function Works:**

1.  The function checks if the destination folder ID is provided. If not, it retrieves the root folder ID (`root_id`) if necessary.
2.  It opens the file for reading.
3.  It sends a `u` (upload) request to the API to get the upload URL.
4.  It generates a random upload key and initializes a counter for the AES CTR encryption.
5.  It encrypts the file in chunks using AES CTR encryption with the upload key.
6.  It uploads each chunk to the specified URL.
7.  It calculates a MAC for each chunk and accumulates the MAC values to create the file MAC.
8.  It constructs the attributes for the uploaded file, including the filename.
9.  It encrypts the attributes using the upload key.
10. It encrypts the upload key with the master key.
11. It sends a `p` (put) request to the API to save the file metadata, including the file name, encrypted attributes, and encrypted key.
12. It returns the API response.

## Parameter Details

- `file_id (str):` The unique identifier for a file or folder in Mega.
- `file_key (list):` A list of 8 integers representing the encrypted file key.
- `email (str):` The email address used for login.
- `password (str):` The user's password.
- `filename (str):` The path to the file on the local system.
- `dst (str):` The folder ID where the file should be uploaded.
- `store_path (str):` The path to the directory where a downloaded file should be saved.
- `public (bool):` A flag indicating if a file is accessible publicly.

## Examples

```python
from mega import Mega

# Login with email and password
mega = Mega.from_credentials("your_email@example.com", "your_password")

# Upload a file
file_data = mega.uploadfile("path/to/your/file.txt")
print(file_data)

# Download a file from a public URL
file_path = mega.download_from_url("https://mega.nz/#!%s!%s")
print(f"File downloaded to: {file_path}")

# Get a public URL for a file
public_url = mega.get_public_url(file_id, file_key)
print(f"Public URL: {public_url}")

# Get a list of files
files = mega.get_files()
print(files)