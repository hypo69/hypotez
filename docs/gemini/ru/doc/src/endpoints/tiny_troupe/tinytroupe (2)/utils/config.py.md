# Модуль конфигурации TinyTroupe
## Обзор

Модуль `config.py` предназначен для управления конфигурацией приложения TinyTroupe. Он обеспечивает чтение параметров конфигурации из файлов `config.ini`, как из местоположения по умолчанию, так и из пользовательского расположения (если таковое имеется). Модуль также содержит функции для логирования и вывода текущей конфигурации.

## Подробней

Модуль отвечает за загрузку и предоставление доступа к параметрам конфигурации, необходимым для работы приложения TinyTroupe. Он использует библиотеку `configparser` для чтения `.ini` файлов и предоставляет функции для получения значений параметров конфигурации. Расположение файла в проекте: `hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/utils/config.py`

## Функции

### `read_config_file`

```python
def read_config_file(use_cache: bool = True, verbose: bool = True) -> configparser.ConfigParser:
    """
    Читает параметры конфигурации из файла config.ini.

    Args:
        use_cache (bool, optional): Использовать ли кэшированную конфигурацию, если она существует. По умолчанию True.
        verbose (bool, optional): Выводить ли отладочные сообщения. По умолчанию True.

    Returns:
        configparser.ConfigParser: Объект ConfigParser, содержащий параметры конфигурации.

    Raises:
        ValueError: Если не удается найти файл конфигурации по умолчанию.

    Как работает функция:
    - Проверяет, существует ли кэшированная конфигурация `_config` и допустимо ли ее использование. Если да, возвращает кэшированную конфигурацию.
    - Если кэшированная конфигурация отсутствует или ее использование не разрешено, создает новый объект `configparser.ConfigParser`.
    - Считывает значения по умолчанию из файла `config.ini`, расположенного в каталоге модуля.
    - Пытается переопределить значения по умолчанию значениями из файла `config.ini`, расположенного в текущем рабочем каталоге.
    - Возвращает объект `configparser.ConfigParser` с параметрами конфигурации.

    Примеры:
        >>> config = read_config_file()
        >>> type(config)
        <class 'configparser.ConfigParser'>
    """
```

### `pretty_print_config`

```python
def pretty_print_config(config: configparser.ConfigParser) -> None:
    """
    Выводит текущую конфигурацию в удобочитаемом формате.

    Args:
        config (configparser.ConfigParser): Объект ConfigParser, содержащий параметры конфигурации.

    Returns:
        None

    Как работает функция:
    - Перебирает все секции в объекте `config`.
    - Для каждой секции выводит ее имя.
    - Перебирает все параметры в каждой секции и выводит их в формате "ключ = значение".

    Примеры:
        >>> config = read_config_file()
        >>> pretty_print_config(config)
        =================================
        Current TinyTroupe configuration 
        =================================
        [Section1]
        key1 = value1
        key2 = value2

        [Section2]
        key3 = value3
        ...
    """
```

### `start_logger`

```python
def start_logger(config: configparser.ConfigParser) -> None:
    """
    Инициализирует логгер для приложения TinyTroupe.

    Args:
        config (configparser.ConfigParser): Объект ConfigParser, содержащий параметры конфигурации.

    Returns:
        None

    Как работает функция:
    - Создает логгер с именем "tinytroupe".
    - Определяет уровень логирования из конфигурации (секция "Logging", параметр "LOGLEVEL"). Если параметр не указан, использует уровень INFO по умолчанию.
    - Создает обработчик консоли (logging.StreamHandler) и устанавливает для него уровень логирования.
    - Создает форматтер (logging.Formatter) для сообщений лога.
    - Добавляет форматтер к обработчику консоли.
    - Добавляет обработчик консоли к логгеру.

    Примеры:
        >>> config = read_config_file()
        >>> start_logger(config)
    """