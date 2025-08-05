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
This code block provides functionality to send and receive emails using SMTP and IMAP servers. It includes two main functions:

- `send`: Sends an email using the specified SMTP server.
- `receive`: Retrieves emails from an IMAP server.

Execution Steps
-------------------------
1. **SMTP Email Sending (send function):**
    - Establishes an SMTP connection using the `smtplib` library.
    - Creates an email message using `MIMEText`.
    - Sets the subject, sender, and recipient of the email.
    - Sends the email using the SMTP connection.
    - Closes the connection.
2. **IMAP Email Receiving (receive function):**
    - Establishes an IMAP connection using the `imaplib` library.
    - Selects the desired folder (default: 'inbox').
    - Searches for all emails in the selected folder.
    - Iterates through each email, extracting its subject, sender, and body.
    - Stores the email data in a dictionary.
    - Adds the dictionary to a list of emails.
    - Closes the connection.

Usage Example
-------------------------

```python
from src.utils.smtp import send, receive

# Send an email
send(subject='Test Email', body='This is a test email.', to='recipient@example.com')

# Receive emails from an IMAP server
emails = receive(imap_server='imap.example.com', user='username', password='password')
if emails:
    for email in emails:
        print(f"Subject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"Body: {email['body']}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".