## \file /hypotez/src/logger/README.MD
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module::  src.logger
:platform: Windows, Unix
:synopsis: Модуль с системой логгирования для проекта.

Модуль `src.logger` предоставляет гибкую систему логгирования, которая 
поддерживает запись логов в консоль, файлы и JSON. 
Используется паттерн Singleton для обеспечения единого экземпляра 
логгера во всем приложении.  
Логгер поддерживает различные уровни записи логов (например, INFO, ERROR, DEBUG) 
и включает цветное форматирование для консольных логов.  
Вы также можете настроить форматы вывода логов и управлять записью 
логов в разные файлы.

---

### Классы:

- **SingletonMeta**: Метакласс, реализующий паттерн Singleton для логгера.
- **JsonFormatter**:  Настраиваемый форматтер, выводящий логи в формате JSON.
- **Logger**: Главный класс логгера, который поддерживает логгирование 
  в консоль, файлы и JSON.

---

### Функции:

#### `__init__`
Инициализирует экземпляр логгера с заполнителями для разных типов 
логгеров (консоль, файл и JSON).

#### `_configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger`
Настраивает и возвращает экземпляр логгера.

**Параметры:**

- `name`: Имя логгера.
- `log_path`: Путь к файлу лога.
- `level`: Уровень логирования, например, `logging.DEBUG`. По умолчанию `logging.DEBUG`.
- `formatter`: Настраиваемый форматтер (необязательно).
- `mode`: Режим файла, например, `'a'` для добавления (по умолчанию).

**Возвращает**: Настроенный экземпляр `logging.Logger`.

#### `initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = '')`
Инициализирует логгеры для консольного и файлового логирования 
(info, debug, error и JSON).

**Параметры:**

- `info_log_path`: Путь к файлу лога для info-сообщений (необязательно).
- `debug_log_path`: Путь к файлу лога для debug-сообщений (необязательно).
- `errors_log_path`: Путь к файлу лога для error-сообщений (необязательно).
- `json_log_path`: Путь к файлу лога для JSON (необязательно).

#### `log(level, message, ex=None, exc_info=False, color=None)`
Записывает сообщение в лог на указанном уровне (например, INFO, DEBUG, ERROR) 
с дополнительным исключением и форматированием цвета.

**Параметры:**

- `level`: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
- `message`: Сообщение для записи в лог.
- `ex`: Дополнительное исключение для записи в лог (необязательно).
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `color`: Кортеж с текстом и фоновыми цветами для вывода в консоль 
  (необязательно).

#### `info(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`
Записывает информационное сообщение в лог.

**Параметры:**

- `message`: Информационное сообщение для записи в лог.
- `ex`: Дополнительное исключение для записи в лог (необязательно).
- `exc_info`: Включать ли информацию об исключении (по умолчанию `False`).
- `colors`: Кортеж значений цветов для сообщения (необязательно).

#### `success(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`
Записывает сообщение об успехе в лог.

**Параметры**:

- Те же, что и для `info`.

#### `warning(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`
Записывает предупреждающее сообщение в лог.

**Параметры**:

- Те же, что и для `info`.

#### `debug(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`
Записывает отладочное сообщение в лог.

**Параметры**:

- Те же, что и для `info`.

#### `error(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`
Записывает сообщение об ошибке в лог.

**Параметры**:

- Те же, что и для `info`.

#### `critical(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`
Записывает критическое сообщение в лог.

**Параметры**:

- Те же, что и для `info`.

---

### Параметры логгера

Класс `Logger` принимает несколько дополнительных параметров для 
настройки поведения логгирования.

- **Level**: Управляет серьезностью записываемых в лог сообщений. 
  Общие уровни включают:

  - `logging.DEBUG`: Детальная информация, полезная для диагностики проблем.
  - `logging.INFO`: Общая информация, например, об успешных операциях.
  - `logging.WARNING`: Предупреждения, которые не обязательно требуют 
    немедленных действий.
  - `logging.ERROR`: Сообщения об ошибках.
  - `logging.CRITICAL`: Критические ошибки, требующие немедленного 
    внимания.

- **Formatter**: Определяет, как форматируются сообщения в логах. 
  По умолчанию сообщения форматируются как `'%(asctime)s - %(levelname)s - %(message)s'`. 
  Вы можете предоставить свой собственный форматтер для разных форматов, 
  например, JSON.

- **Color**: Цвета для сообщений в логах в консоли. Цвета 
  указываются как кортеж с двумя элементами:

  - **Text color**: Определяет цвет текста (например, `colorama.Fore.RED`).
  - **Background color**: Определяет цвет фона 
    (например, `colorama.Back.WHITE`).

Цвет можно настроить для разных уровней логирования 
(например, зеленый для info, красный для ошибок и т.д.).

---

### Настройка файлового логирования (`config`)
Чтобы записывать сообщения в лог в файл, вы можете указать пути к файлам 
в конфигурации.

```python
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
```

Пути к файлам, указанные в `config`, используются для записи логов 
в соответствующие файлы для каждого уровня логирования.

---

### Пример использования

#### 1. Инициализация логгера:

```python
logger: Logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
```

#### 2. Запись сообщений в лог на разных уровнях:

```python
logger.info('Это информационное сообщение')
logger.success('Это сообщение об успехе')
logger.warning('Это предупреждающее сообщение')
logger.debug('Это отладочное сообщение')
logger.error('Это сообщение об ошибке')
logger.critical('Это критическое сообщение')
```

#### 3. Настройка цветов:

```python
logger.info('Это сообщение будет зеленым', 
          colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('Это сообщение будет иметь красный фон', 
           colors=(colorama.Fore.WHITE, colorama.Back.RED))
```

---

Этот модуль предоставляет всестороннюю и гибкую систему 
логгирования для приложений Python. 
Вы можете настроить консольное и файловое логирование с 
разными форматами и цветами, управлять уровнями 
логгирования и корректно обрабатывать исключения. 
Конфигурация для файлового логирования хранится в 
словаре `config`, что позволяет легко ее настраивать.
"""

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/README.MD'>src</A> /\n\n</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/logger/readme.ru.md'>Русский</A>
</TD>
</TABLE>