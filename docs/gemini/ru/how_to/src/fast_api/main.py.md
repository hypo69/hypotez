### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой основную функцию управления сервером `FastAPI`. Он включает в себя отображение меню доступных команд, обработку ввода пользователя и выполнение соответствующих действий, таких как запуск, остановка и настройка серверов.

Шаги выполнения
-------------------------
1. **Определение функции `display_menu()`**:
   - Функция выводит на экран список доступных команд для управления сервером `FastAPI`.

2. **Определение функции `main()`**:
   - Создается экземпляр класса `CommandHandler`, который управляет серверами.
   - Запускается бесконечный цикл `while True`, в котором происходит обработка команд пользователя.
   - Вызывается функция `display_menu()` для отображения списка доступных команд.

3. **Обработка ввода пользователя**:
   - Пользователю предлагается ввести команду.
   - Введенная команда преобразуется в нижний регистр и удаляются лишние пробелы.
   - Если введена пустая строка, цикл продолжается.
   - Команда разделяется на части по пробелам.

4. **Выполнение команд**:
   - **`start`**:
     - Проверяется, что введено достаточно аргументов (должен быть указан порт).
     - Извлекается номер порта из ввода пользователя.
     - Запрашивается адрес хоста (по умолчанию `127.0.0.1`).
     - Вызывается метод `start_server` объекта `command_handler` для запуска сервера на указанном порту и хосте.
     - Обрабатываются исключения, если введен некорректный номер порта или произошла другая ошибка.
   - **`status`**:
     - Вызывается метод `status_servers` объекта `command_handler` для отображения статуса всех серверов.
   - **`routes`**:
     - Вызывается метод `get_routes` объекта `command_handler` для отображения всех зарегистрированных маршрутов.
   - **`stop`**:
     - Проверяется, что введено достаточно аргументов (должен быть указан порт).
     - Извлекается номер порта из ввода пользователя.
     - Вызывается метод `stop_server` объекта `command_handler` для остановки сервера на указанном порту.
     - Обрабатываются исключения, если введен некорректный номер порта или произошла другая ошибка.
   - **`stop_all`**:
     - Вызывается метод `stop_all_servers` объекта `command_handler` для остановки всех серверов.
   - **`add_route`**:
     - Проверяется, что введено достаточно аргументов (должен быть указан путь).
     - Извлекается путь из ввода пользователя.
     - Запрашиваются HTTP-методы (по умолчанию `GET`).
     - Методы разделяются по запятым и преобразуются в верхний регистр.
     - Вызывается метод `add_new_route` объекта `command_handler` для добавления нового маршрута.
   - **`shutdown`**:
     - Вызывается метод `stop_all_servers` объекта `command_handler` для остановки всех серверов.
     - Выводится сообщение о завершении работы.
     - Программа завершается с кодом 0.
   - **`help`**:
     - Вызывается функция `display_menu()` для повторного отображения списка команд.
   - **`exit`**:
     - Выводится сообщение о завершении работы.
     - Программа завершается с кодом 0.
   - **Неизвестная команда**:
     - Выводится сообщение о неизвестной команде и предлагается ввести `help` для просмотра списка доступных команд.

5. **Обработка общих исключений**:
   - Если в процессе выполнения команд возникает исключение, оно логируется с использованием `logger.error`.

6. **Запуск основной функции**:
   - Если скрипт запускается как основная программа, вызывается функция `main()`.

Пример использования
-------------------------

```python
import sys
from src.fast_api.fast_api import CommandHandler, logger

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


if __name__ == "__main__":
    main()