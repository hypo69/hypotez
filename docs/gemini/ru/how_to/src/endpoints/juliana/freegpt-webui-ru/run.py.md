### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода является точкой входа для Flask-приложения freegpt-webui-ru. Он загружает конфигурацию, настраивает маршруты для веб-сайта и backend API, а затем запускает Flask-сервер.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `app` (Flask-приложение), `Website` и `Backend_Api` для настройки маршрутов, `load` из `json` для загрузки конфигурации, а также модуль `header` для получения корневого пути.
2. **Загрузка конфигурации из `config.json`**:
   - Функция `j_loads` из модуля `src.utils.jjson` используется для загрузки конфигурации из файла `config.json`, расположенного в директории `src/endpoints/freegpt-webui-ru`.
   - Из загруженной конфигурации извлекается подконфигурация `site_config`, которая содержит параметры запуска веб-сайта, такие как порт.
3. **Настройка маршрутов веб-сайта**:
   - Создается экземпляр класса `Website`, который принимает Flask-приложение `app` в качестве аргумента.
   - Цикл `for route in site.routes` проходит по всем маршрутам, определенным в `site.routes`.
   - Для каждого маршрута добавляется правило URL с помощью `app.add_url_rule()`. Указываются URL-путь (`route`), функция обработки (`site.routes[route]['function']`) и HTTP-методы (`site.routes[route]['methods']`).
4. **Настройка маршрутов backend API**:
   - Создается экземпляр класса `Backend_Api`, который принимает Flask-приложение `app` и полную конфигурацию `config` в качестве аргументов.
   - Аналогично настройке маршрутов веб-сайта, цикл `for route in backend_api.routes` проходит по всем маршрутам, определенным в `backend_api.routes`, и добавляет правила URL для каждого маршрута.
5. **Запуск Flask-сервера**:
   - Выводится сообщение в консоль, указывающее, на каком порту будет запущен сервер (`site_config['port']`).
   - Flask-сервер запускается с помощью `app.run(**site_config)`. Параметры запуска берутся из подконфигурации `site_config`.
   - После завершения работы сервера выводится сообщение о закрытии порта.

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

    # Функция извлекает конфигурацию из config.json
    config = j_loads(__root__ / 'src' / 'endpoints'/ 'freegpt-webui-ru' / 'config.json')
    site_config = config['site_config']

    # Функция настраивает маршруты веб-сайта
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Функция настраивает маршруты backend API
    backend_api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Функция запускает Flask-сервер
    print(f"Running on port {site_config['port']}")
    app.run(**site_config)
    print(f"Closing port {site_config['port']}")