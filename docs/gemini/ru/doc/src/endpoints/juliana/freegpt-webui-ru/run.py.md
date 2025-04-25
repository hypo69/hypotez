# Модуль запуска сервера API для freegpt-webui-ru

## Обзор

Данный модуль содержит код для запуска сервера API для приложения freegpt-webui-ru. 

## Подробнее

Модуль запускает Flask-сервер, который обрабатывает запросы от веб-интерфейса и взаимодействует с бэкендом API для предоставления функциональности. Он настраивает маршруты для веб-сайта и API, а также запускает сервер на указанном порту.

## Классы

### `Website`

**Описание**: Класс, который определяет маршруты и функции для веб-сайта.

**Атрибуты**:

- `routes` (dict): Словарь, содержащий маршруты веб-сайта и соответствующие функции.

**Методы**:

- `__init__(self, app)`: Инициализирует класс с предоставленным объектом Flask-приложения.
- `setup(self, config: dict)`: Настраивает маршруты веб-сайта на основе конфигурации.

### `Backend_Api`

**Описание**: Класс, который определяет маршруты и функции для API бэкенда.

**Атрибуты**:

- `routes` (dict): Словарь, содержащий маршруты API и соответствующие функции.

**Методы**:

- `__init__(self, app, config: dict)`: Инициализирует класс с предоставленным объектом Flask-приложения и конфигурацией.
- `setup(self, config: dict)`: Настраивает маршруты API на основе конфигурации.


## Функции

### `main`

**Назначение**: Точка входа в модуль.

**Как работает функция**:

- Загружает конфигурацию из файла `config.json`.
- Создает экземпляры классов `Website` и `Backend_Api` для настройки маршрутов.
- Запускает Flask-сервер на указанном порту.

**Примеры**:

```python
if __name__ == '__main__':
    # Load configuration from config.json
    config = j_loads(__root__ / 'src' / 'endpoints'/ 'freegpt-webui-ru' / 'config.json')
    site_config = config['site_config']

    # Set up the website routes
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Set up the backend API routes
    backend_api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Run the Flask server
    print(f"Running on port {site_config['port']}")
    app.run(**site_config)
    print(f"Closing port {site_config['port']}")
```

## Параметры класса

- `config` (dict): Словарь, содержащий конфигурацию для веб-сайта и API.

## Примеры

```python
# Example usage:
from server.app import app
from server.website import Website
from server.backend import Backend_Api
from json import load

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads


if __name__ == '__main__':
    # Load configuration from config.json
    config = j_loads(__root__ / 'src' / 'endpoints'/ 'freegpt-webui-ru' / 'config.json')
    site_config = config['site_config']

    # Set up the website routes
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Set up the backend API routes
    backend_api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Run the Flask server
    print(f"Running on port {site_config['port']}")
    app.run(**site_config)
    print(f"Closing port {site_config['port']}")
```