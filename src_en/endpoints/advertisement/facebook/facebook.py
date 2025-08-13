
# # \file /src/endpoints/advertisement/facebook/facebook.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: SRC.endpoints.Advertisement.Facebook 
    : Platform: Windows, Unix
    : synopsis: Facebook advertising module

 Scenarios:
    - Login: Facebook login
    - Post_Message: Sending text messages to the form 
    - upload_Media: uploading a file or file list"""


import os, sys
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, List

from src import gs
from src.utils.jjson import j_loads, j_dumps
from src.utils.printer import pprint
from src.logger.logger import logger
from .scenarios.login import login
from .scenarios import  switch_account, promote_post,  post_title, upload_media, update_images_captions


class Facebook():
    """The class communicates with the Feibuet through the webdraiter"""
    d: 'Driver'  # Strofing annotation type for imprisonment of imports
    start_page: str = r'https://www.facebook.com/hypotez.promocodes'
    promoter: str

    def __init__(self, driver: 'Driver', promoter: str, group_file_paths: list[str], *args, **kwargs):
        """I can convey the already neglected instance of the driver. For example, from Aliexpress
        @Todo:
            - Add a check on which page Facebook opened. If the login page has opened, the script of the login executed"""
        self.d = driver
        self.promoter = promoter
        ...
        
        # self.driver.get_url (self.start_page)
        # switch_account (self.driver) # <- switching the profile, if not on your page

    def login(self) -> bool:
        return login(self)

    def promote_post(self, item: SimpleNamespace) -> bool:
        """The function sends the text to the message form 
        @param Message: Text message. Signs `;` will replace with `shift+enter`
        @returns `true`, if successful, otherwise` false`"""
        ...
        return promote_post(self.d, item)
    
    def promote_event(self, event: SimpleNamespace):
        """An example of a function for promoting an event"""
        ...
