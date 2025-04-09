# Модуль `fast_api`

## Обзор

Модуль `fast_api` представляет собой FastAPI сервер с XML-RPC интерфейсом для удалённого управления. Он позволяет запускать, останавливать и управлять FastAPI серверами через командную строку или XML-RPC вызовы.

## Подробней

Этот модуль предоставляет возможность динамического добавления новых маршрутов к уже работающему приложению, а также мониторинга статуса серверов и зарегистрированных маршрутов. Он использует конфигурационный файл `fast_api.json` для настройки параметров сервера, таких как хост и порты. Для логирования используется модуль `src.logger`.

## Классы

### `FastApiServer`

**Описание**: Класс `FastApiServer` реализует FastAPI сервер с поддержкой Singleton паттерна, обеспечивая единую точку доступа к экземпляру сервера.

**Принцип работы**:
Класс использует Singleton паттерн для создания единственного экземпляра сервера. При инициализации добавляет тестовые маршруты `/hello` и `/post`. Он позволяет добавлять новые маршруты, запускать и останавливать серверы на разных портах, а также получать информацию о статусе серверов и доступных маршрутах.

**Аттрибуты**:
- `_instance`: Приватный атрибут, хранящий единственный экземпляр класса.
- `app` (FastAPI): FastAPI приложение.
- `host` (str): Хост, на котором запускается сервер. По умолчанию берётся из конфигурационного файла.
- `port` (int): Порт, на котором запускается сервер. По умолчанию 8000.
- `router` (APIRouter): FastAPI роутер для добавления маршрутов.
- `server_tasks` (dict): Словарь, хранящий задачи серверов.
- `servers` (dict): Словарь, хранящий запущенные серверы.

**Методы**:
- `__new__(cls, *args, **kwargs)`: Создает новый экземпляр класса, если он еще не создан.
- `__init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs)`: Инициализирует экземпляр класса, добавляет маршруты `/hello` и `/post`, и включает роутер в приложение FastAPI.
- `add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs)`: Добавляет маршрут к FastAPI приложению.
- `_start_server(self, port: int)`: Запускает uvicorn сервер асинхронно.
- `start(self, port: int, as_thread: bool = True)`: Запускает FastAPI сервер на указанном порту.
- `stop(self, port: int)`: Останавливает FastAPI сервер на указанном порту.
- `stop_all(self)`: Останавливает все запущенные сервера.
- `get_servers_status(self)`: Возвращает статус всех серверов.
- `get_routes(self)`: Возвращает список всех роутов.
- `get_app(self)`: Возвращает FastAPI приложение.
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs)`: Добавляет новый маршрут к уже работающему приложению.

### `CommandHandler`

**Описание**: Класс `CommandHandler` обрабатывает команды для FastAPI сервера через XML-RPC.

**Принцип работы**:
Класс инициализирует XML-RPC сервер и регистрирует себя как экземпляр для обработки RPC вызовов. Он предоставляет методы для запуска, остановки и управления серверами, а также для получения информации о статусе серверов и маршрутах.

**Аттрибуты**:
- `rpc_port` (int): Порт для XML-RPC сервера.
- `rpc_server` (SimpleXMLRPCServer): Экземпляр XML-RPC сервера.

**Методы**:
- `__init__(self, rpc_port=9000)`: Инициализирует XML-RPC сервер и регистрирует себя как экземпляр для обработки RPC вызовов.
- `start_server(self, port: int, host: str)`: Запускает FastAPI сервер на указанном порту и хосте.
- `stop_server(self, port: int)`: Останавливает FastAPI сервер на указанном порту.
- `stop_all_servers(self)`: Останавливает все запущенные FastAPI сервера.
- `status_servers(self)`: Показывает статус серверов.
- `get_routes(self)`: Показывает все роуты.
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"])`: Добавляет новый роут к серверу.
- `shutdown(self)`: Останавливает все серверы и завершает работу RPC сервера.

## Функции

### `telegram_webhook`

```python
def telegram_webhook():
    """"""
    return 'Hello, World!'
```

**Назначение**: Функция `telegram_webhook` является обработчиком webhook для Telegram.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строку "Hello, World!".

**Как работает функция**:
1. Функция просто возвращает строку "Hello, World!".

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

**Назначение**: Функция `test_function` является тестовой функцией для проверки работоспособности сервера.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Строку "It is working!!!".

**Как работает функция**:
1. Функция просто возвращает строку "It is working!!!".

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

**Назначение**: Функция `test_post` является тестовой функцией для обработки POST запросов.

**Параметры**:
- `data` (Dict[str, str]): Словарь с данными, переданными в POST запросе.

**Возвращает**:
- `dict`: Словарь с результатом обработки POST запроса.

**Как работает функция**:
1. Функция принимает словарь `data` в качестве аргумента.
2. Функция возвращает словарь, содержащий сообщение "post ok" и переданные данные.

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

**Назначение**: Функция `start_server` запускает FastAPI сервер на указанном порту.

**Параметры**:
- `port` (int): Порт, на котором запускается сервер.
- `host` (str): Хост, на котором запускается сервер.

**Как работает функция**:

1.  Функция проверяет, инициализирован ли уже экземпляр `FastApiServer` (`_api_server_instance`). Если нет, то создается новый экземпляр `FastApiServer` с указанным хостом.
2.  Затем вызывается метод `start` экземпляра `_api_server_instance` для запуска сервера на указанном порту.
3.  Если во время запуска сервера возникает исключение, оно логируется с помощью `logger.error`.

**ASII flowchart**:

```
A [Проверка инициализации _api_server_instance]
│
├─── Нет ─── B [Создание экземпляра FastApiServer]
│           │
│           └─── C [Запуск сервера на указанном порту]
│
└─── Да ─── C [Запуск сервера на указанном порту]
│
└─── D [Обработка исключений при запуске сервера]
```

Где:

*   `A` - Проверка, инициализирован ли `_api_server_instance`.
*   `B` - Создание экземпляра `FastApiServer`.
*   `C` - Запуск сервера на указанном порту с помощью метода `start`.
*   `D` - Обработка исключений, которые могут возникнуть при запуске сервера.

**Примеры**:

```python
start_server(port=8000, host="127.0.0.1")  # Запуск сервера на порту 8000 и хосте 127.0.0.1
start_server(port=9000, host="0.0.0.0")  # Запуск сервера на порту 9000 и хосте 0.0.0.0
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

**Назначение**: Функция `stop_server` останавливает FastAPI сервер на указанном порту.

**Параметры**:
- `port` (int): Порт, на котором необходимо остановить сервер.

**Как работает функция**:

1.  Функция проверяет, инициализирован ли экземпляр `FastApiServer` (`_api_server_instance`).
2.  Если экземпляр существует, вызывается метод `stop` экземпляра `_api_server_instance` для остановки сервера на указанном порту.
3.  Если во время остановки сервера возникает исключение, оно логируется с помощью `logger.error`.

**ASII flowchart**:

```
A [Проверка инициализации _api_server_instance]
│
└─── Да ─── B [Остановка сервера на указанном порту]
│
└─── C [Обработка исключений при остановке сервера]
```

Где:

*   `A` - Проверка, инициализирован ли `_api_server_instance`.
*   `B` - Остановка сервера на указанном порту с помощью метода `stop`.
*   `C` - Обработка исключений, которые могут возникнуть при остановке сервера.

**Примеры**:

```python
stop_server(port=8000)  # Остановка сервера на порту 8000
stop_server(port=9000)  # Остановка сервера на порту 9000
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

**Назначение**: Функция `stop_all_servers` останавливает все запущенные FastAPI сервера.

**Параметры**:
- Отсутствуют.

**Как работает функция**:

1.  Функция проверяет, инициализирован ли экземпляр `FastApiServer` (`_api_server_instance`).
2.  Если экземпляр существует, вызывается метод `stop_all` экземпляра `_api_server_instance` для остановки всех запущенных серверов.
3.  Если во время остановки серверов возникает исключение, оно логируется с помощью `logger.error`.

**ASII flowchart**:

```
A [Проверка инициализации _api_server_instance]
│
└─── Да ─── B [Остановка всех серверов]
│
└─── C [Обработка исключений при остановке серверов]
```

Где:

*   `A` - Проверка, инициализирован ли `_api_server_instance`.
*   `B` - Остановка всех серверов с помощью метода `stop_all`.
*   `C` - Обработка исключений, которые могут возникнуть при остановке серверов.

**Примеры**:

```python
stop_all_servers()  # Остановка всех запущенных серверов
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

**Назначение**: Функция `status_servers` показывает статус запущенных FastAPI серверов.

**Параметры**:
- Отсутствуют.

**Как работает функция**:

1.  Функция проверяет, инициализирован ли экземпляр `FastApiServer` (`_api_server_instance`).
2.  Если экземпляр существует, вызывается метод `get_servers_status` экземпляра `_api_server_instance` для получения статуса серверов.
3.  Если есть запущенные серверы, выводится информация о хосте и статусе каждого сервера.
4.  Если нет запущенных серверов, выводится сообщение "No servers running".
5.  Если экземпляр `FastApiServer` не инициализирован, выводится сообщение "Server not initialized.".

**ASII flowchart**:

```
A [Проверка инициализации _api_server_instance]
│
├─── Нет ─── B [Вывод сообщения "Server not initialized."]
│
└─── Да ─── C [Получение статуса серверов]
│
    ├─── D [Проверка наличия запущенных серверов]
    │
    ├─── Нет ─── E [Вывод сообщения "No servers running"]
    │
    └─── Да ─── F [Вывод информации о хосте и статусе каждого сервера]
```

Где:

*   `A` - Проверка, инициализирован ли `_api_server_instance`.
*   `B` - Вывод сообщения "Server not initialized.".
*   `C` - Получение статуса серверов с помощью метода `get_servers_status`.
*   `D` - Проверка, есть ли запущенные серверы.
*   `E` - Вывод сообщения "No servers running".
*   `F` - Вывод информации о хосте и статусе каждого сервера.

**Примеры**:

```python
status_servers()  # Вывод статуса серверов
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
          print(f"  - Path: {route['path']}, Methods: {route['methods']}")
      else:
        print("No routes defined")
    else:
        print("Server not initialized.")
```

**Назначение**: Функция `get_routes` показывает все зарегистрированные маршруты FastAPI сервера.

**Параметры**:
- Отсутствуют.

**Как работает функция**:

1.  Функция проверяет, инициализирован ли экземпляр `FastApiServer` (`_api_server_instance`).
2.  Если экземпляр существует, вызывается метод `get_routes` экземпляра `_api_server_instance` для получения списка маршрутов.
3.  Если есть маршруты, выводится информация о каждом маршруте, включая путь и поддерживаемые HTTP методы.
4.  Если нет маршрутов, выводится сообщение "No routes defined".
5.  Если экземпляр `FastApiServer` не инициализирован, выводится сообщение "Server not initialized.".

**ASII flowchart**:

```
A [Проверка инициализации _api_server_instance]
│
├─── Нет ─── B [Вывод сообщения "Server not initialized."]
│
└─── Да ─── C [Получение списка маршрутов]
│
    ├─── D [Проверка наличия маршрутов]
    │
    ├─── Нет ─── E [Вывод сообщения "No routes defined"]
    │
    └─── Да ─── F [Вывод информации о каждом маршруте]
```

Где:

*   `A` - Проверка, инициализирован ли `_api_server_instance`.
*   `B` - Вывод сообщения "Server not initialized.".
*   `C` - Получение списка маршрутов с помощью метода `get_routes`.
*   `D` - Проверка, есть ли маршруты.
*   `E` - Вывод сообщения "No routes defined".
*   `F` - Вывод информации о каждом маршруте.

**Примеры**:

```python
get_routes()  # Вывод списка маршрутов
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

**Назначение**: Функция `add_new_route` добавляет новый маршрут к FastAPI серверу.

**Параметры**:
- `path` (str): Путь для нового маршрута.
- `module_name` (str): Имя модуля, содержащего функцию обработчика маршрута.
- `func_name` (str): Имя функции обработчика маршрута.
- `methods` (List[str]): Список HTTP методов, поддерживаемых маршрутом. По умолчанию `["GET"]`.

**Как работает функция**:

1.  Функция проверяет, инициализирован ли экземпляр `FastApiServer` (`_api_server_instance`).
2.  Если экземпляр существует, вызывается метод `add_new_route` экземпляра `_api_server_instance` для добавления нового маршрута.
3.  В случае успешного добавления маршрута выводится сообщение об этом.
4.  Если во время добавления маршрута возникает исключение, оно логируется с помощью `logger.error`.
5.  Если экземпляр `FastApiServer` не инициализирован, выводится сообщение "Server not initialized. Start server first".

**ASII flowchart**:

```
A [Проверка инициализации _api_server_instance]
│
├─── Нет ─── B [Вывод сообщения "Server not initialized. Start server first"]
│
└─── Да ─── C [Добавление нового маршрута]
│
    ├─── D [Обработка исключений при добавлении маршрута]
    │
    └─── E [Вывод сообщения об успешном добавлении маршрута]
```

Где:

*   `A` - Проверка, инициализирован ли `_api_server_instance`.
*   `B` - Вывод сообщения "Server not initialized. Start server first".
*   `C` - Добавление нового маршрута с помощью метода `add_new_route`.
*   `D` - Обработка исключений, которые могут возникнуть при добавлении маршрута.
*   `E` - Вывод сообщения об успешном добавлении маршрута.

**Примеры**:

```python
add_new_route(path="/new_route", module_name="my_module", func_name="my_function", methods=["GET", "POST"])  # Добавление нового маршрута
```

### `parse_port_range`

```python
def parse_port_range(range_str):
    """Разбирает строку с диапазоном портов."""
    if not re.match(r'^[\\d-]+$', range_str):
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
```

**Назначение**: Функция `parse_port_range` разбирает строку с диапазоном портов и возвращает список портов.

**Параметры**:
- `range_str` (str): Строка с диапазоном портов (например, "8000", "8000-8005").

**Возвращает**:
- `List[int]`: Список портов.

**Как работает функция**:

1.  Функция проверяет, соответствует ли строка диапазону портов с помощью регулярного выражения.
2.  Если строка содержит дефис (`-`), она разбивается на начало и конец диапазона, преобразуется в целые числа и возвращается список портов в этом диапазоне.
3.  Если строка не содержит дефис, она преобразуется в целое число и возвращается список, содержащий только этот порт.
4.  Если строка не соответствует диапазону портов или возникает ошибка при преобразовании, выводится сообщение об ошибке и возвращается пустой список.

**ASII flowchart**:

```
A [Проверка соответствия строки диапазону портов]
│
├─── Нет ─── B [Вывод сообщения об ошибке и возврат пустого списка]
│
└─── Да ─── C [Проверка наличия дефиса в строке]
│
    ├─── Да ─── D [Разбиение строки на начало и конец диапазона]
    │           │
    │           └─── E [Преобразование начала и конца диапазона в целые числа]
    │           │
    │           └─── F [Проверка, что начало диапазона меньше или равно концу диапазона]
    │           │
    │           ├─── Нет ─── B [Вывод сообщения об ошибке и возврат пустого списка]
    │           │
    │           └─── Да ─── G [Создание списка портов в диапазоне и возврат его]
    │
    └─── Нет ─── H [Преобразование строки в целое число]
    │           │
    │           └─── I [Создание списка, содержащего только этот порт, и возврат его]
    │
└─── J [Обработка исключений при преобразовании строки в целое число]
```

Где:

*   `A` - Проверка соответствия строки диапазону портов.
*   `B` - Вывод сообщения об ошибке и возврат пустого списка.
*   `C` - Проверка наличия дефиса в строке.
*   `D` - Разбиение строки на начало и конец диапазона.
*   `E` - Преобразование начала и конца диапазона в целые числа.
*   `F` - Проверка, что начало диапазона меньше или равно концу диапазона.
*   `G` - Создание списка портов в диапазоне и возврат его.
*   `H` - Преобразование строки в целое число.
*   `I` - Создание списка, содержащего только этот порт, и возврат его.
*   `J` - Обработка исключений при преобразовании строки в целое число.

**Примеры**:

```python
print(parse_port_range("8000"))  # Вывод: [8000]
print(parse_port_range("8000-8005"))  # Вывод: [8000, 8001, 8002, 8003, 8004, 8005]
print(parse_port_range("invalid"))  # Вывод: Invalid port range: invalid, []
```

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

**Назначение**: Функция `display_menu` выводит меню с доступными командами для управления сервером.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Функция выводит список доступных команд с их описаниями.

**Примеры**:

```python
display_menu()  # Вывод меню с командами
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
```

**Назначение**: Функция `main` является основной функцией управления сервером.

**Параметры**:
- Отсутствуют.

**Как работает функция**:

1.  Создается экземпляр `CommandHandler` для обработки команд.
2.  В бесконечном цикле выводится меню с доступными командами.
3.  Пользователь вводит команду, которая обрабатывается в зависимости от ее типа.
4.  Команды включают запуск сервера, отображение статуса, остановку сервера, добавление маршрута, завершение работы и отображение справки.
5.  Если возникает исключение, оно логируется с помощью `logger.error`.

**ASII flowchart**:

```
A [Создание экземпляра CommandHandler]
│
└─── B [Бесконечный цикл]
│
    ├─── C [Вывод меню с доступными командами]
    │
    ├─── D [Ввод команды пользователя]
    │
    ├─── E [Обработка команды]
    │
    │   ├─── start ─── F [Запуск сервера]
    │   │
    │   ├─── status ─── G [Отображение статуса]
    │   │
    │   ├─── routes ─── H [Отображение маршрутов]
    │   │
    │   ├─── stop ─── I [Остановка сервера]
    │   │
    │   ├─── stop_all ─── J [Остановка всех серверов]
    │   │
    │   ├─── add_route ─── K [Добавление маршрута]
    │   │
    │   ├─── shutdown ─── L [Завершение работы]
    │   │
    │   ├─── help ─── M [Отображение справки]
    │   │
    │   └─── exit ─── N [Выход из программы]
    │
    └─── O [Обработка исключений]
```

Где:

*   `A` - Создание экземпляра `CommandHandler`.
*   `B` - Бесконечный цикл.
*   `C` - Вывод меню с доступными командами.
*   `D` - Ввод команды пользователя.
*   `E` - Обработка команды.
*   `F` - Запуск сервера.
*   `G` - Отображение статуса.
*   `H` - Отображение маршрутов.
*   `I` - Остановка сервера.
*   `J` - Остановка всех серверов.
*   `K` - Добавление маршрута.
*   `L` - Завершение работы.
*   `M` - Отображение справки.
*   `N` - Выход из программы.
*   `O` - Обработка исключений.

**Примеры**:

Для запуска сервера необходимо выполнить скрипт и ввести команду `start <port>`, где `<port>` - номер порта.
Для остановки сервера - `stop <port>`. Для завершения работы - `shutdown`.
```
python fast_api.py