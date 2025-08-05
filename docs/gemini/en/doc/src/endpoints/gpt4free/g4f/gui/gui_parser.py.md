# GUI Parser

## Overview

This module provides a function for parsing command-line arguments for the GUI application.

## Details

The `gui_parser()` function creates an `ArgumentParser` object and adds various command-line arguments for customizing the GUI's behavior.

## Functions

### `gui_parser`

**Purpose**: Creates an `ArgumentParser` object and adds arguments for controlling the GUI.

**Parameters**: None

**Returns**:
- `ArgumentParser`: The `ArgumentParser` object configured with GUI-specific arguments.

**How the Function Works**:
- Creates an `ArgumentParser` object with the description "Run the GUI".
- Adds arguments for the following:
    - `--host`: The hostname for the server. Defaults to "0.0.0.0".
    - `--port`: The port for the server. Defaults to 8080.
    - `--debug`: Enables debug mode.
    - `--ignore-cookie-files`: Prevents reading cookie files.
    - `--ignored-providers`: Specifies a list of providers to ignore.
    - `--cookie-browsers`: Specifies a list of browsers to access or retrieve cookies from.
- Returns the configured `ArgumentParser` object.

**Examples**:

```python
# Parsing arguments with default values
parser = gui_parser()
args = parser.parse_args()
print(args)
# Output: Namespace(debug=False, host='0.0.0.0', ignore_cookie_files=False, ignored_providers=[], port=8080, cookie_browsers=[])

# Parsing arguments with custom values
parser = gui_parser()
args = parser.parse_args(["--host", "127.0.0.1", "--port", "8081", "--debug", "--ignore-cookie-files", "--ignored-providers", "Google", "Bing"])
print(args)
# Output: Namespace(debug=True, host='127.0.0.1', ignore_cookie_files=True, ignored_providers=['Google', 'Bing'], port=8081, cookie_browsers=[])
```