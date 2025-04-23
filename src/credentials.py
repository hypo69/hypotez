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
 - ProgramSettings: `https://github.com/hypo69/hypotez/blob/master/src/credentials.md`
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

def set_project_root(marker_files=('__root__','.git')) -> Path:
    """
    Finds the root directory of the project starting from the current file's directory,
    searching upwards and stopping at the first directory containing any of the marker files.
    

    Args:
        marker_files (tuple): Filenames or directory names to identify the project root.
    
    Returns:
        Path: Path to the root directory if found, otherwise the directory where the script is located.
    """
    __root__:Path
    current_path:Path = Path(__file__).resolve().parent
    __root__ = current_path
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            __root__ = parent
            break
    if __root__ not in sys.path:
        sys.path.insert(0, str(__root__))
    return __root__

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
    host_name:str = field(default_factory=lambda: socket.gethostname())
    
    base_dir: Path = field(default_factory=lambda: set_project_root())
    config: SimpleNamespace = field(default_factory=lambda: SimpleNamespace())
    credentials: SimpleNamespace = field(default_factory=lambda: SimpleNamespace(
        aliexpress=SimpleNamespace(
            api_key=None,
            secret=None,
            tracking_id=None,
            username=None,
            email=None,
            password=None
        ),
        presta=SimpleNamespace(
            client=SimpleNamespace(
                server=None,
                port=None,
                database=None,
                user=None,
                password=None,
            )
        ),
        openai=SimpleNamespace(
            owner = SimpleNamespace(
            api_key=None, 
            assistants= [SimpleNamespace()], 
            project_api=None
            )
        ),

        gemini=SimpleNamespace(owner = SimpleNamespace(api_key=None)),

        rev_com=SimpleNamespace(owner = SimpleNamespace(client_api=None,
                                user_api=None)),

        shutter_stock=SimpleNamespace(owner = SimpleNamespace(token=None)),

        discord=SimpleNamespace(
                owner = SimpleNamespace(
                application_id=None, 
                public_key=None, 
                bot_token=None)
        ),

        telegram=SimpleNamespace(
            bot=SimpleNamespace()
        ),

        serpapi=SimpleNamespace(owner = SimpleNamespace(api_key=None,)),
        smtp=[],
        facebook=[],
        gapi={}
    ))
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
        self.config = j_loads_ns(self.base_dir / 'src' / 'config.json')
        if not self.config:
            logger.error('Ошибка при загрузке настроек')
            ...
            sys.exit()
        self.config.timestamp_format = getattr(self.config, 'timestamp_format', '%y_%m_%d_%H_%M_%S_%f')
        self.config.project_name = self.base_dir.name
        self.host = getattr( self.config,'host', '0.0.0.0')
        self.git = getattr( self.config,'git', 'hypo') 
        self.git_user = getattr( self.config,'git_user', 'hypo69')
        self.current_release = getattr( self.config,'current_release', '')
        self.path:SimpleNamespace = SimpleNamespace(
            root = Path(self.base_dir),
            bin = Path(self.base_dir / 'bin'), # <- тут бинарники (chrome, firefox, ffmpeg, ...)
            src = Path(self.base_dir) / 'src', # <- тут весь код
            endpoints = Path(self.base_dir) / 'src' / 'endpoints', # <- тут все клиенты
            secrets = Path(self.base_dir / 'secrets'),  # <- это папка с паролями и базой данных ! Ей нельзя попадать в гит!!!

            toolbox = Path(self.base_dir / 'toolbox'), # <- служебные утилиты
            log = Path( getattr(self.config.path, 'log', self.base_dir / 'log')), 
            tmp = Path( getattr(self.config.path, 'tmp', self.base_dir / 'tmp')),
            data = Path( getattr(self.config.path, 'data', self.base_dir / 'data')), # <- дата от endpoints (hypo69, kazarinov, prestashop, etc ...)
            google_drive = Path( getattr(self.config.path, 'google_drive', self.base_dir / 'google_drive')), # <- GOOGLE DRIVE ЧЕРЕЗ ЛОКАЛЬНЫЙ ДИСК (NOT API) 
            external_storage = Path(getattr(self.config.path, 'external_storage',  self.base_dir / 'external_storage') ), # <- Внешний диск 
        )



    
        # Paths to bin directories
        gtk_bin_dir = self.path.bin  / 'gtk' / 'gtk-nsis-pack' / 'bin'
        ffmpeg_bin_dir = self.base_dir  / 'bin' / 'ffmpeg' / 'bin'
        graphviz_bin_dir = self.base_dir  / 'bin' / 'graphviz' / 'bin'
        wkhtmltopdf_bin_dir = self.base_dir  / 'bin' / 'wkhtmltopdf' / 'files' / 'bin'

        for bin_path in [self.base_dir, gtk_bin_dir, ffmpeg_bin_dir, graphviz_bin_dir, wkhtmltopdf_bin_dir]:
            if bin_path not in sys.path:
                sys.path.insert(0, str(bin_path))  # <- определяю пути к бунарникам в системных путях

        os.environ['WEASYPRINT_DLL_DIRECTORIES'] = str(gtk_bin_dir)

        # Suppress GTK log output to the console
        warnings.filterwarnings("ignore", category=UserWarning)
        self._load_credentials()
        
        
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

        if not self._load_discord_credentials(kp):
            print('Failed to load Discord credentials')

        if not self._load_telegram_credentials(kp):
            print('Failed to load Telegram credentials')

        if not self._load_prestashop_credentials(kp):
            print('Failed to load prestashop credentials')

        if not self._load_smtp_credentials(kp):
            print('Failed to load SMTP credentials')

        if not self._load_facebook_credentials(kp):
            print('Failed to load Facebook credentials')

        if not self._load_gapi_credentials(kp):
            print('Failed to load GAPI credentials')

        if not self._load_serpapi_credentials(kp):
            print('Failed to load https://serpapi.com credentials')
            

    def _open_kp(self, retry: int = 3) -> PyKeePass | None:
        """ Open KeePass database
        Args:
            retry (int): Number of retries
        """
        while retry > 0:
            try:
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~ ⚠️ ФАЙЛ ПАРОЛЯ В ОТКРЫТОМ ВИДЕ ⚠️ ~~~~~~~~~~~~~~~~~~~~~~~
                password:str = Path( self.path.google_drive / '..' / 'secrets' / 'password.txt').read_text(encoding="utf-8") or None
                """password: содержит строку пароля в ⚠️ открытом ⚠️ виде. Можно удалить или сам файл или вытереть его содржимое """
                
                kp = PyKeePass(str(self.path.secrets / 'credentials.kdbx'), 
                               password = password or getpass.getpass(print('🔐 Enter KeePass master password: ').lower()))
               
                return kp
            except Exception as ex:
                print(f"😔 Failed to open KeePass database Exception: {ex}\n {retry-1} retries left.")
                ...
                retry -= 1
                if retry < 1:
                    logger.critical('🚨 Failed to open KeePass database after multiple attempts', None, False)
                    ...
                    sys.exit()

    # Define methods for loading various credentials
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

    def _load_openai_credentials(self, kp: PyKeePass) -> bool:
        """ Load OpenAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            openai_api_keys = kp.find_groups(path=['openai']).entries
            assistants:list = kp.find_groups(path=['openai','assistants']).entries

            for entry in openai_api_keys:
                try:
                    entry_ns = SimpleNamespace()
                    setattr(self.credentials.openai, entry.title, entry_ns)
                    _entry = getattr(self.credentials.openai, entry.title)
                    setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
                    setattr(_entry, 'project_api', entry.custom_properties.get('project_api', None))
                    return True
                except Exception as ex:
                    logger.error(f"Failed to extract OpenAI API key from KeePass ", ex)
                    ...                 

            return True
        except Exception as ex:
            print(f"Failed to extract OpenAI credentials from KeePass ",ex )
            ...
            return False


    def _load_gemini_credentials(self, kp: PyKeePass) -> bool:
        """ Load GoogleAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        gemini_api_keys = kp.find_groups(path=['gemini']).entries

        for entry in gemini_api_keys:
            try:
                entry_ns = SimpleNamespace()
                setattr(self.credentials.gemini, entry.title, entry_ns)
                _entry = getattr(self.credentials.gemini, entry.title)
                setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
            except Exception as ex:
                print(f"Failed to extract `gemini` credentials from KeePass {ex}")
                ...
                return False
        return True

    def _load_telegram_credentials(self, kp: PyKeePass) -> bool:
        """Load Telegram credentials from KeePass.

        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entries = kp.find_groups(path=['telegram']).entries
            for entry in entries:
                setattr(self.credentials.telegram, entry.title, entry.custom_properties.get('token', None))
            return True
        except Exception as ex:
            print(f"Failed to extract Telegram credentials from KeePass {ex}")
            ...
            return False

    def _load_discord_credentials(self, kp: PyKeePass) -> bool:
        """ Load Discord credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['discord']).entries[0]
            self.credentials.discord.application_id = entry.custom_properties.get('application_id', None)
            self.credentials.discord.public_key = entry.custom_properties.get('public_key', None)
            self.credentials.discord.bot_token = entry.custom_properties.get('bot_token', None)
            return True
        except Exception as ex:
            print(f"Failed to extract Discord credentials from KeePass {ex}")
            ...
            return False

    def _load_prestashop_credentials(self, kp: PyKeePass) -> bool:
         """ Load prestashop credentials from KeePass
         Args:
            kp (PyKeePass): The KeePass database instance.
         Returns:
            bool: True if loading was successful, False otherwise.
         """

         for entry in kp.find_groups(path=['prestashop', 'clients']).entries:
            try:

                client_ns = SimpleNamespace()
        

                setattr(self.credentials.presta.client, entry.title, client_ns)
        

                current_client = getattr(self.credentials.presta.client, entry.title)

                setattr(current_client, 'api_key', entry.custom_properties.get('api_key', None))
                setattr(current_client, 'api_domain', entry.custom_properties.get('api_domain', None))
                setattr(current_client, 'db_server', entry.custom_properties.get('db_server', None))
                setattr(current_client, 'db_user', entry.custom_properties.get('db_user', None))
                setattr(current_client, 'db_password', entry.custom_properties.get('db_password', None))

            except Exception as ex:
                print(f"Failed to extract prestashop credentials from KeePass ",ex)
                ...
                return False

         return True

    def _load_serpapi_credentials(self, kp: PyKeePass) -> bool:
        """ Load OpenAI credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            serpapi_credentials = kp.find_groups(path=['serpapi.com']).entries
           
            for entry in serpapi_credentials:


                try:
                    entry_ns = SimpleNamespace()
        
                    setattr(self.credentials.serpapi, entry.title, entry_ns)
        
                    _entry = getattr(self.credentials.serpapi, entry.title)
                    setattr(_entry, 'api_key', entry.custom_properties.get('api_key', None))
                
                except Exception as ex:
                    logger.error(f"Failed to extract serpapi.com API key from KeePass ", ex)
                    ...                 
            return True
        except Exception as ex:
            print(f"Failed to extract OpenAI credentials from KeePass {ex}" )
            ...
            return False
        
    def _load_smtp_credentials(self, kp: PyKeePass) -> bool:
        """ Load SMTP credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['smtp']).entries:
                self.credentials.smtp.append(SimpleNamespace(
                    server=entry.custom_properties.get('server', None),
                    port=entry.custom_properties.get('port', None),
                    user=entry.custom_properties.get('user', None),
                    password=entry.custom_properties.get('password', None),
                ))
            return True
        except Exception as ex:
            print(f"Failed to extract SMTP credentials from KeePass {ex}")
            ...
            return False

    def _load_facebook_credentials(self, kp: PyKeePass) -> bool:
        """ Load Facebook credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            for entry in kp.find_groups(path=['facebook']).entries:
                self.credentials.facebook.append(SimpleNamespace(
                    app_id=entry.custom_properties.get('app_id', None),
                    app_secret=entry.custom_properties.get('app_secret', None),
                    access_token=entry.custom_properties.get('access_token', None),
                ))
            return True
        except Exception as ex:
            print(f"Failed to extract Facebook credentials from KeePass {ex}")
            ...
            return False

    def _load_gapi_credentials(self, kp: PyKeePass) -> bool:
        """ Load Google API credentials from KeePass
        Args:
            kp (PyKeePass): The KeePass database instance.

        Returns:
            bool: True if loading was successful, False otherwise.
        """
        try:
            entry = kp.find_groups(path=['google','gapi']).entries[0]
            self.credentials.gapi['api_key'] = entry.custom_properties.get('api_key', None)
            return True
        except Exception as ex:
            print(f"Failed to extract GAPI credentials from KeePass {ex}") 
            ...
            return False

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