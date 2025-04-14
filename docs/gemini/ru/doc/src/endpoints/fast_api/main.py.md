# Модуль управления Fast API сервером

## Обзор

Модуль `src.fast_api.main` предоставляет интерфейс командной строки для управления сервером Fast API. Он позволяет запускать, останавливать, просматривать статус и добавлять новые маршруты к серверу.

## Подробнее

Этот модуль предназначен для управления Fast API сервером через командную строку. Он предоставляет набор команд для выполнения различных операций, таких как запуск сервера на определенном порту, отображение статуса серверов, добавление новых маршрутов и остановка серверов. Основной функцией модуля является `main`, которая обрабатывает ввод пользователя и вызывает соответствующие методы класса `CommandHandler` для выполнения запрошенных действий.

## Функции

### `display_menu`

```python
def display_menu():
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
```

**Назначение**: Выводит на экран меню с перечнем доступных команд для управления сервером.

**Параметры**: Отсутствуют.

**Возвращает**: Ничего (None).

**Как работает функция**: Функция `display_menu` выводит в консоль список доступных команд и их описание. Этот список включает команды для запуска, остановки, просмотра статуса и добавления новых маршрутов к серверу Fast API.

**Примеры**:

```python
display_menu()
# Вывод в консоль:
# Available commands:
#   start <port>        - Start server on the specified port
#   status              - Show all served ports status
#   routes              - Show all registered routes
#   stop <port>         - Stop server on the specified port
#   stop_all            - Stop all servers
#   add_route <path>    - Add a new route to the server
#   shutdown            - Stop all servers and exit
#   help                - Show this help menu
#   exit                - Exit the program
```

### `main`

```python
def main():
    """Основная функция управления сервером."""
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
                if len(parts) != 2:
                    print("Usage: add_route <path>")
                    continue
                path = parts[1]
                methods = input("Enter HTTP methods (comma-separated, default: GET): ").strip().upper() or "GET"
                methods = [method.strip() for method in methods.split(",")]
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
            logger.error(f"An error occurred:", ex, exc_info=True)
```

**Назначение**: Основная функция, управляющая сервером Fast API через командную строку.

**Параметры**: Отсутствуют.

**Возвращает**: Ничего (None).

**Как работает функция**:

1.  Создает экземпляр класса `CommandHandler`.
2.  В бесконечном цикле:
    *   Вызывает функцию `display_menu` для отображения доступных команд.
    *   Запрашивает ввод команды от пользователя.
    *   Обрабатывает введенную команду:
        *   Если команда `start`: запрашивает номер порта и хост, затем вызывает метод `start_server` объекта `command_handler`.
        *   Если команда `status`: вызывает метод `status_servers` объекта `command_handler`.
        *   Если команда `routes`: вызывает метод `get_routes` объекта `command_handler`.
        *   Если команда `stop`: запрашивает номер порта и вызывает метод `stop_server` объекта `command_handler`.
        *   Если команда `stop_all`: вызывает метод `stop_all_servers` объекта `command_handler`.
        *   Если команда `add_route`: запрашивает путь и HTTP методы, затем вызывает метод `add_new_route` объекта `command_handler`.
        *   Если команда `shutdown`: вызывает метод `stop_all_servers` объекта `command_handler` и завершает работу программы.
        *   Если команда `help`: вызывает функцию `display_menu`.
        *   Если команда `exit`: завершает работу программы.
        *   Если команда неизвестна: выводит сообщение об ошибке.
    *   Обрабатывает возможные исключения и логирует их с помощью `logger.error`.

**Примеры**:

```python
# Запуск сервера на порту 8000
# Ввод пользователя: start 8000
# Запрос хоста: Enter host address (default: 127.0.0.1):
# (если пользователь ничего не введет, будет использован хост по умолчанию 127.0.0.1)
# После успешного запуска в консоли будет отображено сообщение от command_handler.start_server
```

```python
# Отображение статуса серверов
# Ввод пользователя: status
# После выполнения в консоли будет отображен статус серверов, полученный от command_handler.status_servers()
```

```python
# Добавление нового маршрута /test с методом POST
# Ввод пользователя: add_route /test
# Запрос методов: Enter HTTP methods (comma-separated, default: GET): POST
# После успешного добавления маршрута в консоли будет отображено сообщение от command_handler.add_new_route
```