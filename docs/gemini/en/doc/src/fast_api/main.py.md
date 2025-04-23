# Модуль `main.py`

## Обзор

Модуль `main.py` управляет параметрами Fast API сервера. Он предоставляет интерфейс командной строки для запуска, остановки и управления серверами Fast API.

## Детали

Этот модуль является точкой входа для управления серверами Fast API. Он включает в себя обработку команд, таких как запуск, остановка, просмотр статуса и добавление новых маршрутов.

## Функции

### `display_menu`

```python
def display_menu():
    """Выводит меню с доступными командами."""
```

**Назначение**: Выводит в консоль список доступных команд для управления сервером.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Ничего. Функция просто выводит текст в консоль.

**Принцип работы**:
- Функция выводит список доступных команд и их описание, чтобы пользователь мог взаимодействовать с сервером через командную строку.

**Примеры**:
```
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

### `main`

```python
def main():
    """Основная функция управления сервером."""
```

**Назначение**: Основная функция управления сервером.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Ничего.

**Принцип работы**:
1.  Создает экземпляр класса `CommandHandler`.
2.  Запускает бесконечный цикл для обработки команд, вводимых пользователем.
3.  Выводит меню доступных команд.
4.  Считывает команду, введенную пользователем, и разделяет ее на части.
5.  Выполняет соответствующую команду на основе введенных данных:
    *   `start`: Запускает сервер на указанном порту и хосте.
    *   `status`: Выводит статус всех обслуживаемых портов.
    *   `routes`: Выводит все зарегистрированные маршруты.
    *   `stop`: Останавливает сервер на указанном порту.
    *   `stop_all`: Останавливает все серверы.
    *   `add_route`: Добавляет новый маршрут к серверу.
    *   `shutdown`: Останавливает все серверы и завершает программу.
    *   `help`: Выводит меню с доступными командами.
    *   `exit`: Завершает программу.
6.  Обрабатывает возможные исключения, такие как `ValueError` (неверный номер порта) и другие исключения, логируя их с помощью `logger.error`.

**Примеры**:
```
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
```
```
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
Enter command: status
```

## Дополнительные детали

-   Импортирует модуль `header`.
-   Использует `CommandHandler` из модуля `src.fast_api.fast_api` для управления серверами.
-   Использует `logger` из модуля `src.fast_api.fast_api` для логирования ошибок.