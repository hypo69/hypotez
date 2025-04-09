# Модуль для создания парсера аргументов командной строки для графического интерфейса (GUI)
=========================================================================================

Модуль содержит функцию `gui_parser`, которая создает и настраивает парсер аргументов командной строки для запуска графического интерфейса. Этот парсер используется для определения параметров запуска GUI, таких как хост, порт, режим отладки, игнорирование файлов cookie и список игнорируемых провайдеров.

## Обзор

Модуль `gui_parser` предоставляет функцию для создания парсера аргументов командной строки, который используется для настройки и запуска графического интерфейса (GUI) приложения. Этот парсер позволяет передавать различные параметры, такие как хост, порт, режим отладки, параметры для работы с cookie и список провайдеров, которые следует игнорировать.

## Подробнее

Данный модуль играет важную роль в настройке GUI, позволяя пользователям указывать параметры запуска через командную строку. Это особенно полезно для отладки, тестирования и настройки приложения под различные окружения. Функция `gui_parser` создает объект `ArgumentParser` и добавляет необходимые аргументы, которые затем могут быть использованы для получения значений параметров запуска.

## Функции

### `gui_parser`

```python
def gui_parser():
    """
    Создает и настраивает парсер аргументов командной строки для запуска графического интерфейса.

    Args:
        None

    Returns:
        ArgumentParser: Объект парсера аргументов командной строки.
    """
```

**Как работает функция**:

1. **Создание парсера**: Инициализируется объект `ArgumentParser` с описанием "Run the GUI".
2. **Добавление аргументов**: К парсеру добавляются аргументы, такие как `--host`, `--port`, `--debug`, `--ignore-cookie-files`, `--ignored-providers` и `--cookie-browsers`.
3. **Настройка аргументов**:
   - `--host`: Тип `str`, значение по умолчанию `"0.0.0.0"`, помощь `"hostname"`.
   - `--port`, `-p`: Тип `int`, значение по умолчанию `8080`, помощь `"port"`.
   - `--debug`, `-d`, `-debug`: `action="store_true"`, помощь `"debug mode"`.
   - `--ignore-cookie-files`: `action="store_true"`, помощь `"Don't read .har and cookie files."`.
   - `--ignored-providers`: `nargs="+"`, `choices=[provider.__name__ for provider in Provider.__providers__ if provider.working]`, `default=[]`, помощь `"List of providers to ignore when processing request. (incompatible with --reload and --workers)"`.
   - `--cookie-browsers`: `nargs="+"`, `choices=[browser.__name__ for browser in browsers]`, `default=[]`, помощь `"List of browsers to access or retrieve cookies from."`.
4. **Возврат парсера**: Функция возвращает настроенный объект `ArgumentParser`.

```
Создание парсера --> Добавление аргументов (host, port, debug, ignore-cookie-files, ignored-providers, cookie-browsers) --> Возврат парсера
```

**Примеры**:

1. **Запуск GUI с указанием хоста и порта**:
   ```python
   parser = gui_parser()
   args = parser.parse_args(['--host', '127.0.0.1', '--port', '9000'])
   print(args.host, args.port)
   ```

2. **Запуск GUI в режиме отладки с игнорированием файлов cookie**:
   ```python
   parser = gui_parser()
   args = parser.parse_args(['--debug', '--ignore-cookie-files'])
   print(args.debug, args.ignore_cookie_files)
   ```

3. **Запуск GUI с указанием игнорируемых провайдеров и браузеров cookie**:
   ```python
   parser = gui_parser()
   providers = [provider.__name__ for provider in Provider.__providers__ if provider.working][:2]  # Берем первые два доступных провайдера для примера
   browsers_list = [browser.__name__ for browser in browsers][:2]  # Берем первые два доступных браузера для примера
   args = parser.parse_args(['--ignored-providers'] + providers + ['--cookie-browsers'] + browsers_list)
   print(args.ignored_providers, args.cookie_browsers)