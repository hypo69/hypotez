### **Анализ кода модуля `fast_api.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Использование FastAPI для создания веб-сервера.
  - Реализация Singleton для класса `FastApiServer`.
  - Поддержка динамической регистрации маршрутов.
  - Использование `logger` для логирования.
  - Обработка исключений с логированием ошибок.
- **Минусы**:
  - Неполная документация функций и классов.
  - Смешанный стиль комментариев (русский/английский).
  - Отсутствие аннотаций типов для некоторых переменных.
  - Использование `print` вместо `logger.info` для информационных сообщений.
  - Дублирование функциональности (например, `start_server` и `CommandHandler.start_server`).
  - Не все функции имеют docstring.

#### **Рекомендации по улучшению**:
1. **Документирование кода**:
   - Добавить docstring к каждой функции и классу, описывая их назначение, параметры и возвращаемые значения.
   - Перевести все комментарии и docstring на русский язык.
   - Использовать подробные и понятные описания в docstring.
2. **Аннотации типов**:
   - Добавить аннотации типов для всех переменных и параметров функций, где они отсутствуют.
3. **Логирование**:
   - Заменить все `print` на `logger.info` для вывода информационных сообщений.
4. **Обработка исключений**:
   - Убедиться, что все исключения обрабатываются с использованием `logger.error` и `exc_info=True`.
5. **Рефакторинг**:
   - Избегать дублирования кода (например, вынести общую логику запуска сервера в отдельную функцию).
   - Упростить структуру, где это возможно (например, убрать излишнюю вложенность).
6. **Конфигурация**:
   - Улучшить обработку конфигурационных файлов, чтобы обеспечить более гибкую настройку сервера.
7. **Безопасность**:
   - Рассмотреть возможность добавления дополнительных мер безопасности, таких как валидация входных данных и защита от common web vulnerabilities.
8. **Зависимости**:
   - Управление зависимостями должно быть четким и понятным, например, через `requirements.txt` или `pyproject.toml`.
9. **Соответствие PEP8**:
   - Проверить код на соответствие стандартам PEP8 и исправить все нарушения.

#### **Оптимизированный код**:

```python
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
FastAPI сервер с XML-RPC интерфейсом для удалённого управления
====================================================

Модуль содержит класс :class:`FastApiServer`, который реализует FastAPI сервер
с интерфейсом XML-RPC для удалённого управления.

Пример использования
----------------------

>>> server = FastApiServer(host='127.0.0.1', port=8000)
>>> server.start(port=8000)
"""
import asyncio
import functools
import json
import os
import sys
import threading
from types import SimpleNamespace
from typing import List, Callable, Dict, Optional
from pathlib import Path
from contextlib import asynccontextmanager
from xmlrpc.server import SimpleXMLRPCServer
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, APIRouter
import importlib  # Добавлен для динамического импорта

import header  # <-- Обязательный импорт
from header import __root__
from src.fast_api.routes import Routes
from src import gs
from src.utils.jjson import j_loads, j_loads_ns
from src.logger import logger
import re

load_dotenv()

try:
    config: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'fast_api' / 'fast_api.json')
    config.ports: list = config.ports if isinstance(config.ports, list) else [config.ports]
except Exception as ex:
    logger.critical('Config file not found!', exc_info=True)
    sys.exit()

_api_server_instance = None


class FastApiServer:
    """
    FastAPI сервер с реализацией Singleton.

    Реализует Singleton для управления экземпляром FastAPI сервера.
    """

    _instance = None
    app: FastAPI = FastAPI()
    host: str = config.host
    port: int = 8000
    router: APIRouter = APIRouter()

    def __new__(cls, *args, **kwargs):
        """
        Создает или возвращает существующий экземпляр класса.

        Реализует паттерн Singleton, гарантируя, что только один экземпляр
        класса существует в течение времени выполнения программы.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str = '127.0.0.1', title: str = 'FastAPI RPC Server', **kwargs):
        """
        Инициализирует экземпляр класса FastApiServer.

        Args:
            host (str): Хост, на котором будет запущен сервер. По умолчанию '127.0.0.1'.
            title (str): Заголовок FastAPI приложения. По умолчанию 'FastAPI RPC Server'.
            **kwargs: Дополнительные аргументы для FastAPI.
        """
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.add_route('/hello', test_function)
        self.add_route('/post', test_post, methods=['POST'])
        # self.add_route("/telegram_webhook", telegram_webhook, methods=["POST"])

        self.app = FastAPI()
        self.host = host or config.host
        self.server_tasks = {}
        self.servers = {}
        self.app.include_router(self.router)

    def add_route(self, path: str, func: Callable, methods: List[str] = ['GET'], **kwargs):
        """
        Добавляет маршрут к FastAPI приложению.

        Args:
            path (str): Путь маршрута.
            func (Callable): Функция, обрабатывающая маршрут.
            methods (List[str]): Список HTTP методов для маршрута. По умолчанию ['GET'].
            **kwargs: Дополнительные аргументы для `router.add_api_route`.
        """
        try:
            self.router.add_api_route(path, func, methods=methods, **kwargs)
            logger.info(f'Маршрут {path} зарегистрирван')
        except Exception as ex:
            logger.error(f'Ошибка добавления маршрута {path}', ex, exc_info=True)

    async def _start_server(self, port: int):
        """
        Запускает uvicorn сервер асинхронно.

        Args:
            port (int): Порт, на котором будет запущен сервер.
        """
        config = uvicorn.Config(self.app, host=self.host, port=port, log_level='debug')
        server = uvicorn.Server(config)
        try:
            await server.serve()
            logger.success(f'Server started on: {self.host}:{port}')
        except Exception as ex:
            logger.error(f'Error running server on port {port}: {ex}', exc_info=True)
        finally:
            self.servers.pop(port, None)

    def start(self, port: int, as_thread: bool = True):
        """
        Запускает FastAPI сервер на указанном порту.

        Args:
            port (int): Порт для запуска сервера.
            as_thread (bool): Запускать ли сервер в отдельном потоке. По умолчанию True.
        """
        if port in self.servers:
            logger.info(f'Server already running on port {port}')
            return

        task = threading.Thread(target=asyncio.run, args=(self._start_server(port),), daemon=True)
        self.server_tasks[port] = task
        self.servers[port] = task
        task.start()

    def stop(self, port: int):
        """
        Останавливает FastAPI сервер на указанном порту.

        Args:
            port (int): Порт сервера для остановки.
        """
        if port in self.servers:
            try:
                self.servers[port]._thread.join(1)
                self.servers.pop(port)
                logger.info(f'Server on port {port} stopped.')
            except Exception as ex:
                logger.error(f'Error stopping server on port {port}: {ex}', exc_info=True)
        else:
            logger.info(f'Server on port {port} is not running or already stopped.')

    def stop_all(self):
        """Останавливает все запущенные сервера."""
        for port in list(self.servers):
            self.stop(port)

    def get_servers_status(self) -> Dict[int, str]:
        """
        Возвращает статус всех серверов.

        Returns:
            Dict[int, str]: Словарь, где ключ - порт, значение - статус сервера.
        """
        return {port: 'Running' if task.is_alive() else 'Stopped' for port, task in self.servers.items()}

    def get_routes(self) -> List[Dict[str, str]]:
        """
        Возвращает список всех роутов.

        Returns:
            List[Dict[str, str]]: Список словарей, где каждый словарь содержит путь и методы роута.
        """
        routes = []
        for route in self.app.routes:
            if hasattr(route, 'path'):
                methods = getattr(route, 'methods', ['GET'])
                routes.append({'path': route.path, 'methods': list(methods)})
        return routes

    def get_app(self) -> FastAPI:
        """
        Возвращает FastAPI приложение.

        Returns:
            FastAPI: FastAPI приложение.
        """
        return self.app

    def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ['GET'], **kwargs):
        """
        Добавляет новый маршрут к уже работающему приложению.

        Args:
            path (str): Путь для нового маршрута.
            module_name (str): Имя модуля, содержащего функцию для маршрута.
            func_name (str): Имя функции, которая будет обрабатывать маршрут.
            methods (List[str]): Список HTTP методов для маршрута. По умолчанию ['GET'].
            **kwargs: Дополнительные аргументы для `add_route`.
        """
        try:
            # Динамически импортируем модуль
            module = importlib.import_module(module_name)
            # Получаем функцию из модуля
            func = getattr(module, func_name, None)
            if func is None:
                raise AttributeError(f"Function '{func_name}' not found in module '{module_name}'")

            self.add_route(path, func, methods=methods, **kwargs)
            logger.info(f'Маршрут {path} зарегистрирован из модуля {module_name}')
        except Exception as ex:
            logger.error(f'Ошибка добавления маршрута {path} из модуля {module_name}: {ex}', exc_info=True)


def telegram_webhook() -> str:
    """
    Обработчик Telegram webhook.

    Returns:
        str: Приветственное сообщение.
    """
    return 'Hello, World!'


def test_function() -> str:
    """
    Тестовая функция для проверки работы сервера.

    Returns:
        str: Строка 'It is working!!!'.
    """
    return 'It is working!!!'


def test_post(data: Dict[str, str]) -> Dict[str, str]:
    """
    Тестовая функция для обработки POST запросов.

    Args:
        data (Dict[str, str]): Данные, переданные в POST запросе.

    Returns:
        Dict[str, str]: Словарь с результатом и данными.
    """
    return {'result': 'post ok', 'data': data}


def start_server(port: int, host: str):
    """
    Запускает FastAPI сервер на указанном порту.

    Args:
        port (int): Порт для запуска сервера.
        host (str): Хост для запуска сервера.
    """
    global _api_server_instance
    if _api_server_instance is None:
        _api_server_instance = FastApiServer(host=host)
    try:
        _api_server_instance.start(port=port)
    except Exception as ex:
        logger.error(f'Ошибка запуска FastAPI сервера на порту {port}:', ex, exc_info=True)


def stop_server(port: int):
    """
    Останавливает FastAPI сервер на указанном порту.

    Args:
        port (int): Порт сервера для остановки.
    """
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.stop(port=port)
        except Exception as ex:
            logger.error(f'Ошибка остановки FastAPI сервера на порту {port}:', ex, exc_info=True)


def stop_all_servers():
    """Останавливает все запущенные FastAPI сервера."""
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.stop_all()
        except Exception as ex:
            logger.error(f'Ошибка остановки всех FastAPI серверов:', ex, exc_info=True)


def status_servers():
    """Показывает статус серверов."""
    global _api_server_instance
    if _api_server_instance:
        servers = _api_server_instance.get_servers_status()
        if servers:
            logger.info(f'Server initialized on host {_api_server_instance.host}')
            for port, status in servers.items():
                logger.info(f'  - Port {port}: {status}')
        else:
            logger.info('No servers running')
    else:
        logger.info('Server not initialized.')


def get_routes():
    """Показывает все роуты."""
    global _api_server_instance
    if _api_server_instance:
        routes = _api_server_instance.get_routes()
        if routes:
            logger.info('Available routes:')
            for route in routes:
                logger.info(f'  - Path: {route["path"]}, Methods: {route["methods"]}')
        else:
            logger.info('No routes defined')
    else:
        logger.info('Server not initialized.')


def add_new_route(path: str, module_name: str, func_name: str, methods: List[str] = ['GET']):
    """
    Добавляет новый роут к серверу.

    Args:
        path (str): Путь для нового маршрута.
        module_name (str): Имя модуля, содержащего функцию для маршрута.
        func_name (str): Имя функции, которая будет обрабатывать маршрут.
        methods (List[str]): Список HTTP методов для маршрута. По умолчанию ['GET'].
    """
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)
            logger.info(f'Route added: {path}, {methods=}')
        except Exception as ex:
            logger.error(f'Ошибка добавления нового роута {path}:', ex, exc_info=True)
    else:
        logger.info('Server not initialized. Start server first')


def parse_port_range(range_str: str) -> List[int]:
    """
    Разбирает строку с диапазоном портов.

    Args:
        range_str (str): Строка с диапазоном портов.

    Returns:
        List[int]: Список портов.
    """
    if not re.match(r'^[\d-]+$', range_str):
        logger.info(f'Invalid port range: {range_str}')
        return []
    if '-' in range_str:
        try:
            start, end = map(int, range_str.split('-'))
            if start > end:
                raise ValueError('Invalid port range')
            return list(range(start, end + 1))
        except ValueError:
            logger.info(f'Invalid port range: {range_str}')
            return []
    else:
        try:
            return [int(range_str)]
        except ValueError:
            logger.info(f'Invalid port: {range_str}')
            return []


class CommandHandler:
    """
    Обработчик команд для FastAPI сервера через XML-RPC.

    Предоставляет интерфейс для управления сервером через XML-RPC.
    """

    def __init__(self, rpc_port: int = 9000):
        """
        Инициализирует обработчик команд.

        Args:
            rpc_port (int): Порт для XML-RPC сервера. По умолчанию 9000.
        """
        self.rpc_port = rpc_port
        self.rpc_server = SimpleXMLRPCServer(('localhost', self.rpc_port), allow_none=True)
        self.rpc_server.register_instance(self)
        threading.Thread(target=self.rpc_server.serve_forever, daemon=True).start()
        logger.info(f'RPC server started on port: {self.rpc_port}')

    def start_server(self, port: int, host: str):
        """
        Запускает FastAPI сервер.

        Args:
            port (int): Порт для запуска сервера.
            host (str): Хост для запуска сервера.
        """
        start_server(port=port, host=host)

    def stop_server(self, port: int):
        """
        Останавливает FastAPI сервер.

        Args:
            port (int): Порт сервера для остановки.
        """
        stop_server(port=port)

    def stop_all_servers(self):
        """Останавливает все запущенные FastAPI сервера."""
        stop_all_servers()

    def status_servers(self):
        """Выводит статус серверов."""
        status_servers()

    def get_routes(self):
        """Выводит список роутов."""
        get_routes()

    def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ['GET']):
        """
        Добавляет новый роут к серверу.

        Args:
            path (str): Путь для нового маршрута.
            module_name (str): Имя модуля, содержащего функцию для маршрута.
            func_name (str): Имя функции, которая будет обрабатывать маршрут.
            methods (List[str]): Список HTTP методов для маршрута. По умолчанию ['GET'].
        """
        add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)

    def shutdown(self):
        """Останавливает все сервера и завершает работу."""
        self.stop_all_servers()
        self.rpc_server.shutdown()
        logger.info('RPC server shutdown')
        sys.exit(0)


def display_menu():
    """Выводит меню с доступными командами."""
    logger.info('\nAvailable commands:')
    logger.info('  start <port>        - Start server on the specified port')
    logger.info('  status              - Show all served ports status')
    logger.info('  routes              - Show all registered routes')
    logger.info('  stop <port>         - Stop server on the specified port')
    logger.info('  stop_all            - Stop all servers')
    logger.info('  add_route <path>    - Add a new route to the server')
    logger.info('  shutdown            - Stop all servers and exit')
    logger.info('  help                - Show this help menu')
    logger.info('  exit                - Exit the program')


def main():
    """Основная функция управления сервером."""
    command_handler = CommandHandler()
    while True:
        display_menu()
        try:
            command_line = input('Enter command: ').strip().lower()
            if not command_line:
                continue

            parts = command_line.split()
            command = parts[0]

            if command == 'start':
                if len(parts) != 2:
                    logger.info('Usage: start <port>')
                    continue
                try:
                    port = int(parts[1])
                    host = input('Enter host address (default: 127.0.0.1): ').strip() or '127.0.0.1'
                    command_handler.start_server(port=port, host=host)
                except ValueError:
                    logger.info('Invalid port number.')
                except Exception as ex:
                    logger.error('An error occurred:', ex, exc_info=True)

            elif command == 'status':
                command_handler.status_servers()

            elif command == 'routes':
                command_handler.get_routes()

            elif command == 'stop':
                if len(parts) != 2:
                    logger.info('Usage: stop <port>')
                    continue
                try:
                    port = int(parts[1])
                    command_handler.stop_server(port=port)
                except ValueError:
                    logger.info('Invalid port number.')
                except Exception as ex:
                    logger.error('An error occurred:', ex, exc_info=True)

            elif command == 'stop_all':
                command_handler.stop_all_servers()

            elif command == 'add_route':
                if len(parts) < 2:
                    logger.info('Usage: add_route <path> <module_name> <func_name>')
                    continue
                path = parts[1]
                module_name = input('Enter module name: ').strip()
                func_name = input('Enter function name: ').strip()
                methods = input('Enter HTTP methods (comma-separated, default: GET): ').strip().upper() or 'GET'
                methods = [method.strip() for method in methods.split(',')]
                command_handler.add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)

            elif command == 'shutdown':
                command_handler.shutdown()  # call shutdown method on command_handler

            elif command == 'help':
                display_menu()

            elif command == 'exit':
                logger.info('Exiting the program.')
                sys.exit(0)

            else:
                logger.info("Unknown command. Type 'help' to see the list of available commands")

        except Exception as ex:
            logger.error('An error occurred:', ex, exc_info=True)


if __name__ == '__main__':
    main()