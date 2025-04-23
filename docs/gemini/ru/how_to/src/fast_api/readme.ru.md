## Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Этот блок кода реализует систему управления FastAPI сервером через XML-RPC. `fast_api_rpc.py` представляет собой серверную часть, которая запускает FastAPI сервер и предоставляет интерфейс для удаленного управления им. `main.py` является клиентской частью, которая позволяет пользователю отправлять команды на сервер для управления FastAPI.

Шаги выполнения
-------------------------
1.  Запустите `fast_api_rpc.py` для запуска XML-RPC сервера и FastAPI сервера(ов). `CommandHandler` управляет вызовами функций управления сервером.
2.  Запустите `main.py`, который отобразит меню доступных команд и запросит ввод пользователя.
3.  Введите команду в `main.py`, например, `start 8000`, чтобы запустить FastAPI сервер на порту 8000.
4.  `main.py` отправит XML-RPC запрос на сервер `fast_api_rpc.py` для выполнения команды.
5.  XML-RPC сервер в `fast_api_rpc.py` получит запрос и вызовет соответствующий метод `CommandHandler`, например, `start_server`.
6.  FastAPI сервер будет запущен или остановлен в соответствии с командой.
7.  Результат выполнения команды будет отправлен обратно клиенту `main.py`.
8.  `main.py` отобразит результат выполнения команды в консоль.

Пример использования
-------------------------

```python
# fast_api_rpc.py (серверная часть)
from fastapi import FastAPI
from xmlrpc.server import SimpleXMLRPCServer
import threading

class FastApiServer:
    def __init__(self, port: int, host: str = "0.0.0.0"):
        self.port = port
        self.host = host
        self.app = FastAPI()

    def start(self):
        import uvicorn
        uvicorn.run(self.app, host=self.host, port=self.port)

class CommandHandler:
    def __init__(self):
        self.rpc_server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
        self.rpc_server.register_instance(self)
        threading.Thread(target=self.rpc_server.serve_forever, daemon=True).start()
        self.servers = {}

    def start_server(self, port: int, host: str = "0.0.0.0"):
        if port not in self.servers:
            server = FastApiServer(port, host)
            self.servers[port] = server
            threading.Thread(target=server.start, daemon=True).start()
            return f"Сервер запущен на порту {port}"
        return f"Сервер уже запущен на порту {port}"

# main.py (клиентская часть)
from xmlrpc.client import ServerProxy

rpc_client = ServerProxy("http://localhost:9000", allow_none=True)

while True:
    print("Доступные команды: start <port>, stop <port>, exit")
    command = input("Введите команду: ")
    parts = command.split()
    if parts[0] == "start":
        if len(parts) > 1:
            port = int(parts[1])
            result = rpc_client.start_server(port=port, host="0.0.0.0")
            print(result)
        else:
            print("Необходимо указать порт")
    elif parts[0] == "exit":
        break