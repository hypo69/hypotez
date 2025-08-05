# Модуль `external_client.py`

## Обзор

Модуль `external_client.py` предоставляет пример использования XML-RPC клиента для управления сервером Fast API из внешнего кода. 

## Подробней

Этот модуль реализует XML-RPC (eXtensible Markup Language Remote Procedure Call) клиента, который позволяет управлять сервером Fast API из внешнего кода. 
Клиент взаимодействует с сервером через протокол XML-RPC, отправляя запросы и получая ответы в формате XML.

## Функции

### `main()`

**Назначение**:  Функция  `main()`  используется для управления сервером Fast API через XML-RPC. Она демонстрирует примеры запуска, добавления новых маршрутов, получения статуса и остановки серверов.

**Параметры**:  Функция не принимает параметров.

**Возвращает**:  Функция не возвращает значения.

**Вызывает исключения**:  
- `Exception`:  Возникает при возникновении ошибок во время взаимодействия с XML-RPC сервером.

**Как работает функция**:

1. **Создает соединение с XML-RPC сервером**:  Функция `main()`  инициализирует объект `rpc_client`  класса  `ServerProxy`, который устанавливает соединение с сервером Fast API по адресу `http://localhost:9000`.  
2. **Выполняет операции управления сервером**:  Затем функция `main()`  использует методы `rpc_client`  для выполнения операций с сервером Fast API:
    - `start_server()`:  Запускает сервер на указанном порту.
    - `add_new_route()`:  Добавляет новый маршрут для обработчика запросов.
    - `status_servers()`:  Получает статус серверов.
    - `stop_server()`:  Останавливает сервер на указанном порту.
    - `shutdown()`:  Закрывает соединение с XML-RPC сервером.
3. **Обрабатывает исключения**:  Функция  `main()`  использует  блок  `try...except`  для обработки ошибок, которые могут возникнуть во время взаимодействия с XML-RPC сервером.  В случае возникновения исключения, функция выводит сообщение об ошибке в консоль.
4. **Закрывает соединение**:  Функция  `main()`  использует  блок  `finally`  для гарантированного закрытия соединения с XML-RPC сервером, даже если произошла ошибка.

**Примеры**:

```python
# Пример: Запуск сервера на порту 8001
print("Starting server on port 8001...")
rpc_client.start_server(8001, "127.0.0.1")

# Пример: Добавление нового маршрута /test_route
print("Adding new route /test_route...")
rpc_client.add_new_route("/test_route", 'lambda: {"message": "Hello from test_route"}\', ["GET"])

# Пример: Получение статуса серверов
print("Getting server status...")
rpc_client.status_servers()

# Пример: Остановка сервера на порту 8001
print("Stopping server on port 8001...")
rpc_client.stop_server(8001)

# Пример: Получение статуса серверов
print("Getting server status...")
rpc_client.status_servers()
```


## Внутренние функции

### `__main__`

**Назначение**:  Точка входа в приложение.

**Параметры**:  Функция не принимает параметров.

**Возвращает**:  Функция не возвращает значения.

**Как работает функция**:

- **Вызывает функцию `main()`**:  Эта функция просто запускает функцию `main()`, чтобы инициировать процесс управления сервером Fast API.

**Примеры**:

```python
if __name__ == "__main__":
    main()
```

##  Примеры

```python
import sys
from xmlrpc.client import ServerProxy
import time

def main():
    """Основная функция для управления сервером через RPC из внешнего кода."""
    rpc_client = ServerProxy("http://localhost:9000", allow_none=True)
    
    try:
        # Пример: Запуск сервера на порту 8001
        print("Starting server on port 8001...")
        rpc_client.start_server(8001, "127.0.0.1")
        time.sleep(1)
        
        # Пример: Добавление нового маршрута /test_route
        print("Adding new route /test_route...")
        rpc_client.add_new_route("/test_route", \'lambda: {"message": "Hello from test_route"}\', ["GET"])
        time.sleep(1)

        # Пример: Получение статуса серверов
        print("Getting server status...")
        rpc_client.status_servers()
        time.sleep(1)

       # Пример: Остановка сервера на порту 8001
        print("Stopping server on port 8001...")
        rpc_client.stop_server(8001)
        time.sleep(1)
        
        # Пример: Получение статуса серверов
        print("Getting server status...")
        rpc_client.status_servers()
        time.sleep(1)

    except Exception as ex:
        print(f"An error occurred: {ex}")
    finally:
        print("Shutting down RPC server")
        rpc_client.shutdown()


if __name__ == "__main__":
    main()
```

```markdown