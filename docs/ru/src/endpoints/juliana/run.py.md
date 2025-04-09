# Модуль запуска приложения (run.py)

## Обзор

Данный модуль является точкой входа в приложение. Он отвечает за загрузку конфигурации, настройку маршрутов для веб-сайта и backend API, а также запуск Flask-сервера.

## Подробнее

Этот модуль выполняет следующие основные задачи:

1.  Загрузка конфигурации из файла `config.json`.
2.  Настройка маршрутов для веб-сайта на основе класса `Website` и его атрибута `routes`.
3.  Настройка маршрутов для backend API на основе класса `Backend_Api` и его атрибута `routes`.
4.  Запуск Flask-сервера с использованием конфигурации из `site_config`.

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

**Назначение**: Главная функция, запускающая приложение.

**Как работает функция**:

1.  **Загрузка конфигурации:**
    *   Загружает конфигурацию из файла `config.json` с использованием `json.load`.
    *   Извлекает конфигурацию сайта (`site_config`) из загруженной конфигурации.

2.  **Настройка маршрутов веб-сайта:**
    *   Создает экземпляр класса `Website`, передавая ему объект приложения Flask (`app`).
    *   Итерируется по маршрутам, определенным в атрибуте `routes` экземпляра `site`.
    *   Добавляет каждый маршрут в приложение Flask с помощью `app.add_url_rule()`, связывая маршрут с соответствующей функцией и HTTP-методами.

3.  **Настройка маршрутов backend API:**
    *   Создает экземпляр класса `Backend_Api`, передавая ему объект приложения Flask (`app`) и общую конфигурацию (`config`).
    *   Аналогично настройке маршрутов веб-сайта, итерируется по маршрутам, определенным в атрибуте `routes` экземпляра `backend_api`.
    *   Добавляет каждый маршрут в приложение Flask с помощью `app.add_url_rule()`, связывая маршрут с соответствующей функцией и HTTP-методами.

4.  **Запуск Flask-сервера:**
    *   Выводит сообщение о запуске сервера на определенном порту.
    *   Запускает Flask-сервер с использованием конфигурации, указанной в `site_config`.
    *   Выводит сообщение о завершении работы сервера после его остановки.

**ASCII flowchart**:

```
Загрузка конфигурации из config.json
│
Создание экземпляра Website
│
Настройка маршрутов веб-сайта
│
Создание экземпляра Backend_Api
│
Настройка маршрутов backend API
│
Запуск Flask-сервера
│
Завершение работы сервера
```

**Примеры**:

```python
# Предполагается, что в config.json есть структура, например:
# {
#     "site_config": {
#         "port": 5000,
#         "debug": True
#     },
#     ...
# }