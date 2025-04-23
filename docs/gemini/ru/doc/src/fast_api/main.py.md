# Модуль управления параметрами Fast API сервера

## Обзор

Модуль `src.fast_api.main` предоставляет функциональность для управления Fast API сервером, включая запуск, остановку, получение статуса и добавление новых маршрутов. Он включает в себя функцию `main`, которая обрабатывает команды, вводимые пользователем через консоль.

## Подробнее

Этот модуль является основным входным файлом для управления сервером Fast API. Он использует класс `CommandHandler` из модуля `src.fast_api.fast_api` для выполнения различных операций с сервером.
Модуль предоставляет интерфейс командной строки для управления сервером, позволяя пользователям запускать, останавливать, получать статус серверов, а также добавлять новые маршруты.

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

**Назначение**: Выводит в консоль список доступных команд для управления сервером.

**Параметры**: Нет.

**Возвращает**: Нет.

**Вызывает исключения**: Нет.

**Как работает функция**:

- Функция выводит список доступных команд и их описание в консоль.

**Примеры**:

```python
display_menu()
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
                print("Unknown command. Type \'help\' to see the list of available commands")

        except Exception as ex:
            logger.error(f"An error occurred:", ex, exc_info=True)
```

**Назначение**: Основная функция управления сервером, обрабатывает команды пользователя.

**Параметры**: Нет.

**Возвращает**: Нет.

**Вызывает исключения**:
- `ValueError`: Если введен некорректный номер порта.
- `Exception`: При возникновении других ошибок.

**Как работает функция**:

1.  Создает экземпляр класса `CommandHandler`.
2.  Входит в бесконечный цикл, в котором:
    *   Вызывает функцию `display_menu` для отображения доступных команд.
    *   Запрашивает ввод команды от пользователя.
    *   Разделяет введенную строку на части, чтобы определить команду и аргументы.
    *   Выполняет различные действия в зависимости от введенной команды:
        *   `start`: Запускает сервер на указанном порту. Запрашивает у пользователя хост, если он не указан, использует "127.0.0.1" по умолчанию.
        *   `status`: Выводит статус всех серверов.
        *   `routes`: Выводит список всех зарегистрированных маршрутов.
        *   `stop`: Останавливает сервер на указанном порту.
        *   `stop_all`: Останавливает все серверы.
        *   `add_route`: Добавляет новый маршрут к серверу. Запрашивает у пользователя HTTP методы, если они не указаны, использует "GET" по умолчанию.
        *   `shutdown`: Останавливает все серверы и завершает работу программы.
        *   `help`: Выводит меню с доступными командами.
        *   `exit`: Завершает работу программы.
        *   Если введена неизвестная команда, выводит сообщение об ошибке.
    *   Обрабатывает исключения, которые могут возникнуть при выполнении команд, и логирует их с использованием `logger.error`.

**Примеры**:

```python
main()