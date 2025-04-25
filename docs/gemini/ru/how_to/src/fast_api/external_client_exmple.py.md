## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой пример использования XML-RPC клиента для управления сервером Fast API из внешнего кода. Он демонстрирует взаимодействие с сервером через RPC (Remote Procedure Call) для выполнения различных операций, таких как запуск сервера, добавление маршрутов, получение статуса сервера и его остановка.

Шаги выполнения
-------------------------
1. **Инициализация RPC клиента**: Создается объект `ServerProxy`, который устанавливает соединение с сервером Fast API по указанному URL.
2. **Выполнение действий**: С помощью RPC клиента `rpc_client` вызываются методы на сервере Fast API.
    - `start_server(port, host)`: запускает сервер на указанном порту и хосте.
    - `add_new_route(path, handler, methods)`: добавляет новый маршрут с указанным путем, обработчиком и методами HTTP-запросов.
    - `status_servers()`:  возвращает информацию о статусе всех запущенных серверов.
    - `stop_server(port)`: останавливает сервер, работающий на указанном порту.
    - `shutdown()`:  завершает соединение с RPC сервером.
3. **Обработка ошибок**: Блок `try...except` обрабатывает возможные ошибки при взаимодействии с RPC сервером. 
4. **Завершение**:  В блоке `finally` выполняется `shutdown()`, чтобы завершить соединение с RPC сервером.

Пример использования
-------------------------

```python
                ## \file /src/fast_api/external_client.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.fast_api.external_client
    :platform: Windows, Unix
    :synopsis: Example XML-RPC client for managing the Fast API server from external code.

"""

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