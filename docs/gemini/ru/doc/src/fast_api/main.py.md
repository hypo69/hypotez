# Модуль Fast API: Управление сервером

## Обзор

Этот модуль (`src/fast_api/main.py`) предоставляет простой консольный интерфейс для управления сервером Fast API.  Он позволяет запускать, останавливать, изменять конфигурацию и выводить информацию о сервере.

## Подробней

Модуль взаимодействует с классом `CommandHandler`, который предоставляет  функционал для управления сервером Fast API.  Он позволяет запускать, останавливать, изменять конфигурацию и выводить информацию о сервере.
 Модуль `src/fast_api/fast_api` содержит класс `CommandHandler`, который предоставляет базовый функционал для управления сервером Fast API. 

## Функции

### `display_menu()`

**Назначение**: Выводит меню с доступными командами.

**Как работает функция**:
- Функция выводит список доступных команд с кратким описанием.
- Команды позволяют пользователю управлять сервером Fast API, включая запуск, остановку, настройку и получение информации о нем.

**Примеры**:
```python
>>> display_menu()
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
```

### `main()`

**Назначение**: Основная функция управления сервером.

**Как работает функция**:
-  Создается объект `command_handler` типа `CommandHandler`, который используется для взаимодействия с сервером.
- В бесконечном цикле:
    - Выводит меню доступных команд.
    - Считывает команду пользователя.
    - Разбирает команду на части.
    - Выполняет соответствующую команду, используя методы `command_handler`.
    - Обрабатывает исключения с помощью `logger`.
    - Предоставляет пользователю информацию о результатах выполнения команды.

**Параметры**: 
-  None

**Возвращает**: 
-  None

**Вызывает исключения**: 
-  `Exception`:  Возникает при возникновении необработанных ошибок во время выполнения команды.

**Примеры**:
```python
>>> main()
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program

Enter command: start 8000
Enter host address (default: 127.0.0.1): 
Server started on http://127.0.0.1:8000
```

## Примеры

**Запуск сервера:**

```
>>> main()
Enter command: start 8000
Enter host address (default: 127.0.0.1): 
Server started on http://127.0.0.1:8000
```

**Остановка сервера:**

```
>>> main()
Enter command: stop 8000
Server stopped on port 8000
```

**Добавление нового маршрута:**

```
>>> main()
Enter command: add_route /new_route
Enter HTTP methods (comma-separated, default: GET): POST
Route /new_route added with methods: ['POST']
```

**Вызов помощи:**

```
>>> main()
Enter command: help
Available commands:
  start <port>        - Start server on the specified port
  status              - Show all served ports status
  routes              - Show all registered routes
  stop <port>         - Stop server on the specified port
  stop_all            - Stop all servers
  add_route <path>    - Add a new route to the server
  shutdown            - Stop all servers and exit
  help                - Show this help menu
  exit                - Exit the program
```

**Выход из программы:**

```
>>> main()
Enter command: exit
Exiting the program.