## \file src/webdriver/pydoll/options.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Класс ChromiumOptions для настройки браузера Pydoll Chrome.
===============================================================
Модуль предоставляет класс ChromiumOptions для конфигурации параметров запуска
браузера Chrome в проекте Pydoll. Позволяет настраивать различные опции
браузера, управлять аргументами командной строки и экспериментальными возможностями.

```rst
.. module:: src.webdriver.pydoll.options
```
"""

import header
from header import __root__
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns


class ChromiumOptions:
    """
    Класс для управления опциями запуска браузера Pydoll Chrome.
    
    Предоставляет методы для добавления аргументов командной строки,
    настройки экспериментальных опций, управления расширениями
    и другими параметрами браузера.
    """
    
    def __init__(self):
        """
        Инициализация объекта Options.
        
        Создает пустые списки и словари для хранения различных опций браузера.
        """
        self._arguments: List[str] = []
        self._binary_location: Optional[str] = None
        self._extensions: List[str] = []
        self._experimental_options: Dict[str, Any] = {}
        self._prefs: Dict[str, Any] = {}
        self._debugger_address: Optional[str] = None
        self._page_load_strategy: str = 'normal'
        self._unhandled_prompt_behavior: str = 'dismiss_and_notify'
        self._timeouts: Dict[str, int] = {
            'implicit': 0,
            'page_load': 300000,
            'script': 30000
        }
    
    @property
    def binary_location(self) -> Optional[str]:
        """
        Путь к исполняемому файлу браузера.
        
        Returns:
            Optional[str]: Путь к браузеру или None, если не установлен.
        """
        return self._binary_location
    
    @binary_location.setter
    def binary_location(self, path: str) -> None:
        """
        Устанавливает путь к исполняемому файлу браузера.
        
        Args:
            path (str): Путь к исполняемому файлу браузера.
        """
        if not isinstance(path, str):
            logger.error(f'Binary location must be a string, got: {type(path)}')
            return
        
        path_obj = Path(path)
        if not path_obj.exists():
            logger.warning(f'Binary location does not exist: {path}')
        
        self._binary_location = str(path_obj)
    
    @property
    def arguments(self) -> List[str]:
        """
        Список аргументов командной строки для браузера.
        
        Returns:
            List[str]: Список аргументов.
        """
        return self._arguments.copy()
    
    def add_argument(self, argument: str) -> None:
        """
        Добавляет аргумент командной строки для браузера.
        
        Args:
            argument (str): Аргумент командной строки (например, '--headless').
            
        Example:
            >>> options = ChromiumOptions()
            >>> options.add_argument('--headless')
            >>> options.add_argument('--window-size=1920,1080')
        """
        if not isinstance(argument, str):
            logger.error(f'Argument must be a string, got: {type(argument)}')
            return
        
        if argument.strip() and argument not in self._arguments:
            self._arguments.append(argument.strip())
        else:
            logger.debug(f'Argument already exists or is empty: {argument}')
    
    def remove_argument(self, argument: str) -> bool:
        """
        Удаляет аргумент командной строки.
        
        Args:
            argument (str): Аргумент для удаления.
            
        Returns:
            bool: True, если аргумент был удален, False, если не найден.
        """
        if argument in self._arguments:
            self._arguments.remove(argument)
            return True
        return False
    
    def add_extension(self, extension_path: str) -> None:
        """
        Добавляет расширение для загрузки в браузер.
        
        Args:
            extension_path (str): Путь к файлу расширения (.crx) или папке с расширением.
        """
        if not isinstance(extension_path, str):
            logger.error(f'Extension path must be a string, got: {type(extension_path)}')
            return
        
        path_obj = Path(extension_path)
        if not path_obj.exists():
            logger.warning(f'Extension path does not exist: {extension_path}')
        
        if extension_path not in self._extensions:
            self._extensions.append(str(path_obj))
    
    @property
    def extensions(self) -> List[str]:
        """
        Список путей к расширениям.
        
        Returns:
            List[str]: Список путей к расширениям.
        """
        return self._extensions.copy()
    
    def add_experimental_option(self, name: str, value: Any) -> None:
        """
        Добавляет экспериментальную опцию Chrome.
        
        Args:
            name (str): Название опции.
            value (Any): Значение опции.
            
        Example:
            >>> options = ChromiumOptions()
            >>> options.add_experimental_option('useAutomationExtension', False)
            >>> options.add_experimental_option('excludeSwitches', ['enable-automation'])
        """
        if not isinstance(name, str):
            logger.error(f'Option name must be a string, got: {type(name)}')
            return
        
        self._experimental_options[name] = value
    
    @property
    def experimental_options(self) -> Dict[str, Any]:
        """
        Словарь экспериментальных опций.
        
        Returns:
            Dict[str, Any]: Словарь экспериментальных опций.
        """
        return self._experimental_options.copy()
    
    def set_preference(self, name: str, value: Any) -> None:
        """
        Устанавливает пользовательскую настройку браузера.
        
        Args:
            name (str): Название настройки.
            value (Any): Значение настройки.
            
        Example:
            >>> options = ChromiumOptions()
            >>> options.set_preference('profile.default_content_setting_values.notifications', 2)
            >>> options.set_preference('profile.managed_default_content_settings.images', 2)
        """
        if not isinstance(name, str):
            logger.error(f'Preference name must be a string, got: {type(name)}')
            return
        
        self._prefs[name] = value
    
    @property
    def preferences(self) -> Dict[str, Any]:
        """
        Словарь пользовательских настроек браузера.
        
        Returns:
            Dict[str, Any]: Словарь настроек.
        """
        return self._prefs.copy()
    
    @property
    def debugger_address(self) -> Optional[str]:
        """
        Адрес отладчика Chrome DevTools.
        
        Returns:
            Optional[str]: Адрес отладчика или None.
        """
        return self._debugger_address
    
    @debugger_address.setter
    def debugger_address(self, address: str) -> None:
        """
        Устанавливает адрес отладчика Chrome DevTools.
        
        Args:
            address (str): Адрес в формате 'host:port' (например, '127.0.0.1:9222').
        """
        if not isinstance(address, str):
            logger.error(f'Debugger address must be a string, got: {type(address)}')
            return
        
        self._debugger_address = address
    
    @property
    def page_load_strategy(self) -> str:
        """
        Стратегия загрузки страниц.
        
        Returns:
            str: Стратегия загрузки ('normal', 'eager', 'none').
        """
        return self._page_load_strategy
    
    @page_load_strategy.setter
    def page_load_strategy(self, strategy: str) -> None:
        """
        Устанавливает стратегию загрузки страниц.
        
        Args:
            strategy (str): Стратегия ('normal', 'eager', 'none').
        """
        valid_strategies = ['normal', 'eager', 'none']
        if strategy not in valid_strategies:
            logger.error(f'Invalid page load strategy: {strategy}. Valid options: {valid_strategies}')
            return
        
        self._page_load_strategy = strategy
    
    def set_timeout(self, timeout_type: str, seconds: int) -> None:
        """
        Устанавливает таймаут для различных операций.
        
        Args:
            timeout_type (str): Тип таймаута ('implicit', 'page_load', 'script').
            seconds (int): Время ожидания в секундах.
        """
        valid_types = ['implicit', 'page_load', 'script']
        if timeout_type not in valid_types:
            logger.error(f'Invalid timeout type: {timeout_type}. Valid options: {valid_types}')
            return
        
        if not isinstance(seconds, int) or seconds < 0:
            logger.error(f'Timeout must be a non-negative integer, got: {seconds}')
            return
        
        self._timeouts[timeout_type] = seconds
    
    @property
    def timeouts(self) -> Dict[str, int]:
        """
        Словарь таймаутов.
        
        Returns:
            Dict[str, int]: Словарь таймаутов.
        """
        return self._timeouts.copy()
    
    def add_mobile_emulation(self, device_metrics: Dict[str, Any]) -> None:
        """
        Добавляет эмуляцию мобильного устройства.
        
        Args:
            device_metrics (Dict[str, Any]): Параметры устройства для эмуляции.
            
        Example:
            >>> options = ChromiumOptions()
            >>> mobile_emulation = {
            ...     'deviceMetrics': {
            ...         'width': 375,
            ...         'height': 667,
            ...         'pixelRatio': 2.0
            ...     },
            ...     'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)...'
            ... }
            >>> options.add_mobile_emulation(mobile_emulation)
        """
        if not isinstance(device_metrics, dict):
            logger.error(f'Device metrics must be a dictionary, got: {type(device_metrics)}')
            return
        
        self.add_experimental_option('mobileEmulation', device_metrics)
    
    def add_encoded_extension(self, extension: str) -> None:
        """
        Добавляет закодированное расширение.
        
        Args:
            extension (str): Base64-закодированное расширение.
        """
        if not isinstance(extension, str):
            logger.error(f'Extension must be a string, got: {type(extension)}')
            return
        
        if 'extensions' not in self._experimental_options:
            self._experimental_options['extensions'] = []
        
        self._experimental_options['extensions'].append(extension)
    
    def to_capabilities(self) -> Dict[str, Any]:
        """
        Преобразует опции в формат capabilities для WebDriver.
        
        Returns:
            Dict[str, Any]: Словарь capabilities.
        """
        capabilities = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'ANY',
            'goog:chromeOptions': {}
        }
        
        chrome_options = capabilities['goog:chromeOptions']
        
        if self._arguments:
            chrome_options['args'] = self._arguments
        
        if self._binary_location:
            chrome_options['binary'] = self._binary_location
        
        if self._extensions:
            chrome_options['extensions'] = self._extensions
        
        if self._experimental_options:
            chrome_options.update(self._experimental_options)
        
        if self._prefs:
            chrome_options['prefs'] = self._prefs
        
        if self._debugger_address:
            chrome_options['debuggerAddress'] = self._debugger_address
        
        # Добавляем таймауты на уровне capabilities
        if self._timeouts:
            capabilities['timeouts'] = self._timeouts
        
        if self._page_load_strategy != 'normal':
            capabilities['pageLoadStrategy'] = self._page_load_strategy
        
        if self._unhandled_prompt_behavior != 'dismiss_and_notify':
            capabilities['unhandledPromptBehavior'] = self._unhandled_prompt_behavior
        
        return capabilities
    
    def __str__(self) -> str:
        """
        Строковое представление объекта ChromiumOptions.
        
        Returns:
            str: Строковое представление.
        """
        return (
            f"ChromiumOptions(arguments={len(self._arguments)}, "
            f"extensions={len(self._extensions)}, "
            f"experimental_options={len(self._experimental_options)}, "
            f"binary_location='{self._binary_location}', "
            f"preferences={len(self._prefs)})"
        )
    
    def __repr__(self) -> str:
        """
        Представление объекта для отладки.
        
        Returns:
            str: Детальное представление объекта.
        """
        return self.__str__()
    
    @classmethod
    def from_config(cls, config_data: Union[Dict[str, Any], Path, str]) -> 'ChromiumOptions':
        """
        Создает объект ChromiumOptions из конфигурационных данных.
        
        Args:
            config_data (Union[Dict[str, Any], Path, str]): Конфигурационные данные,
                путь к файлу конфигурации или JSON строка.
                
        Returns:
            ChromiumOptions: Объект ChromiumOptions с настройками из конфигурации.
            
        Example:
            >>> config = {'arguments': ['--headless', '--no-sandbox']}
            >>> options = ChromiumOptions.from_config(config)
        """
        options = cls()
        
        try:
            if isinstance(config_data, (str, Path)):
                config = j_loads_ns(config_data)
                if hasattr(config, '__dict__'):
                    config = vars(config)
                else:
                    config = config_data if isinstance(config_data, dict) else {}
            else:
                config = config_data or {}
            
            # Добавляем аргументы
            if 'arguments' in config:
                for arg in config['arguments']:
                    options.add_argument(arg)
            
            # Устанавливаем binary_location
            if 'binary_location' in config and config['binary_location']:
                options.binary_location = config['binary_location']
            
            # Добавляем расширения
            if 'extensions' in config:
                for ext in config['extensions']:
                    options.add_extension(ext)
            
            # Добавляем экспериментальные опции
            if 'experimental_options' in config:
                for name, value in config['experimental_options'].items():
                    options.add_experimental_option(name, value)
            
            # Устанавливаем preferences
            if 'preferences' in config:
                for name, value in config['preferences'].items():
                    options.set_preference(name, value)
            
            # Устанавливаем debugger_address
            if 'debugger_address' in config and config['debugger_address']:
                options.debugger_address = config['debugger_address']
            
            # Устанавливаем page_load_strategy
            if 'page_load_strategy' in config:
                options.page_load_strategy = config['page_load_strategy']
            
            # Устанавливаем таймауты
            if 'timeouts' in config:
                for timeout_type, seconds in config['timeouts'].items():
                    options.set_timeout(timeout_type, seconds)
                    
        except Exception as ex:
            logger.error(f'Error loading options from config: {ex}', ex, exc_info=True)
        
        return options


class Options(ChromiumOptions):
    """
    Класс Options для совместимости с существующим кодом.
    
    Наследуется от ChromiumOptions и предоставляет тот же функционал
    под привычным именем Options.
    """
    
    def __init__(self):
        """
        Инициализация объекта Options.
        
        Вызывает конструктор родительского класса ChromiumOptions.
        """
        super().__init__()
    
    def __str__(self) -> str:
        """
        Строковое представление объекта Options.
        
        Returns:
            str: Строковое представление.
        """
        return (
            f"Options(arguments={len(self._arguments)}, "
            f"extensions={len(self._extensions)}, "
            f"experimental_options={len(self._experimental_options)}, "
            f"binary_location='{self._binary_location}', "
            f"preferences={len(self._prefs)})"
        )
    
    @classmethod
    def from_config(cls, config_data: Union[Dict[str, Any], Path, str]) -> 'Options':
        """
        Создает объект Options из конфигурационных данных.
        
        Args:
            config_data (Union[Dict[str, Any], Path, str]): Конфигурационные данные,
                путь к файлу конфигурации или JSON строка.
                
        Returns:
            Options: Объект Options с настройками из конфигурации.
            
        Example:
            >>> config = {'arguments': ['--headless', '--no-sandbox']}
            >>> options = Options.from_config(config)
        """
        options = cls()
        
        try:
            if isinstance(config_data, (str, Path)):
                config = j_loads_ns(config_data)
                if hasattr(config, '__dict__'):
                    config = vars(config)
                else:
                    config = config_data if isinstance(config_data, dict) else {}
            else:
                config = config_data or {}
            
            # Добавляем аргументы
            if 'arguments' in config:
                for arg in config['arguments']:
                    options.add_argument(arg)
            
            # Устанавливаем binary_location
            if 'binary_location' in config and config['binary_location']:
                options.binary_location = config['binary_location']
            
            # Добавляем расширения
            if 'extensions' in config:
                for ext in config['extensions']:
                    options.add_extension(ext)
            
            # Добавляем экспериментальные опции
            if 'experimental_options' in config:
                for name, value in config['experimental_options'].items():
                    options.add_experimental_option(name, value)
            
            # Устанавливаем preferences
            if 'preferences' in config:
                for name, value in config['preferences'].items():
                    options.set_preference(name, value)
            
            # Устанавливаем debugger_address
            if 'debugger_address' in config and config['debugger_address']:
                options.debugger_address = config['debugger_address']
            
            # Устанавливаем page_load_strategy
            if 'page_load_strategy' in config:
                options.page_load_strategy = config['page_load_strategy']
            
            # Устанавливаем таймауты
            if 'timeouts' in config:
                for timeout_type, seconds in config['timeouts'].items():
                    options.set_timeout(timeout_type, seconds)
                    
        except Exception as ex:
            logger.error(f'Error loading options from config: {ex}', ex, exc_info=True)
        
        return options