# Module: `crypt.py`

## Overview

This module provides functions for encrypting and decrypting data using the Advanced Encryption Standard (AES) algorithm in CBC (Cipher Block Chaining) mode. The module utilizes the `Crypto.Cipher` library for encryption and decryption operations. 

## Details

This module implements a simple encryption scheme for data protection. It employs AES in CBC mode, a robust and widely used symmetric encryption algorithm. The key used for encryption and decryption is derived from a user-provided key and a randomly generated salt, ensuring enhanced security. This module is designed for use within the `hypotez` project.

## Functions

### `pad(data: str) -> bytes`

**Purpose**: This function adds padding to the provided string data to ensure it aligns with the block size required by the AES encryption algorithm. 

**Parameters**:

- `data` (str): The string data to be padded.

**Returns**:

- `bytes`: The padded data in bytes format.

**How the Function Works**:

1. **Convert to Bytes**: The input string is converted to bytes using `data.encode()`.
2. **Calculate Padding**: The function calculates the number of bytes needed to pad the data to make it a multiple of the AES block size (16 bytes).
3. **Append Padding**: The calculated number of padding bytes (with the value equal to the number of padding bytes) is appended to the original data in bytes format.

### `encrypt(data, key)`

**Purpose**: This function encrypts the provided data using the AES algorithm in CBC mode. 

**Parameters**:

- `data`: The data to be encrypted.
- `key`: The key used for encryption.

**Returns**:

- `str`: A JSON string representing the encrypted data, including the ciphertext, initialization vector (IV), and salt.

**How the Function Works**:

1. **Generate Salt**: A random 8-character salt is generated consisting of lowercase letters.
2. **Derive Key and IV**: The key and IV used for encryption are derived from the provided `key` and generated `salt` by repeatedly hashing them using MD5. This process is repeated three times.
3. **Pad Data**: The data is padded using the `pad()` function to align it with the AES block size.
4. **Perform Encryption**: The padded data is encrypted using the derived key and IV in CBC mode using `AES.new()`.
5. **Encode and Return**: The ciphertext is base64 encoded, and a JSON string containing the ciphertext, IV, and salt is returned.

### `unpad(data: bytes) -> bytes`

**Purpose**: This function removes padding from the provided data. 

**Parameters**:

- `data` (bytes): The padded data in bytes format.

**Returns**:

- `bytes`: The unpadded data in bytes format.

**How the Function Works**:

1. **Extract Padding**: The padding value is obtained from the last byte of the data.
2. **Remove Padding**: The padding bytes are removed from the end of the data.

### `decrypt(data: str, key: str)`

**Purpose**: This function decrypts the provided data that was previously encrypted using the `encrypt()` function. 

**Parameters**:

- `data` (str): The encrypted data represented as a JSON string.
- `key` (str): The key used for decryption.

**Returns**:

- `str`: The decrypted data as a string.

**How the Function Works**:

1. **Parse JSON**: The JSON string containing the encrypted data is parsed to extract the ciphertext, IV, and salt.
2. **Derive Key and IV**: The key and IV are derived from the provided `key` and extracted salt using MD5 hashing, as done in the `encrypt()` function.
3. **Perform Decryption**: The ciphertext is decrypted using the derived key and IV in CBC mode using `AES.new()`.
4. **Remove Padding**: The padding is removed from the decrypted data using `unpad()`.
5. **Return Decrypted Data**: The unpadded data is returned as a string.

## Examples

```python
# Encryption example
data_to_encrypt = "This is some sensitive data to be encrypted."
key = "your_secret_key"

encrypted_data = encrypt(data_to_encrypt, key)

# Decryption example
decrypted_data = decrypt(encrypted_data, key)

# Print the results
print(f"Original data: {data_to_encrypt}")
print(f"Encrypted data: {encrypted_data}")
print(f"Decrypted data: {decrypted_data}")