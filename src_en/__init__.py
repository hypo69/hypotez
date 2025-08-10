## \file /src/__init__.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src
    :platform: Windows, Unix
    :synopsis: Root of the project.

Root of the project.
========================================================================================
•	USE_ENV:bool: A variable that determines where to read secrets: API keys, etc.
•	If USE_ENV is True, the `gs` module will be imported from `gs.py`, and secrets will be read from `.env` files.
•	If USE_ENV is False, the `gs` module will be imported from `credentials.py`, and secrets will be read from the `gs` object (e.g., `token = gs.path.telegram.kazarinov_bot`).

Example usage
-------------

```python
    from src import gs, USE_ENV

    if USE_ENV:
        print("Using .env files for secrets.")
    else:
        print("Using credentials.py for secrets.")

    print(f"Telegram bot token path: {gs.path.telegram.kazarinov_bot}")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/__init__.py
"""

from .check_release import check_latest_release

USE_ENV:bool = False

if USE_ENV:
	from .gs import gs
else:
	from .credentials import gs

if check_latest_release(gs.git, gs.git_user):
            ...  # Logic for what to do when there is a new version of hypo69 on github
