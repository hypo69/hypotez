# src/webdriver/pydoll/options.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Options class for advanced configuration of the Pydoll Chrome browser.
==================================================================
This class is completely autonomous. When an instance is created, it
automatically reads the `browser.json` file, applies the settings, and
allows for flexible overriding of any parameters through arguments
in the constructor.
"""

from pathlib import Path
from typing import Dict, Any, Union, List, Tuple

from header import __root__
# from src.webdriver.pydoll.llib.browser.options import ChromiumOptions
from pydoll.browser.options import ChromiumOptions
from src.logger.logger import logger
from src.utils.jjson import j_loads

class Options(ChromiumOptions):
    """
    A standalone class for managing Pydoll Chrome options, which
    reads the configuration file itself and stores all settings as attributes.
    """
    _CONFIG_FILE_PATH = __root__ / 'src' / 'webdriver' / 'pydoll' / 'browser.json'

    def __init__(self, **overrides: Any):
        """
        Initializes and configures the Options object.
        """

        super().__init__()

        # Attributes for storing all types of settings
        self._arguments_map: Dict[str, Union[str, bool]] = {}
        self.experimental_options: Dict[str, Any] = {}
        self.extensions: List[str] = []
        self.timeouts: Dict[str, int] = {}
        self.page_load_strategy: str = 'normal'
        self.debugger_address: str = ''
        self.mobile_emulation: Dict[str, Any] = {}

        logger.debug("Initializing Options...")

        if not self._CONFIG_FILE_PATH.exists():
            raise FileNotFoundError(f"Critical error: Configuration file '{self._CONFIG_FILE_PATH}' not found.")

        try:
            default_options: dict = j_loads(self._CONFIG_FILE_PATH)
            if not default_options:
                raise ValueError(f"Configuration file '{self._CONFIG_FILE_PATH}' is empty or invalid.")
            logger.debug(f"Successfully loaded config from {self._CONFIG_FILE_PATH}")
        except Exception as ex:
            logger.error(f"Failed to load or parse '{self._CONFIG_FILE_PATH}': ", ex, exc_info=True)
            raise

        final_config = {**default_options, **overrides}
        
        self._apply_unified_config(final_config)

        logger.info("Options configured successfully.")

    # --- Overridden parent methods ---

    @staticmethod
    def _parse_argument(argument: str) -> Tuple[str, Union[str, bool]]:
        parts = argument.split('=', 1)
        return parts[0], parts[1] if len(parts) > 1 else True

    def add_argument(self, argument: str):
        key, value = self._parse_argument(argument)
        self._arguments_map[key] = value

    @property
    def arguments(self) -> List[str]:
        final_list = []
        for key, value in self._arguments_map.items():
            final_list.append(key if value is True else f"{key}={value}")
        return final_list

    @arguments.setter
    def arguments(self, args_list: List[str]):
        self._arguments_map = {}
        for arg in args_list:
            self.add_argument(arg)

    # --- Main configuration logic ---

    def _apply_unified_config(self, config: Dict[str, Any]):
        """Applies all settings, storing them in class attributes."""
        # 1. Command line arguments
        self.arguments = config.get('arguments', [])
        if config.get('headless'): self.add_argument('--headless=new')
        if config.get('incognito'): self.add_argument('--incognito')
        if user_agent := config.get('user_agent'): self.add_argument(f'user-agent={user_agent}')
        if user_data_dir := config.get('user_data_dir'): self.add_argument(f'--user-data-dir={user_data_dir}')
        if profile_directory := config.get('profile_directory'): self.add_argument(f'--profile-directory={profile_directory}')

        # 2. Experimental Options and Preferences
        final_experimental_options = config.get('experimental_options', {}).copy()
        final_preferences = final_experimental_options.get('prefs', {}).copy()

        if base_preferences := config.get('preferences', {}):
            final_preferences.update(base_preferences)

        if config.get('disable_images'):
            final_preferences["profile.managed_default_content_settings.images"] = 2

        final_experimental_options['prefs'] = final_preferences
        self.experimental_options = final_experimental_options

        # 3. Other settings
        self.binary_location = config.get('binary_location', '')
        self.page_load_strategy = config.get('page_load_strategy', 'normal')
        self.debugger_address = config.get('debugger_address', '')
        self.extensions = config.get('extensions', [])
        self.timeouts = config.get('timeouts', {})

        # 4. Mobile emulation
        if mobile_emulation_config := config.get('mobile_emulation', {}):
            if mobile_emulation_config.get('enabled'):
                self.mobile_emulation = mobile_emulation_config
