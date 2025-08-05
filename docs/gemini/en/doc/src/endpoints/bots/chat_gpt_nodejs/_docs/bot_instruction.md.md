# Chat GPT Node.js Bot Instruction

## Overview

This document provides a detailed instruction set for interacting with the Chat GPT Node.js bot within the `hypotez` project.  It outlines the available commands, their syntax, and examples for practical use.

## Details

This instruction set serves as a guide for developers working with the Chat GPT Node.js bot. It defines the commands that can be used to interact with the bot, train it, and test its performance. The bot is built on the Node.js framework and leverages the ChatGPT API for natural language processing.

## Commands

### `!hi`

**Purpose**:  Greets the user with a friendly message.

**Parameters**: None.

**Returns**: A greeting message from the bot.

**Example**:

```
!hi
```

### `!train <data> <data_dir> <positive> <attachment>`

**Purpose**: Trains the model with the provided data.  The data can be provided as a file, a directory, or a file attachment.

**Parameters**:

- **`<data>`**:  Path to the training data file (optional).
- **`<data_dir>`**: Path to the training data directory (optional).
- **`<positive>`**: Indicates whether the training data is positive (optional).
- **`<attachment>`**: Path to the file attachment (optional).

**Returns**:  A confirmation message indicating the training process has started.

**Example**:

```
!train data.json data_dir/ positive attachment.txt
```

### `!test <test_data>`

**Purpose**: Tests the model's performance with provided JSON test data.

**Parameters**:

- **`<test_data>`**: Path to the JSON file containing test data.

**Returns**: A summary of the model's performance on the test data.

**Example**:

```
!test test_data.json
```

### `!archive <directory>`

**Purpose**: Archives files in the specified directory.

**Parameters**:

- **`<directory>`**:  Path to the directory containing files to be archived.

**Returns**:  A confirmation message indicating the archiving process is complete.

**Example**:

```
!archive /path/to/directory
```

### `!select_dataset <path_to_dir_positive> <positive>`

**Purpose**: Selects a dataset for training from the specified directory.  

**Parameters**:

- **`<path_to_dir_positive>`**: Path to the directory containing positive training data.
- **`<positive>`**: Indicates whether the data in the directory is positive.

**Returns**:  A confirmation message indicating the dataset has been selected.

**Example**:

```
!select_dataset /path/to/positive_data true
```

### `!instruction`

**Purpose**:  Displays this instruction message.

**Parameters**: None.

**Returns**:  The current set of bot instructions.

**Example**:

```
!instruction
```

## Examples of Use

**Example 1: Training the model with a file attachment**

```
!train attachment.txt
```

**Example 2: Testing the model with JSON data**

```
!test test_data.json
```

**Example 3: Archiving files in a directory**

```
!archive /path/to/directory
```

## Conclusion

This instruction set provides a comprehensive overview of the Chat GPT Node.js bot's commands and their usage within the `hypotez` project.  It serves as a valuable resource for developers seeking to leverage the bot's capabilities for natural language processing tasks.