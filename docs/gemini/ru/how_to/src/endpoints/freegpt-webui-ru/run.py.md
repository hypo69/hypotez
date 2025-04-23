### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код запускает веб-приложение Flask, настраивает маршруты для веб-сайта и backend API, используя конфигурацию из JSON-файла.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `server.app`, `server.website`, `server.backend`, `json`, `header`, `src.gs`, `src.utils.jjson`.
2. **Загрузка конфигурации**: Функция `j_loads` загружает конфигурацию из файла `config.json`, расположенного в директории `src/endpoints/freegpt-webui-ru/`.
3. **Настройка маршрутов веб-сайта**:
   - Создается экземпляр класса `Website`, которому передается объект `app` Flask.
   - Происходит итерация по маршрутам веб-сайта, определенным в `site.routes`.
   - Для каждого маршрута добавляется правило URL с помощью `app.add_url_rule`, связывающее URL с функцией и методом(ами).
4. **Настройка маршрутов backend API**:
   - Создается экземпляр класса `Backend_Api`, которому передается объект `app` Flask и конфигурация.
   - Происходит итерация по маршрутам API, определенным в `backend_api.routes`.
   - Для каждого маршрута добавляется правило URL с помощью `app.add_url_rule`, связывающее URL с функцией и методом(ами).
5. **Запуск Flask-сервера**:
   - Извлекается порт из конфигурации сайта `site_config['port']`.
   - Выводится сообщение о запуске сервера на указанном порту.
   - Flask-сервер запускается с использованием параметров из `site_config`.
6. **Завершение работы сервера**:
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