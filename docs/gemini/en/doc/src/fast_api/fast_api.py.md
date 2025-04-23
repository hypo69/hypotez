# Модуль `fast_api.fast_api`

## Обзор

Модуль предоставляет FastAPI сервер с XML-RPC интерфейсом для удалённого управления.

## Подробнее

Модуль содержит классы и функции для запуска и управления FastAPI сервером, который может принимать команды через XML-RPC. Он использует библиотеку `uvicorn` для асинхронного запуска сервера и предоставляет возможность добавления новых маршрутов во время работы сервера.

## Содержание

- [Классы](#Классы)
    - [`FastApiServer`](#FastApiServer)
    - [`CommandHandler`](#CommandHandler)
- [Функции](#Функции)
    - [`telegram_webhook`](#telegram_webhook)
    - [`test_function`](#test_function)
    - [`test_post`](#test_post)
    - [`start_server`](#start_server)
    - [`stop_server`](#stop_server)
    - [`stop_all_servers`](#stop_all_servers)
    - [`status_servers`](#status_servers)
    - [`get_routes`](#get_routes)
    - [`add_new_route`](#add_new_route)
    - [`parse_port_range`](#parse_port_range)
    - [`display_menu`](#display_menu)
    - [`main`](#main)

## Классы

### `FastApiServer`

Класс `FastApiServer` представляет собой Singleton-реализацию FastAPI сервера.

**Описание**:
Реализует FastAPI сервер с возможностью добавления маршрутов и управления сервером.

**Атрибуты**:
- `_instance`: Приватный атрибут для хранения экземпляра класса (Singleton).
- `app` (FastAPI): FastAPI приложение.
- `host` (str): Хост для запуска сервера (по умолчанию "127.0.0.1").
- `port` (int): Порт для запуска сервера (по умолчанию 8000).
- `router` (APIRouter): FastAPI роутер для добавления маршрутов.
- `server_tasks` (dict): Словарь задач серверов.
- `servers` (dict): Словарь запущенных серверов.

**Методы**:

- `__new__(cls, *args, **kwargs)`
- `__init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs)`
- `add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs)`
- `_start_server(self, port: int)`
- `start(self, port: int, as_thread: bool = True)`
- `stop(self, port: int)`
- `stop_all(self)`
- `get_servers_status(self)`
- `get_routes(self)`
- `get_app(self)`
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs)`

#### `__new__(cls, *args, **kwargs)`

```python
def __new__(cls, *args, **kwargs):
    """Реализация Singleton."""
    ...
```

**Описание**:
    Реализует Singleton паттерн, гарантируя, что у класса будет только один экземпляр.

#### `__init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs)`

```python
def __init__(self, host: str = "127.0.0.1", title: str = "FastAPI RPC Server", **kwargs):
    """Инициализирует FastAPI сервер."""
    ...
```

**Описание**:
Инициализирует экземпляр класса `FastApiServer`, добавляет базовые маршруты ("/hello" и "/post"), а также настраивает FastAPI приложение.
Если объект уже инициализирован, повторная инициализация не происходит.

**Параметры**:
- `host` (str, optional): Хост для запуска сервера. По умолчанию "127.0.0.1".
- `title` (str, optional): Заголовок FastAPI сервера. По умолчанию "FastAPI RPC Server".
- `**kwargs`: Дополнительные аргументы.

#### `add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs)`

```python
def add_route(self, path: str, func: Callable, methods: List[str] = ["GET"], **kwargs):
    """Добавляет маршрут к FastAPI приложению."""
    ...
```

**Описание**:
Добавляет новый маршрут к FastAPI приложению с указанным путем, функцией-обработчиком и HTTP методами.

**Параметры**:
- `path` (str): Путь для маршрута.
- `func` (Callable): Функция-обработчик для маршрута.
- `methods` (List[str], optional): Список HTTP методов, поддерживаемых маршрутом. По умолчанию `["GET"]`.
- `**kwargs`: Дополнительные аргументы для `router.add_api_route`.

**Пример**:
```python
server = FastApiServer()
server.add_route("/test", lambda: {"message": "Test route"})
```

#### `_start_server(self, port: int)`

```python
async def _start_server(self, port: int):
    """Запускает uvicorn сервер асинхронно."""
    ...
```

**Описание**:
Асинхронно запускает uvicorn сервер на указанном порту.

**Параметры**:
- `port` (int): Порт для запуска сервера.

#### `start(self, port: int, as_thread: bool = True)`

```python
def start(self, port: int, as_thread: bool = True):
    """Запускает FastAPI сервер на указанном порту."""
    ...
```

**Описание**:
Запускает FastAPI сервер на указанном порту в отдельном потоке.

**Параметры**:
- `port` (int): Порт для запуска сервера.
- `as_thread` (bool, optional): Флаг, указывающий, запускать ли сервер в отдельном потоке. По умолчанию `True`.

#### `stop(self, port: int)`

```python
def stop(self, port: int):
    """Останавливает FastAPI сервер на указанном порту."""
    ...
```

**Описание**:
Останавливает FastAPI сервер, работающий на указанном порту.

**Параметры**:
- `port` (int): Порт сервера для остановки.

#### `stop_all(self)`

```python
def stop_all(self):
    """Останавливает все запущенные сервера."""
    ...
```

**Описание**:
Останавливает все запущенные экземпляры FastAPI сервера.

#### `get_servers_status(self)`

```python
def get_servers_status(self):
    """Возвращает статус всех серверов."""
    ...
```

**Описание**:
Возвращает словарь, содержащий статус каждого запущенного сервера (порт и статус: "Running" или "Stopped").

**Возвращает**:
- `dict`: Словарь со статусами серверов.

#### `get_routes(self)`

```python
def get_routes(self):
    """Возвращает список всех роутов."""
    ...
```

**Описание**:
Возвращает список всех зарегистрированных маршрутов в FastAPI приложении.

**Возвращает**:
- `list`: Список маршрутов, где каждый маршрут представлен словарем с полями "path" и "methods".

#### `get_app(self)`

```python
def get_app(self):
    """Возвращает FastAPI приложение."""
    ...
```

**Описание**:
Возвращает экземпляр FastAPI приложения.

**Возвращает**:
- `FastAPI`: FastAPI приложение.

#### `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs)`

```python
def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"], **kwargs):
    """Добавляет новый маршрут к уже работающему приложению."""
    ...
```

**Описание**:
Добавляет новый маршрут к уже работающему FastAPI приложению, динамически импортируя модуль и функцию-обработчик.

**Параметры**:
- `path` (str): Путь для нового маршрута.
- `module_name` (str): Имя модуля, содержащего функцию-обработчик.
- `func_name` (str): Имя функции-обработчика.
- `methods` (List[str], optional): Список HTTP методов, поддерживаемых маршрутом. По умолчанию `["GET"]`.
- `**kwargs`: Дополнительные аргументы для `router.add_api_route`.

### `CommandHandler`

Класс `CommandHandler` предназначен для обработки команд управления FastAPI сервером через XML-RPC.

**Описание**:
Предоставляет интерфейс для удалённого управления сервером через XML-RPC.

**Атрибуты**:
- `rpc_port` (int): Порт для XML-RPC сервера (по умолчанию 9000).
- `rpc_server` (SimpleXMLRPCServer): XML-RPC сервер.

**Методы**:
- `__init__(self, rpc_port=9000)`
- `start_server(self, port: int, host: str)`
- `stop_server(self, port: int)`
- `stop_all_servers(self)`
- `status_servers(self)`
- `get_routes(self)`
- `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"])`
- `shutdown(self)`

#### `__init__(self, rpc_port=9000)`

```python
def __init__(self, rpc_port=9000):
    """Инициализирует обработчик команд."""
    ...
```

**Описание**:
Инициализирует экземпляр класса `CommandHandler`, запускает XML-RPC сервер в отдельном потоке.

**Параметры**:
- `rpc_port` (int, optional): Порт для XML-RPC сервера. По умолчанию 9000.

#### `start_server(self, port: int, host: str)`

```python
def start_server(self, port: int, host: str):
    """Запускает FastAPI сервер."""
    ...
```

**Описание**:
Запускает FastAPI сервер на указанном порту и хосте.

**Параметры**:
- `port` (int): Порт для запуска сервера.
- `host` (str): Хост для запуска сервера.

#### `stop_server(self, port: int)`

```python
def stop_server(self, port: int):
    """Останавливает FastAPI сервер."""
    ...
```

**Описание**:
Останавливает FastAPI сервер на указанном порту.

**Параметры**:
- `port` (int): Порт сервера для остановки.

#### `stop_all_servers(self)`

```python
def stop_all_servers(self):
    """Останавливает все запущенные FastAPI сервера."""
    ...
```

**Описание**:
Останавливает все запущенные экземпляры FastAPI сервера.

#### `status_servers(self)`

```python
def status_servers(self):
    """Показывает статус серверов."""
    ...
```

**Описание**:
Выводит статус всех запущенных серверов.

#### `get_routes(self)`

```python
def get_routes(self):
    """Показывает все роуты."""
    ...
```

**Описание**:
Выводит список всех зарегистрированных маршрутов.

#### `add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"])`

```python
def add_new_route(self, path: str, module_name: str, func_name: str, methods: List[str] = ["GET"]):
    """Добавляет новый роут к серверу."""
    ...
```

**Описание**:
Добавляет новый маршрут к серверу, используя указанные параметры.

**Параметры**:
- `path` (str): Путь для нового маршрута.
- `module_name` (str): Имя модуля, содержащего функцию-обработчик.
- `func_name` (str): Имя функции-обработчика.
- `methods` (List[str], optional): Список HTTP методов, поддерживаемых маршрутом. По умолчанию `["GET"]`.

#### `shutdown(self)`

```python
def shutdown(self):
    """Останавливает все сервера и завершает работу."""
    ...
```

**Описание**:
Останавливает все запущенные серверы и завершает работу XML-RPC сервера.

## Функции

### `telegram_webhook()`

```python
def telegram_webhook():
    """"""
    ...
```

**Описание**:
Заглушка для telegram webhook.

**Возвращает**:
- `str`: "Hello, World!".

### `test_function()`

```python
def test_function():
    ...
```

**Описание**:
Тестовая функция, возвращающая строку "It is working!!!".

**Возвращает**:
- `str`: "It is working!!!".

### `test_post(data: Dict[str, str])`

```python
def test_post(data: Dict[str, str]):
    ...
```

**Описание**:
Тестовая функция для обработки POST запросов.

**Параметры**:
- `data` (Dict[str, str]): Данные, переданные в POST запросе.

**Возвращает**:
- `dict`: Словарь с результатом обработки POST запроса и переданными данными.

### `start_server(port: int, host: str)`

```python
def start_server(port: int, host: str):
    """Запускает FastAPI сервер на указанном порту."""
    ...
```

**Описание**:
Запускает FastAPI сервер на указанном порту и хосте. Использует глобальную переменную `_api_server_instance` для хранения экземпляра сервера.

**Параметры**:
- `port` (int): Порт для запуска сервера.
- `host` (str): Хост для запуска сервера.

### `stop_server(port: int)`

```python
def stop_server(port: int):
    """Останавливает FastAPI сервер на указанном порту."""
    ...
```

**Описание**:
Останавливает FastAPI сервер, работающий на указанном порту.

**Параметры**:
- `port` (int): Порт сервера для остановки.

### `stop_all_servers()`

```python
def stop_all_servers():
    """Останавливает все запущенные FastAPI сервера."""
    ...
```

**Описание**:
Останавливает все запущенные экземпляры FastAPI сервера.

### `status_servers()`

```python
def status_servers():
    """Показывает статус серверов."""
    ...
```

**Описание**:
Выводит статус всех запущенных серверов.

### `get_routes()`

```python
def get_routes():
    """Показывает все роуты."""
    ...
```

**Описание**:
Выводит список всех зарегистрированных маршрутов.

### `add_new_route(path: str, module_name: str, func_name: str, methods: List[str] = ["GET"])`

```python
def add_new_route(path: str, module_name: str, func_name: str, methods: List[str] = ["GET"]):
    """Добавляет новый роут к серверу."""
    ...
```

**Описание**:
Добавляет новый маршрут к серверу, используя указанные параметры.

**Параметры**:
- `path` (str): Путь для нового маршрута.
- `module_name` (str): Имя модуля, содержащего функцию-обработчик.
- `func_name` (str): Имя функции-обработчика.
- `methods` (List[str], optional): Список HTTP методов, поддерживаемых маршрутом. По умолчанию `["GET"]`.

### `parse_port_range(range_str)`

```python
def parse_port_range(range_str):
    """Разбирает строку с диапазоном портов."""
    ...
```

**Описание**:
Разбирает строку с диапазоном портов и возвращает список портов.

**Параметры**:
- `range_str` (str): Строка с диапазоном портов (например, "8000-8005" или "8000").

**Возвращает**:
- `list`: Список портов.

### `display_menu()`

```python
def display_menu():
    """Выводит меню с доступными командами."""
    ...
```

**Описание**:
Выводит в консоль меню с доступными командами для управления сервером.

### `main()`

```python
def main():
    """Основная функция управления сервером."""
    ...
```

**Описание**:
Основная функция управления сервером. Создает экземпляр `CommandHandler`, обрабатывает команды, вводимые пользователем, и вызывает соответствующие методы для управления сервером.