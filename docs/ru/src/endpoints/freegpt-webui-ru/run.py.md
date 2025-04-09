# Модуль запуска веб-приложения FreeGPT WebUI на Flask
## Обзор

Модуль `run.py` является точкой входа для запуска веб-приложения FreeGPT WebUI. Он загружает конфигурацию из файла `config.json`, настраивает маршруты для веб-сайта и backend API, а затем запускает Flask-сервер.

## Подробнее
Этот модуль инициализирует и запускает веб-приложение FreeGPT WebUI, используя Flask. Он загружает конфигурацию из `config.json`, создает экземпляры классов `Website` и `Backend_Api` для настройки маршрутов и запускает сервер с параметрами конфигурации.

## Функции

### `__main__`

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
```

**Назначение**: Главная функция, запускающая Flask-сервер и настраивающая маршруты для веб-приложения и backend API.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Ничего.

**Вызывает исключения**:
- Возможные исключения при загрузке конфигурации из `config.json` или при запуске Flask-сервера.

**Как работает функция**:
1. Загружает конфигурацию из файла `config.json`.
2. Извлекает конфигурацию сайта из загруженной конфигурации.
3. Создает экземпляр класса `Website` и настраивает маршруты для веб-сайта, добавляя их в Flask-приложение.
4. Создает экземпляр класса `Backend_Api` и настраивает маршруты для backend API, добавляя их в Flask-приложение.
5. Запускает Flask-сервер с использованием параметров конфигурации сайта.
6. Выводит сообщение о закрытии порта после остановки сервера.

**Внутренние функции**:
- Отсутствуют.

**ASCII flowchart**:
```
Загрузка конфигурации из config.json
    ↓
Извлечение конфигурации сайта
    ↓
Создание экземпляра Website и настройка маршрутов
    ↓
Создание экземпляра Backend_Api и настройка маршрутов
    ↓
Запуск Flask-сервера
    ↓
Вывод сообщения о закрытии порта
```

**Примеры**:

```python
# Пример запуска приложения с конфигурацией по умолчанию
# Файл config.json должен существовать и содержать необходимые настройки для сайта и backend API.
# После запуска приложения, оно будет доступно по адресу, указанному в site_config['host'] и site_config['port'].