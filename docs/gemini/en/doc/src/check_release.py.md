# Module Name

## Overview

The `check_release.py` module is designed to verify the latest release version of a GitHub repository. It interacts with the GitHub API to fetch information about the most recent release and returns the version tag. This module is essential for applications needing to stay updated with the latest versions of software or libraries hosted on GitHub.

## More details

This module provides a function, `check_latest_release`, that takes the repository owner and name as input, constructs an API request to GitHub, and retrieves the latest release tag. It handles HTTP responses, extracts the tag name, and logs errors if fetching fails. The module uses the `requests` library to make HTTP requests and the `logger` from the `src.logger` module for logging errors.

## Classes

There are no classes defined in this module.

## Functions

### `check_latest_release`

```python
def check_latest_release(repo: str, owner: str):
    """Check the latest release version of a GitHub repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        str: The latest release version if available, else None.
    """
```

**Purpose**: This function checks the latest release version of a specified GitHub repository.

**Parameters**:
- `repo` (str): The name of the repository.
- `owner` (str): The owner (username or organization) of the repository.

**Returns**:
- `str`: The latest release version tag if available.
- `None`: If the request fails or if there are any errors.

**How the function works**:
1. The function constructs a URL to the GitHub API endpoint for retrieving the latest release of the specified repository.
2. It makes an HTTP GET request to the constructed URL using the `requests` library.
3. It checks the HTTP status code of the response:
   - If the status code is 200 (OK), it parses the JSON response to extract the `tag_name` (which represents the latest release version).
   - If the status code is not 200, it logs an error message with the status code and returns `None`.

**Examples**:

```python
from src.check_release import check_latest_release
from src.logger.logger import logger

# Пример вызова функции для репозитория "google/gson"
repo_name = "gson"
repo_owner = "google"
latest_version = check_latest_release(repo_name, repo_owner)

if latest_version:
    logger.info(f"Latest release version of {repo_owner}/{repo_name}: {latest_version}")
else:
    logger.error(f"Could not retrieve the latest release version of {repo_owner}/{repo_name}")