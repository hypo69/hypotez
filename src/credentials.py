## \file /src/credentials.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль credentials
====================
Модуль credentials предназначен для хранения глобальных настроек проекта, таких как пути, пароли, логины и параметры API. 
Он использует паттерн Singleton для обеспечения единственного экземпляра настроек в течение всего времени работы приложения.


Документация: 
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
    """Декоратор для реализации Singleton."""
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
    `ProgramSettings` - класс настроек программы.
    
    Синглтон, хранящий основные параметры и настройки проекта.
    """
    host_name: str = field(default_factory=lambda: socket.gethostname())
    config: SimpleNamespace = field(default_factory=lambda: SimpleNamespace())

    # ---------------------------------- Ключи, пароли, апи ---------------------
    credentials: SimpleNamespace = field(default_factory=lambda: SimpleNamespace(
        aliexpress=SimpleNamespace(
            api_key = None,
            secret = None,
            tracking_id = None,
            username = None,
            email = None,
            password = None
        ),
        presta=SimpleNamespace(
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
                        sce_id = None)),


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
    # ------------------------------------ пути ---------------------------------
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
        """Выполняет инициализацию после создания экземпляра класса."""
        self.config = j_loads_ns(__root__ / 'src' / 'config.json')
        if not self.config:
            logger.error('Ошибка при загрузке настроек')
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
            bin = Path(__root__ / 'bin'), # <- тут бинарники (chrome, firefox, ffmpeg, ...)
            src = Path(__root__) / 'src', # <- тут весь код
            endpoints = Path(__root__) / 'src' / 'endpoints', # <- тут все клиенты
            secrets = Path(__root__ / 'secrets'),  # <- это папка с паролями и базой данных ! Ей нельзя попадать в гит!!!

            toolbox = Path(__root__ / 'toolbox'), # <- служебные утилиты
            log = Path( getattr(self.config.path, 'log', __root__ / 'log')), 
            tmp = Path( getattr(self.config.path, 'tmp', __root__ / 'tmp')),
            data = Path( getattr(self.config.path, 'data', __root__ / 'data')), # <- дата от endpoints (hypo69, kazarinov, prestashop, etc ...)
            google_drive = Path( getattr(self.config.path, 'google_drive', __root__ / 'google_drive')), # <- GOOGLE DRIVE ЧЕРЕЗ ЛОКАЛЬНЫЙ ДИСК (NOT API) 
            external_storage = Path(getattr(self.config.path, 'external_storage',  __root__ / 'external_storage') ), # <- Внешний диск 
        )
    
        # Paths to bin directories
        gtk_bin_dir = self.path.bin  / 'gtk' / 'gtk-nsis-pack' / 'bin'
        ffmpeg_bin_dir = __root__  / 'bin' / 'ffmpeg' / 'bin'
        graphviz_bin_dir = __root__  / 'bin' / 'graphviz' / 'bin'
        wkhtmltopdf_bin_dir = __root__  / 'bin' / 'wkhtmltopdf' / 'files' / 'bin'

        for bin_path in [__root__, gtk_bin_dir, ffmpeg_bin_dir, graphviz_bin_dir, wkhtmltopdf_bin_dir]:
            if bin_path not in sys.path:
                sys.path.insert(0, str(bin_path))  # <- определяю пути к бунарникам в системных путях

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
            self.credentials.aliexpress.api_key = entry.custom_properties.get('api_key', None)
            self.credentials.aliexpress.secret = entry.custom_properties.get('secret', None)
            self.credentials.aliexpress.tracking_id = entry.custom_properties.get('tracking_id', None)
            self.credentials.aliexpress.email = entry.custom_properties.get('email', None)
            self.credentials.aliexpress.password = entry.password
            return True
        except Exception as ex:
            print(f"Failed to extract Aliexpress API key from KeePass {ex}" )
            ...
            return False

    def _load_credentials(self) -> None:
        """ Загружает учетные данные из настроек."""

        kp = self._open_kp(3)
        if not kp:
            print("Error :( ")
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
            raise ValueError(f'failed sets: `discord` credentionals {ex}')
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
            raise ValueError(f'failed sets: `facebook` credentionals {ex}')


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
            raise ValueError(f'failed sets: `gemini` credentionals {ex}')


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
            raise ValueError(f'failed sets: `gemini` credentionals {ex}')


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
                setattr(_entry, 'sce_id', entry.custom_properties.get('sce_id', None))
      
            return True
        except Exception as ex:
            raise ValueError(f'failed sets: `google_custom_search` credentionals {ex}')

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
            raise ValueError(f'failed sets: `openai` credentionals \n{ex}')


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
            for entry in kp.find_groups(path=['prestashop', 'clients']).entries:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.presta.client, entry.title, entry_ns)
                _entry = getattr(self.credentials.presta.client, entry.title)

                setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
                setattr(_entry, 'api_domain', entry.custom_properties.get('api_domain', None))
                setattr(_entry, 'db_server', entry.custom_properties.get('db_server', None))
                setattr(_entry, 'db_user', entry.custom_properties.get('db_user', None))
                setattr(_entry, 'db_password', entry.custom_properties.get('db_password', None))
            return True 
        except Exception as ex:
            raise ValueError(f'failed sets: `gemini` credentionals \n{ex}')

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
            raise ValueError('failed sets: `serpapi` credentionals ')

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
            raise ValueError(f'failed sets: `smtp` credentionals \n{ex}')
            

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
            raise ValueError(f'failed sets: `travility` credentionals \n{ex}')

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
            raise ValueError(f'failed sets: `telegram` credentionals \n{ex}')


    def _open_kp(self, retry: int = 3) -> PyKeePass | None:
        """ Open KeePass database
        Args:
            retry (int): Number of retries
        """
        password:str = ''
        password_file = Path( self.path.secrets / 'password.txt')
        try:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~ ⚠️ ФАЙЛ ПАРОЛЯ В ОТКРЫТОМ ВИДЕ ⚠️ ~~~~~~~~~~~~~~~~~~~~~~~
            if password_file.exists():
                password = password_file.read_text(encoding="utf-8").strip() or None
                if password:
                    print("🔑 Found password in password.txt (DEBUG MODE)")
                else:
                     print("ℹ️ password.txt exists but is empty.")
            """password: содержит строку пароля в ⚠️ открытом ⚠️ виде. Можно удалить или сам файл или вытереть его содржимое """
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
        """Возвращает текущую метку времени в формате год-месяц-день-часы-минуты-секунды-милисекунды.

        Этот метод возвращает строку, представляющую текущую метку времени, в формате `год_месяц_день_часы_минуты_секунды_миллисекунды`.
    
        Args:
            dformat (str, optional): Формат для метки времени. По умолчанию `'%y_%m_%d_%H_%M_%S_%f'`.
        
        Returns:
            str: Текущая метка времени в строковом формате.
        """
        timestamp = datetime.now().strftime(self.config.timestamp_format)
        # Вернём только первые 3 цифры миллисекунд, т.к. %f возвращает микросекунды (6 цифр)
        return f"{timestamp[:-3]}"


# Global instance of ProgamSettings
gs: ProgramSettings = ProgramSettings()

