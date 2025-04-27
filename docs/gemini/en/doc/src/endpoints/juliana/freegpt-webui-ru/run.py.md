# Модуль `run.py`

## Обзор

Модуль `run.py` запускает веб-приложение, которое предоставляет API для взаимодействия с различными моделями ИИ. Он содержит конфигурацию сервера, обработку маршрутов (routes) и запуск сервера Flask.

## Детали

Этот модуль отвечает за запуск веб-приложения, которое предоставляет доступ к различным моделям ИИ. Он использует конфигурацию, которая загружается из файла `config.json`, для настройки сервера и определяет маршруты (routes) для сайта (Website) и API (Backend_Api). В модуле используется библиотека Flask для создания веб-приложения и обработки запросов.

## Classes

### `Website`

**Описание**: Класс `Website` определяет маршруты и функции для сайта. 

**Attributes**:
    - `app`: экземпляр объекта Flask.
    - `routes`: словарь, который содержит информацию о маршрутах сайта.

**Methods**:

    - `__init__(self, app: Flask, routes: Optional[Dict] = None)`: Конструктор класса `Website`. Принимает экземпляр объекта Flask и опционально словарь маршрутов.
        - **Parameters**:
            - `app`: Экземпляр объекта Flask, который будет использоваться для определения маршрутов.
            - `routes`: Словарь, который содержит информацию о маршрутах сайта. По умолчанию `None`.
    - `get_routes(self, routes: Optional[Dict] = None)`: Метод возвращает словарь маршрутов.
        - **Parameters**:
            - `routes`: Словарь, который содержит информацию о маршрутах сайта. По умолчанию `None`.
        - **Returns**:
            - `Dict`: Словарь маршрутов сайта.
    
### `Backend_Api`

**Описание**: Класс `Backend_Api` определяет маршруты и функции для API.

**Attributes**:
    - `app`: экземпляр объекта Flask.
    - `config`: конфигурационный словарь.
    - `routes`: словарь, который содержит информацию о маршрутах API.

**Methods**:

    - `__init__(self, app: Flask, config: Dict)`: Конструктор класса `Backend_Api`. Принимает экземпляр объекта Flask и конфигурационный словарь.
        - **Parameters**:
            - `app`: Экземпляр объекта Flask, который будет использоваться для определения маршрутов.
            - `config`: Конфигурационный словарь, который содержит настройки API.
    - `get_routes(self, routes: Optional[Dict] = None)`: Метод возвращает словарь маршрутов.
        - **Parameters**:
            - `routes`: Словарь, который содержит информацию о маршрутах API. По умолчанию `None`.
        - **Returns**:
            - `Dict`: Словарь маршрутов API.


## Functions

### `run.py`

**Purpose**: Запуск веб-приложения.

**Parameters**:
    - **None**

**Returns**:
    - **None**

**Raises Exceptions**:
    - **None**

**How the Function Works**:
    - Загружает конфигурацию из файла `config.json`.
    - Инициализирует объект `Website` для обработки маршрутов сайта.
    - Инициализирует объект `Backend_Api` для обработки маршрутов API.
    - Запускает сервер Flask, используя конфигурационные параметры из `site_config`.

**Examples**:

```python
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
    config = j_loads(__root__ / 'src' / 'endpoints' / 'freegpt-webui-ru' / 'config.json')
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