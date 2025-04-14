# Модуль для создания парсера аргументов командной строки для GUI
=================================================================

Модуль содержит функцию `gui_parser`, которая создает и настраивает парсер аргументов командной строки для запуска графического интерфейса (GUI).

## Обзор

Этот модуль предоставляет функцию `gui_parser`, которая использует `ArgumentParser` из модуля `argparse` для определения аргументов командной строки, необходимых для запуска GUI. Аргументы включают хост, порт, режим отладки, игнорирование файлов cookie, список игнорируемых провайдеров и список используемых браузеров для cookie.

## Подробнее

Этот модуль помогает стандартизировать и упростить процесс запуска GUI, предоставляя возможность настройки через командную строку. Он определяет аргументы, такие как хост и порт, а также параметры для отладки и обработки файлов cookie.

## Функции

### `gui_parser`

```python
def gui_parser() -> ArgumentParser:
    """Создает парсер аргументов командной строки для GUI.

    Returns:
        ArgumentParser: Объект парсера аргументов.

    Raises:
        No exceptions.

    Example:
        >>> parser = gui_parser()
        >>> args = parser.parse_args(['--port', '8000', '--debug'])
        >>> print(args.port, args.debug)
        8000 True
    """
    parser = ArgumentParser(description="Run the GUI")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="hostname")
    parser.add_argument("--port", "-p", type=int, default=8080, help="port")
    parser.add_argument("--debug", "-d", "-debug", action="store_true", help="debug mode")
    parser.add_argument("--ignore-cookie-files", action="store_true", help="Don't read .har and cookie files.")
    parser.add_argument("--ignored-providers", nargs="+", choices=[provider.__name__ for provider in Provider.__providers__ if provider.working],
                            default=[], help="List of providers to ignore when processing request. (incompatible with --reload and --workers)")
    parser.add_argument("--cookie-browsers", nargs="+", choices=[browser.__name__ for browser in browsers],
                            default=[], help="List of browsers to access or retrieve cookies from.")
    return parser
```

**Назначение**: Создает и настраивает парсер аргументов командной строки для запуска GUI.

**Возвращает**:
- `ArgumentParser`: Объект парсера аргументов, настроенный с необходимыми аргументами.

**Как работает функция**:
- Функция создает экземпляр `ArgumentParser` с описанием "Run the GUI".
- Добавляет аргумент `--host` типа `str` с значением по умолчанию `"0.0.0.0"` и описанием `"hostname"`.
- Добавляет аргумент `--port` (или `-p`) типа `int` со значением по умолчанию `8080` и описанием `"port"`.
- Добавляет аргумент `--debug` (или `-d`, или `-debug`) типа `bool` с использованием `action="store_true"` для включения режима отладки.
- Добавляет аргумент `--ignore-cookie-files` типа `bool` с использованием `action="store_true"` для игнорирования файлов cookie.
- Добавляет аргумент `--ignored-providers` типа `list` с выбором из списка доступных провайдеров и значением по умолчанию `[]`.
- Добавляет аргумент `--cookie-browsers` типа `list` с выбором из списка доступных браузеров и значением по умолчанию `[]`.
- Возвращает настроенный объект `ArgumentParser`.

**Примеры**:

```python
>>> parser = gui_parser()
>>> args = parser.parse_args(['--port', '8000', '--debug'])
>>> print(args.port, args.debug)
8000 True
```

```python
>>> parser = gui_parser()
>>> args = parser.parse_args(['--host', '127.0.0.1', '--ignore-cookie-files'])
>>> print(args.host, args.ignore_cookie_files)
127.0.0.1 True