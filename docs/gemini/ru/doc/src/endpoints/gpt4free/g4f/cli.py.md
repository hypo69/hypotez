# Модуль для запуска gpt4free через CLI

## Обзор

Модуль предоставляет интерфейс командной строки (CLI) для запуска gpt4free в различных режимах, включая API и GUI. Он использует библиотеку `argparse` для обработки аргументов командной строки и позволяет настраивать параметры API, такие как адрес привязки, порт, режим отладки, модель и провайдер.

## Подробней

Этот модуль является точкой входа для запуска приложения gpt4free. Он определяет аргументы командной строки для настройки API и GUI, а затем запускает соответствующий режим в зависимости от указанных аргументов. Он также устанавливает конфигурацию приложения на основе аргументов командной строки.

## Функции

### `get_api_parser`

```python
def get_api_parser() -> ArgumentParser:
    """
    Создает парсер аргументов для API.

    Args:
        Нет

    Returns:
        ArgumentParser: Парсер аргументов для API.

    Как работает функция:
    1. Создает экземпляр `ArgumentParser` с описанием "Run the API and GUI".
    2. Добавляет аргументы, такие как `--bind`, `--port`, `--debug`, `--gui`, `--model`, `--provider`, `--image-provider`, `--proxy`, `--workers`, `--disable-colors`, `--ignore-cookie-files`, `--g4f-api-key`, `--ignored-providers`, `--cookie-browsers`, `--reload`, `--demo`, `--ssl-keyfile`, `--ssl-certfile`, `--log-config` для настройки API.
    3. Возвращает настроенный парсер аргументов.

    ASCII flowchart:
    Создание парсера аргументов (api_parser)
    ↓
    Добавление аргументов для настройки API
    ↓
    Возврат парсера аргументов

    Примеры:
    >>> parser = get_api_parser()
    >>> args = parser.parse_args(['--port', '8080', '--debug'])
    >>> args.port
    '8080'
    >>> args.debug
    True
    """
```

### `main`

```python
def main() -> None:
    """
    Главная функция для запуска gpt4free через CLI.

    Args:
        Нет

    Returns:
        None

    Как работает функция:
    1. Создает основной парсер аргументов `ArgumentParser` с описанием "Run gpt4free".
    2. Добавляет подпарсеры для режимов "api" и "gui", используя `get_api_parser` и `gui_parser` соответственно.
    3. Разбирает аргументы командной строки.
    4. В зависимости от режима ("api" или "gui"), вызывает `run_api_args` или `run_gui_args`.
    5. Если режим не указан, выводит справку и завершает программу с кодом ошибки 1.

    ASCII flowchart:
    Создание основного парсера (parser)
    ↓
    Добавление подпарсеров для режимов "api" и "gui"
    ↓
    Разбор аргументов командной строки (args)
    ↓
    Вызов `run_api_args` или `run_gui_args` в зависимости от режима
    ↓
    Завершение программы

    Примеры:
    Для запуска API:
    >>> main(['api', '--port', '8080'])

    Для запуска GUI:
    >>> main(['gui'])
    """
```

### `run_api_args`

```python
def run_api_args(args: argparse.Namespace) -> None:
    """
    Запускает API с заданными аргументами.

    Args:
        args (argparse.Namespace): Аргументы командной строки, содержащие настройки API.

    Returns:
        None

    Как работает функция:
    1. Импортирует `AppConfig` и `run_api` из `g4f.api`.
    2. Устанавливает конфигурацию приложения `AppConfig` на основе аргументов командной строки, таких как `ignore_cookie_files`, `ignored_providers`, `g4f_api_key`, `provider`, `image_provider`, `proxy`, `model`, `gui`, `demo`.
    3. Если указаны браузеры для cookie, обновляет список `g4f.cookies.browsers`.
    4. Запускает API с заданными параметрами, такими как `bind`, `port`, `debug`, `workers`, `use_colors`, `reload`, `ssl_keyfile`, `ssl_certfile`, `log_config`.

    ASCII flowchart:
    Импорт `AppConfig` и `run_api`
    ↓
    Установка конфигурации приложения `AppConfig`
    ↓
    Обновление списка `g4f.cookies.browsers` (если указаны браузеры для cookie)
    ↓
    Запуск API с заданными параметрами

    Примеры:
    >>> args = argparse.Namespace(ignore_cookie_files=True, ignored_providers=[], g4f_api_key=None, provider=None, image_provider=None, proxy=None, model=None, gui=False, demo=False, cookie_browsers=[], bind=None, port='8080', debug=True, workers=None, disable_colors=False, reload=False, ssl_keyfile=None, ssl_certfile=None, log_config=None)
    >>> run_api_args(args)
    # Запустит API с указанными параметрами
    """