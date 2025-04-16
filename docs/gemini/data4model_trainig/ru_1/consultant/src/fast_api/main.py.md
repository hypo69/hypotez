### **Анализ кода модуля `main.py`**

## \file /src/fast_api/main.py

Модуль является точкой входа для управления сервером Fast API. Он предоставляет интерфейс командной строки для запуска, остановки, просмотра статуса и добавления маршрутов к серверу.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура меню команд.
  - Обработка исключений для предотвращения аварийного завершения программы.
  - Использование `logger` для регистрации ошибок.
- **Минусы**:
  - Отсутствуют аннотации типов для параметров функций и переменных.
  - Аргументы `logger.error` не соответствуют ожидаемым.
  - Не все строки соответствуют PEP8.
  - Не все docstring переведены на русский язык.
  - `header` импортируется, но не используется.
  - Не реализован механизм Gracefull Shutdown для серверов, что может приводить к обрыву активных соединений.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Улучшить читаемость и упростить отладку, добавив аннотации типов для всех переменных и параметров функций.
2.  **Исправить аргументы `logger.error`**:
    - Изменить порядок передачи аргументов в `logger.error`, чтобы сначала передавалась строка сообщения, затем объект исключения, и `exc_info=True`.
3.  **Удалить неиспользуемые импорты**:
    - Убрать импорт `header`, так как он не используется в коде.
4.  **Добавить docstring на русском языке**:
    - Описать, что делает каждая функция.
    - Перевести существующие docstring на русский язык, чтобы соответствовать требованиям.
5.  **Добавить graceful shutdown**
    -   Реализовать Gracefull Shutdown для серверов, чтобы не обрывать активные соединения.

**Оптимизированный код:**

```python
## \file /src/fast_api/main.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль управления параметрами Fast API сервера
==============================================

Модуль предоставляет интерфейс командной строки для управления сервером Fast API,
включая запуск, остановку, просмотр статуса и добавление маршрутов.

Пример использования:
----------------------
Запустите `python src/fast_api/main.py` и следуйте инструкциям в командной строке.
"""

import sys
# import header  # <-- Обязательный импорт # Удален неиспользуемый импорт
from src.fast_api.fast_api import CommandHandler, logger
from typing import List


def display_menu() -> None:
    """
    Выводит меню с доступными командами.
    """
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
    """
    Основная функция управления сервером.
    """
    command_handler: CommandHandler = CommandHandler()  # Добавлена аннотация типа
    while True:
        display_menu()
        try:
            command_line: str = input("Enter command: ").strip().lower()  # Добавлена аннотация типа
            if not command_line:
                continue

            parts: List[str] = command_line.split()  # Добавлена аннотация типа
            command: str = parts[0]  # Добавлена аннотация типа

            if command == "start":
                if len(parts) != 2:
                    print("Usage: start <port>")
                    continue
                try:
                    port: int = int(parts[1])  # Добавлена аннотация типа
                    host: str = input("Enter host address (default: 127.0.0.1): ").strip() or "127.0.0.1"  # Добавлена аннотация типа
                    command_handler.start_server(port=port, host=host)
                except ValueError:
                    print("Invalid port number.")
                except Exception as ex:
                    logger.error("An error occurred:", ex, exc_info=True) # Исправлен порядок аргументов

            elif command == "status":
                command_handler.status_servers()

            elif command == "routes":
                command_handler.get_routes()

            elif command == "stop":
                if len(parts) != 2:
                    print("Usage: stop <port>")
                    continue
                try:
                    port: int = int(parts[1])  # Добавлена аннотация типа
                    command_handler.stop_server(port=port)
                except ValueError:
                    print("Invalid port number.")
                except Exception as ex:
                    logger.error("An error occurred:", ex, exc_info=True) # Исправлен порядок аргументов

            elif command == "stop_all":
                command_handler.stop_all_servers()

            elif command == "add_route":
                if len(parts) != 2:
                    print("Usage: add_route <path>")
                    continue
                path: str = parts[1]  # Добавлена аннотация типа
                methods_input: str = input("Enter HTTP methods (comma-separated, default: GET): ").strip().upper() or "GET"  # Добавлена аннотация типа
                methods: List[str] = [method.strip() for method in methods_input.split(",")]  # Добавлена аннотация типа
                command_handler.add_new_route(path=path, func="lambda: {\"message\": \"Hello from the new route\"}", methods=methods)


            elif command == "shutdown":
                command_handler.stop_all_servers()
                print("Shutting down all servers.")
                sys.exit(0)

            elif command == "help":
                display_menu()

            elif command == "exit":
                print("Exiting the program.")
                sys.exit(0)

            else:
                print("Unknown command. Type 'help' to see the list of available commands")

        except Exception as ex:
            logger.error("An error occurred:", ex, exc_info=True) # Исправлен порядок аргументов


if __name__ == "__main__":
    main()