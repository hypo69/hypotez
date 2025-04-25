# Модуль логгера

## Обзор

Модуль `src.logger.logger` предоставляет централизованный механизм для ведения журналов в проекте `hypotez`. Он обеспечивает функциональность записи логов в консоль, в файлы и в формате JSON. Модуль реализует паттерн Singleton, гарантируя, что будет только один экземпляр логгера в течение всего приложения. 

## Подробнее

Модуль использует стандартную библиотеку `logging` для ведения журналов. Он также использует библиотеку `colorama` для вывода цветных сообщений в консоль, что повышает читаемость логов. 

### Логирование в консоль

Логгер выводит сообщения в консоль, используя стандартный обработчик `StreamHandler` из библиотеки `logging`. Уровень логирования по умолчанию установлен на `DEBUG`, что означает, что все сообщения, включая `DEBUG`, `INFO`, `WARNING`, `ERROR` и `CRITICAL`, будут выводиться в консоль.

### Логирование в файлы

Логгер записывает сообщения в отдельные файлы для различных уровней логирования:
- `info.log`: Сообщения уровня `INFO` и выше.
- `debug.log`: Сообщения уровня `DEBUG` и выше.
- `errors.log`: Сообщения уровня `ERROR` и выше.

### Логирование в JSON

Логгер также может записывать сообщения в файл в формате JSON.  Файл JSON будет содержать информацию о дате и времени, уровне логирования, тексте сообщения и, при необходимости, информацию об исключении.

## Классы

### `class SingletonMeta`

**Описание**: Метакласс для реализации паттерна Singleton. Гарантирует, что будет только один экземпляр класса `Logger`.

**Наследует**: `type`

**Атрибуты**:
- `_instances (dict)`: Словарь, хранящий экземпляры классов.
- `_lock (threading.Lock)`: Объект блокировки для обеспечения потокобезопасности при создании экземпляра класса.


### `class JsonFormatter`

**Описание**: Кастомный форматтер для вывода сообщений в JSON.

**Наследует**: `logging.Formatter`

**Методы**:

- `format(record: logging.LogRecord) -> str`: Форматирует запись лога в формате JSON.

### `class Logger`

**Описание**: Класс `Logger` реализует паттерн Singleton. 
Он обеспечивает запись логов в консоль, в файлы и в формате JSON.

**Наследует**: `SingletonMeta`

**Атрибуты**:
- `log_files_path (Path)`: Путь к каталогу, где хранятся файлы логов.
- `info_log_path (Path)`: Путь к файлу `info.log`.
- `debug_log_path (Path)`: Путь к файлу `debug.log`.
- `errors_log_path (Path)`: Путь к файлу `errors.log`.
- `json_log_path (Path)`: Путь к файлу JSON.


**Методы**:

- `__init__(self, info_log_path: Optional[str] = None, debug_log_path: Optional[str] = None, errors_log_path: Optional[str] = None, json_log_path: Optional[str] = None)`: Инициализирует экземпляр `Logger`.  
    - Задает пути к файлам логов.
    - Создает каталог для файлов логов, если он не существует.
    - Создает файлы логов, если они не существуют.
    - Инициализирует логгеры для консоли и файлов.
    - Инициализирует форматтер для JSON-логов.


- `_format_message(self, message: str, ex: Optional[Exception] = None, color: Optional[Tuple[str, str]] = None, level: Optional[int] = None) -> str`: Форматирует сообщение лога, добавляя цвет, символ уровня и информацию об исключении (при необходимости).


- `_ex_full_info(self, ex: Optional[Exception] = None) -> str`: Возвращает полную информацию об исключении, включая имя файла, имя функции, номер строки и текст исключения.


- `log(self, level: int, message: str, ex: Optional[Exception] = None, exc_info: bool = False, color: Optional[Tuple[str, str]] = None) -> None`:  Записывает сообщение в лог с заданным уровнем и с дополнительными параметрами.

- `info(self, message: str, ex: Optional[Exception] = None, exc_info: bool = False, text_color: str = "green", bg_color: str = "") -> None`:  Записывает информационное сообщение в лог.

- `success(self, message: str, ex: Optional[Exception] = None, exc_info: bool = False, text_color: str = "yellow", bg_color: str = "") -> None`:  Записывает сообщение об успешном завершении операции в лог.

- `warning(self, message: str, ex: Optional[Exception] = None, exc_info: bool = False, text_color: str = "light_red", bg_color: str = "") -> None`:  Записывает предупреждение в лог.

- `debug(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = "cyan", bg_color: str = "") -> None`:  Записывает отладочное сообщение в лог.

- `exception(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = "cyan", bg_color: str = "light_gray") -> None`:  Записывает сообщение об исключении в лог.

- `error(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = "red", bg_color: str = "") -> None`:  Записывает сообщение об ошибке в лог.

- `critical(self, message: str, ex: Optional[Exception] = None, exc_info: bool = True, text_color: str = "red", bg_color: str = "white") -> None`:  Записывает критическое сообщение в лог.

## Примеры

### Использование `Logger`

```python
from src.logger import logger

# Запись информационного сообщения
logger.info("Начинаем обработку данных")

# Запись сообщения об успешном завершении
logger.success("Обработка данных завершена успешно")

# Запись предупреждения
logger.warning("Обнаружено предупреждение")

# Запись сообщения об ошибке
try:
    # ... Код, который может вызвать ошибку
except Exception as ex:
    logger.error("Ошибка при обработке данных", ex, exc_info=True)

# Запись отладочного сообщения
logger.debug("Проверка значения переменной x: ", x)

# Запись критического сообщения
logger.critical("Критическая ошибка!")
```

### Изменение цвета и фона сообщений

```python
# Запись сообщения с зеленым текстом
logger.info("Начинаем обработку данных", text_color="green")

# Запись сообщения с желтым текстом на красном фоне
logger.warning("Обнаружено предупреждение", text_color="yellow", bg_color="red")

# Запись сообщения с красным текстом на белом фоне
logger.error("Ошибка при обработке данных", text_color="red", bg_color="white")