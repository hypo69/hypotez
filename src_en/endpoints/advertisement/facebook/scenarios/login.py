# # \file /src/endpoints/advertisement/facebook/scenarios/login.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.endpoints.advertisement.facebook.scenarios 
	:platform: Windows, Unix
	:synopsis: Facebook login scenario"""


from pathlib import Path
from typing import Dict
from src import gs
from src.webdriver.selenium.driver import Driver
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.logger.logger import logger

# Loading locators for Facebook authorization
locators = j_loads_ns(
            Path(gs.path.src / 'endpoints' / 'advertisement' / 'facebook' / 'locators' / 'login.json'))
if not locators:
    logger.debug(f"Ошибка в файле локаторов")
    ...

def login(d: Driver) -> bool:
    """Enters Facebook.

    The function uses the transmitted `driver` to perform authorization on Facebook, filling out
    Login and password, and then presses the entrance button.

    Args:
        D (Driver): a copy of the driver for interaction with web elements.

    Returns:
        Bool: `true`, if the authorization was successful, otherwise` false`.

    RAISES:
        Exception: If there is an error when entering a login, password or pressing a button."""
    credentials = gs.facebook_credentials[0]
    try:
        # Entering the login
        d.send_key_to_webelement(locators.email, credentials.username)
    except Exception as ex:
        logger.error("Invalid login", ex)
        return False

    d.wait(1.3)
    try:
        # Password entering
        d.send_key_to_webelement(locators['password'], credentials['password'])
    except Exception as ex:
        logger.error("Invalid login", ex)
        return False

    d.wait(0.5)
    try:
        # Pressing the entrance button
        d.execute_locator(locators['button'])
    except Exception as ex:
        logger.error("Invalid login", ex)
        return False

    return True
