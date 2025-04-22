## Анализ кода модуля `src.logger`

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структурированность документации.
  - Описание всех основных классов и функций модуля.
  - Наличие примеров использования.
- **Минусы**:
  - Документация представлена в формате Markdown, но отсутствует docstring в самом коде.
  - Нет информации об использовании SingletonMeta и JsonFormatter в примерах.
  - Некоторые параметры функций описаны недостаточно подробно.
  - Нет описания зависимостей, например, `colorama`.

**Рекомендации по улучшению:**

1. **Добавить docstring в код**:
   - Добавить docstring ко всем классам, функциям и методам в самом файле `src.logger`.

2. **Расширить примеры использования**:
   - Добавить примеры использования `SingletonMeta` и `JsonFormatter`, чтобы показать, как их можно применять на практике.

3. **Детализировать описание параметров**:
   - Улучшить описание параметров функций, указав возможные значения и типы данных более явно. Например, для параметра `level` указать, что это может быть `logging.DEBUG`, `logging.INFO` и т.д.

4. **Добавить информацию о зависимостях**:
   - Указать в документации, что для использования цветов необходимо установить библиотеку `colorama`.

5. **Перевести документацию на русский язык**:
   - Создать версию документации на русском языке, чтобы облегчить понимание модуля для русскоязычных разработчиков.

6. **Улучшить форматирование**:
   - Проверить и исправить форматирование Markdown, чтобы улучшить читаемость.

**Оптимизированный код:**

```markdown
## \file src/logger/README.MD
# -*- coding: utf-8 -*-

```rst
 .. module:: src.logger
```

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/README.MD'>src</A> /

</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/logger/readme.ru.md'>Русский</A>
</TD>
</TABLE>

### Documentation for the `src.logger` Module

Модуль `src.logger` предоставляет гибкую систему логирования, поддерживающую вывод в консоль, файлы и JSON формат.
Он использует Singleton паттерн для гарантии, что только один экземпляр логгера используется во всем приложении.
Логгер поддерживает различные уровни логирования (например, `INFO`, `ERROR`, `DEBUG`) и включает цветной вывод для консольных логов.
Можно настраивать форматы вывода логов и управлять записью в разные файлы.

---

### Classes:

- **SingletonMeta**: Метакласс, реализующий Singleton паттерн для логгера.
- **JsonFormatter**: Пользовательский форматтер, выводящий логи в JSON формате.
- **Logger**: Основной класс логгера, поддерживающий вывод в консоль, файлы и JSON формат.

---

### Functions:

#### `__init__`

Инициализирует экземпляр Logger, создавая placeholders для разных типов логгеров (консольный, файловый и JSON).

#### `_configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger`

Конфигурирует и возвращает экземпляр логгера.

**Parameters:**
- `name` (str): Имя логгера.
- `log_path` (str): Путь к файлу логов.
- `level` (Optional[int]): Уровень логирования, например, `logging.DEBUG`. По умолчанию `logging.DEBUG`.
- `formatter` (Optional[logging.Formatter]): Пользовательский форматтер (опционально).
- `mode` (Optional[str]): Режим файла, например, `'a'` для добавления (по умолчанию).

**Returns**: Configured `logging.Logger` instance.

#### `initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = '')`

Инициализирует логгеры для консоли и файлов (info, debug, error и JSON).

**Parameters:**
- `info_log_path` (Optional[str]): Путь к файлу info логов (опционально).
- `debug_log_path` (Optional[str]): Путь к файлу debug логов (опционально).
- `errors_log_path` (Optional[str]): Путь к файлу error логов (опционально).
- `json_log_path` (Optional[str]): Путь к файлу JSON логов (опционально).

#### `log(level, message, ex=None, exc_info=False, color=None)`

Записывает сообщение на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с опциональным исключением и цветовым форматированием.

**Parameters:**
- `level`: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
- `message`: Сообщение лога.
- `ex`: Опциональное исключение для записи.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `color`: Кортеж с цветами текста и фона для вывода в консоль (опционально).

#### `info(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`

Записывает информационное сообщение.

**Parameters:**
- `message`: Информационное сообщение для записи.
- `ex`: Опциональное исключение для записи.
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `colors`: Кортеж значений цвета для сообщения (опционально).

#### `success(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`

Записывает сообщение об успехе.

**Parameters**:\
- Аналогично `info`.

#### `warning(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`

Записывает предупреждающее сообщение.

**Parameters**:\
- Аналогично `info`.

#### `debug(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`

Записывает отладочное сообщение.

**Parameters**:\
- Аналогично `info`.

#### `error(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`

Записывает сообщение об ошибке.

**Parameters**:\
- Аналогично `info`.

#### `critical(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`

Записывает критическое сообщение.

**Parameters**:\
- Аналогично `info`.

---

### Parameters for the Logger

Класс `Logger` принимает несколько опциональных параметров для настройки поведения логирования.

- **Level**: Управляет серьезностью записываемых логов. Общие уровни включают:
  - `logging.DEBUG`: Детальная информация, полезная для диагностики проблем.
  - `logging.INFO`: Общая информация, например, об успешных операциях.
  - `logging.WARNING`: Предупреждения, которые не обязательно требуют немедленных действий.
  - `logging.ERROR`: Сообщения об ошибках.
  - `logging.CRITICAL`: Критические ошибки, требующие немедленного внимания.

- **Formatter**: Определяет, как форматируются сообщения логов. По умолчанию сообщения форматируются как `'%(asctime)s - %(levelname)s - %(message)s'`.
  Можно предоставить пользовательский форматтер для различных форматов, таких как JSON.

- **Color**: Цвета для сообщений логов в консоли. Цвета указываются в виде кортежа с двумя элементами:
  - **Text color**: Указывает цвет текста (например, `colorama.Fore.RED`).
  - **Background color**: Указывает цвет фона (например, `colorama.Back.WHITE`).

Цвет можно настроить для разных уровней логов (например, зеленый для info, красный для error и т.д.).
Для использования цветов необходимо установить библиотеку `colorama`.

---

### File Logging Configuration (`config`)

Для записи сообщений в файл можно указать пути к файлам в конфигурации.

```python
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
```

Пути к файлам, указанные в `config`, используются для записи логов в соответствующие файлы для каждого уровня логов.

---

### Example Usage

#### 1. Initializing the Logger:

```python
from src.logger import Logger # corrected import
import colorama # added import for colorama

logger: Logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
```

#### 2. Logging Messages at Different Levels:

```python
logger.info('This is an info message')
logger.success('This is a success message')
logger.warning('This is a warning message')
logger.debug('This is a debug message')
logger.error('This is an error message')
logger.critical('This is a critical message')
```

#### 3. Customizing Colors:

```python
logger.info('This message will be green', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('This message will have a red background', colors=(colorama.Fore.WHITE, colorama.Back.RED))
```

---

Этот модуль предоставляет всестороннюю и гибкую систему логирования для Python приложений.
Можно настраивать вывод в консоль и файлы с разными форматами и цветами, управлять уровнями логирования и обрабатывать исключения.
Конфигурация для файлового логирования хранится в словаре `config`, что позволяет легко настраивать параметры.