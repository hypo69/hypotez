# Модуль `cli`

## Обзор

Модуль `cli` предоставляет интерфейс командной строки для запуска `gpt4free` в режимах API и GUI.

## Детали

Данный модуль используется для запуска `gpt4free` с различными параметрами конфигурации. Он предоставляет два режима запуска: `api` и `gui`.

- Режим `api` запускает API `gpt4free`, который обеспечивает доступ к функциональности модели через HTTP-интерфейс.
- Режим `gui` запускает графический интерфейс `gpt4free`, который позволяет пользователям взаимодействовать с моделью без необходимости использования командной строки.

##  Функции

### `get_api_parser()`

**Цель**: Функция создает объект парсера аргументов командной строки для API `gpt4free`.

**Параметры**:
- Нет

**Возвращает**:
- `ArgumentParser`: Объект парсера аргументов командной строки для API `gpt4free`.

**Описание**:
- Функция создает объект `ArgumentParser`, который используется для обработки аргументов командной строки, переданных при запуске API.
- Она добавляет следующие аргументы:
    - `--bind`: Строка, которая определяет адрес и порт для привязки сервера API.
    - `--port`: Порт для сервера API.
    - `--debug`: Включает подробное логгирование.
    - `--gui`: Запускает GUI в дополнение к API.
    - `--model`: Имя модели для использования по умолчанию.
    - `--provider`: Имя провайдера для использования по умолчанию.
    - `--image-provider`: Имя провайдера для использования по умолчанию для генерации изображений.
    - `--proxy`: Прокси-сервер, который будет использоваться по умолчанию.
    - `--workers`: Количество рабочих потоков для сервера API.
    - `--disable-colors`: Отключает использование цвета в выводе.
    - `--ignore-cookie-files`: Не читает файлы `.har` и `cookie`.
    - `--g4f-api-key`: Устанавливает ключ аутентификации для API.
    - `--ignored-providers`: Список провайдеров, которые будут игнорироваться при обработке запросов.
    - `--cookie-browsers`: Список браузеров, из которых будут извлекаться или к которым будут обращаться файлы cookie.
    - `--reload`: Включает перезагрузку.
    - `--demo`: Включает демо-режим.
    - `--ssl-keyfile`: Путь к файлу с ключом SSL для HTTPS.
    - `--ssl-certfile`: Путь к файлу с сертификатом SSL для HTTPS.
    - `--log-config`: Путь к конфигурационному файлу логгирования.

**Примеры**:
```python
>>> parser = get_api_parser()
>>> parser.parse_args()
Namespace(bind='0.0.0.0:1337', port=None, debug=False, gui=False, model=None, provider=None, image_provider=None, proxy=None, workers=None, disable_colors=False, ignore_cookie_files=False, g4f_api_key=None, ignored_providers=[], cookie_browsers=[], reload=False, demo=False, ssl_keyfile=None, ssl_certfile=None, log_config=None)
```

### `main()`

**Цель**:  Функция является точкой входа для запуска `gpt4free`.

**Параметры**:
- Нет

**Возвращает**:
- Нет

**Описание**:
- Функция создает объект `ArgumentParser`, который используется для обработки аргументов командной строки, переданных при запуске `gpt4free`.
- Она добавляет два подпарсера: `api` и `gui`.
- Подпарсер `api` наследует парсер аргументов для API, созданный функцией `get_api_parser()`.
- Подпарсер `gui` наследует парсер аргументов для GUI, определенный в модуле `gui.run`.
- После обработки аргументов командной строки, функция запускает соответствующий режим: `api` или `gui`.
- Если режим не указан, то выводится справка по доступным режимам.

**Примеры**:
```python
>>> main()
usage: cli.py [-h] {api,gui} ...
cli.py: error: argument mode: invalid choice: 'invalid' (choose from 'api', 'gui')

# Запуск в режиме API:
>>> main()
usage: cli.py [-h] {api,gui} ...
cli.py api [-h] [--bind BIND] [--port PORT] [--debug] [--gui] [--model MODEL] [--provider PROVIDER] ...

# Запуск в режиме GUI:
>>> main()
usage: cli.py [-h] {api,gui} ...
cli.py gui [-h] [--bind BIND] [--port PORT] [--debug] [--gui] [--model MODEL] [--provider PROVIDER] ...
```

### `run_api_args()`

**Цель**: Функция запускает API `gpt4free` с использованием переданных аргументов командной строки.

**Параметры**:
- `args`: Объект `Namespace`, содержащий аргументы командной строки.

**Возвращает**:
- Нет

**Описание**:
- Функция устанавливает конфигурацию API, используя аргументы командной строки.
- Затем она запускает API `gpt4free` с использованием модуля `g4f.api`.

**Примеры**:
```python
>>> run_api_args(Namespace(bind='0.0.0.0:1337', port=None, debug=False, gui=False, model=None, provider=None, image_provider=None, proxy=None, workers=None, disable_colors=False, ignore_cookie_files=False, g4f_api_key=None, ignored_providers=[], cookie_browsers=[], reload=False, demo=False, ssl_keyfile=None, ssl_certfile=None, log_config=None))
# Запуск API gpt4free
```

##  Внутренние функции

Нет.


##  Примеры

**Пример 1**: Запуск API `gpt4free` на порту 1337.

```bash
python cli.py api --port 1337
```

**Пример 2**: Запуск API `gpt4free` в режиме отладки.

```bash
python cli.py api --debug
```

**Пример 3**: Запуск API `gpt4free` с использованием провайдера `GPT4Free` и модели `gpt-3.5-turbo`.

```bash
python cli.py api --provider GPT4Free --model gpt-3.5-turbo
```

##  Использование

Модуль `cli` предоставляет простой способ запуска `gpt4free` в режимах API и GUI. Вы можете использовать этот модуль для настройки и запуска `gpt4free` с различными параметрами конфигурации.

```python
# Запуск API gpt4free в режиме отладки.
python cli.py api --debug
```

```python
# Запуск API gpt4free с использованием провайдера GPT4Free и модели gpt-3.5-turbo.
python cli.py api --provider GPT4Free --model gpt-3.5-turbo
```

```python
# Запуск API gpt4free в демо-режиме.
python cli.py api --demo
```

```python
# Запуск GUI gpt4free.
python cli.py gui
```

**Пример работы с драйвером webdriver:**

```python
from src.webdirver import Driver, Chrome, Firefox, Playwright

driver = Driver(Chrome)
```