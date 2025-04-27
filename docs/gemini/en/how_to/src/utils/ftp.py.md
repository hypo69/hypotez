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
This code block provides functions for interacting with an FTP server. It includes functions to send, receive, and delete files from the FTP server.

Execution Steps
-------------------------
1. **Connect to FTP server**: The `write`, `read`, and `delete` functions first establish a connection to the FTP server using the provided credentials and server information.
2. **Perform the desired operation**: 
    - `write`: Sends a file from a local path to a specified directory and filename on the FTP server.
    - `read`: Retrieves a file from the specified directory and filename on the FTP server and saves it to a local path.
    - `delete`: Deletes a file with the specified name from the specified directory on the FTP server.
3. **Close the connection**: After completing the operation, the FTP session is closed to release the connection resources.

Usage Example
-------------------------

```python
# Example: Sending a file to FTP server
from src.utils.ftp import write

success = write('local_path/to/file.txt', '/remote/directory', 'file.txt')
if success:
    print("File sent successfully!")
else:
    print("Failed to send file")

# Example: Retrieving a file from FTP server
from src.utils.ftp import read

file_content = read('local_path/to/file.txt', '/remote/directory', 'file.txt')
if file_content:
    print(f"File content: {file_content[:100]}...")
else:
    print("Failed to retrieve file")

# Example: Deleting a file from FTP server
from src.utils.ftp import delete

success = delete('local_path/to/file.txt', '/remote/directory', 'file.txt')
if success:
    print("File deleted successfully!")
else:
    print("Failed to delete file")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".