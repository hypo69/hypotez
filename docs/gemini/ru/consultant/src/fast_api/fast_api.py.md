### **Анализ кода модуля `fast_api.py`**

## \file /hypotez/src/fast_api/fast_api.py

Модуль представляет собой FastAPI сервер с XML-RPC интерфейсом для удалённого управления.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование `logger` для логирования.
  - Наличие `CommandHandler` для обработки команд через XML-RPC.
  - Конфигурация загружается из файла `fast_api.json`.
  - Применение `j_loads_ns` для загрузки конфигурации.
- **Минусы**:
  - Отсутствие подробной документации для всех функций и классов.
  - Смешанный стиль: где-то есть docstring, где-то нет.
  - Использование глобальных переменных (например, `_api_server_instance`).
  - Не все переменные аннотированы типами.
  -  Не везде используется `ex` вместо `e` в блоках обработки исключений.
  - Местами есть лишние комментарии.

**Рекомендации по улучшению:**

1. **Документация**:
   - Добавить docstring ко всем функциям, методам и классам, включая описание аргументов, возвращаемых значений и возможных исключений.
   - Перевести все docstring на русский язык.
2. **Глобальные переменные**:
   - Избегать использования глобальных переменных, таких как `_api_server_instance`. Рассмотреть возможность передачи инстанса `FastApiServer` между функциями или использования dependency injection.
3. **Аннотации типов**:
   - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений.
4. **Обработка исключений**:
   - Использовать `ex` вместо `e` в блоках `except`.
   - Указывать более конкретные типы исключений в блоках `except`.
5. **Логирование**:
   - Убедиться, что все исключения логируются с использованием `logger.error` и передачей `exc_info=True`.
6. **Конфигурация**:
   - Рассмотреть возможность использования более продвинутых инструментов для управления конфигурацией, таких как Pydantic settings.
7. **Структура**:
   - Разделить код на более мелкие, логически связанные функции и классы для повышения читаемости и упрощения тестирования.
8. **Комментарии**:
   - Сделать комментарии более информативными и убрать лишние.
9. **Обработка ошибок**:
    - Улучшить обработку ошибок, чтобы предоставлять более информативные сообщения пользователю.
10. **Зависимости**:
    - Явное указание зависимостей в `requirements.txt` или `pyproject.toml`.

**Оптимизированный код:**

```python
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль FastAPI сервера с XML-RPC интерфейсом для удалённого управления
=====================================================================

Модуль содержит класс :class:`FastApiServer`, который реализует FastAPI сервер
с интерфейсом XML-RPC для удалённого управления.

Пример использования
----------------------

>>> server = FastApiServer(host='127.0.0.1')
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
from src.utils.printer import pprint as print
from src.logger import logger
import re

load_dotenv()

try:
    config: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'fast_api' / 'fast_api.json')
    config.ports: list = config.ports if isinstance(config.ports, list) else [config.ports]
except Exception as ex:
    logger.critical('Config file not found!', ex, exc_info=True)
    sys.exit()

_api_server_instance = None


class FastApiServer:
    """
    FastAPI сервер с реализацией Singleton.

    Реализует функциональность FastAPI сервера для управления через XML-RPC.

    Attributes:
        _instance (FastApiServer | None): Единственный экземпляр класса.
        app (FastAPI): FastAPI приложение.
        host (str): Хост для запуска сервера.
        port (int): Порт для запуска сервера.
        router (APIRouter): FastAPI роутер для обработки запросов.
        server_tasks (dict): Словарь для хранения задач серверов.
        servers (dict): Словарь для хранения запущенных серверов.
    """

    _instance: Optional["FastApiServer"] = None
    app: FastAPI = FastAPI()
    host: str = config.host
    port: int = 8000
    router: APIRouter = APIRouter()

    def __new__(cls, *args, **kwargs) -> "FastApiServer":
        """
        Создает новый экземпляр класса, если он еще не существует.

        Returns:
            FastApiServer: Единственный экземпляр класса.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs):
        """
        Инициализирует экземпляр класса FastApiServer.

        Args:
            host (str, optional): Хост для запуска сервера. По умолчанию "127.0.0.1".
            title (str, optional): Заголовок FastAPI приложения. По умолчанию "FastAPI RPC Server".
            **kwargs: Дополнительные аргументы для FastAPI.
        """
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.add_route("/hello", test_function)
        self.add_route("/post", test_post, methods=["POST"])
        # self.add_route("/telegram_webhook", telegram_webhook, methods=["POST"])

        self.app = FastAPI()
        self.host = host or config.host
        self.server_tasks: Dict[int, threading.Thread] = {}
        self.servers: Dict[int, threading.Thread] = {}
        self.app.include_router(self.router)

    def add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs) -> None:
        """
        Добавляет маршрут к FastAPI приложению.

        Args:
            path (str): Путь маршрута.
            func (Callable): Функция, обрабатывающая маршрут.
            methods (List[str], optional): Список HTTP методов для маршрута. По умолчанию ["GET"].
            **kwargs: Дополнительные аргументы для `router.add_api_route`.

        """
        try:
            self.router.add_api_route(path, func, methods=methods, **kwargs)
            logger.info(f'Маршрут {path} зарегистрирован')
        except Exception as ex:
            logger.error(f'Ошибка добавления маршрута {path}', ex, exc_info=True)

    async def _start_server(self, port: int) -> None:
        """
        Запускает uvicorn сервер асинхронно.

        Args:
            port (int): Порт для запуска сервера.

        """
        config = uvicorn.Config(self.app, host=self.host, port=port, log_level="debug")
        server = uvicorn.Server(config)
        try:
            await server.serve()
            logger.success(f'Server started on: {self.host}:{port}')
        except Exception as ex:
            logger.error(f'Error running server on port {port}: {ex}', exc_info=True)
        finally:
            self.servers.pop(port, None)

    def start(self, port: int, as_thread: bool = True) -> None:
        """
        Запускает FastAPI сервер на указанном порту.

        Args:
            port (int): Порт для запуска сервера.
            as_thread (bool, optional): Запускать сервер в отдельном потоке. По умолчанию True.

        """
        if port in self.servers:
            print(f'Server already running on port {port}')
            return

        task = threading.Thread(target=asyncio.run, args=(self._start_server(port),), daemon=True)
        self.server_tasks[port] = task
        self.servers[port] = task
        task.start()

    def stop(self, port: int) -> None:
        """
        Останавливает FastAPI сервер на указанном порту.

        Args:
            port (int): Порт для остановки сервера.

        """
        if port in self.servers:
            try:
                self.servers[port].join(1)
                self.servers.pop(port)
                print(f'Server on port {port} stopped.')
            except Exception as ex:
                logger.error(f'Error stopping server on port {port}: {ex}', exc_info=True)
        else:
            print(f'Server on port {port} is not running or already stopped.')

    def stop_all(self) -> None:
        """Останавливает все запущенные сервера."""
        for port in list(self.servers):
            self.stop(port)

    def get_servers_status(self) -> Dict[int, str]:
        """
        Возвращает статус всех серверов.

        Returns:
            Dict[int, str]: Словарь, где ключ - порт, значение - статус ("Running" или "Stopped").

        """
        return {port: 'Running' if task.is_alive() else 'Stopped' for port, task in self.servers.items()}

    def get_routes(self) -> List[Dict[str, str]]:
        """
        Возвращает список всех роутов.

        Returns:
            List[Dict[str, str]]: Список словарей, где каждый словарь содержит информацию о роуте (путь и методы).
        """
        routes = []
        for route in self.app.routes:
            if hasattr(route, "path"):
                methods = getattr(route, "methods", ["GET"])
                routes.append({"path": route.path, "methods": list(methods)})
        return routes

    def get_app(self) -> FastAPI:
        """
        Возвращает FastAPI приложение.

        Returns:
            FastAPI: FastAPI приложение.

        """
        return self.app

    def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs) -> None:
        """
        Добавляет новый маршрут к уже работающему приложению.

        Args:
            path (str): Путь маршрута.
            module_name (str): Имя модуля, содержащего функцию для маршрута.
            func_name (str): Имя функции, обрабатывающей маршрут.
            methods (List[str], optional): Список HTTP методов для маршрута. По умолчанию ["GET"].
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
    Обработчик webhook для Telegram.

    Returns:
        str: Приветственное сообщение.
    """
    return 'Hello, World!'


def test_function() -> str:
    """
    Тестовая функция.

    Returns:
        str: Строка "It is working!!!".
    """
    return "It is working!!!"


def test_post(data: Dict[str, str]) -> Dict[str, str]:
    """
    Тестовая функция для обработки POST запросов.

    Args:
        data (Dict[str, str]): Данные, переданные в POST запросе.

    Returns:
        Dict[str, str]: Словарь с результатом обработки и переданными данными.
    """
    return {"result": "post ok", "data": data}


def start_server(port: int, host: str) -> None:
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


def stop_server(port: int) -> None:
    """
    Останавливает FastAPI сервер на указанном порту.

    Args:
        port (int): Порт для остановки сервера.
    """
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.stop(port=port)
        except Exception as ex:
            logger.error(f'Ошибка остановки FastAPI сервера на порту {port}:', ex, exc_info=True)


def stop_all_servers() -> None:
    """Останавливает все запущенные FastAPI сервера."""
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.stop_all()
        except Exception as ex:
            logger.error(f'Ошибка остановки всех FastAPI серверов:', ex, exc_info=True)


def status_servers() -> None:
    """Выводит статус серверов."""
    global _api_server_instance
    if _api_server_instance:
        servers = _api_server_instance.get_servers_status()
        if servers:
            print(f'Server initialized on host {_api_server_instance.host}')
            for port, status in servers.items():
                print(f'  - Port {port}: {status}')
        else:
            print('No servers running')
    else:
        print('Server not initialized.')


def get_routes() -> None:
    """Выводит все роуты."""
    global _api_server_instance
    if _api_server_instance:
        routes = _api_server_instance.get_routes()
        if routes:
            print('Available routes:')
            for route in routes:
                print(f'  - Path: {route["path"]}, Methods: {route["methods"]}')
        else:
            print('No routes defined')
    else:
        print('Server not initialized.')


def add_new_route(path: str, module_name: str, func_name: str, methods: List[str] = ["GET"]) -> None:
    """
    Добавляет новый роут к серверу.

    Args:
        path (str): Путь маршрута.
        module_name (str): Имя модуля, содержащего функцию для маршрута.
        func_name (str): Имя функции, обрабатывающей маршрут.
        methods (List[str], optional): Список HTTP методов для маршрута. По умолчанию ["GET"].
    """
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)
            print(f'Route added: {path}, {methods=}')
        except Exception as ex:
            logger.error(f'Ошибка добавления нового роута {path}:', ex, exc_info=True)
    else:
        print('Server not initialized. Start server first')


def parse_port_range(range_str: str) -> List[int]:
    """
    Разбирает строку с диапазоном портов.

    Args:
        range_str (str): Строка с диапазоном портов (например, "8000-8005" или "8000").

    Returns:
        List[int]: Список портов.
    """
    if not re.match(r'^[\d-]+$', range_str):
        print(f'Invalid port range: {range_str}')
        return []
    if '-' in range_str:
        try:
            start, end = map(int, range_str.split('-'))
            if start > end:
                raise ValueError("Invalid port range")
            return list(range(start, end + 1))
        except ValueError:
            print(f'Invalid port range: {range_str}')
            return []
    else:
        try:
            return [int(range_str)]
        except ValueError:
            print(f'Invalid port: {range_str}')
            return []


class CommandHandler:
    """
    Обработчик команд для FastAPI сервера через XML-RPC.

    Предоставляет интерфейс для управления сервером через XML-RPC.

    Args:
        rpc_port (int, optional): Порт для XML-RPC сервера. По умолчанию 9000.
    """

    def __init__(self, rpc_port: int = 9000):
        """
        Инициализирует обработчик команд.

        Args:
            rpc_port (int, optional): Порт для XML-RPC сервера. По умолчанию 9000.
        """
        self.rpc_port: int = rpc_port
        self.rpc_server: SimpleXMLRPCServer = SimpleXMLRPCServer(("localhost", self.rpc_port), allow_none=True)
        self.rpc_server.register_instance(self)
        threading.Thread(target=self.rpc_server.serve_forever, daemon=True).start()
        print(f'RPC server started on port: {self.rpc_port}')

    def start_server(self, port: int, host: str) -> None:
        """
        Запускает FastAPI сервер.

        Args:
            port (int): Порт для запуска сервера.
            host (str): Хост для запуска сервера.
        """
        start_server(port=port, host=host)

    def stop_server(self, port: int) -> None:
        """
        Останавливает FastAPI сервер.

        Args:
            port (int): Порт для остановки сервера.
        """
        stop_server(port=port)

    def stop_all_servers(self) -> None:
        """Останавливает все FastAPI сервера."""
        stop_all_servers()

    def status_servers(self) -> None:
        """Выводит статус всех FastAPI серверов."""
        status_servers()

    def get_routes(self) -> None:
        """Выводит все маршруты FastAPI сервера."""
        get_routes()

    def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"]) -> None:
        """
        Добавляет новый маршрут к FastAPI серверу.

        Args:
            path (str): Путь маршрута.
            module_name (str): Имя модуля, содержащего функцию для маршрута.
            func_name (str): Имя функции, обрабатывающей маршрут.
            methods (List[str], optional): Список HTTP методов для маршрута. По умолчанию ["GET"].
        """
        add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)

    def shutdown(self) -> None:
        """Останавливает все сервера и завершает работу RPC сервера."""
        self.stop_all_servers()
        self.rpc_server.shutdown()
        print("RPC server shutdown")
        sys.exit(0)


def display_menu() -> None:
    """Выводит меню с доступными командами."""
    print("\nAvailable commands:")
    print("  start <port>        - Start server on the specified port")
    print("  status              - Show all served ports status")
    print("  routes              - Show all registered routes")
    print("  stop <port>         - Stop server on the specified port")
    print("  stop_all            - Stop all servers")
    print("  add_route <path>    - Add a new route to the server")
    print("  shutdown            - Stop all servers and exit")
    print("  help                - Show this help menu")
    print("  exit                - Exit the program")


def main() -> None:
    """Основная функция управления сервером."""
    command_handler: CommandHandler = CommandHandler()
    while True:
        display_menu()
        try:
            command_line: str = input("Enter command: ").strip().lower()
            if not command_line:
                continue

            parts: List[str] = command_line.split()
            command: str = parts[0]

            if command == "start":
                if len(parts) != 2:
                    print("Usage: start <port>")
                    continue
                try:
                    port: int = int(parts[1])
                    host: str = input("Enter host address (default: 127.0.0.1): ").strip() or "127.0.0.1"
                    command_handler.start_server(port=port, host=host)
                except ValueError:
                    print("Invalid port number.")
                except Exception as ex:
                    logger.error("An error occurred:", ex, exc_info=True)

            elif command == "status":
                command_handler.status_servers()

            elif command == "routes":
                command_handler.get_routes()

            elif command == "stop":
                if len(parts) != 2:
                    print("Usage: stop <port>")
                    continue
                try:
                    port: int = int(parts[1])
                    command_handler.stop_server(port=port)
                except ValueError:
                    print("Invalid port number.")
                except Exception as ex:
                    logger.error("An error occurred:", ex, exc_info=True)

            elif command == "stop_all":
                command_handler.stop_all_servers()

            elif command == "add_route":
                if len(parts) < 2:
                    print("Usage: add_route <path> <module_name> <func_name>")
                    continue
                path: str = parts[1]
                module_name: str = input("Enter module name: ").strip()
                func_name: str = input("Enter function name: ").strip()
                methods_str: str = input("Enter HTTP methods (comma-separated, default: GET): ").strip().upper() or "GET"
                methods: List[str] = [method.strip() for method in methods_str.split(",")]
                command_handler.add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)

            elif command == "shutdown":
                command_handler.shutdown()  # call shutdown method on command_handler

            elif command == "help":
                display_menu()

            elif command == "exit":
                print("Exiting the program.")
                sys.exit(0)

            else:
                print("Unknown command. Type 'help' to see the list of available commands")

        except Exception as ex:
            logger.error("An error occurred:", ex, exc_info=True)


if __name__ == "__main__":
    main()