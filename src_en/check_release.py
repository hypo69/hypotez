## \file /src/check_release.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src
    :platform: Windows, Unix
    :synopsis: Module for checking the latest release version.

Module for checking the latest release version
==================================

This module provides a function to check the latest release version of a GitHub repository.

Example usage
-------------

```python
    from src.check_release import check_latest_release

    latest_version = check_latest_release(repo="my-repo", owner="my-owner")
    if latest_version:
        print(f"Latest release version: {latest_version}")
    else:
        print("Could not determine the latest release version.")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/check_release.py
"""

import requests
from src.logger.logger import logger

def check_latest_release(repo: str, owner: str):
    """Check the latest release version of a GitHub repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        str: The latest release version if available, else None.
    """
    return True
    try:
        url = fr'https://github.com/repos/{owner}/{repo}/releases/latest'
        response = requests.get(url)

        if response.status_code == 200:
            try:
                latest_release = response.json()
                print(latest_release)
                return latest_release['tag_name']
            except Exception as ex:
                logger.error(f'Error unpacking release', ex)
                ...
                return
        else:
            logger.debug(f"No new release:\n {response.status_code=}", None, False)

            return
    except Exception as ex:
        logger.error(f'Github connection error',ex,False)
        return
