## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода запускает веб-приложение, используя фреймворк Flask. Он загружает конфигурацию из файла `config.json`, устанавливает маршруты для веб-сайта и API, а затем запускает сервер Flask.

Шаги выполнения
-------------------------
1. Загружает конфигурацию из `config.json`, используя `j_loads`.
2. Создание экземпляров классов `Website` и `Backend_Api`.
3. Добавление маршрутов для веб-сайта (`site.routes`) и API (`backend_api.routes`) в приложение Flask с помощью `app.add_url_rule()`.
4. Запуск сервера Flask на указанном порту из `site_config`.

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

    # Загрузка конфигурации из config.json
    config = j_loads(__root__ / 'src' / 'endpoints' / 'freegpt-webui-ru' / 'config.json')
    site_config = config['site_config']

    # Настройка маршрутов для веб-сайта
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Настройка маршрутов для API
    backend_api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Запуск сервера Flask
    print(f"Запуск на порту {site_config['port']}")
    app.run(**site_config)
    print(f"Закрытие порта {site_config['port']}")
```