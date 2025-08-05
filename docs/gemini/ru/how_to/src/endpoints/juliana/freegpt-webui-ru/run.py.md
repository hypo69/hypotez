## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода запускает веб-приложение на основе Flask. Он загружает конфигурационные данные из файла `config.json`, настраивает маршруты веб-сайта и API, а затем запускает сервер Flask.

Шаги выполнения
-------------------------
1. **Загрузка конфигурации:**
    - Код загружает конфигурационные данные из файла `config.json` с помощью `j_loads`.
    - Он извлекает настройки веб-сайта из `site_config` и сохраняет их в переменную `site_config`.
2. **Настройка маршрутов веб-сайта:**
    - Создается объект `Website` с помощью `Website(app)`.
    - Код итерирует по маршрутам, определенным в `site.routes`, и добавляет их в Flask-приложение с помощью `app.add_url_rule`.
3. **Настройка маршрутов API:**
    - Создается объект `Backend_Api` с помощью `Backend_Api(app, config)`.
    - Код итерирует по маршрутам, определенным в `backend_api.routes`, и добавляет их в Flask-приложение с помощью `app.add_url_rule`.
4. **Запуск сервера Flask:**
    - Код выводит в консоль сообщение о запуске сервера на определенном порту.
    - Запускается сервер Flask с помощью `app.run(**site_config)`.
    - Код выводит в консоль сообщение о завершении работы сервера на определенном порту.

Пример использования
-------------------------

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