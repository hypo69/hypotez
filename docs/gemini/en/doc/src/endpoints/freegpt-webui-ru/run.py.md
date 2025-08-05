# Модуль `run.py`

## Обзор

Этот модуль отвечает за запуск сервера Flask для веб-приложения. Он настраивает маршруты как для веб-сайта, так и для API-интерфейса.

## Детали

Этот модуль используется для запуска веб-приложения, которое предоставляет доступ к различным функциям, предоставляемым `hypotez`. Он загружает конфигурацию из файла `config.json`, настраивает маршруты для веб-сайта и API-интерфейса, а затем запускает сервер Flask.

## Классы

### `Website`

**Описание:**
Класс `Website` отвечает за обработку маршрутов веб-сайта.

**Атрибуты:**

- `app`: Объект Flask приложения.

**Методы:**

- `__init__(app: Flask)`: Инициализирует объект `Website`.
- `routes`: Словарь, содержащий список маршрутов веб-сайта, их функции обработки и методы HTTP.

## Функции

### `j_loads(path: Path) -> dict`:

**Описание:**
Функция `j_loads` используется для загрузки JSON-файла с заданного пути.

**Параметры:**

- `path (Path)`: Путь к JSON-файлу.

**Возвращает:**

- `dict`: Словарь, содержащий данные из JSON-файла.

**Примеры:**

```python
>>> from pathlib import Path
>>> path = Path('path/to/file.json')
>>> data = j_loads(path)
>>> print(data)
{'key1': 'value1', 'key2': 'value2'}
```


## Как работает код:

- Модуль `run.py` начинает с импорта необходимых модулей, включая `app` из `server`, `Website` из `server`, `Backend_Api` из `server`, а также `j_loads` из `src.utils.jjson`.
- Затем он загружает конфигурацию из файла `config.json`.
- Далее он создает объект `Website` и добавляет маршруты для веб-сайта в приложение Flask.
- После этого он создает объект `Backend_Api` и добавляет маршруты для API-интерфейса в приложение Flask.
- Наконец, он запускает сервер Flask.

## Примеры:

```python
>>> from server.app import app
>>> from server.website import Website
>>> from server.backend import Backend_Api
>>> from json import load
>>> import header
>>> from header import __root__
>>> from src import gs
>>> from src.utils.jjson import j_loads

>>> if __name__ == '__main__':
...     config = j_loads(__root__ / 'src' / 'endpoints' / 'freegpt-webui-ru' / 'config.json')
...     site_config = config['site_config']
...     site = Website(app)
...     for route in site.routes:
...         app.add_url_rule(route, view_func=site.routes[route]['function'], methods=site.routes[route]['methods'])
...     backend_api = Backend_Api(app, config)
...     for route in backend_api.routes:
...         app.add_url_rule(route, view_func=backend_api.routes[route]['function'], methods=backend_api.routes[route]['methods'])
...     print(f"Running on port {site_config['port']}")
...     app.run(**site_config)
...     print(f"Closing port {site_config['port']}")
```

##  Дополнительная информация:

- Для получения более подробной информации о структуре веб-сайта и API-интерфейса обратитесь к документации модулей `server.website` и `server.backend`.
- Для получения более подробной информации о конфигурации приложения обратитесь к документации файла `config.json`.