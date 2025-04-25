# Модуль `gui_parser`

## Обзор

Модуль `gui_parser`  предоставляет функцию `gui_parser()`, которая создает объект `ArgumentParser` для парсинга аргументов командной строки, необходимых для запуска графического интерфейса (GUI) приложения. 

## Подробнее

`gui_parser()`  используется для настройки аргументов командной строки, которые определяют поведение графического интерфейса. 

## Функции

### `gui_parser()`

**Назначение**: Создает объект `ArgumentParser` для парсинга аргументов командной строки для запуска GUI приложения.

**Параметры**: 

- Отсутствуют.

**Возвращает**: 

- `ArgumentParser`: Объект `ArgumentParser`, который можно использовать для парсинга аргументов командной строки.

**Вызывает исключения**:

- Отсутствуют.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.gui.gui_parser import gui_parser

parser = gui_parser()
args = parser.parse_args()

# Доступ к аргументам через `args`
print(args.host)  # выводит "0.0.0.0" по умолчанию
print(args.port)  # выводит 8080 по умолчанию
print(args.debug)  # выводит False по умолчанию
```

**Как работает функция**:

1. Функция `gui_parser()`  инициализирует объект `ArgumentParser` с описанием "Запуск GUI".
2. Она добавляет следующие аргументы:
    - `--host`:  хост, по умолчанию "0.0.0.0".
    - `--port` или `-p`:  порт, по умолчанию 8080.
    - `--debug` или `-d`:  включить режим отладки, по умолчанию False.
    - `--ignore-cookie-files`:  игнорировать файлы .har и cookie, по умолчанию False.
    - `--ignored-providers`:  список провайдеров, которые нужно игнорировать при обработке запросов.
    - `--cookie-browsers`:  список браузеров, из которых нужно получить cookies.
3. Функция возвращает объект `ArgumentParser`.

**Внутренние функции**: 

- Отсутствуют.

**Примеры**: 

- Запуск GUI с хостом "localhost" и портом 8081:
    ```bash
    python your_script.py --host localhost --port 8081
    ```
- Запуск GUI с включенным режимом отладки:
    ```bash
    python your_script.py --debug
    ```
- Запуск GUI с игнорированием файлов .har и cookie:
    ```bash
    python your_script.py --ignore-cookie-files
    ```

**Примеры**:

- Запуск с использованием аргумента `--ignored-providers`:
    ```bash
    python your_script.py --ignored-providers Google Bing  # Игнорирует провайдеров Google и Bing
    ```

- Запуск с использованием аргумента `--cookie-browsers`:
    ```bash
    python your_script.py --cookie-browsers Chrome Firefox  # Использует cookies из Chrome и Firefox
    ```


## Параметры класса

- Отсутствуют.

```markdown