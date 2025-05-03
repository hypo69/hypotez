## \file /src/check_release.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
```rst
.. module:: src 
	:platform: Windows, Unix
	:synopsis:
```
Модуль проверки актуальной версии
==================================

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
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            latest_release = response.json()
            print(latest_release)
            return latest_release['tag_name']
        except Exception as ex:
            logger.error(f'Ошибка распаковки релиза', ex)
            ...
            return
    else:
        logger.warning(f"Нет нового релиза: {url}\n {response.status_code=}", None, False)
        #TODO: Код не проверен
        return 

