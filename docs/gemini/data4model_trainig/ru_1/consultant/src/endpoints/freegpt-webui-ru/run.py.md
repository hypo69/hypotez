### Анализ кода модуля `run.py`

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет настройку и запуск веб-приложения Flask.
    - Разделение на `Website` и `Backend_Api` для организации маршрутов.
- **Минусы**:
    - Отсутствуют аннотации типов.
    - Использование `load` вместо `j_loads`.
    - Отсутствует обработка исключений при загрузке конфигурации.
    - Не используется модуль `logger` для логирования.
    - Не описаны docstring для классов, методов и функций.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    - Добавить docstring к классам `Website` и `Backend_Api`.
    - Добавить docstring ко всем функциям, включая `inner_function`.
2.  **Заменить `load` на `j_loads`**:
    - Использовать `j_loads` для загрузки `config.json`.
3.  **Добавить обработку исключений**:
    - Добавить блок `try...except` для обработки возможных исключений при загрузке конфигурационного файла.
4.  **Использовать логирование**:
    - Заменить `print` на `logger.info` для вывода информации о запуске и остановке сервера.
5.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.

**Оптимизированный код:**

```python
"""
Модуль запуска веб-приложения
==============================

Модуль содержит основную точку входа для запуска веб-приложения Flask,
настраивает маршруты для сайта и бэкенд API, а также обрабатывает конфигурацию.

Пример использования
----------------------

>>> python run.py
"""
from server.app import app
from server.website import Website
from server.backend import Backend_Api
from json import load
from src.logger import logger  # Добавлен импорт logger


if __name__ == '__main__':
    """
    Основная точка входа для запуска веб-приложения.
    Загружает конфигурацию, настраивает маршруты и запускает Flask-сервер.
    """
    try:
        # Load configuration from config.json
        config: dict = load(open('config.json', 'r')) #TODO: заменить load(open на j_loads
        site_config: dict = config['site_config']
    except FileNotFoundError as ex:
        logger.error('Configuration file not found.', ex, exc_info=True)
        raise  # Перебросить исключение, чтобы остановить выполнение
    except Exception as ex:
        logger.error('Error loading configuration.', ex, exc_info=True)
        raise  # Перебросить исключение, чтобы остановить выполнение

    # Set up the website routes
    site: Website = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Set up the backend API routes
    backend_api: Backend_Api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Run the Flask server
    logger.info(f"Running on port {site_config['port']}")
    app.run(**site_config)
    logger.info(f"Closing port {site_config['port']}")
```