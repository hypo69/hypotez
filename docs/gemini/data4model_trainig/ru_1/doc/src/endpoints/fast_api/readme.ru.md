# Документация для разработчика: `fast_api_rpc.py` и `main.py`

## Обзор

Этот документ предназначен для разработчиков, работающих с проектом `hypotez`, и предоставляет подробное описание взаимодействия между файлами `fast_api_rpc.py` (серверная часть) и `main.py` (клиентская часть). Описывает основные компоненты, их взаимодействие и принципы работы системы управления FastAPI серверами через XML-RPC.

## Подробней

Данный код представляет собой систему, позволяющую управлять FastAPI серверами удаленно. Это достигается посредством использования XML-RPC для связи между клиентской (`main.py`) и серверной (`fast_api_rpc.py`) частями приложения. Серверная часть предоставляет API для запуска, остановки, получения статуса серверов и добавления новых маршрутов. Клиентская часть предоставляет интерфейс командной строки для взаимодействия с сервером.
XML-RPC (Remote Procedure Call) — это протокол удаленного вызова процедур, использующий XML для кодирования вызовов функций и ответов, и HTTP в качестве транспорта.

## Основные компоненты

### `fast_api_rpc.py` (Серверная часть)

#### Обзор

`fast_api_rpc.py` содержит классы и функции, необходимые для запуска и управления FastAPI серверами. Он предоставляет интерфейс XML-RPC для удаленного управления серверами.

#### Классы

##### `FastApiServer`

**Описание**: Этот класс содержит логику для запуска FastAPI-сервера. Он отвечает за создание и настройку веб-сервера, а также за добавление новых маршрутов.

##### `CommandHandler`

**Описание**: Класс управляет вызовами функций управления сервером.
**Атрибуты**:
- `rpc_server` (SimpleXMLRPCServer): Объект XML-RPC сервера, принимающий удаленные вызовы.

**Методы**:
- `__init__(self)`: Инициализирует объект `CommandHandler`, создает и запускает XML-RPC сервер в отдельном потоке.
- `register_instance(self)`: Регистрирует экземпляр класса для обработки RPC-запросов.
- `start_server(self, port: int, host: str) -> None`: Запускает FastAPI сервер на указанном порту и хосте.
- `stop_server(self, port: int) -> None`: Останавливает FastAPI сервер, работающий на указанном порту.
- `stop_all_servers(self) -> None`: Останавливает все запущенные FastAPI серверы.
- `status_servers(self) -> list`: Возвращает список со статусами всех серверов.
- `add_new_route(self, port: int, path: str, handler: str) -> None`: Добавляет новый маршрут к указанному серверу.
- `shutdown(self) -> None`: Останавливает XML-RPC сервер.

#### Методы класса `CommandHandler`

##### `__init__`

```python
   def __init__(self):
        """
        Инициализирует объект `CommandHandler`, создает и запускает XML-RPC сервер в отдельном потоке.
        Создает экземпляр `SimpleXMLRPCServer`, который слушает запросы на порту `9000` (по умолчанию).
        Метод `register_instance(self)` позволяет сделать все методы этого класса доступными для удаленного вызова.
        `threading.Thread(target=self.rpc_server.serve_forever, daemon=True).start()` запускает XML-RPC сервер в отдельном потоке, что позволяет ему работать параллельно с остальным кодом.
        """
        ...
```

**Назначение**: Инициализация обработчика команд, создание и запуск XML-RPC сервера.

**Как работает функция**:
- Создается экземпляр XML-RPC сервера, который начинает прослушивать порт 9000 для входящих RPC-запросов.
- Все методы класса `CommandHandler` регистрируются для удаленного вызова через XML-RPC.
- XML-RPC сервер запускается в отдельном потоке, чтобы не блокировать основной поток выполнения.

##### `register_instance`

```python
    def register_instance(self):
        """
        Регистрирует экземпляр класса для обработки RPC-запросов.
        """
        ...
```

**Назначение**: Регистрация методов экземпляра класса для удаленного вызова.

**Как работает функция**:
- Позволяет сделать все методы класса доступными для удаленного вызова через XML-RPC.

##### `start_server`

```python
    def start_server(self, port: int, host: str):
        """
        Запускает FastAPI сервер на указанном порту и хосте.
        Args:
            port (int): Порт для запуска сервера.
            host (str): Хост для запуска сервера.

        Returns:
            None
        """
        ...
```

**Назначение**: Запуск FastAPI сервера на заданном порту и хосте.

**Параметры**:
- `port` (int): Порт, на котором будет запущен сервер.
- `host` (str): Хост, на котором будет запущен сервер.

**Как работает функция**:
- Функция отвечает за запуск FastAPI сервера с указанными параметрами порта и хоста.

##### `stop_server`

```python
    def stop_server(self, port: int):
        """
        Останавливает FastAPI сервер, работающий на указанном порту.
        Args:
            port (int): Порт сервера, который необходимо остановить.
        Returns:
            None
        """
        ...
```

**Назначение**: Остановка FastAPI сервера на указанном порту.

**Параметры**:
- `port` (int): Порт сервера, который необходимо остановить.

**Как работает функция**:
- Функция останавливает FastAPI сервер, прослушивающий указанный порт.

##### `stop_all_servers`

```python
    def stop_all_servers(self):
        """
        Останавливает все запущенные FastAPI серверы.
        Returns:
            None
        """
        ...
```

**Назначение**: Остановка всех запущенных FastAPI серверов.

**Как работает функция**:
- Функция останавливает все запущенные FastAPI серверы, перебирая их в списке.

##### `status_servers`

```python
    def status_servers(self):
        """
        Возвращает список со статусами всех серверов.
        Returns:
            list: Список статусов серверов.
        """
        ...
```

**Назначение**: Получение статусов всех запущенных FastAPI серверов.

**Возвращает**:
- `list`: Список, содержащий статусы всех серверов.

**Как работает функция**:
- Функция возвращает информацию о статусе каждого запущенного FastAPI сервера.

##### `add_new_route`

```python
    def add_new_route(self, port: int, path: str, handler: str):
        """
        Добавляет новый маршрут к указанному серверу.
        Args:
            port (int): Порт сервера, к которому добавляется маршрут.
            path (str): Путь нового маршрута.
            handler (str): Обработчик для нового маршрута.

        Returns:
            None
        """
        ...
```

**Назначение**: Добавление нового маршрута к существующему FastAPI серверу.

**Параметры**:
- `port` (int): Порт сервера, к которому необходимо добавить маршрут.
- `path` (str): Путь для нового маршрута.
- `handler` (str): Обработчик (функция), который будет вызван при обращении к маршруту.

**Как работает функция**:
- Функция добавляет новый маршрут к указанному FastAPI серверу с заданным обработчиком.

##### `shutdown`

```python
    def shutdown(self):
        """
        Останавливает XML-RPC сервер.
        Returns:
            None
        """
        ...
```

**Назначение**: Остановка XML-RPC сервера.

**Как работает функция**:
- Функция останавливает XML-RPC сервер, завершая его работу.

### `main.py` (Клиентская часть)

#### Обзор

`main.py` предоставляет клиентский интерфейс для взаимодействия с XML-RPC сервером, определенным в `fast_api_rpc.py`. Он позволяет пользователю отправлять команды для управления FastAPI серверами через командную строку.

#### Классы

Здесь нет явно определенных классов. Код в файле `main.py` выполняет роль клиента, использующего `xmlrpc.client.ServerProxy` для связи с сервером.

#### Переменные

- `rpc_client`: Экземпляр `xmlrpc.client.ServerProxy`, используемый для взаимодействия с удаленным сервером.

#### Основные функции и логика

1.  **`ServerProxy`**: Этот класс из библиотеки `xmlrpc.client` используется для создания объекта, через который можно вызывать методы XML-RPC сервера. `rpc_client = ServerProxy("http://localhost:9000", allow_none=True)` устанавливает соединение с сервером.
2.  **Цикл `while True`**:
    *   Отображает меню доступных команд.
    *   Запрашивает ввод пользователя.
    *   Парсит введенную строку, выделяя команду и её аргументы.
    *   В зависимости от введенной команды вызывает соответствующий метод RPC-сервера через объект `rpc_client`.

## Взаимодействие между компонентами

1.  **Запуск `fast_api_rpc.py`**: Когда ты запускаешь `fast_api_rpc.py`, происходит следующее:
    *   Создается экземпляр `CommandHandler`.
    *   В конструкторе `CommandHandler` создается XML-RPC сервер, который начинает слушать порт `9000`.
    *   Запускается FastAPI-сервер(ы) в соответствии с кодом, который мы создали.
2.  **Запуск `main.py`**: Когда ты запускаешь `main.py`, происходит следующее:
    *   Создается экземпляр `CommandHandler` (но он не играет роли, поскольку в `main.py` используется только RPC-клиент).
    *   Создается `ServerProxy`, который подключается к XML-RPC серверу по адресу `http://localhost:9000`.
    *   `main.py` начинает показывать меню и ожидать ввода пользователя.
3.  **Ввод команды:** Когда пользователь вводит команду в `main.py`, например `start 8000`:
    *   `main.py` анализирует эту строку, выделяет команду `start` и порт `8000`.
    *   `main.py` вызывает метод `start_server(port=8000, host="0.0.0.0")` у объекта `rpc_client`. Это *не* вызов метода на локальном объекте, а запрос к XML-RPC серверу.
4.  **Обработка запроса на сервере:** XML-RPC клиент `rpc_client` создает XML-сообщение, которое отправляет на сервер `fast_api_rpc.py`.
    *   XML-RPC сервер в `fast_api_rpc.py` получает этот запрос.
    *   Он понимает, что нужно вызвать метод `start_server` у объекта `CommandHandler`.
    *   Вызывается метод `start_server`, который вызывает функцию `start_server` и запускает FastAPI сервер.
5.  **Возврат ответа:** XML-RPC сервер формирует ответ, содержащий результат вызова (в данном случае, это может быть `None`).
    *   Этот ответ отправляется обратно клиенту `main.py`.
    *   Клиент получает ответ.
6.  **Отображение результата:** `main.py` может отобразить результат в консоль (или проигнорировать его, если это None).
7.  **Повторение цикла:** `main.py` возвращается к началу цикла, отображая меню и ожидая ввода следующей команды.

## Ключевые моменты

*   **Разделение ответственности:** `fast_api_rpc.py` отвечает за управление сервером и предоставление интерфейса для управления, `main.py` отвечает за взаимодействие с пользователем и отправку команд.
*   **XML-RPC:** `xmlrpc` используется для организации связи между двумя процессами, что позволяет вызывать методы сервера из клиентской программы.
*   **Потоки:** XML-RPC сервер запущен в отдельном потоке, поэтому он может работать параллельно с остальным кодом.
*   **Удаленный вызов:** `ServerProxy` позволяет вызывать методы, как если бы они были частью локального кода, хотя на самом деле они выполняются на удаленном сервере.

## Преимущества данного подхода

*   **Управление сервером из другой программы:** Мы можем контролировать запущенный сервер через другой процесс или даже с другой машины.
*   **Разделение кода:** Логика управления сервером и пользовательский интерфейс разделены, что делает код более модульным и легким в обслуживании.
*   **Гибкость:** Мы можем добавить новые методы управления сервером, просто добавив их в `CommandHandler`, и они автоматически станут доступны через RPC.