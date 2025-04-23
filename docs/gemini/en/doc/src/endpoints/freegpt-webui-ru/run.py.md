# Модуль запуска веб-интерфейса FreeGPT

## Обзор

Модуль предназначен для запуска веб-интерфейса FreeGPT с использованием Flask. Он настраивает маршруты для веб-сайта и backend API, а также запускает Flask-сервер.

## Более подробная информация

Этот модуль является точкой входа для запуска веб-интерфейса FreeGPT. Он загружает конфигурацию из файла `config.json`, настраивает маршруты для веб-сайта и backend API, а затем запускает Flask-сервер. Модуль использует классы `Website` и `Backend_Api` для настройки маршрутов и обработки запросов.

## Функции

### `__main__`

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

**Назначение**: Точка входа в приложение. Загружает конфигурацию, настраивает маршруты и запускает Flask-сервер.

**Как работает функция**:

1.  Загружает конфигурацию из файла `config.json` с помощью функции `j_loads`.
2.  Извлекает конфигурацию сайта из загруженной конфигурации.
3.  Создает экземпляр класса `Website` и настраивает маршруты для веб-сайта, используя метод `add_url_rule` объекта `app`.
4.  Создает экземпляр класса `Backend_Api` и настраивает маршруты для backend API, используя метод `add_url_rule` объекта `app`.
5.  Запускает Flask-сервер с использованием конфигурации сайта.
6.  Выводит в консоль сообщение о запуске сервера и закрытии порта.

**Примеры**:

```python
# Пример запуска приложения
# (Предполагается, что config.json существует и содержит необходимые настройки)
# Этот код будет запущен при выполнении файла run.py