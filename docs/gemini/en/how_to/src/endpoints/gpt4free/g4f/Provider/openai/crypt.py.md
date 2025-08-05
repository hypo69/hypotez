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
This code block defines encryption and decryption functions using AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode. It utilizes a salt for key derivation and base64 encoding for secure data transmission.

Execution Steps
-------------------------
1. **Encryption (`encrypt` function)**:
    - Generates a random 8-character salt.
    - Derives the encryption key and initialization vector (IV) from the provided key and salt using repeated hashing with MD5.
    - Pads the input data using PKCS#7 padding to ensure it's a multiple of the block size (16 bytes).
    - Creates an AES object in CBC mode using the derived key and IV.
    - Encrypts the padded data using the AES object.
    - Base64 encodes the encrypted data and stores it along with the IV and salt in a JSON object.
    - Returns the JSON object as a string.

2. **Decryption (`decrypt` function)**:
    - Parses the JSON data received from the `encrypt` function.
    - Decodes the base64-encoded ciphertext and retrieves the IV and salt.
    - Derives the encryption key and IV from the provided key and salt using repeated hashing with MD5, replicating the encryption process.
    - Creates an AES object in CBC mode using the derived key and IV.
    - Decrypts the ciphertext using the AES object.
    - Removes padding from the decrypted data using PKCS#7 unpadding.
    - Returns the unpadded data as a string.

3. **Padding (`pad` function)**:
    - Converts the input string to bytes.
    - Calculates the number of bytes needed for padding (to make the data length a multiple of 16).
    - Appends padding bytes with their value to the data.
    - Returns the padded data as bytes.

4. **Unpadding (`unpad` function)**:
    - Extracts the padding value from the last byte of the data.
    - Removes the padding bytes from the data.
    - Returns the unpadded data as bytes.

Usage Example
-------------------------

```python
    from src.endpoints.gpt4free.g4f.Provider.openai.crypt import encrypt, decrypt

    key = "your_secret_key"  # Replace with your actual secret key
    data = "This is a secret message"

    encrypted_data = encrypt(data, key)
    print(f"Encrypted data: {encrypted_data}")  # Prints a JSON object with the ciphertext, IV, and salt

    decrypted_data = decrypt(encrypted_data, key)
    print(f"Decrypted data: {decrypted_data}")  # Prints the original message: "This is a secret message"
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".