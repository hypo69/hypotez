# Модуль `cli.py`

## Обзор

Модуль `cli.py` является точкой входа для запуска `gpt4free` в различных режимах: API и GUI (графический интерфейс). Он определяет аргументы командной строки и запускает соответствующий режим работы.

## Более подробно

Этот модуль предоставляет интерфейс командной строки для запуска API или графического интерфейса `gpt4free`. Он использует `argparse` для обработки аргументов командной строки и запускает API или GUI с соответствующими параметрами. Поддерживается настройка различных параметров, таких как привязка, порт, режим отладки, модель, провайдер и другие.

## Функции

### `get_api_parser`

```python
def get_api_parser() -> ArgumentParser:
    """
    Создает парсер аргументов для режима API.

    Returns:
        ArgumentParser: Парсер аргументов для режима API.
    """
```

**Назначение**:
Функция создает и настраивает парсер аргументов командной строки для режима API.

**Возвращает**:
- `ArgumentParser`: Объект парсера аргументов, настроенный для обработки аргументов, специфичных для API.

**Как работает**:
- Создает экземпляр `ArgumentParser` с описанием "Run the API and GUI".
- Добавляет аргументы, такие как `--bind`, `--port`, `--debug`, `--gui`, `--model`, `--provider`, `--image-provider`, `--proxy`, `--workers`, `--disable-colors`, `--ignore-cookie-files`, `--g4f-api-key`, `--ignored-providers`, `--cookie-browsers`, `--reload`, `--demo`, `--ssl-keyfile`, `--ssl-certfile`, и `--log-config`.
- Устанавливает типы, значения по умолчанию и подсказки для каждого аргумента.

**Пример использования**:
```python
parser = get_api_parser()
args = parser.parse_args(['--port', '8080', '--debug'])
print(args.port)  # Вывод: 8080
print(args.debug)  # Вывод: True
```

### `main`

```python
def main() -> None:
    """
    Основная функция для запуска gpt4free.
    """
```

**Назначение**:
Основная функция, которая анализирует аргументы командной строки и запускает соответствующий режим (`api` или `gui`).

**Как работает**:
- Создает основной парсер аргументов с помощью `argparse.ArgumentParser`.
- Добавляет подпарсеры для режимов `api` и `gui`, используя `get_api_parser()` и `gui_parser()` соответственно.
- Анализирует аргументы командной строки с помощью `parser.parse_args()`.
- В зависимости от режима, запускает `run_api_args()` или `run_gui_args()`.
- Если режим не указан, выводит справку и завершает программу.

**Пример использования**:
```python
# Пример запуска API с аргументами (в реальном коде аргументы передаются через командную строку)
import sys
sys.argv = ['cli.py', 'api', '--port', '8080', '--debug']
main()
```

### `run_api_args`

```python
def run_api_args(args: argparse.Namespace) -> None:
    """
    Запускает API с заданными аргументами.

    Args:
        args (argparse.Namespace): Аргументы командной строки.
    """
```

**Назначение**:
Функция для запуска API с заданными аргументами.

**Параметры**:
- `args` (`argparse.Namespace`): Аргументы командной строки, переданные из функции `main`.

**Как работает**:
- Импортирует `AppConfig` и `run_api` из `g4f.api`.
- Устанавливает конфигурацию `AppConfig` на основе аргументов командной строки, таких как `ignore_cookie_files`, `ignored_providers`, `g4f_api_key`, `provider`, `image_provider`, `proxy`, `model`, `gui` и `demo`.
- Если указаны браузеры для cookie, обновляет список `g4f.cookies.browsers`.
- Запускает API с помощью `run_api()`, передавая аргументы, такие как `bind`, `port`, `debug`, `workers`, `use_colors`, `reload`, `ssl_keyfile`, `ssl_certfile` и `log_config`.

**Пример использования**:
```python
# Пример вызова run_api_args с аргументами (в реальном коде аргументы передаются через командную строку)
import argparse
from argparse import Namespace
# Создаем Namespace с необходимыми аргументами
args = Namespace(ignore_cookie_files=True, ignored_providers=[], g4f_api_key=None, provider=None, image_provider=None, proxy=None, model=None, gui=None, demo=False, cookie_browsers=[], bind=None, port=8080, debug=True, workers=None, disable_colors=False, reload=False, ssl_keyfile=None, ssl_certfile=None, log_config=None)
run_api_args(args)