# Модуль FastAPI сервера с XML-RPC интерфейсом для удалённого управления
====================================================

Модуль содержит класс `FastApiServer`, который реализует FastAPI сервер с интерфейсом XML-RPC для удалённого управления.
Он также содержит функции для запуска, остановки и управления сервером через командную строку или XML-RPC.

## Обзор

Этот модуль реализует FastAPI сервер с возможностью удалённого управления через XML-RPC. Он предоставляет функциональность для динамического добавления маршрутов, управления сервером через командную строку и XML-RPC, а также мониторинга состояния сервера. Модуль использует конфигурационный файл `fast_api.json` для настройки параметров сервера, таких как хост и порты.

## Подробнее

Модуль предназначен для создания и управления FastAPI сервером, который может быть использован для различных целей, таких как предоставление API для других приложений или сервисов. Он предоставляет удобный интерфейс для управления сервером через командную строку или XML-RPC, что позволяет автоматизировать процессы развёртывания и управления сервером.

## Классы

### `FastApiServer`

**Описание**: Класс, реализующий FastAPI сервер с функциональностью Singleton.

**Наследует**: Не наследует другие классы.

**Атрибуты**:
- `_instance`: Приватный атрибут, хранящий единственный экземпляр класса.
- `app` (FastAPI): FastAPI приложение.
- `host` (str): Хост сервера. По умолчанию берётся из конфигурационного файла.
- `port` (int): Порт сервера. По умолчанию 8000.
- `router` (APIRouter): APIRouter для добавления маршрутов.
- `server_tasks` (dict): Словарь для хранения задач сервера.
- `servers` (dict): Словарь для хранения серверов.

**Методы**:
- `__new__(cls, *args, **kwargs)`: Создаёт и возвращает единственный экземпляр класса.
- `__init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs)`: Инициализирует экземпляр класса, добавляет маршруты `/hello` и `/post`, и включает роутер в приложение FastAPI.
- `add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs)`: Добавляет маршрут к FastAPI приложению.
- `_start_server(self, port: int)`: Запускает uvicorn сервер асинхронно.
- `start(self, port: int, as_thread: bool = True)`: Запускает FastAPI сервер на указанном порту.
- `stop(self, port: int)`: Останавливает FastAPI сервер на указанном порту.
- `stop_all(self)`: Останавливает все запущенные сервера.
- `get_servers_status(self)`: Возвращает статус всех серверов.
- `get_routes(self)`: Возвращает список всех роутов.
- `get_app(self)`: Возвращает FastAPI приложение.
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs)`: Добавляет новый маршрут к уже работающему приложению, динамически импортируя модуль и функцию.

**Принцип работы**:

Класс `FastApiServer` реализован как Singleton, что гарантирует наличие только одного экземпляра сервера в приложении. При инициализации создается FastAPI приложение, настраивается роутер и добавляются стандартные маршруты. Методы `start` и `stop` позволяют запускать и останавливать сервер на указанных портах. Метод `add_route` используется для добавления новых маршрутов в приложение.

### `CommandHandler`

**Описание**: Обработчик команд для FastAPI сервера через XML-RPC.

**Наследует**: Не наследует другие классы.

**Атрибуты**:
- `rpc_port` (int): Порт для XML-RPC сервера. По умолчанию 9000.
- `rpc_server` (SimpleXMLRPCServer): Экземпляр XML-RPC сервера.

**Методы**:
- `__init__(self, rpc_port=9000)`: Инициализирует XML-RPC сервер и регистрирует экземпляр класса для обработки RPC вызовов.
- `start_server(self, port: int, host: str)`: Запускает FastAPI сервер на указанном порту и хосте.
- `stop_server(self, port: int)`: Останавливает FastAPI сервер на указанном порту.
- `stop_all_servers(self)`: Останавливает все запущенные FastAPI сервера.
- `status_servers(self)`: Показывает статус серверов.
- `get_routes(self)`: Возвращает список всех роутов.
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"])`: Добавляет новый роут к серверу.
- `shutdown(self)`: Останавливает все сервера и выключает XML-RPC сервер.

**Принцип работы**:

Класс `CommandHandler` предоставляет интерфейс для управления FastAPI сервером через XML-RPC. При инициализации создается XML-RPC сервер, который слушает указанный порт и регистрирует методы класса для удалённого вызова. Методы класса вызывают соответствующие функции для управления сервером.

## Функции

### `telegram_webhook`

```python
def telegram_webhook():
    """"""
    return \'Hello, World!\'
```

**Назначение**: Обработчик webhook для Telegram (в данный момент просто возвращает "Hello, World!").

**Параметры**: Нет параметров.

**Возвращает**:
- `str`: Строка "Hello, World!".

**Как работает функция**:
Функция просто возвращает строку "Hello, World!".

**Примеры**:
```python
result = telegram_webhook()
print(result)  # Вывод: Hello, World!
```

### `test_function`

```python
def test_function():
    return "It is working!!!"
```

**Назначение**: Тестовая функция, возвращающая строку "It is working!!!".

**Параметры**: Нет параметров.

**Возвращает**:
- `str`: Строка "It is working!!!".

**Как работает функция**:
Функция просто возвращает строку "It is working!!!".

**Примеры**:
```python
result = test_function()
print(result)  # Вывод: It is working!!!
```

### `test_post`

```python
def test_post(data: Dict[str, str]):
    return {"result": "post ok", "data": data}
```

**Назначение**: Тестовая функция для обработки POST запросов, возвращающая словарь с результатом и данными.

**Параметры**:
- `data` (Dict[str, str]): Словарь с данными, переданными в POST запросе.

**Возвращает**:
- `dict`: Словарь с результатом "post ok" и переданными данными.

**Как работает функция**:
Функция принимает словарь `data` и возвращает новый словарь, содержащий результат "post ok" и переданные данные.

**Примеры**:
```python
data = {"key1": "value1", "key2": "value2"}
result = test_post(data)
print(result)  # Вывод: {'result': 'post ok', 'data': {'key1': 'value1', 'key2': 'value2'}}
```

### `start_server`

```python
def start_server(port: int, host: str):
    """Запускает FastAPI сервер на указанном порту."""
    global _api_server_instance
    if _api_server_instance is None:
        _api_server_instance = FastApiServer(host=host)
    try:
      _api_server_instance.start(port=port)
    except Exception as ex:
      logger.error(f"Ошибка запуска FastAPI сервера на порту {port}:",ex, exc_info=True)
```

**Назначение**: Запускает FastAPI сервер на указанном порту.

**Параметры**:
- `port` (int): Порт для запуска сервера.
- `host` (str): Хост для запуска сервера.

**Как работает функция**:
Функция проверяет, инициализирован ли экземпляр `FastApiServer`. Если нет, то создает его. Затем вызывает метод `start` для запуска сервера на указанном порту. В случае ошибки логирует сообщение об ошибке.

**Примеры**:
```python
start_server(port=8000, host="127.0.0.1")
```

### `stop_server`

```python
def stop_server(port: int):
    """Останавливает FastAPI сервер на указанном порту."""
    global _api_server_instance
    if _api_server_instance:
        try:
            _api_server_instance.stop(port=port)
        except Exception as ex:
            logger.error(f"Ошибка остановки FastAPI сервера на порту {port}:",ex, exc_info=True)
```

**Назначение**: Останавливает FastAPI сервер на указанном порту.

**Параметры**:
- `port` (int): Порт сервера для остановки.

**Как работает функция**:
Функция проверяет, инициализирован ли экземпляр `FastApiServer`. Если да, то вызывает метод `stop` для остановки сервера на указанном порту. В случае ошибки логирует сообщение об ошибке.

**Примеры**:
```python
stop_server(port=8000)
```

### `stop_all_servers`

```python
def stop_all_servers():
    """Останавливает все запущенные FastAPI сервера."""
    global _api_server_instance
    if _api_server_instance:
      try:
        _api_server_instance.stop_all()
      except Exception as ex:
        logger.error(f"Ошибка остановки всех FastAPI серверов:",ex, exc_info=True)
```

**Назначение**: Останавливает все запущенные FastAPI сервера.

**Параметры**: Нет параметров.

**Как работает функция**:
Функция проверяет, инициализирован ли экземпляр `FastApiServer`. Если да, то вызывает метод `stop_all` для остановки всех серверов. В случае ошибки логирует сообщение об ошибке.

**Примеры**:
```python
stop_all_servers()
```

### `status_servers`

```python
def status_servers():
    """Показывает статус серверов."""
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
```

**Назначение**: Показывает статус серверов.

**Параметры**: Нет параметров.

**Как работает функция**:
Функция проверяет, инициализирован ли экземпляр `FastApiServer`. Если да, то вызывает метод `get_servers_status` для получения статуса всех серверов. Затем выводит информацию о статусе серверов.

**Примеры**:
```python
status_servers()
```

### `get_routes`

```python
def get_routes():
    """Показывает все роуты."""
    global _api_server_instance
    if _api_server_instance:
      routes = _api_server_instance.get_routes()
      if routes:
        print("Available routes:")
        for route in routes:
          print(f"  - Path: {route[\'path\']}, Methods: {route[\'methods']}")
      else:
        print("No routes defined")
    else:
        print("Server not initialized.")
```

**Назначение**: Показывает все роуты.

**Параметры**: Нет параметров.

**Как работает функция**:
Функция проверяет, инициализирован ли экземпляр `FastApiServer`. Если да, то вызывает метод `get_routes` для получения списка всех роутов. Затем выводит информацию о роутах.

**Примеры**:
```python
get_routes()
```

### `add_new_route`

```python
def add_new_route(path: str, module_name: str, func_name: str, methods: List[str] = ["GET"]):
    """Добавляет новый роут к серверу."""
    global _api_server_instance
    if _api_server_instance:
      try:
          _api_server_instance.add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)
          print(f"Route added: {path}, {methods=}")
      except Exception as ex:
        logger.error(f"Ошибка добавления нового роута {path}:",ex, exc_info=True)
    else:
        print("Server not initialized. Start server first")
```

**Назначение**: Добавляет новый роут к серверу.

**Параметры**:
- `path` (str): Путь для нового роута.
- `module_name` (str): Имя модуля, содержащего функцию для роута.
- `func_name` (str): Имя функции, которая будет обрабатывать запросы к роуту.
- `methods` (List[str]): Список HTTP методов, поддерживаемых роутом.

**Как работает функция**:
Функция проверяет, инициализирован ли экземпляр `FastApiServer`. Если да, то вызывает метод `add_new_route` для добавления нового роута. В случае ошибки логирует сообщение об ошибке.

**Примеры**:
```python
add_new_route(path="/new_route", module_name="my_module", func_name="my_function", methods=["GET", "POST"])
```

### `parse_port_range`

```python
def parse_port_range(range_str):
    """Разбирает строку с диапазоном портов."""
    if not re.match(r\'^[\\d-]+$\', range_str):\n        print(f"Invalid port range: {range_str}")\n        return []\n    if \'-\' in range_str:\n        try:\n            start, end = map(int, range_str.split(\'-\'))\n            if start > end:\n                raise ValueError("Invalid port range")\n            return list(range(start, end + 1))\n        except ValueError:\n            print(f"Invalid port range: {range_str}")\n            return []\n    else:\n        try:\n            return [int(range_str)]\n        except ValueError:\n            print(f"Invalid port: {range_str}")\n            return []
```

**Назначение**: Разбирает строку с диапазоном портов.

**Параметры**:
- `range_str` (str): Строка с диапазоном портов (например, "8000-8005" или "8000").

**Возвращает**:
- `List[int]`: Список портов.

**Как работает функция**:
Функция проверяет, соответствует ли строка диапазону портов. Если строка содержит дефис, то разбирает её на начало и конец диапазона. Если строка не содержит дефис, то пытается преобразовать её в целое число. В случае ошибки выводит сообщение об ошибке и возвращает пустой список.

**Примеры**:
```python
ports = parse_port_range("8000-8005")
print(ports)  # Вывод: [8000, 8001, 8002, 8003, 8004, 8005]

ports = parse_port_range("8000")
print(ports)  # Вывод: [8000]

ports = parse_port_range("invalid")
print(ports)  # Вывод: []
```

### `display_menu`

```python
def display_menu():
    """Выводит меню с доступными командами."""
    print("\\nAvailable commands:")
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

**Назначение**: Выводит меню с доступными командами.

**Параметры**: Нет параметров.

**Как работает функция**:
Функция просто выводит список доступных команд в консоль.

**Примеры**:
```python
display_menu()
```

### `main`

```python
def main():
    """Основная функция управления сервером."""
    command_handler = CommandHandler()\n    while True:\n        display_menu()\n        try:\n            command_line = input("Enter command: ").strip().lower()\n            if not command_line:\n                continue\n\n            parts = command_line.split()\n            command = parts[0]\n\n            if command == "start":\n                if len(parts) != 2:\n                    print("Usage: start <port>")\n                    continue\n                try:\n                    port = int(parts[1])\n                    host = input("Enter host address (default: 127.0.0.1): ").strip() or "127.0.0.1"\n                    command_handler.start_server(port=port, host=host)\n                except ValueError:\n                    print("Invalid port number.")\n                except Exception as ex:\n                    logger.error(f"An error occurred:", ex, exc_info=True)\n\n            elif command == "status":\n                command_handler.status_servers()\n\n            elif command == "routes":\n                command_handler.get_routes()\n            \n            elif command == "stop":\n               if len(parts) != 2:\n                   print("Usage: stop <port>")\n                   continue\n               try:\n                    port = int(parts[1])\n                    command_handler.stop_server(port=port)\n               except ValueError:\n                   print("Invalid port number.")\n               except Exception as ex:\n                  logger.error(f"An error occurred:", ex, exc_info=True)\n            \n            elif command == "stop_all":\n               command_handler.stop_all_servers()\n            \n            elif command == "add_route":\n                if len(parts) < 2:\n                    print("Usage: add_route <path> <module_name> <func_name>")\n                    continue\n                path = parts[1]\n                module_name = input("Enter module name: ").strip()\n                func_name = input("Enter function name: ").strip()\n                methods = input("Enter HTTP methods (comma-separated, default: GET): ").strip().upper() or "GET"\n                methods = [method.strip() for method in methods.split(",")]\n                command_handler.add_new_route(path=path, module_name=module_name, func_name=func_name, methods=methods)\n\n\n            elif command == "shutdown":\n                command_handler.shutdown()  # call shutdown method on command_handler\n\n            elif command == "help":\n                display_menu()\n\n            elif command == "exit":\n                print("Exiting the program.")\n                sys.exit(0)\n            \n            else:\n                print("Unknown command. Type \'help\' to see the list of available commands")\n\n        except Exception as ex:\n            logger.error(f"An error occurred:", ex, exc_info=True)
```

**Назначение**: Основная функция управления сервером через командную строку.

**Как работает функция**:
Функция создает экземпляр `CommandHandler`, выводит меню с доступными командами и ожидает ввода пользователя. В зависимости от введенной команды вызывает соответствующие методы `CommandHandler` для управления сервером. Функция работает в бесконечном цикле, пока пользователь не введет команду `exit` или `shutdown`.
В цикле обрабатываются следующие команды:
- `start`: Запускает сервер на указанном порту.
- `status`: Показывает статус всех серверов.
- `routes`: Показывает все зарегистрированные маршруты.
- `stop`: Останавливает сервер на указанном порту.
- `stop_all`: Останавливает все запущенные серверы.
- `add_route`: Добавляет новый маршрут к серверу.
- `shutdown`: Останавливает все серверы и завершает программу.
- `help`: Выводит меню с доступными командами.
- `exit`: Завершает программу.

**Внутренние функции**: Внутри функции `main` нет внутренних функций.

**Примеры**:
Запуск программы и ввод команд:
```
python fast_api.py
```
```
Enter command: start 8000
Enter host address (default: 127.0.0.1): 
```
```
Enter command: status
```

## Параметры класса

- `host` (str): Более подробное Описание параметра `host`.
- `port` (Optional[int], optional): Более подробное Описание параметра `port`. По умолчанию `None`.