# Module for checking the latest release version
## Overview

This module provides a function for checking the latest release version of a GitHub repository. The `check_latest_release` function utilizes the GitHub API to retrieve information about the latest release and returns the tag name.

## Details
The module utilizes the GitHub API to retrieve information about the latest release. It checks the status code of the response and if successful, extracts the tag name from the JSON response. If there are any issues, the module logs an error message and returns None.

## Functions
### `check_latest_release`
**Purpose**:  Проверяет последнюю версию релиза репозитория GitHub.

**Parameters**:
- `repo` (str): Имя репозитория.
- `owner` (str): Владелец репозитория.

**Returns**:
- `str`: Тег последней версии, если она доступна; иначе None.

**Raises Exceptions**:
- `None`

**How the Function Works**:
- The function constructs the URL for the GitHub API endpoint that provides information about the latest release of the specified repository.
- It uses the `requests` library to send a GET request to the API endpoint.
- The function checks the status code of the response. If the status code is 200 (successful), it attempts to parse the JSON response and extract the tag name (`tag_name`).
- If there is an error parsing the JSON response, the function logs an error message and returns None.
- If the status code is not 200, the function logs a warning message and returns None.

**Examples**:

```python
from src.check_release import check_latest_release

# Get the latest release version for the "hypotez" repository owned by "hypotez-dev"
latest_release_version = check_latest_release(repo="hypotez", owner="hypotez-dev")

# Print the latest release version
print(f"Latest release version: {latest_release_version}")
```

**Inner Functions**:
- None