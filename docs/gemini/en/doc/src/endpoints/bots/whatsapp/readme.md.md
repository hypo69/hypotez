# WhatsApp Bot for Automated Messaging

## Overview

This document provides a comprehensive guide to creating a Python script for automating WhatsApp message sending. Users can customize the script to send a desired number of messages within a specific time range. For optimal performance, it's crucial to keep track of updates to libraries and the WhatsApp web version.

## Details

This guide outlines the development of a Python script that automates the sending of random WhatsApp messages within a defined time period. The target audience for this guide includes developers with basic Python programming knowledge and an understanding of command-line operations.

## Prerequisites

* **Python 3.6+:** The script requires Python 3.6 or a later version. 
* **pip Package Manager:** The script relies on the `pip` package manager for installing libraries.
* **Web Browser and WhatsApp Web:** The system must have a web browser (e.g., Chrome or Firefox) installed with the ability to access WhatsApp Web.

## Components

### Libraries

* **`pywhatkit`:** This library facilitates interaction with the WhatsApp web version and message sending.
* **`pyautogui`:** This library automates mouse and keyboard actions.
* **`pynput`:** This library provides keyboard input control.
* **`emoji`:** This library enables the inclusion of emoji in messages.
* **`random`:** This library generates random messages and timing.
* **`time`:** This library manages delays and execution times.

### Installation

Install the required libraries using the `pip` package manager:

```bash
pip install pywhatkit pyautogui pynput emoji
```

## Development Process

### Sending Messages Function (`send_whatsapp_message`)

**Purpose**: This function sends a WhatsApp message to a specified recipient.

**Parameters**:

* `phone_number` (str): The recipient's phone number (including the country code).
* `message` (str): The message text.
* `hour` (int): The hour of message sending (0-23).
* `minutes` (int): The minute of message sending (0-59).

**Implementation**:

1.  Utilize `pywhatkit.sendwhatmsg` to initialize message sending.
2.  Employ `time.sleep` to introduce a delay for WhatsApp web loading.
3.  Utilize `pyautogui` and `pynput` to simulate pressing the "Enter" key for message sending.
4.  Handle exceptions with a `try...except` block to display errors.

### Message Bank

* Create a list of strings (`messages`) to store the messages.
* Use `emoji.emojize` to add emoji to messages.
* Employ `random.choice` to randomly select a message.

### User Input

* Obtain the number of messages (`num_messages`) using the `input` function.
* Get the starting hour (`start_hour`) and ending hour (`end_hour`) of the sending range using `input`.

### Main Sending Loop

* A `while` loop continues until the message count (`message_count`) reaches the specified quantity (`num_messages`).
* Generate random hours and minutes using `random.randint`.
* Call the `send_whatsapp_message` function with the acquired data.
* Increment the message counter.

## Potential Issues and Solutions

* **`pywhatkit` Issues:** In case of unsuccessful automatic message sending, use `pyautogui` and `pynput` to emulate keystrokes and send the message.
* **WhatsApp Web Connection:** The first-time use requires connecting to WhatsApp Web through a web browser.
* **Dynamic Delay:** The loading speed of WhatsApp Web can vary, so increasing the delay time for stability is recommended.
* **Browser and WhatsApp Version Dependency:** Changes to the browser or WhatsApp web version might necessitate adjustments to the script.

## Code Example

```python
# ... (Code) ...
```

## Executing the Script

1.  Save the script in a file with the `.py` extension.
2.  Run the script in the terminal using the command: `python filename.py`
3.  Follow the on-screen instructions to enter the required data.

## Additional Notes

* For stable operation, it's essential to monitor updates to libraries and the web version of WhatsApp.
* The provided code serves as a starting point and can be customized according to specific needs.

## Conclusion

This guide provides a comprehensive overview of developing a Python script for automating WhatsApp message sending. By following the instructions and adapting the code to specific requirements, users can easily automate their WhatsApp communication.