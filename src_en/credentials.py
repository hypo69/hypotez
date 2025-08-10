## \file /src/credentials.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Module credentials
====================
The credentials module is designed to store global project settings such as paths, passwords, logins, and API parameters.
It uses the Singleton pattern to ensure a single instance of settings throughout the application's runtime.


Documentation:
 - kepass: `https://github.com/hypo69/hypotez/blob/master/src/keepass.md`
 - ProgramSettings: `https://github.com/hypo69/hypotez/blob/master/src/credentials.md#programsettings`
```rst
.. module:: src.header
```
"""

import datetime
from datetime import datetime
import getpass
import os
import sys
import json
import warnings
import socket
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List, Dict

from pykeepass import PyKeePass

import header
from header import __root__
#from src.check_release import check_latest_release
from src.logger.logger import logger
from src.logger.exceptions import (
    CredentialsError,
    DefaultSettingsException,
    HeaderChecksumError,
    KeePassException,
    PayloadChecksumError,
    UnableToSendToRecycleBin,
)

from src.utils.jjson import j_loads, j_loads_ns
from src.utils.printer import pprint as print



def singleton(cls):
    """Decorator for implementing Singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
@dataclass
class ProgramSettings:
    """ 
    `ProgramSettings` - program settings class. 
    
    Singleton storing main project parameters and settings.
    """
    host_name: str = field(default_factory=lambda: socket.gethostname())
    config: SimpleNamespace = field(default_factory=lambda: SimpleNamespace())

    # ---------------------------------- Keys, passwords, APIs ---------------------
    credentials: SimpleNamespace = field(default_factory=lambda: SimpleNamespace(
        aliexpress=SimpleNamespace(
            api_key = None,
            secret = None,
            tracking_id = None,
            username = None,
            email = None,
            password = None
        ),
        prestashop=SimpleNamespace(
            client=SimpleNamespace(
                server = None,
                port = None,
                database = None,
                user = None,
                password = None,
            )
        ),
        openai=SimpleNamespace(
            owner = SimpleNamespace(
                api_key = None,
                assistants = [SimpleNamespace()],
                project_api = None
            )
        ),

        gemini=SimpleNamespace(owner = SimpleNamespace(api_key = None)),

        rev_com=SimpleNamespace(owner = SimpleNamespace(client_api = None,
                                user_api = None)),

        google_custom_search=SimpleNamespace(owner = SimpleNamespace(api_key = None,
                        cse_id = None)),


        shutter_stock=SimpleNamespace(owner = SimpleNamespace(token = None)),

        discord=SimpleNamespace(
                owner = SimpleNamespace(
                    email = None,
                    port = None,
                    receiver = None,
                    server = None,
                )),

        telegram=SimpleNamespace(bot = SimpleNamespace()),

        serpapi=SimpleNamespace(owner = SimpleNamespace(api_key = None,)),
        smtp=SimpleNamespace(
            owner = SimpleNamespace(
                api_key = None,
                assistants = [SimpleNamespace()],
                project_api = None
            )
        ),

        # facebook = SimpleNamespace(
        #     owner = SimpleNamespace(
        #         api_key = None,
        #         assistants = [SimpleNamespace()],
        #         project_api = None
        #     )
        # ),

        gapi = SimpleNamespace(owner = SimpleNamespace(api_key = None,)),
    ))
    # ------------------------------------ paths ---------------------------------
    path: SimpleNamespace = field(default_factory=lambda: SimpleNamespace(
        root = None,
        src = None,
        bin = None,
        log = None,
        tmp = None,
        data = None,
        secrets = None,
        google_drive = None,
        external_storage = None,
        tools = None,
        dev_null ='nul' if sys.platform == 'win32' else '/dev/null'
    ))
    host:str = field(default='')
    git:str = field(default='')
    git_user:str = field(default='')
    current_release:str = field(default='')

    def __post_init__(self):
        """Performs initialization after class instance creation."""
        self.config = j_loads_ns(__root__ / 'src' / 'config.json')
        if not self.config:
            logger.error('Error loading settings')
            ...
            sys.exit()
        self.config.timestamp_format = getattr(self.config, 'timestamp_format', '%y_%m_%d_%H_%M_%S_%f')
        self.config.project_name = __root__.name
        self.host = getattr( self.config,'host', '0.0.0.0')
        self.git = getattr( self.config,'git', 'hypo')
        self.git_user = getattr( self.config,'git_user', 'hypo69')
        self.current_release = getattr( self.config,'current_release', '')
        self.path:SimpleNamespace = SimpleNamespace(
            root = Path(__root__),
            bin = Path(__root__ / 'bin'), # <- binaries here (chrome, firefox, ffmpeg, ...)
            src = Path(__root__) / 'src', # <- all code here
            endpoints = Path(__root__) / 'src' / 'endpoints', # <- all clients here
            secrets = Path(__root__ / 'secrets'),  # <- this folder contains passwords and database! It must not be committed to git!!!

            toolbox = Path(__root__ / 'toolbox'), # <- utility tools
            log = Path( getattr(self.config.path, 'log', __root__ / 'log')),
            tmp = Path( getattr(self.config.path, 'tmp', __root__ / 'tmp')),
            data = Path( getattr(self.config.path, 'data', __root__ / 'data')), # <- data from endpoints (hypo69, kazarinov, prestashop, etc ...)
            google_drive = Path( getattr(self.config.path, 'google_drive', __root__ / 'google_drive')), # <- GOOGLE DRIVE VIA LOCAL DISK (NOT API)
            external_storage = Path(getattr(self.config.path, 'external_storage',  __root__ / 'external_storage') ), # <- External disk
        )

        # Paths to bin directories
        gtk_bin_dir = self.path.bin  / 'gtk' / 'gtk-nsis-pack' / 'bin'
        ffmpeg_bin_dir = __root__  / 'bin' / 'ffmpeg' / 'bin'
        graphviz_bin_dir = __root__  / 'bin' / 'graphviz' / 'bin'
        wkhtmltopdf_bin_dir = __root__  / 'bin' / 'wkhtmltopdf' / 'files' / 'bin'

        for bin_path in [__root__, gtk_bin_dir, ffmpeg_bin_dir, graphviz_bin_dir, wkhtmltopdf_bin_dir]:
            if bin_path not in sys.path:
                sys.path.insert(0, str(bin_path))  # <- define paths to binaries in system paths

        os.environ['WEASYPRINT_DLL_DIRECTORIES'] = str(gtk_bin_dir)

        # Suppress GTK log output to the console
        warnings.filterwarnings("ignore", category=UserWarning)
        self._load_credentials()

    def _load_aliexpress_credentials(self, kp: PyKeePass) -> bool:
        """ Load Aliexpress API credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['suppliers', 'aliexpress', 'api']).entries[0]
            self.credentials.aliexpress_com.api_key = entry.custom_properties.get('api_key', None)
            self.credentials.aliexpress_com.secret = entry.custom_properties.get('secret', None)
            self.credentials.aliexpress_com.tracking_id = entry.custom_properties.get('tracking_id', None)
            self.credentials.aliexpress_com.username = entry.custom_properties.get('username', None)
            self.credentials.aliexpress_com.email = entry.custom_properties.get('email', None)
            self.credentials.aliexpress_com.password = entry.password
            return True
        except Exception as ex:
            print(f"Failed to extract Aliexpress API key from KeePass {ex}" )
            ...
            return False

    def _load_credentials(self) -> None:
        """ Loads credentials from settings."""

        kp = self._open_kp(3)
        if not kp:
            print("Error :(" )
            ...
            sys.exit(1)

        if not self._load_aliexpress_credentials(kp):
            print('Failed to load Aliexpress credentials')

        if not self._load_openai_credentials(kp):
            print('Failed to load OpenAI credentials')

        if not self._load_gemini_credentials(kp):
            print('Failed to load GoogleAI credentials')

        if not self._load_google_custom_search_credentials(kp):
            print('Failed to load GoogleAI credentials')

        if not self._load_discord_credentials(kp):
            print('Failed to load Discord credentials')

        if not self._load_telegram_credentials(kp):
            print('Failed to load Telegram credentials')

        if not self._load_prestashop_credentials(kp):
            print('Failed to load prestashop credentials')

        if not self._load_smtp_credentials(kp):
            print('Failed to load SMTP credentials')

        # if not self._load_facebook_credentials(kp):
        #     print('Failed to load Facebook credentials')

        if not self._load_gapi_credentials(kp):
            print('Failed to load GAPI credentials')

        if not self._load_serpapi_credentials(kp):
            print('Failed to load https://serpapi.com credentials')

    def _load_discord_credentials(self, kp: PyKeePass) -> bool:
        """ Load Discord credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:

            for entry in kp.find_groups(path=['discord']).entries:
                setattr(self.credentials.discord, entry.title, SimpleNamespace())
                _entry = getattr(self.credentials.discord, entry.title)
                setattr(_entry, 'application_id', entry.custom_properties.get('application_id', None))
                setattr(_entry, 'public_key', entry.custom_properties.get('public_key', None))
                setattr(_entry, 'bot_token', entry.custom_properties.get('bot_token', None))
        except Exception as ex:
            raise ValueError(f'failed sets: `discord` credentianals {ex}')
        return True


    def _load_facebook_credentials(self, kp: PyKeePass) -> bool:
        """ Load Facebook credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['facebook']).entries:
                setattr(self.credentials.facebook, entry.title, SimpleNamespace())
                _entry = getattr(self.credentials.facebook, entry.title)
                setattr(_entry, 'api_id', entry.custom_properties.get('api_id', None))
                setattr(_entry, 'app_secret', entry.custom_properties.get('app_secret', None))
                setattr(_entry, 'access_token', entry.custom_properties.get('access_token', None))
                return True
        except Exception as ex:
            raise ValueError(f'failed sets: `facebook` credentianals {ex}')


    def _load_gapi_credentials(self, kp: PyKeePass) -> bool:
        """ Load Google API credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['google','gapi']).entries:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.gapi, entry.title, entry_ns)
                _entry = getattr(self.credentials.gapi, entry.title)
                setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))

        except Exception as ex:
            raise ValueError(f'failed sets: `gemini` credentianals {ex}')


    def _load_gemini_credentials(self, kp: PyKeePass) -> bool:
        """ Load GoogleAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['gemini']).entries:
                    entry_ns = SimpleNamespace()
                    setattr(self.credentials.gemini, entry.title, entry_ns)
                    _entry = getattr(self.credentials.gemini, entry.title)
                    setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))

            return True
        except Exception as ex:
            raise ValueError(f'failed sets: `gemini` credentianals {ex}')


    def _load_google_custom_search_credentials(self, kp: PyKeePass) -> bool:
        """ Load OpenAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['google','google_custom_search']).entries:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.google_custom_search, entry.title, entry_ns)
                _entry = getattr(self.credentials.google_custom_search, entry.title)
                setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
                setattr(_entry, 'cse_id', entry.custom_properties.get('cse_id', None))

            return True
        except Exception as ex:
            raise ValueError(f'failed sets: `google_custom_search` credentianals {ex}')

    def _load_openai_credentials(self, kp: PyKeePass) -> bool:
        """ Load OpenAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            assistants:list = kp.find_groups(path=['openai','assistants']).entries

            for entry in kp.find_groups(path=['openai']).entries:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.openai, entry.title, entry_ns)
                _entry = getattr(self.credentials.openai, entry.title)
                setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
                setattr(_entry, 'project_api', entry.custom_properties.get('project_api', None))
                return True
        except Exception as ex:
            raise ValueError(f'failed sets: `openai` credentianals \n{ex}')


    def _load_prestashop_credentials(self, kp: PyKeePass) -> bool:
        """ Load prestashop credentials from KeePass
        Args:
        kp (PyKeePass): The KeePass database instance.
        Returns:
        bool: True if loading was successful, False otherwise.
        """
        # It's generally better to return True outside the loop after all entries are processed.
        # If any entry fails, it should probably return False immediately or collect errors.
        # Following the original pattern, we return True at the end.
        try:
            for entry in kp.find_groups(path=['prestashop']).entries:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.prestashop, entry.title, entry_ns)
                _entry = getattr(self.credentials.prestashop, entry.title)

                setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
                setattr(_entry, 'api_domain', entry.custom_properties.get('api_domain', None))
                setattr(_entry, 'db_server', entry.custom_properties.get('db_server', None))
                setattr(_entry, 'db_user', entry.custom_properties.get('db_user', None))
                setattr(_entry, 'db_password', entry.custom_properties.get('db_password', None))
            return True
        except Exception as ex:
            raise ValueError(f'failed sets: `prestashop` credentianals \n{ex}')

    def _load_serpapi_credentials(self, kp: PyKeePass) -> bool:
        """ Load serpapi.com credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['serpapi.com']).entries:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.serpapi, entry.title, entry_ns)
                _entry = getattr(self.credentials.serpapi, entry.title)
                setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
            return True
        except Exception as ex:
            # Error finding the 'tavily' group itself
            raise ValueError('failed sets: `serpapi` credentianals ')

    def _load_smtp_credentials(self, kp: PyKeePass) -> bool:
        """ Load SMTP credentials from KeePass
        Args:
        kp (PyKeePass): The KeePass database instance.

        Returns:
        bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['smtp']).entries:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.smtp, entry.title, entry_ns)
                _entry = getattr(self.credentials.smtp, entry.title)
                setattr(_entry, 'email', entry.custom_properties.get('email', None))
                setattr(_entry, 'password', entry.password )
                setattr(_entry, 'server', entry.custom_properties.get('server', None))
                setattr(_entry, 'port', entry.custom_properties.get('port', None))
                setattr(_entry, 'receiver', entry.custom_properties.get('receiver', None))
            return True

        except Exception as ex:
            raise ValueError(f'failed sets: `smtp` credentianals \n{ex}')


    def _load_tavily_credentials(self, kp: PyKeePass) -> bool:
        """ Load Tavily credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:

            for entry in kp.find_groups(path=['tavily']).entries:
                    # Assuming each entry title corresponds to a sub-namespace (like 'owner')
                    entry_ns = SimpleNamespace()
                    setattr(self.credentials.tavily, entry.title, entry_ns)
                    _entry_ns_ref = getattr(self.credentials.tavily, entry.title)
                    setattr(_entry_ns_ref, 'api_key', entry.custom_properties.get('api_key', None))
            return True #
        except Exception as ex:
            raise ValueError(f'failed sets: `travility` credentianals \n{ex}')

    def _load_telegram_credentials(self, kp: PyKeePass) -> bool:
        """Load Telegram credentials from KeePass.

        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['telegram']).entries:
                    # Assuming each entry title corresponds to a sub-namespace (like 'owner')
                    entry_ns = SimpleNamespace()
                    setattr(self.credentials.telegram, entry.title, entry_ns)
                    _entry_ns_ref = getattr(self.credentials.telegram, entry.title)
                    setattr(_entry_ns_ref, 'token', entry.custom_properties.get('token', None))
            return True #
        except Exception as ex:
            raise ValueError(f'failed sets: `telegram` credentianals \n{ex}')


    def _open_kp(self, retry: int = 3) -> PyKeePass | None:
        """ Open KeePass database
        Args:
            retry (int): Number of retries
        """
        password:str = ''
        password_file = Path( self.path.secrets / 'password.txt')
        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~ ⚠️ PASSWORD FILE IN PLAIN TEXT ⚠️ ~~~~~~~~~~~~~~~~~~~~~~~ 
            if password_file.exists():
                password = password_file.read_text(encoding="utf-8").strip() or None
                if password:
                    print("🔑 Found password in password.txt (DEBUG MODE)")
                else:
                     print("ℹ️ password.txt exists but is empty.")
            """password: contains the password string in ⚠️ plain text ⚠️. You can delete the file itself or erase its contents """
        except Exception as ex:
            print(f"ℹ️ Could not read password file ({password_file}): {ex}")

        kdbx_path = str(self.path.secrets / 'credentials.kdbx')
        if not Path(kdbx_path).exists():
            logger.critical(f"🚨 KeePass database file not found at: {kdbx_path}")
            sys.exit(-1)


        while retry > 0:
                try:
                    # Only prompt if password wasn't read from file
                    if not password:
                        prompt_message = f'🔐 Enter KeePass master password for {kdbx_path}: '
                        password_input = getpass.getpass(prompt=prompt_message)
                        if not password_input: # Handle empty input
                            print("⛔ Password cannot be empty.")
                            retry -=1
                            if retry > 0: continue
                            else: break # Exit loop if retries exhausted
                        password = password_input # Use the entered password

                    kp = PyKeePass(kdbx_path, password=password)
                    print(f"✅ Successfully opened KeePass database: {kdbx_path}")
                    # Clear password from memory after use if it came from input
                    if 'password_input' in locals():
                        del password_input
                        password = '' # Clear the variable too
                    return kp

                except Exception as ex: # More specific exception? e.g., pykeepass.exceptions.CredentialsError
                    retry -= 1
                    print(f"😔 Failed to open KeePass database. Exception: {ex}\n {retry} retries left.")
                    password = '' # Clear potentially incorrect password to force re-prompt or exit

                    if retry > 0: continue
                    else: break # Exit loop

        # If loop finishes without returning kp
        logger.critical(f'🚨 Failed to open KeePass database ({kdbx_path}) after multiple attempts')
        sys.exit(-1) # Exit the program

    @property
    def now(self) -> str:
        """Returns the current timestamp in year-month-day-hour-minute-second-millisecond format.

        This method returns a string representing the current timestamp in the format `year_month_day_hour_minute_second_millisecond`.

        Args:
            dformat (str, optional): Format for the timestamp. Defaults to `'%y_%m_%d_%H_%M_%S_%f'`.

        Returns:
            str: The current timestamp in string format.
        """
        timestamp = datetime.now().strftime(self.config.timestamp_format)
        # Return only the first 3 digits of milliseconds, as %f returns microseconds (6 digits)
        return f"{timestamp[:-3]}"


# Global instance of ProgamSettings
gs: ProgramSettings = ProgramSettings()
