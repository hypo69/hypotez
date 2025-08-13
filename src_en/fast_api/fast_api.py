# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Fastapi server with XML-RPC interface for remote control
===============================================================

.. Module :: src.fast_api.fast_api_rpc
    : Platform: Windows, Unix
    : synopsis: Fastapi server with XML-RPC interface for remote control"""
import asyncio
import functools
import json
import os
import sys
import threading
from types import SimpleNamespace
from typing import List, Callable, Dict
from pathlib import Path
from contextlib import asynccontextmanager
from xmlrpc.server import SimpleXMLRPCServer
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, APIRouter
import importlib  # Added for dynamic imports

import header  # <- Mandatory import
from header import __root__
from src.fast_api.routes import Routes
from src import gs
from src.utils.jjson import j_loads, j_loads_ns
from src.utils.printer import pprint as print
from src.logger import logger

route_functions = Routes()

import re

load_dotenv()


try:
    config: SimpleNamespace = j_loads_ns(__root__ / 'src' / 'fast_api' / 'fast_api.json')
    config.ports: list = config.ports if isinstance(config.ports, list) else [config.ports]
except Exception as ex:
    logger.critical(f"Config file not found!")
    sys.exit()

_api_server_instance = None


class FastApiServer:
    """Fastapi server with Singleton implementation."""

    _instance = None
    app: FastAPI = FastAPI()
    host: str = config.host
    port: int = 8000
    router: APIRouter = APIRouter()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.add_route("/hello", test_function)
        self.add_route("/post", test_post, methods=["POST"])
        # self.add_route("/telegram_webhook", telegram_webhook, methods=["POST"])

        self.app = FastAPI()
        self.host = host or config.host
        self.server_tasks = {}
        self.servers = {}
        self.app.include_router(self.router)

    def add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs):
        """Adds the route to Fastapi to the application."""
        try:
            self.router.add_api_route(path, func, methods=methods, **kwargs)
            logger.info(f"Маршрут {path} зарегистрирван")
        except Exception as ex:
            logger.error(f"Ошибка добавления маршрута {path}", exc_info=True)

    async def _start_server(self, port: int):
        """The uvicorn server triggers asynchronously."""
        config = uvicorn.Config(self.app, host=self.host, port=port, log_level="debug")
        server = uvicorn.Server(config)
        try:
            await server.serve()
            logger.success(f"Server started on: {self.host}:{port}")
        except Exception as e:
            logger.error(f"Error running server on port {port}: {e}", exc_info=True)
        finally:
            self.servers.pop(port, None)

    def start(self, port: int, as_thread:bool = True):
        """Laits the Fastapi server on the specified port."""
        if port in self.servers:
            print(f"Server already running on port {port}")
            return

        task = threading.Thread(target=asyncio.run, args=(self._start_server(port),), daemon=True)
        self.server_tasks[port] = task
        self.servers[port] = task
        task.start()

    def stop(self, port: int):
        """Stops the Fastapi server on the specified port."""
        if port in self.servers:
            try:
                self.servers[port]._thread.join(1)
                self.servers.pop(port)
                print(f"Server on port {port} stopped.")
            except Exception as e:
                logger.error(f"Error stopping server on port {port}: {e}", exc_info=True)
        else:
            print(f"Server on port {port} is not running or already stopped.")

    def stop_all(self):
        """Stops all the running servers."""
        for port in list(self.servers):
            self.stop(port)

    def get_servers_status(self):
        """Returns the status of all servers."""
        return {port: "Running" if task.is_alive() else "Stopped" for port, task in self.servers.items()}

    def get_routes(self):
      """Returns a list of all routes."""
      routes = []
      for route in self.app.routes:
          if hasattr(route, "path"):
            methods = getattr(route, "methods", ["GET"])
            routes.append({"path": route.path, "methods": list(methods)})
      return routes

    def get_app(self):
        """Returns Fastapi application."""
        return self.app

    def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs):
        """Adds a new route to an already working application."""
        try:
            # Dynamically import the module
            module = importlib.import_module(module_name)
            # We get a function from the module
            func = getattr(module, func_name, None)
            if func is None:
                raise AttributeError(f"Function '{func_name}' not found in module '{module_name}'")
            
            self.add_route(path, func, methods=methods, **kwargs)
            logger.info(f"Маршрут {path} зарегистрирован из модуля {module_name}")
        except Exception as ex:
            logger.error(f"Ошибка добавления маршрута {path} из модуля {module_name}: {ex}", exc_info=True)


def telegram_webhook():
    """"""
    return 'Hello, World!'


def test_function():
    return "It is working!!!"


def test_post(data: Dict[str, str]):
    return {"result": "post ok", "data": data}


def start_server(port: int, host: str):
    """Laits the Fastapi server on the specified port."""
    global _api_server_instance
    if _api_server_instance is None:
        _api_server_instance = FastApiServer(host=host)
    try:
      _api_server_instance.start(port=port)
    except Exception as ex:
      logger.error(f"Ошибка запуска FastAPI сервера на порту {port}:",ex, exc_info=True)


def stop_server(port: int):
    """Stops the Fastapi server on the specified port."""
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.stop(port=port)
        except Exception as ex:
            logger.error(f"Ошибка остановки FastAPI сервера на порту {port}:",ex, exc_info=True)


def stop_all_servers():
    """Stops all the running server running Fastapi."""
    global _api_server_instance
    if _api_server_instance:
      try:
        _api_server_instance.stop_all()
      except Exception as ex:
        logger.error(f"Ошибка остановки всех FastAPI серверов:",ex, exc_info=True)


def status_servers():
    """Shows the status of servers."""
    global _api_server_instance
    if _api_server_instance:
        servers = _api_server_instance.get_servers_status()
        if servers:
            print(f"Server initialized on host {_api_server_instance.host}")
            for port, status in servers.items():
                print(f"  - Port {port}: {status}")
        else:
            print("No servers running")
    else:
        print("Server not initialized.")

def get_routes():
    """Shows all the routes."""
    global _api_server_instance
    if _api_server_instance:
      routes = _api_server_instance.get_routes()
      if routes:
        print("Available routes:")
        for route in routes:
          print(f"  - Path: {route['path']}, Methods: {route['methods']}")
      else:
        print("No routes defined")
    else:
        print("Server not initialized.")


def add_new_route(path: str, module_name: str, func_name: str, methods: List[str] = ["GET"]):
    """Adds a new Rout to the server."""
    global _api_server_instance
    if _api_server_instance:
      try:
          _api_server_instance.add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)
          print(f"Route added: {path}, {methods=}")
      except Exception as ex:
        logger.error(f"Ошибка добавления нового роута {path}:",ex, exc_info=True)
    else:
        print("Server not initialized. Start server first")


def parse_port_range(range_str):
    """Disassembles the line with the port range."""
    if not re.match(r'^[\d-]+$', range_str):
        print(f"Invalid port range: {range_str}")
        return []
    if '-' in range_str:
        try:
            start, end = map(int, range_str.split('-'))
            if start > end:
                raise ValueError("Invalid port range")
            return list(range(start, end + 1))
        except ValueError:
            print(f"Invalid port range: {range_str}")
            return []
    else:
        try:
            return [int(range_str)]
        except ValueError:
            print(f"Invalid port: {range_str}")
            return []


class CommandHandler:
    """Team handler for Fastapi server via XML-RPC."""

    def __init__(self, rpc_port=9000):
        self.rpc_port = rpc_port
        self.rpc_server = SimpleXMLRPCServer(("localhost", self.rpc_port), allow_none=True)
        self.rpc_server.register_instance(self)
        threading.Thread(target=self.rpc_server.serve_forever, daemon=True).start()
        print(f"RPC server started on port: {self.rpc_port}")

    def start_server(self, port: int, host: str):
        start_server(port=port, host=host)

    def stop_server(self, port: int):
        stop_server(port=port)

    def stop_all_servers(self):
        stop_all_servers()

    def status_servers(self):
        status_servers()

    def get_routes(self):
        get_routes()

    def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"]):
        add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)

    def shutdown(self):
        self.stop_all_servers()
        self.rpc_server.shutdown()
        print("RPC server shutdown")
        sys.exit(0)


def display_menu():
    """Displays a menu with available commands."""
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


def main():
    """The main function of server management."""
    command_handler = CommandHandler()
    while True:
        display_menu()
        try:
            command_line = input("Enter command: ").strip().lower()
            if not command_line:
                continue

            parts = command_line.split()
            command = parts[0]

            if command == "start":
                if len(parts) != 2:
                    print("Usage: start <port>")
                    continue
                try:
                    port = int(parts[1])
                    host = input("Enter host address (default: 127.0.0.1): ").strip() or "127.0.0.1"
                    command_handler.start_server(port=port, host=host)
                except ValueError:
                    print("Invalid port number.")
                except Exception as ex:
                    logger.error(f"An error occurred:", ex, exc_info=True)

            elif command == "status":
                command_handler.status_servers()

            elif command == "routes":
                command_handler.get_routes()
            
            elif command == "stop":
               if len(parts) != 2:
                   print("Usage: stop <port>")
                   continue
               try:
                    port = int(parts[1])
                    command_handler.stop_server(port=port)
               except ValueError:
                   print("Invalid port number.")
               except Exception as ex:
                  logger.error(f"An error occurred:", ex, exc_info=True)
            
            elif command == "stop_all":
               command_handler.stop_all_servers()
            
            elif command == "add_route":
                if len(parts) < 2:
                    print("Usage: add_route <path> <module_name> <func_name>")
                    continue
                path = parts[1]
                module_name = input("Enter module name: ").strip()
                func_name = input("Enter function name: ").strip()
                methods = input("Enter HTTP methods (comma-separated, default: GET): ").strip().upper() or "GET"
                methods = [method.strip() for method in methods.split(",")]
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
            logger.error(f"An error occurred:", ex, exc_info=True)


if __name__ == "__main__":
    main()