# Модуль запуска приложения

## Обзор

Данный модуль является точкой входа для запуска веб-приложения. Он загружает конфигурацию из файла `config.json`, настраивает маршруты для веб-сайта и backend API, а затем запускает Flask-сервер.

## Подробней

Модуль выполняет следующие шаги:

1.  Загружает конфигурацию из файла `config.json`. Эта конфигурация содержит настройки для веб-сайта и backend API.
2.  Создает экземпляры классов `Website` и `Backend_Api`, передавая им объект Flask-приложения (`app`) и конфигурацию.
3.  Добавляет маршруты для веб-сайта и backend API в Flask-приложение. Маршруты определяются в классах `Website` и `Backend_Api`.
4.  Запускает Flask-сервер, используя настройки из конфигурации веб-сайта.

## Классы

В данном модуле напрямую не определены классы, но используются классы `Website` и `Backend_Api` из других модулей.

## Функции

### `__main__`

**Назначение**: Главная функция, запускающая веб-приложение.

**Как работает функция**:

1.  Загружает конфигурацию из файла `config.json`.

2.  Инициализирует экземпляры классов `Website` и `Backend_Api` с необходимыми параметрами (Flask-приложение и конфигурация).

3.  Добавляет маршруты из `Website` и `Backend_Api` в приложение Flask.

4.  Запускает Flask-сервер с использованием конфигурации веб-сайта.

**Примеры**:

Запуск приложения:

```python
if __name__ == '__main__':
    # Load configuration from config.json
    config = load(open('config.json', 'r'))
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