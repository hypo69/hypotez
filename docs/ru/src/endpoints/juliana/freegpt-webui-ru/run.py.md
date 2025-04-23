# Модуль запуска веб-интерфейса FreeGPT на русском языке

## Обзор

Этот модуль предназначен для запуска веб-интерфейса FreeGPT на русском языке с использованием фреймворка Flask. Он загружает конфигурацию из файла `config.json`, настраивает маршруты для веб-сайта и backend API, а затем запускает Flask-сервер.

## Подробнее

Модуль `run.py` является точкой входа для запуска веб-интерфейса FreeGPT на русском языке. Он выполняет следующие действия:

1.  Загружает конфигурацию из файла `config.json`.
2.  Настраивает маршруты для веб-сайта, используя класс `Website` из модуля `server.website`.
3.  Настраивает маршруты для backend API, используя класс `Backend_Api` из модуля `server.backend`.
4.  Запускает Flask-сервер с использованием конфигурации из `config.json`.

## Классы

В данном модуле классы не используются.

## Функции

В данном модуле функции не используются.

## Параметры

-   `config` (dict): Словарь с конфигурацией, загруженной из файла `config.json`.
-   `site_config` (dict): Словарь с конфигурацией веб-сайта, извлеченной из `config['site_config']`.
-   `site` (Website): Экземпляр класса `Website`, используемый для настройки маршрутов веб-сайта.
-   `backend_api` (Backend_Api): Экземпляр класса `Backend_Api`, используемый для настройки маршрутов backend API.

## Как работает модуль

1.  Модуль начинается с импорта необходимых библиотек и модулей, таких как `Flask`, `json`, `Website`, `Backend_Api` и других.
2.  Загружается конфигурация из файла `config.json` с использованием функции `j_loads`.
3.  Создается экземпляр класса `Website` и настраиваются маршруты для веб-сайта.
4.  Создается экземпляр класса `Backend_Api` и настраиваются маршруты для backend API.
5.  Запускается Flask-сервер с использованием конфигурации, загруженной из `config.json`.

## Примеры

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